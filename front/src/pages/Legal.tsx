// Mentions légales (version démo). Les informations d'éditeur sont à compléter par l'équipe.

import { CONTRACT_ID } from "../config";

export function Legal() {
  return (
    <div className="page legal">
      <h1>Legal notice</h1>
      <section className="panel prose">
        <h2>Demo only</h2>
        <p>
          Memaster is a hackathon demo running exclusively on the <strong>NEAR testnet</strong>. Testnet NEAR and the
          tokens used here have no monetary value. Nothing on this site is an offer to buy or sell real assets, and it
          is not available on mainnet.
        </p>
        <h2>No affiliation</h2>
        <p>
          Memecoin names and tickers are cited as factual data. Card visuals are original, abstract generative art.
          Memaster is not affiliated with, endorsed by or partnered with the projects, creators or rights holders
          mentioned.
        </p>
        <h2>Prices and tokens</h2>
        <p>
          Coin prices come from public market data (DexScreener, CoinGecko) and are shown for information only. Token
          amounts are estimates. No value is guaranteed.
        </p>
        <h2>Smart contract</h2>
        <p>
          Draws, rates, burns and the market run in the contract <span className="mono">{CONTRACT_ID}</span>. The drop
          rates and the table hash are public on the <a href="#/rates">Drop rates</a> page.
        </p>
        <h2>Publisher</h2>
        <p className="muted">Memaster team, NEAR hackathon. Contact details to be completed.</p>
      </section>
    </div>
  );
}
