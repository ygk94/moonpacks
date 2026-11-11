//! NEP-171 (cœur), 177 (métadonnées), 178 (approbations), 181 (énumération), 199 (payouts).
//!
//! **Stockage minimal par carte.** Une carte est un emplacement de pack : `token_id = pack_id × 10 +
//! emplacement`, son propriétaire est `CardSlot::owner` (`None` = l'acheteur du pack), sa référence
//! (série, index de carte) est dans le pack et son tirage. Les métadonnées NEP-177 et l'adossement
//! sont reconstruits à chaque lecture depuis la table de série (`nft_token`, `nft_tokens*`,
//! `get_card`, `get_backing`). Les listes NEP-181 sont rangées par blocs (8 o par carte) et le
//! retrait se fait par échange avec la dernière entrée.
//!
//! Toute sortie d'une carte passe par `before_transfer` : refus en `Redeeming`, retrait de l'annonce.

use crate::types::*;
use crate::*;
use near_contract_standards::non_fungible_token::approval::{ext_nft_approval_receiver, NonFungibleTokenApproval};
use near_contract_standards::non_fungible_token::core::{
    ext_nft_receiver, ext_nft_resolver, NonFungibleTokenCore, NonFungibleTokenResolver,
};
use near_contract_standards::non_fungible_token::enumeration::NonFungibleTokenEnumeration;
use near_contract_standards::non_fungible_token::events::{NftBurn, NftMint, NftTransfer};
use near_contract_standards::non_fungible_token::metadata::NonFungibleTokenMetadataProvider;
use near_contract_standards::non_fungible_token::Token;
use near_sdk::{Promise, PromiseOrValue};
use std::collections::HashMap;

/// Gaz fixe de `nft_resolve_transfer` (le standard n'en donne que 5 Tgas ; mesuré : voir README).
pub const GAS_FOR_RESOLVE_TRANSFER: Gas = Gas::from_tgas(15);
/// Gaz minimal pour `nft_transfer_call` : propre exécution + receveur + résolution.
pub const MIN_GAS_FOR_NFT_TRANSFER_CALL: Gas = Gas::from_tgas(45);
/// Gaz gardé par `nft_approve` quand il appelle `nft_on_approve` (comme le standard).
const GAS_FOR_NFT_APPROVE: Gas = Gas::from_tgas(10);

/// Octets d'une approbation, comme le standard (`bytes_for_approved_account_id`).
fn approval_bytes(a: &AccountId) -> u64 {
    a.as_str().len() as u64 + 4 + 8
}

/// Rend au propriétaire le stockage de ses approbations effacées, comme le standard. Renvoie le
/// montant rendu (yoctoNEAR).
pub(crate) fn refund_approvals(owner: &AccountId, approvals: Option<&HashMap<AccountId, u64>>) -> u128 {
    if let Some(a) = approvals {
        let bytes: u64 = a.keys().map(approval_bytes).sum();
        if bytes > 0 {
            let amount = env::storage_byte_cost().as_yoctonear() * bytes as u128;
            Contract::refund(owner, amount);
            return amount;
        }
    }
    0
}

fn pack_slot(tid: u64) -> (u64, usize) {
    (tid / 10, (tid % 10) as usize)
}

impl Contract {
    // ------------------------------------------------------------ lecture

    /// Carte vivante (non brûlée) : (pack_id, emplacement, pack).
    pub(crate) fn live(&self, token_id: &str) -> Option<(u64, usize, &Pack)> {
        let tid = parse_token_id(token_id)?;
        let (pid, slot) = pack_slot(tid);
        let pack = self.packs.get(&pid)?;
        let card = pack.cards.get(slot)?;
        (card.state != CardState::Burned).then_some((pid, slot, pack))
    }

    pub(crate) fn expect_live(&self, token_id: &str) -> (u64, usize, &Pack) {
        self.live(token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"))
    }

    pub(crate) fn owner_of(&self, token_id: &str) -> Option<AccountId> {
        let (_, slot, pack) = self.live(token_id)?;
        Some(pack.cards[slot].owner.clone().unwrap_or_else(|| pack.owner_id.clone()))
    }

    pub(crate) fn card_state(&self, token_id: &str) -> CardState {
        let (_, slot, pack) = self.expect_live(token_id);
        pack.cards[slot].state
    }

    /// Adossement courant d'une carte : celui de la table, ou celui donné par l'oracle
    /// (résurrection) ; pour une mythique, celui de son contenu révélé.
    pub(crate) fn backing_of(&self, series_id: u32, kind: CardKind, index: u32) -> Option<Backing> {
        match kind {
            CardKind::Visible => self
                .card_def(series_id, index)
                .backing
                .or_else(|| self.resurrected.get(&(series_id, index)).cloned()),
            CardKind::Mythic => self.series_ref(series_id).revealed_mythics[index as usize]
                .as_ref()
                .and_then(|r| r.content.backing.clone()),
        }
    }

    pub(crate) fn token_backing(&self, token_id: &str) -> Option<Backing> {
        let (_, slot, pack) = self.live(token_id)?;
        self.slot_backing(pack, slot)
    }

    /// Adossement d'un exemplaire. Série à table de valeur : l'actif est celui de la carte (table ou
    /// oracle) et le montant est la part de la valeur tirée pour ce pack (`draw::split_value`),
    /// recalculée depuis `Pack::value`. Cas spéciaux, adossement fixe : une mythique (son contenu
    /// révélé) et une carte devenue brûlable après son tirage (montant de l'oracle).
    pub(crate) fn slot_backing(&self, pack: &Pack, slot: usize) -> Option<Backing> {
        let d = pack.draws[slot];
        let mut b = self.backing_of(pack.series_id, d.kind, d.index)?;
        if let Some(amount) = self.slot_value(pack, slot) {
            b.amount = U128(amount);
        }
        Some(b)
    }

    /// Part de la valeur du pack attribuée à l'emplacement `slot` (`None` s'il n'en a pas).
    pub(crate) fn slot_value(&self, pack: &Pack, slot: usize) -> Option<u128> {
        let pv = pack.value?;
        if pv.mask & (1u16 << slot) == 0 {
            return None;
        }
        let s = self.series_ref(pack.series_id);
        let v = crate::mechanics::value_params(&s.table)?;
        let slots: Vec<(Rarity, bool)> =
            pack.draws.iter().enumerate().map(|(i, d)| (d.final_rarity, pv.mask & (1u16 << i) != 0)).collect();
        draw::split_value(draw::value_total(s.table.price.0, pv.bps), &slots, &v.multipliers)[slot]
    }

    /// Métadonnées NEP-177 reconstruites depuis la table.
    pub(crate) fn token_metadata(&self, pack_id: u64, pack: &Pack, slot: usize) -> TokenMetadata {
        let d = pack.draws[slot];
        let sid = pack.series_id;
        match d.kind {
            CardKind::Visible => {
                let c = self.card_def(sid, d.index);
                let burnable = c.backing.is_some() || self.resurrected.contains_key(&(sid, d.index));
                Self::card_metadata(sid, &c, pack_id, burnable, pack.revealed_at_ms)
            }
            CardKind::Mythic => Self::mythic_metadata(sid, pack_id, pack.revealed_at_ms),
        }
    }

    pub(crate) fn token_view(&self, tid: u64) -> Option<Token> {
        let token_id = tid.to_string();
        let (pid, slot, pack) = self.live(&token_id)?;
        let owner_id = pack.cards[slot].owner.clone().unwrap_or_else(|| pack.owner_id.clone());
        let approved: HashMap<AccountId, u64> = self
            .approvals
            .get(&tid)
            .map(|a| a.accounts.iter().map(|(k, v)| (k.clone(), *v)).collect())
            .unwrap_or_default();
        Some(Token {
            token_id,
            owner_id,
            metadata: Some(self.token_metadata(pid, pack, slot)),
            approved_account_ids: Some(approved),
        })
    }

    pub(crate) fn slot_mut_by_id(&mut self, token_id: &str) -> &mut CardSlot {
        let tid = parse_token_id(token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        self.slot_mut(tid)
    }

    fn slot_mut(&mut self, tid: u64) -> &mut CardSlot {
        let (pid, slot) = pack_slot(tid);
        &mut self.packs.get_mut(&pid).unwrap_or_else(|| env::panic_str("Pack inconnu")).cards[slot]
    }

    // ------------------------------------------------------------ listes par blocs

    fn owner_list_push(&mut self, owner: &AccountId, tid: u64) -> u32 {
        let len = self.owner_token_count.get(owner).copied().unwrap_or(0);
        let key = (owner.clone(), len / OWNER_CHUNK);
        if len % OWNER_CHUNK == 0 {
            self.owner_tokens.insert(key, vec![tid]);
        } else {
            self.owner_tokens.get_mut(&key).unwrap_or_else(|| env::panic_str("Bloc de liste manquant")).push(tid);
        }
        self.owner_token_count.insert(owner.clone(), len + 1);
        len
    }

    /// Retire l'entrée `pos` (échange avec la dernière). Renvoie la carte déplacée en `pos`.
    fn owner_list_remove(&mut self, owner: &AccountId, pos: u32) -> Option<u64> {
        let len = self.owner_token_count.get(owner).copied().unwrap_or(0);
        require!(pos < len, "Liste du propriétaire incohérente");
        let last_pos = len - 1;
        let last_key = (owner.clone(), last_pos / OWNER_CHUNK);
        let chunk = self.owner_tokens.get_mut(&last_key).unwrap_or_else(|| env::panic_str("Bloc de liste manquant"));
        let last = chunk.pop().unwrap_or_else(|| env::panic_str("Bloc de liste vide"));
        if chunk.is_empty() {
            self.owner_tokens.remove(&last_key);
        }
        if last_pos == 0 {
            self.owner_token_count.remove(owner);
        } else {
            self.owner_token_count.insert(owner.clone(), last_pos);
        }
        if pos == last_pos {
            return None;
        }
        let key = (owner.clone(), pos / OWNER_CHUNK);
        self.owner_tokens.get_mut(&key).unwrap_or_else(|| env::panic_str("Bloc de liste manquant"))
            [(pos % OWNER_CHUNK) as usize] = last;
        Some(last)
    }

    fn global_push(&mut self, tid: u64) -> u32 {
        let len = self.total_supply;
        let key = len / GLOBAL_CHUNK;
        if len % GLOBAL_CHUNK == 0 {
            self.all_tokens.insert(key, vec![tid]);
        } else {
            self.all_tokens.get_mut(&key).unwrap_or_else(|| env::panic_str("Bloc de liste manquant")).push(tid);
        }
        self.total_supply = len + 1;
        len
    }

    fn global_remove(&mut self, pos: u32) -> Option<u64> {
        let len = self.total_supply;
        require!(pos < len, "Liste globale incohérente");
        let last_pos = len - 1;
        let chunk = self.all_tokens.get_mut(&(last_pos / GLOBAL_CHUNK)).unwrap_or_else(|| env::panic_str("Bloc de liste manquant"));
        let last = chunk.pop().unwrap_or_else(|| env::panic_str("Bloc de liste vide"));
        if chunk.is_empty() {
            self.all_tokens.remove(&(last_pos / GLOBAL_CHUNK));
        }
        self.total_supply = last_pos;
        if pos == last_pos {
            return None;
        }
        self.all_tokens.get_mut(&(pos / GLOBAL_CHUNK)).unwrap_or_else(|| env::panic_str("Bloc de liste manquant"))
            [(pos % GLOBAL_CHUNK) as usize] = last;
        Some(last)
    }

    /// Entrées `[from, to)` d'une liste par blocs (`get(bloc)`).
    fn list_range(get: impl Fn(u32) -> Option<Vec<u64>>, chunk: u32, from: u32, to: u32) -> Vec<u64> {
        let mut out = Vec::new();
        let mut i = from;
        while i < to {
            let Some(c) = get(i / chunk) else { break };
            let lo = (i % chunk) as usize;
            let hi = (lo + (to - i) as usize).min(c.len());
            if hi <= lo {
                break;
            }
            out.extend_from_slice(&c[lo..hi]);
            i += (hi - lo) as u32;
        }
        out
    }

    // ------------------------------------------------------------ écriture

    /// Crée la carte de l'emplacement suivant du pack (déjà enregistré dans `packs`).
    /// Aucun chemin d'échec qui dépende de la carte tirée.
    pub(crate) fn internal_mint_slot(&mut self, pack_id: u64, owner: &AccountId) -> TokenId {
        let slot = self.packs.get(&pack_id).map(|p| p.cards.len()).unwrap_or(0);
        let tid = pack_id * 10 + slot as u64;
        let owner_pos = self.owner_list_push(owner, tid);
        let global_pos = self.global_push(tid);
        self.packs
            .get_mut(&pack_id)
            .unwrap_or_else(|| env::panic_str("Pack inconnu"))
            .cards
            .push(CardSlot { owner: None, state: CardState::Normal, owner_pos, global_pos });
        tid.to_string()
    }

    /// Change le propriétaire sans contrôle (listes et emplacement mis à jour).
    pub(crate) fn internal_transfer_unguarded(&mut self, token_id: &str, from: &AccountId, to: &AccountId) {
        let tid = parse_token_id(token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        let pos = self.slot_mut(tid).owner_pos;
        if let Some(moved) = self.owner_list_remove(from, pos) {
            self.slot_mut(moved).owner_pos = pos;
        }
        let new_pos = self.owner_list_push(to, tid);
        let buyer = self.packs.get(&(tid / 10)).map(|p| p.owner_id.clone());
        let slot = self.slot_mut(tid);
        slot.owner = if buyer.as_ref() == Some(to) { None } else { Some(to.clone()) };
        slot.owner_pos = new_pos;
    }

    /// Efface les approbations (l'identifiant suivant est gardé) et les renvoie.
    pub(crate) fn take_approvals(&mut self, token_id: &str) -> HashMap<AccountId, u64> {
        let Some(tid) = parse_token_id(token_id) else { return HashMap::new() };
        match self.approvals.get_mut(&tid) {
            Some(a) => std::mem::take(&mut a.accounts).into_iter().collect(),
            None => HashMap::new(),
        }
    }

    /// Transfert NEP-171 contrôlé (propriétaire ou compte approuvé). Renvoie l'ancien propriétaire
    /// et ses approbations effacées.
    pub(crate) fn internal_transfer(
        &mut self,
        sender_id: &AccountId,
        receiver_id: &AccountId,
        token_id: &TokenId,
        approval_id: Option<u64>,
        memo: Option<String>,
    ) -> (AccountId, HashMap<AccountId, u64>) {
        let owner_id = self.owner_of(token_id).unwrap_or_else(|| env::panic_str("Token not found"));
        let approvals = self.take_approvals(token_id);
        let authorized = if sender_id != &owner_id {
            let actual = approvals.get(sender_id).unwrap_or_else(|| env::panic_str("Sender not approved"));
            require!(
                approval_id.is_none() || approval_id == Some(*actual),
                format!("The actual approval_id {:?} is different from the given approval_id {:?}", actual, approval_id)
            );
            Some(sender_id)
        } else {
            None
        };
        require!(&owner_id != receiver_id, "Current and next owner must differ");
        self.internal_transfer_unguarded(token_id, &owner_id, receiver_id);
        NftTransfer {
            old_owner_id: &owner_id,
            new_owner_id: receiver_id,
            token_ids: &[token_id],
            authorized_id: authorized.map(|a| a.as_ref()),
            memo: memo.as_deref(),
        }
        .emit();
        (owner_id, approvals)
    }

    /// Brûle une carte : retirée des listes, emplacement marqué `Burned`, approbations rendues.
    /// Renvoie le montant déjà rendu pour les approbations (yoctoNEAR).
    pub(crate) fn internal_burn(&mut self, token_id: &TokenId, owner: &AccountId) -> u128 {
        let tid = parse_token_id(token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        let (owner_pos, global_pos) = {
            let s = self.slot_mut(tid);
            (s.owner_pos, s.global_pos)
        };
        if let Some(moved) = self.owner_list_remove(owner, owner_pos) {
            self.slot_mut(moved).owner_pos = owner_pos;
        }
        if let Some(moved) = self.global_remove(global_pos) {
            self.slot_mut(moved).global_pos = global_pos;
        }
        let slot = self.slot_mut(tid);
        slot.state = CardState::Burned;
        slot.owner = None;
        let mut refunded = 0;
        if let Some(a) = self.approvals.remove(&tid) {
            let a: HashMap<AccountId, u64> = a.accounts.into_iter().collect();
            refunded = refund_approvals(owner, Some(&a));
        }
        NftBurn { owner_id: owner, token_ids: &[token_id], authorized_id: None, memo: Some("redeem") }.emit();
        refunded
    }

    pub(crate) fn emit_mint(owner: &AccountId, token_ids: &[TokenId], pack_id: u64) {
        NftMint {
            owner_id: owner,
            token_ids: &token_ids.iter().map(|s| s.as_str()).collect::<Vec<_>>(),
            memo: Some(&format!("pack {}", pack_id)),
        }
        .emit();
    }

    pub(crate) fn before_transfer(&mut self, token_id: &TokenId) {
        if let Some((_, slot, pack)) = self.live(token_id) {
            require!(pack.cards[slot].state == CardState::Normal, "Carte en cours de burn : transfert refusé");
        }
        self.remove_listing(token_id, "transferred");
    }

    /// Payout NEP-199 : redevances de la série, le reste au propriétaire.
    pub(crate) fn compute_payout(
        &self,
        token_id: &TokenId,
        owner: &AccountId,
        balance: u128,
        max_len_payout: Option<u32>,
    ) -> Payout {
        let royalties = self
            .live(token_id)
            .map(|(_, _, p)| self.series_ref(p.series_id).table.royalties.clone())
            .unwrap_or_default();
        let mut payout: HashMap<AccountId, U128> = HashMap::new();
        let mut paid: u128 = 0;
        for r in royalties.iter() {
            let amount = balance * r.bps as u128 / 10_000;
            paid += amount;
            let e = payout.entry(r.account_id.clone()).or_insert(U128(0));
            e.0 += amount;
        }
        let e = payout.entry(owner.clone()).or_insert(U128(0));
        e.0 += balance - paid;
        if let Some(max) = max_len_payout {
            require!(payout.len() as u32 <= max, "Payout trop long pour max_len_payout");
        }
        Payout { payout }
    }
}

#[near]
impl NonFungibleTokenCore for Contract {
    #[payable]
    fn nft_transfer(
        &mut self,
        receiver_id: AccountId,
        token_id: TokenId,
        approval_id: Option<u64>,
        memo: Option<String>,
    ) {
        near_sdk::assert_one_yocto();
        self.before_transfer(&token_id);
        let sender = env::predecessor_account_id();
        let (old_owner, approvals) = self.internal_transfer(&sender, &receiver_id, &token_id, approval_id, memo);
        refund_approvals(&old_owner, Some(&approvals));
    }

    #[payable]
    fn nft_transfer_call(
        &mut self,
        receiver_id: AccountId,
        token_id: TokenId,
        approval_id: Option<u64>,
        memo: Option<String>,
        msg: String,
    ) -> PromiseOrValue<bool> {
        near_sdk::assert_one_yocto();
        require!(env::prepaid_gas() >= MIN_GAS_FOR_NFT_TRANSFER_CALL, "Gaz insuffisant pour nft_transfer_call");
        self.before_transfer(&token_id);
        let sender = env::predecessor_account_id();
        let (old_owner, old_approvals) =
            self.internal_transfer(&sender, &receiver_id, &token_id, approval_id, memo);
        // Comme le standard, mais avec une résolution à 15 Tgas fixes au lieu de 5.
        ext_nft_receiver::ext(receiver_id.clone())
            .with_unused_gas_weight(1)
            .nft_on_transfer(sender, old_owner.clone(), token_id.clone(), msg)
            .then(
                ext_nft_resolver::ext(env::current_account_id())
                    .with_static_gas(GAS_FOR_RESOLVE_TRANSFER)
                    .with_unused_gas_weight(0)
                    .nft_resolve_transfer(old_owner, receiver_id, token_id, Some(old_approvals)),
            )
            .into()
    }

    fn nft_token(&self, token_id: TokenId) -> Option<Token> {
        self.token_view(parse_token_id(&token_id)?)
    }
}

#[near]
impl NonFungibleTokenResolver for Contract {
    #[private]
    fn nft_resolve_transfer(
        &mut self,
        previous_owner_id: AccountId,
        receiver_id: AccountId,
        token_id: TokenId,
        approved_account_ids: Option<HashMap<AccountId, u64>>,
    ) -> bool {
        let must_revert = env::promise_result_checked(0, "false".len())
            .ok()
            .and_then(|v| near_sdk::serde_json::from_slice::<bool>(&v).ok())
            .unwrap_or(true);
        let current = self.owner_of(&token_id);
        let keep = !must_revert
            || current.as_ref() != Some(&receiver_id)
            || self.card_state(&token_id) == CardState::Redeeming;
        if keep {
            // Le destinataire garde la carte (ou elle a déjà bougé, ou elle est brûlée / en burn) :
            // l'annonce éventuelle n'est pas touchée ; les approbations du précédent propriétaire
            // sont effacées, leur stockage lui est rendu.
            refund_approvals(&previous_owner_id, approved_account_ids.as_ref());
            return true;
        }
        // Retour réel au précédent propriétaire : seule une annonce posée entre-temps par le
        // destinataire est retirée.
        if self.listings.get(&token_id).is_some() {
            self.remove_listing(&token_id, "transfer_reverted");
        }
        self.internal_transfer_unguarded(&token_id, &receiver_id, &previous_owner_id);
        let receiver_approvals = self.take_approvals(&token_id);
        refund_approvals(&receiver_id, Some(&receiver_approvals));
        if let (Some(prev), Some(tid)) = (approved_account_ids, parse_token_id(&token_id)) {
            if !prev.is_empty() {
                let rec = self.approvals.get_mut(&tid);
                match rec {
                    Some(r) => r.accounts = prev.into_iter().collect(),
                    None => {
                        let next_id = prev.values().max().copied().unwrap_or(0) + 1;
                        self.approvals.insert(tid, TokenApprovals { next_id, accounts: prev.into_iter().collect() });
                    }
                }
            }
        }
        NftTransfer {
            old_owner_id: &receiver_id,
            new_owner_id: &previous_owner_id,
            token_ids: &[&token_id],
            authorized_id: None,
            memo: None,
        }
        .emit();
        false
    }
}

#[near]
impl NonFungibleTokenApproval for Contract {
    #[payable]
    fn nft_approve(&mut self, token_id: TokenId, account_id: AccountId, msg: Option<String>) -> Option<Promise> {
        require!(env::attached_deposit().as_yoctonear() >= 1, "Requires attached deposit of at least 1 yoctoNEAR");
        let owner_id = self.owner_of(&token_id).unwrap_or_else(|| env::panic_str("Token not found"));
        require!(env::predecessor_account_id() == owner_id, "Predecessor must be token owner.");
        let tid = parse_token_id(&token_id).unwrap();
        let mut rec = self.approvals.get(&tid).cloned().unwrap_or(TokenApprovals { next_id: 1, ..Default::default() });
        let approval_id = rec.next_id.max(1);
        let old = rec.accounts.insert(account_id.clone(), approval_id);
        rec.next_id = approval_id + 1;
        self.approvals.insert(tid, rec);
        let storage_used = if old.is_none() { approval_bytes(&account_id) } else { 0 };
        let cost = env::storage_byte_cost().as_yoctonear() * storage_used as u128;
        let deposit = env::attached_deposit().as_yoctonear();
        require!(cost <= deposit, format!("Must attach {} yoctoNEAR to cover storage", cost));
        if deposit - cost > 1 {
            Self::refund(&env::predecessor_account_id(), deposit - cost);
        }
        msg.map(|msg| {
            ext_nft_approval_receiver::ext(account_id)
                .with_static_gas(env::prepaid_gas().saturating_sub(GAS_FOR_NFT_APPROVE))
                .nft_on_approve(token_id, owner_id, approval_id, msg)
        })
    }

    #[payable]
    fn nft_revoke(&mut self, token_id: TokenId, account_id: AccountId) {
        near_sdk::assert_one_yocto();
        let owner_id = self.owner_of(&token_id).unwrap_or_else(|| env::panic_str("Token not found"));
        let pred = env::predecessor_account_id();
        require!(pred == owner_id, "Predecessor must be token owner.");
        let tid = parse_token_id(&token_id).unwrap();
        if let Some(rec) = self.approvals.get_mut(&tid) {
            if rec.accounts.remove(&account_id).is_some() {
                Self::refund(&pred, env::storage_byte_cost().as_yoctonear() * approval_bytes(&account_id) as u128);
            }
        }
    }

    #[payable]
    fn nft_revoke_all(&mut self, token_id: TokenId) {
        near_sdk::assert_one_yocto();
        let owner_id = self.owner_of(&token_id).unwrap_or_else(|| env::panic_str("Token not found"));
        let pred = env::predecessor_account_id();
        require!(pred == owner_id, "Predecessor must be token owner.");
        let removed = self.take_approvals(&token_id);
        refund_approvals(&pred, Some(&removed));
    }

    fn nft_is_approved(&self, token_id: TokenId, approved_account_id: AccountId, approval_id: Option<u64>) -> bool {
        self.owner_of(&token_id).unwrap_or_else(|| env::panic_str("Token not found"));
        let tid = parse_token_id(&token_id).unwrap();
        match self.approvals.get(&tid).and_then(|a| a.accounts.get(&approved_account_id)) {
            Some(actual) => approval_id.is_none_or(|given| given == *actual),
            None => false,
        }
    }
}

#[near]
impl NonFungibleTokenEnumeration for Contract {
    fn nft_total_supply(&self) -> U128 {
        U128(self.total_supply as u128)
    }

    fn nft_tokens(&self, from_index: Option<U128>, limit: Option<u64>) -> Vec<Token> {
        let start: u128 = from_index.map(|x| x.0).unwrap_or(0);
        require!(self.total_supply as u128 >= start, "Out of bounds, please use a smaller from_index.");
        let limit = limit.unwrap_or(u64::MAX);
        require!(limit != 0, "Cannot provide limit of 0.");
        let from = start as u32;
        let to = (from as u64).saturating_add(limit).min(self.total_supply as u64) as u32;
        Self::list_range(|k| self.all_tokens.get(&k).cloned(), GLOBAL_CHUNK, from, to)
            .into_iter()
            .filter_map(|t| self.token_view(t))
            .collect()
    }

    fn nft_supply_for_owner(&self, account_id: AccountId) -> U128 {
        U128(self.owner_token_count.get(&account_id).copied().unwrap_or(0) as u128)
    }

    fn nft_tokens_for_owner(&self, account_id: AccountId, from_index: Option<U128>, limit: Option<u64>) -> Vec<Token> {
        let len = self.owner_token_count.get(&account_id).copied().unwrap_or(0);
        if len == 0 {
            return vec![];
        }
        let start: u128 = from_index.map(|x| x.0).unwrap_or(0);
        require!(len as u128 > start, "Out of bounds, please use a smaller from_index.");
        let limit = limit.unwrap_or(u64::MAX);
        require!(limit != 0, "Cannot provide limit of 0.");
        let from = start as u32;
        let to = (from as u64).saturating_add(limit).min(len as u64) as u32;
        Self::list_range(|k| self.owner_tokens.get(&(account_id.clone(), k)).cloned(), OWNER_CHUNK, from, to)
            .into_iter()
            .filter_map(|t| self.token_view(t))
            .collect()
    }
}

#[near]
impl NonFungibleTokenMetadataProvider for Contract {
    fn nft_metadata(&self) -> NFTContractMetadata {
        self.metadata.clone()
    }
}

#[near]
impl Contract {
    /// NEP-199 : répartition d'un montant `balance` pour cette carte.
    pub fn nft_payout(&self, token_id: TokenId, balance: U128, max_len_payout: Option<u32>) -> Payout {
        let owner = self.owner_of(&token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        self.compute_payout(&token_id, &owner, balance.0, max_len_payout)
    }

    /// NEP-199 : transfert + répartition (pour marchés externes approuvés).
    #[payable]
    pub fn nft_transfer_payout(
        &mut self,
        receiver_id: AccountId,
        token_id: TokenId,
        approval_id: Option<u64>,
        memo: Option<String>,
        balance: U128,
        max_len_payout: Option<u32>,
    ) -> Payout {
        near_sdk::assert_one_yocto();
        let owner = self.owner_of(&token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        let payout = self.compute_payout(&token_id, &owner, balance.0, max_len_payout);
        self.before_transfer(&token_id);
        let sender = env::predecessor_account_id();
        let (old_owner, approvals) = self.internal_transfer(&sender, &receiver_id, &token_id, approval_id, memo);
        refund_approvals(&old_owner, Some(&approvals));
        payout
    }
}
