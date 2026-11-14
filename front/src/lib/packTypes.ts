// Packs thématiques de la boutique : familles de mèmes (Dog, Cat, Frog), chaînes (Solana, BNB Chain, Ethereum) et
// OG (coins de 2013-2018, en packs de 1, 2 et 5 cartes).
//
// Ces packs ne sont pas encore sur le contrat : la boutique les montre « Coming soon ». Chacun devient achetable
// dès qu'une série ouverte porte son nom on-chain (`seriesName`, par exemple « Moonpacks Dog » ; « Memaster » est
// accepté). Les filtres ci-dessous sont aussi ceux à utiliser pour construire la table de la série
// (docs/front/packs-thematiques.md), afin que le site annonce exactement les cartes du pack.

import type { SeriesView } from "../near/types";
import type { CatalogEntry } from "./catalog";

export type PackRowId = "families" | "chains" | "og";

export interface PackType {
  id: string;
  row: PackRowId;
  title: string;
  /** Nom on-chain attendu de la série, sans la marque (« Dog » ↔ « Moonpacks Dog » ou « Memaster Dog »). */
  seriesName: string;
  cards: number;
  emoji: string;
  /** Cartes du catalogue public qui entrent dans le pack. */
  match: (e: CatalogEntry) => boolean;
}

const text = (e: CatalogEntry) => `${e.name} ${e.ticker}`.toLowerCase();
const word = (re: RegExp) => (e: CatalogEntry) => re.test(text(e));

export const DOG = /doge|shib|\binu\b|inu\b|\bdog|dog\b|bonk|floki|\bwif\b|puppy|corgi|pup\b|shiba/;
export const CAT = /\bcat|cat\b|kitty|kitten|popcat|\bmew\b|meow|neko|\bnyan/;
export const FROG = /pepe|frog|toad|ribbit|\bkek\b/;
export const OG_ERA = "2013-2018";

export const PACK_TYPES: PackType[] = [
  // « cat in a dogs world » est un chat : un coin qui est aussi un chat va dans le pack Cat.
  { id: "dog", row: "families", title: "Dog pack", seriesName: "Dog", cards: 5, emoji: "🐕", match: (e) => DOG.test(text(e)) && !CAT.test(text(e)) },
  { id: "cat", row: "families", title: "Cat pack", seriesName: "Cat", cards: 5, emoji: "🐈", match: word(CAT) },
  { id: "frog", row: "families", title: "Frog pack", seriesName: "Frog", cards: 5, emoji: "🐸", match: word(FROG) },
  { id: "solana", row: "chains", title: "Solana pack", seriesName: "Solana", cards: 5, emoji: "◎", match: (e) => e.chain === "Solana" },
  { id: "bnb", row: "chains", title: "BNB Chain pack", seriesName: "BNB Chain", cards: 5, emoji: "⬡", match: (e) => e.chain === "BNB Chain" },
  { id: "ethereum", row: "chains", title: "Ethereum pack", seriesName: "Ethereum", cards: 5, emoji: "Ξ", match: (e) => e.chain === "Ethereum" },
  { id: "og-1", row: "og", title: "OG single", seriesName: "OG 1", cards: 1, emoji: "🏛️", match: (e) => e.era === OG_ERA },
  { id: "og-2", row: "og", title: "OG duo", seriesName: "OG 2", cards: 2, emoji: "🏛️", match: (e) => e.era === OG_ERA },
  { id: "og-5", row: "og", title: "OG pack", seriesName: "OG 5", cards: 5, emoji: "🏛️", match: (e) => e.era === OG_ERA },
];

export const PACK_ROWS: { id: PackRowId; title: string; lead: string }[] = [
  { id: "families", title: "Meme families", lead: "One family per pack: only dogs, only cats or only frogs." },
  { id: "chains", title: "Chain packs", lead: "Memecoins from a single chain." },
  { id: "og", title: "OG packs", lead: "Only the memecoins of 2013 to 2018, the Doge era. Small packs." },
];

/** Identifiants des cartes du catalogue qui entrent dans un pack (mythiques jamais incluses : absentes du catalogue). */
export function cardsOf(type: PackType, catalog: Record<string, CatalogEntry>): string[] {
  return Object.entries(catalog)
    .filter(([, e]) => type.match(e))
    .map(([id]) => id);
}

const norm = (s: string) => s.toLowerCase().replace(/^(moonpacks|memaster)\s+/, "").trim();

/** Série ouverte qui porte le nom du pack, s'il y en a une. */
export function seriesFor(type: PackType, open: SeriesView[]): SeriesView | undefined {
  return open.find((s) => norm(s.name) === type.seriesName.toLowerCase() && s.cards_per_pack === type.cards);
}

/** Séries ouvertes qui ne sont pas un pack thématique : les lignes Classic et Full Moon. */
export function regularSeries(open: SeriesView[]): SeriesView[] {
  return open.filter((s) => !PACK_TYPES.some((t) => norm(s.name) === t.seriesName.toLowerCase()));
}
