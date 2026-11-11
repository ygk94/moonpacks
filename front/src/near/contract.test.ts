import { beforeEach, describe, expect, it, vi } from "vitest";

const view = vi.fn();
vi.mock("./rpc", async (orig) => ({ ...(await orig<typeof import("./rpc")>()), view: (...a: unknown[]) => view(...a) }));

describe("contract version", () => {
  beforeEach(() => {
    vi.resetModules();
    view.mockReset();
  });

  it("recognises v3 by its get_treasury view", async () => {
    view.mockResolvedValue({ balance: "1" });
    const { isV3Contract } = await import("./contract");
    expect(await isV3Contract()).toBe(true);
    expect(await isV3Contract()).toBe(true);
    expect(view).toHaveBeenCalledTimes(1);
    expect(view).toHaveBeenCalledWith("get_treasury");
  });

  it("treats a contract without get_treasury as app2, once", async () => {
    const { RpcError } = await import("./rpc");
    view.mockRejectedValue(new RpcError("MethodResolveError(MethodNotFound)"));
    const { isV3Contract } = await import("./contract");
    expect(await isV3Contract()).toBe(false);
    await isV3Contract();
    expect(view).toHaveBeenCalledTimes(1);
  });

  it("promises nothing on a network error, and asks again later", async () => {
    view.mockRejectedValueOnce(new Error("RPC 429")).mockResolvedValueOnce({});
    const { isV3Contract } = await import("./contract");
    expect(await isV3Contract()).toBe(false);
    expect(await isV3Contract()).toBe(true);
  });
});

describe("card definitions", () => {
  beforeEach(() => {
    vi.resetModules();
    view.mockReset();
  });

  it("are cached per series (v3 has an entry and a standard series)", async () => {
    view.mockImplementation(async (method: string, args: { series_id: number }) =>
      method === "get_series" ? { card_count: 1 } : [{ card_id: `card-of-series-${args.series_id}` }],
    );
    const { getCardDefs } = await import("./contract");
    expect((await getCardDefs(0))[0].card_id).toBe("card-of-series-0");
    expect((await getCardDefs(1))[0].card_id).toBe("card-of-series-1");
    await getCardDefs(1);
    expect(view.mock.calls.filter(([m]) => m === "get_series_cards")).toHaveLength(2);
  });
});
