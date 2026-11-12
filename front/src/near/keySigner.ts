// Signature locale d'une transaction NEAR avec une clé ed25519 : base58, borsh minimal, WebCrypto.
// Réservé aux tests de bout en bout (wallet de test, `testKeyWallet.ts`) et au script `npm run e2e`.
// Aucune dépendance et aucune importation, pour être chargé aussi par Node (`scripts/e2e.mjs`).
// Ne journalise jamais la clé.

const ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";

export function base58Decode(s: string): Uint8Array {
  let n = 0n;
  for (const ch of s) {
    const v = ALPHABET.indexOf(ch);
    if (v < 0) throw new Error("Invalid base58 string.");
    n = n * 58n + BigInt(v);
  }
  const bytes: number[] = [];
  while (n > 0n) {
    bytes.unshift(Number(n & 0xffn));
    n >>= 8n;
  }
  for (const ch of s) {
    if (ch !== "1") break;
    bytes.unshift(0);
  }
  return Uint8Array.from(bytes);
}

export function base58Encode(b: Uint8Array): string {
  let n = 0n;
  for (const x of b) n = (n << 8n) | BigInt(x);
  let out = "";
  while (n > 0n) {
    out = ALPHABET[Number(n % 58n)] + out;
    n /= 58n;
  }
  for (const x of b) {
    if (x !== 0) break;
    out = "1" + out;
  }
  return out;
}

export function toBase64(b: Uint8Array): string {
  let s = "";
  for (const x of b) s += String.fromCharCode(x);
  return btoa(s);
}

// Borsh : seulement ce que demande une transaction.
class Writer {
  private parts: number[] = [];
  u8(v: number) {
    this.parts.push(v & 0xff);
  }
  u32(v: number) {
    for (let i = 0; i < 4; i++) this.parts.push((v >>> (8 * i)) & 0xff);
  }
  uint(v: bigint, bytes: number) {
    if (v < 0n || v >= 1n << BigInt(8 * bytes)) throw new Error("Integer out of range.");
    for (let i = 0; i < bytes; i++) this.parts.push(Number((v >> BigInt(8 * i)) & 0xffn));
  }
  bytes(b: Uint8Array) {
    for (const x of b) this.parts.push(x);
  }
  vec(b: Uint8Array) {
    this.u32(b.length);
    this.bytes(b);
  }
  str(s: string) {
    this.vec(new TextEncoder().encode(s));
  }
  done(): Uint8Array<ArrayBuffer> {
    return Uint8Array.from(this.parts);
  }
}

export type KeyAction =
  | { type: "FunctionCall"; methodName: string; args: Record<string, unknown> | Uint8Array; gas: string; deposit: string }
  | { type: "Transfer"; deposit: string }
  | { type: "DeleteAccount"; beneficiaryId: string };

export interface UnsignedTx {
  signerId: string;
  publicKey: Uint8Array; // 32 octets
  nonce: bigint;
  receiverId: string;
  blockHash: Uint8Array; // 32 octets
  actions: KeyAction[];
}

export function serializeTx(tx: UnsignedTx): Uint8Array<ArrayBuffer> {
  if (tx.publicKey.length !== 32 || tx.blockHash.length !== 32) throw new Error("Bad key or block hash length.");
  const w = new Writer();
  w.str(tx.signerId);
  w.u8(0); // ed25519
  w.bytes(tx.publicKey);
  w.uint(tx.nonce, 8);
  w.str(tx.receiverId);
  w.bytes(tx.blockHash);
  w.u32(tx.actions.length);
  for (const a of tx.actions) {
    if (a.type === "FunctionCall") {
      w.u8(2);
      w.str(a.methodName);
      w.vec(a.args instanceof Uint8Array ? a.args : new TextEncoder().encode(JSON.stringify(a.args)));
      w.uint(BigInt(a.gas), 8);
      w.uint(BigInt(a.deposit), 16);
    } else if (a.type === "Transfer") {
      w.u8(3);
      w.uint(BigInt(a.deposit), 16);
    } else {
      w.u8(7);
      w.str(a.beneficiaryId);
    }
  }
  return w.done();
}

/** Clé NEAR `ed25519:<base58 de 64 octets>` (graine puis clé publique). */
export interface KeyPair {
  publicKey: Uint8Array;
  publicKeyText: string;
  sign: (msg: Uint8Array<ArrayBuffer>) => Promise<Uint8Array>;
}

const PKCS8_ED25519_PREFIX = Uint8Array.from([0x30, 0x2e, 0x02, 0x01, 0x00, 0x30, 0x05, 0x06, 0x03, 0x2b, 0x65, 0x70, 0x04, 0x22, 0x04, 0x20]);

export async function keyPairFromSecret(secret: string): Promise<KeyPair> {
  const m = /^ed25519:([1-9A-HJ-NP-Za-km-z]+)$/.exec(secret.trim());
  if (!m) throw new Error("Expected an ed25519 secret key.");
  const raw = base58Decode(m[1]);
  if (raw.length !== 64) throw new Error("Expected a 64-byte ed25519 secret key.");
  const seed = raw.slice(0, 32);
  const publicKey = raw.slice(32);
  const pkcs8 = new Uint8Array(48);
  pkcs8.set(PKCS8_ED25519_PREFIX);
  pkcs8.set(seed, 16);
  const key = await crypto.subtle.importKey("pkcs8", pkcs8, { name: "Ed25519" }, false, ["sign"]);
  return {
    publicKey,
    publicKeyText: `ed25519:${base58Encode(publicKey)}`,
    sign: async (msg) => new Uint8Array(await crypto.subtle.sign({ name: "Ed25519" }, key, msg)),
  };
}

/** Transaction signée (borsh) et son hash en base58. */
export async function signTx(tx: UnsignedTx, key: KeyPair): Promise<{ signed: Uint8Array; hash: string }> {
  const body = serializeTx(tx);
  const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", body));
  const sig = await key.sign(digest);
  const signed = new Uint8Array(body.length + 1 + 64);
  signed.set(body);
  signed[body.length] = 0; // ed25519
  signed.set(sig, body.length + 1);
  return { signed, hash: base58Encode(digest) };
}

type Rpc = <T>(method: string, params: unknown) => Promise<T>;

export function jsonRpc(url: string): Rpc {
  let id = 1;
  return async <T>(method: string, params: unknown): Promise<T> => {
    for (let attempt = 0; ; attempt++) {
      const res = await fetch(url, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ jsonrpc: "2.0", id: id++, method, params }),
      }).catch((e: unknown) => ({ status: 0, error: e }) as const);
      // Limite de débit ou panne passagère : on réessaie (la transaction n'est envoyée qu'une fois par hash).
      if (!("json" in res) || res.status === 429 || res.status >= 500) {
        if (attempt >= 5) throw new Error(`RPC unavailable (${res.status})`);
        await new Promise((r) => setTimeout(r, 500 * 2 ** attempt));
        continue;
      }
      const body = await res.json();
      if (body.error) {
        const data = body.error.data ?? body.error.cause ?? body.error.message;
        const err = new Error(typeof data === "string" ? data : JSON.stringify(data)) as Error & { rpcName?: string };
        err.rpcName = body.error.cause?.name ?? body.error.name;
        throw err;
      }
      return body.result as T;
    }
  };
}

/**
 * Signe et envoie une transaction, puis attend son exécution (`EXECUTED_OPTIMISTIC`, reçus compris).
 * Renvoie le résultat complet de `send_tx`, ou `{ transaction: { hash } }` si l'attente du RPC expire :
 * l'appelant relit alors la transaction par son hash.
 */
export async function signAndSend(
  rpc: Rpc,
  key: KeyPair,
  signerId: string,
  receiverId: string,
  actions: KeyAction[],
): Promise<unknown> {
  const ak = await rpc<{ nonce: number | string; block_hash: string }>("query", {
    request_type: "view_access_key",
    finality: "final",
    account_id: signerId,
    public_key: key.publicKeyText,
  });
  const { signed, hash } = await signTx(
    { signerId, publicKey: key.publicKey, nonce: BigInt(ak.nonce) + 1n, receiverId, blockHash: base58Decode(ak.block_hash), actions },
    key,
  );
  try {
    return await rpc("send_tx", { signed_tx_base64: toBase64(signed), wait_until: "EXECUTED_OPTIMISTIC" });
  } catch (e) {
    const name = (e as { rpcName?: string }).rpcName;
    if (name === "TIMEOUT_ERROR" || /timeout/i.test(String((e as Error).message))) return { transaction: { hash } };
    throw e;
  }
}
