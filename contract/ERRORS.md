# Codes d'erreur du contrat Memaster

Chaque `require!` et chaque panique du contrat commence par un **code stable** suivi de `: ` puis du texte français
(par exemple `E_DEPOSIT: Dépôt insuffisant : … yoctoNEAR requis (prix … + stockage …)`). Le front peut se fonder sur
le code seul, qui ne changera pas, et traduire à partir de cette liste au lieu de suivre les textes. Les `{}` sont des
valeurs insérées à l'exécution (montants, index, noms de champ).

Lire le code dans un échec : `/\b(E_[A-Z0-9_]+): /` sur le message de la panique (`FunctionCallError` /
`ExecutionError`).

Le test `tests_v3::every_error_has_a_stable_code_listed_in_errors_md` échoue si un `require!` ou une panique du
contrat n'a pas de code, si un code manque dans ce fichier, ou si ce fichier liste un code qui n'existe plus.

Colonne « Qui » : `public` pour une erreur que tout utilisateur peut provoquer (achat, marché, burn, transferts),
`révélateur` pour `reveal_mythic`, `owner` et `oracle` pour les méthodes d'administration, `interne` pour un
invariant qui ne peut échouer que sur un bug.

**Messages sans code**, produits par near-sdk et non modifiables : `Method X is private` (méthode `#[private]`),
`Method X doesn't accept deposit` (dépôt joint à une méthode non `#[payable]`), erreurs de désérialisation des
arguments (`Failed to deserialize input from JSON`), `The contract is not initialized`, et les validations de
`NFTContractMetadata::assert_valid` à l'initialisation. Les erreurs du protocole (`NotEnoughBalance`,
`LackBalanceForState`, gaz épuisé) ne viennent pas du contrat.

| Code | Texte français | Proposition anglaise | Qui | Fichiers |
|---|---|---|---|---|
| `E_GAS` | Gaz insuffisant : {} requis | Not enough gas attached: {} required. | public | pack.rs |
| `E_GAS` | Gaz insuffisant pour le burn | Not enough gas attached for the burn. | public | redeem.rs |
| `E_GAS` | Gaz insuffisant pour nft_transfer_call | Not enough gas attached for nft_transfer_call. | public | nft.rs |
| `E_SERIES_NOT_ON_SALE` | Série non ouverte à la vente | This series is not on sale. | public | pack.rs |
| `E_DEPOSIT` | Dépôt insuffisant : {} yoctoNEAR requis (prix {} + stockage {}) | Insufficient deposit: {} yoctoNEAR required (price {} + storage {}). | public | pack.rs |
| `E_RETRY_TOO_EARLY` | Délai de relance non écoulé | The reveal cannot be retried yet. | public | pack.rs |
| `E_ALREADY_REVEALED` | Tirage déjà écrit : relance interdite | This pack is already revealed: retry refused. | public | pack.rs |
| `E_ALREADY_REVEALED` | Tirage déjà écrit : remboursement interdit | This pack is already revealed: refund refused. | public | pack.rs |
| `E_ALREADY_REFUNDED` | Pack déjà remboursé | This pack has already been refunded. | public | pack.rs |
| `E_NOT_STUCK` | Seul un pack bloqué (stuck) est remboursable | Only a stuck pack can be refunded. | public | pack.rs |
| `E_NOT_PACK_OWNER` | Seul l'acheteur du pack peut relancer le tirage | Only the buyer of this pack can retry the reveal. | public | pack.rs |
| `E_PRICE_TOO_HIGH` | Prix trop élevé : {} yoctoNEAR au plus | Price too high: {} yoctoNEAR at most. | public | market.rs |
| `E_AMOUNT_TOO_LARGE` | Montant trop élevé pour le calcul des redevances | Amount too large for the royalty computation. | public | nft.rs |
| `E_UNKNOWN_PACK` | Pack inconnu | Unknown pack. | public | nft.rs, pack.rs |
| `E_UNKNOWN_SERIES` | Série inconnue | Unknown series. | public | lib.rs, pack.rs, series.rs |
| `E_SERIES_NOT_OPEN` | Série non ouverte | This series is not open. | owner, oracle | mechanics.rs, series.rs |
| `E_UNKNOWN_CARD` | Carte inconnue | Unknown card. | public | market.rs, nft.rs, redeem.rs |
| `E_TOKEN_NOT_FOUND` | Token not found | Token not found. | public | nft.rs |
| `E_NOT_APPROVED` | Sender not approved | Sender not approved. | public | nft.rs |
| `E_APPROVAL_ID` | The actual approval_id {:?} is different from the given approval_id {:?} | The actual approval_id {:?} is different from the given approval_id {:?}. | public | nft.rs |
| `E_SAME_OWNER` | Current and next owner must differ | Current and next owner must differ. | public | nft.rs |
| `E_CARD_REDEEMING` | Carte en cours de burn | This card is being burned. | public | market.rs |
| `E_CARD_REDEEMING` | Carte en cours de burn : transfert refusé | This card is being burned: transfer refused. | public | nft.rs |
| `E_PAYOUT_TOO_LONG` | Payout trop long pour max_len_payout | Payout longer than max_len_payout. | public | nft.rs |
| `E_ONE_YOCTO` | Requires attached deposit of at least 1 yoctoNEAR | Requires attached deposit of at least 1 yoctoNEAR. | public | nft.rs |
| `E_ONE_YOCTO` | Requires attached deposit of exactly 1 yoctoNEAR | Requires attached deposit of exactly 1 yoctoNEAR. | public | lib.rs |
| `E_NOT_TOKEN_OWNER` | Predecessor must be token owner. | Predecessor must be token owner. | public | nft.rs |
| `E_STORAGE_DEPOSIT` | Dépôt insuffisant pour le stockage : {cost} yoctoNEAR exigés ({added} o), {deposit} joints | Insufficient storage deposit: {cost} yoctoNEAR required ({added} bytes), {deposit} attached. | public (révélateur), owner, oracle | series.rs |
| `E_STORAGE_DEPOSIT` | Dépôt insuffisant pour le stockage : {} yoctoNEAR | Insufficient storage deposit: {} yoctoNEAR. | public (révélateur), owner, oracle | mechanics.rs, mythic.rs |
| `E_STORAGE_DEPOSIT` | Must attach {} yoctoNEAR to cover storage | Must attach {} yoctoNEAR to cover storage. | public | nft.rs |
| `E_OUT_OF_BOUNDS` | Out of bounds, please use a smaller from_index. | Out of bounds, please use a smaller from_index. | public | nft.rs |
| `E_ZERO_LIMIT` | Cannot provide limit of 0. | Cannot provide limit of 0. | public | nft.rs |
| `E_LIST_NOT_OWNER` | Seul le propriétaire peut vendre | Only the owner can list this card. | public | market.rs |
| `E_ZERO_PRICE` | Prix nul | The price must be greater than zero. | public | market.rs |
| `E_ALREADY_LISTED` | Déjà en vente | This card is already listed. | public | market.rs |
| `E_LISTING_DEPOSIT` | Dépôt d'annonce : {} yoctoNEAR requis | Listing deposit: {} yoctoNEAR required. | public | market.rs |
| `E_NOT_LISTED` | Pas en vente | This card is not listed. | public | market.rs |
| `E_NOT_SELLER` | Seul le vendeur peut retirer l'annonce | Only the seller can remove this listing. | public | market.rs |
| `E_PRICE_CHANGED` | Le prix de l'annonce a changé | The listing price has changed. | public | market.rs |
| `E_SELF_BUY` | Le vendeur ne peut pas acheter sa carte | The seller cannot buy their own card. | public | market.rs |
| `E_STALE_LISTING` | Annonce périmée | This listing is outdated. | public | market.rs |
| `E_DEPOSIT_BELOW_PRICE` | Dépôt inférieur au prix | The attached deposit is lower than the price. | public | market.rs |
| `E_BURN_NOT_OWNER` | Seul le propriétaire peut brûler | Only the owner can burn this card. | public | redeem.rs |
| `E_LISTED_CANNOT_BURN` | Carte en vente : retirez l'annonce d'abord | This card is listed: remove the listing first. | public | redeem.rs |
| `E_NO_REDEEMER` | Aucun redeemer configuré | No redeemer configured. | public | redeem.rs |
| `E_NOT_BURNABLE` | Carte non brûlable | This card is not burnable. | public | redeem.rs |
| `E_BURN_IN_PROGRESS` | Burn déjà en cours | A burn is already in progress for this card. | public | redeem.rs |
| `E_SEL_HEX` | sel : hex invalide | sel: invalid hex. | public (révélateur) | mythic.rs |
| `E_SEL_LENGTH` | sel : 32 octets exactement | sel: exactly 32 bytes. | public (révélateur) | mythic.rs |
| `E_CARD_ID` | card_id invalide | Invalid card_id. | public (révélateur) | mythic.rs |
| `E_TITLE` | title invalide | Invalid title. | public (révélateur) | mythic.rs |
| `E_URL_LENGTH` | URL trop longue | URL too long. | public (révélateur) | mythic.rs |
| `E_UNKNOWN_MYTHIC` | Index de mythique inconnu | Unknown mythic index. | public (révélateur) | mythic.rs |
| `E_MYTHIC_REVEALED` | Mythique déjà révélée | Mythic already revealed. | public (révélateur) | mythic.rs |
| `E_MYTHIC_NOT_DRAWN` | Mythique jamais sortie : révélation refusée | This mythic was never drawn: reveal refused. | public (révélateur) | mythic.rs |
| `E_COMMITMENT_MISMATCH` | sha256(card_id \|\| sel) ne correspond pas à l'engagement | sha256(card_id \|\| sel) does not match the commitment. | public (révélateur) | mythic.rs |
| `E_CONTENT_MISMATCH` | Le contenu ne correspond pas à content_hash | The content does not match content_hash. | public (révélateur) | mythic.rs |
| `E_NOT_OWNER` | Réservé à l'owner | Owner only. | owner | lib.rs |
| `E_NOTHING_TO_WITHDRAW` | Rien à retirer | Nothing to withdraw. | owner | treasury.rs |
| `E_WITHDRAW_LIMIT` | Retrait refusé : {} yoctoNEAR demandés, {} retirables (engagements {}) | Withdrawal refused: {} yoctoNEAR requested, {} withdrawable (commitments {}). | owner | treasury.rs |
| `E_INIT_PARAM` | reveal_steps hors bornes | reveal_steps out of bounds. | owner (init) | lib.rs |
| `E_INIT_PARAM` | retry_delay_blocks ≥ {MIN_RETRY_DELAY_BLOCKS} (sinon un tiers peut bloquer un pack en Stuck) | retry_delay_blocks must be ≥ {MIN_RETRY_DELAY_BLOCKS}. | owner (init) | lib.rs |
| `E_NO_ORACLE_PROPOSAL` | Aucun changement d'oracle proposé | No oracle change proposed. | owner | lib.rs |
| `E_ORACLE_DELAY` | Délai du changement d'oracle non écoulé : bloc {} au plus tôt | Oracle change delay not elapsed: block {} at the earliest. | owner | lib.rs |
| `E_NO_ORACLE` | Aucun oracle de prix configuré | No price oracle configured. | oracle | mechanics.rs |
| `E_NOT_ORACLE` | Réservé à l'oracle de prix | Price oracle only. | oracle | mechanics.rs |
| `E_UNKNOWN_CARD_INDEX` | Index de carte inconnu | Unknown card index. | oracle | mechanics.rs |
| `E_NOT_RESURRECTABLE` | Carte non ressuscitable : absente de mechanics.resurrection.eligible (table hachée) | This card cannot be resurrected: not in mechanics.resurrection.eligible (hashed table). | oracle | mechanics.rs |
| `E_RESURRECT_RARITY` | Résurrection réservée aux cartes épiques et légendaires | Resurrection is for epic and legendary cards only. | oracle | mechanics.rs |
| `E_ALREADY_BACKED` | Carte déjà adossée par la table | This card is already backed by the table. | oracle | mechanics.rs |
| `E_LENGTH` | {what} : longueur invalide | {what}: invalid length. | owner | series.rs |
| `E_BACKING_AMOUNT` | amount doit être > 0 | amount must be > 0. | owner, oracle | series.rs |
| `E_PRICE` | Le prix doit être > 0 | The price must be > 0. | owner | series.rs |
| `E_CARDS_PER_PACK` | cards_per_pack hors bornes | cards_per_pack out of bounds. | owner | series.rs |
| `E_TOO_MANY_MYTHICS` | Trop de mythiques | Too many mythics. | owner | series.rs |
| `E_WEIGHTS_ZERO` | Poids de rareté nuls | Rarity weights are all zero. | owner | series.rs |
| `E_WEIGHTS_ZERO` | {what} : poids nuls | {what}: weights are all zero. | owner | mechanics.rs |
| `E_COMMITMENT_FORMAT` | commitment : 64 caractères hex minuscules | commitment: 64 lowercase hex characters. | owner | series.rs |
| `E_COMMITMENT_FORMAT` | content_hash : 64 caractères hex minuscules | content_hash: 64 lowercase hex characters. | owner | series.rs |
| `E_MYTHIC_CAP` | Plafond de mythique hors bornes | Mythic cap out of bounds. | owner | series.rs |
| `E_DUPLICATE_COMMITMENT` | Engagement en double | Duplicate commitment. | owner | series.rs |
| `E_DUPLICATE_COMMITMENT` | content_hash en double | Duplicate content_hash. | owner | series.rs |
| `E_MYTHIC_WEIGHT` | Poids mythique sans engagement de poids non nul | Mythic weight without a commitment of non-zero weight. | owner | series.rs |
| `E_MYTHIC_WEIGHT` | {what} : poids mythique sans engagement de poids non nul | {what}: mythic weight without a commitment of non-zero weight. | owner | mechanics.rs |
| `E_ROYALTIES` | Redevances > 50 % | Royalties > 50 %. | owner | series.rs |
| `E_ROYALTIES` | Trop de redevances | Too many royalties. | owner | series.rs |
| `E_VISIBLE_MYTHIC` | Les mythiques passent par des engagements | Mythics must be commitments. | owner | series.rs |
| `E_RARITY_WEIGHT` | Carte dans une rareté de poids nul | Card in a rarity of zero weight. | owner | series.rs |
| `E_DUPLICATE_CARD_ID` | card_id en double | Duplicate card_id. | owner | series.rs |
| `E_DUPLICATE_CARD_ID` | card_id en double ou hors ordre (par lots, card_id strictement croissants) | Duplicate or out-of-order card_id (batched loading: strictly increasing card_id). | owner | series.rs |
| `E_RARITY_WITHOUT_CARD` | Rareté {} sans carte | Rarity {} has no card. | owner | series.rs |
| `E_NO_UNLIMITED_COMMON` | Il faut au moins une commune sans plafond et de poids non nul | At least one uncapped common of non-zero weight is required. | owner | series.rs |
| `E_TOO_MANY_CARDS` | Trop de cartes | Too many cards. | owner | series.rs |
| `E_TOO_MANY_CARDS` | Trop de cartes pour un appel ({} au plus) : utiliser append_series_cards | Too many cards for one call ({} at most): use append_series_cards. | owner | series.rs |
| `E_BATCH_SIZE` | Lot de 1 à {} cartes | Batch of 1 to {} cards. | owner | series.rs |
| `E_DRAFT_DELETED` | Brouillon déjà supprimé | Draft already deleted. | owner | series.rs |
| `E_DRAFT_DELETED` | Brouillon supprimé | Draft deleted. | owner | series.rs |
| `E_TABLE_FROZEN` | Série déjà ouverte | Series already open. | owner | series.rs |
| `E_TABLE_FROZEN` | Table figée : série déjà ouverte | Table frozen: series already open. | owner | series.rs |
| `E_NOT_BATCHED` | Série complète : append_series_cards suit create_series_batched | Complete series: append_series_cards follows create_series_batched. | owner | series.rs |
| `E_NOT_DRAFT` | Seul un brouillon peut être supprimé | Only a draft can be deleted. | owner | series.rs |
| `E_STATUS_TRANSITION` | Transition de statut invalide | Invalid status transition. | owner | series.rs |
| `E_TABLE_FORMAT` | Motif "cards":[ présent plusieurs fois dans l'en-tête | Pattern "cards":[ appears more than once in the header. | owner | hash_stream.rs |
| `E_MECH_VALUE` | value : prix trop élevé pour ces valeurs et multiplicateurs (dépassement de u128) | value: price too high for these values and multipliers (u128 overflow). | owner | mechanics.rs |
| `E_MECH_VALUE` | value.multipliers.mythic = 0 (une mythique garde l'adossement de son contenu) | value.multipliers.mythic = 0 (a mythic keeps the backing of its content). | owner | mechanics.rs |
| `E_MECH_VALUE` | value.multipliers.{} : 1 à {MAX_VALUE_MULT} | value.multipliers.{}: 1 to {MAX_VALUE_MULT}. | owner | mechanics.rs |
| `E_MECH_VALUE` | value.{what} : 1 à {MAX_VALUE_TIERS} paliers | value.{what}: 1 to {MAX_VALUE_TIERS} tiers. | owner | mechanics.rs |
| `E_MECH_VALUE` | value.{what} : poids nuls interdits | value.{what}: zero weights are not allowed. | owner | mechanics.rs |
| `E_MECH_VALUE` | value.{what} : valeur hors de [{min_bps}, {max_bps}] points de base | value.{what}: value outside [{min_bps}, {max_bps}] basis points. | owner | mechanics.rs |
| `E_MECH_GOLD` | gold.slots : 1 à 10 emplacements | gold.slots: 1 to 10 slots. | owner | mechanics.rs |
| `E_MECH_GOLD` | gold.slots[{i}] : poids sous le plancher {} | gold.slots[{i}]: weight below the floor {}. | owner | mechanics.rs |
| `E_MECH_PITY` | pity : gold pack inatteignable (p_max_ppb = 0 sans n_max) | pity: gold pack unreachable (p_max_ppb = 0 without n_max). | owner | mechanics.rs |
| `E_MECH_PITY` | pity : p0_ppb ≤ p_max_ppb | pity: p0_ppb ≤ p_max_ppb. | owner | mechanics.rs |
| `E_MECH_PITY` | pity : probabilités en ppb (≤ 10⁹) | pity: probabilities in ppb (≤ 10⁹). | owner | mechanics.rs |
| `E_MECH_PITY` | pity exige gold | pity requires gold. | owner | mechanics.rs |
| `E_MECH_PITY` | pity.n_max hors bornes (absent, ou 1 à 10 000) | pity.n_max out of bounds (absent, or 1 to 10,000). | owner | mechanics.rs |
| `E_MECH_RESURRECTION` | resurrection.eligible : 200 cartes au plus | resurrection.eligible: 200 cards at most. | owner | mechanics.rs |
| `E_MECH_RESURRECTION` | resurrection.eligible : carte déjà adossée par la table | resurrection.eligible: card already backed by the table. | owner | mechanics.rs |
| `E_MECH_RESURRECTION` | resurrection.eligible : cartes épiques et légendaires seulement | resurrection.eligible: epic and legendary cards only. | owner | mechanics.rs |
| `E_MECH_RESURRECTION` | resurrection.eligible : index de carte inconnu | resurrection.eligible: unknown card index. | owner | mechanics.rs |
| `E_MECH_RESURRECTION` | resurrection.eligible : index strictement croissants | resurrection.eligible: strictly increasing indexes. | owner | mechanics.rs |
| `E_MECH_BURN` | burn.floor_bps ≤ 10 000 | burn.floor_bps ≤ 10,000. | owner | mechanics.rs |
| `E_MECH_BURN` | burn.prior_k ≤ 1 000 000 | burn.prior_k ≤ 1,000,000. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush : 1 à 96 seaux | rush: 1 to 96 buckets. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush : fenêtre courte plus courte que la fenêtre longue | rush: the short window must be shorter than the long window. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush : seaux et durée ≥ 1 bloc | rush: buckets and duration ≥ 1 block. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush : window_blocks et baseline_blocks multiples de bucket_blocks | rush: window_blocks and baseline_blocks must be multiples of bucket_blocks. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush.max_per_account ≥ 1 | rush.max_per_account ≥ 1. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush.min_packs ≥ 1 | rush.min_packs ≥ 1. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush.ratio_bps inatteignable pour ces fenêtres | rush.ratio_bps unreachable for these windows. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush.ratio_bps ≥ 10 000 (×1) | rush.ratio_bps ≥ 10,000 (×1). | owner | mechanics.rs |
| `E_MECH_BURNABLE` | Brûlable garantie : il faut une carte adossée par la table, sans plafond et de poids non nul | Guaranteed burnable: a table-backed, uncapped card of non-zero weight is required. | owner | mechanics.rs |
| `E_TEST_HOOK` | test-hooks: échec simulé du dernier reçu | test-hooks: simulated failure of the last receipt. | tests | pack.rs |
| `E_INTERNAL` | Bloc de cartes manquant | Internal error (card chunk). | interne | series.rs, views.rs |
| `E_INTERNAL` | Bloc de liste manquant | Internal error (list chunk). | interne | nft.rs, pack.rs |
| `E_INTERNAL` | Bloc de liste vide | Internal error (list chunk). | interne | nft.rs |
| `E_INTERNAL` | Blocs de cartes incohérents | Internal error (card chunks). | interne | lib.rs, views.rs |
| `E_INTERNAL` | Carte de table inconnue | Internal error (table card). | interne | lib.rs |
| `E_INTERNAL` | Champ cards introuvable | Internal error (cards field). | interne | hash_stream.rs |
| `E_INTERNAL` | En-tête : tableau cards non vide | Internal error (non-empty header cards). | interne | hash_stream.rs |
| `E_INTERNAL` | Hash de chargement absent | Internal error (loading hash). | interne | series.rs |
| `E_INTERNAL` | JSON impossible | Internal error (JSON). | interne | hash_stream.rs, series.rs |
| `E_INTERNAL` | Liste du propriétaire incohérente | Internal error (owner list). | interne | nft.rs |
| `E_INTERNAL` | Liste globale incohérente | Internal error (global list). | interne | nft.rs |
| `E_INTERNAL` | Sérialisation de la table impossible | Internal error (serialization). | interne | series.rs |
| `E_INTERNAL` | Sérialisation impossible | Internal error (serialization). | interne | mythic.rs |
| `E_INTERNAL` | Table non hachée | Internal error (table not hashed). | interne | pack.rs |
