// Types des vues du contrat (contract/src/views.rs, types.rs). Les montants U128 sont des chaînes.

export type Rarity = "common" | "rare" | "epic" | "legendary" | "mythic";
export const RARITIES: Rarity[] = ["common", "rare", "epic", "legendary", "mythic"];
export const RARITY_RANK: Record<Rarity, number> = { common: 0, rare: 1, epic: 2, legendary: 3, mythic: 4 };

export type CardKind = "visible" | "mythic";
export type CardState = "normal" | "redeeming" | "burned";
// `refunded` (v3) : pack `stuck` remboursé par `refund_stuck_pack`, état final.
export type PackStatus = "pending" | "revealed" | "stuck" | "refunded";
export type PackMode = "base" | "gold" | "rush";

export interface Backing {
  asset_id: string;
  amount: string;
}

export interface Listing {
  seller_id: string;
  price: string;
  deposit: string;
}

export interface SeriesView {
  series_id: number;
  status: "draft" | "open" | "paused" | "closed" | "deleted";
  name: string;
  price: string;
  cards_per_pack: number;
  table_hash: string | null;
  storage_per_pack: number;
  required_deposit: string;
  min_gas: string;
  packs_sold: number;
  card_count: number;
  /** Types de packs de la série (packs thématiques, contrat avec `kinds`). Absent sur app2 et app3. */
  kinds?: PackKindView[];
}

/** Type de pack d'une série, tel que `get_series` le décrit. */
export interface PackKindView {
  kind: number;
  name: string;
  price: string;
  required_deposit: string;
  cards_per_pack: number;
  card_count: number;
  mythics: boolean;
  value: boolean;
  slots: { floor: Rarity; weights: Record<Rarity, number> | null; burnable: boolean }[] | null;
}

export interface CardDef {
  card_id: string;
  title: string;
  rarity: Rarity;
  weight: number;
  cap: number | null;
  media: string | null;
  backing: Backing | null;
}

export interface CardView {
  token_id: string;
  owner_id: string;
  series_id: number;
  kind: CardKind;
  index: number;
  card_id: string | null;
  rarity: Rarity;
  state: CardState;
  sealed: boolean;
  backing: Backing | null;
  listing: Listing | null;
}

export interface DrawRecord {
  slot: number;
  rolled_rarity: Rarity;
  final_rarity: Rarity;
  kind: CardKind;
  index: number;
  token_id: string;
}

export interface PackView {
  pack_id: number;
  /** Type de pack (pack thématique), `null` pour le pack de base. */
  kind?: number | null;
  series_id: number;
  owner_id: string;
  price_paid: string;
  storage_prepaid: string;
  /** v3 : stockage mesuré du pack (octets). Absent sur app2. */
  storage_used?: number;
  bought_at_height: number;
  status: PackStatus;
  attempt: number;
  step: number;
  last_progress_height: number;
  token_ids: string[];
  draws: DrawRecord[];
  rush: boolean;
  mode: PackMode;
  value: { bps: number; total: string; amounts: (string | null)[] } | null;
}

export interface RushState {
  enabled: boolean;
  params?: {
    ratio_bps: number;
    min_packs: number;
    window_blocks: number;
    baseline_blocks: number;
    bucket_blocks: number;
    duration_blocks: number;
    cooldown_blocks: number;
    max_per_account: number;
  };
  height?: number;
  last_trigger?: number | null;
  rush_until?: number | null;
  rush_count?: number;
  window_count?: number;
  baseline_count?: number;
  start_height?: number | null;
  pause_until?: number | null;
  active?: boolean;
  account?: { account_id: string; rush_packs: number; remaining: number } | null;
}

export interface ContractConfig {
  owner_id: string;
  redeemer_id: string | null;
  reveal_steps: number;
  retry_delay_blocks: number;
  gas: { min_entry: string; min_redeem: string };
  listing_deposit: string;
  next_pack_id: number;
  total_supply: number;
}

export interface NftToken {
  token_id: string;
  owner_id: string;
  metadata: { title: string | null; media: string | null; extra: string | null } | null;
}

export interface RatesCard {
  index?: number;
  mythic_index?: number;
  card_id?: string;
  commitment?: string;
  weight: number;
  cap: number | null;
  minted: number;
  burnable?: boolean;
  ppm: number;
  ppb: number;
}

export interface RatesRarity {
  rarity: Rarity;
  rarity_ppb: number;
  rush_rarity_ppb: number | null;
  gold_slot_ppb: number[] | null;
  cards: RatesCard[];
}

export interface RatesPage {
  series_id: number;
  table_hash: string | null;
  card_count: number;
  from_index: number;
  next_index: number | null;
  rarities: RatesRarity[];
}

/** Événement NEP-297 du contrat (`standard: "memaster"`). */
export interface MemasterEvent {
  standard: string;
  version: string;
  event: string;
  data: Record<string, unknown>[];
}
