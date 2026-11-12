// Connexion wallet (near-connect) : MetaMask (comptes 0x…, NEP-518) en tête, wallets NEAR natifs en secours.

import { NearConnector, type NearConnectorOptions, type NearWalletBase } from "@hot-labs/near-connect";
import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { CONTRACT_ID, NETWORK, RPC_URL, WALLETCONNECT_PROJECT_ID } from "../config";
import { failureOf, txHashOf } from "./events";
import { txStatus, type TxOutcome } from "./rpc";

// Identifiant near-connect du connecteur « Ethereum Wallets » (MetaMask et autres wallets EVM).
export const EVM_WALLET_ID = "ethereum-wallets";

export interface WalletOption {
  id: string;
  name: string;
  icon: string;
  description: string;
  evm: boolean;
}

interface CallOptions {
  deposit?: string;
  gas?: string;
}

interface WalletState {
  accountId: string | null;
  walletName: string | null;
  isEvm: boolean;
  ready: boolean;
  options: WalletOption[];
  connect: (walletId: string) => Promise<void>;
  disconnect: () => Promise<void>;
  /** Signe et envoie un appel au contrat ; rejette avec le message de panique si la transaction échoue. */
  call: (method: string, args: Record<string, unknown>, opts?: CallOptions) => Promise<TxOutcome>;
}

const Ctx = createContext<WalletState | null>(null);

// WalletConnect (wallets mobiles, MetaMask sur iOS) : actif seulement si un projectId est fourni
// (VITE_WALLETCONNECT_PROJECT_ID, gratuit sur cloud.reown.com). Le client est chargé à la demande.
const walletConnect = WALLETCONNECT_PROJECT_ID
  ? import("@walletconnect/sign-client").then((m) =>
      m.default.init({
        projectId: WALLETCONNECT_PROJECT_ID,
        metadata: {
          name: "Memaster (testnet demo)",
          description: "Memecoin booster packs on NEAR testnet",
          url: window.location.origin,
          icons: [`${window.location.origin}/cards/dos-mythique.svg`],
        },
      }),
    )
  : undefined;

const connector = new NearConnector({
  network: NETWORK,
  providers: { testnet: [RPC_URL] },
  features: { testnet: true, signAndSendTransaction: true },
  autoConnect: true,
  // Les types de near-connect et du client WalletConnect diffèrent sur des détails sans effet ici.
  walletConnect: walletConnect as unknown as NearConnectorOptions["walletConnect"],
});

// Wallet de test (clé locale injectée par `npm run e2e`) : seulement en dev et avec VITE_E2E_KEY_WALLET=1.
// `import.meta.env.DEV` vaut `false` dans un build : le module n'y est jamais inclus.
const E2E_KEY_WALLET = import.meta.env.DEV && import.meta.env.VITE_E2E_KEY_WALLET === "1";
const testWallet = E2E_KEY_WALLET ? import("./testKeyWallet") : null;

const isEvmAccount = (id: string | null) => !!id && /^0x[0-9a-f]{40}$/i.test(id);

export function WalletProvider({ children }: { children: ReactNode }) {
  const [accountId, setAccountId] = useState<string | null>(null);
  const [wallet, setWallet] = useState<NearWalletBase | null>(null);
  const [ready, setReady] = useState(false);
  const [options, setOptions] = useState<WalletOption[]>([]);

  useEffect(() => {
    const refreshOptions = () => {
      const list = connector.availableWallets
        .filter((w) => w.manifest.features?.testnet !== false)
        .map((w) => ({
          id: w.manifest.id,
          name: w.manifest.id === EVM_WALLET_ID ? "MetaMask" : w.manifest.name,
          icon: w.manifest.icon,
          description: w.manifest.id === EVM_WALLET_ID ? "MetaMask and other Ethereum wallets" : w.manifest.description,
          evm: w.manifest.id === EVM_WALLET_ID,
        }))
        // MetaMask en premier, puis l'ordre du manifeste.
        .sort((a, b) => Number(b.evm) - Number(a.evm));
      setOptions(list);
      testWallet?.then((m) => setOptions((o) => (o.some((w) => w.id === m.TEST_WALLET_ID) ? o : [m.TEST_WALLET_OPTION, ...o])));
    };
    const onIn = (t: { wallet: NearWalletBase; accounts: { accountId: string }[] }) => {
      setWallet(t.wallet);
      setAccountId(t.accounts[0]?.accountId ?? null);
    };
    const onOut = () => {
      setWallet(null);
      setAccountId(null);
    };
    connector.on("wallet:signIn", onIn);
    connector.on("wallet:signOut", onOut);
    connector.on("selector:walletsChanged", refreshOptions);
    connector.on("selector:manifestUpdated", refreshOptions);
    connector.whenManifestLoaded
      .then(async () => {
        refreshOptions();
        try {
          const { wallet: w, accounts } = await connector.getConnectedWallet();
          setWallet(w);
          setAccountId(accounts[0]?.accountId ?? null);
        } catch {
          // aucun wallet connecté
        }
      })
      .finally(() => setReady(true));
    return () => {
      connector.off("wallet:signIn", onIn);
      connector.off("wallet:signOut", onOut);
      connector.off("selector:walletsChanged", refreshOptions);
      connector.off("selector:manifestUpdated", refreshOptions);
    };
  }, []);

  const connect = useCallback(async (walletId: string) => {
    const test = await testWallet;
    const w = test && walletId === test.TEST_WALLET_ID ? await test.createTestKeyWallet() : await connector.connect({ walletId });
    const accounts = await w.getAccounts({ network: NETWORK });
    setWallet(w);
    setAccountId(accounts[0]?.accountId ?? null);
  }, []);

  const disconnect = useCallback(async () => {
    const test = await testWallet;
    if (!(test && wallet?.manifest.id === test.TEST_WALLET_ID)) await connector.disconnect();
    setWallet(null);
    setAccountId(null);
  }, [wallet]);

  const call = useCallback(
    async (method: string, args: Record<string, unknown>, opts: CallOptions = {}) => {
      if (!wallet || !accountId) throw new Error("Connect a wallet first.");
      const out = (await wallet.signAndSendTransaction({
        network: NETWORK,
        signerId: accountId,
        receiverId: CONTRACT_ID,
        actions: [
          {
            type: "FunctionCall",
            params: { methodName: method, args, gas: opts.gas ?? "100000000000000", deposit: opts.deposit ?? "0" },
          },
        ],
      })) as unknown as Partial<TxOutcome>;
      // Certains wallets ne renvoient que le hash : on relit alors la transaction et ses reçus.
      let full: TxOutcome;
      if (out?.receipts_outcome && out.status) full = out as TxOutcome;
      else {
        const hash = txHashOf(out);
        // Signée mais illisible : on ne prétend pas qu'elle a échoué.
        if (!hash) throw new Error("The wallet did not return the transaction. Check your wallet history before retrying.");
        full = await txStatus(hash, accountId);
      }
      const failure = failureOf(full);
      if (failure) throw new Error(failure);
      return full;
    },
    [wallet, accountId],
  );

  const value = useMemo<WalletState>(
    () => ({
      accountId,
      walletName: wallet?.manifest.id === EVM_WALLET_ID ? "MetaMask" : (wallet?.manifest.name ?? null),
      isEvm: isEvmAccount(accountId) || wallet?.manifest.id === EVM_WALLET_ID,
      ready,
      options,
      connect,
      disconnect,
      call,
    }),
    [accountId, wallet, ready, options, connect, disconnect, call],
  );
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useWallet(): WalletState {
  const v = useContext(Ctx);
  if (!v) throw new Error("useWallet outside WalletProvider");
  return v;
}
