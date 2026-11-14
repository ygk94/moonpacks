import { useState } from "react";
import { BRAND } from "../lib/brand";
import { shortAccount } from "../lib/format";
import { navigate, useRoute } from "../lib/router";
import { humanError } from "../near/errors";
import { useWallet } from "../near/wallet";
import { Modal } from "./Modal";

const LINKS = [
  ["/shop", "Shop"],
  ["/collection", "Collection"],
  ["/market", "Market"],
  ["/rates", "Odds"],
] as const;

/** Bandeau permanent (consigne, règle 8). */
export function DemoBanner() {
  return (
    <div className="demo-banner" role="note">
      {/* Le burn passe par un redeemer factice sur testnet : aucun vrai jeton n'est livré. Version courte sur mobile. */}
      <span className="demo-banner__long">Demo · NEAR testnet</span>
      <span className="demo-banner__short">Testnet demo</span>
      <span className="demo-banner__sep">·</span>
      <span className="demo-banner__long">Token delivery simulated</span>
      <span className="demo-banner__short">Simulated burns</span>
      <span className="demo-banner__sep">·</span>
      <a href="#/legal">
        <span className="demo-banner__long">Legal notice</span>
        <span className="demo-banner__short">Legal</span>
      </a>
    </div>
  );
}

export function Header() {
  const { path } = useRoute();
  const { accountId, walletName, disconnect } = useWallet();
  const [open, setOpen] = useState(false);
  return (
    <header className="header">
      <a className="header__logo" href="#/">
        <span className="header__mark">🌙</span>
        <span>{BRAND.toUpperCase()}</span>
      </a>
      <nav className="header__nav">
        {LINKS.map(([href, label]) => (
          <a key={href} href={`#${href}`} className={path.startsWith(href) ? "active" : ""}>
            {label}
          </a>
        ))}
      </nav>
      <div className="header__wallet">
        {accountId ? (
          <button className="btn btn--account" onClick={() => setOpen(true)} title={accountId}>
            <span className="dot" /> {shortAccount(accountId)}
          </button>
        ) : (
          <ConnectButton />
        )}
      </div>
      <Modal open={open} onClose={() => setOpen(false)}>
        <h2>Account</h2>
        <p className="mono break">{accountId}</p>
        <p className="muted">Connected with {walletName}</p>
        <div className="row">
          <button
            className="btn"
            onClick={() => {
              setOpen(false);
              navigate("/collection");
            }}
          >
            My collection
          </button>
          <button
            className="btn btn--ghost"
            onClick={async () => {
              await disconnect();
              setOpen(false);
            }}
          >
            Disconnect
          </button>
        </div>
      </Modal>
    </header>
  );
}

export function ConnectButton({ big, label = "Connect wallet" }: { big?: boolean; label?: string }) {
  const { options, connect, ready } = useWallet();
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const choose = async (id: string) => {
    setBusy(id);
    setError(null);
    try {
      await connect(id);
      setOpen(false);
    } catch (e) {
      setError(humanError(e));
    } finally {
      setBusy(null);
    }
  };

  return (
    <>
      <button className={`btn btn--primary${big ? " btn--big" : ""}`} onClick={() => setOpen(true)} disabled={!ready}>
        {label}
      </button>
      <Modal open={open} onClose={() => setOpen(false)}>
        <h2>Connect wallet</h2>
        <p className="muted">
          New to NEAR with MetaMask? Your wallet will first ask you to sign a one-time setup transaction that activates
          your account on NEAR.
        </p>
        <ul className="wallets">
          {options.map((w) => (
            <li key={w.id}>
              <button className={`wallet${w.evm ? " wallet--featured" : ""}`} onClick={() => choose(w.id)} disabled={!!busy}>
                {w.icon && <img src={w.icon} alt="" />}
                <span className="wallet__text">
                  <strong>{w.name}</strong>
                  <small>{w.evm ? "Recommended · " : ""}{w.description}</small>
                </span>
                {busy === w.id && <span className="spinner" />}
              </button>
            </li>
          ))}
          {!options.length && <li className="muted">Loading wallets…</li>}
        </ul>
        {error && <p className="error">{error}</p>}
      </Modal>
    </>
  );
}
