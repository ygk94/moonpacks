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
