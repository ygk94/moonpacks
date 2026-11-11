import { describe, expect, it } from "vitest";
import { eventsOf, failureOf, findEvent, parseLogs, returnValue, txHashOf } from "./events";

const ev = (event: string, data: object) =>
  `EVENT_JSON:${JSON.stringify({ standard: "memaster", version: "1.0.0", event, data: [data] })}`;

describe("events", () => {
  it("keeps only memaster NEP-297 events", () => {
    const logs = [
      ev("pack_bought", { pack_id: 7 }),
      `EVENT_JSON:${JSON.stringify({ standard: "nep171", version: "1.0.0", event: "nft_mint", data: [] })}`,
      "plain log",
      "EVENT_JSON:{broken",
    ];
    expect(parseLogs(logs).map((e) => e.event)).toEqual(["pack_bought"]);
  });

  it("reads events from the transaction and every receipt", () => {
    const outcome = {
      transaction_outcome: { outcome: { logs: [] } },
      receipts_outcome: [
        { outcome: { logs: [ev("pack_bought", { pack_id: 3 })], status: {}, executor_id: "c" } },
        { outcome: { logs: [ev("pack_revealed", { pack_id: 3 })], status: {}, executor_id: "c" } },
      ],
    };
    const events = eventsOf(outcome);
    expect(events.map((e) => e.event)).toEqual(["pack_bought", "pack_revealed"]);
    expect(findEvent(events, "pack_bought")).toEqual({ pack_id: 3 });
    expect(findEvent(events, "card_sold")).toBeUndefined();
  });

  it("tolerates an event without data", () => {
    const events = parseLogs([`EVENT_JSON:${JSON.stringify({ standard: "memaster", version: "1.0.0", event: "pack_bought" })}`]);
    expect(findEvent(events, "pack_bought")).toBeUndefined();
  });

  it("finds the transaction hash in what a wallet returns", () => {
    const h = "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin";
    expect(txHashOf({ transaction: { hash: h } })).toBe(h);
    expect(txHashOf({ transaction_outcome: { id: h } })).toBe(h);
    expect(txHashOf(h)).toBe(h);
    expect(txHashOf(undefined)).toBeUndefined();
    expect(txHashOf({})).toBeUndefined();
    expect(txHashOf("not a hash")).toBeUndefined();
  });

  it("decodes the return value", () => {
    expect(returnValue<string>({ status: { SuccessValue: btoa('"31"') } })).toBe("31");
    expect(returnValue({ status: { SuccessValue: "" } })).toBeUndefined();
    expect(returnValue({ status: { Failure: {} } })).toBeUndefined();
  });

  it("finds the contract panic in a failed receipt", () => {
    const outcome = {
      status: { SuccessValue: "" },
      receipts_outcome: [
        {
          outcome: {
            logs: [],
            executor_id: "c",
            status: {
              Failure: {
                ActionError: {
                  kind: { FunctionCallError: { ExecutionError: "Smart contract panicked: Dépôt insuffisant : 1 yoctoNEAR requis" } },
                },
              },
            },
          },
        },
      ],
    };
    expect(failureOf(outcome)).toBe("Dépôt insuffisant : 1 yoctoNEAR requis");
  });
});
