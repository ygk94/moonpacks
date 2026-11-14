//! SHA-256 incrémental, dont l'état intermédiaire est stocké entre deux transactions.
//!
//! `table_hash = sha256(serde_json::to_vec(table))` reste la définition du hash. Pour une grosse
//! table chargée par lots, hacher 1,7 Mo de JSON d'un coup à l'ouverture coûterait près de
//! 300 Tgas (mesuré). On hache donc au fil du chargement : l'en-tête jusqu'à `"cards":[` à la
//! création, chaque carte à son ajout, puis la fin de l'en-tête (`],"mythics":…}`) à l'ouverture.
//! Le résultat est identique octet pour octet, ce que vérifient les tests. Le contrat ne recalcule
//! jamais le hash d'une grosse table : le vérificateur la relit page par page et le recalcule.

// `compress256` de sha2 0.10 prend des `GenericArray` (marqués obsolètes par generic-array 0.14.9).
#![allow(deprecated)]

use near_sdk::near;
use sha2::digest::generic_array::GenericArray;

const H0: [u32; 8] = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
];

#[near(serializers = [borsh])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Sha256Stream {
    state: [u32; 8],
    /// Octets en attente (moins de 64).
    buf: Vec<u8>,
    /// Longueur totale hachée, en octets.
    len: u64,
}

impl Default for Sha256Stream {
    fn default() -> Self {
        Self { state: H0, buf: Vec::new(), len: 0 }
    }
}

impl Sha256Stream {
    pub fn update(&mut self, mut data: &[u8]) {
        self.len += data.len() as u64;
        if !self.buf.is_empty() {
            let take = (64 - self.buf.len()).min(data.len());
            self.buf.extend_from_slice(&data[..take]);
            data = &data[take..];
            if self.buf.len() < 64 {
                return;
            }
            let block = GenericArray::clone_from_slice(&self.buf);
            sha2::compress256(&mut self.state, &[block]);
            self.buf.clear();
        }
        let full = data.len() / 64 * 64;
        if full > 0 {
            let blocks: Vec<_> = data[..full].chunks_exact(64).map(GenericArray::clone_from_slice).collect();
            sha2::compress256(&mut self.state, &blocks);
        }
        self.buf.extend_from_slice(&data[full..]);
    }

    pub fn finalize(mut self) -> [u8; 32] {
        let bits = self.len.wrapping_mul(8);
        let mut pad = vec![0x80u8];
        let rem = (self.buf.len() + 1) % 64;
        pad.resize(1 + if rem <= 56 { 56 - rem } else { 120 - rem }, 0);
        pad.extend_from_slice(&bits.to_be_bytes());
        let len = self.len;
        self.update(&pad);
        self.len = len;
        debug_assert!(self.buf.is_empty());
        let mut out = [0u8; 32];
        for (i, w) in self.state.iter().enumerate() {
            out[4 * i..4 * i + 4].copy_from_slice(&w.to_be_bytes());
        }
        out
    }
}

/// Clé du tableau des cartes dans le JSON de la table.
pub const CARDS_KEY: &[u8] = b"\"cards\":[";

/// Sérialisation JSON de l'en-tête (table sans cartes) coupée autour du tableau `cards` :
/// `table_json = avant || cartes séparées par "," || après`.
pub fn header_json_parts(header: &crate::types::SeriesTable) -> (Vec<u8>, Vec<u8>) {
    assert!(header.cards.is_empty(), "en-tête sans cartes attendu");
    let bytes = near_sdk::serde_json::to_vec(header).unwrap_or_else(|_| near_sdk::env::panic_str("E_INTERNAL: JSON impossible"));
    split_at_cards(&bytes)
}

/// Coupe le JSON d'un en-tête juste après `"cards":[`. Panique si le motif n'apparaît pas
/// **exactement une fois**, ou si le tableau qui suit n'est pas vide (`]`).
///
/// Aujourd'hui le motif ne peut apparaître qu'une fois : les chaînes (nom, engagements, comptes)
/// ont leurs `"` échappés, donc `"cards":[` ne peut pas naître à l'intérieur d'une valeur. Le
/// contrôle rend cette propriété explicite : un champ ajouté plus tard qui la casserait fait
/// paniquer la création au lieu de produire un hash faux.
pub fn split_at_cards(bytes: &[u8]) -> (Vec<u8>, Vec<u8>) {
    let mut hits = bytes.windows(CARDS_KEY.len()).enumerate().filter(|(_, w)| *w == CARDS_KEY).map(|(i, _)| i);
    let pos = hits.next().unwrap_or_else(|| near_sdk::env::panic_str("E_INTERNAL: Champ cards introuvable"));
    if hits.next().is_some() {
        near_sdk::env::panic_str("E_TABLE_FORMAT: Motif \"cards\":[ présent plusieurs fois dans l'en-tête");
    }
    let cut = pos + CARDS_KEY.len();
    if bytes.get(cut) != Some(&b']') {
        near_sdk::env::panic_str("E_INTERNAL: En-tête : tableau cards non vide");
    }
    (bytes[..cut].to_vec(), bytes[cut..].to_vec())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::types::*;
    use near_sdk::json_types::U128;

    #[test]
    fn stream_matches_one_shot_sha256() {
        let data: Vec<u8> = (0..2_000u32).map(|i| (i * 7 + i / 3) as u8).collect();
        for split in [0usize, 1, 55, 56, 63, 64, 65, 119, 120, 128, 1000, 1999, 2000] {
            for total in [0usize, 1, 55, 56, 57, 63, 64, 65, 127, 128, 129, 1999, 2000] {
                if split > total {
                    continue;
                }
                let mut s = Sha256Stream::default();
                s.update(&data[..split]);
                // découpage irrégulier du reste
                let mut rest = &data[split..total];
                let mut k = 1;
                while !rest.is_empty() {
                    let n = k.min(rest.len());
                    s.update(&rest[..n]);
                    rest = &rest[n..];
                    k = k * 3 + 1;
                }
                assert_eq!(s.finalize(), near_sdk::env::sha256_array(&data[..total]), "split {split} total {total}");
            }
        }
    }

    fn header() -> SeriesTable {
        SeriesTable {
            kinds: None,
            // Nom piégé : contient le motif, échappé par serde.
            name: "x\"cards\":[y".into(),
            price: U128(7),
            cards_per_pack: 3,
            rarity_weights: RarityWeights { mythic: 1, legendary: 2, epic: 3, rare: 4, common: 5 },
            cards: vec![],
            mythics: vec![MythicCommitment { commitment: "a".repeat(64), content_hash: "b".repeat(64), weight: 1, cap: 2 }],
            royalties: vec![Royalty { account_id: "r.near".parse().unwrap(), bps: 10 }],
            mechanics: None,
        }
    }

    /// Verrou de l'ordre des champs de `SeriesTable` (et de ses sous-types) : le hash, la coupe de
    /// l'en-tête et `canon.py` du vérificateur en dépendent. Ajouter, retirer ou déplacer un champ
    /// casse ce test ; il faut alors mettre à jour `canon.py` et la coupe en connaissance de cause.
    #[test]
    fn series_table_field_order_is_locked() {
        let mut t = header();
        t.cards.push(CardDef {
            card_id: "c".into(),
            title: "C".into(),
            rarity: Rarity::Common,
            weight: 1,
            cap: None,
            media: Some("m".into()),
            reference: None,
            backing: Some(Backing { asset_id: "a".into(), amount: U128(9) }),
        });
        let json = String::from_utf8(near_sdk::serde_json::to_vec(&t).unwrap()).unwrap();
        assert_eq!(
            json,
            concat!(
                r#"{"name":"x\"cards\":[y","price":"7","cards_per_pack":3,"#,
                r#""rarity_weights":{"mythic":1,"legendary":2,"epic":3,"rare":4,"common":5},"#,
                r#""cards":[{"card_id":"c","title":"C","rarity":"common","weight":1,"cap":null,"media":"m","reference":null,"backing":{"asset_id":"a","amount":"9"}}],"#,
                r#""mythics":[{"commitment":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","content_hash":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","weight":1,"cap":2}],"#,
                r#""royalties":[{"account_id":"r.near","bps":10}]}"#,
            )
        );
        // La coupe retombe sur la table complète.
        let (before, after) = header_json_parts(&header());
        let card = near_sdk::serde_json::to_vec(&t.cards[0]).unwrap();
        assert_eq!([before, card, after].concat(), json.into_bytes());
    }

    /// Avec des mécaniques : le champ `mechanics` vient en dernier, ses sous-champs dans cet ordre,
    /// et la coupe de l'en-tête retombe toujours sur la table complète. Sans mécanique, le champ
    /// est absent (test précédent) : les tables d'avant gardent leurs octets et leur hash.
    #[test]
    fn mechanics_field_order_is_locked() {
        let mut t = header();
        t.mechanics = Some(Mechanics {
            gold: Some(GoldParams {
                slots: vec![
                    GoldSlot { floor: Rarity::Rare, weights: None, burnable: true },
                    GoldSlot {
                        floor: Rarity::Legendary,
                        weights: Some(RarityWeights { mythic: 20, legendary: 80, epic: 0, rare: 0, common: 0 }),
                        burnable: false,
                    },
                ],
            }),
            pity: Some(PityParams { p0_ppb: 20_000, k_ppb: 20, p_max_ppb: 40_000, n_max: None }),
            burn: Some(BurnParams { floor_bps: 2_500, prior_k: 20 }),
            rush: Some(RushParams {
                ratio_bps: 25_000,
                min_packs: 50,
                window_blocks: 6_000,
                baseline_blocks: 144_000,
                bucket_blocks: 1_500,
                duration_blocks: 3_000,
                cooldown_blocks: 36_000,
                max_per_account: 3,
                weights: RarityWeights { mythic: 3, legendary: 30, epic: 241, rare: 936, common: 8_790 },
            }),
            resurrection: Some(ResurrectionParams { eligible: vec![0, 3] }),
            value: Some(ValueParams {
                normal: vec![(2_000, 5), (20_000, 1)],
                gold: vec![(30_000, 1)],
                rush: vec![(9_000, 2)],
                multipliers: RarityWeights { mythic: 0, legendary: 50, epic: 20, rare: 3, common: 1 },
            }),
        });
        let json = String::from_utf8(near_sdk::serde_json::to_vec(&t).unwrap()).unwrap();
        assert!(json.ends_with(concat!(
            r#""royalties":[{"account_id":"r.near","bps":10}],"#,
            r#""mechanics":{"gold":{"slots":[{"floor":"rare","weights":null,"burnable":true},"#,
            r#"{"floor":"legendary","weights":{"mythic":20,"legendary":80,"epic":0,"rare":0,"common":0},"burnable":false}]},"#,
            r#""pity":{"p0_ppb":20000,"k_ppb":20,"p_max_ppb":40000,"n_max":null},"burn":{"floor_bps":2500,"prior_k":20},"#,
            r#""rush":{"ratio_bps":25000,"min_packs":50,"window_blocks":6000,"baseline_blocks":144000,"#,
            r#""bucket_blocks":1500,"duration_blocks":3000,"cooldown_blocks":36000,"max_per_account":3,"#,
            r#""weights":{"mythic":3,"legendary":30,"epic":241,"rare":936,"common":8790}},"#,
            r#""resurrection":{"eligible":[0,3]},"#,
            r#""value":{"normal":[[2000,5],[20000,1]],"gold":[[30000,1]],"rush":[[9000,2]],"#,
            r#""multipliers":{"mythic":0,"legendary":50,"epic":20,"rare":3,"common":1}}}}"#,
        )), "{json}");
        let (before, after) = header_json_parts(&t);
        assert_eq!([before, after].concat(), json.into_bytes());
        // `"mechanics": null` explicite = absent.
        let back: SeriesTable = near_sdk::serde_json::from_str(&json_without_mechanics_null()).unwrap();
        assert!(back.mechanics.is_none());
    }

    fn json_without_mechanics_null() -> String {
        let mut v = near_sdk::serde_json::to_value(header()).unwrap();
        v["mechanics"] = near_sdk::serde_json::Value::Null;
        v.to_string()
    }

    #[test]
    #[should_panic(expected = "plusieurs fois")]
    fn cards_key_twice_panics() {
        split_at_cards(br#"{"a":[],"cards":[],"b":{"cards":[]}}"#);
    }

    #[test]
    #[should_panic(expected = "introuvable")]
    fn cards_key_missing_panics() {
        split_at_cards(br#"{"name":"x"}"#);
    }
}
