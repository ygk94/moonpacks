// Wallet de test pour les parcours de bout en bout (`npm run e2e`) : signe avec une clé ed25519 locale.
//
// Chargé seulement en dev et si VITE_E2E_KEY_WALLET=1 (voir wallet.tsx) : absent de tout build de production
// (`scripts/check-no-e2e-wallet.mjs`, `e2e-wallet-build.test.ts`). La clé n'est jamais dans le bundle : le script
// Playwright l'injecte dans la page (`page.addInitScript`, objet `window.__MEMASTER_E2E_KEY__`), et ce module la
// retire de `window` dès qu'il l'a lue. Seules les actions FunctionCall sont acceptées.

import type { NearWalletBase } from "@hot-labs/near-connect";
import { NETWORK, RPC_URL } from "../config";
import { jsonRpc, keyPairFromSecret, signAndSend, type KeyAction } from "./keySigner";

export const TEST_WALLET_ID = "e2e-key-wallet";
export const TEST_WALLET_OPTION = {
  id: TEST_WALLET_ID,
  name: "Test key (e2e)",
  icon: "",
  description: "Local ed25519 key injected by the end-to-end tests",
  evm: false,
};

interface InjectedKey {
  accountId: string;
  secretKey: string;
}

type FunctionCallInput = {
  type: string;
  params: { methodName: string; args: Record<string, unknown> | Uint8Array; gas?: string; deposit?: string };
};

export async function createTestKeyWallet(): Promise<NearWalletBase> {
  const w = window as unknown as { __MEMASTER_E2E_KEY__?: InjectedKey };
  const injected = w.__MEMASTER_E2E_KEY__;
  delete w.__MEMASTER_E2E_KEY__;
  if (!injected?.accountId || !injected.secretKey) throw new Error("No test key was injected in this page.");
  if (NETWORK !== "testnet") throw new Error("The test wallet is testnet only.");
  const key = await keyPairFromSecret(injected.secretKey);
  const accountId = injected.accountId;
  const rpc = jsonRpc(RPC_URL);
  const unsupported = async () => {
    throw new Error("Not supported by the test wallet.");
  };

  const wallet = {
    manifest: { id: TEST_WALLET_ID, name: TEST_WALLET_OPTION.name, icon: "", description: TEST_WALLET_OPTION.description },
    getAccounts: async () => [{ accountId, publicKey: key.publicKeyText }],
    signIn: async () => [{ accountId, publicKey: key.publicKeyText }],
    signOut: async () => undefined,
    signAndSendTransaction: async (p: { signerId?: string; receiverId: string; actions: FunctionCallInput[] }) => {
      if (p.signerId && p.signerId !== accountId) throw new Error("Wrong signer for the test wallet.");
      const actions: KeyAction[] = p.actions.map((a) => {
        if (a.type !== "FunctionCall") throw new Error("The test wallet only signs FunctionCall actions.");
        return {
          type: "FunctionCall",
          methodName: a.params.methodName,
          args: a.params.args,
          gas: a.params.gas ?? "30000000000000",
          deposit: a.params.deposit ?? "0",
        };
      });
      return signAndSend(rpc, key, accountId, p.receiverId, actions);
    },
    signAndSendTransactions: unsupported,
    signInAndSignMessage: unsupported,
    signMessage: unsupported,
    signDelegateActions: unsupported,
  };
  return wallet as unknown as NearWalletBase;
}
