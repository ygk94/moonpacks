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

## Contrat v4 : types de packs (prêt à déployer, 14/11)

Le contrat porte les packs thématiques **dans la même série** : `SeriesTable.kinds` (`docs/mecaniques-spec.md`,
section 13). Mêmes compteurs et mêmes plafonds que le pack de base, donc **aucune réimpression** ni dilution de la
rareté ; chaque type a ses règles (taille, cartes, mythiques, plancher par carte, brûlable garantie ou non). Le site
trouve tout seul un type de pack du même nom et de la même taille (`offerFor`).

Tout est prêt dans le dépôt, il ne reste que le déploiement (clés du compte owner, machine de Hugo) :

- `contract/scripts/build_v4.py` relit sur la chaîne les deux séries de `app3`, vérifie leur hash, et écrit
  `contract/series-v4/classic` et `contract/series-v4/full-moon` (versionnés, sans secret). Mêmes cartes, mêmes
  mythiques (mêmes engagements : les préimages de app3 les révèlent), noms « Moonpacks Classic » et « Moonpacks Full
  Moon », visuels servis par le site ;
- `contract/scripts/deploy_v4.sh` déploie le tout sur `app4` (avec `redeemer4`, `oracle4`) en une commande ;
- le site lit le contrat de la variable de dépôt `CONTRACT_ID` (CI) ; vide, il reste sur `app3`.

```bash
cd contract && ./scripts/deploy_v4.sh
gh variable set CONTRACT_ID --body app4.simpletea5483.testnet
gh workflow run ci.yml --ref main -f deploy=true
```

Les 9 types de la série Classic (`contract/series-v4/classic/manifest.json`) :

| Pack | Cartes | Prix (NEAR) | Cartes possibles | Mythiques | Règles par carte | Valeur (table) |
|---|---:|---:|---:|---|---|---|
| Dog | 8 | 0,088 | 282 | non | aucune ; 1 pack sur 3 avec une brûlable (poids) | non |
| Cat | 5 | 0,066 | 98 | non | 5e : au moins `rare` | non |
| Frog | 3 | 0,040 | 57 | non | 3e : au moins `rare` | non |
| Solana | 5 | 0,083 | 170 | **oui** | 1re : au moins `epic` ; 5e : brûlable | oui |
| BNB Chain | 10 | 0,110 | 214 | non | aucune | non |
| Ethereum | 3 | 0,066 | 122 | non | 1re : au moins `epic` | non |
| OG 1 / OG 2 / OG 5 | 1 / 2 / 5 | 0,011 / 0,022 / 0,055 | 94 | non | aucune | non (collection) |

Prix : 0,011 NEAR par carte comme le Classic (0,0552 les 5), un peu plus quand le pack a un plancher ou une brûlable
garantie. Cat et Ethereum n'ont pas de brûlable sans plafond dans leurs cartes : le contrat refuserait une brûlable
garantie, donc pas de valeur, seulement un plancher. Les prix sont des propositions, faciles à changer dans
`build_v4.py` avant le déploiement (le hash change, rien d'autre).

**Effet du pack Dog sur le Classic.** Les 3 brûlables communes passent à un poids de 4 (au lieu de 1) dans la série
Classic, pour le pack Dog. Dans le pack Classic de base, une commune est donc brûlable 1,1 % du temps au lieu de 0,3 %,
sans changer les cotes par rareté ni la valeur moyenne (validée par `validate_series.py`). Full Moon ne change pas.

## Autre voie : une série par pack (sans contrat v4)

Un pack devient achetable dès qu'une série **ouverte** porte le nom ci-dessous (« Moonpacks » ou « Memaster » devant
est accepté) et le bon nombre de cartes par pack. Rien d'autre à changer dans le site.

| Pack | Nom de la série | Cartes par pack | Cartes de la table (filtre de `front/src/lib/packTypes.ts`) | Cartes publiques |
|---|---|---:|---|---:|
| Dog | `Moonpacks Dog` | **8** | nom ou ticker : dog, shib, inu, bonk, floki, wif, puppy, corgi (hors chats) | 293 |
| Cat | `Moonpacks Cat` | 5 | cat, kitty, kitten, popcat, mew, meow, neko, nyan | 100 |
| Frog | `Moonpacks Frog` | 3 | pepe, frog, toad, ribbit, kek | 59 |
| Solana | `Moonpacks Solana` | 5 | chaîne Solana | 199 |
| BNB Chain | `Moonpacks BNB Chain` | 10 | chaîne BNB Chain | 236 |
| Ethereum | `Moonpacks Ethereum` | 3 | chaîne Ethereum | 133 |
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
