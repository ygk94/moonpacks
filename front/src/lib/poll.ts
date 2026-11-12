// Relecture après une transaction : un nœud RPC en retard peut encore renvoyer l'ancien état juste après
// l'exécution (vu par `npm run e2e` : après une nouvelle mise en vente, le détail montrait encore « List »).

/** Relit `read()` jusqu'à ce que `done(valeur)` soit vrai, au plus `tries` fois ; renvoie la dernière valeur lue. */
export async function readUntil<T>(
  read: () => Promise<T>,
  done: (v: T) => boolean,
  { tries = 10, intervalMs = 800, sleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms)) } = {},
): Promise<T | undefined> {
  let last: T | undefined;
  for (let i = 0; i < tries; i++) {
    try {
      last = await read();
      if (done(last)) return last;
    } catch {
      // erreur réseau passagère : on réessaie
    }
    if (i + 1 < tries) await sleep(intervalMs);
  }
  return last;
}
