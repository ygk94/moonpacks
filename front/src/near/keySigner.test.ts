// Signature locale du wallet de test : base58, borsh d'une transaction, signature ed25519 vérifiable.
// Clé générée pour le test, jamais une vraie clé.

import { describe, expect, it } from "vitest";
import { base58Decode, base58Encode, keyPairFromSecret, serializeTx, signTx } from "./keySigner";

async function freshSecret(): Promise<{ secret: string; spki: CryptoKey }> {
  const kp = (await crypto.subtle.generateKey({ name: "Ed25519" }, true, ["sign", "verify"])) as CryptoKeyPair;
  const pkcs8 = new Uint8Array(await crypto.subtle.exportKey("pkcs8", kp.privateKey));
  const pub = new Uint8Array(await crypto.subtle.exportKey("raw", kp.publicKey));
  const raw = new Uint8Array(64);
  raw.set(pkcs8.slice(16, 48));
  raw.set(pub, 32);
  return { secret: `ed25519:${base58Encode(raw)}`, spki: kp.publicKey };
}

describe("key signer", () => {
  it("round-trips base58, leading zeros included", () => {
    const b = Uint8Array.from([0, 0, 1, 2, 255, 128]);
    expect(base58Decode(base58Encode(b))).toEqual(b);
    expect(base58Encode(Uint8Array.from([0, 0]))).toBe("11");
    // Hash de bloc connu (32 octets).
    expect(base58Decode("11111111111111111111111111111111").length).toBe(32);
  });

  it("serializes a FunctionCall transaction in borsh", () => {
    const bytes = serializeTx({
      signerId: "a",
      publicKey: new Uint8Array(32).fill(1),
      nonce: 5n,
      receiverId: "b",
      blockHash: new Uint8Array(32).fill(2),
      actions: [{ type: "FunctionCall", methodName: "m", args: { x: 1 }, gas: "7", deposit: "9" }],
    });
    const hex = Buffer.from(bytes).toString("hex");
    const expected =
      "01000000" + "61" + // signer_id
      "00" + "01".repeat(32) + // public_key
      "0500000000000000" + // nonce
      "01000000" + "62" + // receiver_id
      "02".repeat(32) + // block_hash
      "01000000" + // 1 action
      "02" + "01000000" + "6d" + // FunctionCall, method
      "07000000" + Buffer.from('{"x":1}').toString("hex") + // args
      "0700000000000000" + // gas
      "09" + "00".repeat(15); // deposit u128
    expect(hex).toBe(expected);
  });

  it("signs the sha256 of the transaction with the ed25519 key", async () => {
    const { secret, spki } = await freshSecret();
    const key = await keyPairFromSecret(secret);
    const tx = {
      signerId: "buyer.testnet",
      publicKey: key.publicKey,
      nonce: 1n,
      receiverId: "app.testnet",
      blockHash: new Uint8Array(32),
      actions: [{ type: "Transfer" as const, deposit: "1" }],
    };
    const { signed, hash } = await signTx(tx, key);
    const body = serializeTx(tx);
    const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", body));
    expect(hash).toBe(base58Encode(digest));
    expect(signed.slice(0, body.length)).toEqual(body);
    expect(signed[body.length]).toBe(0);
    const sig = signed.slice(body.length + 1);
    expect(sig.length).toBe(64);
    expect(await crypto.subtle.verify({ name: "Ed25519" }, spki, sig, digest)).toBe(true);
  });

  it("rejects a malformed key without echoing it", async () => {
    await expect(keyPairFromSecret("ed25519:abc")).rejects.toThrow("Expected a 64-byte ed25519 secret key.");
    await expect(keyPairFromSecret("secp256k1:zzz")).rejects.toThrow("Expected an ed25519 secret key.");
  });
});
