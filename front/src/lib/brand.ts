// Nom affiché du projet. Le contrat et ses séries portent encore « Memaster » (nom provisoire, écrit on-chain) :
// on le remplace à l'affichage.

export const BRAND = "Moonpacks";

/** « Memaster Entry » → « Moonpacks Entry ». */
export function seriesName(name: string): string {
  return name.replace(/^Memaster\b/i, BRAND);
}
