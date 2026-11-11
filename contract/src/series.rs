//! Séries : création (brouillon), ouverture (gel + hash), pause, fermeture.
//! Une table ouverte n'est jamais modifiable.

use crate::hash_stream::{header_json_parts, Sha256Stream};
use crate::types::*;
use crate::*;
use near_sdk::serde_json::json;

#[cfg(test)]
pub(crate) fn table_hash(table: &SeriesTable) -> [u8; 32] {
    let bytes = near_sdk::serde_json::to_vec(table)
        .unwrap_or_else(|_| env::panic_str("Sérialisation de la table impossible"));
    env::sha256_array(&bytes)
}

fn check_len(s: &str, max: usize, what: &str) {
    require!(!s.is_empty() && s.len() <= max, format!("{what} : longueur invalide"));
}

fn check_opt_url(s: &Option<String>, what: &str) {
    if let Some(u) = s {
        check_len(u, MAX_URL_LEN, what);
    }
}

pub(crate) fn check_backing(b: &Option<Backing>) {
    if let Some(b) = b {
        check_len(&b.asset_id, MAX_ASSET_ID_LEN, "asset_id");
        require!(b.amount.0 > 0, "amount doit être > 0");
    }
}

fn is_hex32(s: &str) -> bool {
    s.len() == 64 && hex_decode(s).is_some()
}

/// En-tête de la table : tout sauf les cartes visibles.
fn validate_header(table: &SeriesTable) {
    check_len(&table.name, MAX_TITLE_LEN, "name");
    require!(table.price.0 > 0, "Le prix doit être > 0");
    require!(
        table.cards_per_pack >= 1 && table.cards_per_pack <= MAX_CARDS_PER_PACK,
        "cards_per_pack hors bornes"
    );
    require!(table.mythics.len() <= MAX_MYTHICS_PER_SERIES, "Trop de mythiques");
    require!(table.rarity_weights.total() > 0, "Poids de rareté nuls");
    let mut commits = std::collections::BTreeSet::new();
    let mut contents = std::collections::BTreeSet::new();
    for m in &table.mythics {
        require!(is_hex32(&m.commitment), "commitment : 64 caractères hex minuscules");
        require!(is_hex32(&m.content_hash), "content_hash : 64 caractères hex minuscules");
        require!(m.cap >= 1 && m.cap <= MAX_MYTHIC_CAP, "Plafond de mythique hors bornes");
        require!(commits.insert(m.commitment.as_str()), "Engagement en double");
        require!(contents.insert(m.content_hash.as_str()), "content_hash en double");
    }
    if table.rarity_weights.mythic > 0 {
        require!(
            table.mythics.iter().any(|m| m.weight > 0),
            "Poids mythique sans engagement de poids non nul"
        );
    }
    require!(table.royalties.len() <= MAX_ROYALTIES, "Trop de redevances");
    let bps: u32 = table.royalties.iter().map(|r| r.bps as u32).sum();
    require!(bps <= MAX_ROYALTY_BPS, "Redevances > 50 %");
}

/// Contrôles carte par carte, et unicité des `card_id` dans `cards`.
fn validate_cards(weights: &RarityWeights, cards: &[CardDef]) {
    let mut ids = std::collections::BTreeSet::new();
    for c in cards {
        check_len(&c.card_id, MAX_ID_LEN, "card_id");
        check_len(&c.title, MAX_TITLE_LEN, "title");
        check_opt_url(&c.media, "media");
        check_opt_url(&c.reference, "reference");
        check_backing(&c.backing);
        require!(c.rarity != Rarity::Mythic, "Les mythiques passent par des engagements");
        require!(weights.get(c.rarity) > 0, "Carte dans une rareté de poids nul");
        require!(ids.insert(c.card_id.as_str()), "card_id en double");
    }
}

/// Règles qui portent sur la table entière : chaque rareté pondérée a une carte, et une commune
/// illimitée existe (le tirage n'échoue jamais). Sur les données compactes : pas besoin de relire
/// les cartes à l'ouverture.
fn validate_coverage(weights: &RarityWeights, cards: &[DrawCard]) {
    for r in [Rarity::Legendary, Rarity::Epic, Rarity::Rare, Rarity::Common] {
        if weights.get(r) > 0 {
            require!(
                cards.iter().any(|c| c.rarity == r && c.weight > 0),
                format!("Rareté {} sans carte", r.as_str())
            );
        }
    }
    require!(
        weights.common > 0
            && cards.iter().any(|c| c.rarity == Rarity::Common && c.cap.is_none() && c.weight > 0),
        "Il faut au moins une commune sans plafond et de poids non nul"
    );
}

/// Validation complète d'une table (à la création non partielle, et toujours à l'ouverture).
pub(crate) fn validate_table(table: &SeriesTable) {
    validate_header(table);
    require!(table.cards.len() <= MAX_CARDS_PER_SERIES, "Trop de cartes");
    validate_cards(&table.rarity_weights, &table.cards);
    let compact: Vec<DrawCard> = table.cards.iter().map(DrawCard::from).collect();
    validate_coverage(&table.rarity_weights, &compact);
}

/// Validation d'un appel : complète, ou sans les règles de couverture si la table sera
/// complétée par `append_series_cards` (elles sont alors vérifiées à l'ouverture).
fn validate_call(table: &SeriesTable, partial: bool) {
    require!(
        table.cards.len() <= MAX_CARDS_PER_CALL,
        format!("Trop de cartes pour un appel ({} au plus) : utiliser append_series_cards", MAX_CARDS_PER_CALL)
    );
    if partial {
        validate_header(table);
        validate_cards(&table.rarity_weights, &table.cards);
    } else {
        validate_table(table);
    }
}

#[near]
impl Contract {
    /// Crée une série en brouillon à partir d'une table complète (au plus `MAX_CARDS_PER_CALL`
    /// cartes). Renvoie son identifiant.
    pub fn create_series(&mut self, table: SeriesTable) -> u32 {
        self.create(table, false)
    }

    /// Crée un brouillon avec le premier lot de cartes d'une grosse table, à compléter par
    /// `append_series_cards`. Les règles de couverture (une carte par rareté pondérée, une
    /// commune illimitée) et l'unicité des `card_id` entre lots sont vérifiées par `open_series`.
    ///
    /// Le stockage est payé par l'owner : le dépôt doit couvrir l'augmentation mesurée
    /// (`env::storage_usage()` avant et après), l'excédent est rendu.
    #[payable]
    pub fn create_series_batched(&mut self, table: SeriesTable) -> u32 {
        let before = env::storage_usage();
        let id = self.create(table, true);
        self.charge_storage(id, before);
        id
    }

    /// Remplace la table d'un brouillon (cartes déjà chargées comprises). Impossible après l'ouverture.
    pub fn replace_series_table(&mut self, series_id: u32, table: SeriesTable) {
        self.replace(series_id, table, false)
    }

    /// Comme `replace_series_table`, avec le premier lot d'une grosse table (lots suivants par
    /// `append_series_cards`, validation complète à l'ouverture).
    pub fn replace_series_table_batched(&mut self, series_id: u32, table: SeriesTable) {
        self.replace(series_id, table, true)
    }

    /// Ajoute un lot de cartes visibles à la fin de la table d'un brouillon (au plus
    /// `MAX_CARDS_PER_CALL`, `MAX_CARDS_PER_SERIES` en tout). Renvoie le nombre total de cartes.
    /// Impossible après l'ouverture : le hash est calculé une fois, par `open_series`.
    /// Payable comme `create_series_batched` : le dépôt couvre le stockage ajouté, l'excédent est rendu.
    #[payable]
    pub fn append_series_cards(&mut self, series_id: u32, cards: Vec<CardDef>) -> u32 {
        self.assert_owner();
        let before = env::storage_usage();
        let s = self.series_ref(series_id);
        require!(s.status != SeriesStatus::Deleted, "Brouillon supprimé");
        require!(s.status == SeriesStatus::Draft, "Table figée : série déjà ouverte");
        require!(s.batched, "Série complète : append_series_cards suit create_series_batched");
        require!(
            !cards.is_empty() && cards.len() <= MAX_CARDS_PER_CALL,
            format!("Lot de 1 à {} cartes", MAX_CARDS_PER_CALL)
        );
        validate_cards(&s.table.rarity_weights, &cards);
        let from = s.draw_cards.len();
        let count = cards.len();
        self.push_cards(series_id, cards);
        self.charge_storage(series_id, before);
        let total = self.series_ref(series_id).draw_cards.len() as u32;
        events::emit(
            "series_cards_appended",
            json!({ "series_id": series_id, "from_index": from, "count": count, "total": total }),
        );
        total
    }

    /// Ouvre la série : la table est figée, son hash et le stockage du pire cas sont fixés.
    /// Aucune méthode n'écrit plus les cartes ni l'en-tête ensuite.
    ///
    /// Le hash est `sha256(serde_json::to_vec(table complète))`, calculé au fil du chargement
    /// (`hash_stream`) : l'ouverture ne relit pas les cartes, quelle que soit la taille de la table.
    pub fn open_series(&mut self, series_id: u32) -> String {
        self.assert_owner();
        let s = self.series_ref(series_id);
        require!(s.status != SeriesStatus::Deleted, "Brouillon supprimé");
        require!(s.status == SeriesStatus::Draft, "Série déjà ouverte");
        // Règles de couverture (déjà vérifiées à la création d'une table complète, pas d'une table par lots).
        validate_coverage(&s.table.rarity_weights, &s.draw_cards);
        let storage = self.worst_case_pack_storage(series_id);
        let s = self.series.get_mut(series_id).unwrap();
        let mut stream = s.hash_stream.take().unwrap_or_else(|| env::panic_str("Hash de chargement absent"));
        stream.update(&header_json_parts(&s.table).1);
        let h = stream.finalize();
        s.table_hash = Some(h);
        s.storage_per_pack = storage;
        s.status = SeriesStatus::Open;
        s.last_card_id = None;
        let hh = hex32(&h);
        events::emit(
            "series_opened",
            json!({ "series_id": series_id, "table_hash": hh, "storage_per_pack": storage, "card_count": s.draw_cards.len() }),
        );
        hh
    }

    /// Supprime un brouillon (jamais une série ouverte) : blocs de cartes, données de tirage,
    /// compteurs, mythiques, redevances et flux de hachage sont effacés. Le stockage libéré
    /// (mesuré) est rendu à l'owner, **dans la limite de ce qu'il a payé** pour ce brouillon
    /// (`storage_deposit`) : un brouillon créé par `create_series` (stockage à la charge du
    /// contrat) libère du stockage sans rien rembourser. Renvoie le montant rendu (yoctoNEAR).
    ///
    /// L'emplacement de la série reste (les identifiants sont des index de `Vector`, jamais
    /// réutilisés) : statut `deleted`, en-tête réduit au nom, au prix et aux poids (environ 200 o,
    /// non rendus).
    pub fn delete_draft(&mut self, series_id: u32) -> U128 {
        self.assert_owner();
        let s = self.series_ref(series_id);
        require!(s.status != SeriesStatus::Deleted, "Brouillon déjà supprimé");
        require!(s.status == SeriesStatus::Draft, "Seul un brouillon peut être supprimé");
        let before = env::storage_usage();
        self.clear_cards(series_id);
        let s = self.series.get_mut(series_id).unwrap();
        s.status = SeriesStatus::Deleted;
        s.batched = false;
        s.last_card_id = None;
        s.hash_stream = None;
        s.table.mythics = Vec::new();
        s.table.royalties = Vec::new();
        s.draw_cards = Vec::new();
        s.minted = Vec::new();
        s.mythic_minted = Vec::new();
        s.revealed_mythics = Vec::new();
        s.sealed_tokens = Vec::new();
        self.series.flush();
        self.series_cards.flush();
        let freed = before.saturating_sub(env::storage_usage());
        let s = self.series.get_mut(series_id).unwrap();
        let refund = (env::storage_byte_cost().as_yoctonear() * freed as u128).min(s.storage_deposit);
        s.storage_deposit -= refund;
        Self::refund(&self.owner_id, refund);
        events::emit(
            "series_draft_deleted",
            json!({ "series_id": series_id, "freed_bytes": freed, "refund": U128(refund) }),
        );
        U128(refund)
    }

    /// Met en pause les ventes (le tirage, le marché et le burn continuent).
    pub fn pause_series(&mut self, series_id: u32) {
        self.set_status(series_id, SeriesStatus::Open, SeriesStatus::Paused, "series_paused");
    }

    pub fn resume_series(&mut self, series_id: u32) {
        self.set_status(series_id, SeriesStatus::Paused, SeriesStatus::Open, "series_resumed");
    }

    /// Fin définitive des ventes.
    pub fn close_series(&mut self, series_id: u32) {
        self.assert_owner();
        let s = self.series.get_mut(series_id).unwrap_or_else(|| env::panic_str("Série inconnue"));
        require!(
            matches!(s.status, SeriesStatus::Open | SeriesStatus::Paused),
            "Série non ouverte"
        );
        s.status = SeriesStatus::Closed;
        events::emit("series_closed", json!({ "series_id": series_id }));
    }
}

impl Contract {
    fn set_status(&mut self, series_id: u32, from: SeriesStatus, to: SeriesStatus, ev: &str) {
        self.assert_owner();
        let s = self.series.get_mut(series_id).unwrap_or_else(|| env::panic_str("Série inconnue"));
        require!(s.status == from, "Transition de statut invalide");
        s.status = to;
        events::emit(ev, json!({ "series_id": series_id }));
    }

    fn replace(&mut self, series_id: u32, table: SeriesTable, partial: bool) {
        self.assert_owner();
        validate_call(&table, partial);
        require!(self.series_ref(series_id).status != SeriesStatus::Deleted, "Brouillon supprimé");
        require!(
            self.series_ref(series_id).status == SeriesStatus::Draft,
            "Table figée : série déjà ouverte"
        );
        self.clear_cards(series_id);
        let mut header = table;
        let cards = std::mem::take(&mut header.cards);
        let m = header.mythics.len();
        let s = self.series.get_mut(series_id).unwrap();
        let mut stream = Sha256Stream::default();
        stream.update(&header_json_parts(&header).0);
        s.hash_stream = Some(stream);
        s.batched = partial;
        s.last_card_id = None;
        s.table = header;
        s.mythic_minted = vec![0; m];
        s.revealed_mythics = vec![None; m];
        s.sealed_tokens = vec![Vec::new(); m];
        self.push_cards(series_id, cards);
    }

    fn create(&mut self, table: SeriesTable, partial: bool) -> u32 {
        self.assert_owner();
        validate_call(&table, partial);
        let id = self.series.len();
        let m = table.mythics.len();
        let mut header = table;
        let cards = std::mem::take(&mut header.cards);
        let mut stream = Sha256Stream::default();
        stream.update(&header_json_parts(&header).0);
        self.series.push(Series {
            id,
            status: SeriesStatus::Draft,
            batched: partial,
            last_card_id: None,
            hash_stream: Some(stream),
            table: header,
            draw_cards: Vec::new(),
            max_card_meta_bytes: 0,
            max_card_backing_bytes: 0,
            table_hash: None,
            minted: Vec::new(),
            mythic_minted: vec![0; m],
            revealed_mythics: vec![None; m],
            sealed_tokens: vec![Vec::new(); m],
            storage_per_pack: 0,
            packs_sold: 0,
            storage_deposit: 0,
        });
        self.push_cards(id, cards);
        events::emit("series_created", json!({ "series_id": id, "batched": partial }));
        id
    }

    /// Fait payer à l'appelant (l'owner) le stockage ajouté depuis `before` : écrit l'état en
    /// attente (`flush`), mesure `env::storage_usage()`, exige un dépôt au moins égal au coût et
    /// rend l'excédent. Le montant retenu s'ajoute à `storage_deposit` (même taille : la mesure
    /// reste juste).
    fn charge_storage(&mut self, series_id: u32, before: u64) -> u128 {
        self.series.flush();
        self.series_cards.flush();
        let added = env::storage_usage().saturating_sub(before);
        let cost = env::storage_byte_cost().as_yoctonear() * added as u128;
        let deposit = env::attached_deposit().as_yoctonear();
        require!(
            deposit >= cost,
            format!("Dépôt insuffisant pour le stockage : {cost} yoctoNEAR exigés ({added} o), {deposit} joints")
        );
        self.series.get_mut(series_id).unwrap().storage_deposit += cost;
        Self::refund(&env::predecessor_account_id(), deposit - cost);
        cost
    }

    /// Ajoute des cartes (déjà validées une à une) à la fin de la table d'un brouillon.
    fn push_cards(&mut self, series_id: u32, cards: Vec<CardDef>) {
        let s = self.series.get_mut(series_id).unwrap_or_else(|| env::panic_str("Série inconnue"));
        require!(s.status == SeriesStatus::Draft, "Table figée : série déjà ouverte");
        require!(s.draw_cards.len() + cards.len() <= MAX_CARDS_PER_SERIES, "Trop de cartes");
        let len = |m: &TokenMetadata| near_sdk::borsh::to_vec(m).map(|v| v.len()).unwrap_or(0) as u64;
        let stream = s.hash_stream.as_mut().unwrap_or_else(|| env::panic_str("Hash de chargement absent"));
        for c in cards {
            let idx = s.draw_cards.len() as u32;
            if s.batched {
                // Par lots, l'unicité des card_id entre lots tient à leur ordre strictement
                // croissant (octets UTF-8) : rien à relire à l'ouverture.
                require!(
                    s.last_card_id.as_ref().is_none_or(|last| c.card_id > *last),
                    "card_id en double ou hors ordre (par lots, card_id strictement croissants)"
                );
                s.last_card_id = Some(c.card_id.clone());
            }
            if idx > 0 {
                stream.update(b",");
            }
            stream.update(&near_sdk::serde_json::to_vec(&c).unwrap_or_else(|_| env::panic_str("JSON impossible")));
            let meta = Self::card_metadata(series_id, &c, u64::MAX);
            s.max_card_meta_bytes = s.max_card_meta_bytes.max(len(&meta));
            if let Some(b) = &c.backing {
                s.max_card_backing_bytes =
                    s.max_card_backing_bytes.max(BACKING_BASE_BYTES + b.asset_id.len() as u64);
            }
            s.draw_cards.push(DrawCard::from(&c));
            s.minted.push(0);
            let key = (series_id, idx / CARDS_PER_CHUNK);
            if idx % CARDS_PER_CHUNK == 0 {
                self.series_cards.insert(key, vec![c]);
            } else {
                self.series_cards
                    .get_mut(&key)
                    .unwrap_or_else(|| env::panic_str("Bloc de cartes manquant"))
                    .push(c);
            }
        }
    }

    /// Retire toutes les cartes d'un brouillon.
    fn clear_cards(&mut self, series_id: u32) {
        let s = self.series.get_mut(series_id).unwrap_or_else(|| env::panic_str("Série inconnue"));
        let chunks = (s.draw_cards.len() as u32).div_ceil(CARDS_PER_CHUNK);
        s.draw_cards.clear();
        s.minted.clear();
        s.max_card_meta_bytes = 0;
        s.max_card_backing_bytes = 0;
        for k in 0..chunks {
            self.series_cards.remove(&(series_id, k));
        }
    }

    /// Stockage du pire cas d'un booster, en octets (voir README pour la mesure réelle).
    /// Les maxima des cartes visibles sont tenus à jour au chargement (`push_cards`).
    pub(crate) fn worst_case_pack_storage(&self, series_id: u32) -> u64 {
        let s = self.series_ref(series_id);
        let len = |m: &TokenMetadata| near_sdk::borsh::to_vec(m).map(|v| v.len()).unwrap_or(0) as u64;
        let mut max_meta = s.max_card_meta_bytes;
        let mut max_backing = s.max_card_backing_bytes;
        if !s.table.mythics.is_empty() {
            // Une mythique déjà révélée peut sortir avec un contenu de taille maximale.
            let dummy = RevealedMythic {
                card_id: "x".repeat(MAX_ID_LEN),
                sel: "0".repeat(64),
                content: MythicContent {
                    title: "x".repeat(MAX_TITLE_LEN),
                    media: Some("x".repeat(MAX_URL_LEN)),
                    reference: Some("x".repeat(MAX_URL_LEN)),
                    backing: None,
                },
                revealed_at_height: 0,
            };
            for m in &s.table.mythics {
                let meta = Self::revealed_mythic_metadata(
                    series_id,
                    m,
                    &dummy,
                    u64::MAX,
                    Some(u64::MAX.to_string()),
                );
                max_meta = max_meta.max(len(&meta));
            }
            max_backing = max_backing.max(BACKING_BASE_BYTES + MAX_ASSET_ID_LEN as u64);
        }
        let per_card = self.tokens.extra_storage_in_bytes_per_token
            + max_meta as u64
            + max_backing
            + PER_CARD_EXTRA_BYTES;
        PACK_BASE_BYTES
            + self.config.reveal_steps as u64 * SEED_RECORD_BYTES
            + OWNER_PACK_LIST_BYTES
            + s.table.cards_per_pack as u64 * per_card
    }
}
