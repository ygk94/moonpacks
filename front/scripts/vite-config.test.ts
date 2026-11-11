import { afterEach, describe, expect, it, vi } from "vitest";

describe("vite dev server", () => {
  afterEach(() => {
    delete process.env.DEV_HOST;
    vi.resetModules();
  });
  it("listens on 127.0.0.1 by default", async () => {
    delete process.env.DEV_HOST;
    const { default: c } = await import("../vite.config");
    expect(c.server?.host).toBe("127.0.0.1");
    expect(c.preview?.host).toBe("127.0.0.1");
  });
  it("opens to the local network with DEV_HOST", async () => {
    process.env.DEV_HOST = "0.0.0.0";
    const { default: c } = await import("../vite.config");
    expect(c.server?.host).toBe("0.0.0.0");
  });
});
