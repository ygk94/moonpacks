// Logique pure de l'indexeur (testée par vitest) : extraction des événements d'une transaction et classement.

/**
 * Événements Memaster (NEP-297) d'une transaction de l'API fastnear (`/v0/transactions`) : journaux des reçus
 * exécutés par `contractId`, dans l'ordre d'exécution (hauteur, puis ordre dans le bloc).
 */
export function eventsFromTx(tx, contractId) {
  const receipts = [...(tx?.receipts ?? [])].sort(
    (a, b) =>
      a.execution_outcome.block_height - b.execution_outcome.block_height ||
      (a.execution_outcome.index ?? 0) - (b.execution_outcome.index ?? 0),
  );
  const out = [];
  for (const r of receipts) {
    const eo = r.execution_outcome;
    const outcome = eo?.outcome;
    if (!outcome || outcome.executor_id !== contractId) continue;
    // Reçu en échec : son état est annulé, ses journaux ne comptent pas.
    if (outcome.status && typeof outcome.status === "object" && "Failure" in outcome.status) continue;
    const ts = Math.floor(Number(eo.block_timestamp) / 1e6);
    outcome.logs.forEach((log, i) => {
      if (!log.startsWith("EVENT_JSON:")) return;
      let e;
      try {
        e = JSON.parse(log.slice("EVENT_JSON:".length));
      } catch {
        return;
      }
      if (e.standard !== "memaster") return;
      for (const data of e.data ?? []) {
        out.push({
          height: eo.block_height,
          ts,
          receipt_id: eo.id,
          log_index: i,
          event: e.event,
          token_id: data.token_id != null ? String(data.token_id) : null,
          data,
        });
      }
    });
  }
  return out;
}

/** Cartes d'un `pack_revealed` : identité publique de chaque token (jamais de card_id pour une mythique). */
export function tokensFromReveal(data, cardIdOf) {
  return (data.draws ?? []).map((d) => ({
    token_id: String(d.token_id),
    series_id: data.series_id,
    kind: d.kind,
    card_index: d.kind === "visible" ? d.index : null,
    card_id: d.kind === "visible" ? (cardIdOf(data.series_id, d.index) ?? null) : null,
    rarity: d.final_rarity,
  }));
}

/**
 * Classement « Trending » sur une fenêtre : par carte (ou « mythic » pour toutes les mythiques),
 * ventes et mises en vente, volume et dernier prix. Score = 2 × ventes + annonces.
 * `rows` : { event, card_id, kind, rarity, price, ts }.
 */
export function rankTrending(rows, limit = 8) {
  const by = new Map();
  for (const r of rows) {
    const key = r.kind === "mythic" ? "mythic" : r.card_id;
    if (!key) continue;
    let g = by.get(key);
    if (!g) {
      g = { card_id: r.kind === "mythic" ? null : r.card_id, kind: r.kind, rarity: r.rarity, sales: 0, listings: 0, volume: 0n, last_price: null, last_ts: 0 };
      by.set(key, g);
    }
    if (r.event === "card_sold") {
      g.sales++;
      g.volume += BigInt(r.price ?? 0);
      if (r.ts >= g.last_ts) {
        g.last_price = r.price;
        g.last_ts = r.ts;
      }
    } else if (r.event === "card_listed") {
      g.listings++;
    }
  }
  return [...by.values()]
    .map((g) => ({ ...g, score: 2 * g.sales + g.listings, volume: g.volume.toString() }))
    .sort((a, b) => b.score - a.score || b.sales - a.sales || b.last_ts - a.last_ts)
    .slice(0, limit)
    .map(({ last_ts: _, ...g }) => g);
}

/** Adresse d'écoute de l'API : la machine seule par défaut, `INDEXER_HOST` pour l'ouvrir (ex. 0.0.0.0). */
export function listenHost(env) {
  return env.INDEXER_HOST || "127.0.0.1";
}
