import { readdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { CODE_MESSAGES, errorCode, humanError } from "./errors";
import { failureOf } from "./events";

// contract/ERRORS.md: one row per message, `| `E_CODE` | description | who | files |`.
const md = readFileSync(resolve(__dirname, "../../../contract/ERRORS.md"), "utf8");
const rows = md
  .split("\n")
  .filter((l) => l.startsWith("| `E_"))
  .map((l) => ({ code: l.split("|")[1].trim().replace(/`/g, "") }));
// On-chain panic texts, read from the contract source: `"E_CODE: text"` (the text after the code is French).
const src = readdirSync(resolve(__dirname, "../../../contract/src"))
  .filter((f) => f.endsWith(".rs") && !f.startsWith("tests"))
  .map((f) => readFileSync(resolve(__dirname, "../../../contract/src", f), "utf8"))
  .join("\n");
const messages = [...src.matchAll(/"(E_[A-Z0-9_]+): ((?:[^"\\]|\\.)*)"/g)].map((m) => ({ code: m[1], fr: m[2].replace(/\\"/g, '"') }));
const documented = new Set(rows.map((r) => r.code));
const panic = (text: string) => new Error(`Smart contract panicked: ${text}`);
// Inserted values: a number for each `{…}` of the message.
const sample = (fr: string) => fr.replace(/\{[^}]*\}/g, "42");

describe("contract error codes (contract/ERRORS.md)", () => {
  it("reads the codes of ERRORS.md", () => {
    expect(rows.length).toBeGreaterThan(100);
    expect(documented.size).toBeGreaterThan(80);
    expect(documented).toContain("E_NOT_PACK_OWNER");
  });

  it("translates every documented code", () => {
    const missing = [...documented].filter((c) => !CODE_MESSAGES[c]);
    expect(missing, "codes of ERRORS.md without a translation in errors.ts").toEqual([]);
  });

  it("translates no code that the contract does not have", () => {
    const unknown = Object.keys(CODE_MESSAGES).filter((c) => !documented.has(c));
    expect(unknown, "codes in errors.ts that are not in ERRORS.md").toEqual([]);
  });

  it("reads the panic messages of the contract source", () => {
    expect(messages.length).toBeGreaterThan(100);
    expect(messages.filter((m) => !documented.has(m.code))).toEqual([]);
  });

  it("gives an English text for every contract message, without French or a raw panic", () => {
    for (const r of messages) {
      const out = humanError(panic(`${r.code}: ${sample(r.fr)}`));
      expect(out, r.fr).not.toMatch(/[éèàçêô]|panicked|E_[A-Z]|\{/);
      expect(out.length, r.fr).toBeGreaterThan(5);
    }
  });

  it("uses the English proposal of ERRORS.md", () => {
    expect(humanError(panic("E_NOT_PACK_OWNER: Seul l'acheteur du pack peut relancer le tirage"))).toBe(
      "Only the buyer of this pack can retry the reveal.",
    );
    expect(humanError(panic("E_NOT_STUCK: Seul un pack bloqué (stuck) est remboursable"))).toBe("Only a stuck pack can be refunded.");
    expect(humanError(panic("E_SELF_BUY: Le vendeur ne peut pas acheter sa carte"))).toBe("The seller cannot buy their own card.");
  });

  it("picks the variant from the French text", () => {
    expect(humanError(panic("E_GAS: Gaz insuffisant pour le burn"))).toBe("Not enough gas attached for the burn.");
    expect(humanError(panic("E_GAS: Gaz insuffisant : 160 Tgas requis"))).toBe("Not enough gas attached: 160 Tgas required.");
    expect(humanError(panic("E_ALREADY_REVEALED: Tirage déjà écrit : remboursement interdit"))).toMatch(/refund refused/);
    expect(humanError(panic("E_CARD_REDEEMING: Carte en cours de burn : transfert refusé"))).toMatch(/transfer refused/);
    expect(humanError(panic("E_CARD_REDEEMING: Carte en cours de burn"))).toBe("This card is being burned.");
  });

  it("shows yoctoNEAR amounts in NEAR", () => {
    const msg = "E_DEPOSIT: Dépôt insuffisant : 116000000000000000000000 yoctoNEAR requis (prix 100000000000000000000000 + stockage 16050000000000000000000)";
    expect(humanError(panic(msg))).toBe("Insufficient deposit: 0.116 NEAR required (price 0.1 NEAR + storage 0.01605 NEAR).");
    expect(humanError(panic("E_LISTING_DEPOSIT: Dépôt d'annonce : 5000000000000000000000 yoctoNEAR requis"))).toBe(
      "Listing deposit: 0.005 NEAR required.",
    );
  });

  it("still translates a code whose French text changed", () => {
    expect(humanError(panic("E_SELF_BUY: nouveau texte"))).toBe("The seller cannot buy their own card.");
    expect(humanError(panic("E_GAS: autre texte"))).toBe("Not enough gas attached: … required.");
  });

  it("reads the code through failureOf, as the wallet hook does", () => {
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
                  kind: { FunctionCallError: { ExecutionError: "Smart contract panicked: E_STALE_LISTING: Annonce périmée" } },
                },
              },
            },
          },
        },
      ],
    };
    const f = failureOf(outcome)!;
    expect(errorCode(f)).toEqual({ code: "E_STALE_LISTING", text: "Annonce périmée" });
    expect(humanError(new Error(f))).toBe("This listing is outdated.");
  });
});

describe("contract errors without a code (app2, protocol, wallet)", () => {
  it("translates known panics", () => {
    expect(humanError(new Error("Dépôt insuffisant : 116 yoctoNEAR requis"))).toMatch(/^Insufficient deposit/);
    expect(humanError("Carte en vente : retirez l'annonce d'abord")).toMatch(/listed for sale/);
    expect(humanError(new Error("Le prix de l'annonce a changé"))).toMatch(/price changed/);
    expect(humanError(new Error("User rejected the request"))).toBe("Transaction cancelled in the wallet.");
    expect(humanError(new Error("LackBalanceForState"))).toMatch(/balance is too low/);
  });

  it("never leaves French text from the app2 contract", () => {
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

  it("keeps the burn-specific gas message", () => {
    expect(humanError(new Error("Gaz insuffisant pour le burn"))).toMatch(/for the burn/);
    expect(humanError(new Error("Gaz insuffisant : 160 Tgas requis"))).toMatch(/^Not enough gas attached to the transaction/);
  });

  it("falls back to the raw message for an unknown code", () => {
    expect(humanError(new Error("E_SOMETHING_NEW: nouveau"))).toBe("E_SOMETHING_NEW: nouveau");
  });
});
