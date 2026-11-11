//! Mythiques secrètes. La table publique ne contient que
//! `commitment = sha256(card_id || sel)` et `content_hash = sha256(json(content) || sel)`,
//! avec le poids et le plafond. À la première sortie, la carte est créée « scellée » ;
//! quiconque détient la préimage (en pratique l'owner) la révèle et le contrat vérifie les deux hashs.

use crate::series::check_backing;
use crate::types::*;
use crate::*;
use near_sdk::serde_json::json;

pub(crate) fn compute_commitments(card_id: &str, sel: &[u8], content: &MythicContent) -> ([u8; 32], [u8; 32]) {
    let mut a = card_id.as_bytes().to_vec();
    a.extend_from_slice(sel);
    let mut b = near_sdk::serde_json::to_vec(content)
        .unwrap_or_else(|_| env::panic_str("E_INTERNAL: Sérialisation impossible"));
    b.extend_from_slice(sel);
    (env::sha256_array(&a), env::sha256_array(&b))
}

/// Le sel doit faire exactement 32 octets (64 caractères hex), un par mythique :
/// un sel court ou réutilisé permettrait de retrouver les autres mythiques par force brute
/// sur le catalogue après une première révélation.
pub(crate) fn decode_sel(sel: &str) -> Vec<u8> {
    let b = hex_decode(sel).unwrap_or_else(|| env::panic_str("E_SEL_HEX: sel : hex invalide"));
    require!(b.len() == 32, "E_SEL_LENGTH: sel : 32 octets exactement");
    b
}

#[near(serializers = [json])]
pub struct CommitmentPair {
    pub commitment: String,
    pub content_hash: String,
}

#[near]
impl Contract {
    /// Aide (lecture) : calcule les engagements d'une mythique. `sel` en hex (32 octets conseillés).
    /// À appeler hors ligne de préférence (une vue RPC transmet le secret au nœud interrogé).
    pub fn compute_mythic_commitment(&self, card_id: String, sel: String, content: MythicContent) -> CommitmentPair {
        let sel = decode_sel(&sel);
        let (c, h) = compute_commitments(&card_id, &sel, &content);
        CommitmentPair { commitment: hex32(&c), content_hash: hex32(&h) }
    }

    /// Révèle une mythique déjà sortie au moins une fois. Le dépôt couvre le stockage ajouté
    /// (excédent rendu). **Publie le contenu** (`card_id`, sel, titre, médias, adossement) dans
    /// `mythic_revealed` et `get_mythic_commitments` : c'est ce qui rend l'engagement vérifiable, et
    /// ce qu'exige le burn d'une mythique (son adossement est dans le contenu). Les métadonnées
    /// NEP-177 et `get_card` restent anonymes (« ? »).
    #[payable]
    pub fn reveal_mythic(
        &mut self,
        series_id: u32,
        mythic_index: u32,
        card_id: String,
        sel: String,
        content: MythicContent,
    ) {
        let start = env::storage_usage();
        require!(!card_id.is_empty() && card_id.len() <= MAX_ID_LEN, "E_CARD_ID: card_id invalide");
        require!(!content.title.is_empty() && content.title.len() <= MAX_TITLE_LEN, "E_TITLE: title invalide");
        for u in [&content.media, &content.reference].into_iter().flatten() {
            require!(u.len() <= MAX_URL_LEN, "E_URL_LENGTH: URL trop longue");
        }
        check_backing(&content.backing);
        let sel_bytes = decode_sel(&sel);

        let mut series = self.series_ref(series_id).clone();
        let j = mythic_index as usize;
        require!(j < series.table.mythics.len(), "E_UNKNOWN_MYTHIC: Index de mythique inconnu");
        require!(series.revealed_mythics[j].is_none(), "E_MYTHIC_REVEALED: Mythique déjà révélée");
        require!(series.mythic_minted[j] > 0, "E_MYTHIC_NOT_DRAWN: Mythique jamais sortie : révélation refusée");
        let m = series.table.mythics[j].clone();
        let (c, h) = compute_commitments(&card_id, &sel_bytes, &content);
        require!(hex32(&c) == m.commitment, "E_COMMITMENT_MISMATCH: sha256(card_id || sel) ne correspond pas à l'engagement");
        require!(hex32(&h) == m.content_hash, "E_CONTENT_MISMATCH: Le contenu ne correspond pas à content_hash");

        let revealed = RevealedMythic {
            card_id: card_id.clone(),
            sel: sel.clone(),
            content: content.clone(),
            revealed_at_height: env::block_height(),
        };
        // Les cartes déjà tirées ne stockent que leur référence : leurs métadonnées et leur
        // adossement se lisent désormais dans `revealed_mythics`, rien à réécrire carte par carte.
        // La liste des cartes scellées ne sert plus qu'à l'événement : elle est vidée ici
        // (`updated_at` des cartes créées scellées se déduit de la date de leur tirage).
        let sealed = std::mem::take(&mut series.sealed_tokens[j]);
        series.revealed_mythics[j] = Some(revealed);
        series.mythic_revealed_ms[j] = env::block_timestamp_ms();
        *self.series.get_mut(series_id).unwrap() = series;

        events::emit(
            "mythic_revealed",
            json!({
                "series_id": series_id, "mythic_index": mythic_index, "card_id": card_id,
                "sel": sel, "content": content, "commitment": m.commitment,
                "content_hash": m.content_hash, "token_ids": sealed,
            }),
        );
        // Pas de `nft_metadata_update` : les métadonnées d'une mythique restent anonymes (« ? »)
        // après la révélation, elles ne changent pas.

        // Stockage : flush explicite pour mesurer, puis facturation au révélateur.
        self.series.flush();
        let end = env::storage_usage();
        let cost = env::storage_byte_cost().as_yoctonear() * end.saturating_sub(start) as u128;
        let deposit = env::attached_deposit().as_yoctonear();
        require!(deposit >= cost, format!("E_STORAGE_DEPOSIT: Dépôt insuffisant pour le stockage : {} yoctoNEAR", cost));
        Self::refund(&env::predecessor_account_id(), deposit - cost);
    }
}
