// Ordre de révélation d'un pack : l'ordre des emplacements, sauf la ou les brûlables, montrées en dernier.

export function burnableLast<T extends { burnable: boolean }>(cards: T[]): T[] {
  return [...cards.filter((c) => !c.burnable), ...cards.filter((c) => c.burnable)];
}
