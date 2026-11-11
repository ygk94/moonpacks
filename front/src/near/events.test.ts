import { describe, expect, it } from "vitest";
import { humanError } from "./errors";
import { eventsOf, failureOf, findEvent, parseLogs, returnValue } from "./events";

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

describe("contract errors in English", () => {
  it("translates known panics", () => {
    expect(humanError(new Error("Dépôt insuffisant : 116 yoctoNEAR requis"))).toMatch(/^Insufficient deposit/);
    expect(humanError("Carte en vente : retirez l'annonce d'abord")).toMatch(/listed for sale/);
    expect(humanError(new Error("Le prix de l'annonce a changé"))).toMatch(/price changed/);
    expect(humanError(new Error("User rejected the request"))).toBe("Transaction cancelled in the wallet.");
  });
  it("never leaves French text from the contract", () => {
    const panics = [
      "Gaz insuffisant : 160 Tgas requis",
      "Série non ouverte à la vente",
      "Délai de relance non écoulé",
      "Tirage déjà écrit : relance interdite",
      "Seul le propriétaire peut brûler",
      "Burn déjà en cours",
      "Carte non brûlable",
      "Déjà en vente",
      "Pas en vente",
      "Le vendeur ne peut pas acheter sa carte",
      "Annonce périmée",
      "Dépôt inférieur au prix",
      "Carte en cours de burn",
    ];
    for (const p of panics) expect(humanError(new Error(p)), p).not.toMatch(/[éèàç]|Carte|Dépôt|Série/);
  });
});
