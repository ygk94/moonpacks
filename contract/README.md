# Moonpacks contract (NEAR, Rust)

A single NEAR contract (crate name `memaster`) that sells memecoin trading-card packs as NFTs. It holds the card
NFTs, sells and reveals packs with on-chain randomness, keeps sealed "mythic" cards behind hash commitments, runs an
integrated marketplace, burns backed cards against an abstract redeemer, and implements the series mechanics (gold
packs and pity, burn-driven rarity, gold rush, resurrection of dead coins, random token value per pack, pack kinds).
The full mechanics reference is [`docs/mechanics.md`](../docs/mechanics.md).

**Testnet only, never deployed to mainnet.**

| Deployment | Account | Notes |
|---|---|---|
| Current (v4, pack kinds) | `app4.simpletea5483.testnet` | Used by the web app, https://moonpacks-ochre.vercel.app |
| Previous (v3) | `app3.memaster-demo-j7xg7z.testnet` | Storage refunds, stuck-pack refund, treasury |
| Previous (v2) | `app2.memaster-demo-j7xg7z.testnet` | Gold pack, value tables, anonymous mythics |
| Previous (v1) | `app.memaster-demo-j7xg7z.testnet` | No mechanics, no value |

Each version changed the Borsh state layout, so each one lives on a fresh account (no in-place migration).

Toolchain: near-sdk 5.30.1, near-contract-standards 5.30.1, cargo-near 0.23.0. Sandbox tests use near-workspaces
0.24.0 and cargo-near-build 0.11.5.

## Source layout

| File | Role |
|---|---|
| `src/lib.rs` | State, `new`, gas / limit / storage constants, `set_redeemer`, price-oracle role, card metadata rebuilt on read, `token_id_of` / `parse_token_id` |
| `src/types.rs` | Series table and mechanics (`SeriesTable`, `Mechanics`, `GoldSlot`, `ValueParams`, `PackKind`), cards, mythic commitments, compact pack records |
| `src/series.rs` | Series lifecycle: create (single call or batched), append, replace, delete draft, open, pause, resume, close |
| `src/hash_stream.rs` | Incremental SHA-256 of the table JSON, maintained while the table is loaded in batches |
| `src/pack.rs` | `buy_pack`, chained `reveal_step` receipts, `retry_reveal`, `refund_stuck_pack`, final draw and mint, storage metering |
| `src/draw.rs` | Pure, deterministic draw (also the reference for the off-chain verifier): pity, burn weights, rush window, gold slots and fallback, pack kinds, value split |
| `src/mechanics.rs` | Mechanics validation, burn counters, `set_resurrected`, mechanics views |
| `src/mythic.rs` | `reveal_mythic`, `compute_mythic_commitment` |
| `src/market.rs` | `list`, `delist`, `buy` |
| `src/redeem.rs` | `redeem`, `on_redeem_complete`, `Redeemer` interface |
| `src/treasury.rs` | `get_treasury`, `withdraw_revenue` |
| `src/nft.rs` | NEP-171 core, NEP-177 metadata, NEP-178 approvals, NEP-181 enumeration, NEP-199 payouts, rewritten on top of the compact per-card storage |
| `src/views.rs` | Read-only views |
| `src/events.rs` | NEP-297 events (`standard: "memaster"`, `version: "1.0.0"`) |
| `src/tests*.rs` | Unit tests (see [Tests](#tests)) |
| `tests/sandbox.rs` | Integration tests and gas / storage measurements on near-sandbox |
| `mock-redeemer/` | Test redeemer: records `redeem(owner, asset_id, amount)` or panics on demand |
| `mock-oracle/` | Test price oracle: `push_resurrection` forwards to `set_resurrected` (reads no price) |
| `ERRORS.md` | Stable error codes (`E_...`), checked by a unit test |
| `scripts/` | Series building, validation and testnet deployment (see [Scripts](#scripts)) |
| `series-v4/` | Prebuilt call arguments for the two v4 series (`classic`, `full-moon`) |

## Data model

- **Series.** Stored in a `Vector`, identified by index (`u32`), never reused. Status: draft, open, paused, closed
  or deleted. A series carries a frozen `SeriesTable` plus mutable counters kept outside the table (`minted` per
  card, burn counters, rush ring buffer).
- **`SeriesTable`** (JSON field order is part of the hash and is locked by
  `hash_stream::tests::series_table_field_order_is_locked`): `name`, `price`, `cards_per_pack` (1 to 10),
  `rarity_weights` (common, rare, epic, legendary, mythic), `cards` (visible cards: id, rarity, weight, optional cap,
  media, optional backing), `mythics` (commitments only), `royalties` (NEP-199, at most 10, at most 50 % total),
  then the optional `mechanics` and `kinds`. Optional fields are omitted from the JSON when absent, so an older table
  keeps exactly the same bytes and hash.
- **Table hash.** `table_hash = sha256(serde_json::to_vec(table))`, computed when the series is opened and stored.
  These are exactly the bytes returned by `get_series_table`, and also the bytes rebuilt from `get_series_header`
  plus all pages of `get_series_cards`, which is what the verifier does.
- **Limits.** 200 cards per call, 2 000 cards and 20 mythics per series, mythic cap at most 100, 16 pack kinds per
  series. Every rarity with a non-zero weight needs at least one card (or a weighted commitment for mythics), and
  there must be at least one uncapped common, so a draw can never fail.
- **Cards (compact).** `token_id = pack_id * 10 + slot`. A card only stores a 10-byte `CardSlot` (owner, state,
  list positions) and a 31-byte `PackDraw` (rolls, rarity, kind, index) inside its pack. NEP-177 metadata, backing
  and the sealed state of mythics are rebuilt on read from the table. NEP-181 lists are stored in chunks
  (8 bytes per card).
- **Packs.** `Pending` → `Revealed`, or `Pending` → `Stuck` → `Refunded`. A pack records its series, optional kind,
  seeds, attempt counter, storage used and, for value tables, the drawn value (7 bytes).
- **Per-account state.** Pack list per owner (paginated), pity counter per (account, series), rush cap entry per
  (account, series).

## Series lifecycle (owner)

| Method | Notes |
|---|---|
| `create_series(table)` | Creates a draft in one call (at most 200 cards). Storage paid by the contract. |
| `create_series_batched(table)` | Payable. Header, mythics and first batch of cards. The deposit must cover the measured storage increase (10^19 yoctoNEAR per byte); the excess is refunded and the kept amount is accumulated in `storage_deposit`. |
| `append_series_cards(series_id, cards)` | Payable, same storage rule. At most 200 cards per call; `card_id`s must be strictly increasing (UTF-8 bytes) across batches, which guarantees uniqueness without rereading the table. |
| `replace_series_table(series_id, table)` / `replace_series_table_batched(...)` | Drafts only. |
| `delete_draft(series_id)` | Drafts only. Frees cards, counters, mythics and hash stream, refunds freed storage to the owner, capped at what the owner paid. The series id stays as a small `deleted` stub. |
| `open_series(series_id)` | Checks coverage rules, finalizes and stores `table_hash`, computes worst-case pack storage. The table is frozen forever: no method writes an open table. Returns the hash. |
| `pause_series` / `resume_series` / `close_series` | Sales only. Reveals, the market and burns keep working during a pause. |

The table hash is computed incrementally (`hash_stream.rs`): header up to `"cards":[` at creation, each card on
append, the tail at opening. That cut requires the pattern `"cards":[` to appear exactly once in the serialized
header (this is why pack kinds use `pool` instead of `cards`).

## Buying and revealing a pack

1. **`buy_pack(series_id, kind)`**, one signature. `kind` is `null` for the base pack or a pack-kind index. The
   deposit must be at least `price + worst-case storage` (`get_series(id).required_deposit`, or the per-kind value
   in `get_series(id).kinds`) and the attached gas at least `get_series(id).min_gas` (160 Tgas with k = 3). Excess
   deposit is refunded immediately. The price is then earned, except for a stuck pack (step 6).
2. **Commit chain.** `acc0 = sha256("memaster:pack" || pack_id_le || owner || table_hash)`, then `k` private
   `reveal_step` receipts (k = 3 by default, 2 to 6, set in `new`), each computing
   `acc = sha256(acc || env::random_seed() || pack_id_le || owner)`. Gas per receipt is fixed by the contract
   (`ENTRY_OWN_GAS` 20 Tgas, `INTERMEDIATE_STEP_GAS` 10 Tgas, `FINAL_STEP_GAS` 120 Tgas). Each contract-created
   receipt runs in a later block, so the seeds of several block producers enter `acc`.
3. **Final draw** (last receipt). With mechanics, the pack's rate table is chosen first: gold pack if the pity roll
   succeeds, otherwise the rush table if the pack was bought during a rush (frozen at purchase), otherwise the base
   table. Each slot then draws a rarity (`rarity_roll`), falls back to a lower rarity if that rarity is exhausted
   by caps, and draws a card (`card_roll`, with burn-driven weights). With a value table, the last slot of a normal
   pack is drawn among burnable cards, and `value_roll` picks the pack value, which is split among the pack's
   burnable cards. Exact formulas and tags: [`docs/mechanics.md`](../docs/mechanics.md).
4. **Mint and log.** Cards are minted directly (never via `*_transfer_call`). `pack_revealed` logs seeds, block
   heights, intermediate and final `acc`, every draw, a `storage` block and, for mechanics series, a `mechanics`
   block (`mode`, `rush`, `pity`, `burn_seq`, `resurrect_seq`, `value`). Unused prepaid storage
   (`storage_per_pack - storage_used`) is refunded to the buyer by a plain transfer.
5. **Stale steps** (wrong attempt, wrong order, pack already revealed or not pending) are ignored without panicking.
   **`retry_reveal(pack_id)`** is reserved to the pack buyer, only while the pack is `Pending` with no card written,
   and only after `retry_delay_blocks` blocks without progress (100 by default, at least 20). It bumps the attempt
   counter, which invalidates older steps.
6. **Stuck and refund.** After `MAX_ATTEMPTS` (10) failed attempts, the next `retry_reveal` moves the pack to
   `Stuck` (`pack_stuck`). `refund_stuck_pack(pack_id)` can be called by anyone, always pays the buyer (price plus
   unused prepaid storage), moves the pack to the final `Refunded` state and emits `pack_refunded`.

There is no cancel method. `refund_stuck_pack` is the only refund path, and it rejects revealed packs (checked
against the ABI by a sandbox test).

**Why a failed draw cannot be exploited.** The last receipt has no failure path that depends on the result: fixed
gas, prepaid storage, no `require` on cards, value or counters, and the storage refund is an outgoing transfer always
covered by the balance (`withdraw_revenue` keeps commitments and a reserve). A failed last receipt's seed is public
(`hash(action_hash || random_value)`), so its would-be result can be recomputed, but nobody can make only bad draws
fail. A revealed pack can never become `Stuck`, so there is no free re-roll.

**Known limit.** A block producer knows its block's seed before including the last receipt and could withhold it.
`k > 1` does not help against the last producer; it only prevents a single actor (the buyer or the producer of the
purchase block) from fixing the result at purchase time. There is no external VRF.

## Sealed mythics

- The public table only lists, per mythic, `commitment = sha256(card_id || sel)`,
  `content_hash = sha256(json(MythicContent) || sel)`, weight and cap (mandatory, at most 100). Odds are public
  (`get_rates`) without revealing which coin it is. The second hash binds title, media and backing, so the owner
  cannot choose the backing after the fact.
- `sel` must be exactly 32 bytes and unique per mythic; duplicate commitments or content hashes are rejected.
  Generate commitments offline with `python3 scripts/gen_mythics.py INPUT.json PUBLIC.json SECRETS.json`
  (example input: `scripts/example-mythics.json`). Preimages go to `scripts/secrets/`, which is git-ignored.
- On first draw the card is minted **sealed** (`mythic_drawn`). Whoever holds the preimage calls
  `reveal_mythic`; the contract checks both hashes, refuses a mythic that was never drawn, makes the backing
  available to `redeem`, and publishes `card_id`, `sel` and content in `mythic_revealed` and
  `get_mythic_commitments`. The revealer pays the added storage.
- Mythic metadata is anonymous before and after reveal: title `?`, description `?`, the same `?` image
  (`MYTHIC_MEDIA`), `extra` limited to `series_id`, `rarity`, `pack_id`. `get_card` never returns `card_id` or
  backing for a mythic. A sealed card can be transferred and sold but not burned.
- `compute_mythic_commitment` is a convenience view; calling it over RPC sends the secret to that node, so prefer
  computing commitments offline.

## Pack kinds (v4)

A series can offer themed pack kinds alongside its base pack (`SeriesTable.kinds`, `PackKind`): `name` (1 to 32
bytes, unique), `price`, `cards_per_pack` (1 to 10), `pool` (strictly increasing card indexes, empty = all cards),
`mythics` (whether mythics can drop), `slots` (optional per-slot rule: rarity floor, own weights, burnable-only),
and `value` (apply the series value table, scaled to the kind's price).

Kinds draw from the **same table, with the same `minted` counters and caps** as the base pack: nothing is
reprinted, and a card drawn in a themed pack counts toward its series-wide cap. A kind never yields a gold pack and
does not move the pity counter; it uses the rush table during a rush. Buy with `buy_pack(series_id, kind)`; the
deposit is the kind's price plus the series worst-case storage. `pack_bought` and `pack_revealed` carry `kind` only
for kind packs, so base-pack events keep their previous shape. Errors: `E_KINDS` (validation), `E_UNKNOWN_KIND`
(purchase). Details: [`docs/mechanics.md`](../docs/mechanics.md), section 13.

The deployed v4 contract has two series: series 0 "Moonpacks Classic" with nine kinds (Dog, Cat, Frog, Solana,
BNB Chain, Ethereum, OG 1, OG 2, OG 5) and series 1 "Moonpacks Full Moon" (base pack only).

## Mechanics (summary)

All mechanics parameters live in `SeriesTable.mechanics` and are therefore covered by `table_hash`. Every piece of
state that influences a draw is frozen and logged, so the verifier replays every pack from events alone.

- **Gold pack and pity.** Per (account, series) counter; gold chance grows from 1 in 50 000 to at most 1 in 25 000
  (no guarantee by default). A gold pack has per-slot rarity floors.
- **Burn-driven rarity.** Burning a card lowers its weight among the burnable cards of its rarity (floor 25 %,
  smoothed by a prior), without changing rarity odds.
- **Gold rush.** A traffic spike relative to the last 24 h triggers a rush window with boosted odds, capped per
  account.
- **Resurrection.** A trusted price oracle can make a hashed list of epic and legendary "dead" cards burnable.
  Oracle changes are two-step: `propose_price_oracle`, then `accept_price_oracle` after `oracle_delay_blocks`
  (144 000 blocks by default); `revoke_price_oracle` is immediate.
- **Value per pack.** A random value (normal table 20 % to 200 % of the price) split among the pack's burnable cards
  by rarity multiplier; `redeem` passes each card's share to the redeemer.

## Marketplace

- `list(token_id, price)`: 0.005 NEAR deposit (refunded on delist or sale), price at most 10^9 NEAR
  (`MAX_LISTING_PRICE`).
- `delist(token_id)`.
- `buy(token_id, expected_price)`: the expected price protects against a seller relisting higher just before the
  purchase. The seller receives the price minus the series royalties; excess deposit is refunded.
- Any transfer removes the listing. Listed cards cannot be burned, and nothing is allowed on a card in `Redeeming`.

## Burn (redeem)

`redeem(token_id)` (1 yoctoNEAR, at least 70 Tgas, owner only, backed card, not listed) moves the card to
`Redeeming`, then calls `redeemer.redeem(owner, asset_id, amount)` (30 Tgas) and the private
`on_redeem_complete` (20 Tgas). If the redeemer receipt succeeds, the card is burned, burn counters are updated
(`card_redeemed`), and the freed storage is refunded to the owner. If it fails, the card returns to `Normal`
(`redeem_failed`). In a value-table series, `amount` is the card's share of the pack value, not the table amount.
**Interface contract: the redeemer must panic if it does not deliver.** The redeemer is trusted and set by the owner
with `set_redeemer`; token sourcing is out of scope of this contract.

## Treasury

`withdraw_revenue(amount)` (owner, 1 yoctoNEAR; `null` withdraws everything withdrawable) can only withdraw
`balance - commitments`, where commitments are occupied storage, listing deposits, escrow of pending and stuck packs,
the value reserved for live burnable cards, and a 1 NEAR reserve (`TREASURY_MIN_RESERVE`). Emits
`revenue_withdrawn`. Backings that are not in NEAR (fixed table backings, mythics) are not reserved.

## Storage deposits

- **Buyers** prepay a worst-case bound (`storage_per_pack`, computed at opening for 64-character accounts and a
  first purchase). Each pack receipt meters what it writes (`Pack::storage_used`) and the last receipt refunds the
  difference. On testnet this means about 1 040 bytes used on an account's first purchase and about 600 bytes
  afterwards, out of 1 605 bytes prepaid.
- **Burns** refund the bytes freed (list entries, emptied chunks, approvals), never more. The pack slot itself
  stays, because it anchors other cards' `token_id`s and value shares.
- **Owner** pays storage for batched series loading and gets it back from `delete_draft`. `scripts/build_series.py`
  writes the deposit for each call into `manifest.json` (`deposits`).
- **Oracle** pays for `set_resurrected`; the **revealer** pays for `reveal_mythic`.
- The contract itself pays for retry seeds and for list entries of market buyers and transfer recipients.
- Approvals storage is refunded on transfer, sale and burn, as in the NEP-178 standard.

## Public methods

### Change methods

| Method | Caller | Notes |
|---|---|---|
| `new(owner_id, redeemer_id, metadata, reveal_steps, retry_delay_blocks, oracle_delay_blocks)` | contract account (`#[private]`) | Init |
| `set_redeemer(redeemer_id)` | owner | |
| `propose_price_oracle(price_oracle_id)` / `accept_price_oracle()` / `revoke_price_oracle()` | owner | Two-step oracle change |
| `create_series`, `create_series_batched`, `append_series_cards`, `replace_series_table`, `replace_series_table_batched`, `delete_draft`, `open_series`, `pause_series`, `resume_series`, `close_series` | owner | See [Series lifecycle](#series-lifecycle-owner) |
| `buy_pack(series_id, kind)` | anyone | Payable |
| `reveal_step(pack_id, attempt, step)` | contract (`#[private]`) | Chained reveal receipts |
| `retry_reveal(pack_id)` | pack buyer | |
| `refund_stuck_pack(pack_id)` | anyone | Pays the buyer |
| `reveal_mythic(series_id, mythic_index, card_id, sel, content)` | preimage holder | Payable (storage) |
| `set_resurrected(series_id, card_index, backing)` | price oracle | Payable (storage) |
| `list(token_id, price)`, `delist(token_id)`, `buy(token_id, expected_price)` | card owner / buyer | |
| `redeem(token_id)` | card owner | 1 yoctoNEAR |
| `on_redeem_complete(...)` | contract (`#[private]`) | Redeem callback |
| `withdraw_revenue(amount)` | owner | 1 yoctoNEAR |
| `nft_transfer`, `nft_transfer_call`, `nft_resolve_transfer`, `nft_approve`, `nft_revoke`, `nft_revoke_all`, `nft_transfer_payout` | standard | NEP-171 / 178 / 199 |

`nft_transfer_call` is reimplemented to give `nft_resolve_transfer` a fixed 15 Tgas (5 in near-contract-standards)
and requires at least 45 Tgas. `nft_resolve_transfer` removes a listing only if the card actually returns to the
previous owner.

The `test-hooks` Cargo feature adds `test_set_reveal_failure` (owner), which makes the last reveal receipt fail. It
exists only for retry / stuck / treasury tests and **must never be deployed**.

### Views

| View | Notes |
|---|---|
| `get_config` | Owner, redeemer, oracle (and pending oracle), reveal steps, delays, gas constants, listing deposit, counters |
| `get_series_count`, `get_series(series_id)` | Includes `required_deposit`, `min_gas`, status, counters, `kinds` |
| `get_series_header(series_id)` | Table without cards, stored `table_hash`, `card_count`, `storage_deposit` |
| `get_series_cards(series_id, from_index, limit)` | Paginated, at most 200 cards per page |
| `get_series_table_hash(series_id)` | Stored hash, never recomputed |
| `get_series_table(series_id)` | Whole table; small series only (expensive at maximum size) |
| `get_rates(series_id, from_index, limit)` | Per-rarity sums over the whole table, paginated card list, all mythic commitments |
| `get_kind_rates(series_id, kind, from_index, limit)` | Same, restricted to a pack kind's pool and rules |
| `get_mythic_commitments(series_id)` | Commitments and revealed preimages |
| `compute_mythic_commitment(card_id, sel, content)` | Helper (sends the secret to the RPC node) |
| `get_pack(pack_id)` | Status, draws, `kind`, price paid, `storage_used`, value |
| `get_pack_count_for_owner(account_id)`, `get_packs_for_owner(account_id, from_index, limit)` | Paginated, at most 100 per call |
| `get_card(token_id)`, `get_backing(token_id)` | Card view and current backing (value share in value-table series) |
| `get_listing(token_id)`, `get_listings(from_index, limit)` | Marketplace |
| `get_pity(account_id, series_id)` | `n`, `p_ppb`, `packs_to_max`, `guaranteed_in`, params |
| `get_rush_state(series_id, at_height, account_id)` | Rush window and per-account remaining rush packs |
| `get_burns(series_id, from_index, limit)` | Burn counters, paginated |
| `get_resurrected(series_id, card_index)` | Oracle backing, if any |
| `get_treasury` | Balance, storage, commitments, withdrawable |
| `nft_token`, `nft_tokens`, `nft_tokens_for_owner`, `nft_total_supply`, `nft_supply_for_owner`, `nft_metadata`, `nft_is_approved`, `nft_payout` | NEP-171 / 177 / 178 / 181 / 199 |

## Events

NEP-297, logged as `EVENT_JSON:{"standard":"memaster","version":"1.0.0","event":...,"data":[...]}`. NEP-171
events (`nft_mint`, `nft_transfer`, `nft_burn`) use the standard format. No `nft_metadata_update` is emitted.

| Area | Events |
|---|---|
| Admin | `redeemer_set`, `price_oracle_proposed`, `price_oracle_accepted`, `price_oracle_revoked`, `revenue_withdrawn` |
| Series | `series_created`, `series_cards_appended`, `series_opened`, `series_closed`, `series_draft_deleted` |
| Packs | `pack_bought`, `reveal_step`, `reveal_retried`, `pack_revealed`, `pack_stuck`, `pack_refunded` |
| Mythics | `mythic_drawn`, `mythic_revealed` |
| Market | `card_listed`, `card_delisted`, `card_sold` |
| Burn and oracle | `redeem_started`, `card_redeemed`, `redeem_failed`, `card_resurrected` |

## Errors

Every `require!` and panic message starts with a stable code (`E_...: `). The full list is in
[`ERRORS.md`](ERRORS.md); the unit test `tests_v3::every_error_has_a_stable_code_listed_in_errors_md` fails if a
message has no code or if the list is out of date.

## Build and test

```bash
cd contract
rustup target add wasm32-unknown-unknown        # required by cargo-near
cargo install cargo-near --locked               # 0.23.0

cargo near build non-reproducible-wasm          # -> target/near/memaster.wasm
(cd mock-redeemer && cargo near build non-reproducible-wasm)
(cd mock-oracle && cargo near build non-reproducible-wasm)

cargo test --lib                                # unit tests (python3 needed for script and fuzz tests)
MEMASTER_FUZZ_CASES=5000 cargo test --lib tests_fuzz -- --nocapture   # longer differential fuzz (MEMASTER_FUZZ_SEED to replay)
cargo test --test sandbox -- --nocapture        # sandbox integration tests, measurements printed
cargo test                                      # everything

python3 -m unittest discover -s scripts/tests   # Python script tests
```

Sandbox tests build their own wasm files (production, `--features test-hooks`, mocks) into `target/near-test/`.
The first run downloads the near-sandbox binary, so it needs network access.

## Tests

- **Unit tests** (about 160, `src/tests.rs`, `tests_batch.rs`, `tests_mech.rs`, `tests_v3.rs`, `tests_kinds.rs`,
  `tests_limits.rs`, `tests_fuzz.rs`, `hash_stream.rs`): table validation, hash equal to the view bytes, frozen
  tables, deposit and gas checks, full draws, stale steps, retry rules, cap fallback, draw frequencies, mythic
  commitments, market and royalties, burns, batched loading (same hash, view and draws as a single-call table),
  mechanics (pity, burns, rush, resurrection, gold slots, value split down to the last yocto), storage refunds,
  stuck refunds, treasury limits, error codes, and pack kinds.
- **Differential fuzz** (`tests_fuzz.rs`): random valid tables and states, compared bit for bit with the Python
  verifier (`verifier/`); the offline validator `scripts/validate_series.py` is checked against `validate_table`
  on randomly mutated tables. Pack-kind draws are cross-checked between Rust, Python and TypeScript through
  `verifier/tests/vectors/kind_vectors.json`.
- **Sandbox** (22 tests, `tests/sandbox.rs`), including: `buy_pack_and_measurements`, `distribution_over_300_packs`,
  `mythic_reveal_and_commitment_check`, `integrated_market`, `burn_success_and_failure`, `no_cancellation_possible`,
  `retry_reveal_after_failed_draw`, `worst_case_fits_in_270_tgas`, `catalogue_v2_batched_load_and_packs`,
  `max_size_series_fits`, `mechanics_end_to_end`, `value_and_gold_pack_end_to_end`,
  `worst_case_cascade_with_burns_fits`, `stuck_pack_is_refunded_once`, `withdraw_revenue_respects_commitments`,
  `draft_storage_is_paid_by_owner_and_refunded_on_delete`.

## Gas and storage (measured)

| Case | Result |
|---|---|
| Required gas for `buy_pack` | `min_gas = 20 + (k - 1) x 10 + 120 = 160 Tgas` with k = 3, under the 270 Tgas per-transaction ceiling of the MetaMask adapter |
| Testnet pack (v3 demo series, 5 cards) | 29.4 to 31.1 Tgas burned in total, `buy_pack` about 8 Tgas, last receipt 14.3 to 15.8 Tgas |
| Worst case last receipt (2 000 cards, 10 per pack, all mechanics, cascading exhausted rarities) | about 50 Tgas out of a fixed 120 |
| Buyer cost | deposit plus gas actually burned (about 0.002 to 0.003 NEAR); the account must temporarily hold the prepaid gas (about 0.16 NEAR at 160 Tgas) |
| Successful `redeem` | about 9 Tgas in sandbox; `on_redeem_complete` under its 20 Tgas budget |
| `reveal_mythic` with 100 sealed cards | 5 Tgas |
| Maximum-size series (2 000 cards) | loaded in batches, `open_series` about 11 Tgas, about 16.6 NEAR of owner-paid storage |
| Light views at maximum size | `get_series_header` 4.7 Tgas, `get_series_table_hash` 4.3 Tgas, a 200-card page of `get_series_cards` / `get_rates` 22 to 34 Tgas |

## Scripts

All scripts run from `contract/` with python3 (standard library only, plus `verifier/` for hashing).

| Script | Role |
|---|---|
| `scripts/build_series.py PARAMS.json` | Builds the series call arguments from a catalogue (`--catalogue`, default `docs/data/catalogue-v2.json`) and a parameter file (`scripts/serie-exemple.json`, `serie-demo-entree.json`, `serie-demo-standard.json`). Writes `scripts/out/<slug>/`: `create_series_batched.json`, `append_series_cards.NN.json`, `open_series.json`, `table.json` (exact bytes of `get_series_table`), `table_hash.txt` and `manifest.json` (with per-call `deposits`). Options: `--series-id`, `--tables-valeur` (value tables), `--media-base`, `--sels` (reuse salts), `--new-secrets`, `--mythiques` (git-ignored file with the real mythic identities), `--secrets`, `--out`. Refuses to write if a real mythic name would appear in a public output, and runs `validate_series.py`. |
| `scripts/validate_series.py DIR_OR_TABLE` | Run before `open_series` (an open table is frozen forever). Re-implements the contract's table rules offline, checks batches against `table.json` and `table_hash.txt`, mean value per table (rush at most 80 %, normal at most 100 %), mythic preimages (`--secrets`), and scans public files for leaked secrets (`--scan`, `--git`). `validate_series.py --git` alone runs the leak check over all tracked files. |
| `scripts/build_v4.py` | Builds the two v4 series into `series-v4/classic` and `series-v4/full-moon` (same output format as `build_series.py`). It rereads the public v3 tables from `--source` (default `app3.memaster-demo-j7xg7z.testnet`), checks their hash, keeps the same mythic commitments, renames the series, points card media to `--media-base` (default `https://moonpacks-ochre.vercel.app/cards`), and adds the nine pack kinds of series 0 using the front-end pack filters applied to `--catalog` (default `front/public/catalog.json`). No secret needed. |
| `scripts/deploy_testnet.sh` | Idempotent testnet deployment (refuses anything but testnet; each completed step is skipped on rerun): builds the wasm files, creates the contract, redeemer and oracle sub-accounts, deploys and initializes them, installs the oracle in two steps, loads one series in batches with the manifest deposits, checks the on-chain draft against the local table (card count, hash, `validate_series.py`) before opening it, and optionally creates a control series without mechanics. Keys are read from `~/.near-credentials` (or the system keychain with `KEYCHAIN=system`); nothing is read from or written to the repo. Main variables: `ROOT_ID` (required), `CONTRACT_ID`, `REDEEMER_ID`, `ORACLE_ID`, `SERIES_ID`, `SERIES_PARAMS`, `SERIES_OUT`, `PREBUILT=1`, `SECRETS`, `SKIP_BUILD=1`, `SKIP_CONTROL=1`, `BUYERS`. See the header of the script for the full list. |
| `scripts/deploy_v4.sh` | One-command v4 deployment: runs `deploy_testnet.sh` twice with `PREBUILT=1` to create `app4`, `redeemer4` and `oracle4` under `ROOT_ID`, then loads and opens series 0 (`series-v4/classic`) and series 1 (`series-v4/full-moon`). No test buyers. Costs roughly 11 NEAR for the contract account, about 6.3 NEAR of series storage deposits and 3 NEAR for the mocks. |
| `scripts/gen_mythics.py` | Generates mythic commitments and git-ignored preimages (see [Sealed mythics](#sealed-mythics)). |

Example (v4, current deployment):

```bash
cd contract
python3 scripts/build_v4.py                                   # optional: series-v4/ is versioned
ROOT_ID=<your-account>.testnet ./scripts/deploy_v4.sh         # creates app4.<your-account>.testnet
```

Example of a single batched call with near-cli-rs:

```bash
near contract call-function as-transaction <contract> append_series_cards \
  file-args scripts/out/<slug>/append_series_cards.01.json prepaid-gas '300 Tgas' \
  attached-deposit '<manifest deposits value> yoctonear' sign-as <owner> network-config testnet sign-with-keychain send
```

## Known limits

- **Randomness.** The producer of the last receipt's block knows the seed and can withhold the block. No external VRF.
- **Trusted roles.** The redeemer and the price oracle are trusted; the contract checks neither prices nor token
  inventory. A redeemer that succeeds without delivering breaks the burn guarantee. If `on_redeem_complete` ran out
  of gas, the card would stay in `Redeeming`.
- **Mythic reveal is off-chain.** Until the preimage holder reveals, a drawn mythic stays sealed and cannot be
  burned.
- **Rush cap is per account.** A many-account (Sybil) actor can bypass it; the expected gain is bounded in
  [`docs/mechanics.md`](../docs/mechanics.md), section 4. Rush coverage (at most 80 %) is only checked off-chain.
- **Value.** The contract draws and splits a value in yoctoNEAR and passes it to the redeemer; it does not fund it.
- **Owner key.** The owner keeps a full-access key and builds are not reproducible: open tables are immutable by
  code, not by governance.
- **Coverage.** Measured on sandbox and testnet only. Gold packs and mythics have not been drawn on testnet (odds too
  low); those paths are covered by unit and sandbox tests.
