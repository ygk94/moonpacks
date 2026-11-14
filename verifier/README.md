# Moonpacks verifier

`memaster_verifier` lets anyone check the Moonpacks contract (`../contract/`) from public chain data only: the
series table, the contract's NEP-297 events (`pack_bought`, `pack_revealed`, `card_redeemed`, `card_resurrected`,
`mythic_revealed`) and the NEAR RPC.

- Python 3.9+, **standard library only** (nothing to install).
- Independent reimplementation: `core.py` follows the contract's draw algorithm (`contract/src/draw.rs`) and
  `canon.py` reproduces `serde_json` serialization for the table hash and mythic commitments. No Rust code is
  reused; byte-for-byte agreement is checked against vectors produced by the contract itself (see [Tests](#tests)).
  The web app runs the same checks in the browser (`../front/src/verify/`).

## What is verified

| Command | Check |
|---|---|
| `table` | Reads the series table page by page (`get_series_header`, then `get_series_cards` at the same block), checks each page and the card count, **recomputes the table hash locally** and compares it with the hash stored when the series was opened. With `--file`, hashes a local table (its canonical form). Prints the weights per rarity. |
| `pack` | For a `pack_revealed` event: event `table_hash` equals `sha256(table)`; `initial_acc = sha256("memaster:pack" ‖ pack_id_le ‖ owner ‖ table_hash)`; each `acc = sha256(acc ‖ seed ‖ pack_id_le ‖ owner)` over the logged seeds (retries included); then, for every slot, rarity roll, target rarity, fallback, card roll and card. Also checks pack types (themed packs), the storage refund, and the series mechanics below. |
| `mythic` | `sha256(card_id ‖ salt) = commitment` and `sha256(json(content) ‖ salt) = content_hash`, against the commitments **in the hashed table**, not those the event claims. The salt must be 32 bytes. |
| `stats` | Chi-squared test of the rolled rarities against the published weights, then of the cards within each uncapped rarity. `--replay` also replays and verifies every draw from the series opening. |
| `code` | The deployed account's `code_hash` equals the sha256 (base58) of a local wasm. |

### Mechanics replay

Everything that influences a draw is logged, so a series with mechanics is **replayed from events alone**
(`verify.SeriesReplay`): pity counter and gold-pack decision, rate table (base, rush, gold), gold-pack slots and
floors, pack value tier and its split between burnable cards, gold rush state (from `pack_bought`), burn-weighted
card choice and resurrections. A missing `pack_bought`, burn or resurrection is reported as an error or as a
partial check. See [`../docs/mechanics.md`](../docs/mechanics.md) for the rules.

### Cap state

Card choice depends on how many copies were already minted. `pack` gets that state from one of:

1. `--snapshot FILE`: `minted` / `mythic_minted` just before the draw (the output of `get_series` works);
2. `--history FILE`: all events of the series in execution order, replayed from the opening (most reliable);
3. `--rpc` alone: `get_series` read at the block before the draw's last receipt (needs an archival node for old
   draws);
4. `--no-state`: partial check (seed chain, rarity roll and target rarity, downward fallback; not the card roll).

## What cannot be verified

- **Seed origin.** The verifier starts from the logged seeds. That each seed is the receipt's `env::random_seed()`
  relies on the deployed code.
- **Block producer influence.** The producer of the last block knows its seed and could withhold the block. No
  script can detect this; the contract uses no external VRF.
- **Event completeness.** Replays assume a complete, ordered event list (from an indexer or archival node). Sequence
  numbers detect a missing burn or resurrection; the order of two draws finalized in the same block follows the file.
- **Source code.** `code` compares the deployed code with a local wasm; without a reproducible build, this does not
  prove the wasm comes from the published source.
- **Unrevealed mythics.** Before reveal, only the commitment, weight and cap are public.
- NFT `token_id`s and metadata, the price oracle's resurrection decision, and failed draws (whose state is rolled
  back) are not checked.

## Usage

Run from `verifier/`:

```sh

# Table hash, read page by page from the chain
python3 -m memaster_verifier table --rpc testnet --contract app4.simpletea5483.testnet --series 0
# ... or from a file
python3 -m memaster_verifier table --file table.json --expected-hash <hex>

# A pack from its transaction (buy_pack, or retry_reveal)
python3 -m memaster_verifier pack --rpc testnet --contract app4.simpletea5483.testnet \
    --tx-hash <hash> --sender alice.testnet
# ... with the full series history for the cap state
python3 -m memaster_verifier pack --rpc testnet --contract app4.simpletea5483.testnet \
    --tx-hash <hash> --sender alice.testnet --history series0.jsonl
# Offline: event, table and snapshot from files
python3 -m memaster_verifier pack --event ev.json --table table.json --snapshot get_series.json
# Whole series replayed from its opening
python3 -m memaster_verifier pack --event series0.jsonl --table table.json

# Mythic reveal
python3 -m memaster_verifier mythic --rpc testnet --contract app4.simpletea5483.testnet --series 0
python3 -m memaster_verifier mythic --event mythic_revealed.json --table table.json

# Observed frequencies vs published odds, with full replay
python3 -m memaster_verifier stats --events series0.jsonl --table table.json --replay

# Deployed code vs a local wasm
python3 -m memaster_verifier code --rpc testnet --contract app4.simpletea5483.testnet --wasm memaster.wasm
```

Options per command:
- all: `--rpc` (URL, `testnet` = `https://rpc.testnet.fastnear.com`, or `mainnet`), `--contract`
- `table`: `--series`, `--file`, `--expected-hash`, `--page-size` (max 200), `--draft` (table loaded but not yet opened)
- `pack`: `--event`, `--tx-hash`, `--sender`, `--pack-id`, `--table`, one of `--snapshot` / `--history` /
  `--no-state`, `-v`
- `mythic`: `--series`, `--index`, `--event`, `--table`, `--card-id`, `--sel` (hex salt), `--content`
- `stats`: `--events FILE...` (required), `--series`, `--table`, `--alpha` (default 0.001), `--replay`
- `code`: `--wasm` (required)

Without `--table`, `pack`, `mythic` and `stats` read the table from the chain and refuse it if its recomputed hash
differs from the stored one. Event files may be a JSON object, a list, JSONL, or raw `EVENT_JSON:{…}` log lines.
On HTTP 429 the RPC client retries with backoff (or `Retry-After`).

Exit codes: `0` verified, `1` mismatch (or significant statistical deviation), `2` input or RPC error.

## Tests

```sh
cd verifier
python -m unittest discover -s tests -t .
```

Offline; a few tests are skipped when optional local build outputs are absent.

### Cross-language test vectors

The vectors in `tests/vectors/` are generated from the compiled contract code by the Rust crate `vectorgen/`, which
depends on `../contract` without modifying it:

- `draw_vectors.json`: random tables (caps reached, zero weights, mythics, extreme `pack_id`s, tricky Unicode)
  covering serialization, table hash, `initial_acc`, `mix`, `roll`, full draws and mythic commitments;
- `mech_vectors.json`: tables with mechanics (pity, gold packs, burns, resurrections, pack value, value split,
  gold rush sequences);
- `kind_vectors.json`: pack types (themed packs);
- `sandbox_vectors.json` / `sandbox_mech_vectors.json`: real events from the contract wasm deployed in
  near-sandbox; the test also runs this CLI against the sandbox RPC;
- `fuzz_vectors.json`: a fixed fuzz corpus from the contract's own tests (`contract/src/tests_fuzz.rs`).

Regenerate:

```sh
cd verifier/vectorgen
cargo test --test gen_vectors -- draw_vectors mech_vectors kind_vectors   # pure vectors, no network
cargo test --test gen_vectors sandbox_vectors -- --nocapture             # deploys the wasm in near-sandbox
```

`MEMASTER_WASM` sets the wasm to deploy (default `../../contract/target/near/memaster.wasm`, built with
`cargo near build non-reproducible-wasm` in `contract/`), `VECTORS_OUT` the output folder (default
`../tests/vectors`), `NEAR_SANDBOX_BIN_PATH` a local near-sandbox binary, and `SKIP_PY_RPC=1` skips the Python CLI
run.

## Layout

| File | Role |
|---|---|
| `memaster_verifier/core.py` | Draw algorithm (mechanics included), table hash, mythic commitments |
| `memaster_verifier/canon.py` | `serde_json`-identical serialization |
| `memaster_verifier/verify.py` | Table, pack and mythic checks; series replay |
| `memaster_verifier/stats.py` | Chi-squared goodness of fit (no scipy) |
| `memaster_verifier/rpc.py` | Minimal NEAR JSON-RPC client |
| `memaster_verifier/cli.py` | Command-line interface |
| `tests/` | unittest suite and vectors |
| `vectorgen/` | Rust vector generator (contract code and sandbox) |
