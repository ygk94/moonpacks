// Les messages de panique du contrat sont en français : on les traduit pour l'interface (anglais seulement).

const MESSAGES: [RegExp, string][] = [
  [/Dépôt insuffisant/, "Insufficient deposit: the attached amount must cover the pack price plus the storage deposit."],
  // Le message propre au burn avant le message générique (le premier qui correspond l'emporte).
  [/Gaz insuffisant pour le burn/, "Not enough gas attached for the burn. Please try again."],
  [/Gaz insuffisant/, "Not enough gas attached to the transaction. Please try again."],
  [/Série non ouverte/, "This series is not on sale right now."],
  [/Série inconnue/, "This pack series does not exist."],
  [/Délai de relance non écoulé/, "The reveal can only be retried a little later. Please wait a few seconds."],
  [/Tirage déjà écrit/, "This pack is already revealed."],
  [/Pack inconnu/, "Unknown pack."],
  [/Seul le propriétaire peut brûler/, "Only the owner of this card can burn it."],
  [/Carte en vente : retirez/, "This card is listed for sale. Remove the listing before burning it."],
  [/Burn déjà en cours/, "A burn is already in progress for this card."],
  [/Carte non brûlable/, "This card is not burnable."],
  [/Aucun redeemer/, "Burning is not available right now."],
  [/Le prix de l'annonce a changé/, "The listing price changed. Please check the new price."],
  [/Déjà en vente/, "This card is already listed."],
  [/Prix nul|Le prix doit être > 0/, "The price must be greater than zero."],
  [/Dépôt d'annonce/, "Listing a card requires a small storage deposit, returned when the listing ends."],
  [/Pas en vente/, "This card is not listed anymore."],
  [/Le vendeur ne peut pas acheter/, "You cannot buy your own card."],
  [/Annonce périmée/, "This listing is outdated."],
  [/Dépôt inférieur au prix/, "The attached amount is lower than the price."],
  [/Carte en cours de burn/, "This card is being burned."],
  [/Seul le propriétaire peut vendre/, "Only the owner can list this card."],
  [/Seul le vendeur peut retirer/, "Only the seller can remove this listing."],
  [/Carte inconnue/, "Unknown card."],
  [/NotEnoughBalance|LackBalanceForState|not enough balance/i, "Your wallet balance is too low for this transaction."],
  [/reject|cancel|denied|closed|User rejected/i, "Transaction cancelled in the wallet."],
];

export function humanError(e: unknown): string {
  const raw = e instanceof Error ? e.message : typeof e === "string" ? e : JSON.stringify(e);
  for (const [re, msg] of MESSAGES) if (re.test(raw)) return msg;
  return raw.length > 200 ? raw.slice(0, 200) + "…" : raw || "Something went wrong.";
}
