// Mentions légales et données personnelles (démo hackathon, testnet).

import { CONTACT_EMAIL, CONTRACT_ID } from "../config";
import { BRAND } from "../lib/brand";

export function Legal() {
  return (
    <div className="page legal">
      <h1>Legal notice</h1>
      <section className="panel prose">
        <h2>Publisher</h2>
        <p>
          {BRAND} is a non-commercial student project built by a team of two for the NEAR Hackathon (2026).
          {CONTACT_EMAIL ? (
            <>
              {" "}
              Contact: <a href={`mailto:${CONTACT_EMAIL}`}>{CONTACT_EMAIL}</a>.
            </>
          ) : null}
        </p>

        <h2>Hosting</h2>
        <p>Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, United States (vercel.com).</p>

        <h2>Demo only</h2>
        <p>
          {BRAND} runs exclusively on the <strong>NEAR testnet</strong>. Testnet NEAR and the tokens used here have no
          monetary value. Nothing on this site is an offer to buy or sell real assets, and the service is not available
          on mainnet.
        </p>

        <h2>Simulation</h2>
        <p>
          On this demo, burning a card does not deliver real memecoin tokens: the delivery goes through a test service
          that only records it. The token amounts shown are estimates computed from public market prices. The draws,
          the drop rates, the cards, the market and the burn itself are real transactions of the testnet contract.
        </p>

        <h2>No affiliation</h2>
        <p>
          Memecoin names and tickers are cited as factual data. Card visuals are original, abstract generative art.{" "}
          {BRAND} is not affiliated with, endorsed by or partnered with the projects, creators or rights holders
          mentioned.
        </p>

        <h2>Prices and tokens</h2>
        <p>
          Coin prices come from public market data (DexScreener, CoinGecko) and are shown for information only. No value
          is guaranteed.
        </p>

        <h2>Smart contract</h2>
        <p>
          Draws, rates, burns and the market run in the contract <span className="mono">{CONTRACT_ID}</span>. The drop
          rates and the table hash are public on the <a href="#/rates">Drop rates</a> page.
        </p>

        <h2>Personal data</h2>
        <p>
          There is no account and no tracking or advertising cookie. Your browser keeps a short-lived cache of public
          prices and your wallet connection in local storage, on your device only. Your wallet address and your
          transactions are public on the NEAR testnet, like any blockchain transaction. To display the site, your
          browser contacts the NEAR RPC provider (FastNear), CoinGecko, DexScreener, your wallet provider and the host,
          which receive your IP address as for any web request.
        </p>
      </section>
    </div>
  );
}
