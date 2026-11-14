# Packs de la boutique (13-14/11)

La boutique (`front/src/pages/Shop.tsx`) montre cinq lignes. Les deux premières sont achetables sur `app3`, les trois
autres sont affichées « Coming soon » tant que leurs séries n'existent pas sur le contrat.

## Lignes achetables

| Ligne | Série on-chain | Différence |
|---|---|---|
| **Classic** | `Memaster Entry` (série 0, 0,0552 NEAR) | — |
| **Full Moon** | `Memaster Standard` (série 1, 0,1381 NEAR) | Mêmes cartes et mêmes cotes, la carte brûlable bloque 2,5× plus de jetons |

Chaque ligne propose 5, 10 et 20 cartes. Un pack du contrat fait 5 cartes : 10 et 20 cartes sont 2 et 4 packs achetés
d'un coup (une seule validation si le wallet sait signer un lot, sinon une par pack), ouverts dans une seule animation.
Il n'y a **pas de remise** : le contrat n'a qu'un prix par série. Une remise demanderait des séries à 10 cartes à un prix
par carte plus bas (10 cartes au plus par pack, `MAX_CARDS_PER_PACK`) ; c'est à décider avec Hugo (risque « jeu
d'argent »).

## Lignes « Coming soon » : séries à créer (Hugo, clés du contrat)

Un pack devient achetable dès qu'une série **ouverte** porte le nom ci-dessous (« Moonpacks » ou « Memaster » devant
est accepté) et le bon nombre de cartes par pack. Rien d'autre à changer dans le site.

| Pack | Nom de la série | Cartes par pack | Cartes de la table (filtre de `front/src/lib/packTypes.ts`) | Cartes publiques |
|---|---|---:|---|---:|
| Dog | `Moonpacks Dog` | **8** | nom ou ticker : doge, shib, inu, dog, bonk, floki, wif, puppy, corgi, shiba (hors chats) | 291 |
| Cat | `Moonpacks Cat` | 5 | cat, kitty, kitten, popcat, mew, meow, neko, nyan | 100 |
| Frog | `Moonpacks Frog` | 5 | pepe, frog, toad, ribbit, kek | 59 |
| Solana | `Moonpacks Solana` | 5 | chaîne Solana | 199 |
| BNB Chain | `Moonpacks BNB Chain` | 5 | chaîne BNB Chain | 236 |
| Ethereum | `Moonpacks Ethereum` | 5 | chaîne Ethereum | 133 |
| OG single | `Moonpacks OG 1` | 1 | époque 2013-2018 | 123 |
| OG duo | `Moonpacks OG 2` | 2 | époque 2013-2018 | 123 |
| OG pack | `Moonpacks OG 5` | 5 | époque 2013-2018 | 123 |

### Dog : 8 cartes, une carte brûlable dans 1 pack sur 3 (Enzo, 14/11)

Pas de table de valeur, donc pas de brûlable garantie : les brûlables sont des cartes ordinaires de la table, avec leur
adossement fixe, et leur poids règle la chance d'en tirer une. Pour 1 pack sur 3 avec 8 cartes, il faut environ
**4,9 % de chances par carte** (1 − (2/3)^(1/8)).

Contrainte : la seule brûlable « chien » de `app3`, `dogwifhat-wif`, est légendaire (0,2 % par carte). Elle ne peut pas
donner 1 sur 3 à elle seule. Proposition :

- garder WIF dans la table (légendaire, plafond 50) ;
- ajouter les 3 brûlables communes de `app3` (`black-dragon-blackdragon`, `jambo-meme-cooking-jambo`,
  `nearkat-nearkat`) avec un **poids de 4** chacune, à côté des 209 communes « chien » de poids 1. Elles font alors
  5,4 % des communes, soit 4,9 % par carte, et **33 % des packs** ont au moins une brûlable ;
- ces trois coins ne sont pas des chiens : c'est l'entorse au thème. Autre voie, plus propre, mais à financer : adosser
  des communes « chien » disponibles sur NEAR Intents.

Le site annonce « 1 in 3 packs holds a burnable card » : la table doit le respecter (vérifiable par `get_rates`).

Points à régler en créant ces séries :

- **Brûlables.** Une série avec table de valeur exige une carte brûlable sans plafond par rareté de repli
  (`docs/mecaniques-spec.md`, validation). Les petits packs (OG 1, OG 2) et les familles peu fournies en brûlables
  (Frog) demandent de vérifier qu'il y en a, ou de créer la série sans table de valeur (cartes de collection).
- **Prix.** À fixer par série. Le site affiche le prix lu sur le contrat.
- **Mythiques.** Les filtres portent sur le catalogue public, qui n'a jamais les mythiques. Ajouter ou non les 3
  mythiques scellées à chaque série relève du script de série, pas du site.
- **Les 101 jetons « À décider »** restent exclus de toutes les séries.
