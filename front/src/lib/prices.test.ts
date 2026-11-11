import { describe, expect, it } from "vitest";
import { createPriceClient, TTL_MS } from "./prices";

function memoryStorage(): Storage {
  const m = new Map<string, string>();
  return {
    get length() {
      return m.size;
    },
    clear: () => m.clear(),
    getItem: (k) => m.get(k) ?? null,
    key: (i) => [...m.keys()][i] ?? null,
    removeItem: (k) => void m.delete(k),
    setItem: (k, v) => void m.set(k, v),
  };
}

const json = (body: unknown, status = 200) => ({
  ok: status >= 200 && status < 300,
  status,
  json: async () => body,
  headers: new Headers(),
});

function setup(responder: (url: string) => ReturnType<typeof json> | Promise<never>, storage: Storage = memoryStorage()) {
  const calls: string[] = [];
  let t = 1_000_000;
  const client = createPriceClient({
    fetch: async (url) => {
      calls.push(url);
      return responder(url);
    },
    storage: () => storage,
    now: () => t,
    batchMs: 0,
  });
  return { client, calls, storage, advance: (ms: number) => (t += ms) };
}

const geckoIds = (url: string) => decodeURIComponent(new URL(url).searchParams.get("ids") ?? "").split(",");

describe("public prices: cache, batching, back-off", () => {
  it("groups the CoinGecko ids asked together into one call", async () => {
    const { client, calls } = setup(() => json({ near: { usd: 2.5 }, "coin-alpha": { usd: 0.1 }, "coin-beta": { usd: 0.00001 } }));
    const [n, d, p] = await Promise.all([client.nearUsd(), client.coingecko("coin-alpha"), client.coingecko("coin-beta")]);
    expect([n, d, p]).toEqual([2.5, 0.1, 0.00001]);
    expect(calls).toHaveLength(1);
    expect(geckoIds(calls[0]).sort()).toEqual(["coin-alpha", "coin-beta", "near"]);
  });

  it("serves the cache for 5 minutes, then asks again", async () => {
    const { client, calls, advance } = setup(() => json({ near: { usd: 3 } }));
    await client.nearUsd();
    advance(TTL_MS - 1);
    expect(await client.nearUsd()).toBe(3);
    expect(calls).toHaveLength(1);
    advance(2);
    await client.nearUsd();
    expect(calls).toHaveLength(2);
  });

  it("keeps the cache in localStorage across page loads", async () => {
    const storage = memoryStorage();
    const first = setup(() => json({ near: { usd: 4 } }), storage);
    await first.client.nearUsd();
    const second = setup(() => {
      throw new Error("must not be called");
    }, storage);
    expect(await second.client.nearUsd()).toBe(4);
    expect(second.calls).toHaveLength(0);
  });

  it("works when localStorage throws", async () => {
    const broken = {
      getItem: () => {
        throw new Error("SecurityError");
      },
      setItem: () => {
        throw new Error("QuotaExceededError");
      },
    } as unknown as Storage;
    const { client } = setup(() => json({ near: { usd: 5 } }), broken);
    expect(await client.nearUsd()).toBe(5);
    expect(await client.nearUsd()).toBe(5);
  });

  it("backs off after a 429 and keeps showing the last known price", async () => {
    let status = 200;
    const { client, calls, advance } = setup(() => (status === 200 ? json({ near: { usd: 6 } }) : json({}, status)));
    expect(await client.nearUsd()).toBe(6);
    advance(TTL_MS + 1);
    status = 429;
    expect(await client.nearUsd()).toBe(6); // périmé mais connu : pas « Not available »
    expect(client.isBackingOff()).toBe(true);
    expect(calls).toHaveLength(2);
    // Pendant le recul, aucun appel.
    advance(10_000);
    expect(await client.nearUsd()).toBe(6);
    expect(calls).toHaveLength(2);
    // Après le recul, on redemande ; un succès lève le recul.
    status = 200;
    advance(30_000);
    expect(await client.nearUsd()).toBe(6);
    expect(calls).toHaveLength(3);
    expect(client.isBackingOff()).toBe(false);
  });

  it("treats a CORS-less 429 (network error) like a 429", async () => {
    const { client } = setup(() => Promise.reject(new TypeError("Failed to fetch")));
    expect(await client.nearUsd()).toBeNull();
    expect(client.isBackingOff()).toBe(true);
  });

  it("reads a coin on DexScreener first, with the same cache", async () => {
    const addr = "0xAbC";
    const { client, calls } = setup((url) =>
      url.includes("dexscreener")
        ? json({ pairs: [{ priceUsd: "0.5", liquidity: { usd: 10 }, baseToken: { address: "0xabc" } }] })
        : json({}),
    );
    expect(await client.coinUsd({ address: addr, coingecko: "x" })).toBe(0.5);
    expect(await client.coinUsd({ address: addr, coingecko: "x" })).toBe(0.5);
    expect(calls).toHaveLength(1);
  });
});
