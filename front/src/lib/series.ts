// Séries affichées par la page des taux et le gold rush (contrat v3 : « entrée » et « standard »).

import type { RushState, SeriesView } from "../near/types";

/** Séries dont les taux sont publics : table figée, et pas en brouillon ni supprimées. */
export function publicSeries(all: SeriesView[]): SeriesView[] {
  return all.filter((s) => s.table_hash != null && s.status !== "draft" && s.status !== "deleted");
}

/** Série choisie : celle de `?series=N` si elle existe, sinon `fallback` (VITE_SERIES_ID), sinon la première. */
export function pickSeries(param: string | null, list: SeriesView[], fallback: number): number | null {
  if (!list.length) return null;
  const ids = list.map((s) => s.series_id);
  const wanted = param != null && /^\d+$/.test(param) ? Number(param) : null;
  if (wanted != null && ids.includes(wanted)) return wanted;
  return ids.includes(fallback) ? fallback : ids[0];
}

/** Seuil du gold rush : au moins `min_packs` dans la fenêtre, et un rythme `ratio` fois supérieur à la moyenne. */
export function rushTarget(rush: Pick<RushState, "params" | "baseline_count">): number {
  const p = rush.params!;
  const bsz = Math.max(1, p.bucket_blocks);
  const ml = Math.max(1, Math.floor(p.baseline_blocks / bsz));
  const mw = Math.min(Math.max(1, Math.floor(p.window_blocks / bsz)), ml);
  const baseline = rush.baseline_count ?? 0;
  const byRatio = Math.ceil((p.ratio_bps * baseline * mw) / (ml * 10_000));
  return Math.max(p.min_packs, byRatio, 1);
}
