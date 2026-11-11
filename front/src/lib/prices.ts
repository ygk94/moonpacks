// Cours hors chaîne, lus par des API publiques sans clé :
// - NEAR/USD : CoinGecko ;
// - cours d'un coin : DexScreener (par adresse, toutes chaînes, pool le plus liquide), sinon CoinGecko (par id).
// Voir docs/oracle-prix.md. Ces cours servent à l'affichage seulement, jamais à une « valeur garantie ».

const TTL = 60_000;
const cache = new Map<string, { at: number; value: Promise<number | null> }>();

function cached(key: string, load: () => Promise<number | null>): Promise<number | null> {
  const hit = cache.get(key);
  if (hit && Date.now() - hit.at < TTL) return hit.value;
  const value = load().catch(() => null);
  cache.set(key, { at: Date.now(), value });
  return value;
}

async function coingecko(id: string): Promise<number | null> {
  const r = await fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${encodeURIComponent(id)}&vs_currencies=usd`);
  if (!r.ok) return null;
  const j = await r.json();
  const v = j?.[id]?.usd;
  return typeof v === "number" && v > 0 ? v : null;
}

async function dexscreener(address: string): Promise<number | null> {
  const r = await fetch(`https://api.dexscreener.com/latest/dex/tokens/${encodeURIComponent(address)}`);
  if (!r.ok) return null;
  const j = await r.json();
  const pairs: { priceUsd?: string; liquidity?: { usd?: number }; baseToken?: { address?: string } }[] = j?.pairs ?? [];
  const own = pairs.filter((p) => p.baseToken?.address?.toLowerCase() === address.toLowerCase() && p.priceUsd);
  own.sort((a, b) => (b.liquidity?.usd ?? 0) - (a.liquidity?.usd ?? 0));
  const v = Number(own[0]?.priceUsd);
  return v > 0 ? v : null;
}

export const nearUsd = () => cached("near", () => coingecko("near"));

export function coinUsd(coin: { address: string | null; coingecko: string | null }): Promise<number | null> {
  const key = `coin:${coin.address ?? ""}:${coin.coingecko ?? ""}`;
  return cached(key, async () => {
    if (coin.address) {
      const v = await dexscreener(coin.address).catch(() => null);
      if (v) return v;
    }
    return coin.coingecko ? coingecko(coin.coingecko) : null;
  });
}
