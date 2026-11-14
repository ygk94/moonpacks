# Memaster contract error codes

Every `require!` and every panic in the contract starts with a **stable code**, followed by `: ` and a human-readable
message. In the deployed build, the message text after the code is in **French**; it may change between versions.
Clients should rely on the code only, which will not change, and use the English descriptions below to display or
handle the error. In the descriptions, `{}` stands for values inserted at runtime (amounts, indexes, field names).

Extracting the code from a failure: match `/\b(E_[A-Z0-9_]+): /` against the panic message (`FunctionCallError` /
`ExecutionError`).

The test `tests_v3::every_error_has_a_stable_code_listed_in_errors_md` fails if a `require!` or a panic in the
contract has no code, if a code is missing from this file, or if this file lists a code that no longer exists.

"Who" column: `public` for an error any user can trigger (buying, market, burn, transfers), `revealer` for
`reveal_mythic`, `owner` and `oracle` for administration methods, `internal` for an invariant that can only fail
because of a bug.

**Messages without a code**, produced by near-sdk and not customizable: `Method X is private` (`#[private]` method),
`Method X doesn't accept deposit` (deposit attached to a method that is not `#[payable]`), argument deserialization
errors (`Failed to deserialize input from JSON`), `The contract is not initialized`, and the
`NFTContractMetadata::assert_valid` checks at initialization. Protocol errors (`NotEnoughBalance`,
`LackBalanceForState`, gas exhausted) do not come from the contract.

| Code | Description | Who | Files |
|---|---|---|---|
| `E_GAS` | Not enough gas attached to buy a pack: {} required. | public | pack.rs |
| `E_GAS` | Not enough gas attached for the burn. | public | redeem.rs |
| `E_GAS` | Not enough gas attached for nft_transfer_call. | public | nft.rs |
| `E_SERIES_NOT_ON_SALE` | The series is not on sale. | public | pack.rs |
| `E_DEPOSIT` | Insufficient deposit when buying a pack: {} yoctoNEAR required (price {} + storage {}). | public | pack.rs |
| `E_RETRY_TOO_EARLY` | The reveal of the pack cannot be retried yet (retry delay not elapsed). | public | pack.rs |
| `E_ALREADY_REVEALED` | The pack draw is already written: retry refused. | public | pack.rs |
| `E_ALREADY_REVEALED` | The pack draw is already written: refund refused. | public | pack.rs |
| `E_ALREADY_REFUNDED` | The pack has already been refunded. | public | pack.rs |
| `E_NOT_STUCK` | Only a stuck pack can be refunded. | public | pack.rs |
| `E_NOT_PACK_OWNER` | Only the buyer of the pack can retry the reveal. | public | pack.rs |
| `E_PRICE_TOO_HIGH` | Listing price too high: {} yoctoNEAR at most. | public | market.rs |
| `E_AMOUNT_TOO_LARGE` | Amount too large for the royalty computation. | public | nft.rs |
| `E_UNKNOWN_PACK` | Unknown pack. | public | nft.rs, pack.rs |
| `E_UNKNOWN_KIND` | Unknown pack type in this series. | public | pack.rs, views.rs |
| `E_UNKNOWN_SERIES` | Unknown series. | public | lib.rs, pack.rs, series.rs |
| `E_SERIES_NOT_OPEN` | The series is not open. | owner, oracle | mechanics.rs, series.rs |
| `E_UNKNOWN_CARD` | Unknown card. | public | market.rs, nft.rs, redeem.rs |
| `E_TOKEN_NOT_FOUND` | Token not found. | public | nft.rs |
| `E_NOT_APPROVED` | Sender not approved for this token. | public | nft.rs |
| `E_APPROVAL_ID` | The actual approval_id {:?} is different from the given approval_id {:?}. | public | nft.rs |
| `E_SAME_OWNER` | Current and next owner must differ. | public | nft.rs |
| `E_CARD_REDEEMING` | The card is being burned: it cannot be listed. | public | market.rs |
| `E_CARD_REDEEMING` | The card is being burned: transfer refused. | public | nft.rs |
| `E_PAYOUT_TOO_LONG` | The payout is longer than max_len_payout. | public | nft.rs |
| `E_ONE_YOCTO` | Requires an attached deposit of at least 1 yoctoNEAR. | public | nft.rs |
| `E_ONE_YOCTO` | Requires an attached deposit of exactly 1 yoctoNEAR. | public | lib.rs |
| `E_NOT_TOKEN_OWNER` | The predecessor must be the token owner. | public | nft.rs |
| `E_STORAGE_DEPOSIT` | Insufficient storage deposit: {cost} yoctoNEAR required ({added} bytes), {deposit} attached. | public (revealer), owner, oracle | series.rs |
| `E_STORAGE_DEPOSIT` | Insufficient storage deposit: {} yoctoNEAR. | public (revealer), owner, oracle | mechanics.rs, mythic.rs |
| `E_STORAGE_DEPOSIT` | Must attach {} yoctoNEAR to cover storage. | public | nft.rs |
| `E_OUT_OF_BOUNDS` | Out of bounds in a paginated view: use a smaller from_index. | public | nft.rs |
| `E_ZERO_LIMIT` | A paginated view was called with a limit of 0. | public | nft.rs |
| `E_LIST_NOT_OWNER` | Only the owner of the card can list it. | public | market.rs |
| `E_ZERO_PRICE` | The listing price must be greater than zero. | public | market.rs |
| `E_ALREADY_LISTED` | The card is already listed. | public | market.rs |
| `E_LISTING_DEPOSIT` | Listing deposit: {} yoctoNEAR required. | public | market.rs |
| `E_NOT_LISTED` | The card is not listed. | public | market.rs |
| `E_NOT_SELLER` | Only the seller can remove the listing. | public | market.rs |
| `E_PRICE_CHANGED` | The listing price has changed since the buyer read it. | public | market.rs |
| `E_SELF_BUY` | The seller cannot buy their own card. | public | market.rs |
| `E_STALE_LISTING` | The listing is outdated. | public | market.rs |
| `E_DEPOSIT_BELOW_PRICE` | The attached deposit is lower than the listing price. | public | market.rs |
| `E_BURN_NOT_OWNER` | Only the owner of the card can burn it. | public | redeem.rs |
| `E_LISTED_CANNOT_BURN` | The card is listed: remove the listing before burning it. | public | redeem.rs |
| `E_NO_REDEEMER` | No redeemer is configured. | public | redeem.rs |
| `E_NOT_BURNABLE` | The card is not burnable. | public | redeem.rs |
| `E_BURN_IN_PROGRESS` | A burn is already in progress for this card. | public | redeem.rs |
| `E_SEL_HEX` | Mythic reveal: the salt is not valid hex. | public (revealer) | mythic.rs |
| `E_SEL_LENGTH` | Mythic reveal: the salt must be exactly 32 bytes. | public (revealer) | mythic.rs |
| `E_CARD_ID` | Mythic reveal: invalid card_id. | public (revealer) | mythic.rs |
| `E_TITLE` | Mythic reveal: invalid title. | public (revealer) | mythic.rs |
| `E_URL_LENGTH` | Mythic reveal: URL too long. | public (revealer) | mythic.rs |
| `E_UNKNOWN_MYTHIC` | Unknown mythic index. | public (revealer) | mythic.rs |
| `E_MYTHIC_REVEALED` | The mythic is already revealed. | public (revealer) | mythic.rs |
| `E_MYTHIC_NOT_DRAWN` | The mythic was never drawn: reveal refused. | public (revealer) | mythic.rs |
| `E_COMMITMENT_MISMATCH` | sha256(card_id \|\| salt) does not match the commitment. | public (revealer) | mythic.rs |
| `E_CONTENT_MISMATCH` | The revealed content does not match content_hash. | public (revealer) | mythic.rs |
| `E_NOT_OWNER` | The method is restricted to the contract owner. | owner | lib.rs |
| `E_NOTHING_TO_WITHDRAW` | There is nothing to withdraw from the treasury. | owner | treasury.rs |
| `E_WITHDRAW_LIMIT` | Withdrawal refused: {} yoctoNEAR requested, {} withdrawable (commitments {}). | owner | treasury.rs |
| `E_INIT_PARAM` | Initialization: reveal_steps out of bounds. | owner (init) | lib.rs |
| `E_INIT_PARAM` | Initialization: retry_delay_blocks must be at least {MIN_RETRY_DELAY_BLOCKS} (otherwise a third party could force a pack into the stuck state). | owner (init) | lib.rs |
| `E_NO_ORACLE_PROPOSAL` | No oracle change has been proposed. | owner | lib.rs |
| `E_ORACLE_DELAY` | The oracle change delay has not elapsed: block {} at the earliest. | owner | lib.rs |
| `E_NO_ORACLE` | No price oracle is configured. | oracle | mechanics.rs |
| `E_NOT_ORACLE` | The method is restricted to the price oracle. | oracle | mechanics.rs |
| `E_UNKNOWN_CARD_INDEX` | Unknown card index. | oracle | mechanics.rs |
| `E_NOT_RESURRECTABLE` | The card cannot be resurrected: it is not in mechanics.resurrection.eligible (hashed table). | oracle | mechanics.rs |
| `E_RESURRECT_RARITY` | Resurrection is for epic and legendary cards only. | oracle | mechanics.rs |
| `E_ALREADY_BACKED` | The card is already backed by the table. | oracle | mechanics.rs |
| `E_LENGTH` | {what}: invalid length. | owner | series.rs |
| `E_BACKING_AMOUNT` | The backing amount must be greater than zero. | owner, oracle | series.rs |
| `E_PRICE` | The series price must be greater than zero. | owner | series.rs |
| `E_CARDS_PER_PACK` | cards_per_pack out of bounds. | owner | series.rs |
| `E_KINDS` | Invalid pack types in the series (size, name, price, cards, slot rules or guaranteed burnable). | owner | mechanics.rs |
| `E_TOO_MANY_MYTHICS` | Too many mythics in the series. | owner | series.rs |
| `E_WEIGHTS_ZERO` | The rarity weights are all zero. | owner | series.rs |
| `E_WEIGHTS_ZERO` | {what}: the weights are all zero. | owner | mechanics.rs |
| `E_COMMITMENT_FORMAT` | commitment must be 64 lowercase hex characters. | owner | series.rs |
| `E_COMMITMENT_FORMAT` | content_hash must be 64 lowercase hex characters. | owner | series.rs |
| `E_MYTHIC_CAP` | Mythic cap out of bounds. | owner | series.rs |
| `E_DUPLICATE_COMMITMENT` | Duplicate mythic commitment. | owner | series.rs |
| `E_DUPLICATE_COMMITMENT` | Duplicate content_hash. | owner | series.rs |
| `E_MYTHIC_WEIGHT` | Non-zero mythic weight without any mythic commitment. | owner | series.rs |
| `E_MYTHIC_WEIGHT` | {what}: non-zero mythic weight without any mythic commitment. | owner | mechanics.rs |
| `E_ROYALTIES` | Total royalties exceed 50 %. | owner | series.rs |
| `E_ROYALTIES` | Too many royalty recipients. | owner | series.rs |
| `E_VISIBLE_MYTHIC` | Mythics must be declared as commitments, not as visible cards. | owner | series.rs |
| `E_RARITY_WEIGHT` | A card belongs to a rarity whose weight is zero. | owner | series.rs |
| `E_DUPLICATE_CARD_ID` | Duplicate card_id. | owner | series.rs |
| `E_DUPLICATE_CARD_ID` | Duplicate or out-of-order card_id (batched loading requires strictly increasing card_id). | owner | series.rs |
| `E_RARITY_WITHOUT_CARD` | Rarity {} has no card. | owner | series.rs |
| `E_NO_UNLIMITED_COMMON` | At least one uncapped common card of non-zero weight is required. | owner | series.rs |
| `E_TOO_MANY_CARDS` | Too many cards in the series. | owner | series.rs |
| `E_TOO_MANY_CARDS` | Too many cards for one call ({} at most): use append_series_cards. | owner | series.rs |
| `E_BATCH_SIZE` | A batch must contain 1 to {} cards. | owner | series.rs |
| `E_DRAFT_DELETED` | The draft series has already been deleted. | owner | series.rs |
| `E_DRAFT_DELETED` | The draft series has been deleted. | owner | series.rs |
| `E_TABLE_FROZEN` | The series is already open. | owner | series.rs |
| `E_TABLE_FROZEN` | The card table is frozen: the series is already open. | owner | series.rs |
| `E_NOT_BATCHED` | The series is complete: append_series_cards only follows create_series_batched. | owner | series.rs |
| `E_NOT_DRAFT` | Only a draft series can be deleted. | owner | series.rs |
| `E_STATUS_TRANSITION` | Invalid series status transition. | owner | series.rs |
| `E_TABLE_FORMAT` | The pattern "cards":[ appears more than once in the table header. | owner | hash_stream.rs |
| `E_MECH_VALUE` | value: price too high for these values and multipliers (u128 overflow). | owner | mechanics.rs |
| `E_MECH_VALUE` | value.multipliers.mythic is 0 (a mythic keeps the backing of its content). | owner | mechanics.rs |
| `E_MECH_VALUE` | value.multipliers.{} must be 1 to {MAX_VALUE_MULT}. | owner | mechanics.rs |
| `E_MECH_VALUE` | value.{what} must have 1 to {MAX_VALUE_TIERS} tiers. | owner | mechanics.rs |
| `E_MECH_VALUE` | value.{what}: zero weights are not allowed. | owner | mechanics.rs |
| `E_MECH_VALUE` | value.{what}: value outside [{min_bps}, {max_bps}] basis points. | owner | mechanics.rs |
| `E_MECH_GOLD` | gold.slots must have 1 to 10 slots. | owner | mechanics.rs |
| `E_MECH_GOLD` | gold.slots[{i}]: weight below the floor {}. | owner | mechanics.rs |
| `E_MECH_PITY` | pity: gold pack unreachable (p_max_ppb = 0 without n_max). | owner | mechanics.rs |
| `E_MECH_PITY` | pity: p0_ppb must be ≤ p_max_ppb. | owner | mechanics.rs |
| `E_MECH_PITY` | pity: probabilities are in ppb (≤ 10⁹). | owner | mechanics.rs |
| `E_MECH_PITY` | pity requires gold. | owner | mechanics.rs |
| `E_MECH_PITY` | pity.n_max out of bounds (absent, or 1 to 10,000). | owner | mechanics.rs |
| `E_MECH_RESURRECTION` | resurrection.eligible: 200 cards at most. | owner | mechanics.rs |
| `E_MECH_RESURRECTION` | resurrection.eligible: card already backed by the table. | owner | mechanics.rs |
| `E_MECH_RESURRECTION` | resurrection.eligible: epic and legendary cards only. | owner | mechanics.rs |
| `E_MECH_RESURRECTION` | resurrection.eligible: unknown card index. | owner | mechanics.rs |
| `E_MECH_RESURRECTION` | resurrection.eligible: indexes must be strictly increasing. | owner | mechanics.rs |
| `E_MECH_BURN` | burn.floor_bps must be ≤ 10,000. | owner | mechanics.rs |
| `E_MECH_BURN` | burn.prior_k must be ≤ 1,000,000. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush: 1 to 96 buckets. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush: the short window must be shorter than the long window. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush: buckets and duration must be ≥ 1 block. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush: window_blocks and baseline_blocks must be multiples of bucket_blocks. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush.max_per_account must be ≥ 1. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush.min_packs must be ≥ 1. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush.ratio_bps is unreachable for these windows. | owner | mechanics.rs |
| `E_MECH_RUSH` | rush.ratio_bps must be ≥ 10,000 (×1). | owner | mechanics.rs |
| `E_MECH_BURNABLE` | Guaranteed burnable: a table-backed, uncapped card of non-zero weight is required. | owner | mechanics.rs |
| `E_TEST_HOOK` | test-hooks build only: simulated failure of the last receipt. | tests | pack.rs |
| `E_INTERNAL` | Internal error: missing card chunk. | internal | series.rs, views.rs |
| `E_INTERNAL` | Internal error: missing list chunk. | internal | nft.rs, pack.rs |
| `E_INTERNAL` | Internal error: empty list chunk. | internal | nft.rs |
| `E_INTERNAL` | Internal error: inconsistent card chunks. | internal | lib.rs, views.rs |
| `E_INTERNAL` | Internal error: unknown table card. | internal | lib.rs |
| `E_INTERNAL` | Internal error: cards field not found. | internal | hash_stream.rs |
| `E_INTERNAL` | Internal error: non-empty cards array in the table header. | internal | hash_stream.rs |
| `E_INTERNAL` | Internal error: missing loading hash. | internal | series.rs |
| `E_INTERNAL` | Internal error: JSON serialization failed. | internal | hash_stream.rs, series.rs |
| `E_INTERNAL` | Internal error: inconsistent owner list. | internal | nft.rs |
| `E_INTERNAL` | Internal error: inconsistent global list. | internal | nft.rs |
| `E_INTERNAL` | Internal error: table serialization failed. | internal | series.rs |
| `E_INTERNAL` | Internal error: serialization failed. | internal | mythic.rs |
| `E_INTERNAL` | Internal error: table not hashed. | internal | pack.rs |
