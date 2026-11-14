// Erreurs du contrat traduites pour l'interface (anglais seulement).
//
// Contrat v3 : chaque `require!` et chaque panique commence par un code stable `E_…: ` suivi du texte français
// (contract/ERRORS.md). On traduit par le code, avec les propositions anglaises d'ERRORS.md ; quand un code a
// plusieurs textes, le texte français choisit la variante. Les montants en yoctoNEAR s'affichent en NEAR.
// Repli : les messages sans code (contrat app2, protocole, wallet) passent par l'ancienne liste en français.
// errors.test.ts échoue si un code d'ERRORS.md n'est pas traduit ici, ou si un code d'ici n'y figure plus.

import { formatNearExact } from "../lib/format";

/**
 * Par code, les variantes [texte français d'ERRORS.md, anglais]. Dans le français, `{…}` est une valeur insérée par
 * le contrat ; dans l'anglais, `{near}` reprend une valeur en yoctoNEAR et l'affiche en NEAR, tout autre `{…}` la
 * recopie telle quelle, dans l'ordre du français.
 */
export const CODE_MESSAGES: Record<string, [fr: string, en: string][]> = {
  E_GAS: [
    ["Gaz insuffisant : {} requis", "Not enough gas attached: {} required."],
    ["Gaz insuffisant pour le burn", "Not enough gas attached for the burn."],
    ["Gaz insuffisant pour nft_transfer_call", "Not enough gas attached for nft_transfer_call."],
  ],
  E_SERIES_NOT_ON_SALE: [["Série non ouverte à la vente", "This series is not on sale."]],
  E_DEPOSIT: [
    ["Dépôt insuffisant : {} yoctoNEAR requis (prix {} + stockage {})", "Insufficient deposit: {near} required (price {near} + storage {near})."],
  ],
  E_RETRY_TOO_EARLY: [["Délai de relance non écoulé", "The reveal cannot be retried yet."]],
  E_ALREADY_REVEALED: [
    ["Tirage déjà écrit : relance interdite", "This pack is already revealed: retry refused."],
    ["Tirage déjà écrit : remboursement interdit", "This pack is already revealed: refund refused."],
  ],
  E_ALREADY_REFUNDED: [["Pack déjà remboursé", "This pack has already been refunded."]],
  E_NOT_STUCK: [["Seul un pack bloqué (stuck) est remboursable", "Only a stuck pack can be refunded."]],
  E_NOT_PACK_OWNER: [
    ["Seul l'acheteur du pack peut relancer le tirage", "Only the buyer of this pack can retry the reveal."],
  ],
  E_PRICE_TOO_HIGH: [["Prix trop élevé : {} yoctoNEAR au plus", "Price too high: {near} at most."]],
  E_AMOUNT_TOO_LARGE: [
    ["Montant trop élevé pour le calcul des redevances", "Amount too large for the royalty computation."],
  ],
  E_UNKNOWN_PACK: [["Pack inconnu", "Unknown pack."]],
  E_UNKNOWN_KIND: [["Type de pack inconnu dans cette série", "Unknown pack type in this series."]],
  E_KINDS: [["kinds : types de packs invalides (taille, nom, prix, cartes, règles, brûlable garantie)", "Invalid pack types in the series (size, name, price, cards, slot rules or guaranteed burnable)."]],
  E_UNKNOWN_SERIES: [["Série inconnue", "Unknown series."]],
  E_SERIES_NOT_OPEN: [["Série non ouverte", "This series is not open."]],
  E_UNKNOWN_CARD: [["Carte inconnue", "Unknown card."]],
  E_TOKEN_NOT_FOUND: [["Token not found", "Token not found."]],
  E_NOT_APPROVED: [["Sender not approved", "Sender not approved."]],
  E_APPROVAL_ID: [
    ["The actual approval_id {:?} is different from the given approval_id {:?}", "The actual approval_id {:?} is different from the given approval_id {:?}."],
  ],
  E_SAME_OWNER: [["Current and next owner must differ", "Current and next owner must differ."]],
  E_CARD_REDEEMING: [
    ["Carte en cours de burn", "This card is being burned."],
    ["Carte en cours de burn : transfert refusé", "This card is being burned: transfer refused."],
  ],
  E_PAYOUT_TOO_LONG: [["Payout trop long pour max_len_payout", "Payout longer than max_len_payout."]],
  E_ONE_YOCTO: [
    ["Requires attached deposit of at least 1 yoctoNEAR", "Requires attached deposit of at least 1 yoctoNEAR."],
    ["Requires attached deposit of exactly 1 yoctoNEAR", "Requires attached deposit of exactly 1 yoctoNEAR."],
  ],
  E_NOT_TOKEN_OWNER: [["Predecessor must be token owner.", "Predecessor must be token owner."]],
  E_STORAGE_DEPOSIT: [
    ["Dépôt insuffisant pour le stockage : {cost} yoctoNEAR exigés ({added} o), {deposit} joints", "Insufficient storage deposit: {near} required ({added} bytes), {near} attached."],
    ["Dépôt insuffisant pour le stockage : {} yoctoNEAR", "Insufficient storage deposit: {near}."],
    ["Must attach {} yoctoNEAR to cover storage", "Must attach {near} to cover storage."],
  ],
  E_OUT_OF_BOUNDS: [
    ["Out of bounds, please use a smaller from_index.", "Out of bounds, please use a smaller from_index."],
  ],
  E_ZERO_LIMIT: [["Cannot provide limit of 0.", "Cannot provide limit of 0."]],
  E_LIST_NOT_OWNER: [["Seul le propriétaire peut vendre", "Only the owner can list this card."]],
  E_ZERO_PRICE: [["Prix nul", "The price must be greater than zero."]],
  E_ALREADY_LISTED: [["Déjà en vente", "This card is already listed."]],
  E_LISTING_DEPOSIT: [["Dépôt d'annonce : {} yoctoNEAR requis", "Listing deposit: {near} required."]],
  E_NOT_LISTED: [["Pas en vente", "This card is not listed."]],
  E_NOT_SELLER: [["Seul le vendeur peut retirer l'annonce", "Only the seller can remove this listing."]],
  E_PRICE_CHANGED: [["Le prix de l'annonce a changé", "The listing price has changed."]],
  E_SELF_BUY: [["Le vendeur ne peut pas acheter sa carte", "The seller cannot buy their own card."]],
  E_STALE_LISTING: [["Annonce périmée", "This listing is outdated."]],
  E_DEPOSIT_BELOW_PRICE: [["Dépôt inférieur au prix", "The attached deposit is lower than the price."]],
  E_BURN_NOT_OWNER: [["Seul le propriétaire peut brûler", "Only the owner can burn this card."]],
  E_LISTED_CANNOT_BURN: [
    ["Carte en vente : retirez l'annonce d'abord", "This card is listed: remove the listing first."],
  ],
  E_NO_REDEEMER: [["Aucun redeemer configuré", "No redeemer configured."]],
  E_NOT_BURNABLE: [["Carte non brûlable", "This card is not burnable."]],
  E_BURN_IN_PROGRESS: [["Burn déjà en cours", "A burn is already in progress for this card."]],
  E_SEL_HEX: [["sel : hex invalide", "sel: invalid hex."]],
  E_SEL_LENGTH: [["sel : 32 octets exactement", "sel: exactly 32 bytes."]],
  E_CARD_ID: [["card_id invalide", "Invalid card_id."]],
  E_TITLE: [["title invalide", "Invalid title."]],
  E_URL_LENGTH: [["URL trop longue", "URL too long."]],
  E_UNKNOWN_MYTHIC: [["Index de mythique inconnu", "Unknown mythic index."]],
  E_MYTHIC_REVEALED: [["Mythique déjà révélée", "Mythic already revealed."]],
  E_MYTHIC_NOT_DRAWN: [["Mythique jamais sortie : révélation refusée", "This mythic was never drawn: reveal refused."]],
  E_COMMITMENT_MISMATCH: [
    ["sha256(card_id || sel) ne correspond pas à l'engagement", "sha256(card_id || sel) does not match the commitment."],
  ],
  E_CONTENT_MISMATCH: [["Le contenu ne correspond pas à content_hash", "The content does not match content_hash."]],
  E_NOT_OWNER: [["Réservé à l'owner", "Owner only."]],
  E_NOTHING_TO_WITHDRAW: [["Rien à retirer", "Nothing to withdraw."]],
  E_WITHDRAW_LIMIT: [
    ["Retrait refusé : {} yoctoNEAR demandés, {} retirables (engagements {})", "Withdrawal refused: {near} requested, {near} withdrawable (commitments {near})."],
  ],
  E_INIT_PARAM: [
    ["reveal_steps hors bornes", "reveal_steps out of bounds."],
    ["retry_delay_blocks ≥ {MIN_RETRY_DELAY_BLOCKS} (sinon un tiers peut bloquer un pack en Stuck)", "retry_delay_blocks must be ≥ {MIN_RETRY_DELAY_BLOCKS}."],
  ],
  E_NO_ORACLE_PROPOSAL: [["Aucun changement d'oracle proposé", "No oracle change proposed."]],
  E_ORACLE_DELAY: [
    ["Délai du changement d'oracle non écoulé : bloc {} au plus tôt", "Oracle change delay not elapsed: block {} at the earliest."],
  ],
  E_NO_ORACLE: [["Aucun oracle de prix configuré", "No price oracle configured."]],
  E_NOT_ORACLE: [["Réservé à l'oracle de prix", "Price oracle only."]],
  E_UNKNOWN_CARD_INDEX: [["Index de carte inconnu", "Unknown card index."]],
  E_NOT_RESURRECTABLE: [
    ["Carte non ressuscitable : absente de mechanics.resurrection.eligible (table hachée)", "This card cannot be resurrected: not in mechanics.resurrection.eligible (hashed table)."],
  ],
  E_RESURRECT_RARITY: [
    ["Résurrection réservée aux cartes épiques et légendaires", "Resurrection is for epic and legendary cards only."],
  ],
  E_ALREADY_BACKED: [["Carte déjà adossée par la table", "This card is already backed by the table."]],
  E_LENGTH: [["{what} : longueur invalide", "{what}: invalid length."]],
  E_BACKING_AMOUNT: [["amount doit être > 0", "amount must be > 0."]],
  E_PRICE: [["Le prix doit être > 0", "The price must be > 0."]],
  E_CARDS_PER_PACK: [["cards_per_pack hors bornes", "cards_per_pack out of bounds."]],
  E_TOO_MANY_MYTHICS: [["Trop de mythiques", "Too many mythics."]],
  E_WEIGHTS_ZERO: [
    ["Poids de rareté nuls", "Rarity weights are all zero."],
    ["{what} : poids nuls", "{what}: weights are all zero."],
  ],
  E_COMMITMENT_FORMAT: [
    ["commitment : 64 caractères hex minuscules", "commitment: 64 lowercase hex characters."],
    ["content_hash : 64 caractères hex minuscules", "content_hash: 64 lowercase hex characters."],
  ],
  E_MYTHIC_CAP: [["Plafond de mythique hors bornes", "Mythic cap out of bounds."]],
  E_DUPLICATE_COMMITMENT: [
    ["Engagement en double", "Duplicate commitment."],
    ["content_hash en double", "Duplicate content_hash."],
  ],
  E_MYTHIC_WEIGHT: [
    ["Poids mythique sans engagement de poids non nul", "Mythic weight without a commitment of non-zero weight."],
    ["{what} : poids mythique sans engagement de poids non nul", "{what}: mythic weight without a commitment of non-zero weight."],
  ],
  E_ROYALTIES: [
    ["Redevances > 50 %", "Royalties > 50 %."],
    ["Trop de redevances", "Too many royalties."],
  ],
  E_VISIBLE_MYTHIC: [["Les mythiques passent par des engagements", "Mythics must be commitments."]],
  E_RARITY_WEIGHT: [["Carte dans une rareté de poids nul", "Card in a rarity of zero weight."]],
  E_DUPLICATE_CARD_ID: [
    ["card_id en double", "Duplicate card_id."],
    ["card_id en double ou hors ordre (par lots, card_id strictement croissants)", "Duplicate or out-of-order card_id (batched loading: strictly increasing card_id)."],
  ],
  E_RARITY_WITHOUT_CARD: [["Rareté {} sans carte", "Rarity {} has no card."]],
  E_NO_UNLIMITED_COMMON: [
    ["Il faut au moins une commune sans plafond et de poids non nul", "At least one uncapped common of non-zero weight is required."],
  ],
  E_TOO_MANY_CARDS: [
    ["Trop de cartes", "Too many cards."],
    ["Trop de cartes pour un appel ({} au plus) : utiliser append_series_cards", "Too many cards for one call ({} at most): use append_series_cards."],
  ],
  E_BATCH_SIZE: [["Lot de 1 à {} cartes", "Batch of 1 to {} cards."]],
  E_DRAFT_DELETED: [
    ["Brouillon déjà supprimé", "Draft already deleted."],
    ["Brouillon supprimé", "Draft deleted."],
  ],
  E_TABLE_FROZEN: [
    ["Série déjà ouverte", "Series already open."],
    ["Table figée : série déjà ouverte", "Table frozen: series already open."],
  ],
  E_NOT_BATCHED: [
    ["Série complète : append_series_cards suit create_series_batched", "Complete series: append_series_cards follows create_series_batched."],
  ],
  E_NOT_DRAFT: [["Seul un brouillon peut être supprimé", "Only a draft can be deleted."]],
  E_STATUS_TRANSITION: [["Transition de statut invalide", "Invalid status transition."]],
  E_TABLE_FORMAT: [
    ["Motif \"cards\":[ présent plusieurs fois dans l'en-tête", "Pattern \"cards\":[ appears more than once in the header."],
  ],
  E_MECH_VALUE: [
    ["value : prix trop élevé pour ces valeurs et multiplicateurs (dépassement de u128)", "value: price too high for these values and multipliers (u128 overflow)."],
    ["value.multipliers.mythic = 0 (une mythique garde l'adossement de son contenu)", "value.multipliers.mythic = 0 (a mythic keeps the backing of its content)."],
    ["value.multipliers.{} : 1 à {MAX_VALUE_MULT}", "value.multipliers.{}: 1 to {MAX_VALUE_MULT}."],
    ["value.{what} : 1 à {MAX_VALUE_TIERS} paliers", "value.{what}: 1 to {MAX_VALUE_TIERS} tiers."],
    ["value.{what} : poids nuls interdits", "value.{what}: zero weights are not allowed."],
    ["value.{what} : valeur hors de [{min_bps}, {max_bps}] points de base", "value.{what}: value outside [{min_bps}, {max_bps}] basis points."],
  ],
  E_MECH_GOLD: [
    ["gold.slots : 1 à 10 emplacements", "gold.slots: 1 to 10 slots."],
    ["gold.slots[{i}] : poids sous le plancher {}", "gold.slots[{i}]: weight below the floor {}."],
  ],
  E_MECH_PITY: [
    ["pity : gold pack inatteignable (p_max_ppb = 0 sans n_max)", "pity: gold pack unreachable (p_max_ppb = 0 without n_max)."],
    ["pity : p0_ppb ≤ p_max_ppb", "pity: p0_ppb ≤ p_max_ppb."],
    ["pity : probabilités en ppb (≤ 10⁹)", "pity: probabilities in ppb (≤ 10⁹)."],
    ["pity exige gold", "pity requires gold."],
    ["pity.n_max hors bornes (absent, ou 1 à 10 000)", "pity.n_max out of bounds (absent, or 1 to 10,000)."],
  ],
  E_MECH_RESURRECTION: [
    ["resurrection.eligible : 200 cartes au plus", "resurrection.eligible: 200 cards at most."],
    ["resurrection.eligible : carte déjà adossée par la table", "resurrection.eligible: card already backed by the table."],
    ["resurrection.eligible : cartes épiques et légendaires seulement", "resurrection.eligible: epic and legendary cards only."],
    ["resurrection.eligible : index de carte inconnu", "resurrection.eligible: unknown card index."],
    ["resurrection.eligible : index strictement croissants", "resurrection.eligible: strictly increasing indexes."],
  ],
  E_MECH_BURN: [
    ["burn.floor_bps ≤ 10 000", "burn.floor_bps ≤ 10,000."],
    ["burn.prior_k ≤ 1 000 000", "burn.prior_k ≤ 1,000,000."],
  ],
  E_MECH_RUSH: [
    ["rush : 1 à 96 seaux", "rush: 1 to 96 buckets."],
    ["rush : fenêtre courte plus courte que la fenêtre longue", "rush: the short window must be shorter than the long window."],
    ["rush : seaux et durée ≥ 1 bloc", "rush: buckets and duration ≥ 1 block."],
    ["rush : window_blocks et baseline_blocks multiples de bucket_blocks", "rush: window_blocks and baseline_blocks must be multiples of bucket_blocks."],
    ["rush.max_per_account ≥ 1", "rush.max_per_account ≥ 1."],
    ["rush.min_packs ≥ 1", "rush.min_packs ≥ 1."],
    ["rush.ratio_bps inatteignable pour ces fenêtres", "rush.ratio_bps unreachable for these windows."],
    ["rush.ratio_bps ≥ 10 000 (×1)", "rush.ratio_bps ≥ 10,000 (×1)."],
  ],
  E_MECH_BURNABLE: [
    ["Brûlable garantie : il faut une carte adossée par la table, sans plafond et de poids non nul", "Guaranteed burnable: a table-backed, uncapped card of non-zero weight is required."],
  ],
  E_TEST_HOOK: [["test-hooks: échec simulé du dernier reçu", "test-hooks: simulated failure of the last receipt."]],
  E_INTERNAL: [
    ["Bloc de cartes manquant", "Internal error (card chunk)."],
    ["Bloc de liste manquant", "Internal error (list chunk)."],
    ["Bloc de liste vide", "Internal error (list chunk)."],
    ["Blocs de cartes incohérents", "Internal error (card chunks)."],
    ["Carte de table inconnue", "Internal error (table card)."],
    ["Champ cards introuvable", "Internal error (cards field)."],
    ["En-tête : tableau cards non vide", "Internal error (non-empty header cards)."],
    ["Hash de chargement absent", "Internal error (loading hash)."],
    ["JSON impossible", "Internal error (JSON)."],
    ["Liste du propriétaire incohérente", "Internal error (owner list)."],
    ["Liste globale incohérente", "Internal error (global list)."],
    ["Sérialisation de la table impossible", "Internal error (serialization)."],
    ["Sérialisation impossible", "Internal error (serialization)."],
    ["Table non hachée", "Internal error (table not hashed)."],
  ],
};

// Messages sans code : contrat app2 (texte français seul), protocole et wallet. Le premier qui correspond l'emporte.
const LEGACY: [RegExp, string][] = [
  [/Dépôt insuffisant/, "Insufficient deposit: the attached amount must cover the pack price plus the storage deposit."],
  // Le message propre au burn avant le message générique (le premier qui correspond l'emporte).
  [/Gaz insuffisant pour le burn/, "Not enough gas attached for the burn. Please try again."],
  [/Gaz insuffisant/, "Not enough gas attached to the transaction. Please try again."],
  [/Série non ouverte/, "This series is not on sale right now."],
  [/Série inconnue/, "This pack series does not exist."],
  [/Délai de relance non écoulé/, "The reveal can only be retried a little later. Please wait a few seconds."],
  [/Tirage déjà écrit/, "This pack is already revealed."],
  [/Pack inconnu/, "Unknown pack."],
  [/Seul le propriétaire peut brûler/, "Only the owner of this card can burn it."],
  [/Carte en vente : retirez/, "This card is listed for sale. Remove the listing before burning it."],
  [/Burn déjà en cours/, "A burn is already in progress for this card."],
  [/Carte non brûlable/, "This card is not burnable."],
  [/Aucun redeemer/, "Burning is not available right now."],
  [/Le prix de l'annonce a changé/, "The listing price changed. Please check the new price."],
  [/Déjà en vente/, "This card is already listed."],
  [/Prix nul|Le prix doit être > 0/, "The price must be greater than zero."],
  [/Dépôt d'annonce/, "Listing a card requires a small storage deposit, returned when the listing ends."],
  [/Pas en vente/, "This card is not listed anymore."],
  [/Le vendeur ne peut pas acheter/, "You cannot buy your own card."],
  [/Annonce périmée/, "This listing is outdated."],
  [/Dépôt inférieur au prix/, "The attached amount is lower than the price."],
  [/Carte en cours de burn/, "This card is being burned."],
  [/Seul le propriétaire peut vendre/, "Only the owner can list this card."],
  [/Seul le vendeur peut retirer/, "Only the seller can remove this listing."],
  [/Carte inconnue/, "Unknown card."],
  [/NotEnoughBalance|LackBalanceForState|not enough balance/i, "Your wallet balance is too low for this transaction."],
  [/reject|cancel|denied|closed|User rejected/i, "Transaction cancelled in the wallet."],
];

const CODE_RE = /\b(E_[A-Z0-9_]+): ([^"\\\n]*)/;
const PLACEHOLDER = /\{[^}]*\}/g;

/** Code `E_…` d'un message d'échec et le texte qui le suit, ou `null` (message sans code). */
export function errorCode(raw: string): { code: string; text: string } | null {
  const m = raw.match(CODE_RE);
  return m ? { code: m[1], text: m[2].trim() } : null;
}

const escapeRe = (s: string) => s.replace(/[.*+?^$()|[\]{}\\]/g, "\\$&");

/** Texte français d'ERRORS.md → expression qui capture les valeurs insérées (`whole` : jusqu'à la fin). */
function frPattern(fr: string, whole: boolean): RegExp {
  return new RegExp(`^${fr.split(PLACEHOLDER).map(escapeRe).join("(.+?)")}${whole ? "$" : ""}`);
}

function fill(en: string, values: string[]): string {
  let i = 0;
  return en.replace(PLACEHOLDER, (p) => {
    const v = values[i++]?.trim();
    if (!v) return "…";
    return p === "{near}" && /^\d+$/.test(v) ? `${formatNearExact(v)} NEAR` : v;
  });
}

/** Traduction d'un message à code, ou `undefined` si le code n'est pas connu. */
export function translateCode(code: string, text: string): string | undefined {
  const variants = CODE_MESSAGES[code];
  if (!variants) return undefined;
  // Variante dont le français correspond en entier, sinon le plus long préfixe, sinon la première sans valeurs.
  for (const whole of [true, false]) {
    const hits = variants
      .map(([fr, en]) => ({ fr, en, m: text.match(frPattern(fr, whole)) }))
      .filter((h) => h.m)
      .sort((a, b) => b.fr.length - a.fr.length);
    if (hits.length) return fill(hits[0].en, hits[0].m!.slice(1));
  }
  return fill(variants[0][1], []);
}

export function humanError(e: unknown): string {
  const raw = (e instanceof Error ? e.message : typeof e === "string" ? e : JSON.stringify(e)) ?? "";
  const coded = errorCode(raw);
  const translated = coded && translateCode(coded.code, coded.text);
  if (translated) return translated;
  for (const [re, msg] of LEGACY) if (re.test(raw)) return msg;
  return raw.length > 200 ? raw.slice(0, 200) + "…" : raw || "Something went wrong.";
}
