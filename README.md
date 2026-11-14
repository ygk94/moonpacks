# Moonpacks

Memecoin trading-card packs on NEAR. You buy a pack, the cards are drawn on-chain with verifiable randomness and minted
as NFTs (NEP-171), and some cards are **burnable**: burning one pays out tokens of the memecoin it shows.

Built for **NEAR HACKATHON** (tracks: NFTs, Memecoins). Testnet only.

- **Live demo:** https://moonpacks-ochre.vercel.app (NEAR testnet, MetaMask or any NEAR wallet)
- **Contract:** [`app4.simpletea5483.testnet`](https://testnet.nearblocks.io/address/app4.simpletea5483.testnet)

## The problem

Memecoin culture is mostly charts and speculation. There is no fun, collectible way to own a piece of a meme's history,
and blind-box products in crypto usually hide their odds and their draws, so nobody can check that a pack was fair.

## The product

- **1,527 cards**, one per memecoin, from the 2013 classics to recent launches, across many chains. Rarity follows each
  coin's peak market cap. Dead coins are collection cards; a few cards are sealed **mythics** whose identity is committed
  on-chain (hash) and revealed only when one is pulled.
- **Packs**: Classic (5 cards) and Full Moon (same cards, burnable cards hold 2.5× more tokens), sold by 5, 10 or 20
  cards, plus 9 **themed packs** drawn from the same series: Dog, Cat, Frog, Solana, BNB Chain, Ethereum, OG 1/2/5 (only
  2013-2018 coins). Themed packs share the series' mint counters and caps, so they never reprint or dilute rarity.
- **Burnable cards**: a card backed by a token amount can be burned to redeem that amount. Burns feed back into the
  odds (burned coins get rarer in later packs).
- **Mechanics** written into the contract: gold packs with a pity counter, community "rush" windows with better odds,
  burn-driven rarity, resurrection of dead coins whose price comes back, value tables per pack. Full spec:
  [`docs/mechanics.md`](docs/mechanics.md).
- **Transparency**: the full draw table is stored on-chain with its SHA-256 hash; every pack logs its random seeds and
  draws as events, and anyone can recompute a pack in the browser (Odds page) or with the Python verifier.
- **Market**: cards can be listed and bought between players (NEAR payments, royalties).

## How NEAR is used

- **Smart contract (Rust, near-sdk 5)** holds the series tables, sells packs, mints NEP-171 NFTs, runs the market and
  the burns. Everything a player sees comes from contract views; nothing is decided off-chain.
- **On-chain randomness**: a pack is revealed over 3 blocks, each step mixing the block's `random_seed` into an
  accumulator, so the buyer cannot choose the outcome by retrying in one transaction.
- **Chain abstraction for users**: wallets via `@hot-labs/near-connect`, with MetaMask first (NEAR accounts controlled by
  an Ethereum wallet), so a memecoin trader does not need a new wallet.
- **NEAR Intents (designed, simulated on testnet)**: burnable cards are meant to be backed by tokens held through NEAR
  Intents and paid out on burn. NEAR Intents has no testnet, so on this demo the payout goes to a mock redeemer
  contract and **no real tokens are sent**; the site says so on every burn.

## Try it (judges)

All steps use NEAR **testnet**; get free testnet NEAR from https://near-faucet.io.

1. Open https://moonpacks-ochre.vercel.app → you see the landing page and two packs.
2. Click **Connect wallet**, pick MetaMask or a NEAR wallet on testnet → your account appears in the header.
3. Go to **Shop**, click **Open** on a Classic 5-card pack (0.0552 NEAR + a refundable storage deposit), confirm in
   the wallet → the pack opens and the 5 cards are revealed one by one.
4. In **Shop**, open a themed pack (e.g. **OG single**, 0.011 NEAR) → you get one card from the 2013-2018 era only.
5. Go to **Collection** → your cards are there as NFTs, grouped by pack. Click **Verify this pack** → the app reads the
   table and the pack from the chain and recomputes every draw in your browser → all checks pass.
6. Click a burnable card → it shows its token backing; burn it → the NFT is destroyed and a (simulated) token payout is
   recorded. Or choose **Sell on the market** to list it.
7. Go to **Odds** → the drop rates of each pack and, under "Verify it yourself", the contract code hash and the table
   hash frozen on-chain, with the verifier command to recompute them.
8. Go to **Market** → buy a card listed by another account.

## Repository

| Folder | What it is |
|---|---|
| [`contract/`](contract/README.md) | NEAR smart contract (Rust): series, packs, reveal, NFTs, market, burn, mechanics, pack kinds; mock redeemer and price-oracle contracts; deployment scripts |
| [`front/`](front/README.md) | Web app (Vite, React, TypeScript), deployed to Vercel by CI |
| [`verifier/`](verifier/README.md) | Independent Python verifier of table hashes and pack draws, with cross-language test vectors from the Rust code |
| [`sim/`](sim/README.md) | Monte-Carlo simulation of the pack economy used to set prices, odds and value tables |
| [`art/`](art/README.md) | Procedural card-art generator (original SVG artwork, no third-party logos) |
| `docs/` | Mechanics spec and the data the series were built from (catalogue, CoinGecko snapshot, NEAR Intents token lists) |

## Run it locally

Requirements: Rust (stable) with `wasm32-unknown-unknown`, Node.js 24, Python 3.12.

```bash
# Web app against the deployed testnet contract
cd front && npm ci && npm run dev          # http://localhost:5173

# Tests
cd contract && cargo test --lib            # contract unit tests
cd verifier && python -m unittest discover -s tests -t .
cd front && npm test
cd art && python -m unittest discover -s tests
cd sim && pip install -r requirements.txt && python -m pytest -q tests
```

Deploy your own copy on testnet (needs `near-cli-rs` and `cargo-near`, and a funded testnet account whose key is in
the NEAR CLI keychain):

```bash
cd contract
ROOT_ID=<your-account>.testnet KEYCHAIN=system ./scripts/deploy_v4.sh
```

Then point the web app at it with `VITE_CONTRACT_ID=app4.<your-account>.testnet` (see `front/.env.example`).

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
- Market data comes from public CoinGecko and NEAR Intents endpoints (snapshots in `docs/data/`). Card art is generated;
  no coin logos are used.

## Limits

- Testnet only. Paid random packs with resellable value may fall under gambling law in some countries; no mainnet
  launch without legal review.
- Token payouts on burn are simulated (see above). The price oracle used for dead-coin resurrection is a mock on testnet.

## License

[MIT](LICENSE)
