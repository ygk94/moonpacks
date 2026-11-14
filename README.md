# Moonpacks

Memecoin trading-card packs on NEAR testnet. You buy a pack; the contract draws the cards on-chain from a draw table
whose SHA-256 is frozen on-chain, mints them as NEP-171 NFTs, and logs every seed and roll so anyone can recompute the
pack. Some cards are **burnable**: burning one triggers a payout of the memecoin it shows (simulated on testnet, see
[Limits](#limits)).

Built for **NEAR HACKATHON** (tracks: `nfts`, `memecoins`). Testnet only, never deployed to mainnet.

- **Live demo:** https://moonpacks-ochre.vercel.app (NEAR testnet, MetaMask or any NEAR wallet)
- **Contract:** [`app4.simpletea5483.testnet`](https://testnet.nearblocks.io/address/app4.simpletea5483.testnet)

## For automated reviewers

Prerequisites: Rust 1.99 (tested with 1.99.1) with the `wasm32-unknown-unknown` target, Node.js 24, Python 3.12
(Python 3.8 fails on type hints). No key, no account, no wallet and no Docker for anything in this section. Times were
measured on a fresh clone on an Apple Silicon laptop on 14/11/2026.

| Component | Status | Network | Check | Time |
|---|---|---|---|---|
| Contract (series, packs, reveal, NFTs, market, burn, mechanics) | built, 163 unit tests | none | `cd contract && cargo test --lib --locked` | about 2 min (first build) |
| Deployed draw tables | 2 series open on testnet, hashes frozen | testnet RPC, read only | `table` command in [Verify the claims](#verify-the-claims) | about 3 s |
| Pack verification (seed chain and every roll) | built in Python and in the web app | testnet RPC, read only | `pack` command, or **Verify this pack** in the app | seconds |
| Python verifier vs the Rust draw code | 110 tests with vectors produced by the contract | none | `cd verifier && python3.12 -m unittest discover -s tests -t .` | about 10 s |
| Web app | deployed on Vercel, 141 tests | testnet | `cd front && npm ci && npm test -- --run` | under 1 min |
| Card art generator | built | none | `cd art && python3.12 -m unittest discover -s tests` | about 3 s |
| Token payout on burn | **simulated** (mock redeemer) | testnet | see [Limits](#limits) | |
| Price oracle for resurrection | **mock**, reads no price | testnet | `contract/mock-oracle/` | |

## Verify the claims

| ID | Claim | Command (from the repo root) | Expected | Does NOT prove |
|---|---|---|---|---|
| C1 | The Classic draw table on testnet is the one in this repo | `cd verifier && python3.12 -m memaster_verifier table --rpc testnet --contract app4.simpletea5483.testnet --series 0` | ends with `=> VÉRIFIÉ` (verified; the verifier prints in French); hash `85b20c22…af4af8f4`, as in `contract/series-v4/classic/table_hash.txt` | that the deployed wasm comes from this source (no reproducible build) |
| C2 | Same for Full Moon | same command with `--series 1` | `=> VÉRIFIÉ`; hash `6508bc63…37ac4eb21`, as in `contract/series-v4/full-moon/table_hash.txt` | same |
| C3 | 1,527 visible cards plus 3 sealed mythics per series | count `cards` and `mythics` in `contract/series-v4/classic/table.json` (or `card_count` in `get_series`) | 1,527 cards (1,054 common, 224 rare, 228 epic, 21 legendary) and 3 mythic commitments | which coins the mythics are (sealed until drawn and revealed) |
| C4 | A pack can be recomputed from public data | `cd verifier && python3.12 -m memaster_verifier pack --rpc testnet --contract app4.simpletea5483.testnet --tx-hash <buy_pack tx> --sender <buyer>` | `=> VÉRIFIÉ` | that the last block producer did not withhold its block (see [How NEAR is used](#how-near-is-used)) |
| C5 | The verifier agrees with the Rust draw code byte for byte | `cd verifier && python3.12 -m unittest discover -s tests -t .` | `Ran 110 tests … OK (skipped=2)` | behaviour of the deployed wasm |
| C6 | Contract logic | `cd contract && cargo test --lib --locked` | `test result: ok. 163 passed` | behaviour on a live network (integration tests: `cargo test --test sandbox`, needs near-sandbox) |
| C7 | Full Moon burnable cards hold 2.5× the tokens of Classic ones, at 2.5× the price | compare `backing.amount` of a card and `price` in the two `table.json` files | e.g. Black Dragon 3.07e31 vs 7.68e31 units; 0.0552 vs 0.1381 NEAR | that a payout is real (it is simulated) |

Testnet usage as of 14/11/2026 (`get_series`): 3 Classic packs sold, 0 Full Moon, no mythic drawn. Gold packs, pity,
rush windows, burns and resurrections are covered by unit tests; they have not been demonstrated on testnet.

## The problem

Memecoin culture is mostly charts and speculation. There is no fun, collectible way to own a piece of a meme's history,
and blind-box products in crypto usually hide their odds and their draws, so nobody can check that a pack was fair.

## The product

- **1,527 visible cards plus 3 sealed mythics**, one card per memecoin, from the 2013 classics to recent launches,
  across many chains. Rarity follows each coin's peak market cap. Dead coins are collection cards. The mythics' identity
  is committed on-chain (two hashes) and revealed only after one is drawn, by whoever holds the preimage.
- **Packs**: two series, Classic (5 cards, 0.0552 NEAR) and Full Moon (the same cards, 5 cards, 0.1381 NEAR; burnable
  cards hold 2.5× more tokens). The shop sells them by 5, 10 or 20 cards, as 1, 2 or 4 packs of 5. Plus 9 **themed packs**
  drawn from the Classic series: Dog (8 cards), Cat (5), Frog (3), Solana (5), BNB Chain (10), Ethereum (3), and OG
  single, duo and pack (1, 2 or 5 cards, 2013-2018 coins only). Themed packs share the series' mint counters and caps, so
  they never reprint or dilute rarity. The contract accepts 1 to 10 cards per pack.
- **Burnable cards**: a card backed by a token amount can be burned to redeem that amount. Burns lower that coin's draw
  weight in later packs, down to a 25 % floor.
- **Mechanics** written into the contract: gold packs with a pity counter, community "rush" windows with better odds,
  burn-driven weights, resurrection of dead coins (triggered by a price oracle), random value per pack. Full spec:
  [`docs/mechanics.md`](docs/mechanics.md).
- **Transparency**: the full draw table is stored on-chain with its SHA-256 hash; every pack logs its random seeds and
  draws as NEP-297 events, and anyone can recompute a pack in the browser (Collection, **Verify this pack**) or with the
  Python verifier.
- **Market**: cards can be listed and bought between players (NEAR payments, NEP-199 royalties).

## How NEAR is used

- **Smart contract (Rust, near-sdk 5.30)** holds the series tables, sells packs, mints NEP-171 NFTs (with NEP-177, 178,
  181 and 199), runs the market and the burns. Draws are computed on-chain. Two roles are trusted or off-chain: the price
  oracle that triggers resurrections, and the holder of the mythic preimages, who reveals a drawn mythic.
- **On-chain randomness**: a pack is revealed over k receipts (3 by default, 2 to 6), each mixing its block's
  `random_seed` into a commit chain, so the buyer cannot choose the outcome by retrying in one transaction. The last
  block producer can withhold its seed; there is no external VRF. Details: [`contract/README.md`](contract/README.md).
- **Chain abstraction for users**: wallets via `@hot-labs/near-connect`, with MetaMask first (NEAR accounts controlled by
  an Ethereum wallet), so a memecoin trader does not need a new wallet.
- **NEAR Intents (designed, simulated on testnet)**: burnable cards are meant to be backed by tokens held through NEAR
  Intents and paid out on burn. The Intents contract `intents.near` has code on mainnet; `intents.testnet` has none
  (checked with `view_account` on 14/11/2026). So on this demo the payout goes to a mock redeemer contract and **no real
  tokens are sent**; the site says so on every burn. The contract calls an abstract `Redeemer` interface
  (`contract/src/redeem.rs`); it does not call NEP-141 `ft_transfer` itself.

| Track | Where in the code |
|---|---|
| `nfts` | `contract/src/nft.rs` (NEP-171/177/178/181/199), `contract/src/mythic.rs` (sealed mythics), `contract/src/market.rs` |
| `memecoins` | `contract/src/mechanics.rs` and `contract/src/draw.rs` (burn weights, rush, resurrection, value per pack), `contract/src/redeem.rs` (burn and payout); testnet accounts `app4`, `redeemer4`, `oracle4` |

## Try it (judges)

Needs a NEAR **testnet** wallet with a few testnet NEAR (free from https://near-faucet.io).

1. Open https://moonpacks-ochre.vercel.app → the landing page and two packs.
2. Click **Connect wallet**, pick MetaMask or a NEAR wallet on testnet → your account appears in the header.
3. Go to **Shop**, click **Open** on a Classic 5-card pack (0.0552 NEAR plus a storage deposit, 0.07545 NEAR attached in
   total; unused storage is refunded), confirm in the wallet → the 5 cards are revealed one by one.
4. In **Shop**, open a themed pack (e.g. **OG single**, 0.011 NEAR) → one card from the 2013-2018 era only.
5. Go to **Collection** → your cards are there as NFTs, grouped by pack. Click **Verify this pack** → the app reads the
   table and the pack from the chain and recomputes every draw in your browser → all checks pass.
6. Click a burnable card → it shows its token backing; burn it → the NFT is destroyed and the mock redeemer records a
   simulated payout. Or choose **Sell on the market** to list it.
7. Go to **Odds** → the drop rates of each pack and, under **Verify it yourself**, the contract code hash and the table
   hash frozen on-chain, with the verifier command to recompute them.
8. Go to **Market** → buy a card listed by another account, if one is listed.

## Repository

| Folder | What it is |
|---|---|
| [`contract/`](contract/README.md) | NEAR smart contract (Rust): series, packs, reveal, NFTs, market, burn, mechanics, pack kinds; mock redeemer and price-oracle contracts; deployment scripts |
| [`front/`](front/README.md) | Web app (Vite, React, TypeScript), deployed to Vercel by CI |
| [`verifier/`](verifier/README.md) | Independent Python verifier of table hashes and pack draws, with cross-language test vectors from the Rust code |
| [`sim/`](sim/README.md) | Monte-Carlo simulation of the pack economy used to set prices, odds and value tables |
| [`art/`](art/README.md) | Procedural card-art generator (original SVG artwork, no third-party logos) |
| `docs/` | Mechanics spec and the data the series were built from (catalogue, CoinGecko snapshot, NEAR Intents token lists) |

Naming: `memaster` (crate, event standard, Python package, older testnet accounts) is the project's former working
name. Some script names, code comments and verifier messages are in French. `front/src/near/testKeyWallet.ts` is a test
wallet for end-to-end runs, loaded only in dev mode; it contains no key (the test script injects one at run time).

## Run it locally

Requirements: Rust 1.99 with `wasm32-unknown-unknown`, Node.js 24, Python 3.12. Versions are not pinned by a
toolchain file; these are the ones tested.

```bash
# Web app against the deployed testnet contract
cd front && npm ci && npm run dev          # http://localhost:5173

# Tests
cd contract && cargo test --lib --locked   # contract unit tests
cd verifier && python3.12 -m unittest discover -s tests -t .
cd front && npm test -- --run
cd art && python3.12 -m unittest discover -s tests
cd sim && pip install -r requirements.txt && python3.12 -m pytest -q tests
```

### Deploy your own copy on testnet

Needs `near-cli-rs`, `cargo-near` 0.23, and a funded testnet account whose key is in the NEAR CLI keychain. Always set
`ROOT_ID`: without it the script targets the team's account, whose key you do not have.

```bash
cd contract
ROOT_ID=<your-account>.testnet KEYCHAIN=system ./scripts/deploy_v4.sh
```

The script loads the prebuilt series in `contract/series-v4/`. The preimages of their 3 mythics are not in the
repository (`scripts/secrets/` is git-ignored), so on your copy those mythics can be drawn but never revealed. To get
mythics you can reveal, build your own series: `python3.12 scripts/gen_mythics.py INPUT.json PUBLIC.json SECRETS.json`
(example input: `scripts/example-mythics.json`), then `scripts/build_series.py` (see
[`contract/README.md`](contract/README.md#scripts)).

Then point the web app at it with `VITE_CONTRACT_ID=app4.<your-account>.testnet` (see `front/.env.example`).

## Economics

| Item | Cost (testnet NEAR) | Source |
|---|---|---|
| Classic pack | 0.0552, plus storage: 0.07545 attached, unused storage refunded | `get_series(0)` |
| Full Moon pack | 0.1381, plus storage: 0.15415 attached | `get_series(1)` |
| Deploying a full copy | about 20 (11 for the contract account, about 6.3 of storage for the two series, 3 for the mocks) | estimate in `contract/scripts/deploy_v4.sh` |

Prices and odds were set with the Monte-Carlo simulation in [`sim/`](sim/README.md).

## Deployments (testnet)

| Version | Contract | Notes |
|---|---|---|
| v4 (current) | `app4.simpletea5483.testnet` | Pack kinds (themed packs); series 0 "Moonpacks Classic" + 9 kinds, series 1 "Moonpacks Full Moon" |
| v3 | `app3.memaster-demo-j7xg7z.testnet` | Two series, storage refunds |
| v2, v1 | `app2.` / `app.memaster-demo-j7xg7z.testnet` | Earlier iterations |

## Hackathon disclosure

- All code in this repository was written during the hackathon window (first commit 2026-11-11); there is no
  pre-existing codebase.
- Libraries: near-sdk and near-contract-standards (Rust), sha2; React, framer-motion, `@hot-labs/near-connect`,
  Vite, Vitest; Python standard library, NumPy and PyYAML for the simulation (see `sim/requirements.txt`).
- AI coding assistants were used during development.
- Market data comes from public CoinGecko and NEAR Intents endpoints (snapshots in `docs/data/`). Card art is generated
  procedurally; no coin logos are used. Coin names and tickers are used only to identify the coins.

## Limits

- Testnet only. Paid random packs with resellable value may fall under gambling law in some countries; no mainnet
  launch without legal review.
- Token payouts on burn are simulated by a mock redeemer; no token moves.
- The price oracle is a mock that reads no price: on testnet, resurrections are pushed by hand.
- The last block producer of a reveal can withhold its seed; there is no external VRF.
- Mythic reveals depend on the preimage holder.
- Gold packs, mythic draws, rush windows and resurrections have not happened on testnet yet; unit tests cover them.
- The deployed wasm is not reproducibly built, so the verifier's `code` check only compares it with a local build.

## Related project

Some team members also built **ONA** at NEAR HACKATHON (track `privacy`): a private end-to-end AI agent, a separate
project with its own repository: https://github.com/enzoblain/ONA. No code, contract or server is shared between the two
projects.

## License

[MIT](LICENSE)
