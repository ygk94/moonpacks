// Configuration lue dans les variables d'environnement (voir .env.example). Aucun secret ici.

const env = import.meta.env;

export const NETWORK = (env.VITE_NETWORK ?? "testnet") as "testnet" | "mainnet";
export const CONTRACT_ID: string = env.VITE_CONTRACT_ID ?? "app3.memaster-demo-j7xg7z.testnet";
// fastnear : l'ancien rpc.testnet.near.org renvoie des 429.
export const RPC_URL: string = env.VITE_RPC_URL ?? "https://rpc.testnet.fastnear.com";
export const SERIES_ID = Number(env.VITE_SERIES_ID ?? 0);
export const BLOCK_TIME_S = Number(env.VITE_BLOCK_TIME_S ?? 0.6);
// Indexeur facultatif (front/indexer/) : Trending et ventes récentes. En dev, 127.0.0.1:8787 par défaut ;
// vide : désactivé. Sans réponse, le front se rabat sur les annonces du contrat.
export const INDEXER_URL: string = (env.VITE_INDEXER_URL ?? (env.DEV ? "http://127.0.0.1:8787" : "")).replace(/\/$/, "");

// WalletConnect : vide = désactivé (voir src/near/wallet.tsx).
export const WALLETCONNECT_PROJECT_ID: string = env.VITE_WALLETCONNECT_PROJECT_ID ?? "";

export const EXPLORER = NETWORK === "testnet" ? "https://testnet.nearblocks.io" : "https://nearblocks.io";

if (NETWORK !== "testnet") {
  // Mainnet : jamais sans avis juridique (consigne front, section 7).
  throw new Error("Memaster front is a testnet-only demo.");
}
