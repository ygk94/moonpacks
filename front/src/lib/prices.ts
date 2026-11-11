// Cours hors chaîne, lus par des API publiques sans clé :
// - NEAR/USD : CoinGecko ;
// - cours d'un coin : DexScreener (par adresse, toutes chaînes, pool le plus liquide), sinon CoinGecko (par id).
// Voir docs/oracle-prix.md. Ces cours servent à l'affichage seulement, jamais à une « valeur garantie ».
//
// CoinGecko sans clé limite fortement le débit (429, souvent sans en-tête CORS : le navigateur n'y voit qu'un échec
// réseau). Pour que le cours ne passe pas à « Not available » en naviguant :
// - cache de 5 min en mémoire et dans localStorage (lecture et écriture protégées : navigation privée, quota) ;
// - requêtes regroupées : les ids demandés dans la même fenêtre partent en un seul appel `ids=a,b,c` ;
// - recul après un 429 ou un échec réseau (30 s, doublé jusqu'à 10 min, `Retry-After` respecté) ; pendant le recul,
//   et si un appel échoue, on sert la dernière valeur connue (1 h au plus).

export const TTL_MS = 5 * 60_000;
export const STALE_MS = 60 * 60_000;
const STORAGE_KEY = "memaster.prices.v1";
const BACKOFF_MIN_MS = 30_000;
const BACKOFF_MAX_MS = 10 * 60_000;
const BATCH_MS = 40;
const MAX_IDS = 50;

type Fetch = (url: string) => Promise<Pick<Response, "ok" | "status" | "json" | "headers">>;
interface Entry {
  at: number;
  v: number | null;
}
export interface PriceClientOptions {
  fetch?: Fetch;
  storage?: () => Storage | undefined;
  now?: () => number;
  batchMs?: number;
}

class RateLimited extends Error {}

export function createPriceClient(opts: PriceClientOptions = {}) {
  const doFetch: Fetch = opts.fetch ?? ((u) => fetch(u));
  const now = opts.now ?? Date.now;
  const batchMs = opts.batchMs ?? BATCH_MS;
  const storage =
    opts.storage ??
    (() => {
      try {
        return globalThis.localStorage;
      } catch {
        return undefined;
      }
    });

  // --- Cache : mémoire, recopié dans localStorage -------------------------------------------------
  const mem = new Map<string, Entry>();
  let loaded = false;
  const load = () => {
    if (loaded) return;
    loaded = true;
    try {
      const raw = storage()?.getItem(STORAGE_KEY);
      const saved = raw ? (JSON.parse(raw) as Record<string, Entry>) : {};
      for (const [k, e] of Object.entries(saved)) {
        if (e && typeof e.at === "number" && (e.v === null || typeof e.v === "number")) mem.set(k, e);
      }
    } catch {
      // stockage indisponible ou illisible : cache en mémoire seulement
    }
  };
  const save = () => {
    try {
      const keep: Record<string, Entry> = {};
      for (const [k, e] of mem) if (now() - e.at < STALE_MS) keep[k] = e;
      storage()?.setItem(STORAGE_KEY, JSON.stringify(keep));
    } catch {
      // quota dépassé, navigation privée : sans effet sur l'affichage
    }
  };
  const get = (key: string): Entry | undefined => {
    load();
    return mem.get(key);
  };
  const put = (key: string, v: number | null) => {
    mem.set(key, { at: now(), v });
    save();
  };
  const fresh = (e: Entry | undefined) => !!e && now() - e.at < TTL_MS;
  /** Dernière valeur connue, même périmée (1 h au plus), quand l'API ne répond pas. */
  const stale = (key: string) => {
    const e = get(key);
    return e && e.v != null && now() - e.at < STALE_MS ? e.v : null;
  };

  // --- Recul après un 429 --------------------------------------------------------------------------
  const backoff = { until: 0, delay: 0 };
  const blocked = () => now() < backoff.until;
  const penalize = (retryAfterS?: number) => {
    backoff.delay = Math.min(BACKOFF_MAX_MS, backoff.delay ? backoff.delay * 2 : BACKOFF_MIN_MS);
    const wait = retryAfterS && retryAfterS > 0 ? Math.max(retryAfterS * 1000, backoff.delay) : backoff.delay;
    backoff.until = now() + Math.min(wait, BACKOFF_MAX_MS);
  };
  const recover = () => {
    backoff.delay = 0;
    backoff.until = 0;
  };

  // --- CoinGecko, requêtes regroupées --------------------------------------------------------------
  const inflight = new Map<string, Promise<number | null>>();
  let queue: { id: string; resolve: (v: number | null) => void }[] = [];
  let timer: ReturnType<typeof setTimeout> | null = null;

  async function flush() {
    timer = null;
    const batch = queue;
    queue = [];
    for (let i = 0; i < batch.length; i += MAX_IDS) {
      const part = batch.slice(i, i + MAX_IDS);
      const ids = [...new Set(part.map((p) => p.id))];
      let prices: Record<string, number | null> | null = null;
      if (!blocked()) {
        try {
          const r = await doFetch(
            `https://api.coingecko.com/api/v3/simple/price?ids=${ids.map(encodeURIComponent).join(",")}&vs_currencies=usd`,
          );
          if (r.status === 429) throw new RateLimited(r.headers?.get?.("retry-after") ?? "");
          if (!r.ok) throw new Error(`CoinGecko ${r.status}`);
          const j = (await r.json()) as Record<string, { usd?: unknown }>;
          recover();
          prices = {};
          for (const id of ids) {
            const v = j?.[id]?.usd;
            prices[id] = typeof v === "number" && v > 0 ? v : null;
            put(`cg:${id}`, prices[id]);
          }
        } catch (e) {
          // 429, ou 429 sans CORS vu comme un échec réseau : on recule.
          if (e instanceof RateLimited || e instanceof TypeError) penalize(Number((e as Error).message) || undefined);
        }
      }
      for (const p of part) p.resolve(prices ? prices[p.id] : stale(`cg:${p.id}`));
    }
  }

  function coingecko(id: string): Promise<number | null> {
    const key = `cg:${id}`;
    const hit = get(key);
    if (fresh(hit)) return Promise.resolve(hit!.v);
    if (blocked()) return Promise.resolve(stale(key));
    const pending = inflight.get(key);
    if (pending) return pending;
    const p = new Promise<number | null>((resolve) => {
      queue.push({ id, resolve });
      if (!timer) timer = setTimeout(flush, batchMs);
    }).finally(() => inflight.delete(key));
    inflight.set(key, p);
    return p;
  }

  // --- DexScreener (par adresse), même cache ---------------------------------------------------------
  function dexscreener(address: string): Promise<number | null> {
    const key = `dex:${address.toLowerCase()}`;
    const hit = get(key);
    if (fresh(hit)) return Promise.resolve(hit!.v);
    const pending = inflight.get(key);
    if (pending) return pending;
    const p = (async () => {
      try {
        const r = await doFetch(`https://api.dexscreener.com/latest/dex/tokens/${encodeURIComponent(address)}`);
        if (!r.ok) return stale(key);
        const j = await r.json();
        const pairs: { priceUsd?: string; liquidity?: { usd?: number }; baseToken?: { address?: string } }[] = j?.pairs ?? [];
        const own = pairs.filter((x) => x.baseToken?.address?.toLowerCase() === address.toLowerCase() && x.priceUsd);
        own.sort((a, b) => (b.liquidity?.usd ?? 0) - (a.liquidity?.usd ?? 0));
        const v = Number(own[0]?.priceUsd);
        const value = v > 0 ? v : null;
        put(key, value);
        return value;
      } catch {
        return stale(key);
      }
    })().finally(() => inflight.delete(key));
    inflight.set(key, p);
    return p;
  }

  const nearUsd = () => coingecko("near");

  async function coinUsd(coin: { address: string | null; coingecko: string | null }): Promise<number | null> {
    if (coin.address) {
      const v = await dexscreener(coin.address);
      if (v) return v;
    }
    return coin.coingecko ? coingecko(coin.coingecko) : null;
  }

  return { nearUsd, coinUsd, coingecko, isBackingOff: blocked };
}

const client = createPriceClient();
export const nearUsd = client.nearUsd;
export const coinUsd = client.coinUsd;
