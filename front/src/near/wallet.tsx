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
  /**
   * Plusieurs appels, une transaction chacun (un `buy_pack` prend jusqu'à 300 Tgas : on ne peut pas les grouper dans
   * une seule transaction). Une seule validation si le wallet sait signer un lot, sinon une par appel. Renvoie les
   * transactions réussies et le nombre d'échecs ; rejette seulement si aucune n'a réussi.
   */
  callMany: (calls: { method: string; args: Record<string, unknown>; opts?: CallOptions }[]) => Promise<{ outcomes: TxOutcome[]; failed: number; firstError?: unknown }>;
}

const Ctx = createContext<WalletState | null>(null);

// WalletConnect (wallets mobiles, MetaMask sur iOS) : actif seulement si un projectId est fourni
// (VITE_WALLETCONNECT_PROJECT_ID, gratuit sur cloud.reown.com). Le client est chargé à la demande.
const walletConnect = WALLETCONNECT_PROJECT_ID
  ? import("@walletconnect/sign-client").then((m) =>
      m.default.init({
        projectId: WALLETCONNECT_PROJECT_ID,
        metadata: {
          name: "Moonpacks (testnet demo)",
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

  const callMany = useCallback(
    async (calls: { method: string; args: Record<string, unknown>; opts?: CallOptions }[]) => {
      if (!wallet || !accountId) throw new Error("Connect a wallet first.");
      const outcomes: TxOutcome[] = [];
      let failed = 0;
      let firstError: unknown;
      const settle = async (out: unknown) => {
        const o = out as Partial<TxOutcome>;
        let full: TxOutcome;
        if (o?.receipts_outcome && o.status) full = o as TxOutcome;
        else {
          const hash = txHashOf(out);
          if (!hash) throw new Error("The wallet did not return the transaction. Check your wallet history before retrying.");
          full = await txStatus(hash, accountId);
        }
        const failure = failureOf(full);
        if (failure) throw new Error(failure);
        return full;
      };
      const batch = calls.length > 1 && wallet.manifest.features?.signAndSendTransactions;
      if (batch) {
        let results: unknown[] | null = null;
        try {
          results = (await wallet.signAndSendTransactions({
            network: NETWORK,
            signerId: accountId,
            transactions: calls.map((c) => ({
              receiverId: CONTRACT_ID,
              actions: [
                {
                  type: "FunctionCall" as const,
                  params: { methodName: c.method, args: c.args, gas: c.opts?.gas ?? "100000000000000", deposit: c.opts?.deposit ?? "0" },
                },
              ],
            })),
          })) as unknown[];
        } catch (e) {
          // Refus dans le wallet : rien n'est parti. Autre erreur : on retombe sur une signature par appel.
          if (/reject|cancel|denied|closed/i.test(String((e as Error)?.message ?? e))) throw e;
        }
        if (results) {
          for (const out of results) {
            try {
              outcomes.push(await settle(out));
            } catch (e) {
              failed++;
              firstError ??= e;
            }
          }
          if (!outcomes.length) throw firstError ?? new Error("No transaction went through.");
          return { outcomes, failed, firstError };
        }
      }
      for (const c of calls) {
        try {
          outcomes.push(await call(c.method, c.args, c.opts));
        } catch (e) {
          // Le premier refus arrête le lot ; les packs déjà achetés restent ouverts.
          if (!outcomes.length) throw e;
          failed += calls.length - outcomes.length;
          firstError = e;
          break;
        }
      }
      return { outcomes, failed, firstError };
    },
    [wallet, accountId, call],
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
      callMany,
    }),
    [accountId, wallet, ready, options, connect, disconnect, call, callMany],
  );
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useWallet(): WalletState {
  const v = useContext(Ctx);
  if (!v) throw new Error("useWallet outside WalletProvider");
  return v;
}
