# R5 : audit du catalogue (786 cartes + 77 « À décider ») et relevé CoinGecko

**Date :** 11 novembre 2026. Audit sans modification de `catalogue-final.md`. Ce document n'est pas un conseil en investissement.

## (a) Méthode

- **Relevé.** `GET /api/v3/coins/markets?category=meme-token`, 250 jetons par page, 27 pages, API publique sans clé, User-Agent générique, 15 s au moins entre deux appels, nouvel essai après chaque 429 selon l'en-tête `Retry-After`. **6 636 jetons** dans `docs/data/coingecko-meme-2026-11-11.csv` (script : `docs/recherche-v2/crawl_coingecko.py`). Pic estimé = `market_cap / (1 + ath_change_percentage/100)`, vide si la capitalisation est nulle ou si l'écart vaut 0, est positif ou vaut -100.
- **Rapprochement carte → jeton.** Sur le nom (variantes sans parenthèses, avec le contenu des parenthèses) puis le ticker ; plus grosse capitalisation en cas d'homonymes. 19 rapprochements jugés faux (homonymes) ont été annulés à la main ; les cartes non rapprochées ont été cherchées dans `/coins/list` (22 794 jetons), et 49 jetons trouvés hors de la catégorie mème ont été lus par un appel `/coins/markets?ids=` (données non versées au CSV, qui reste le relevé brut de la catégorie). **741 cartes sur 863 rapprochées.**
- **Mème ou pas.** Retrait des agents IA présentés comme produits, launchpads, L1/L2, protocoles DeFi, jeux Telegram (tap-to-earn), jetons utilitaires et creator coins. Cas douteux vérifiés par recherche web (MEMDEX100, Zerebro, MEMETOON, AI Companions, BurnedFi, The Grays Currency, Finvesta, Lucidum, Ninja Squad, Real World AI, RaveDAO, Luminous, ASSAI, Send, Acolyte, AIFlow, ChatAI, OSK, My Paqman Coin). Les autres jetons de la catégorie mème de CoinGecko sont gardés par défaut.
- **Pic retenu.** Pic sourcé du catalogue s'il existe ; s'il n'est qu'une borne basse (« ≥ », « > »), l'estimation CoinGecko le remplace quand elle est plus haute ; sinon estimation CoinGecko du jour ; sinon capitalisation actuelle comme plancher ; sinon inconnu. Une correction manuelle : Official Trump (14,6 Md$ au lieu des 20,7 Md$ estimés, l'offre ayant grossi).
- **Rareté v2.** Mythique : DOGE, SHIB, PEPE seulement. Puis selon le pic : légendaire ≥ 1 Md$, épique 100 M$ à 1 Md$, rare 10 à 100 M$, commune en dessous ou pic inconnu. Hausse d'un cran pour une histoire légendaire ou marquante (liste dans la colonne Source). Deux garde-fous sur les pics seulement estimés : (1) une estimation ≥ 1 Md$ n'est retenue en légendaire que pour 17 jetons dont le milliard est connu (WIF, BONK, BRETT, FARTCOIN, BOME, DOG, ELON, GOAT, ORDI, SATS, FLOKI, PNUT, BABYDOGE, MEW, NEIRO, MONA, TRUMP), sinon plafond épique ; (2) écart ≤ -99,5 % : estimation jugée fragile (offre gonflée, mèche de lancement), un cran de moins, sans descendre sous un pic sourcé.
- **État v2.** `mort` : capitalisation < 1 M$ et volume 24 h < 20 000 $, ou jeton introuvable sur CoinGecko. `en déclin (-95 % ou pire)`, `en déclin` (-80 à -95 %), `actif` sinon. `à vérifier` : homonyme sur CoinGecko non rapproché.
- **Limites.** L'estimation suppose une offre constante depuis le plus haut : elle surestime les jetons à émission continue et les mèches sur pools minuscules. Rapprochement sans adresse : quelques cartes « estimé » peuvent viser un homonyme. La rareté v2 suit la consigne à la lettre : beaucoup de mèmes morts mais au pic de 10 à 100 M$ sortent `rare`, pas `commune`.

### Résultats

- **Gardées : 797** (726 du tableau Cartes, 71 d'« À décider »). **Retirées : 66**.
- Rareté v2 des cartes gardées : mythique 3, légendaire 24, épique 160, rare 353, commune 257.
- État v2 des cartes gardées : en déclin 358, mort 340, actif 95, à vérifier 4.
- Rapprochements par ticker seul (à contrôler) : 28.

### Doublons et erreurs relevés

- **Pepecoin n° 99 (PEP) et n° 709 (Pepecoin †, « MEME »)** : même chaîne Pepecoin de 2016, aujourd'hui `pepecoin-network` (ticker PEP). Garder une carte. PepeCoin n° 29 (PEPECOIN) est un ERC-20 distinct.
- **Based Tyler n° 558 et Base God n° 185** : même ticker TYBG, même chaîne Base, CoinGecko n'a qu'un jeton (`base-god`).
- **ANSEM n° 141 / The Black Bull n° 105**, **67 n° 270 / n° 290**, **Dacity n° 321 / AudaCity n° 473**, **Broccoli n° 133 / CZ's Dog n° 55** : doublons possibles, à trancher sur adresse.
- **MEMETOON n° 11** : n'est pas Memecoin (Memeland, n° 669) ; c'est une plateforme de BD sur BNB Chain, retirée.
- **GOATED n° 378** : même ticker que GOAT Network retiré en annexe 1 ; CoinGecko donne `goated-2`, à confirmer.
- **Turbo n° 190** : pic du catalogue « > 70 M$ » ; CoinGecko donne ≈ 987 M$ : passe épique.
- **Official Trump D1** : pic de 72 Md$ (Yahoo) faux, ≈ 14,6 Md$ retenu.
- **DJT D41 / TrumpCoin D59** et **RKC D24 / Red Kitten Crew D26** : CoinGecko ne connaît que le second de chaque paire (`trumpcoin`, ticker DJT ; `red-kitten-crew`, ticker RKC) ; doublons probables. **Hawk D16 / Hawk Tuah D7** : deux jetons distincts sur CoinGecko (`hawk-2`, `hawk-tuah`), pas un doublon.
- **ai16z n° 9** : l'ancien jeton (`ai16z`) est mort après la migration vers ELIZAOS (capitalisation ≈ 0,4 M$).
- **Chaînes.** Pas d'erreur de chaîne prouvée sur les cartes sourcées ; 445 cartes restent « à vérifier » côté chaîne : le relevé ne donne pas la chaîne.

## (b) Audit carte par carte

Source : identifiant CoinGecko du relevé (ou « hors catégorie mème »), capitalisation et volume du 11/11/2026, écart au plus haut ; puis remarques.

| N° | Nom | Ticker | Verdict | Motif si retrait | Rareté actuelle | Rareté v2 | État v2 | Pic retenu | Source |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dogecoin | DOGE | garder |  | légendaire | mythique | en déclin | ≈ 88,80 Md$ (sourcé) | CoinGecko `dogecoin` ; catalogue (pic sourcé) ; cap. ≈ 10,69 Md$, volume 24 h ≈ 470 M$, écart -90,7 % |
| 2 | Shiba Inu | SHIB | garder |  | légendaire | mythique | en déclin | ≈ 40,00 Md$ (sourcé) | CoinGecko `shiba-inu` ; catalogue (pic sourcé) ; cap. ≈ 2,63 Md$, volume 24 h ≈ 49 M$, écart -94,8 % |
| 3 | Pepe | PEPE | garder |  | légendaire | mythique | en déclin | ≈ 11,78 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `pepe` ; cap. ≈ 2,29 Md$, volume 24 h ≈ 702 M$, écart -80,5 % |
| 4 | Pump.fun | PUMP | retirer | launchpad (Pump.fun) : jeton de plateforme, pas un mème | légendaire | — | actif | ≈ 5,60 Md$ (sourcé) | CoinGecko `pump-fun` ; catalogue (pic sourcé) ; cap. ≈ 1,63 Md$, volume 24 h ≈ 105 M$, écart -59,7 % |
| 5 | MemeCore | M | retirer | L1 (MemeCore) : chaîne propre, pas un mème | épique | — | en déclin | ≈ 12,96 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `memecore` ; cap. ≈ 1,82 Md$, volume 24 h ≈ 2,2 M$, écart -86,0 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique |
| 6 | Virtuals Protocol | VIRTUAL | retirer | launchpad d'agents IA (Virtuals Protocol) | épique | — | en déclin | ≈ 3,80 Md$ (sourcé) | CoinGecko `virtual-protocol` ; catalogue (pic sourcé) ; cap. ≈ 350 M$, volume 24 h ≈ 28 M$, écart -89,5 % |
| 7 | dogwifhat † | WIF | garder |  | épique | légendaire | en déclin (-95 % ou pire) | ≈ 4,82 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `dogwifcoin` ; cap. ≈ 158 M$, volume 24 h ≈ 26 M$, écart -96,7 % |
| 8 | Notcoin | NOT | retirer | tap-to-earn Telegram (Notcoin) : jeu d'abord, mème ensuite | épique | — | en déclin (-95 % ou pire) | ≈ 2,97 Md$ (sourcé) | CoinGecko `notcoin` ; catalogue (pic sourcé) ; cap. ≈ 33 M$, volume 24 h ≈ 3,9 M$, écart -98,8 % |
| 9 | ai16z (ElizaOS) | AI16Z | retirer | agent IA / cadriciel ElizaOS (ai16z) ; parodie de a16z mais devenu jeton d'infrastructure | épique | — | mort | ≈ 2,70 Md$ (sourcé) | CoinGecko `ai16z` ; catalogue (pic sourcé) ; cap. ≈ 358 k$, volume 24 h ≈ 6 k$, écart -100,0 % |
| 10 | Bonk | BONK | garder |  | épique | légendaire | en déclin (-95 % ou pire) | ≈ 5,13 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `bonk` ; cap. ≈ 249 M$, volume 24 h ≈ 24 M$, écart -95,1 % |
| 11 | MEMETOON | MEME | retirer | jeton utilitaire d'une plateforme de BD (MEMETOON, BNB Chain) ; pic estimé aberrant | épique* | — | en déclin (-95 % ou pire) | ≈ 2,21 Md$ (estimé CG) | CoinGecko `memetoon` ; cap. ≈ 52 M$, volume 24 h ≈ 0 k$, écart -97,7 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; pas Memecoin de Memeland (n° 669), malgré le ticker MEME |
| 12 | Pudgy Penguins | PENGU | garder |  | épique | légendaire | en déclin | ≈ 2,30 Md$ (sourcé) | CoinGecko `pudgy-penguins` ; catalogue (pic sourcé) ; cap. ≈ 392 M$, volume 24 h ≈ 64 M$, écart -90,9 % — marque NFT, mais jeton sans utilité, traité en mème |
| 13 | Brett † | BRETT | garder |  | épique | légendaire | en déclin (-95 % ou pire) | ≈ 2,32 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `based-brett` ; cap. ≈ 37 M$, volume 24 h ≈ 2,5 M$, écart -98,4 % |
| 15 | SPX6900 | SPX | garder |  | épique | légendaire | en déclin | ≈ 2,00 Md$ (sourcé) | CoinGecko `spx6900` ; catalogue (pic sourcé) ; cap. ≈ 340 M$, volume 24 h ≈ 7,5 M$, écart -83,9 % |
| 16 | Popcat † | POPCAT | garder |  | épique | légendaire | en déclin (-95 % ou pire) | ≈ 1,70 Md$ (sourcé) | CoinGecko `popcat` ; catalogue (pic sourcé) ; cap. ≈ 34 M$, volume 24 h ≈ 4,0 M$, écart -98,3 % |
| 17 | Fartcoin | FARTCOIN | garder |  | épique | légendaire | en déclin (-95 % ou pire) | ≈ 2,48 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `fartcoin` ; cap. ≈ 115 M$, volume 24 h ≈ 12 M$, écart -95,3 % |
| 18 | Ape and Pepe | APEPE | garder |  | épique* | épique | en déclin | ≈ 1,45 Md$ (estimé CG) | CoinGecko `ape-and-pepe` ; cap. ≈ 262 M$, volume 24 h ≈ 16 M$, écart -81,9 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique |
| 19 | OSK | OSK | garder |  | épique* | épique | en déclin (-95 % ou pire) | ≈ 1,05 Md$ (estimé CG) | CoinGecko `osk` ; cap. ≈ 14 M$, volume 24 h ≈ 0 k$, écart -98,7 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique |
| 20 | Animecoin | ANIME | retirer | jeton d'écosystème Azuki / Animechain (Animecoin), pas un mème | épique* | — | en déclin (-95 % ou pire) | ≈ 1,03 Md$ (estimé CG) | CoinGecko `anime` ; cap. ≈ 13 M$, volume 24 h ≈ 3,1 M$, écart -98,7 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique |
| 21 | Book of Meme | BOME | garder |  | épique | légendaire | en déclin (-95 % ou pire) | ≈ 1,50 Md$ (sourcé) | CoinGecko `book-of-meme` ; catalogue (pic sourcé) ; cap. ≈ 42 M$, volume 24 h ≈ 7,1 M$, écart -97,7 % |
| 22 | DOG•GO•TO•THE•MOON | DOG | garder |  | épique | légendaire | en déclin | ≈ 1,13 Md$ (sourcé) | CoinGecko `dog-go-to-the-moon-rune` ; catalogue (pic sourcé) ; cap. ≈ 75 M$, volume 24 h ≈ 458 k$, écart -92,4 % |
| 23 | Loaded Lions | LION | garder |  | épique* | épique | en déclin (-95 % ou pire) | ≈ 971 M$ (estimé CG) | CoinGecko `loaded-lions` ; cap. ≈ 32 M$, volume 24 h ≈ 37 k$, écart -96,7 % |
| 24 | Big Dog Fink | BINK | garder |  | épique* | épique | en déclin (-95 % ou pire) | ≈ 769 M$ (estimé CG) | CoinGecko `big-dog-fink` ; cap. ≈ 9,8 M$, volume 24 h ≈ 0 k$, écart -98,7 % |
| 25 | Dogelon Mars | ELON | garder |  | épique | légendaire | en déclin (-95 % ou pire) | ≈ 1,00 Md$ (sourcé) | CoinGecko `dogelon-mars` ; catalogue (pic sourcé) ; cap. ≈ 22 M$, volume 24 h ≈ 1,3 M$, écart -99,2 % |
| 26 | Goatseus Maximus | GOAT | garder |  | épique | légendaire | en déclin (-95 % ou pire) | ≈ 1,35 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `goatseus-maximus` ; cap. ≈ 13 M$, volume 24 h ≈ 992 k$, écart -99,1 % — premier mème né d'une IA (Truth Terminal) : mème d'abord |
| 27 | Ordinals | ORDI | garder |  | épique | légendaire | en déclin (-95 % ou pire) | ≈ 2,01 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `ordinals` ; cap. ≈ 67 M$, volume 24 h ≈ 7,7 M$, écart -96,7 % — premier BRC-20, expérimental, aucune utilité : mème assumé; rapprochement CoinGecko par ticker seul |
| 28 | Sats | SATS (1000SATS) | garder |  | épique | légendaire | en déclin (-95 % ou pire) | ≈ 1,94 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `sats-ordinals` ; cap. ≈ 18 M$, volume 24 h ≈ 941 k$, écart -99,1 % — BRC-20 sans utilité |
| 29 | PepeCoin | PEPECOIN | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 761 M$ (estimé CG) | CoinGecko `pepecoin-2` ; cap. ≈ 10 M$, volume 24 h ≈ 117 k$, écart -98,7 % — ERC-20 de 2023, distinct de la chaîne Pepecoin (n° 99 / 709) |
| 30 | My Paqman Coin | MPC | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 920 M$ (estimé CG) | CoinGecko `my-paqman-coin` ; cap. ≈ 18 M$, volume 24 h ≈ 0 k$, écart -98,0 % |
| 31 | Pippin † | PIPPIN | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 895 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `pippin` ; cap. ≈ 12 M$, volume 24 h ≈ 695 k$, écart -98,6 % — agent IA mais mème assumé (licorne SVG), lancé pump.fun |
| 32 | Floki | FLOKI | garder |  | rare | légendaire | en déclin | ≈ 3,32 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `floki` ; cap. ≈ 202 M$, volume 24 h ≈ 13 M$, écart -93,9 % |
| 33 | CorgiAI | CORGIAI | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 1,53 Md$ (estimé CG) | CoinGecko `corgiai` ; cap. ≈ 8,5 M$, volume 24 h ≈ 4 k$, écart -99,4 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique |
| 34 | GEKKO | GEKKO | garder |  | rare* | épique | en déclin | ≈ 822 M$ (estimé CG) | CoinGecko `gekko` ; cap. ≈ 46 M$, volume 24 h ≈ 91 k$, écart -94,4 % |
| 35 | Zerebro | ZEREBRO | retirer | agent IA (Zerebro, cadriciel ZerePy) ; lancé sur pump.fun mais positionné agent | rare | — | en déclin (-95 % ou pire) | ≈ 783 M$ (sourcé) | CoinGecko `zerebro` ; catalogue (pic sourcé) ; cap. ≈ 24 M$, volume 24 h ≈ 5,0 M$, écart -97,0 % |
| 36 | aixbt by Virtuals | AIXBT | retirer | agent IA d'analyse (aixbt by Virtuals) | rare | — | en déclin (-95 % ou pire) | ≈ 778 M$ (sourcé) | CoinGecko `aixbt` ; catalogue (pic sourcé) ; cap. ≈ 15 M$, volume 24 h ≈ 1,5 M$, écart -98,4 % — rapprochement CoinGecko par ticker seul |
| 37 | BUILDon | B | garder |  | rare | épique | en déclin | ≈ 763 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `build-on` ; cap. ≈ 117 M$, volume 24 h ≈ 3,1 M$, écart -84,7 % |
| 38 | Hamster Kombat | HMSTR | retirer | tap-to-earn Telegram (Hamster Kombat) | rare | — | en déclin (-95 % ou pire) | ≈ 646 M$ (sourcé) | CoinGecko `hamster-kombat` ; catalogue (pic sourcé) ; cap. ≈ 8,3 M$, volume 24 h ≈ 2,5 M$, écart -98,2 % |
| 39 | AI Companions | AIC | retirer | application de compagnons IA (AI Companions), jeton utilitaire | rare* | — | en déclin (-95 % ou pire) | ≈ 581 M$ (estimé CG) | CoinGecko `ai-companions` ; cap. ≈ 12 M$, volume 24 h ≈ 98 k$, écart -97,9 % |
| 40 | Slerf | SLERF | garder |  | rare | épique | en déclin | ≈ 612 M$ (sourcé) | CoinGecko `slerf-2` ; catalogue (pic sourcé) ; cap. ≈ 1,7 M$, volume 24 h ≈ 3 k$, écart -91,6 % |
| 42 | Peanut the Squirrel | PNUT | garder |  | rare | légendaire | en déclin (-95 % ou pire) | ≈ 2,44 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `peanut-the-squirrel` ; cap. ≈ 33 M$, volume 24 h ≈ 5,3 M$, écart -98,6 % |
| 43 | Rekt | REKT | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 594 M$ (estimé CG) | CoinGecko `rekt-4` ; cap. ≈ 23 M$, volume 24 h ≈ 59 k$, écart -96,1 % |
| 44 | PondCoin | PNDC | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 415 M$ (estimé CG) | CoinGecko `pond-coin` ; cap. ≈ 6,2 M$, volume 24 h ≈ 7 k$, écart -98,5 % |
| 45 | Griffain | GRIFFAIN | retirer | plateforme d'agents IA (Griffain) | rare | — | en déclin (-95 % ou pire) | ≈ 625 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `griffain` ; cap. ≈ 10 M$, volume 24 h ≈ 2,8 M$, écart -98,4 % |
| 46 | The Grays Currency | PTGC | retirer | DAO de rachat et brûlage de LP sur PulseChain (The Grays Currency), DeFi | rare* | — | en déclin (-95 % ou pire) | ≈ 380 M$ (estimé CG) | CoinGecko `the-grays-currency` ; cap. ≈ 5,4 M$, volume 24 h ≈ 3 k$, écart -98,6 % |
| 47 | would | WOULD | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 701 M$ (estimé CG) | CoinGecko `would` ; cap. ≈ 11 M$, volume 24 h ≈ 1 k$, écart -98,5 % |
| 48 | Binance Life (币安人生) | 币安人生 | garder |  | rare | épique | actif | ≈ 524 M$ (sourcé) | CoinGecko `bianrensheng` ; catalogue (pic sourcé) ; cap. ≈ 493 M$, volume 24 h ≈ 3,2 M$, écart -44,9 % — rapprochement CoinGecko par ticker seul |
| 49 | BurnedFi | BURN | retirer | protocole DeFi de brûlage avec jeton BUILD (BurnedFi) | rare* | — | en déclin (-95 % ou pire) | ≈ 554 M$ (estimé CG) | CoinGecko `burnedfi` ; cap. ≈ 15 M$, volume 24 h ≈ 56 k$, écart -97,3 % |
| 50 | Test | TST | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 500 M$ (sourcé) | CoinGecko `test-3` ; catalogue (pic sourcé) ; cap. ≈ 11 M$, volume 24 h ≈ 9,8 M$, écart -97,6 % |
| 51 | Degen † | DEGEN | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 2,32 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `degen-base` ; cap. ≈ 29 M$, volume 24 h ≈ 7,0 M$, écart -98,7 % — né comme mème de la chaîne /degen de Farcaster; estimé ≥ 1 Md$ non confirmé : plafonné à épique |
| 52 | PepeFork | PORK | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 387 M$ (estimé CG) | CoinGecko `pepefork` ; cap. ≈ 4,7 M$, volume 24 h ≈ 11 k$, écart -98,8 % |
| 53 | Artificial Inu | AI | garder |  | rare* | épique | en déclin | ≈ 382 M$ (estimé CG) | CoinGecko `artificial-inu-3` ; cap. ≈ 29 M$, volume 24 h ≈ 3,1 M$, écart -92,3 % |
| 54 | ANDY ETH | ANDY | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 352 M$ (estimé CG) | CoinGecko `andy-the-wisguy` ; cap. ≈ 12 M$, volume 24 h ≈ 96 k$, écart -96,7 % |
| 55 | CZ's Dog | BROCCOLI (BROCCOLI714) | garder |  | rare | épique | en déclin | ≈ 400 M$ (sourcé) | CoinGecko `czs-dog` ; catalogue (pic sourcé) ; cap. ≈ 16 M$, volume 24 h ≈ 3,4 M$, écart -93,5 % — plusieurs Broccoli : voir n° 133 |
| 56 | Mog Coin | MOG | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 400 M$ (sourcé) | CoinGecko `mog-coin` ; catalogue (pic sourcé) ; cap. ≈ 35 M$, volume 24 h ≈ 3,9 M$, écart -97,7 % |
| 57 | ConstitutionDAO | PEOPLE | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 937 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `constitutiondao` ; cap. ≈ 29 M$, volume 24 h ≈ 5,5 M$, écart -96,9 % — crowdfunding raté devenu mème, aucune utilité |
| 58 | Kekius Maximus | KEKIUS | garder |  | rare | épique | actif | ≈ 380 M$ (sourcé) | CoinGecko `kekius-maximus-6` ; catalogue (pic sourcé) ; cap. ≈ 12 M$, volume 24 h ≈ 1 k$, écart -77,7 % |
| 59 | Freysa | FAI | retirer | jeu / agent IA (Freysa) | rare | — | en déclin (-95 % ou pire) | ≈ 500 M$ (sourcé) | CoinGecko `freysa-ai` ; catalogue (pic sourcé) ; cap. ≈ 15 M$, volume 24 h ≈ 95 k$, écart -97,7 % |
| 60 | Milady Cult Coin | CULT | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 362 M$ (estimé CG) | CoinGecko `milady-cult-coin` ; cap. ≈ 7,0 M$, volume 24 h ≈ 144 k$, écart -98,1 % |
| 61 | coco | COCO | garder |  | rare* | épique | actif | ≈ 355 M$ (estimé CG) | CoinGecko `coco-2` ; cap. ≈ 140 M$, volume 24 h ≈ 42 k$, écart -60,5 % |
| 62 | DogeKing | DOGEKING | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 333 M$ (estimé CG) | CoinGecko `dogeking` ; cap. ≈ 3,2 M$, volume 24 h ≈ 40 k$, écart -99,0 % |
| 63 | GAME by Virtuals | GAME | retirer | cadriciel d'agents IA (GAME by Virtuals) | rare | — | en déclin (-95 % ou pire) | ≈ 392 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `game-by-virtuals` ; cap. ≈ 3,2 M$, volume 24 h ≈ 25 k$, écart -99,2 % |
| 64 | Sundog | SUNDOG | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 316 M$ (sourcé) | CoinGecko `sundog` ; catalogue (pic sourcé) ; cap. ≈ 781 k$, volume 24 h ≈ 40 k$, écart -99,8 % |
| 65 | Ava AI | AVA | retirer | agent IA (Ava AI, Holoworld) | rare* | — | en déclin (-95 % ou pire) | ≈ 332 M$ (estimé CG) | CoinGecko `ava-ai` ; cap. ≈ 6,0 M$, volume 24 h ≈ 2,0 M$, écart -98,2 % |
| 66 | Baby Doge Coin | BABYDOGE | garder |  | rare | légendaire | en déclin (-95 % ou pire) | ≈ 1,20 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `baby-doge-coin` ; cap. ≈ 54 M$, volume 24 h ≈ 1,3 M$, écart -95,5 % |
| 67 | Cash Cat | CASHCAT | garder |  | rare* | épique | en déclin | ≈ 310 M$ (estimé CG) | CoinGecko `cash-cat` ; cap. ≈ 60 M$, volume 24 h ≈ 11 M$, écart -80,6 % |
| 68 | TDCCP | TDCCP | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 282 M$ (estimé CG) | CoinGecko `tdccp` ; cap. ≈ 12 M$, volume 24 h ≈ 15 k$, écart -95,6 % |
| 69 | Arc | ARC | retirer | cadriciel d'agents IA Rig (Arc) | rare | — | en déclin | ≈ 623 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `ai-rig-complex` ; cap. ≈ 33 M$, volume 24 h ≈ 1,9 M$, écart -94,7 % |
| 70 | 龙虾 (Lobster) | 龙虾 | garder |  | rare* | épique | en déclin | ≈ 309 M$ (estimé CG) | CoinGecko `lobster-2` ; cap. ≈ 18 M$, volume 24 h ≈ 1,1 M$, écart -94,2 % |
| 71 | SNAP | $NAP | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 245 M$ (estimé CG) | CoinGecko `snap-kero` ; cap. ≈ 2,8 M$, volume 24 h ≈ 0 k$, écart -98,9 % |
| 72 | MORI COIN | MORI | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 200 M$ (estimé CG) | CoinGecko `mori-coin` ; cap. ≈ 2,6 M$, volume 24 h ≈ 90 k$, écart -98,7 % |
| 73 | Nacho the Kat | NACHO | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 216 M$ (estimé CG) | CoinGecko `nacho-the-kat` ; cap. ≈ 2,3 M$, volume 24 h ≈ 2 k$, écart -98,9 % |
| 74 | Toshi † | TOSHI | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 950 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `toshi` ; cap. ≈ 38 M$, volume 24 h ≈ 2,2 M$, écart -96,0 % |
| 75 | Cheems | CHEEMS | garder |  | rare | épique | mort | ≈ 250 M$ (sourcé) | CoinGecko `cheems` ; catalogue (pic sourcé) ; cap. ≈ 207 k$, volume 24 h ≈ 0 k$, écart -99,2 % |
| 76 | Jelly-My-Jelly | JELLYJELLY | garder |  | rare | épique | en déclin | ≈ 250 M$ (sourcé) | CoinGecko `jelly-my-jelly` ; catalogue (pic sourcé) ; cap. ≈ 40 M$, volume 24 h ≈ 2,4 M$, écart -91,6 % — jeton d'une appli vidéo mais présenté comme mème |
| 77 | Landwolf | WOLF | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 250 M$ (sourcé) | CoinGecko `landwolf-0x67` ; catalogue (pic sourcé) ; cap. ≈ 8,3 M$, volume 24 h ≈ 315 k$, écart -96,8 % |
| 78 | Useless Coin | USELESS | garder |  | rare | épique | actif | ≈ 435 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `useless-3` ; cap. ≈ 139 M$, volume 24 h ≈ 12 M$, écart -68,1 % |
| 79 | cat in a dogs world † | MEW | garder |  | rare | légendaire | en déclin (-95 % ou pire) | ≈ 1,15 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `cat-in-a-dogs-world` ; cap. ≈ 31 M$, volume 24 h ≈ 2,3 M$, écart -97,3 % |
| 80 | 4 | 4 / FOUR | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 243 M$ (sourcé) | CoinGecko `4-2` ; catalogue (pic sourcé) ; cap. ≈ 9,1 M$, volume 24 h ≈ 768 k$, écart -96,9 % |
| 81 | DogeBonk | DOBO | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 224 M$ (estimé CG) | CoinGecko `dogebonk` ; cap. ≈ 2,4 M$, volume 24 h ≈ 0 k$, écart -98,9 % |
| 82 | Launch Coin on Believe (ex-PASTERNAK) | LAUNCHCOIN | retirer | jeton du launchpad Believe (ex-PASTERNAK) : renommé en jeton de plateforme | rare | — | mort (absent de CoinGecko) | ≈ 354 M$ (sourcé) | catalogue (pic sourcé) |
| 83 | Mother Iggy | MOTHER | garder |  | rare | épique | mort | ≈ 240 M$ (sourcé) | CoinGecko `mother-iggy` ; catalogue (pic sourcé) ; cap. ≈ 227 k$, volume 24 h ≈ 0 k$, écart -99,9 % |
| 84 | Wiki Cat | WKC | garder |  | rare* | épique | en déclin | ≈ 248 M$ (estimé CG) | CoinGecko `wiki-cat` ; cap. ≈ 27 M$, volume 24 h ≈ 152 k$, écart -89,1 % |
| 85 | Stonks | STNK | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 215 M$ (estimé CG) | CoinGecko `stonks-4` ; cap. ≈ 2,3 M$, volume 24 h ≈ 7 k$, écart -99,0 % |
| 86 | Vine Coin | VINE | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 240 M$ (sourcé) | CoinGecko `vine` ; catalogue (pic sourcé) ; cap. ≈ 5,7 M$, volume 24 h ≈ 4,9 M$, écart -98,8 % — rapprochement CoinGecko par ticker seul |
| 87 | AMATERASU OMIKAMI | OMIKAMI | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 274 M$ (estimé CG) | CoinGecko `amaterasu-omikami` ; cap. ≈ 4,4 M$, volume 24 h ≈ 8 k$, écart -98,4 % |
| 88 | Sudeng | HIPPO | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 216 M$ (sourcé) | CoinGecko `sudeng` ; catalogue (pic sourcé) ; cap. ≈ 793 k$, volume 24 h ≈ 1,9 M$, écart -99,7 % |
| 89 | RSIC•GENESIS•RUNE | RSIC | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 406 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `runecoin` ; cap. ≈ 2,6 M$, volume 24 h ≈ 0 k$, écart -99,4 % |
| 90 | UNCOMMON•GOODS | UNCOMMONGOODS | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 333 M$ (estimé CG) | CoinGecko `uncommon-goods` ; cap. ≈ 2,1 M$, volume 24 h ≈ 0 k$, écart -99,4 % |
| 91 | BasedHype | BASEDHYPE | garder |  | rare* | épique | en déclin | ≈ 200 M$ (estimé CG) | CoinGecko `basedhype` ; cap. ≈ 34 M$, volume 24 h ≈ 0 k$, écart -82,9 % |
| 92 | Fartboy | $FARTBOY | garder |  | rare* | épique | en déclin | ≈ 194 M$ (estimé CG) | CoinGecko `fartboy` ; cap. ≈ 18 M$, volume 24 h ≈ 118 k$, écart -90,7 % |
| 93 | McDull (Meme) | MCDULL | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 206 M$ (estimé CG) | CoinGecko `mcdull` ; cap. ≈ 5,9 M$, volume 24 h ≈ 0 k$, écart -97,1 % |
| 94 | Pepe Unchained | PEPU | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 200 M$ (sourcé) | CoinGecko `pepe-unchained-2` ; catalogue (pic sourcé) ; cap. ≈ 363 k$, volume 24 h ≈ 31 k$, écart -97,3 % — prévente mème ; la chaîne L2 est secondaire |
| 95 | Milady Meme Coin | LADYS | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 380 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `milady-meme-coin` ; cap. ≈ 4,3 M$, volume 24 h ≈ 138 k$, écart -98,9 % |
| 96 | Asteroid Shiba | ASTEROID | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 202 M$ (estimé CG) | CoinGecko `asteroid-shiba` ; cap. ≈ 3,7 M$, volume 24 h ≈ 98 k$, écart -98,2 % |
| 97 | BULLA | BULLA | garder |  | rare* | épique | en déclin | ≈ 195 M$ (estimé CG) | CoinGecko `bulla-3` ; cap. ≈ 26 M$, volume 24 h ≈ 674 k$, écart -86,9 % |
| 98 | MarsMi | MARSMI | garder |  | rare* | épique | en déclin | ≈ 188 M$ (estimé CG) | CoinGecko `marsmi` ; cap. ≈ 11 M$, volume 24 h ≈ 353 k$, écart -94,1 % |
| 99 | Pepecoin | PEP | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 187 M$ (estimé CG) | CoinGecko `pepecoin-network` ; cap. ≈ 7,5 M$, volume 24 h ≈ 90 k$, écart -96,0 % — doublon de n° 709 : Pepecoin (PEP, CoinGecko `pepecoin-network`) est la chaîne Pepecoin de 2016 relancée |
| 100 | Coq Inu † | COQ | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 447 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `coq-inu` ; cap. ≈ 6,3 M$, volume 24 h ≈ 1,9 M$, écart -98,6 % |
| 101 | ElonXCat | EXC | garder |  | rare* | épique | en déclin | ≈ 176 M$ (estimé CG) | CoinGecko `elonxcat` ; cap. ≈ 11 M$, volume 24 h ≈ 0 k$, écart -93,7 % |
| 102 | Kendu | KENDU | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 270 M$ (estimé CG) | CoinGecko `kendu-inu` ; cap. ≈ 1,8 M$, volume 24 h ≈ 1 k$, écart -99,3 % |
| 103 | Onyx Arches | OXA | garder |  | rare* | rare | en déclin (-95 % ou pire) | ≈ 470 M$ (estimé CG) | CoinGecko `onyx-arches` ; cap. ≈ 1,8 M$, volume 24 h ≈ 0 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 104 | RyuJin | RYU | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 140 M$ (estimé CG) | CoinGecko `ryujin` ; cap. ≈ 1,8 M$, volume 24 h ≈ 5 k$, écart -98,7 % |
| 105 | The Black Bull | ANSEM | garder |  | rare* | épique | en déclin | ≈ 186 M$ (estimé CG) | CoinGecko `the-black-bull` ; cap. ≈ 22 M$, volume 24 h ≈ 2,7 M$, écart -88,0 % — doublon possible de n° 141 ANSEM (même ticker) |
| 107 | Anonymous Cat | ZCAT | garder |  | rare* | épique | en déclin | ≈ 170 M$ (estimé CG) | CoinGecko `anonymous-cat` ; cap. ≈ 22 M$, volume 24 h ≈ 2,3 M$, écart -87,1 % |
| 108 | CrazyBunny | CRAZYBUNNY | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 332 M$ (estimé CG) | CoinGecko `crazybunny` ; cap. ≈ 1,7 M$, volume 24 h ≈ 0 k$, écart -99,5 % |
| 109 | Penguin (à ne pas confondre avec Pudgy Penguins) | PENGUIN | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 170 M$ (sourcé) | CoinGecko `nietzschean-penguin` ; catalogue (pic sourcé) ; cap. ≈ 373 k$, volume 24 h ≈ 85 k$, écart -99,8 % |
| 110 | Trollface | TROLL | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 186 M$ (sourcé) | CoinGecko `troll-face` ; catalogue (pic sourcé) ; cap. ≈ 1,5 M$, volume 24 h ≈ 0 k$, écart -99,3 % |
| 111 | Billy (Bitcoin) | BILLY | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 154 M$ (estimé CG) | CoinGecko `billion-dollar-cat-runes` ; cap. ≈ 1,3 M$, volume 24 h ≈ 7 k$, écart -99,1 % — Billy (Bitcoin) : à distinguer de Billy (Solana, n° 563) |
| 112 | Grok | GROK | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 160 M$ (sourcé) | CoinGecko `grok-2` ; catalogue (pic sourcé) ; cap. ≈ 2,2 M$, volume 24 h ≈ 117 k$, écart -98,8 % |
| 113 | 牛来 (Niu Lai) | 牛来 | garder |  | rare* | épique | actif | ≈ 162 M$ (estimé CG) | CoinGecko `niu-lai` ; cap. ≈ 58 M$, volume 24 h ≈ 7,5 M$, écart -64,5 % |
| 114 | BILLION•DOLLAR•CAT | BDC | garder |  | rare | épique | mort (absent de CoinGecko) | ≈ 150 M$ (sourcé) | catalogue (pic sourcé) |
| 115 | GME (Ethereum) | GME | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 170 M$ (estimé CG) | CoinGecko `game-stop` ; cap. ≈ 3,1 M$, volume 24 h ≈ 18 k$, écart -98,2 % |
| 116 | Refund | RFD | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 105 M$ (estimé CG) | CoinGecko `refund` ; cap. ≈ 1,5 M$, volume 24 h ≈ 0 k$, écart -98,5 % |
| 117 | Ribbita | TIBBIR | retirer | agent IA sur Virtuals (Ribbita by Virtuals) | rare | — | actif | ≈ 147 M$ (sourcé) | CoinGecko `ribbita-by-virtuals` ; catalogue (pic sourcé) — rapprochement CoinGecko par ticker seul |
| 118 | Alchemist AI | ALCH | retirer | plateforme IA sans code (Alchemist AI) | rare | — | en déclin | ≈ 243 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `alchemist-ai` ; cap. ≈ 33 M$, volume 24 h ≈ 1,2 M$, écart -86,5 % |
| 119 | GOHOME | GOHOME | garder |  | rare* | épique | actif | ≈ 146 M$ (estimé CG) | CoinGecko `gohome` ; cap. ≈ 39 M$, volume 24 h ≈ 220 k$, écart -73,2 % |
| 120 | Moonbirds | BIRB | garder |  | rare* | épique | en déclin | ≈ 136 M$ (estimé CG) | CoinGecko `moonbirds` ; cap. ≈ 23 M$, volume 24 h ≈ 6,5 M$, écart -83,3 % — marque NFT, jeton sans utilité, comme PENGU |
| 121 | TEDDY BEAR | BEAR | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 128 M$ (estimé CG) | CoinGecko `teddy-bear` ; cap. ≈ 2,7 M$, volume 24 h ≈ 16 k$, écart -97,9 % |
| 122 | Catizen | CATI | retirer | jeu Telegram (Catizen) | rare | — | en déclin (-95 % ou pire) | ≈ 740 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `catizen` ; cap. ≈ 26 M$, volume 24 h ≈ 1,3 M$, écart -96,6 % |
| 123 | 4Chan | 4CHAN | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 145 M$ (estimé CG) | CoinGecko `4chan` ; cap. ≈ 1,3 M$, volume 24 h ≈ 0 k$, écart -99,1 % |
| 124 | A Meme Coin | AMC | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 151 M$ (estimé CG) | CoinGecko `a-meme-coin` ; cap. ≈ 3,8 M$, volume 24 h ≈ 1,1 M$, écart -97,5 % |
| 125 | Bellscoin | BELLS | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 228 M$ (estimé CG) | CoinGecko `bellscoin` ; cap. ≈ 1,3 M$, volume 24 h ≈ 77 k$, écart -99,4 % |
| 126 | EGL1 | EGL1 | garder |  | rare* | épique | en déclin | ≈ 117 M$ (estimé CG) | CoinGecko `egl1` ; cap. ≈ 10 M$, volume 24 h ≈ 1,5 M$, écart -91,3 % |
| 127 | FEED EVERY GORILLA | FEG | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 134 M$ (estimé CG) | CoinGecko `feg-token-2` ; cap. ≈ 2,6 M$, volume 24 h ≈ 207 k$, écart -98,0 % |
| 128 | Gork | GORK | garder |  | rare | épique | mort | ≈ 130 M$ (sourcé) | CoinGecko `gork-2` ; catalogue (pic sourcé) ; cap. ≈ 20 k$, volume 24 h ≈ 0 k$, écart -99,2 % |
| 129 | Shrub | SHRUB | garder |  | rare* | rare | en déclin (-95 % ou pire) | ≈ 243 M$ (estimé CG) | CoinGecko `shrub` ; cap. ≈ 1,2 M$, volume 24 h ≈ 28 k$, écart -99,5 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 130 | Fred the Convicted Raccoon | FRED | garder |  | rare | épique | mort | ≈ 129 M$ (sourcé) | CoinGecko `first-convicted-raccoon` ; catalogue (pic sourcé) ; cap. ≈ 13 k$, volume 24 h ≈ 0 k$, écart -99,4 % |
| 131 | BankrCoin | BNKR | retirer | agent IA de trading / launchpad (BankrCoin) | rare | — | actif | ≈ 120 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `bankercoin-2` ; cap. ≈ 26 M$, volume 24 h ≈ 1,6 M$, écart -78,5 % |
| 132 | Bitcoin Bull | BTCBULL | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 115 M$ (estimé CG) | CoinGecko `bitcoin-bull-2` ; cap. ≈ 2,3 M$, volume 24 h ≈ 1 k$, écart -98,0 % |
| 133 | Broccoli | BROCCOLI | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 111 M$ (estimé CG) | CoinGecko `broccoli-3` ; cap. ≈ 4,8 M$, volume 24 h ≈ 2,0 M$, écart -95,7 % — doublon possible de n° 55 CZ's Dog (Broccoli) |
| 134 | GME (Solana) | GME | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 220 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `gme` ; cap. ≈ 2,3 M$, volume 24 h ≈ 451 k$, écart -99,0 % |
| 135 | Koma Inu | KOMA | garder |  | rare* | épique | en déclin | ≈ 117 M$ (estimé CG) | CoinGecko `koma-inu` ; cap. ≈ 7,9 M$, volume 24 h ≈ 1,6 M$, écart -93,2 % |
| 136 | Marscoin | MARSCOIN | garder |  | rare | épique | en déclin | ≈ 120 M$ (sourcé) | CoinGecko `marscoin-4` ; catalogue (pic sourcé) ; cap. ≈ 42 M$, volume 24 h ≈ 5,3 M$, écart -84,2 % |
| 137 | MEME HORSE | MHORSE | garder |  | rare* | épique | actif | ≈ 121 M$ (estimé CG) | CoinGecko `meme-horse` ; cap. ≈ 49 M$, volume 24 h ≈ 775 k$, écart -59,1 % |
| 138 | PooCoin | POOCOIN | garder |  | rare* | rare | en déclin (-95 % ou pire) | ≈ 89 M$ (estimé CG) | CoinGecko `poocoin` ; cap. ≈ 1,2 M$, volume 24 h ≈ 0 k$, écart -98,6 % |
| 139 | PURPLE PEPE | PURPE | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 133 M$ (estimé CG) | CoinGecko `purple-pepe` ; cap. ≈ 3,5 M$, volume 24 h ≈ 59 k$, écart -97,4 % |
| 140 | XRP ARMY | ARMY | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 112 M$ (estimé CG) | CoinGecko `army-3` ; cap. ≈ 3,4 M$, volume 24 h ≈ 12 k$, écart -97,0 % |
| 141 | ANSEM | ANSEM | garder |  | rare | épique | mort (absent de CoinGecko) | ≈ 112 M$ (sourcé) | catalogue (pic sourcé) — doublon possible de n° 105 The Black Bull (ANSEM) |
| 142 | Housecoin | HOUSE | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 120 M$ (sourcé) | CoinGecko `housecoin-2` ; catalogue (pic sourcé) ; cap. ≈ 576 k$, volume 24 h ≈ 67 k$, écart -99,5 % |
| 143 | Goose Token | GOOSE | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 133 M$ (estimé CG) | CoinGecko `goose-token` ; cap. ≈ 3,4 M$, volume 24 h ≈ 0 k$, écart -97,4 % |
| 144 | Jeff | JEFF | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 130 M$ (estimé CG) | CoinGecko `jeff-3` ; cap. ≈ 2,2 M$, volume 24 h ≈ 2 k$, écart -98,3 % |
| 145 | Monkey Pox | POX | garder |  | rare* | rare | en déclin (-95 % ou pire) | ≈ 99 M$ (estimé CG) | CoinGecko `monkey-pox` ; cap. ≈ 1,1 M$, volume 24 h ≈ 0 k$, écart -98,9 % |
| 146 | Pikaboss | PIKA | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 113 M$ (estimé CG) | CoinGecko `pikaboss` ; cap. ≈ 5,5 M$, volume 24 h ≈ 2 k$, écart -95,1 % |
| 147 | DogBull | DOGO | garder |  | rare* | rare | en déclin (-95 % ou pire) | ≈ 93 M$ (estimé CG) | CoinGecko `dogbull` ; cap. ≈ 3,0 M$, volume 24 h ≈ 0 k$, écart -96,7 % |
| 148 | Jesus Coin | JESUS | garder |  | rare* | rare | en déclin (-95 % ou pire) | ≈ 88 M$ (estimé CG) | CoinGecko `jesus-coin` ; cap. ≈ 2,0 M$, volume 24 h ≈ 1 k$, écart -97,7 % |
| 149 | Official FO | FO | garder |  | rare* | rare | en déclin | ≈ 97 M$ (estimé CG) | CoinGecko `official-fo` ; cap. ≈ 5,9 M$, volume 24 h ≈ 35 k$, écart -93,9 % |
| 150 | Pain | PAIN | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 122 M$ (estimé CG) | CoinGecko `pain` ; cap. ≈ 2,0 M$, volume 24 h ≈ 0 k$, écart -98,3 % |
| 151 | WhiteWhale | WHITEWHALE | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 198 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `the-white-whale` ; cap. ≈ 787 k$, volume 24 h ≈ 28 k$, écart -99,6 % |
| 152 | FART COIN | FRTC | garder |  | commune* | épique | en déclin | ≈ 102 M$ (estimé CG) | CoinGecko `fart-coin` ; cap. ≈ 15 M$, volume 24 h ≈ 35 k$, écart -85,4 % |
| 153 | Daddy Doge | DADDYDOGE | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 83 M$ (estimé CG) | CoinGecko `daddy-doge` ; cap. ≈ 1,9 M$, volume 24 h ≈ 0 k$, écart -97,8 % |
| 154 | Lucidum | LUCIC | garder |  | commune* | rare | en déclin | ≈ 94 M$ (estimé CG) | CoinGecko `lucidum` ; cap. ≈ 16 M$, volume 24 h ≈ 22 k$, écart -82,7 % |
| 155 | 8-Bit Coin | COIN | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 78 M$ (estimé CG) | CoinGecko `8-bit-coin` ; cap. ≈ 2,7 M$, volume 24 h ≈ 80 k$, écart -96,5 % |
| 156 | dogi | DOGI | garder |  | commune* | épique | en déclin (-95 % ou pire) | ≈ 111 M$ (estimé CG) | CoinGecko `dogi` ; cap. ≈ 1,8 M$, volume 24 h ≈ 0 k$, écart -98,4 % |
| 157 | lmeow | LMEOW | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 99 M$ (estimé CG) | CoinGecko `lmeow-2` ; cap. ≈ 1,8 M$, volume 24 h ≈ 5 k$, écart -98,2 % |
| 158 | PotCoin | POT | retirer | jeton PotCoin : monnaie de paiement cannabis (2014), utilitaire | commune | — | mort | ≈ 90 M$ (sourcé) | CoinGecko `potcoin` ; catalogue (pic sourcé) ; cap. ≈ 252 k$, volume 24 h ≈ 0 k$, écart -100,0 % |
| 159 | Shiba Inu Treat | TREAT | garder |  | commune* | épique | en déclin (-95 % ou pire) | ≈ 109 M$ (estimé CG) | CoinGecko `shiba-inu-treat` ; cap. ≈ 834 k$, volume 24 h ≈ 35 k$, écart -99,2 % |
| 160 | Unstable Coin | USDUC | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 75 M$ (estimé CG) | CoinGecko `unstable-coin` ; cap. ≈ 1,8 M$, volume 24 h ≈ 43 k$, écart -97,5 % |
| 161 | Send | SEND | retirer | jeton de l'écosystème SendAI (Send), utilitaire | commune | — | actif | ≈ 90 M$ (sourcé) | CoinGecko `send-3` ; catalogue (pic sourcé) ; cap. ≈ 444 k$, volume 24 h ≈ 1,1 M$, écart -77,4 % |
| 162 | GeorgePlaysClashRoyale | CLASH | garder |  | commune* | rare | en déclin | ≈ 82 M$ (estimé CG) | CoinGecko `georgeplaysclashroyale` ; cap. ≈ 5,7 M$, volume 24 h ≈ 386 k$, écart -93,1 % |
| 163 | SwarmNode.ai | SNAI | retirer | plateforme d'agents IA (SwarmNode.ai) | commune | — | mort | ≈ 83 M$ (sourcé) | CoinGecko `swarmnode-ai-2` ; catalogue (pic sourcé) ; cap. ≈ 128 k$, volume 24 h ≈ 0 k$, écart -94,9 % |
| 164 | DOWGE | DJI6930 | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 85 M$ (estimé CG) | CoinGecko `dowge` ; cap. ≈ 3,7 M$, volume 24 h ≈ 153 k$, écart -95,6 % |
| 165 | 4Stock | 4STOCK | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 80 M$ (sourcé) | CoinGecko `4stock` ; catalogue (pic sourcé) ; cap. ≈ 2,1 M$, volume 24 h ≈ 2,8 M$, écart -96,5 % |
| 166 | Dolos The Bully | BULLY | garder |  | commune | rare | mort | ≈ 80 M$ (sourcé) | CoinGecko `dolos-the-bully` ; catalogue (pic sourcé) ; cap. ≈ 115 k$, volume 24 h ≈ 1 k$, écart -100,0 % |
| 167 | noice | NOICE | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 52 M$ (estimé CG) | CoinGecko `noice` ; cap. ≈ 764 k$, volume 24 h ≈ 27 k$, écart -98,5 % |
| 168 | Qkacoin | QKA | garder |  | commune* | rare | en déclin | ≈ 79 M$ (estimé CG) | CoinGecko `qkacoin` ; cap. ≈ 15 M$, volume 24 h ≈ 2 k$, écart -80,8 % |
| 169 | Book of Ethereum | BOOE | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 78 M$ (estimé CG) | CoinGecko `book-of-ethereum` ; cap. ≈ 3,1 M$, volume 24 h ≈ 31 k$, écart -96,1 % |
| 170 | Moolah | MOOLAH | garder |  | commune* | rare | actif | ≈ 78 M$ (estimé CG) | CoinGecko `moolah` ; cap. ≈ 57 M$, volume 24 h ≈ 290 k$, écart -27,9 % |
| 171 | SquidGrow | SQGROW | garder |  | commune* | rare | en déclin | ≈ 82 M$ (estimé CG) | CoinGecko `squidgrow-2` ; cap. ≈ 4,8 M$, volume 24 h ≈ 9 k$, écart -94,1 % |
| 172 | APES | APES | garder |  | commune* | rare | actif | ≈ 77 M$ (estimé CG) | CoinGecko `apes-2-2` ; cap. ≈ 72 M$, volume 24 h ≈ 0 k$, écart -5,7 % |
| 173 | Basecat | BASECAT | garder |  | commune* | rare | en déclin | ≈ 79 M$ (estimé CG) | CoinGecko `basecat` ; cap. ≈ 6,0 M$, volume 24 h ≈ 1,5 M$, écart -92,4 % |
| 174 | SafeMoon Inu | SMI | garder |  | commune | rare | mort | ≈ 73 M$ (sourcé) | CoinGecko `safemoon-inu` ; catalogue (pic sourcé) ; cap. ≈ 301 k$, volume 24 h ≈ 0 k$, écart -99,7 % |
| 175 | Ninja Squad Token | NST | retirer | jeton utilitaire d'un écosystème NFT / outils de trading (Ninja Squad Token) | commune* | — | en déclin | ≈ 73 M$ (estimé CG) | CoinGecko `ninja-squad` ; cap. ≈ 10 M$, volume 24 h ≈ 222 k$, écart -86,3 % |
| 176 | Yummy | YUMMY | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 81 M$ (estimé CG) | CoinGecko `yummy` ; cap. ≈ 2,2 M$, volume 24 h ≈ 0 k$, écart -97,3 % |
| 177 | Froggie | FROGGIE | garder |  | commune* | rare | en déclin | ≈ 71 M$ (estimé CG) | CoinGecko `froggie` ; cap. ≈ 14 M$, volume 24 h ≈ 70 k$, écart -80,7 % |
| 178 | Kabosu | KABOSU | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 82 M$ (estimé CG) | CoinGecko `kabosu` ; cap. ≈ 2,9 M$, volume 24 h ≈ 0 k$, écart -96,5 % |
| 179 | PHNIX | PHNIX | garder |  | commune* | rare | en déclin | ≈ 68 M$ (estimé CG) | CoinGecko `phnix` ; cap. ≈ 4,1 M$, volume 24 h ≈ 93 k$, écart -94,0 % |
| 180 | FXN | FXN | retirer | réseau d'agents IA (FXN) | commune | — | mort | ≈ 99 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `fxn` ; cap. ≈ 201 k$, volume 24 h ≈ 1 k$, écart -99,8 % |
| 181 | LOBO•THE•WOLF•PUP | LOBO | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 3,59 Md$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `lobo-the-wolf-pup-runes` ; cap. ≈ 32 M$, volume 24 h ≈ 5 k$, écart -99,1 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique |
| 182 | Major | MAJOR | retirer | jeu Telegram (Major) | commune | — | à vérifier (homonyme sur CoinGecko, non rapproché) | ≈ 71 M$ (sourcé) | catalogue (pic sourcé) |
| 183 | Ani | ANI | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 70 M$ (sourcé) | catalogue (pic sourcé) |
| 184 | Aura | AURA | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 231 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `aura-on-sol` ; cap. ≈ 5,6 M$, volume 24 h ≈ 295 k$, écart -97,6 % |
| 185 | Base God | TYBG | garder |  | commune* | rare | mort | ≈ 86 M$ (estimé CG) | CoinGecko `base-god` ; cap. ≈ 676 k$, volume 24 h ≈ 0 k$, écart -99,2 % — doublon probable de n° 558 Based Tyler (TYBG) |
| 186 | Joe Coin | JOE | garder |  | commune* | rare | en déclin | ≈ 75 M$ (estimé CG) | CoinGecko `joe-coin` ; cap. ≈ 4,3 M$, volume 24 h ≈ 31 k$, écart -94,3 % |
| 187 | MEMDEX100 | MEMDEX | garder |  | commune* | rare | mort | ≈ 90 M$ (estimé CG) | CoinGecko `memdex100` ; cap. ≈ 700 k$, volume 24 h ≈ 2 k$, écart -99,2 % — mème communautaire malgré le nom d'indice (pas un fonds) |
| 188 | PeiPei | PEIPEI | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 165 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `peipeicoin-vip` ; cap. ≈ 1,4 M$, volume 24 h ≈ 3 k$, écart -99,2 % |
| 189 | Shina Inu | SHI | garder |  | commune* | rare | mort | ≈ 50 M$ (estimé CG) | CoinGecko `shina-inu` ; cap. ≈ 657 k$, volume 24 h ≈ 2 k$, écart -98,7 % |
| 190 | Turbo | TURBO | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 987 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `turbo` ; cap. ≈ 48 M$, volume 24 h ≈ 4,2 M$, écart -95,1 % — pic du catalogue (> 70 M$) très sous-estimé |
| 191 | USCR | USCR | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 58 M$ (estimé CG) | CoinGecko `uscr` ; cap. ≈ 1,3 M$, volume 24 h ≈ 2 k$, écart -97,7 % |
| 192 | Manyu | MANYU | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 70 M$ (estimé CG) | CoinGecko `manyu-2` ; cap. ≈ 2,7 M$, volume 24 h ≈ 374 k$, écart -96,1 % |
| 193 | pipedog | PIPEDOG | garder |  | commune* | rare | en déclin | ≈ 65 M$ (estimé CG) | CoinGecko `pipedog` ; cap. ≈ 4,4 M$, volume 24 h ≈ 1,6 M$, écart -93,2 % |
| 194 | Boss | BOSS | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 58 M$ (estimé CG) | CoinGecko `boss` ; cap. ≈ 1,3 M$, volume 24 h ≈ 1 k$, écart -97,7 % |
| 195 | Byte | BYTE | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 61 M$ (estimé CG) | CoinGecko `byte` ; cap. ≈ 1,4 M$, volume 24 h ≈ 34 k$, écart -97,8 % |
| 196 | Milo Inu | MILO | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 68 M$ (estimé CG) | CoinGecko `milo-inu` ; cap. ≈ 1,3 M$, volume 24 h ≈ 0 k$, écart -98,0 % |
| 197 | Mochi † | MOCHI | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 81 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `mochi-thecatcoin` ; cap. ≈ 577 k$, volume 24 h ≈ 54 k$, écart -99,3 % |
| 198 | ZZZ | ZZZ | garder |  | commune* | rare | en déclin | ≈ 68 M$ (estimé CG) | CoinGecko `zzz-2` ; cap. ≈ 3,5 M$, volume 24 h ≈ 1,0 M$, écart -94,9 % |
| 199 | Utya | UTYA | garder |  | commune* | rare | actif | ≈ 63 M$ (estimé CG) | CoinGecko `utya` ; cap. ≈ 18 M$, volume 24 h ≈ 380 k$, écart -71,2 % |
| 200 | Build On BNB | BOB | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 58 M$ (estimé CG) | CoinGecko `build-on-bnb` ; cap. ≈ 2,3 M$, volume 24 h ≈ 381 k$, écart -96,0 % |
| 201 | Crob Mob | CROB | garder |  | commune* | rare | en déclin | ≈ 61 M$ (estimé CG) | CoinGecko `crob-mob` ; cap. ≈ 6,6 M$, volume 24 h ≈ 0 k$, écart -89,1 % |
| 202 | Dogz | DOGZ | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 55 M$ (estimé CG) | CoinGecko `dogz` ; cap. ≈ 1,2 M$, volume 24 h ≈ 0 k$, écart -97,8 % |
| 203 | DYZilla | DYZILLA | garder |  | commune* | rare | mort | ≈ 55 M$ (estimé CG) | CoinGecko `dyzilla` ; cap. ≈ 575 k$, volume 24 h ≈ 0 k$, écart -99,0 % |
| 204 | Fair and Free | FAIR3 | garder |  | commune* | rare | mort | ≈ 41 M$ (estimé CG) | CoinGecko `fair-and-free` ; cap. ≈ 555 k$, volume 24 h ≈ 2 k$, écart -98,6 % |
| 205 | Finvesta | FINVESTA | retirer | jeton déflationniste DeFi PulseChain (Finvesta) | commune* | — | en déclin (-95 % ou pire) | ≈ 76 M$ (estimé CG) | CoinGecko `finvesta` ; cap. ≈ 1,2 M$, volume 24 h ≈ 1 k$, écart -98,4 % |
| 206 | Forgive Me Father | $PURGE | garder |  | commune* | rare | mort | ≈ 71 M$ (estimé CG) | CoinGecko `forgive-me-father` ; cap. ≈ 641 k$, volume 24 h ≈ 0 k$, écart -99,1 % |
| 207 | FourBook | FB | garder |  | commune* | rare | mort | ≈ 40 M$ (estimé CG) | CoinGecko `fourbook` ; cap. ≈ 584 k$, volume 24 h ≈ 0 k$, écart -98,5 % |
| 208 | Froge | FROGE | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 46 M$ (estimé CG) | CoinGecko `frogevip` ; cap. ≈ 558 k$, volume 24 h ≈ 33 k$, écart -98,8 % |
| 209 | Hege | HEGE | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 51 M$ (estimé CG) | CoinGecko `hege` ; cap. ≈ 1,2 M$, volume 24 h ≈ 1 k$, écart -97,7 % |
| 210 | Mind of Pepe | MIND | retirer | prévente « agent IA » (Mind of Pepe) | commune* | — | en déclin (-95 % ou pire) | ≈ 107 M$ (estimé CG) | CoinGecko `mind-of-pepe` ; cap. ≈ 568 k$, volume 24 h ≈ 53 k$, écart -99,5 % |
| 211 | Pepe on SOL | PEPE | garder |  | commune* | rare | mort | ≈ 81 M$ (estimé CG) | CoinGecko `pepe-sol` ; cap. ≈ 568 k$, volume 24 h ≈ 2 k$, écart -99,3 % |
| 212 | SHIBA BSC | SHIBSC | garder |  | commune* | rare | mort | ≈ 84 M$ (estimé CG) | CoinGecko `shiba-bsc` ; cap. ≈ 574 k$, volume 24 h ≈ 0 k$, écart -99,3 % |
| 213 | The Spirit of Gambling | TOKABU | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 76 M$ (estimé CG) | CoinGecko `the-spirit-of-gambling` ; cap. ≈ 1,3 M$, volume 24 h ≈ 83 k$, écart -98,3 % |
| 214 | WAR | WAR | garder |  | commune* | rare | mort | ≈ 45 M$ (estimé CG) | CoinGecko `war-2` ; cap. ≈ 647 k$, volume 24 h ≈ 8 k$, écart -98,6 % |
| 215 | Tiger King | TKING | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 59 M$ (sourcé) | catalogue (pic sourcé) |
| 216 | Dessa | DESSA | garder |  | commune* | rare | en déclin | ≈ 59 M$ (estimé CG) | CoinGecko `dessa` ; cap. ≈ 10 M$, volume 24 h ≈ 1,6 M$, écart -82,5 % |
| 217 | Basenji | BENJI | garder |  | commune | rare | mort | ≈ 57 M$ (sourcé) | CoinGecko `basenji` ; catalogue (pic sourcé) ; cap. ≈ 816 k$, volume 24 h ≈ 4 k$, écart -99,2 % |
| 218 | CREPE | CREPE | garder |  | commune* | rare | en déclin | ≈ 54 M$ (estimé CG) | CoinGecko `crepe-2` ; cap. ≈ 5,1 M$, volume 24 h ≈ 138 k$, écart -90,6 % |
| 219 | Kori | KORI | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 58 M$ (estimé CG) | CoinGecko `kori` ; cap. ≈ 1,7 M$, volume 24 h ≈ 29 k$, écart -97,0 % |
| 220 | Luminous | LUM | garder |  | commune | rare | mort | ≈ 80 M$ (sourcé) | CoinGecko `luminous` ; catalogue (pic sourcé) ; cap. ≈ 179 k$, volume 24 h ≈ 1 k$, écart -99,8 % — mème créé par deux agents IA (aethernet, clanker) |
| 221 | Not in Employment, Education, or Training | NEET | garder |  | commune* | rare | actif | ≈ 56 M$ (estimé CG) | CoinGecko `neet` ; cap. ≈ 27 M$, volume 24 h ≈ 1,1 M$, écart -50,8 % |
| 222 | Cocoro | COCORO | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 66 M$ (estimé CG) | CoinGecko `cocoro` ; cap. ≈ 1,1 M$, volume 24 h ≈ 0 k$, écart -98,3 % |
| 223 | MUSHROOM | SHROOM | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 57 M$ (estimé CG) | CoinGecko `mushroom-2` ; cap. ≈ 1,1 M$, volume 24 h ≈ 34 k$, écart -98,1 % |
| 224 | Neur | NEUR | retirer | application d'agent IA (Neur) | commune | — | mort | ≈ 70 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `neur-sh` ; cap. ≈ 59 k$, volume 24 h ≈ 0 k$, écart -99,9 % |
| 225 | PiP | PIP | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 64 M$ (estimé CG) | CoinGecko `pip-3` ; cap. ≈ 1,0 M$, volume 24 h ≈ 6 k$, écart -98,4 % |
| 226 | Hosico Cat | HOSICO | garder |  | commune | rare | mort | ≈ 75 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `hosico-cat` ; cap. ≈ 855 k$, volume 24 h ≈ 0 k$, écart -98,9 % — rapprochement CoinGecko par ticker seul |
| 227 | HoodPork | PORKU | garder |  | commune* | rare | actif | ≈ 53 M$ (estimé CG) | CoinGecko `hoodpork` ; cap. ≈ 16 M$, volume 24 h ≈ 0 k$, écart -69,7 % |
| 228 | wojak | WOJAK | garder |  | commune* | rare | actif | ≈ 53 M$ (estimé CG) | CoinGecko `wojak-5` ; cap. ≈ 13 M$, volume 24 h ≈ 973 k$, écart -75,7 % |
| 229 | Chump Coin | CHUMP | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 57 M$ (estimé CG) | CoinGecko `chump-coin` ; cap. ≈ 2,3 M$, volume 24 h ≈ 1,2 M$, écart -96,0 % |
| 230 | Pwease | PWEASE | garder |  | commune* | rare | en déclin | ≈ 53 M$ (estimé CG) | CoinGecko `pwease` ; cap. ≈ 3,1 M$, volume 24 h ≈ 80 k$, écart -94,2 % |
| 231 | The Bitcoin Bull | TBB | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 48 M$ (estimé CG) | CoinGecko `the-bitcoin-bull` ; cap. ≈ 1,9 M$, volume 24 h ≈ 33 k$, écart -96,0 % |
| 232 | Baby Shiba Inu | BABYSHIBAINU | garder |  | commune* | rare | en déclin | ≈ 51 M$ (estimé CG) | CoinGecko `baby-shiba-inu` ; cap. ≈ 6,0 M$, volume 24 h ≈ 0 k$, écart -88,1 % |
| 233 | Aura Final Boss | KIMCHI | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 45 M$ (estimé CG) | CoinGecko `aura-final-boss-2` ; cap. ≈ 2,2 M$, volume 24 h ≈ 635 k$, écart -95,2 % |
| 234 | AVAX Lambo | LAMBO | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 50 M$ (sourcé) | catalogue (pic sourcé) |
| 235 | Boop | BOOP | garder |  | commune* | rare | mort | ≈ 47 M$ (estimé CG) | CoinGecko `boop-2` ; cap. ≈ 511 k$, volume 24 h ≈ 1 k$, écart -98,9 % |
| 236 | Dupe | DUPE | garder |  | commune* | rare | mort | ≈ 62 M$ (estimé CG) | CoinGecko `dupe` ; cap. ≈ 535 k$, volume 24 h ≈ 1 k$, écart -99,1 % |
| 237 | GOUT | GOUT | garder |  | commune* | rare | mort | ≈ 77 M$ (estimé CG) | CoinGecko `gout` ; cap. ≈ 542 k$, volume 24 h ≈ 0 k$, écart -99,3 % |
| 238 | I love puppies | PUPPIES | garder |  | commune* | rare | en déclin | ≈ 49 M$ (estimé CG) | CoinGecko `i-love-puppies` ; cap. ≈ 5,4 M$, volume 24 h ≈ 439 k$, écart -88,9 % |
| 239 | KiboShib | KIBSHI | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 48 M$ (estimé CG) | CoinGecko `kiboshib` ; cap. ≈ 1,5 M$, volume 24 h ≈ 5 k$, écart -96,8 % |
| 240 | Lofi | LOFI | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 50 M$ (sourcé) | CoinGecko `lofi-2` ; catalogue (pic sourcé) ; cap. ≈ 8,4 M$, volume 24 h ≈ 132 k$, écart -96,6 % |
| 241 | TEH EPIK DUCK | EPIK | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 50 M$ (estimé CG) | CoinGecko `teh-epik-duck` ; cap. ≈ 1,5 M$, volume 24 h ≈ 675 k$, écart -97,1 % |
| 242 | Vita Inu | VINU | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 66 M$ (estimé CG) | CoinGecko `vita-inu` ; cap. ≈ 521 k$, volume 24 h ≈ 108 k$, écart -99,2 % |
| 243 | XDOG | XDOG | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 49 M$ (estimé CG) | CoinGecko `xdog` ; cap. ≈ 1,4 M$, volume 24 h ≈ 544 k$, écart -97,1 % |
| 244 | IlluminatiCoin | NATI | garder |  | commune* | rare | en déclin | ≈ 50 M$ (estimé CG) | CoinGecko `illuminaticoin` ; cap. ≈ 4,3 M$, volume 24 h ≈ 0 k$, écart -91,3 % |
| 246 | Blub | BLUB | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 47 M$ (sourcé) | CoinGecko `blub` ; catalogue (pic sourcé) ; cap. ≈ 1,9 M$, volume 24 h ≈ 2 k$, écart -98,2 % |
| 247 | Dingocoin | DINGO | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 48 M$ (estimé CG) | CoinGecko `dingocoin` ; cap. ≈ 1,4 M$, volume 24 h ≈ 37 k$, écart -97,0 % |
| 248 | Manifesting | MANIFEST | garder |  | commune* | rare | en déclin | ≈ 48 M$ (estimé CG) | CoinGecko `manifesting` ; cap. ≈ 3,5 M$, volume 24 h ≈ 186 k$, écart -92,7 % |
| 249 | BabyCashCat | BABY | garder |  | commune* | rare | en déclin | ≈ 43 M$ (estimé CG) | CoinGecko `babycashcat` ; cap. ≈ 3,6 M$, volume 24 h ≈ 0 k$, écart -91,7 % |
| 250 | KNOTS | KNOTS | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 49 M$ (estimé CG) | CoinGecko `knots` ; cap. ≈ 1,8 M$, volume 24 h ≈ 975 k$, écart -96,4 % |
| 251 | Pepe 2.0 | PEPE2.0 | garder |  | commune | rare | mort | ≈ 45 M$ (sourcé) | CoinGecko `pepe-2-0` ; catalogue (pic sourcé) ; cap. ≈ 264 k$, volume 24 h ≈ 1 k$, écart -99,8 % |
| 252 | Everybody | HOLD | garder |  | commune* | rare | en déclin | ≈ 46 M$ (estimé CG) | CoinGecko `everybody` ; cap. ≈ 3,1 M$, volume 24 h ≈ 10 k$, écart -93,1 % |
| 254 | Bitcoin Wizards | WZRD | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 43 M$ (sourcé) | catalogue (pic sourcé) |
| 255 | Moochii | MOOCHII | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 43 M$ (estimé CG) | CoinGecko `moochii` ; cap. ≈ 1,2 M$, volume 24 h ≈ 0 k$, écart -97,1 % |
| 256 | Anon | ANON | garder |  | commune | rare | mort | ≈ 62 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `super-anon` ; cap. ≈ 35 k$, volume 24 h ≈ 0 k$, écart -99,9 % |
| 257 | Doge KaKi | KAKI | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 44 M$ (estimé CG) | CoinGecko `doge-kaki` ; cap. ≈ 1,6 M$, volume 24 h ≈ 0 k$, écart -96,3 % |
| 258 | Not Pixel | PX | retirer | jeu Telegram (Not Pixel) | commune* | — | en déclin (-95 % ou pire) | ≈ 49 M$ (estimé CG) | CoinGecko `not-pixel` ; cap. ≈ 1,8 M$, volume 24 h ≈ 18 k$, écart -96,4 % |
| 259 | NYC | NYC | garder |  | commune* | rare | actif | ≈ 43 M$ (estimé CG) | CoinGecko `nyc-token` ; cap. ≈ 25 M$, volume 24 h ≈ 0 k$, écart -40,4 % |
| 260 | Jager Hunter | JAGER | garder |  | commune* | rare | en déclin | ≈ 40 M$ (estimé CG) | CoinGecko `jager-hunter` ; cap. ≈ 5,0 M$, volume 24 h ≈ 11 k$, écart -87,7 % |
| 261 | microduck | MICRODUCK | garder |  | commune* | rare | en déclin | ≈ 45 M$ (estimé CG) | CoinGecko `microduck` ; cap. ≈ 2,8 M$, volume 24 h ≈ 1,1 M$, écart -93,7 % |
| 262 | TENDIES | TENDIES | garder |  | commune* | rare | en déclin | ≈ 40 M$ (estimé CG) | CoinGecko `tendies-2` ; cap. ≈ 3,0 M$, volume 24 h ≈ 1,0 M$, écart -92,5 % |
| 263 | 114514 | 114514 | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 40 M$ (sourcé) | catalogue (pic sourcé) |
| 264 | Araracoin | ARARA | garder |  | commune* | rare | actif | ≈ 39 M$ (estimé CG) | CoinGecko `araracoin` ; cap. ≈ 16 M$, volume 24 h ≈ 17 k$, écart -58,6 % |
| 265 | Catcoin | CAT | garder |  | commune* | rare | mort | ≈ 40 M$ (estimé CG) | CoinGecko `catcoin` ; cap. ≈ 811 k$, volume 24 h ≈ 4 k$, écart -98,0 % |
| 266 | CatSlap | SLAP | garder |  | commune* | rare | mort | ≈ 40 M$ (estimé CG) | CoinGecko `catslap` ; cap. ≈ 832 k$, volume 24 h ≈ 0 k$, écart -97,9 % |
| 267 | Clawd | CLAWD | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 40 M$ (sourcé) | catalogue (pic sourcé) |
| 268 | Memory cow Moo | MOO | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 43 M$ (estimé CG) | CoinGecko `memory-cow-moo` ; cap. ≈ 730 k$, volume 24 h ≈ 971 k$, écart -98,3 % |
| 269 | Roaring Kitty | KITTY | garder |  | commune | rare | mort | ≈ 40 M$ (sourcé) | CoinGecko `roaring-kitty-solana` ; catalogue (pic sourcé) ; cap. ≈ 158 k$, volume 24 h ≈ 0 k$, écart -99,5 % |
| 270 | The Official 67 Coin | 67 | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 44 M$ (estimé CG) | CoinGecko `the-official-67-coin` ; cap. ≈ 1,2 M$, volume 24 h ≈ 391 k$, écart -97,2 % — doublon possible de n° 290 SIXSEVEN (ticker 67) |
| 271 | Tralalero Tralala | à vérifier | garder |  | commune | rare | mort | ≈ 40 M$ (sourcé) | CoinGecko `tralalero-tralala` ; catalogue (pic sourcé) ; cap. ≈ 9 k$, volume 24 h ≈ 0 k$, écart -98,9 % |
| 272 | ubik | UBIK | garder |  | commune* | rare | en déclin | ≈ 40 M$ (estimé CG) | CoinGecko `ubik` ; cap. ≈ 5,3 M$, volume 24 h ≈ 1,1 M$, écart -86,7 % |
| 273 | UWON | UWON | garder |  | commune* | rare | mort | ≈ 48 M$ (estimé CG) | CoinGecko `uwon` ; cap. ≈ 813 k$, volume 24 h ≈ 0 k$, écart -98,3 % |
| 274 | Claude Crab | CRABAI | garder |  | commune* | rare | actif | ≈ 39 M$ (estimé CG) | CoinGecko `claude-crab` ; cap. ≈ 15 M$, volume 24 h ≈ 20 k$, écart -61,6 % |
| 275 | KiraKuru | KRA | garder |  | commune* | rare | en déclin | ≈ 39 M$ (estimé CG) | CoinGecko `kirakuru` ; cap. ≈ 2,7 M$, volume 24 h ≈ 0 k$, écart -93,1 % |
| 276 | FUD the Pug † | FUD | garder |  | commune | rare | mort | ≈ 39 M$ (sourcé) | CoinGecko `fud-the-pug` ; catalogue (pic sourcé) ; cap. ≈ 223 k$, volume 24 h ≈ 1 k$, écart -99,6 % |
| 277 | Thinking Cat | HMM | garder |  | commune* | rare | en déclin | ≈ 38 M$ (estimé CG) | CoinGecko `thinking-cat` ; cap. ≈ 5,8 M$, volume 24 h ≈ 1,3 M$, écart -84,8 % |
| 278 | MAGIC•INTERNET•MONEY | MIM | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 38 M$ (sourcé) | catalogue (pic sourcé) |
| 279 | Cets On Gold | CETS | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 32 M$ (estimé CG) | CoinGecko `cets-on-gold` ; cap. ≈ 1,4 M$, volume 24 h ≈ 1,4 M$, écart -95,5 % |
| 280 | Fuzzybear | FUZZY | garder |  | commune* | rare | actif | ≈ 38 M$ (estimé CG) | CoinGecko `fuzzybear` ; cap. ≈ 16 M$, volume 24 h ≈ 107 k$, écart -56,9 % |
| 281 | 哈基米 (Hakimi, Hajimi) | 哈基米 | garder |  | commune | rare | en déclin | ≈ 88 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `hakimi` ; cap. ≈ 16 M$, volume 24 h ≈ 1,2 M$, écart -81,7 % — rapprochement CoinGecko par ticker seul |
| 282 | ASSAI | ASSAI | retirer | agent IA de trading (ASSAI, Assisterr) | commune | — | mort | ≈ 49 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `assai` ; cap. ≈ 9 k$, volume 24 h ≈ 0 k$, écart -100,0 % |
| 283 | Simon's Cat | CAT | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 511 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `simon-s-cat` ; cap. ≈ 13 M$, volume 24 h ≈ 626 k$, écart -97,5 % |
| 284 | Most Wanted | MOST | garder |  | commune* | rare | en déclin | ≈ 38 M$ (estimé CG) | CoinGecko `most-wanted-2` ; cap. ≈ 2,8 M$, volume 24 h ≈ 2 k$, écart -92,7 % |
| 286 | apeonfone | FONE | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 39 M$ (estimé CG) | CoinGecko `apeonfone` ; cap. ≈ 1,3 M$, volume 24 h ≈ 1,3 M$, écart -96,7 % |
| 287 | Dog Wif Nunchucks | NINJA | garder |  | commune* | rare | mort | ≈ 41 M$ (estimé CG) | CoinGecko `dog-wif-nuchucks` ; cap. ≈ 713 k$, volume 24 h ≈ 0 k$, écart -98,3 % |
| 288 | Gstock | GSTOCK | garder |  | commune* | rare | en déclin | ≈ 34 M$ (estimé CG) | CoinGecko `gstock` ; cap. ≈ 3,6 M$, volume 24 h ≈ 1,3 M$, écart -89,6 % |
| 289 | Mistery | MERY | garder |  | commune* | rare | mort | ≈ 36 M$ (estimé CG) | CoinGecko `mistery` ; cap. ≈ 742 k$, volume 24 h ≈ 5 k$, écart -97,9 % |
| 290 | SIXSEVEN | 67 | garder |  | commune* | rare | actif | ≈ 35 M$ (estimé CG) | CoinGecko `sixseven` ; cap. ≈ 9,0 M$, volume 24 h ≈ 2 k$, écart -74,1 % — doublon possible de n° 270 The Official 67 Coin (ticker 67) |
| 291 | Bongo | BONGO | garder |  | commune | rare | mort | ≈ 143 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `bongo-cat` ; cap. ≈ 422 k$, volume 24 h ≈ 3 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins; rapprochement CoinGecko par ticker seul |
| 292 | Buy the DIP | DIP | garder |  | commune* | rare | en déclin | ≈ 34 M$ (estimé CG) | CoinGecko `buy-the-dip` ; cap. ≈ 2,3 M$, volume 24 h ≈ 0 k$, écart -93,2 % |
| 293 | Pofu | POFU | garder |  | commune* | rare | en déclin | ≈ 32 M$ (estimé CG) | CoinGecko `pofu` ; cap. ≈ 5,2 M$, volume 24 h ≈ 0 k$, écart -83,7 % |
| 294 | PUMPSTOP | XCAT | garder |  | commune* | rare | actif | ≈ 32 M$ (estimé CG) | CoinGecko `pumpstop` ; cap. ≈ 18 M$, volume 24 h ≈ 23 k$, écart -44,2 % |
| 295 | KarenCoin | KAREN | garder |  | commune* | rare | en déclin | ≈ 31 M$ (estimé CG) | CoinGecko `karencoin` ; cap. ≈ 1,6 M$, volume 24 h ≈ 0 k$, écart -94,8 % |
| 296 | Salute | SLT | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 29 M$ (estimé CG) | CoinGecko `salute` ; cap. ≈ 1,3 M$, volume 24 h ≈ 2 k$, écart -95,7 % |
| 297 | Little John | JOHN | garder |  | commune* | rare | actif | ≈ 31 M$ (estimé CG) | CoinGecko `little-john` ; cap. ≈ 17 M$, volume 24 h ≈ 0 k$, écart -44,3 % |
| 298 | TANUKI•WISDOM | TANUKI | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 31 M$ (sourcé) | catalogue (pic sourcé) |
| 299 | Yee Token | YEE | garder |  | commune* | rare | en déclin | ≈ 30 M$ (estimé CG) | CoinGecko `yee-token` ; cap. ≈ 4,0 M$, volume 24 h ≈ 429 k$, écart -86,6 % |
| 300 | Dotcom | Y2K | garder |  | commune* | rare | mort | ≈ 35 M$ (estimé CG) | CoinGecko `dotcom` ; cap. ≈ 736 k$, volume 24 h ≈ 8 k$, écart -97,9 % |
| 301 | FLORK | FLORK | garder |  | commune* | rare | en déclin | ≈ 32 M$ (estimé CG) | CoinGecko `flork-3` ; cap. ≈ 1,7 M$, volume 24 h ≈ 150 k$, écart -94,8 % |
| 302 | Giggle Mascot | MAX | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 32 M$ (estimé CG) | CoinGecko `giggle-mascot` ; cap. ≈ 1,5 M$, volume 24 h ≈ 67 k$, écart -95,2 % |
| 303 | Goldn | GOLDN | garder |  | commune* | rare | mort | ≈ 31 M$ (estimé CG) | CoinGecko `goldn` ; cap. ≈ 572 k$, volume 24 h ≈ 0 k$, écart -98,1 % |
| 304 | Harold | HAROLD | garder |  | commune* | rare | actif | ≈ 30 M$ (estimé CG) | CoinGecko `haroldonsol` ; cap. ≈ 15 M$, volume 24 h ≈ 115 k$, écart -48,9 % |
| 305 | HeeeHeee | HEEHEE | garder |  | commune* | rare | mort | ≈ 26 M$ (estimé CG) | CoinGecko `heeeheee` ; cap. ≈ 636 k$, volume 24 h ≈ 0 k$, écart -97,5 % |
| 306 | Kimbo | KIMBO | garder |  | commune | rare | mort | ≈ 50 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `kimbo` ; cap. ≈ 174 k$, volume 24 h ≈ 0 k$, écart -99,6 % |
| 307 | LEO | LEO | garder |  | commune* | rare | mort | ≈ 30 M$ (estimé CG) | CoinGecko `leopold` ; cap. ≈ 645 k$, volume 24 h ≈ 3 k$, écart -97,8 % |
| 308 | Luxxcoin | LUX | garder |  | commune* | rare | en déclin | ≈ 30 M$ (estimé CG) | CoinGecko `luxxcoin` ; cap. ≈ 3,0 M$, volume 24 h ≈ 0 k$, écart -90,1 % |
| 309 | Osaka Protocol | OSAK | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 332 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `osaka-protocol` ; cap. ≈ 11 M$, volume 24 h ≈ 57 k$, écart -96,6 % |
| 310 | uPX | UPX | garder |  | commune* | rare | mort | ≈ 32 M$ (estimé CG) | CoinGecko `upx` ; cap. ≈ 628 k$, volume 24 h ≈ 1 k$, écart -98,0 % |
| 311 | 吉祥马 | 吉祥马 | garder |  | commune* | rare | mort | ≈ 33 M$ (estimé CG) | CoinGecko `jixiangma` ; cap. ≈ 534 k$, volume 24 h ≈ 3 k$, écart -98,4 % |
| 312 | Memetern | MXT | garder |  | commune* | rare | en déclin | ≈ 30 M$ (estimé CG) | CoinGecko `memetern` ; cap. ≈ 5,0 M$, volume 24 h ≈ 0 k$, écart -83,2 % |
| 313 | Super Inu | SI | garder |  | commune* | rare | actif | ≈ 29 M$ (estimé CG) | CoinGecko `super-inu-3` ; cap. ≈ 17 M$, volume 24 h ≈ 2,2 M$, écart -41,9 % |
| 314 | Dora | DORA | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 576 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `dora-2` ; cap. ≈ 1,8 M$, volume 24 h ≈ 0 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 315 | ALLINU | ALLINU | garder |  | commune* | rare | en déclin | ≈ 28 M$ (estimé CG) | CoinGecko `allinu` ; cap. ≈ 2,3 M$, volume 24 h ≈ 1,1 M$, écart -91,8 % |
| 316 | GIVEBACK | GBACK | garder |  | commune* | rare | en déclin | ≈ 28 M$ (estimé CG) | CoinGecko `giveback` ; cap. ≈ 3,6 M$, volume 24 h ≈ 13 k$, écart -87,1 % |
| 317 | MOEW | MOEW | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 32 M$ (estimé CG) | CoinGecko `moew` ; cap. ≈ 1,2 M$, volume 24 h ≈ 157 k$, écart -96,4 % |
| 318 | Attention | ATTN | garder |  | commune* | rare | mort | ≈ 24 M$ (estimé CG) | CoinGecko `attention` ; cap. ≈ 753 k$, volume 24 h ≈ 0 k$, écart -96,9 % |
| 319 | BORGY | $BORGY | garder |  | commune* | rare | en déclin | ≈ 26 M$ (estimé CG) | CoinGecko `borgy` ; cap. ≈ 1,9 M$, volume 24 h ≈ 2 k$, écart -92,7 % |
| 320 | Chomolon Joff | JOFF | garder |  | commune* | rare | en déclin | ≈ 27 M$ (estimé CG) | CoinGecko `chomolon-joff` ; cap. ≈ 5,3 M$, volume 24 h ≈ 37 k$, écart -80,2 % |
| 321 | Dacity Coin | DACITY | garder |  | commune* | rare | actif | ≈ 28 M$ (estimé CG) | CoinGecko `dacity-coin-4` ; cap. ≈ 18 M$, volume 24 h ≈ 2,1 M$, écart -35,8 % — doublon possible de n° 473 AudaCity (DACITYCOIN) |
| 322 | Kaspy | KASPY | garder |  | commune* | rare | mort | ≈ 32 M$ (estimé CG) | CoinGecko `kaspy` ; cap. ≈ 788 k$, volume 24 h ≈ 12 k$, écart -97,5 % |
| 323 | Bear Champ | BCHAMP | garder |  | commune* | rare | en déclin | ≈ 26 M$ (estimé CG) | CoinGecko `bear-champ` ; cap. ≈ 4,6 M$, volume 24 h ≈ 2 k$, écart -82,0 % |
| 324 | BLUE CHIP | BLUECHIP | garder |  | commune* | rare | en déclin | ≈ 25 M$ (estimé CG) | CoinGecko `blue-chip-4` ; cap. ≈ 2,3 M$, volume 24 h ≈ 411 k$, écart -90,6 % |
| 325 | Chill House | CHILLHOUSE | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 29 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `chill-house` ; cap. ≈ 655 k$, volume 24 h ≈ 316 k$, écart -97,8 % |
| 326 | Bundle Cat | BUN | garder |  | commune* | rare | actif | ≈ 24 M$ (estimé CG) | CoinGecko `bundle-cat` ; cap. ≈ 6,1 M$, volume 24 h ≈ 1,5 M$, écart -75,0 % |
| 327 | Buy The Cat | BTC | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 24 M$ (estimé CG) | CoinGecko `buy-the-cat` ; cap. ≈ 504 k$, volume 24 h ≈ 21 k$, écart -97,9 % |
| 328 | PulseChain Peacock | PCOCK | garder |  | commune* | rare | actif | ≈ 26 M$ (estimé CG) | CoinGecko `pulsechain-peacock` ; cap. ≈ 6,7 M$, volume 24 h ≈ 33 k$, écart -74,1 % |
| 329 | Skull of Pepe Token | SKOP | garder |  | commune* | rare | mort | ≈ 21 M$ (estimé CG) | CoinGecko `skull-of-pepe-token` ; cap. ≈ 516 k$, volume 24 h ≈ 14 k$, écart -97,6 % |
| 330 | Theros | THEROS | garder |  | commune* | rare | actif | ≈ 24 M$ (estimé CG) | CoinGecko `theros` ; cap. ≈ 15 M$, volume 24 h ≈ 15 k$, écart -37,0 % |
| 331 | Volt Inu | VOLT | garder |  | commune | rare | actif | ≈ 30 M$ (sourcé) | CoinGecko `volt-inu-3` ; catalogue (pic sourcé) ; cap. ≈ 2,7 M$, volume 24 h ≈ 5 k$, écart -68,6 % |
| 332 | Bobo | BOBO | garder |  | commune* | rare | actif | ≈ 24 M$ (estimé CG) | CoinGecko `bobo-coin-2` ; cap. ≈ 5,0 M$, volume 24 h ≈ 478 k$, écart -79,1 % |
| 333 | CyberLeek | CYBERLEEK | garder |  | commune* | rare | en déclin | ≈ 25 M$ (estimé CG) | CoinGecko `cyberleek` ; cap. ≈ 1,6 M$, volume 24 h ≈ 1,7 M$, écart -93,7 % |
| 334 | Bloo | BLOO | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 23 M$ (sourcé) | catalogue (pic sourcé) |
| 335 | 401jK | 401JK | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 28 M$ (estimé CG) | CoinGecko `401jk` ; cap. ≈ 724 k$, volume 24 h ≈ 25 k$, écart -97,4 % |
| 336 | FOMO人生 | FOMO人生 | garder |  | commune* | rare | actif | ≈ 23 M$ (estimé CG) | CoinGecko `fomo-life` ; cap. ≈ 13 M$, volume 24 h ≈ 25 k$, écart -44,7 % |
| 337 | Hachiko | HACHI | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 23 M$ (estimé CG) | CoinGecko `hachiko-3` ; cap. ≈ 620 k$, volume 24 h ≈ 32 k$, écart -97,3 % |
| 338 | HUNDRED | HUNDRED | garder |  | commune* | rare | actif | ≈ 23 M$ (estimé CG) | CoinGecko `hundred` ; cap. ≈ 22 M$, volume 24 h ≈ 2 k$, écart -5,6 % |
| 339 | Pepes Dog | ZEUS | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 26 M$ (estimé CG) | CoinGecko `pepes-dog` ; cap. ≈ 720 k$, volume 24 h ≈ 24 k$, écart -97,3 % |
| 340 | Playdoge | $PLAY | garder |  | commune* | rare | mort | ≈ 22 M$ (estimé CG) | CoinGecko `playdoge` ; cap. ≈ 725 k$, volume 24 h ≈ 0 k$, écart -96,7 % |
| 341 | Pup Doge | PUPDOGE | garder |  | commune* | rare | en déclin | ≈ 24 M$ (estimé CG) | CoinGecko `pup-doge` ; cap. ≈ 1,6 M$, volume 24 h ≈ 0 k$, écart -93,3 % |
| 342 | Snorter | SNORT | retirer | prévente de bot de trading Telegram (Snorter) | commune* | — | mort | ≈ 22 M$ (estimé CG) | CoinGecko `snorter` ; cap. ≈ 690 k$, volume 24 h ≈ 0 k$, écart -96,8 % |
| 343 | The Toad Pepe | TOAD | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 22 M$ (estimé CG) | CoinGecko `the-toad-pepe` ; cap. ≈ 672 k$, volume 24 h ≈ 378 k$, écart -97,0 % |
| 344 | Tsuki | TSUKI | garder |  | commune* | rare | en déclin | ≈ 24 M$ (estimé CG) | CoinGecko `tsuki` ; cap. ≈ 2,4 M$, volume 24 h ≈ 44 k$, écart -90,1 % |
| 345 | Windoge98 | EXE | garder |  | commune* | rare | mort | ≈ 24 M$ (estimé CG) | CoinGecko `windoge98` ; cap. ≈ 726 k$, volume 24 h ≈ 1 k$, écart -97,0 % |
| 346 | Freedom of Money | FREEDOM OF MONEY | garder |  | commune* | rare | en déclin | ≈ 22 M$ (estimé CG) | CoinGecko `freedom-of-money` ; cap. ≈ 1,3 M$, volume 24 h ≈ 50 k$, écart -94,1 % |
| 347 | Icy | IC | garder |  | commune* | rare | en déclin | ≈ 21 M$ (estimé CG) | CoinGecko `icy` ; cap. ≈ 1,1 M$, volume 24 h ≈ 0 k$, écart -94,8 % |
| 348 | NEFE COIN | NEFE | garder |  | commune* | rare | actif | ≈ 22 M$ (estimé CG) | CoinGecko `nefe-coin` ; cap. ≈ 17 M$, volume 24 h ≈ 0 k$, écart -22,1 % |
| 349 | The Bitcoin Mascot | BITTY | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 20 M$ (estimé CG) | CoinGecko `the-bitcoin-mascot` ; cap. ≈ 925 k$, volume 24 h ≈ 39 k$, écart -95,4 % |
| 350 | CROCAT | CROCAT | garder |  | commune* | rare | en déclin | ≈ 21 M$ (estimé CG) | CoinGecko `crocat` ; cap. ≈ 2,5 M$, volume 24 h ≈ 10 k$, écart -88,3 % |
| 351 | DROP | DROP | garder |  | commune* | rare | en déclin | ≈ 20 M$ (estimé CG) | CoinGecko `drop-2` ; cap. ≈ 2,3 M$, volume 24 h ≈ 13 k$, écart -88,4 % |
| 352 | Pundu | PUNDU | garder |  | commune* | rare | en déclin | ≈ 20 M$ (estimé CG) | CoinGecko `pundu` ; cap. ≈ 1,9 M$, volume 24 h ≈ 0 k$, écart -90,7 % |
| 353 | The Juggernaut | JUGGERNAUT | garder |  | commune* | rare | en déclin | ≈ 21 M$ (estimé CG) | CoinGecko `the-juggernaut` ; cap. ≈ 2,3 M$, volume 24 h ≈ 1,1 M$, écart -89,4 % |
| 354 | The Last Play | RETIRE | garder |  | commune* | rare | en déclin | ≈ 20 M$ (estimé CG) | CoinGecko `the-last-play` ; cap. ≈ 2,2 M$, volume 24 h ≈ 312 k$, écart -89,3 % |
| 355 | CRONUS | CRONUS | garder |  | commune* | rare | en déclin | ≈ 20 M$ (estimé CG) | CoinGecko `cronus-2` ; cap. ≈ 3,9 M$, volume 24 h ≈ 6 k$, écart -80,4 % |
| 356 | memestock | MEMESTOCK | garder |  | commune* | rare | en déclin | ≈ 18 M$ (estimé CG) | CoinGecko `memestock-3` ; cap. ≈ 1,1 M$, volume 24 h ≈ 25 k$, écart -94,0 % |
| 357 | Strategic Super Reserve | SSR | garder |  | commune* | rare | mort | ≈ 17 M$ (estimé CG) | CoinGecko `strategic-solana-reserve` ; cap. ≈ 536 k$, volume 24 h ≈ 1 k$, écart -96,8 % |
| 358 | Wolfi | WOLFI | garder |  | commune | rare | mort | ≈ 20 M$ (sourcé) | CoinGecko `wolfi-2` ; catalogue (pic sourcé) ; cap. ≈ 108 k$, volume 24 h ≈ 0 k$, écart -99,4 % |
| 359 | Fish | FISH | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 19 M$ (sourcé) | catalogue (pic sourcé) |
| 360 | Morning Routine | ROUTINE | garder |  | commune | rare | mort | ≈ 19 M$ (sourcé) | CoinGecko `morning-routine` ; catalogue (pic sourcé) ; cap. ≈ 19 k$, volume 24 h ≈ 0 k$, écart -99,9 % |
| 361 | Rain Coin | RAIN | garder |  | commune* | rare | en déclin | ≈ 18 M$ (estimé CG) | CoinGecko `rain-coin` ; cap. ≈ 2,7 M$, volume 24 h ≈ 8 k$, écart -85,0 % |
| 362 | 金蝶圣甲 (Golden Butterfly Sacred Armor) | 金蝶圣甲 | garder |  | commune* | rare | en déclin | ≈ 20 M$ (estimé CG) | CoinGecko `golden-butterfly-sacred-armor` ; cap. ≈ 2,8 M$, volume 24 h ≈ 26 k$, écart -85,7 % |
| 363 | Cryptocurrency Coin | CRYPTO | garder |  | commune* | rare | en déclin | ≈ 19 M$ (estimé CG) | CoinGecko `cryptocurrency-coin` ; cap. ≈ 2,2 M$, volume 24 h ≈ 7 k$, écart -88,7 % |
| 364 | GLORP | GLORP | garder |  | commune | rare | mort | ≈ 18 M$ (sourcé) | CoinGecko `glorp` ; catalogue (pic sourcé) ; cap. ≈ 106 k$, volume 24 h ≈ 1 k$, écart -99,4 % |
| 365 | JOBCOIN | JOBCOIN | garder |  | commune* | rare | actif | ≈ 18 M$ (estimé CG) | CoinGecko `jobcoin-2` ; cap. ≈ 4,5 M$, volume 24 h ≈ 30 k$, écart -75,1 % |
| 366 | Xavier: Renegade Angel | XAVIER | garder |  | commune* | rare | en déclin | ≈ 19 M$ (estimé CG) | CoinGecko `xavier-renegade-angel` ; cap. ≈ 1,1 M$, volume 24 h ≈ 5 k$, écart -94,4 % |
| 367 | AAA Cat | AAA | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 17 M$ (sourcé) | catalogue (pic sourcé) |
| 368 | Hoppy | HOPPY | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 142 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `hoppy-meme` ; cap. ≈ 959 k$, volume 24 h ≈ 40 k$, écart -99,3 % |
| 369 | frong | FRONG | garder |  | commune* | rare | en déclin | ≈ 16 M$ (estimé CG) | CoinGecko `frong` ; cap. ≈ 1,6 M$, volume 24 h ≈ 91 k$, écart -90,6 % |
| 370 | LUCKY | LUCKY | garder |  | commune* | rare | en déclin | ≈ 15 M$ (estimé CG) | CoinGecko `lucky` ; cap. ≈ 1,5 M$, volume 24 h ≈ 48 k$, écart -89,9 % |
| 371 | NearKat | NEARKAT | garder |  | commune* | rare | mort | ≈ 17 M$ (estimé CG) | CoinGecko `nearkat-2` ; cap. ≈ 713 k$, volume 24 h ≈ 3 k$, écart -95,7 % |
| 372 | Real World AI | RWA | garder |  | commune* | rare | en déclin | ≈ 15 M$ (estimé CG) | CoinGecko `real-world-ai` ; cap. ≈ 1,4 M$, volume 24 h ≈ 9 k$, écart -90,4 % |
| 373 | V2EX | V2EX | garder |  | commune* | rare | en déclin | ≈ 16 M$ (estimé CG) | CoinGecko `v2ex` ; cap. ≈ 1,9 M$, volume 24 h ≈ 1 k$, écart -87,8 % |
| 374 | ATEHUN | ATEHUN | garder |  | commune* | rare | mort | ≈ 13 M$ (estimé CG) | CoinGecko `atehun` ; cap. ≈ 568 k$, volume 24 h ≈ 1 k$, écart -95,8 % |
| 375 | Bitcoin on Base | BTCB | garder |  | commune* | rare | mort | ≈ 15 M$ (estimé CG) | CoinGecko `bitcoin-on-base` ; cap. ≈ 578 k$, volume 24 h ≈ 1 k$, écart -96,2 % |
| 376 | BullDogito | BDOGITO | garder |  | commune* | rare | mort | ≈ 17 M$ (estimé CG) | CoinGecko `bulldogito` ; cap. ≈ 582 k$, volume 24 h ≈ 1 k$, écart -96,5 % |
| 378 | GOATED | GOATED | garder |  | commune* | rare | actif | ≈ 15 M$ (estimé CG) | CoinGecko `goated-2` ; cap. ≈ 3,5 M$, volume 24 h ≈ 0 k$, écart -77,1 % — même ticker que GOAT Network (GOATED), retiré en annexe 1 : vérifier l'identité |
| 379 | Loaf Token | LOAF | garder |  | commune* | rare | en déclin | ≈ 15 M$ (estimé CG) | CoinGecko `loaf-token` ; cap. ≈ 1,7 M$, volume 24 h ≈ 0 k$, écart -88,5 % |
| 381 | The Original Doge | OGDOGE | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 14 M$ (estimé CG) | CoinGecko `the-original-doge` ; cap. ≈ 566 k$, volume 24 h ≈ 83 k$, écart -96,0 % |
| 382 | DEBT | DEBT | garder |  | commune | rare | mort | ≈ 15 M$ (sourcé) | CoinGecko `debt` ; catalogue (pic sourcé) ; cap. ≈ 40 k$, volume 24 h ≈ 0 k$, écart -67,9 % |
| 383 | Barking Puppy | BP | garder |  | commune* | rare | en déclin | ≈ 14 M$ (estimé CG) | CoinGecko `barking-puppy` ; cap. ≈ 1,5 M$, volume 24 h ≈ 55 k$, écart -89,0 % |
| 384 | Jean Phil | JEANPHIL | garder |  | commune* | rare | actif | ≈ 15 M$ (estimé CG) | CoinGecko `jean-phil` ; cap. ≈ 3,2 M$, volume 24 h ≈ 995 k$, écart -78,5 % |
| 385 | Jotchua | JOTCHUA | garder |  | commune* | rare | en déclin | ≈ 14 M$ (estimé CG) | CoinGecko `jotchua` ; cap. ≈ 1,8 M$, volume 24 h ≈ 889 k$, écart -87,0 % |
| 386 | Stairway to gold | GOLD | garder |  | commune* | rare | actif | ≈ 14 M$ (estimé CG) | CoinGecko `stairway-to-gold` ; cap. ≈ 10 M$, volume 24 h ≈ 12 k$, écart -28,4 % |
| 387 | SZN | SZN | garder |  | commune | rare | mort | ≈ 14 M$ (sourcé) | CoinGecko `szn` ; catalogue (pic sourcé) ; cap. ≈ 67 k$, volume 24 h ≈ 0 k$, écart -99,2 % |
| 388 | Z李REAL SUPER COIN | ZREAL | garder |  | commune* | rare | en déclin | ≈ 13 M$ (estimé CG) | CoinGecko `zreal-super-coin` ; cap. ≈ 1,3 M$, volume 24 h ≈ 4 k$, écart -90,6 % |
| 389 | 1000PEPPER | 1000PEPPER | garder |  | commune* | rare | actif | ≈ 13 M$ (estimé CG) | CoinGecko `1000pepper` ; cap. ≈ 4,1 M$, volume 24 h ≈ 202 k$, écart -68,8 % |
| 390 | ALD | ALD | garder |  | commune* | rare | actif | ≈ 13 M$ (estimé CG) | CoinGecko `ald` ; cap. ≈ 4,6 M$, volume 24 h ≈ 216 k$, écart -64,2 % |
| 391 | BEARXRPL | BEAR | garder |  | commune* | rare | en déclin | ≈ 13 M$ (estimé CG) | CoinGecko `bearxrpl` ; cap. ≈ 1,3 M$, volume 24 h ≈ 5 k$, écart -89,4 % |
| 392 | GongFu | GF | garder |  | commune* | rare | en déclin | ≈ 13 M$ (estimé CG) | CoinGecko `gongfu` ; cap. ≈ 2,1 M$, volume 24 h ≈ 1 k$, écart -84,4 % |
| 393 | Strategy Coin | STRATEGY | garder |  | commune* | rare | en déclin | ≈ 12 M$ (estimé CG) | CoinGecko `strategy-coin` ; cap. ≈ 1,9 M$, volume 24 h ≈ 12 k$, écart -84,6 % |
| 394 | World Cup Coin | à vérifier | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 12 M$ (sourcé) | catalogue (pic sourcé) |
| 395 | ALLINDOGE | ALLINDOGE | garder |  | commune* | rare | en déclin | ≈ 13 M$ (estimé CG) | CoinGecko `allindoge` ; cap. ≈ 1,7 M$, volume 24 h ≈ 19 k$, écart -86,5 % |
| 396 | BORED | BORED | garder |  | commune* | rare | en déclin | ≈ 13 M$ (estimé CG) | CoinGecko `edison-bored` ; cap. ≈ 1,5 M$, volume 24 h ≈ 0 k$, écart -88,4 % |
| 397 | Defi Tiger | DTG | garder |  | commune* | rare | mort | ≈ 12 M$ (estimé CG) | CoinGecko `defi-tiger` ; cap. ≈ 589 k$, volume 24 h ≈ 1 k$, écart -95,2 % |
| 398 | dopameme | DOPAMEME | garder |  | commune* | rare | en déclin | ≈ 12 M$ (estimé CG) | CoinGecko `dopameme-2` ; cap. ≈ 669 k$, volume 24 h ≈ 24 k$, écart -94,3 % |
| 399 | LOULOU | LOULOU | garder |  | commune* | rare | en déclin | ≈ 11 M$ (estimé CG) | CoinGecko `loulou` ; cap. ≈ 1,3 M$, volume 24 h ≈ 2 k$, écart -88,7 % |
| 400 | MoonDog AI | MDOGAI | garder |  | commune* | rare | mort | ≈ 14 M$ (estimé CG) | CoinGecko `moondog-ai` ; cap. ≈ 522 k$, volume 24 h ≈ 0 k$, écart -96,3 % |
| 401 | PEPECASH | PECH | garder |  | commune* | rare | mort | ≈ 11 M$ (estimé CG) | CoinGecko `pepecash-3` ; cap. ≈ 562 k$, volume 24 h ≈ 0 k$, écart -94,7 % — à distinguer de Rare Pepe Cash (n° 724) |
| 402 | PEPECAT | PEPECAT | garder |  | commune* | rare | actif | ≈ 12 M$ (estimé CG) | CoinGecko `pepecat-2` ; cap. ≈ 5,7 M$, volume 24 h ≈ 31 k$, écart -51,1 % |
| 403 | SCHIFFY | SCHIFFY | garder |  | commune* | rare | en déclin | ≈ 13 M$ (estimé CG) | CoinGecko `schiffy` ; cap. ≈ 2,1 M$, volume 24 h ≈ 699 k$, écart -83,1 % |
| 404 | vankedisi | VANKEDISI | garder |  | commune* | rare | mort | ≈ 12 M$ (estimé CG) | CoinGecko `vankedisi` ; cap. ≈ 703 k$, volume 24 h ≈ 0 k$, écart -93,9 % |
| 406 | Claudia | CLAUDIA | garder |  | commune* | rare | actif | ≈ 11 M$ (estimé CG) | CoinGecko `claudia-2` ; cap. ≈ 4,9 M$, volume 24 h ≈ 2,9 M$, écart -56,6 % |
| 407 | FATCAT | FATCAT | garder |  | commune* | rare | actif | ≈ 11 M$ (estimé CG) | CoinGecko `fatcat-4` ; cap. ≈ 3,4 M$, volume 24 h ≈ 94 k$, écart -69,6 % |
| 408 | MEMENTO•MORI | MEMENTO | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 11 M$ (sourcé) | catalogue (pic sourcé) |
| 409 | WolfSafePoorPeople | WSPP | garder |  | commune* | rare | actif | ≈ 11 M$ (estimé CG) | CoinGecko `wolfsafepoorpeople` ; cap. ≈ 3,3 M$, volume 24 h ≈ 5 k$, écart -69,0 % |
| 410 | ༼ つ ◕_◕ ༽つ | GIB | garder |  | commune* | rare | en déclin | ≈ 12 M$ (estimé CG) | CoinGecko `_` ; cap. ≈ 1,7 M$, volume 24 h ≈ 3 k$, écart -86,3 % |
| 411 | Suncat | SUNCAT | garder |  | commune | rare | mort | ≈ 24 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `suncat` ; cap. ≈ 197 k$, volume 24 h ≈ 0 k$, écart -99,2 % |
| 412 | The Doge NFT / Own The Doge | DOG | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 575 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `the-doge-nft` ; cap. ≈ 5,3 M$, volume 24 h ≈ 12 k$, écart -99,1 % |
| 413 | Froth | FROTH | garder |  | commune* | rare | mort | ≈ 10 M$ (estimé CG) | CoinGecko `froth` ; cap. ≈ 600 k$, volume 24 h ≈ 0 k$, écart -94,2 % |
| 414 | Official PPshow | PP | garder |  | commune* | commune | mort | ≈ 9,9 M$ (estimé CG) | CoinGecko `official-ppshow` ; cap. ≈ 728 k$, volume 24 h ≈ 4 k$, écart -92,6 % |
| 415 | RONKE | RONKE | garder |  | commune* | commune | mort | ≈ 9,5 M$ (estimé CG) | CoinGecko `ronke` ; cap. ≈ 811 k$, volume 24 h ≈ 13 k$, écart -91,4 % |
| 416 | what the hook? | WTH | garder |  | commune* | rare | actif | ≈ 10 M$ (estimé CG) | CoinGecko `what-the-hook` ; cap. ≈ 4,4 M$, volume 24 h ≈ 179 k$, écart -56,2 % |
| 417 | 中国人能飞火箭 | 中国人能飞 | garder |  | commune* | rare | en déclin | ≈ 10 M$ (estimé CG) | CoinGecko `zhong-guo-ren-neng-fei` ; cap. ≈ 1,4 M$, volume 24 h ≈ 1,2 M$, écart -86,4 % |
| 418 | GameCow | GCOW | garder |  | commune* | commune | actif | ≈ 9,8 M$ (estimé CG) | CoinGecko `gamecow` ; cap. ≈ 2,6 M$, volume 24 h ≈ 13 k$, écart -72,9 % |
| 419 | Commander Vrax | VRAX | garder |  | commune* | commune | actif | ≈ 9,4 M$ (estimé CG) | CoinGecko `commander-vrax-2` ; cap. ≈ 2,8 M$, volume 24 h ≈ 1,4 M$, écart -70,0 % |
| 420 | ANITA | ANITA | garder |  | commune* | commune | en déclin | ≈ 8,8 M$ (estimé CG) | CoinGecko `anita` ; cap. ≈ 1,2 M$, volume 24 h ≈ 17 k$, écart -86,4 % |
| 421 | DITGOLD | DITAU | garder |  | commune* | commune | actif | ≈ 9,1 M$ (estimé CG) | CoinGecko `ditgold` ; cap. ≈ 5,0 M$, volume 24 h ≈ 101 k$, écart -45,5 % |
| 422 | Miu | MIU | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 135 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `miu-2` ; cap. ≈ 1,0 M$, volume 24 h ≈ 46 k$, écart -99,2 % |
| 424 | SHIBA ON BASE | SHIB | garder |  | commune* | commune | mort | ≈ 8,9 M$ (estimé CG) | CoinGecko `shiba-on-base` ; cap. ≈ 716 k$, volume 24 h ≈ 2 k$, écart -92,0 % |
| 425 | WIN界 | WIN界 | garder |  | commune* | commune | actif | ≈ 8,6 M$ (estimé CG) | CoinGecko `win-jie` ; cap. ≈ 2,9 M$, volume 24 h ≈ 32 k$, écart -66,9 % |
| 426 | PsyopAnime | PSYOPANIME | garder |  | commune* | commune | en déclin | ≈ 9,8 M$ (estimé CG) | CoinGecko `psyopanime` ; cap. ≈ 619 k$, volume 24 h ≈ 54 k$, écart -93,7 % |
| 427 | GREEN MORNING | GM | garder |  | commune* | commune | à vérifier (homonyme sur CoinGecko, non rapproché) | inconnu | catalogue ; absent du relevé |
| 428 | Zen AI | ZAI | garder |  | commune* | commune | actif | ≈ 8,3 M$ (estimé CG) | CoinGecko `zen-ai` ; cap. ≈ 2,4 M$, volume 24 h ≈ 20 k$, écart -71,1 % |
| 429 | DOUBT | DOUBT | garder |  | commune* | commune | en déclin | ≈ 8,6 M$ (estimé CG) | CoinGecko `doubt` ; cap. ≈ 1,3 M$, volume 24 h ≈ 3 k$, écart -84,6 % |
| 430 | MemeFi | MEMEFI | retirer | tap-to-earn (MemeFi) | commune | — | mort | ≈ 138 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `memefi-2` ; cap. ≈ 442 k$, volume 24 h ≈ 0 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 431 | RALPH | RALPH | garder |  | commune | commune | mort (absent de CoinGecko) | ≈ 7,8 M$ (sourcé) | catalogue (pic sourcé) |
| 432 | Perpetual Bitcoin | PB | garder |  | commune* | commune | actif | ≈ 7,9 M$ (estimé CG) | CoinGecko `perpetual-bitcoin` ; cap. ≈ 4,7 M$, volume 24 h ≈ 0 k$, écart -40,5 % |
| 433 | PETRO PENGUINS | PENGO | garder |  | commune* | commune | mort | ≈ 7,7 M$ (estimé CG) | CoinGecko `petro-penguins` ; cap. ≈ 757 k$, volume 24 h ≈ 19 k$, écart -90,2 % |
| 434 | The Final Form Bull | CZ | garder |  | commune* | commune | en déclin | ≈ 7,3 M$ (estimé CG) | CoinGecko `the-final-form-bull` ; cap. ≈ 1,3 M$, volume 24 h ≈ 675 k$, écart -82,3 % |
| 435 | Market Dominance | MD | garder |  | commune* | commune | mort | ≈ 7,3 M$ (estimé CG) | CoinGecko `market-dominance` ; cap. ≈ 528 k$, volume 24 h ≈ 1 k$, écart -92,7 % |
| 436 | Harmonic Agent | HARMONIC | garder |  | commune* | commune | en déclin | ≈ 7,2 M$ (estimé CG) | CoinGecko `harmonic-agent` ; cap. ≈ 1,3 M$, volume 24 h ≈ 46 k$, écart -81,9 % |
| 437 | DogWifJob | JOB | garder |  | commune* | commune | actif | ≈ 7,0 M$ (estimé CG) | CoinGecko `dogwifjob` ; cap. ≈ 2,4 M$, volume 24 h ≈ 932 k$, écart -65,2 % |
| 438 | RONIN | RONIN | garder |  | commune* | commune | en déclin | ≈ 7,0 M$ (estimé CG) | CoinGecko `ronin-2` ; cap. ≈ 1,0 M$, volume 24 h ≈ 2 k$, écart -85,4 % |
| 439 | Baby 4 | BABY4 | garder |  | commune* | commune | mort | ≈ 6,2 M$ (estimé CG) | CoinGecko `baby-4` ; cap. ≈ 552 k$, volume 24 h ≈ 0 k$, écart -91,0 % |
| 440 | Greatest Meme Ever | GME | garder |  | commune* | commune | en déclin | ≈ 6,7 M$ (estimé CG) | CoinGecko `greatest-meme-ever` ; cap. ≈ 482 k$, volume 24 h ≈ 50 k$, écart -92,8 % |
| 441 | Rage Guy | RAGEGUY | garder |  | commune* | commune | actif | ≈ 6,5 M$ (estimé CG) | CoinGecko `rage-guy` ; cap. ≈ 2,6 M$, volume 24 h ≈ 36 k$, écart -60,4 % |
| 442 | BabyBonk | BABYBONK | garder |  | commune* | commune | mort | ≈ 6,9 M$ (estimé CG) | CoinGecko `babybonk-3` ; cap. ≈ 733 k$, volume 24 h ≈ 1 k$, écart -89,3 % |
| 443 | BNB Frog Inu | BNBFROG | garder |  | commune* | commune | mort | ≈ 6,3 M$ (estimé CG) | CoinGecko `bnb-frog-inu` ; cap. ≈ 686 k$, volume 24 h ≈ 1 k$, écart -89,2 % |
| 444 | BNB Tiger Inu | BNBTIGER | garder |  | commune* | commune | actif | ≈ 6,1 M$ (estimé CG) | CoinGecko `bnb-tiger-inu` ; cap. ≈ 1,4 M$, volume 24 h ≈ 1 k$, écart -77,7 % |
| 445 | Oh no | OHNO | garder |  | commune* | commune | mort | ≈ 6,6 M$ (estimé CG) | CoinGecko `oh-no` ; cap. ≈ 705 k$, volume 24 h ≈ 0 k$, écart -89,4 % |
| 446 | Unicorn Meat | W🍖 | garder |  | commune* | commune | mort | ≈ 5,9 M$ (estimé CG) | CoinGecko `unicorn-meat` ; cap. ≈ 608 k$, volume 24 h ≈ 0 k$, écart -89,8 % |
| 447 | Vibing Cat Coin | VIBECOIN | garder |  | commune* | commune | actif | ≈ 6,3 M$ (estimé CG) | CoinGecko `vibing-cat-coin` ; cap. ≈ 1,7 M$, volume 24 h ≈ 8 k$, écart -73,2 % |
| 448 | HODL | HODL | garder |  | commune* | commune | actif | ≈ 6,0 M$ (estimé CG) | CoinGecko `hodl-7` ; cap. ≈ 4,2 M$, volume 24 h ≈ 1,4 M$, écart -29,0 % |
| 449 | Choo Choo | CHOO | garder |  | commune* | commune | actif | ≈ 6,0 M$ (estimé CG) | CoinGecko `choo-choo` ; cap. ≈ 1,3 M$, volume 24 h ≈ 1,2 M$, écart -78,9 % |
| 450 | MOTION | MOTION | garder |  | commune* | commune | mort | ≈ 5,7 M$ (estimé CG) | CoinGecko `motion-6` ; cap. ≈ 601 k$, volume 24 h ≈ 0 k$, écart -89,5 % |
| 451 | Zeal | ZEAL | garder |  | commune* | commune | mort | ≈ 6,0 M$ (estimé CG) | CoinGecko `zeal-2` ; cap. ≈ 577 k$, volume 24 h ≈ 16 k$, écart -90,3 % |
| 452 | OciCat Token | OCICAT | garder |  | commune* | commune | mort | ≈ 6,0 M$ (estimé CG) | CoinGecko `ocicat-token` ; cap. ≈ 723 k$, volume 24 h ≈ 1 k$, écart -88,0 % |
| 453 | Yunai by Virtuals | YUNAI | retirer | agent IA sur Virtuals (Yunai by Virtuals) | commune* | — | actif | ≈ 5,6 M$ (estimé CG) | CoinGecko `yunai` ; cap. ≈ 1,3 M$, volume 24 h ≈ 0 k$, écart -76,5 % |
| 454 | NianNian | 年年 | garder |  | commune* | commune | actif | ≈ 5,7 M$ (estimé CG) | CoinGecko `niannian-2` ; cap. ≈ 1,3 M$, volume 24 h ≈ 122 k$, écart -78,1 % |
| 455 | WHISKEY | WHISKEY | garder |  | commune* | commune | actif | ≈ 5,5 M$ (estimé CG) | CoinGecko `whiskey` ; cap. ≈ 1,1 M$, volume 24 h ≈ 1 k$, écart -79,7 % |
| 456 | Whyyoutouzhele | LI | garder |  | commune* | commune | mort | ≈ 5,4 M$ (estimé CG) | CoinGecko `whyyoutouzhele` ; cap. ≈ 513 k$, volume 24 h ≈ 0 k$, écart -90,5 % |
| 457 | OFFICIAL K-POP | KPOP | garder |  | commune* | commune | mort | ≈ 5,7 M$ (estimé CG) | CoinGecko `official-k-pop` ; cap. ≈ 621 k$, volume 24 h ≈ 1 k$, écart -89,0 % |
| 458 | WHALE | WHALE | garder |  | commune* | commune | actif | ≈ 5,3 M$ (estimé CG) | CoinGecko `whale-4` ; cap. ≈ 3,0 M$, volume 24 h ≈ 240 k$, écart -44,2 % |
| 459 | Anthropig | ANTHROPIG | garder |  | commune* | commune | actif | ≈ 5,3 M$ (estimé CG) | CoinGecko `anthropig` ; cap. ≈ 2,5 M$, volume 24 h ≈ 0 k$, écart -52,5 % |
| 460 | Buttcoin | BUTTCOIN | garder |  | commune | rare | en déclin | ≈ 49 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `buttcoin-7` ; cap. ≈ 5,5 M$, volume 24 h ≈ 655 k$, écart -88,8 % |
| 461 | cat wif sword | SWORDCAT | garder |  | commune* | commune | en déclin | ≈ 5,6 M$ (estimé CG) | CoinGecko `cat-wif-sword-2` ; cap. ≈ 748 k$, volume 24 h ≈ 239 k$, écart -86,6 % |
| 462 | Anoncoin | ANONCOIN | garder |  | commune* | commune | actif | ≈ 5,0 M$ (estimé CG) | CoinGecko `anoncoin-2` ; cap. ≈ 1,8 M$, volume 24 h ≈ 19 k$, écart -64,5 % |
| 463 | Hachiko Inu | HACHIKO | garder |  | commune* | commune | en déclin | ≈ 4,8 M$ (estimé CG) | CoinGecko `hachiko-inu-2` ; cap. ≈ 682 k$, volume 24 h ≈ 41 k$, écart -85,7 % |
| 464 | LOXI | LOXI | garder |  | commune* | commune | mort | ≈ 5,4 M$ (estimé CG) | CoinGecko `loxi-2` ; cap. ≈ 722 k$, volume 24 h ≈ 0 k$, écart -86,5 % |
| 466 | FEFER | FEFER | garder |  | commune* | commune | actif | ≈ 4,7 M$ (estimé CG) | CoinGecko `fefer-2` ; cap. ≈ 1,6 M$, volume 24 h ≈ 0 k$, écart -65,6 % |
| 467 | Wolfies | PACK | garder |  | commune* | commune | mort | ≈ 4,9 M$ (estimé CG) | CoinGecko `moonflow-2` ; cap. ≈ 738 k$, volume 24 h ≈ 9 k$, écart -84,9 % |
| 468 | saucecoin | SAUCE | garder |  | commune* | commune | actif | ≈ 4,7 M$ (estimé CG) | CoinGecko `saucecoin` ; cap. ≈ 3,8 M$, volume 24 h ≈ 103 k$, écart -18,8 % |
| 469 | Cartoon Money | CBUCKS | garder |  | commune* | commune | actif | ≈ 5,9 M$ (estimé CG) | CoinGecko `cartoon-money` ; cap. ≈ 5,1 M$, volume 24 h ≈ 670 k$, écart -13,9 % |
| 470 | Infinite Money Glitch | GLITCH | garder |  | commune* | commune | actif | ≈ 4,6 M$ (estimé CG) | CoinGecko `infinite-money-glitch-3` ; cap. ≈ 2,2 M$, volume 24 h ≈ 347 k$, écart -51,2 % |
| 471 | Marvin | MARVIN | garder |  | commune* | commune | actif | ≈ 4,5 M$ (estimé CG) | CoinGecko `marvin-3` ; cap. ≈ 1,4 M$, volume 24 h ≈ 11 k$, écart -68,6 % |
| 472 | NASDANQ | NASDANQ | garder |  | commune* | commune | mort | ≈ 4,6 M$ (estimé CG) | CoinGecko `nasdanq` ; cap. ≈ 400 k$, volume 24 h ≈ 10 k$, écart -91,3 % |
| 473 | AudaCity | DACITYCOIN | garder |  | commune* | commune | actif | ≈ 4,4 M$ (estimé CG) | CoinGecko `audacity` ; cap. ≈ 2,4 M$, volume 24 h ≈ 4,0 M$, écart -45,2 % — doublon possible de n° 321 Dacity Coin |
| 474 | Dog With Purpose | DOPU | garder |  | commune* | commune | actif | ≈ 4,5 M$ (estimé CG) | CoinGecko `dog-with-purpose` ; cap. ≈ 1,2 M$, volume 24 h ≈ 133 k$, écart -74,0 % |
| 475 | Doge Pepe | DOPE | garder |  | commune* | commune | actif | ≈ 4,7 M$ (estimé CG) | CoinGecko `doge-pepe-4` ; cap. ≈ 1,1 M$, volume 24 h ≈ 434 k$, écart -77,2 % |
| 476 | Zhao Cai Mao | 招财猫 | garder |  | commune* | commune | actif | ≈ 4,4 M$ (estimé CG) | CoinGecko `zhao-cai-mao` ; cap. ≈ 2,2 M$, volume 24 h ≈ 64 k$, écart -50,0 % |
| 477 | Scamcoin | SCAM | garder |  | commune* | commune | actif | ≈ 4,3 M$ (estimé CG) | CoinGecko `scamcoin` ; cap. ≈ 2,7 M$, volume 24 h ≈ 25 k$, écart -36,8 % |
| 478 | ClipX | CLIPX | garder |  | commune* | commune | en déclin | ≈ 4,4 M$ (estimé CG) | CoinGecko `klipx-x-tips` ; cap. ≈ 525 k$, volume 24 h ≈ 34 k$, écart -88,1 % |
| 479 | Optimus | OPTIMUS | garder |  | commune* | commune | actif | ≈ 4,3 M$ (estimé CG) | CoinGecko `optimus-2` ; cap. ≈ 1,5 M$, volume 24 h ≈ 17 k$, écart -65,6 % |
| 480 | World is Flat | WIF | garder |  | commune* | commune | actif | ≈ 4,1 M$ (estimé CG) | CoinGecko `world-is-flat` ; cap. ≈ 1,3 M$, volume 24 h ≈ 96 k$, écart -67,9 % |
| 481 | Chameleon | CHAMELEON | garder |  | commune | commune | mort | ≈ 4,0 M$ (sourcé) | CoinGecko `chameleon` ; catalogue (pic sourcé) ; cap. ≈ 126 k$, volume 24 h ≈ 4 k$, écart -97,4 % |
| 482 | Energy | $NRG | garder |  | commune* | commune | actif | ≈ 4,1 M$ (estimé CG) | CoinGecko `energy-2` ; cap. ≈ 1,2 M$, volume 24 h ≈ 4 k$, écart -70,3 % |
| 483 | Panana | $PANANA | garder |  | commune* | commune | mort | ≈ 4,0 M$ (estimé CG) | CoinGecko `panana` ; cap. ≈ 791 k$, volume 24 h ≈ 0 k$, écart -80,1 % |
| 484 | THAT | THAT | garder |  | commune* | commune | actif | ≈ 4,0 M$ (estimé CG) | CoinGecko `that` ; cap. ≈ 3,7 M$, volume 24 h ≈ 17 k$, écart -7,8 % |
| 485 | one life, its worth an attempt | WORTH | garder |  | commune* | commune | mort | ≈ 4,0 M$ (estimé CG) | CoinGecko `one-life-its-worth-an-attempt-2` ; cap. ≈ 546 k$, volume 24 h ≈ 2 k$, écart -86,4 % |
| 486 | CeramicLiberty.com | CL8Y | garder |  | commune* | commune | actif | ≈ 3,8 M$ (estimé CG) | CoinGecko `ceramicliberty-com` ; cap. ≈ 1,4 M$, volume 24 h ≈ 0 k$, écart -62,8 % |
| 487 | Beast | BEAST | garder |  | commune* | commune | actif | ≈ 3,6 M$ (estimé CG) | CoinGecko `beast` ; cap. ≈ 958 k$, volume 24 h ≈ 34 k$, écart -73,4 % |
| 488 | Black Dragon | BLACKDRAGON | garder |  | commune | rare | mort | ≈ 11 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `black-dragon` ; cap. ≈ 503 k$, volume 24 h ≈ 2 k$, écart -95,5 % |
| 489 | Spacebucks | SBX | garder |  | commune* | commune | mort | ≈ 3,2 M$ (estimé CG) | CoinGecko `spacebucks` ; cap. ≈ 643 k$, volume 24 h ≈ 0 k$, écart -80,2 % |
| 490 | daCat | DACAT | garder |  | commune* | commune | actif | ≈ 3,3 M$ (estimé CG) | CoinGecko `dacat` ; cap. ≈ 1,2 M$, volume 24 h ≈ 0 k$, écart -64,9 % |
| 491 | CRYPTO CLOUD | CLOUD | garder |  | commune* | commune | mort | ≈ 3,4 M$ (estimé CG) | CoinGecko `crypto-clouds` ; cap. ≈ 548 k$, volume 24 h ≈ 0 k$, écart -83,8 % |
| 492 | tomochi | TOMOCHI | garder |  | commune* | commune | mort | ≈ 3,5 M$ (estimé CG) | CoinGecko `tomochi` ; cap. ≈ 492 k$, volume 24 h ≈ 2 k$, écart -85,9 % |
| 493 | UNIVERSE | UNIVERSE | garder |  | commune* | commune | actif | ≈ 3,2 M$ (estimé CG) | CoinGecko `universe-3` ; cap. ≈ 2,7 M$, volume 24 h ≈ 0 k$, écart -17,0 % |
| 494 | Bluzo | BLZ | garder |  | commune* | commune | actif | ≈ 3,2 M$ (estimé CG) | CoinGecko `bluzo` ; cap. ≈ 2,1 M$, volume 24 h ≈ 0 k$, écart -34,9 % |
| 495 | Frogonsol | FROG | garder |  | commune* | commune | mort | ≈ 3,2 M$ (estimé CG) | CoinGecko `frogonsol` ; cap. ≈ 596 k$, volume 24 h ≈ 0 k$, écart -81,4 % |
| 496 | MIZU KAPPA | MIZU | garder |  | commune* | commune | actif | ≈ 3,1 M$ (estimé CG) | CoinGecko `mizu-kappa` ; cap. ≈ 1,6 M$, volume 24 h ≈ 1 k$, écart -49,9 % |
| 497 | zuzalu | ZUZALU | garder |  | commune* | commune | actif | ≈ 3,3 M$ (estimé CG) | CoinGecko `zuzalu` ; cap. ≈ 1,1 M$, volume 24 h ≈ 34 k$, écart -66,3 % |
| 498 | AVAX Has No Chill | NOCHILL | garder |  | commune | rare | mort | ≈ 48 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `avax-has-no-chill` ; cap. ≈ 409 k$, volume 24 h ≈ 0 k$, écart -99,2 % |
| 499 | Nads | NADS | garder |  | commune | commune | mort | ≈ 3,0 M$ (sourcé) | CoinGecko `nads` ; catalogue (pic sourcé) ; cap. ≈ 35 k$, volume 24 h ≈ 0 k$, écart -90,6 % |
| 500 | Crobinhood | CROBINHOOD | garder |  | commune* | commune | actif | ≈ 2,9 M$ (estimé CG) | CoinGecko `crobinhood` ; cap. ≈ 1,1 M$, volume 24 h ≈ 25 k$, écart -63,9 % |
| 501 | DUMMY | DUMMY | garder |  | commune* | commune | mort | ≈ 3,1 M$ (estimé CG) | CoinGecko `dummy` ; cap. ≈ 531 k$, volume 24 h ≈ 0 k$, écart -83,0 % |
| 502 | Hot Cherry | à vérifier | garder |  | commune | commune | actif | ≈ 3,5 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `hot-cherry` ; cap. ≈ 1,0 M$, volume 24 h ≈ 15 k$, écart -70,8 % |
| 503 | Lonk | LONK | garder |  | commune | commune | mort | ≈ 4,9 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `lonk-on-near` ; cap. ≈ 45 k$, volume 24 h ≈ 0 k$, écart -99,1 % |
| 504 | Funds Are Safu | SAFU | garder |  | commune* | commune | actif | ≈ 2,8 M$ (estimé CG) | CoinGecko `funds-are-safu-2` ; cap. ≈ 784 k$, volume 24 h ≈ 409 k$, écart -72,1 % |
| 505 | Wobbles | WOBBLES | garder |  | commune* | commune | mort | ≈ 2,7 M$ (estimé CG) | CoinGecko `wobbles` ; cap. ≈ 825 k$, volume 24 h ≈ 2 k$, écart -69,3 % |
| 506 | 亮剑出击 | 亮剑出击 | garder |  | commune* | commune | actif | ≈ 2,5 M$ (estimé CG) | CoinGecko `liang-jian-chu-ji` ; cap. ≈ 1,7 M$, volume 24 h ≈ 6 k$, écart -32,2 % |
| 507 | BIRTHDAY | BIRTHDAY | garder |  | commune* | commune | mort | ≈ 2,4 M$ (estimé CG) | CoinGecko `birthday` ; cap. ≈ 571 k$, volume 24 h ≈ 1 k$, écart -75,9 % |
| 508 | henlo | HENLO | garder |  | commune | commune | mort | ≈ 32 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `henlo-3` ; cap. ≈ 8 k$, volume 24 h ≈ 0 k$, écart -100,0 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 509 | Hestia | HESTIA | garder |  | commune* | commune | mort | ≈ 2,2 M$ (estimé CG) | CoinGecko `hestia` ; cap. ≈ 780 k$, volume 24 h ≈ 3 k$, écart -65,0 % |
| 510 | ShibaKeanu | $SHIBK | garder |  | commune* | commune | mort | ≈ 2,2 M$ (estimé CG) | CoinGecko `shibakeanu` ; cap. ≈ 570 k$, volume 24 h ≈ 0 k$, écart -74,3 % |
| 511 | LOBIN | LOBIN | garder |  | commune* | commune | actif | ≈ 2,1 M$ (estimé CG) | CoinGecko `lobin` ; cap. ≈ 648 k$, volume 24 h ≈ 48 k$, écart -69,0 % |
| 512 | Delivery Guy | DGUY | garder |  | commune* | commune | actif | ≈ 2,0 M$ (estimé CG) | CoinGecko `delivery-guy` ; cap. ≈ 735 k$, volume 24 h ≈ 69 k$, écart -63,7 % |
| 513 | NikolAI | NIKO | garder |  | commune | rare | mort | ≈ 181 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `nikolai` ; cap. ≈ 191 k$, volume 24 h ≈ 2 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 514 | NinjaCat | NINJACAT | garder |  | commune* | commune | actif | ≈ 2,1 M$ (estimé CG) | CoinGecko `ninjacat` ; cap. ≈ 1,2 M$, volume 24 h ≈ 9 k$, écart -41,4 % |
| 515 | UltCat | ULTCAT | garder |  | commune* | commune | mort | ≈ 1,9 M$ (estimé CG) | CoinGecko `ultcat` ; cap. ≈ 598 k$, volume 24 h ≈ 7 k$, écart -69,0 % |
| 516 | DUMBMONEY | DUMBMONEY | garder |  | commune | commune | mort | ≈ 6,3 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `dumb-money-3` ; cap. ≈ 22 k$, volume 24 h ≈ 0 k$, écart -99,6 % |
| 517 | Nya | NYA | garder |  | commune | rare | en déclin | ≈ 14 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `nya` ; cap. ≈ 1,6 M$, volume 24 h ≈ 2 k$, écart -88,7 % |
| 518 | 财富人生 | 财富人生 | garder |  | commune* | commune | mort | ≈ 1,6 M$ (estimé CG) | CoinGecko `cai-fu-ren-sheng` ; cap. ≈ 714 k$, volume 24 h ≈ 5 k$, écart -55,0 % |
| 519 | Troll in Hood | TROLL | garder |  | commune* | commune | mort | ≈ 1,4 M$ (estimé CG) | CoinGecko `troll-in-hood` ; cap. ≈ 850 k$, volume 24 h ≈ 18 k$, écart -40,8 % |
| 520 | EXCELLENCE | EOP | garder |  | commune* | commune | mort | ≈ 1,4 M$ (estimé CG) | CoinGecko `president-platy` ; cap. ≈ 812 k$, volume 24 h ≈ 0 k$, écart -41,8 % |
| 521 | Illuminati | ILUM | garder |  | commune* | commune | mort | ≈ 1,4 M$ (estimé CG) | CoinGecko `illuminati` ; cap. ≈ 635 k$, volume 24 h ≈ 0 k$, écart -55,9 % |
| 522 | Dobermann | DOBERMANN | garder |  | commune* | commune | mort | ≈ 1,1 M$ (estimé CG) | CoinGecko `dobermann-2` ; cap. ≈ 784 k$, volume 24 h ≈ 7 k$, écart -28,6 % |
| 523 | GRIOT | GRIOT | garder |  | commune* | commune | mort | ≈ 1,1 M$ (estimé CG) | CoinGecko `griot` ; cap. ≈ 603 k$, volume 24 h ≈ 3 k$, écart -46,1 % |
| 524 | Jelly Finance Baby | JFB | garder |  | commune* | commune | mort | ≈ 1,1 M$ (estimé CG) | CoinGecko `jelly-finance-baby` ; cap. ≈ 606 k$, volume 24 h ≈ 0 k$, écart -44,6 % |
| 525 | TRON MASCOT | SUNTRON | garder |  | commune* | commune | mort | ≈ 1,2 M$ (estimé CG) | CoinGecko `tron-mascot` ; cap. ≈ 635 k$, volume 24 h ≈ 0 k$, écart -45,5 % |
| 526 | Zoki | ZOKI | garder |  | commune* | commune | mort | ≈ 1,0 M$ (estimé CG) | CoinGecko `zoki` ; cap. ≈ 533 k$, volume 24 h ≈ 1 k$, écart -47,4 % |
| 527 | Hogdog | HOGDOG | garder |  | commune | commune | mort (absent de CoinGecko) | ≈ 860 k$ (sourcé) | catalogue (pic sourcé) |
| 528 | 360noscope420blazeit | MLG | garder |  | commune | rare | mort | ≈ 187 M$ (estimé CG) | CoinGecko `360noscope420blazeit` ; cap. ≈ 539 k$, volume 24 h ≈ 4 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 529 | Acolyte | à vérifier | retirer | plateforme de découverte d'agents IA (Acolyte by Virtuals) | commune | — | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 530 | Act I : The AI Prophecy † | ACT | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 872 M$ (estimé CG) | CoinGecko `act-i-the-ai-prophecy` ; cap. ≈ 9,2 M$, volume 24 h ≈ 22 M$, écart -98,9 % — mème sur l'IA, classé mème par Binance |
| 531 | AI XOVIA | AIX | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 4,50 Md$ (estimé CG) | CoinGecko `ai-xovia` ; cap. ≈ 20 M$, volume 24 h ≈ 4 k$, écart -99,6 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 532 | AIFlow | AIFLOW | retirer | cadriciel d'agents IA sur BNB Chain (AIFlow) | commune | — | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 533 | Akita Inu | AKITA | garder |  | commune | commune | mort | ≈ 803 k$ (estimé CG) | CoinGecko `akita-inu-3` ; cap. ≈ 5 k$, volume 24 h ≈ 0 k$, écart -99,4 % |
| 534 | All Street Bets | BETS | garder |  | commune | commune | mort | ≈ 28 M$ (estimé CG) | CoinGecko `all-street-bets` ; cap. ≈ 44 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 535 | AMC (Solana) | AMC | garder |  | commune | commune | mort | ≈ 7,6 M$ (estimé CG) | CoinGecko `amc-3` ; cap. ≈ 29 k$, volume 24 h ≈ 0 k$, écart -99,6 % |
| 536 | American Pepe | USPEPE | garder |  | commune | commune | mort | ≈ 8,8 M$ (estimé CG) | CoinGecko `american-pepe` ; cap. ≈ 43 k$, volume 24 h ≈ 0 k$, écart -99,5 % |
| 537 | Andwu Tet | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 538 | Andy † | ANDY | garder |  | commune | rare | mort | ≈ 46 M$ (estimé CG) | CoinGecko `andy-on-base` ; cap. ≈ 239 k$, volume 24 h ≈ 0 k$, écart -99,5 % |
| 539 | Anon Inu | AINU | garder |  | commune | rare | mort | ≈ 5,18 Md$ (estimé CG) | CoinGecko `anon-inu` ; cap. ≈ 528 k$, volume 24 h ≈ 0 k$, écart -100,0 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 540 | Apu Apustaja | APU | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 495 M$ (estimé CG) | CoinGecko `apu-s-club` ; cap. ≈ 3,3 M$, volume 24 h ≈ 37 k$, écart -99,3 % |
| 541 | ArbDoge AI † | AIDOGE | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 209 M$ (estimé CG) | CoinGecko `arbdoge-ai` ; cap. ≈ 1,3 M$, volume 24 h ≈ 63 k$, écart -99,4 % |
| 542 | Arbi Pepe | PEPE (Arbitrum) | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 543 | Arbinu | ARBINU | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 544 | AstroElon | ELONONE | garder |  | commune | rare | mort | ≈ 109 M$ (estimé CG) | CoinGecko `astroelon` ; cap. ≈ 145 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 545 | Baby Arbitrum | BARB | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 546 | Baby Claw | BABYCLAW | garder |  | commune | rare | actif | ≈ 91 M$ (plancher : capitalisation actuelle) | CoinGecko `baby-claw` ; cap. ≈ 91 M$, volume 24 h ≈ 0 k$, écart 18791,6 % |
| 547 | Baby Shark Universe | BSU | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 304 M$ (estimé CG) | CoinGecko `baby-shark-universe` ; cap. ≈ 1,3 M$, volume 24 h ≈ 105 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 548 | Balaji (créateur Zora) | BALAJIS | retirer | creator coin Zora (Balaji), jeton de créateur | commune | — | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 549 | Banana For Scale | BANANAS31 | garder |  | commune | épique | en déclin | ≈ 577 M$ (estimé CG) | CoinGecko `banana-for-scale-2` ; cap. ≈ 59 M$, volume 24 h ≈ 2,7 M$, écart -89,8 % |
| 550 | Bananacoin | BCO (à vérifier) | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 551 | Banano † | BAN | garder |  | commune | rare | mort | ≈ 88 M$ (estimé CG) | CoinGecko `banano` ; cap. ≈ 682 k$, volume 24 h ≈ 0 k$, écart -99,2 % |
| 552 | Barsik | BARSIK | garder |  | commune | rare | mort | ≈ 340 M$ (estimé CG) | CoinGecko `hasbulla-s-cat` ; cap. ≈ 95 k$, volume 24 h ≈ 2 k$, écart -100,0 % — écart ≤ -99,5 % : estimation fragile, un cran de moins; rapprochement CoinGecko par ticker seul |
| 553 | Base Baboon | BOON | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 554 | Based Bario | BARIO | garder |  | commune | commune | mort | ≈ 7,1 M$ (estimé CG) | CoinGecko `based-bario` ; cap. ≈ 5 k$, volume 24 h ≈ 0 k$, écart -99,9 % |
| 555 | Based Chad | CHAD | garder |  | commune | rare | mort | ≈ 19 M$ (estimé CG) | CoinGecko `based-chad` ; cap. ≈ 229 k$, volume 24 h ≈ 0 k$, écart -98,8 % |
| 556 | Based Coin | BASED | garder |  | commune | commune | mort | ≈ 1,6 M$ (estimé CG) | CoinGecko `based-coin` ; cap. ≈ 248 k$, volume 24 h ≈ 0 k$, écart -84,3 % |
| 557 | Based Pepe | PEPE | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 184 M$ (estimé CG) | CoinGecko `based-pepe` ; cap. ≈ 2,3 M$, volume 24 h ≈ 1 k$, écart -98,8 % |
| 558 | Based Tyler † | TYBG | garder |  | commune | rare | mort | ≈ 86 M$ (estimé CG) | CoinGecko `base-god` ; cap. ≈ 676 k$, volume 24 h ≈ 0 k$, écart -99,2 % — doublon probable de n° 185 Base God (TYBG) : même ticker, même chaîne; rapprochement CoinGecko par ticker seul |
| 559 | Beercoin | BEER | garder |  | commune | rare | mort | ≈ 507 M$ (estimé CG) | CoinGecko `beercoin-2` ; cap. ≈ 559 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 560 | Believe | BELIEVE | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 457 M$ (estimé CG) | CoinGecko `ben-pasternak` ; cap. ≈ 1,9 M$, volume 24 h ≈ 1,2 M$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 561 | Bera Morning | BM | garder |  | commune | commune | mort | ≈ 10 M$ (estimé CG) | CoinGecko `bm` ; cap. ≈ 10 k$, volume 24 h ≈ 3 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins; rapprochement CoinGecko par ticker seul |
| 562 | Bert | BERT | garder |  | commune | commune | mort | ≈ 842 k$ (estimé CG) | CoinGecko `bert` ; cap. ≈ 40 k$, volume 24 h ≈ 0 k$, écart -95,2 % |
| 563 | Billy † | BILLY | garder |  | commune | rare | mort | ≈ 228 M$ (estimé CG) | CoinGecko `billy` ; cap. ≈ 335 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 564 | Blum | BLUM | retirer | application de trading / jeu Telegram (Blum) | commune | — | en déclin (-95 % ou pire) | ≈ 68 M$ (estimé CG) | CoinGecko `blum` ; cap. ≈ 340 k$, volume 24 h ≈ 38 k$, écart -99,5 % |
| 565 | BNB Tiger OG | BNBTIGEROG | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 3351,98 Md$ (estimé CG) | CoinGecko `bnbtiger` ; cap. ≈ 6,4 M$, volume 24 h ≈ 9 k$, écart -100,0 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 566 | Bob (Monad) | BOB | garder |  | commune | rare | mort | ≈ 43 M$ (estimé CG) | CoinGecko `bob-3` ; cap. ≈ 988 k$, volume 24 h ≈ 3 k$, écart -97,7 % |
| 567 | Bob † | BOB | garder |  | commune | rare | mort | ≈ 43 M$ (estimé CG) | CoinGecko `bob-3` ; cap. ≈ 988 k$, volume 24 h ≈ 3 k$, écart -97,7 % |
| 568 | BOG | BOG | garder |  | commune | commune | mort | ≈ 28 M$ (estimé CG) | CoinGecko `bog` ; cap. ≈ 44 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 569 | Bombardiro | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 570 | Bomeow | BOMEOW | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 571 | Bone ShibaSwap † | BONE | retirer | jeton de gouvernance de ShibaSwap (Bone ShibaSwap) | commune | — | en déclin (-95 % ou pire) | ≈ 3,87 Md$ (estimé CG) | CoinGecko `bone-shibaswap` ; cap. ≈ 11 M$, volume 24 h ≈ 1,8 M$, écart -99,7 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 572 | Brainlet | BRAINLET | garder |  | commune | commune | mort | ≈ 54 M$ (estimé CG) | CoinGecko `brainlet-2` ; cap. ≈ 31 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 573 | Capybara Nation | BARA | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 2,21 Md$ (estimé CG) | CoinGecko `capybara-nation` ; cap. ≈ 7,1 M$, volume 24 h ≈ 3 k$, écart -99,7 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 574 | CateCoin † | CATE | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 658 M$ (estimé CG) | CoinGecko `catecoin` ; cap. ≈ 3,6 M$, volume 24 h ≈ 0 k$, écart -99,4 % |
| 575 | cats (BRC-20) | CATS | garder |  | commune | commune | mort | ≈ 1,0 M$ (estimé CG) | CoinGecko `cats-3` ; cap. ≈ 152 k$, volume 24 h ≈ 0 k$, écart -84,8 % |
| 576 | CATS•IN•THE•SATS | CATS | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 577 | catwifhat | CWIF | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 2,24 Md$ (estimé CG) | CoinGecko `catwifhat-2` ; cap. ≈ 14 M$, volume 24 h ≈ 3 k$, écart -99,4 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique |
| 579 | ChatAI | CHATAI | retirer | jeu IA « play-to-earn » (ChatAI Town) | commune | — | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 580 | ChillDeer | CHILLDEER | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 581 | Chog | CHOG | garder |  | commune | commune | mort | ≈ 5,5 M$ (estimé CG) | CoinGecko `chog` ; cap. ≈ 896 k$, volume 24 h ≈ 8 k$, écart -83,7 % |
| 582 | Chomp | CHOMP | garder |  | commune | commune | mort | ≈ 89 M$ (estimé CG) | CoinGecko `chompcoin` ; cap. ≈ 97 k$, volume 24 h ≈ 1 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins; rapprochement CoinGecko par ticker seul |
| 583 | clank.fun | CLANKFUN | retirer | launchpad (clank.fun) | commune | — | mort | ≈ 7,0 M$ (estimé CG) | CoinGecko `clank-fun` ; cap. ≈ 66 k$, volume 24 h ≈ 0 k$, écart -99,1 % |
| 584 | Comedian † | BAN | garder |  | commune | épique | en déclin | ≈ 378 M$ (estimé CG) | CoinGecko `comedian` ; cap. ≈ 46 M$, volume 24 h ≈ 1,1 M$, écart -87,9 % |
| 585 | Conscious | CONSCIOUS | garder |  | commune | rare | mort | ≈ 198 M$ (estimé CG) | CoinGecko `conscious-token` ; cap. ≈ 333 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 586 | CorgiCoin | à vérifier | garder |  | commune | commune | mort | ≈ 19 M$ (estimé CG) | CoinGecko `corgicoin` ; cap. ≈ 95 k$, volume 24 h ≈ 0 k$, écart -99,5 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 587 | Crash On Base | CRASH | garder |  | commune | rare | mort | ≈ 37 M$ (estimé CG) | CoinGecko `crash-on-base` ; cap. ≈ 238 k$, volume 24 h ≈ 0 k$, écart -99,4 % |
| 588 | Crow with Knife | CAW | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 114 M$ (estimé CG) | CoinGecko `crow-with-knife` ; cap. ≈ 3,9 M$, volume 24 h ≈ 11 k$, écart -96,6 % |
| 589 | Cthulhu Offerings | CTHULHU (à vérifier) | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 590 | Cult DAO | CULT | retirer | DAO d'investissement (Cult DAO), DeFi | commune | — | en déclin (-95 % ou pire) | ≈ 275 M$ (estimé CG) | CoinGecko `cult-dao` ; cap. ≈ 2,1 M$, volume 24 h ≈ 6 k$, écart -99,3 % |
| 591 | CYPHER•GENESIS | CYPHER | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 592 | Davido † | DAVIDO | garder |  | commune | commune | mort | ≈ 3,3 M$ (estimé CG) | CoinGecko `timeless-davido` ; cap. ≈ 9 k$, volume 24 h ≈ 0 k$, écart -99,7 % — rapprochement CoinGecko par ticker seul |
| 593 | DebtReliefBot | DRB | garder |  | commune | rare | en déclin | ≈ 41 M$ (estimé CG) | CoinGecko `debtreliefbot` ; cap. ≈ 7,9 M$, volume 24 h ≈ 177 k$, écart -80,5 % |
| 594 | DED † | DED | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 595 | DeFrogs | DEFROGS | garder |  | commune | commune | mort | ≈ 39 M$ (estimé CG) | CoinGecko `defrogs` ; cap. ≈ 166 k$, volume 24 h ≈ 0 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 596 | Dejitaru Tsuka | TSUKA | garder |  | commune | épique | mort | ≈ 157 M$ (estimé CG) | CoinGecko `dejitaru-tsuka` ; cap. ≈ 915 k$, volume 24 h ≈ 0 k$, écart -99,4 % |
| 597 | Dink Doink | DINK | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 598 | Dino | DINO | garder |  | commune | commune | mort | ≈ 5,9 M$ (estimé CG) | CoinGecko `dino-2` ; cap. ≈ 48 k$, volume 24 h ≈ 0 k$, écart -99,2 % |
| 599 | Doge Dash | DOGEDASH | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 600 | Doge Killer † | LEASH | garder |  | commune | commune | en déclin (-95 % ou pire) | ≈ 1,3 M$ (plancher : capitalisation actuelle) | CoinGecko `leash` ; cap. ≈ 1,3 M$, volume 24 h ≈ 1 k$, écart -100,0 % |
| 601 | Dogechain † | DC | retirer | jeton de chaîne (Dogechain), L2 | commune | — | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 602 | DogeGF | DOGEGF | garder |  | commune | rare | mort | ≈ 226 M$ (estimé CG) | CoinGecko `dogegf` ; cap. ≈ 806 k$, volume 24 h ≈ 0 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 603 | Dogeparty | XDP | retirer | protocole (Dogeparty, fork de Counterparty) | commune | — | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 604 | Doggy | DOGGY | garder |  | commune | commune | mort | ≈ 66 M$ (estimé CG) | CoinGecko `doggy` ; cap. ≈ 170 k$, volume 24 h ≈ 0 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 605 | Doginme † | DOGINME | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 120 M$ (estimé CG) | CoinGecko `doginme` ; cap. ≈ 4,1 M$, volume 24 h ≈ 96 k$, écart -96,6 % |
| 606 | Dogs of Elon | DOE | garder |  | commune | commune | mort | ≈ 6,0 M$ (estimé CG) | CoinGecko `dogs-of-elon` ; cap. ≈ 21 k$, volume 24 h ≈ 0 k$, écart -99,7 % |
| 607 | Dogs † | DOGS | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 844 M$ (estimé CG) | CoinGecko `dogs-2` ; cap. ≈ 17 M$, volume 24 h ≈ 3,7 M$, écart -98,0 % — mème (chien de Durov) distribué par airdrop, pas un tap-to-earn |
| 608 | DogWifCat | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 610 | Dragon Sun | DRGN | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 611 | DropArb | DROP | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 612 | Egg | EGG | garder |  | commune | commune | mort | ≈ 8,6 M$ (estimé CG) | CoinGecko `egg-3` ; cap. ≈ 130 k$, volume 24 h ≈ 5 k$, écart -98,5 % |
| 613 | Elon Buys Twitter | EBT | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 614 | ElonGate † | ELONGATE | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 615 | emo | EMO | garder |  | commune | commune | mort | ≈ 1,9 M$ (estimé CG) | CoinGecko `emonad` ; cap. ≈ 449 k$, volume 24 h ≈ 2 k$, écart -76,1 % — rapprochement CoinGecko par ticker seul |
| 616 | Fantasy Pepe | FEPE | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 617 | Feels Good Man | FEELSGOOD | garder |  | commune | commune | actif | ≈ 5,7 M$ (estimé CG) | CoinGecko `feels-good-man-3` ; cap. ≈ 1,3 M$, volume 24 h ≈ 0 k$, écart -76,8 % |
| 618 | Fofar | FOFAR | garder |  | commune | commune | mort | ≈ 39 M$ (estimé CG) | CoinGecko `fofar-2` ; cap. ≈ 87 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 619 | Frog on ETH | FROG | garder |  | commune | commune | mort | ≈ 10 M$ (estimé CG) | CoinGecko `frog-on-eth` ; cap. ≈ 34 k$, volume 24 h ≈ 0 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 620 | Fronk | FRONK | garder |  | commune | commune | mort | ≈ 10,0 M$ (estimé CG) | CoinGecko `fronk` ; cap. ≈ 85 k$, volume 24 h ≈ 0 k$, écart -99,1 % |
| 621 | Fwog † | FWOG | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 718 M$ (estimé CG) | CoinGecko `fwog` ; cap. ≈ 3,6 M$, volume 24 h ≈ 1,0 M$, écart -99,5 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 622 | GAME•OF•BITCOIN | GAME | garder |  | commune | rare | mort | ≈ 23 M$ (estimé CG) | CoinGecko `game-of-bitcoin-rune` ; cap. ≈ 530 k$, volume 24 h ≈ 0 k$, écart -97,7 % |
| 623 | Garlicoin | GRLC | garder |  | commune | épique | mort | ≈ 40 M$ (estimé CG) | CoinGecko `garlicoin` ; cap. ≈ 410 k$, volume 24 h ≈ 0 k$, écart -99,0 % — histoire : Garlicoin : mème culte de 2018 (pain à l'ail) |
| 624 | Gavun Wud | WUD | garder |  | commune | commune | mort | ≈ 607 k$ (plancher : capitalisation actuelle) | CoinGecko `gavun-wud` ; cap. ≈ 607 k$, volume 24 h ≈ 0 k$, écart -100,0 % |
| 625 | Gecko Inu | GEC | garder |  | commune | commune | mort | ≈ 30 M$ (estimé CG) | CoinGecko `gecko-inu` ; cap. ≈ 103 k$, volume 24 h ≈ 0 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 626 | Gigachad † | GIGA | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 914 M$ (estimé CG) | CoinGecko `gigachad-2` ; cap. ≈ 16 M$, volume 24 h ≈ 1,7 M$, écart -98,2 % |
| 627 | Giggle Academy | GIGGLE | garder |  | commune | épique | en déclin | ≈ 275 M$ (estimé CG) | CoinGecko `giggle-fund` ; cap. ≈ 28 M$, volume 24 h ≈ 2,6 M$, écart -89,8 % — rapprochement CoinGecko par ticker seul |
| 628 | Ginnan | GINNAN | garder |  | commune | commune | mort | ≈ 5,7 M$ (estimé CG) | CoinGecko `ginnan` ; cap. ≈ 208 k$, volume 24 h ≈ 5 k$, écart -96,4 % |
| 629 | Gizmo | GIZMO | garder |  | commune | commune | mort | ≈ 63 M$ (estimé CG) | CoinGecko `gizmo-imaginary-kitten-runes` ; cap. ≈ 232 k$, volume 24 h ≈ 0 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 630 | GMEKitty | GMEKITTY | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 631 | Golden Dragon | GD | garder |  | commune | commune | actif | ≈ 5,2 M$ (estimé CG) | CoinGecko `golden-dragon` ; cap. ≈ 5,2 M$, volume 24 h ≈ 0 k$, écart -0,1 % |
| 632 | GreenHood | HOOD | garder |  | commune | rare | mort | ≈ 191 M$ (estimé CG) | CoinGecko `greenhood` ; cap. ≈ 649 k$, volume 24 h ≈ 0 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 633 | Happy | HAPPY | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 186 M$ (estimé CG) | CoinGecko `happycat-2` ; cap. ≈ 309 k$, volume 24 h ≈ 549 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins; rapprochement CoinGecko par ticker seul |
| 634 | Harambe | HARAMBE | garder |  | commune | rare | en déclin | ≈ 14 M$ (estimé CG) | CoinGecko `harambe` ; cap. ≈ 1,3 M$, volume 24 h ≈ 0 k$, écart -90,7 % |
| 635 | HarryPotterObamaSonic10Inu | BITCOIN | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 373 M$ (estimé CG) | CoinGecko `harrypotterobamasonic10in` ; cap. ≈ 12 M$, volume 24 h ≈ 318 k$, écart -96,8 % |
| 636 | Hasbulla | HASBI | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 637 | Hatch | HATCH | garder |  | commune | rare | mort | ≈ 132 M$ (estimé CG) | CoinGecko `hatch-2` ; cap. ≈ 568 k$, volume 24 h ≈ 0 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 638 | Hehe | HEHE | garder |  | commune | rare | mort | ≈ 39 M$ (estimé CG) | CoinGecko `hehecat` ; cap. ≈ 668 k$, volume 24 h ≈ 3 k$, écart -98,3 % |
| 639 | HeMa | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 640 | Higher † | HIGHER | garder |  | commune | rare | mort | ≈ 114 M$ (estimé CG) | CoinGecko `higher` ; cap. ≈ 153 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 641 | Hoge Finance | HOGE | garder |  | commune | rare | mort | ≈ 367 M$ (estimé CG) | CoinGecko `hoge-finance` ; cap. ≈ 748 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 642 | Hosky † | HOSKY | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 368 M$ (estimé CG) | CoinGecko `hosky` ; cap. ≈ 4,2 M$, volume 24 h ≈ 2 k$, écart -98,9 % |
| 645 | Hypurr Fun | HFUN | retirer | launchpad Hyperliquid (Hypurr Fun) | commune | — | en déclin (-95 % ou pire) | ≈ 299 M$ (estimé CG) | CoinGecko `hypurr-fun` ; cap. ≈ 11 M$, volume 24 h ≈ 45 k$, écart -96,4 % |
| 646 | IKUN | IKUN | garder |  | commune | commune | en déclin (-95 % ou pire) | ≈ 32 M$ (estimé CG) | CoinGecko `ikun` ; cap. ≈ 49 k$, volume 24 h ≈ 26 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 647 | Intel (Intear) | INTEL | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 649 | Jesse (créateur Zora) | JESSE | retirer | creator coin Zora (Jesse), jeton de créateur | commune | — | mort | ≈ 8,9 M$ (estimé CG) | CoinGecko `jesse` ; cap. ≈ 415 k$, volume 24 h ≈ 1 k$, écart -95,3 % |
| 650 | Just a chill guy † | CHILLGUY | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 657 M$ (estimé CG) | CoinGecko `chill-guy` ; cap. ≈ 8,3 M$, volume 24 h ≈ 3,2 M$, écart -98,7 % |
| 652 | Katana Inu | KATA | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 359 M$ (estimé CG) | CoinGecko `katana-inu` ; cap. ≈ 1,2 M$, volume 24 h ≈ 13 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 653 | Kazonomics (créateur Zora) | KAZONOMICS | retirer | creator coin Zora (Kazonomics), jeton de créateur | commune | — | mort | ≈ 52 M$ (estimé CG) | CoinGecko `kazonomics` ; cap. ≈ 793 k$, volume 24 h ≈ 0 k$, écart -98,5 % |
| 654 | Keanu | KEANU | garder |  | commune | commune | mort | ≈ 5,5 M$ (estimé CG) | CoinGecko `keanu` ; cap. ≈ 7 k$, volume 24 h ≈ 0 k$, écart -99,9 % |
| 655 | Ket | KET | garder |  | commune | rare | en déclin | ≈ 19 M$ (estimé CG) | CoinGecko `ket-3` ; cap. ≈ 1,9 M$, volume 24 h ≈ 1,0 M$, écart -89,8 % |
| 656 | Keyboard Cat † | KEYCAT | garder |  | commune | commune | mort | ≈ 9,0 M$ (estimé CG) | CoinGecko `keyboard-cat` ; cap. ≈ 41 k$, volume 24 h ≈ 0 k$, écart -99,5 % |
| 657 | Kishu Inu | KISHU | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 1,69 Md$ (estimé CG) | CoinGecko `kishu-inu` ; cap. ≈ 4,8 M$, volume 24 h ≈ 70 k$, écart -99,7 % — histoire : Kishu Inu : « tueur de Doge » de 2021, pic estimé fragile; estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 658 | Life K Line | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 659 | Ligo | LIGO | garder |  | commune | commune | mort | inconnu | CoinGecko `ligo-ordinals` |
| 660 | Lil Pump | LILPUMP | garder |  | commune | commune | mort | ≈ 2,2 M$ (estimé CG) | CoinGecko `lil-pump` ; cap. ≈ 23 k$, volume 24 h ≈ 0 k$, écart -99,0 % |
| 661 | Lock In | LOCKIN | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 115 M$ (estimé CG) | CoinGecko `lock-in` ; cap. ≈ 815 k$, volume 24 h ≈ 103 k$, écart -99,3 % |
| 662 | Luce † | LUCE | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 319 M$ (estimé CG) | CoinGecko `offcial-mascot-of-the-holy-year` ; cap. ≈ 266 k$, volume 24 h ≈ 25 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 663 | Lucky Meow Coin | LMAO | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 664 | Luckycoin | LKY | garder |  | commune | rare | mort | ≈ 338 M$ (estimé CG) | CoinGecko `luckycoin` ; cap. ≈ 829 k$, volume 24 h ≈ 20 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 665 | Luna by Virtuals | LUNA | retirer | agent IA (Luna by Virtuals) | commune | — | en déclin (-95 % ou pire) | ≈ 252 M$ (estimé CG) | CoinGecko `luna-by-virtuals` ; cap. ≈ 3,2 M$, volume 24 h ≈ 0 k$, écart -98,7 % |
| 667 | Maneki † | MANEKI | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 244 M$ (estimé CG) | CoinGecko `maneki` ; cap. ≈ 2,0 M$, volume 24 h ≈ 27 k$, écart -99,2 % |
| 668 | Maxi Doge | MAXI | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 669 | Memecoin † | MEME | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 3,66 Md$ (estimé CG) | CoinGecko `memecoin-2` ; cap. ≈ 25 M$, volume 24 h ≈ 4,8 M$, écart -99,3 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique |
| 670 | MEME•ECONOMICS | MEMERUNE | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 671 | mfercoin | MFER | garder |  | commune | rare | mort | ≈ 264 M$ (estimé CG) | CoinGecko `mfercoin` ; cap. ≈ 402 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 672 | Mice | MICE | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 673 | Michi † | MICHI | garder |  | commune | commune | actif | ≈ 4,9 M$ (estimé CG) | CoinGecko `michi` ; cap. ≈ 1,9 M$, volume 24 h ≈ 26 k$, écart -62,5 % |
| 674 | Miggles † | MIGGLES | garder |  | commune | épique | mort | ≈ 183 M$ (estimé CG) | CoinGecko `mister-miggles` ; cap. ≈ 959 k$, volume 24 h ≈ 17 k$, écart -99,5 % — rapprochement CoinGecko par ticker seul |
| 675 | Mittens | MITTENS | garder |  | commune | rare | mort | ≈ 13 M$ (estimé CG) | CoinGecko `mittens-2` ; cap. ≈ 143 k$, volume 24 h ≈ 1 k$, écart -98,9 % |
| 676 | Moby AI | MOBY | retirer | agent IA de suivi de baleines (Moby AI) | commune | — | en déclin (-95 % ou pire) | ≈ 192 M$ (estimé CG) | CoinGecko `moby-ai` ; cap. ≈ 1,2 M$, volume 24 h ≈ 338 k$, écart -99,4 % |
| 677 | Molandak | MOLANDAK | garder |  | commune | commune | mort | inconnu | CoinGecko `molandak-2` |
| 678 | Moltbook | à vérifier | garder |  | commune | commune | en déclin (-95 % ou pire) | ≈ 100 M$ (estimé CG) | CoinGecko `moltbook` ; cap. ≈ 250 k$, volume 24 h ≈ 27 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 679 | Momo | MOMO | garder |  | commune | commune | mort | ≈ 41 M$ (estimé CG) | CoinGecko `momo-3` ; cap. ≈ 104 k$, volume 24 h ≈ 3 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 680 | Monacoin † | MONA | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 1,73 Md$ (estimé CG) | CoinGecko `monacoin` ; cap. ≈ 6,1 M$, volume 24 h ≈ 1 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 681 | MONCAT | MONCAT | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 682 | Mongoose | MONGOOSE | garder |  | commune | rare | mort | ≈ 149 M$ (estimé CG) | CoinGecko `mongoose` ; cap. ≈ 570 k$, volume 24 h ≈ 0 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 683 | monKEYS | MONKEYS | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 700 M$ (estimé CG) | CoinGecko `monkeys-2` ; cap. ≈ 1,1 M$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 684 | Moo Deng † | MOODENG | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 673 M$ (estimé CG) | CoinGecko `moo-deng` ; cap. ≈ 30 M$, volume 24 h ≈ 4,4 M$, écart -95,5 % |
| 685 | Mooncat | MCAT | garder |  | commune | commune | mort | ≈ 7,6 M$ (estimé CG) | CoinGecko `mooncat-2` ; cap. ≈ 203 k$, volume 24 h ≈ 6 k$, écart -97,3 % |
| 686 | Mooncoin † | MOON | garder |  | commune | rare | à vérifier (homonyme sur CoinGecko, non rapproché) | inconnu | catalogue ; absent du relevé — histoire : Mooncoin : mème de l'ère 2013-2014 |
| 687 | Mouch | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 688 | Moyaki | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 689 | Mubarak | MUBARAK | garder |  | commune | épique | en déclin | ≈ 211 M$ (estimé CG) | CoinGecko `mubarak` ; cap. ≈ 37 M$, volume 24 h ≈ 5,0 M$, écart -82,5 % |
| 690 | MultiBit | MUBI | retirer | pont et protocole BRC-20 (MultiBit) | commune | — | mort | ≈ 351 M$ (estimé CG) | CoinGecko `multibit` ; cap. ≈ 192 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 691 | Mumu the Bull † | MUMU | garder |  | commune | commune | mort | ≈ 4,2 M$ (estimé CG) | CoinGecko `mumu-the-bull-4` ; cap. ≈ 194 k$, volume 24 h ≈ 8 k$, écart -95,4 % |
| 692 | Muncat | MUNCAT | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 693 | MyOnion.fun | $ONION | garder |  | commune | rare | actif | ≈ 22 M$ (estimé CG) | CoinGecko `myonion-fun` ; cap. ≈ 22 M$, volume 24 h ≈ 0 k$, écart -0,0 % |
| 694 | Myro † | MYRO | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 443 M$ (estimé CG) | CoinGecko `myro` ; cap. ≈ 1,3 M$, volume 24 h ≈ 150 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 695 | Neiro † | NEIRO | garder |  | commune | légendaire | en déclin (-95 % ou pire) | ≈ 1,27 Md$ (estimé CG) | CoinGecko `neiro-3` ; cap. ≈ 25 M$, volume 24 h ≈ 3,5 M$, écart -98,0 % |
| 696 | NEKO | NEKO | garder |  | commune | rare | mort | ≈ 13 M$ (estimé CG) | CoinGecko `neko` ; cap. ≈ 121 k$, volume 24 h ≈ 1 k$, écart -99,1 % |
| 697 | Non-Playable Coin | NPC | garder |  | commune | épique | actif | ≈ 533 M$ (estimé CG) | CoinGecko `non-playable-coin` ; cap. ≈ 110 M$, volume 24 h ≈ 4,3 M$, écart -79,4 % |
| 698 | Nostalgia | NOS | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 699 | Nyancoin | NYAN | garder |  | commune | rare | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé — histoire : Nyancoin : mème de l'ère 2014 |
| 700 | Olen Mosk | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 701 | Ordiswap | ORDS | retirer | DEX BRC-20 (Ordiswap) | commune | — | mort | ≈ 277 M$ (estimé CG) | CoinGecko `ordiswap-token` ; cap. ≈ 127 k$, volume 24 h ≈ 1 k$, écart -100,0 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 702 | Oxbt | OXBT | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 703 | Palu | PALU | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 116 M$ (estimé CG) | CoinGecko `palu` ; cap. ≈ 860 k$, volume 24 h ≈ 367 k$, écart -99,3 % |
| 704 | Pandora | PANDORA | retirer | jeton expérimental ERC-404 (Pandora), pas un mème | commune | — | mort | ≈ 325 M$ (estimé CG) | CoinGecko `pandora` ; cap. ≈ 807 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 705 | Pepe MAGA | PEPE MAGA | garder |  | commune | commune | mort | ≈ 281 k$ (estimé CG) | CoinGecko `pepe-maga` ; cap. ≈ 3 k$, volume 24 h ≈ 0 k$, écart -98,8 % |
| 706 | Pepe on Monad | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 707 | Pepe Ordinals | PEPE | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 708 | PepeCoin on Solana | PEPE | garder |  | commune | rare | mort | ≈ 297 M$ (estimé CG) | CoinGecko `pepecoin-on-solana` ; cap. ≈ 533 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 709 | Pepecoin † | MEME | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 187 M$ (estimé CG) | CoinGecko `pepecoin-network` ; cap. ≈ 7,5 M$, volume 24 h ≈ 90 k$, écart -96,0 % — doublon de n° 99 (CoinGecko `pepecoin-network`, ticker actuel PEP et non MEME) : garder une seule carte |
| 710 | PePeonTron | PEPEONTRON | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 90 M$ (estimé CG) | CoinGecko `pepeontron` ; cap. ≈ 1,2 M$, volume 24 h ≈ 174 k$, écart -98,7 % |
| 711 | PEPPER | PEPPER | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 2,56 Md$ (estimé CG) | CoinGecko `pepper` ; cap. ≈ 4,0 M$, volume 24 h ≈ 20 k$, écart -99,8 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 712 | Pesto the Baby King Penguin | PESTO | garder |  | commune | commune | mort | ≈ 29 M$ (estimé CG) | CoinGecko `pesto-the-baby-king-penguin` ; cap. ≈ 66 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 713 | Pitbull | PIT | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 5,81 Md$ (estimé CG) | CoinGecko `pitbull` ; cap. ≈ 5,3 M$, volume 24 h ≈ 62 k$, écart -99,9 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 714 | Pizza | PIZZA | garder |  | commune | commune | mort | ≈ 2,4 M$ (estimé CG) | CoinGecko `pizza` ; cap. ≈ 66 k$, volume 24 h ≈ 0 k$, écart -97,2 % |
| 715 | PolyDoge | POLYDOGE | garder |  | commune | commune | mort | ≈ 80 M$ (estimé CG) | CoinGecko `polydoge` ; cap. ≈ 170 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 716 | Ponke † | PONKE | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 465 M$ (estimé CG) | CoinGecko `ponke` ; cap. ≈ 9,4 M$, volume 24 h ≈ 2,0 M$, écart -98,0 % |
| 717 | Ponzicoin | PONZI | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 718 | Poodlana | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 719 | Povel Durev | DUREV | garder |  | commune | rare | mort | ≈ 16 M$ (estimé CG) | CoinGecko `povel-durev` ; cap. ≈ 375 k$, volume 24 h ≈ 1 k$, écart -97,6 % |
| 720 | PSYOP † | PSYOP | garder |  | commune | commune | mort | ≈ 1,8 M$ (estimé CG) | CoinGecko `psyop-2` ; cap. ≈ 10 k$, volume 24 h ≈ 0 k$, écart -99,5 % |
| 721 | Punch | PUNCH | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 722 | Pups † | PUPS | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 3,87 Md$ (estimé CG) | CoinGecko `rune-pups` ; cap. ≈ 2,5 M$, volume 24 h ≈ 6 k$, écart -99,9 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins; rapprochement CoinGecko par ticker seul |
| 723 | Purr | PURR | garder |  | commune | épique | en déclin | ≈ 410 M$ (estimé CG) | CoinGecko `purr-2` ; cap. ≈ 54 M$, volume 24 h ≈ 993 k$, écart -86,8 % |
| 724 | Rare Pepe Cash † | PEPECASH | garder |  | commune | épique | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé — histoire : Rare Pepe Cash : premiers mèmes en NFT (Counterparty, 2016) |
| 725 | Rats † | RATS | garder |  | commune | commune | à vérifier (homonyme sur CoinGecko, non rapproché) | inconnu | catalogue ; absent du relevé |
| 726 | RAVE | RAVE | retirer | jeton d'une DAO d'événements (RaveDAO) | commune | — | en déclin (-95 % ou pire) | ≈ 7,59 Md$ (estimé CG) | CoinGecko `ravedao` ; cap. ≈ 35 M$, volume 24 h ≈ 1,3 M$, écart -99,5 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 727 | RED | RED | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 728 | Resistance Dog | REDO | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 138 M$ (estimé CG) | CoinGecko `resistance-dog` ; cap. ≈ 4,0 M$, volume 24 h ≈ 84 k$, écart -97,1 % |
| 729 | Resistance Duck | à vérifier | garder |  | commune | commune | mort | ≈ 1,5 M$ (estimé CG) | CoinGecko `resistance-duck` ; cap. ≈ 5 k$, volume 24 h ≈ 0 k$, écart -99,7 % |
| 730 | Rich Quack | QUACK | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 692 M$ (estimé CG) | CoinGecko `richquack` ; cap. ≈ 1,3 M$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 731 | Rizzmas | RIZZMAS | garder |  | commune | rare | mort | ≈ 91 M$ (estimé CG) | CoinGecko `rizzmas` ; cap. ≈ 578 k$, volume 24 h ≈ 16 k$, écart -99,4 % |
| 732 | Roar | ROAR | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 733 | Roost | ROOST | garder |  | commune | rare | mort | ≈ 132 M$ (estimé CG) | CoinGecko `roost` ; cap. ≈ 141 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 734 | Rosa Inu | ROSA | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 2,20 Md$ (estimé CG) | CoinGecko `rosa-inu` ; cap. ≈ 7,7 M$, volume 24 h ≈ 230 k$, écart -99,7 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 735 | Saitama Inu † | SAITAMA | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 736 | Samoyedcoin † | SAMO | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 1,36 Md$ (estimé CG) | CoinGecko `samoyedcoin` ; cap. ≈ 1,5 M$, volume 24 h ≈ 8 k$, écart -99,9 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 737 | SATOSHI•NAKAMOTO | SATOSHI | garder |  | commune | rare | mort | ≈ 188 M$ (estimé CG) | CoinGecko `satoshi-nakamoto-rune` ; cap. ≈ 388 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 738 | SelfieDogCoin | SELFIE | garder |  | commune | commune | mort | ≈ 64 M$ (estimé CG) | CoinGecko `selfiedogcoin` ; cap. ≈ 195 k$, volume 24 h ≈ 0 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 739 | SEPPUKU•IN•MAY•AND•GO•AWAY | SEPPUKU | garder |  | commune | commune | actif | inconnu | CoinGecko `seppuku` |
| 740 | Shark Cat | SC | garder |  | commune | rare | mort | ≈ 349 M$ (estimé CG) | CoinGecko `shark-cat` ; cap. ≈ 599 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 741 | Shiba Predator | QOM | garder |  | commune | rare | mort | ≈ 228 M$ (estimé CG) | CoinGecko `shiba-predator` ; cap. ≈ 795 k$, volume 24 h ≈ 0 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 742 | ShibaDoge | SHIBDOGE | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 12769,26 Md$ (estimé CG) | CoinGecko `shibadoge` ; cap. ≈ 1,3 M$, volume 24 h ≈ 0 k$, écart -100,0 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 743 | Shitzu † | SHITZU | garder |  | commune | commune | mort | ≈ 5,2 M$ (estimé CG) | CoinGecko `shitzu` ; cap. ≈ 454 k$, volume 24 h ≈ 1 k$, écart -91,3 % |
| 744 | Shoggoth | SHOGGOTH | garder |  | commune | rare | mort | ≈ 173 M$ (estimé CG) | CoinGecko `shoggoth` ; cap. ≈ 667 k$, volume 24 h ≈ 2 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 745 | Sillynubcat | NUB | garder |  | commune | commune | mort | inconnu | CoinGecko `sillynubcat` — rapprochement CoinGecko par ticker seul |
| 746 | Ski Mask Dog † | SKI | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 358 M$ (estimé CG) | CoinGecko `ski-mask-dog` ; cap. ≈ 2,0 M$, volume 24 h ≈ 25 k$, écart -99,4 % |
| 747 | Skibidi | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 748 | Slothana | SLOTH | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 76 M$ (estimé CG) | CoinGecko `slothana` ; cap. ≈ 1,9 M$, volume 24 h ≈ 1 k$, écart -97,4 % |
| 749 | SMLE | SMLE | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 750 | Smog | SMOG | garder |  | commune | commune | mort | inconnu | CoinGecko `smog` |
| 751 | Smole | SMOLE | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 214 M$ (estimé CG) | CoinGecko `smolecoin` ; cap. ≈ 7,1 M$, volume 24 h ≈ 0 k$, écart -96,7 % — rapprochement CoinGecko par ticker seul |
| 752 | Snek † | SNEK | garder |  | commune | épique | en déclin | ≈ 669 M$ (estimé CG) | CoinGecko `snek` ; cap. ≈ 36 M$, volume 24 h ≈ 753 k$, écart -94,7 % |
| 753 | Solala (索拉拉) | 索拉拉 | garder |  | commune | commune | mort | ≈ 2,8 M$ (estimé CG) | CoinGecko `solala` ; cap. ≈ 10 k$, volume 24 h ≈ 0 k$, écart -99,6 % |
| 754 | Solama | SOLAMA | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 102 M$ (estimé CG) | CoinGecko `solama` ; cap. ≈ 497 k$, volume 24 h ≈ 31 k$, écart -99,5 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 755 | SolanaDoge | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 756 | Solciety | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 757 | Solid X | SOLIDX | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 1,14 Md$ (estimé CG) | CoinGecko `solid-x` ; cap. ≈ 2,6 M$, volume 24 h ≈ 1 k$, écart -99,8 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 758 | Sosana | SOSANA | garder |  | commune | rare | en déclin | ≈ 49 M$ (estimé CG) | CoinGecko `sosana` ; cap. ≈ 4,4 M$, volume 24 h ≈ 2 k$, écart -91,1 % |
| 759 | Soulja Boy | SBOY | garder |  | commune | commune | mort | ≈ 5,4 M$ (estimé CG) | CoinGecko `soulja-coin` ; cap. ≈ 14 k$, volume 24 h ≈ 0 k$, écart -99,7 % — rapprochement CoinGecko par ticker seul |
| 760 | Sugar Boy | SUGAR | garder |  | commune | commune | mort | ≈ 25 M$ (estimé CG) | CoinGecko `sugar-boy` ; cap. ≈ 21 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 761 | Suijak | SUIJAK | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 762 | Sun Wukong | SUNWUKONG | garder |  | commune | commune | mort | ≈ 37 M$ (estimé CG) | CoinGecko `sunwukong` ; cap. ≈ 160 k$, volume 24 h ≈ 0 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 764 | Swarms | SWARMS | retirer | cadriciel d'agents IA (Swarms) | commune | — | en déclin (-95 % ou pire) | ≈ 605 M$ (estimé CG) | CoinGecko `swarms` ; cap. ≈ 6,5 M$, volume 24 h ≈ 4,1 M$, écart -98,9 % |
| 765 | Tamadoge † | TAMA | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 766 | TARS AI | TAI | retirer | agent IA (TARS AI) | commune | — | en déclin (-95 % ou pire) | ≈ 2,2 M$ (estimé CG) | CoinGecko `tars-protocol` ; cap. ≈ 12 k$, volume 24 h ≈ 145 k$, écart -99,5 % |
| 767 | Tata | TATA | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 768 | Tbull | TBULL | garder |  | commune | rare | mort | ≈ 30 M$ (estimé CG) | CoinGecko `tron-bull-coin` ; cap. ≈ 261 k$, volume 24 h ≈ 0 k$, écart -99,1 % — rapprochement CoinGecko par ticker seul |
| 769 | TikTok Memes | TIKTOK | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 770 | TJR | TJR | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 771 | Toby | TOBY | garder |  | commune | rare | mort | ≈ 12 M$ (estimé CG) | CoinGecko `toby-2` ; cap. ≈ 126 k$, volume 24 h ≈ 0 k$, écart -98,9 % |
| 772 | tokenbot | CLANKER | retirer | bot launchpad Clanker (tokenbot) | commune | — | en déclin | ≈ 141 M$ (estimé CG) | CoinGecko `tokenbot-2` ; cap. ≈ 13 M$, volume 24 h ≈ 1,5 M$, écart -90,6 % |
| 773 | Ton Inu | à vérifier | garder |  | commune | commune | mort | ≈ 7,9 M$ (estimé CG) | CoinGecko `ton-inu` ; cap. ≈ 41 k$, volume 24 h ≈ 0 k$, écart -99,5 % |
| 774 | Tron Bull | BULL | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 164 M$ (estimé CG) | CoinGecko `tron-bull` ; cap. ≈ 1,0 M$, volume 24 h ≈ 0 k$, écart -99,4 % |
| 776 | Tung Tung | TRIPLET | garder |  | commune | rare | en déclin | ≈ 27 M$ (estimé CG) | CoinGecko `tung-tung-tung-sahur-2` ; cap. ≈ 2,6 M$, volume 24 h ≈ 215 k$, écart -90,2 % — rapprochement CoinGecko par ticker seul |
| 777 | TurtSat | TURT | garder |  | commune | commune | à vérifier (homonyme sur CoinGecko, non rapproché) | inconnu | catalogue ; absent du relevé |
| 778 | Tutorial | TUT | garder |  | commune | épique | en déclin | ≈ 241 M$ (estimé CG) | CoinGecko `tutorial` ; cap. ≈ 14 M$, volume 24 h ≈ 2,3 M$, écart -94,3 % |
| 779 | Tyler | TYLER | garder |  | commune | commune | mort | ≈ 19 M$ (estimé CG) | CoinGecko `tyler-2` ; cap. ≈ 5 k$, volume 24 h ≈ 0 k$, écart -100,0 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 780 | Unicorn Fart Dust | UFD | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 403 M$ (estimé CG) | CoinGecko `unicorn-fart-dust` ; cap. ≈ 4,6 M$, volume 24 h ≈ 638 k$, écart -98,9 % |
| 781 | Useless Ethereum Token † | UET | garder |  | commune | épique | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé — histoire : Useless Ethereum Token : parodie d'ICO culte de 2017 |
| 782 | VaderAI | VADER | retirer | DAO d'investissement agent IA (VaderAI) | commune | — | mort | ≈ 158 M$ (estimé CG) | CoinGecko `vaderai-by-virtuals` ; cap. ≈ 769 k$, volume 24 h ≈ 1 k$, écart -99,5 % — écart ≤ -99,5 % : estimation fragile, un cran de moins; rapprochement CoinGecko par ticker seul |
| 783 | Viva | à vérifier | garder |  | commune | rare | mort | ≈ 11 M$ (estimé CG) | CoinGecko `viva-2` ; cap. ≈ 84 k$, volume 24 h ≈ 0 k$, écart -99,3 % |
| 784 | Waka Flocka Flame † | FLOCKA | garder |  | commune | commune | mort | ≈ 2,9 M$ (estimé CG) | CoinGecko `waka-flocka` ; cap. ≈ 16 k$, volume 24 h ≈ 0 k$, écart -99,5 % — rapprochement CoinGecko par ticker seul |
| 785 | Wall Street Baby | WSB (à vérifier) | garder |  | commune | commune | mort | ≈ 196 k$ (plancher : capitalisation actuelle) | CoinGecko `wall-street-baby` ; cap. ≈ 196 k$, volume 24 h ≈ 1 k$, écart -100,0 % |
| 786 | Wall Street Memes | WSM | garder |  | commune | rare | mort | ≈ 153 M$ (estimé CG) | CoinGecko `wall-street-memes` ; cap. ≈ 272 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 787 | Welsh Corgi Coin † | WELSH | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 146 M$ (estimé CG) | CoinGecko `welsh-corgi-coin` ; cap. ≈ 1,2 M$, volume 24 h ≈ 1 k$, écart -99,2 % |
| 788 | Wen † | WEN | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 372 M$ (estimé CG) | CoinGecko `wen-4` ; cap. ≈ 3,9 M$, volume 24 h ≈ 104 k$, écart -99,0 % |
| 789 | WhitePepe | WHITEPEPE | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 790 | WHY | WHY | garder |  | commune | rare | mort | ≈ 161 M$ (estimé CG) | CoinGecko `why` ; cap. ≈ 766 k$, volume 24 h ≈ 7 k$, écart -99,5 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 791 | Wise Monkey | MONKY | garder |  | commune | rare | mort | ≈ 232 M$ (estimé CG) | CoinGecko `wise-monkey` ; cap. ≈ 281 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 792 | Wojak Coin | WOJAK | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 143 M$ (estimé CG) | CoinGecko `wojak` ; cap. ≈ 1,4 M$, volume 24 h ≈ 1 k$, écart -99,0 % |
| 793 | Wojak Finance | WOJ | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 794 | Woman Yelling at Cat | WYAC | garder |  | commune | commune | mort | ≈ 57 M$ (estimé CG) | CoinGecko `woman-yelling-at-cat` ; cap. ≈ 133 k$, volume 24 h ≈ 8 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 795 | WSB Coin | WSB | garder |  | commune | commune | mort | ≈ 40 M$ (estimé CG) | CoinGecko `wsb-coin` ; cap. ≈ 122 k$, volume 24 h ≈ 0 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 796 | Yeet | YEET | garder |  | commune | commune | mort | ≈ 17 M$ (estimé CG) | CoinGecko `yeet` ; cap. ≈ 9 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 797 | Yellow Ket | KET | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 798 | YooShi | YOOSHI | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 4,19 Md$ (estimé CG) | CoinGecko `yooshi` ; cap. ≈ 2,2 M$, volume 24 h ≈ 0 k$, écart -99,9 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| 800 | 客服小何 (Customer Xiaohe) | KEFU | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 801 | 老子 | 老子 | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 15 M$ (estimé CG) | CoinGecko `laozi` ; cap. ≈ 396 k$, volume 24 h ≈ 377 k$, écart -97,3 % — rapprochement CoinGecko par ticker seul |
| 802 | 雪球 (Snowball) | 雪球 | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 14 M$ (estimé CG) | CoinGecko `xuequi` ; cap. ≈ 445 k$, volume 24 h ≈ 100 k$, écart -96,7 % |
| 803 | Jambo (meme-cooking) | JAMBO | garder |  | commune | commune | mort | ≈ 5,7 M$ (estimé CG) | CoinGecko `jambo-2` ; cap. ≈ 196 k$, volume 24 h ≈ 1 k$, écart -96,5 % |
| 804 | ABG | ABG | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 805 | GNEAR | GNEAR | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 806 | NOEAR | NOEAR | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| 807 | LOUD | LOUD | garder |  | commune | rare | mort | ≈ 17 M$ (estimé CG) | CoinGecko `loud` ; cap. ≈ 181 k$, volume 24 h ≈ 0 k$, écart -98,9 % |
| D1 | Official Trump | TRUMP | garder |  | légendaire | légendaire | en déclin (-95 % ou pire) | ≈ 14,60 Md$ (corrigé) | CoinGecko `official-trump` ; cap. ≈ 318 M$, volume 24 h ≈ 105 M$, écart -98,5 % |
| D2 | SafeMoon | SFM (ex-SAFEMOON) | garder |  | légendaire | légendaire | mort | ≈ 6,00 Md$ (sourcé) | CoinGecko `safemoon-2` ; catalogue (pic sourcé) ; cap. ≈ 151 k$, volume 24 h ≈ 0 k$, écart -100,0 % |
| D3 | Libra | LIBRA | garder |  | épique | légendaire | mort | ≈ 4,40 Md$ (sourcé) | CoinGecko `libra-5` ; catalogue (pic sourcé) ; cap. ≈ 927 k$, volume 24 h ≈ 0 k$, écart -99,6 % |
| D4 | YZY | YZY | garder |  | épique | légendaire | en déclin | ≈ 3,00 Md$ (sourcé) | CoinGecko `yzy` ; catalogue (pic sourcé) ; cap. ≈ 86 M$, volume 24 h ≈ 1 k$, écart -90,2 % |
| D5 | Siren | SIREN | retirer | agent IA DeFAI (Siren) | épique | — | en déclin (-95 % ou pire) | ≈ 2,18 Md$ (sourcé) | CoinGecko `siren-2` ; catalogue (pic sourcé) ; cap. ≈ 18 M$, volume 24 h ≈ 800 k$, écart -98,9 % |
| D6 | Melania Meme | MELANIA | garder |  | épique | légendaire | en déclin (-95 % ou pire) | ≈ 2,00 Md$ (sourcé) | CoinGecko `melania-meme` ; catalogue (pic sourcé) ; cap. ≈ 56 M$, volume 24 h ≈ 4,3 M$, écart -99,6 % |
| D7 | Hawk Tuah | HAWK | garder |  | rare | épique | mort | ≈ 500 M$ (sourcé) | CoinGecko `hawk-tuah` ; catalogue (pic sourcé) ; cap. ≈ 132 k$, volume 24 h ≈ 0 k$, écart -99,2 % |
| D8 | Normie | NORMIE | garder |  | rare | épique | en déclin (-95 % ou pire) | ≈ 130 M$ (sourcé) | CoinGecko `normie-6` ; catalogue (pic sourcé) ; cap. ≈ 1,3 M$, volume 24 h ≈ 11 k$, écart -95,0 % |
| D9 | Coinye | COINYE | garder |  | rare | épique | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé — histoire : Coinye : premier rug et procès de Kanye West (2014) |
| D10 | Squid Game | SQUID | garder |  | rare | légendaire | mort | ≈ 201 M$ (estimé CG) | CoinGecko `squid-game` ; cap. ≈ 39 k$, volume 24 h ≈ 0 k$, écart -100,0 % — histoire : SQUID : x 80 000 en une semaine puis rug, épisode culte; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D11 | Bald | BALD | garder |  | commune | épique | en déclin | ≈ 100 M$ (sourcé) | CoinGecko `bald` ; catalogue (pic sourcé) ; cap. ≈ 11 M$, volume 24 h ≈ 0 k$, écart -88,2 % |
| D12 | Boner Coin | BONER | garder |  | commune* | rare | en déclin | ≈ 82 M$ (estimé CG) | CoinGecko `boner-coin` ; cap. ≈ 4,5 M$, volume 24 h ≈ 275 k$, écart -94,5 % |
| D13 | Pussy Financial | PUSSY | garder |  | commune* | rare | mort | ≈ 65 M$ (estimé CG) | CoinGecko `pussy-financial` ; cap. ≈ 633 k$, volume 24 h ≈ 0 k$, écart -99,0 % |
| D14 | Gooncoin | GOONC | garder |  | commune | rare | mort | ≈ 68 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `gooncoin` ; cap. ≈ 23 k$, volume 24 h ≈ 0 k$, écart -100,0 % |
| D15 | Jenner | JENNER | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 44 M$ (sourcé) | catalogue (pic sourcé) |
| D16 | Hawk | HAWK | garder |  | commune* | rare | en déclin (-95 % ou pire) | ≈ 49 M$ (estimé CG) | CoinGecko `hawk-2` ; cap. ≈ 1,7 M$, volume 24 h ≈ 2 k$, écart -96,5 % — doublon possible de D7 Hawk Tuah |
| D17 | Wolf | WOLF | garder |  | commune | rare | en déclin | ≈ 40 M$ (sourcé) | CoinGecko `wolf-2` ; catalogue (pic sourcé) ; cap. ≈ 6,5 M$, volume 24 h ≈ 1 k$, écart -86,5 % |
| D18 | GrokCoin | GROKCOIN | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 34 M$ (sourcé) | catalogue (pic sourcé) |
| D19 | Ben Coin (BitBoy) | BEN | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 30 M$ (sourcé) | catalogue (pic sourcé) |
| D20 | Hulk Hogan | HULK | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 19 M$ (sourcé) | catalogue (pic sourcé) |
| D21 | Hoodrat | HOODRAT | garder |  | commune* | rare | mort | ≈ 17 M$ (estimé CG) | CoinGecko `hoodrat-4` ; cap. ≈ 732 k$, volume 24 h ≈ 11 k$, écart -95,7 % |
| D22 | SexCoin | SXC | retirer | monnaie de paiement de l'industrie adulte (SexCoin), utilitaire | commune | — | mort (absent de CoinGecko) | ≈ 18 M$ (sourcé) | catalogue (pic sourcé) |
| D23 | Chonketha the Wet Beaver | CHONKETHA | garder |  | commune* | rare | en déclin | ≈ 12 M$ (estimé CG) | CoinGecko `chonketha-the-wet-beaver` ; cap. ≈ 1,6 M$, volume 24 h ≈ 28 k$, écart -86,9 % |
| D24 | RKC | RKC | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 12 M$ (sourcé) | catalogue (pic sourcé) |
| D25 | Wanko | WANKO | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 10 M$ (sourcé) | catalogue (pic sourcé) |
| D26 | Red Kitten Crew | RKC | garder |  | commune* | commune | en déclin | ≈ 9,0 M$ (estimé CG) | CoinGecko `red-kitten-crew` ; cap. ≈ 634 k$, volume 24 h ≈ 30 k$, écart -93,0 % — doublon possible de D24 RKC |
| D27 | Fapcoin | FAPCOIN | garder |  | commune* | commune | en déclin | ≈ 7,9 M$ (estimé CG) | CoinGecko `fapcoin-4` ; cap. ≈ 1,5 M$, volume 24 h ≈ 123 k$, écart -80,4 % |
| D28 | CockCardano | COCK | garder |  | commune* | commune | mort | ≈ 7,4 M$ (estimé CG) | CoinGecko `cockcardano` ; cap. ≈ 696 k$, volume 24 h ≈ 1 k$, écart -90,6 % |
| D29 | Groyper | GROYP | garder |  | commune* | commune | actif | ≈ 4,1 M$ (estimé CG) | CoinGecko `groyper-3` ; cap. ≈ 1,5 M$, volume 24 h ≈ 11 k$, écart -64,3 % |
| D30 | MechaHitler | MECHAHITLER | garder |  | commune | commune | mort (absent de CoinGecko) | ≈ 2,2 M$ (sourcé) | catalogue (pic sourcé) |
| D31 | AIAI | AIAI | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D32 | Barron | BARRON | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D33 | Beratardio | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D34 | Bitconnect | BCC | retirer | plateforme de prêt frauduleuse (Bitconnect), pas un mème | commune | — | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D35 | Butthole Coin | BUTTHOLE | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 133 M$ (estimé CG) | CoinGecko `butthole-coin` ; cap. ≈ 340 k$, volume 24 h ≈ 29 k$, écart -99,7 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D36 | Chudjak | CHUD | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 32 M$ (estimé CG) | CoinGecko `chudjak` ; cap. ≈ 727 k$, volume 24 h ≈ 64 k$, écart -97,7 % |
| D37 | CR7 | CR7 | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D38 | CryptoZoo | ZOO | retirer | jeu NFT (CryptoZoo), pas un mème | commune | — | à vérifier (homonyme sur CoinGecko, non rapproché) | inconnu | catalogue ; absent du relevé |
| D39 | CumRocket † | CUMMIES | retirer | jeton d'une plateforme de contenus adultes (CumRocket), utilitaire | commune | — | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D40 | Daddy Tate | DADDY | garder |  | commune | épique | en déclin (-95 % ou pire) | ≈ 173 M$ (estimé CG) | CoinGecko `daddy-tate` ; cap. ≈ 3,2 M$, volume 24 h ≈ 139 k$, écart -98,1 % |
| D41 | DJT | DJT | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D42 | Doja | DOJA | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D43 | Elon Sperm | à vérifier | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D44 | Enron | ENRON | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D45 | EthereumMax | EMAX | garder |  | commune | commune | mort | inconnu | CoinGecko `ethereummax` — mème promu par des célébrités (Kardashian, SEC) |
| D46 | Funky | FUNKY | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D47 | Hood | HOOD | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D48 | Jason Derulo | JASON | garder |  | commune | commune | mort | ≈ 35 M$ (estimé CG) | CoinGecko `jason-derulo` ; cap. ≈ 34 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D49 | Jeton « Epstein » de McAfee | WHACKD (à vérifier) | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D50 | M3M3 | M3M3 | garder |  | commune | rare | mort | ≈ 187 M$ (estimé CG) | CoinGecko `m3m3` ; cap. ≈ 78 k$, volume 24 h ≈ 0 k$, écart -100,0 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D51 | Mates | MATES | garder |  | commune | commune | mort | ≈ 72 M$ (estimé CG) | CoinGecko `mates` ; cap. ≈ 46 k$, volume 24 h ≈ 0 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D52 | Mbappé | MBAPPE | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D53 | Retardio † | RETARDIO | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 242 M$ (estimé CG) | CoinGecko `retardio` ; cap. ≈ 848 k$, volume 24 h ≈ 42 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D54 | Rich the Kid | RICH | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D55 | RTR | RTR | garder |  | commune | commune | mort | ≈ 45 M$ (estimé CG) | CoinGecko `restore-the-republic` ; cap. ≈ 216 k$, volume 24 h ≈ 0 k$, écart -99,5 % — écart ≤ -99,5 % : estimation fragile, un cran de moins; rapprochement CoinGecko par ticker seul |
| D56 | Sydney Sweeney | SWEENEY | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D57 | Testicle | TESTICLE | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 23 M$ (estimé CG) | CoinGecko `testicle` ; cap. ≈ 141 k$, volume 24 h ≈ 27 k$, écart -99,4 % |
| D58 | Titcoin | TIT | retirer | monnaie de paiement de l'industrie adulte (Titcoin), utilitaire | commune | — | mort | inconnu | CoinGecko `titcoin-2` |
| D59 | TrumpCoin | DJT | garder |  | commune | rare | mort | ≈ 183 M$ (estimé CG) | CoinGecko `trumpcoin` ; cap. ≈ 759 k$, volume 24 h ≈ 0 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins; doublon possible de D41 DJT |
| D60 | Trust | TRUST | garder |  | commune | rare | en déclin | ≈ 73 M$ (estimé CG) | CoinGecko `trust-3` ; cap. ≈ 4,3 M$, volume 24 h ≈ 0 k$, écart -94,0 % |
| D61 | Vantard | VANTARD | garder |  | commune | commune | mort (absent de CoinGecko) | inconnu | catalogue ; absent du relevé |
| D62 | Whoren | WHOREN | garder |  | commune | commune | mort | ≈ 38 M$ (estimé CG) | CoinGecko `elizabath-whoren` ; cap. ≈ 19 k$, volume 24 h ≈ 0 k$, écart -100,0 % — écart ≤ -99,5 % : estimation fragile, un cran de moins; rapprochement CoinGecko par ticker seul |
| D63 | 我踏马来了 | 我踏马来了 | garder |  | commune | rare | en déclin | ≈ 62 M$ (estimé CG) | CoinGecko `wo-ta-ma-laile` ; cap. ≈ 7,8 M$, volume 24 h ≈ 663 k$, écart -87,5 % |
| D64 | America Party | AMERICA | garder |  | rare* | épique | en déclin (-95 % ou pire) | ≈ 643 M$ (estimé CG) | CoinGecko `america-party-5` ; cap. ≈ 30 M$, volume 24 h ≈ 0 k$, écart -95,3 % |
| D65 | MAGA | TRUMP (ERC-20) | garder |  | rare | épique | mort | ≈ 788 M$ (estimé CG, au-dessus de la borne sourcée) | CoinGecko `maga` ; cap. ≈ 876 k$, volume 24 h ≈ 0 k$, écart -99,9 % |
| D66 | AGENDA 47 | A47 | garder |  | commune* | rare | mort | ≈ 41 M$ (estimé CG) | CoinGecko `agenda-47` ; cap. ≈ 724 k$, volume 24 h ≈ 4 k$, écart -98,2 % |
| D67 | Danold Tromp | DANOLD | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 15 M$ (sourcé) | catalogue (pic sourcé) |
| D68 | PutinCoin | PUT | garder |  | commune | rare | mort (absent de CoinGecko) | ≈ 11 M$ (sourcé) | catalogue (pic sourcé) |
| D69 | Central African Republic Meme | CAR | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 770 M$ (estimé CG) | CoinGecko `central-african-republic-meme` ; cap. ≈ 1,8 M$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D70 | Doland Tremp | TREMP | garder |  | commune | rare | mort | ≈ 151 M$ (estimé CG) | CoinGecko `donald-tremp` ; cap. ≈ 294 k$, volume 24 h ≈ 1 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D71 | Hunter Biden's Laptop | LAPTOP | garder |  | commune | rare | en déclin (-95 % ou pire) | ≈ 34,13 Md$ (estimé CG) | CoinGecko `hunter-biden-s-laptop-3` ; cap. ≈ 4,2 M$, volume 24 h ≈ 1,3 M$, écart -100,0 % — estimé ≥ 1 Md$ non confirmé : plafonné à épique; écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D72 | Hunter Boden | HUNTER | garder |  | commune | commune | mort | ≈ 4,5 M$ (estimé CG) | CoinGecko `hunter-boden` ; cap. ≈ 24 k$, volume 24 h ≈ 0 k$, écart -99,5 % |
| D73 | Jeo Boden | BODEN | garder |  | commune | rare | mort | ≈ 718 M$ (estimé CG) | CoinGecko `jeo-boden` ; cap. ≈ 739 k$, volume 24 h ≈ 8 k$, écart -99,9 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D74 | Kamala Horris † | KAMA | garder |  | commune | rare | mort | ≈ 39 M$ (estimé CG) | CoinGecko `kamala-horris` ; cap. ≈ 310 k$, volume 24 h ≈ 3 k$, écart -99,2 % |
| D75 | MAGA Hat | MAGA | garder |  | commune | rare | mort | ≈ 305 M$ (estimé CG) | CoinGecko `maga-hat` ; cap. ≈ 472 k$, volume 24 h ≈ 2 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D76 | Super Trump | STRUMP | garder |  | commune | commune | mort | ≈ 68 M$ (estimé CG) | CoinGecko `super-trump` ; cap. ≈ 135 k$, volume 24 h ≈ 0 k$, écart -99,8 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |
| D77 | TrumpCoin † | TRUMP | garder |  | commune | rare | mort | ≈ 183 M$ (estimé CG) | CoinGecko `trumpcoin` ; cap. ≈ 759 k$, volume 24 h ≈ 0 k$, écart -99,6 % — écart ≤ -99,5 % : estimation fragile, un cran de moins |

## (c) Candidats « anciens morts » absents du catalogue

Jetons du relevé non rapprochés d'une carte, pic estimé ≥ 10 M$, écart ≤ -95 %. Versions enveloppées, Binance-Peg et actions tokenisées exclues. **290 jetons à estimation exploitable** (écart entre -95 et -99,5 %) dans le premier tableau ; **957 à estimation fragile** (écart ≤ -99,5 %), dont 940 sous 1 Md$ listés dans le second tableau ; les 17 restants (pics estimés de plus de 1 Md$ avec -99,5 % ou pire) sont des artefacts d'offre et ne sont pas listés. La rareté indiquée applique les mêmes règles qu'en (b) ; elle est indicative.

### C1. Estimation exploitable

| CoinGecko id | Nom | Ticker | Pic estimé | Date du plus haut | Écart | Cap. actuelle | Rareté v2 indicative | Remarque |
|---|---|---|---|---|---|---|---|---|
| `slerf` | Slerf [OLD] | SLERF | ≈ 652 M$ | 2024-03-18 | -98,8 % | ≈ 8,0 M$ | épique | copie ou ancienne version d'une carte |
| `kekius-maximus` | Kekius Maximus | KEKIUS | ≈ 401 M$ | 2025-01-01 | -98,9 % | ≈ 4,4 M$ | épique | copie ou ancienne version d'une carte |
| `hatom` | Hatom | HTM | ≈ 357 M$ | 2023-12-09 | -98,7 % | ≈ 4,8 M$ | épique |  |
| `ahatoken` | AhaToken | AHT | ≈ 284 M$ | 2021-04-02 | -97,6 % | ≈ 6,8 M$ | épique |  |
| `aavegotchi` | Aavegotchi | GHST | ≈ 192 M$ | 2024-04-01 | -98,6 % | ≈ 2,6 M$ | épique |  |
| `bertram-the-pomeranian` | Bertram The Pomeranian | BERT | ≈ 184 M$ | 2024-11-15 | -95,1 % | ≈ 9,0 M$ | épique |  |
| `moo-deng-2` | MOO DENG | MOODENG | ≈ 177 M$ | 2024-11-19 | -99,4 % | ≈ 1,0 M$ | épique | copie ou ancienne version d'une carte |
| `-6` | "　" | "　" | ≈ 174 M$ | 2024-12-07 | -99,5 % | ≈ 877 k$ | épique | mort |
| `keyboard-cat-base` | Keyboard Cat (Base) | KEYCAT | ≈ 158 M$ | 2024-11-15 | -97,3 % | ≈ 4,3 M$ | épique |  |
| `sigma` | Sigma | SIGMA | ≈ 155 M$ | 2024-11-10 | -99,4 % | ≈ 986 k$ | épique | mort |
| `torch-of-liberty` | Torch of Liberty | LIBERTY | ≈ 145 M$ | 2025-08-15 | -99,4 % | ≈ 920 k$ | épique | mort |
| `wuffi` | WUFFI | WUF | ≈ 138 M$ | 2024-07-21 | -99,3 % | ≈ 968 k$ | épique | mort |
| `mimbogamegroup` | MimboGameGroup | MGG | ≈ 131 M$ | 2026-04-01 | -99,3 % | ≈ 892 k$ | épique | nature à vérifier; mort |
| `troll` | Troll | TROLL | ≈ 129 M$ | 2024-01-16 | -99,5 % | ≈ 663 k$ | épique | mort |
| `minimini` | mini | MINI | ≈ 85 M$ | 2024-10-13 | -99,4 % | ≈ 472 k$ | rare |  |
| `pooh` | POOH | POOH | ≈ 82 M$ | 2023-05-06 | -98,8 % | ≈ 989 k$ | rare | mort |
| `ping` | Ping | PING | ≈ 79 M$ | 2025-10-25 | -99,5 % | ≈ 408 k$ | rare | mort |
| `aerobud` | AEROBUD | AEROBUD | ≈ 73 M$ | 2024-12-06 | -99,4 % | ≈ 472 k$ | rare | mort |
| `araistotle` | ArAIstotle | FACY | ≈ 73 M$ | 2025-10-05 | -99,3 % | ≈ 475 k$ | rare | mort |
| `mstr2100` | MSTR2100 | MSTR | ≈ 72 M$ | 2024-11-08 | -99,5 % | ≈ 369 k$ | rare |  |
| `carrot-by-puffer` | Carrot by Puffer | CARROT | ≈ 66 M$ | 2025-01-31 | -98,2 % | ≈ 1,2 M$ | rare |  |
| `guacamole` | Guacamole | GUAC | ≈ 64 M$ | 2024-03-08 | -99,3 % | ≈ 422 k$ | rare | mort |
| `wall-street-pepe` | Wall Street Pepe | WEPE | ≈ 63 M$ | 2025-02-17 | -98,5 % | ≈ 928 k$ | rare |  |
| `war` | WAR [OLD] | WAR | ≈ 63 M$ | 2026-03-06 | -99,1 % | ≈ 564 k$ | rare | copie ou ancienne version d'une carte; mort |
| `wojak-4` | Wojak | WOJAK | ≈ 62 M$ | 2025-11-28 | -98,1 % | ≈ 1,2 M$ | rare | copie ou ancienne version d'une carte |
| `shikoku` | Shikoku | SHIK | ≈ 59 M$ | 2023-01-04 | -99,5 % | ≈ 300 k$ | rare | mort |
| `gorbagana` | Gorbagana | GOR | ≈ 57 M$ | 2025-06-21 | -99,2 % | ≈ 429 k$ | rare |  |
| `lets-go-brandon` | Lets Go Brandon | LETSGO | ≈ 55 M$ | 2022-03-02 | -99,3 % | ≈ 405 k$ | rare | mort |
| `private-aviation-finance-token` | Private Aviation Finance Token | CINO | ≈ 53 M$ | 2025-08-13 | -95,5 % | ≈ 2,4 M$ | rare | nature à vérifier |
| `bullish-degen` | Bullish Degen | BULLISH | ≈ 52 M$ | 2025-11-29 | -99,4 % | ≈ 302 k$ | rare |  |
| `any-inu` | Any Inu | AI | ≈ 51 M$ | 2024-03-04 | -99,3 % | ≈ 335 k$ | rare | mort |
| `ton-fish-memecoin` | TON FISH MEMECOIN | FISH | ≈ 50 M$ | 2024-03-17 | -99,2 % | ≈ 373 k$ | rare | mort |
| `customer-service-xiao-he` | 客服小何 (Customer Service Xiao He) | 客服小何 | ≈ 49 M$ | 2025-10-09 | -96,5 % | ≈ 1,7 M$ | rare |  |
| `trog` | Trog | TROG | ≈ 49 M$ | 2024-06-05 | -99,2 % | ≈ 383 k$ | rare | mort |
| `ftmtoken` | FTMTOKEN | FTMX | ≈ 49 M$ | 2025-09-25 | -97,9 % | ≈ 1,0 M$ | rare |  |
| `the-balkan-dwarf` | The Balkan Dwarf | $KEKEC | ≈ 48 M$ | 2024-11-06 | -99,1 % | ≈ 425 k$ | rare | mort |
| `terminus-2` | Terminus | TERMINUS | ≈ 48 M$ | 2024-09-23 | -99,2 % | ≈ 372 k$ | rare | mort |
| `chickencoin` | Chickencoin | CHKN | ≈ 48 M$ | 2024-04-02 | -98,0 % | ≈ 972 k$ | rare | mort |
| `goldenboys` | GoldenBoys | GOLD | ≈ 48 M$ | 2024-07-28 | -98,1 % | ≈ 895 k$ | rare | mort |
| `brett-memecoin` | Brett (ETH) | BRETT | ≈ 45 M$ | 2024-09-26 | -99,1 % | ≈ 424 k$ | rare | mort |
| `xdoge-2` | XDOGE | XDOGE | ≈ 45 M$ | 2024-11-21 | -97,5 % | ≈ 1,1 M$ | rare |  |
| `coding-dino` | Coding Dino | DINO | ≈ 44 M$ | 2025-05-21 | -97,3 % | ≈ 1,2 M$ | rare |  |
| `fourcoin` | FourCoin | FOUR | ≈ 43 M$ | 2023-05-09 | -99,0 % | ≈ 443 k$ | rare | mort |
| `frodo-the-virtual-samurai` | Frodo the Virtual Samurai | FROG | ≈ 43 M$ | 2024-12-19 | -98,9 % | ≈ 467 k$ | rare | mort |
| `waffles` | Waffles | WAFFLES | ≈ 42 M$ | 2024-06-07 | -99,0 % | ≈ 417 k$ | rare | mort |
| `1-coin-can-change-your-life` | 1 Coin Can Change Your Life | 1-COIN-CAN-CHANGE-YOUR-LIFE | ≈ 42 M$ | 2025-11-05 | -99,3 % | ≈ 307 k$ | rare |  |
| `simmi-token` | Simmi Token | SIMMI | ≈ 42 M$ | 2024-12-04 | -99,4 % | ≈ 257 k$ | rare | mort |
| `opus-2` | Opus Genesis | OPUS | ≈ 42 M$ | 2024-11-28 | -99,4 % | ≈ 264 k$ | rare | mort |
| `doge-1-satellite` | DOGE-1 Satellite | DOGE-1 | ≈ 41 M$ | 2025-09-15 | -98,8 % | ≈ 510 k$ | rare | mort |
| `america-party-4` | America Party | AP | ≈ 41 M$ | 2025-07-07 | -99,4 % | ≈ 227 k$ | rare | copie ou ancienne version d'une carte; mort |
| `swasticoin` | Swasticoin | YZY | ≈ 41 M$ | 2025-03-15 | -98,8 % | ≈ 479 k$ | rare | mort |
| `stupidcoin-2` | StupidCoin | STUPID | ≈ 40 M$ | 2025-01-27 | -99,4 % | ≈ 231 k$ | rare |  |
| `bibi` | BIBI | BIBI | ≈ 40 M$ | 2024-03-06 | -99,4 % | ≈ 251 k$ | rare | mort |
| `stanley-cup-coin` | STAN | STAN | ≈ 39 M$ | 2024-05-04 | -99,3 % | ≈ 271 k$ | rare | mort |
| `real-smurf-cat` | Real Smurf Cat | SMURFCAT | ≈ 39 M$ | 2023-10-27 | -99,1 % | ≈ 341 k$ | rare | mort |
| `moai` | MOAI | MOAI | ≈ 39 M$ | 2024-11-05 | -99,5 % | ≈ 198 k$ | rare | mort |
| `npc-on-solana` | NPC On Solana | NPCS | ≈ 39 M$ | 2024-10-17 | -99,0 % | ≈ 379 k$ | rare | mort |
| `honk` | Honk | HONK | ≈ 39 M$ | 2024-03-09 | -99,3 % | ≈ 274 k$ | rare | mort |
| `au79` | AU79 | AU79 | ≈ 38 M$ | 2025-09-13 | -98,9 % | ≈ 414 k$ | rare | mort |
| `tao-inu` | TAO INU | TAONU | ≈ 38 M$ | 2024-03-17 | -99,5 % | ≈ 196 k$ | rare | mort |
| `tdoge` | τDoge | TDOGE | ≈ 38 M$ | 2021-06-03 | -99,4 % | ≈ 226 k$ | rare | mort |
| `bonkearn` | BonkEarn | BERN | ≈ 38 M$ | 2023-11-23 | -97,3 % | ≈ 1,0 M$ | rare |  |
| `san-chan` | San Chan | SAN | ≈ 37 M$ | 2025-02-02 | -98,9 % | ≈ 422 k$ | rare | mort |
| `fric` | FRIC | FRIC | ≈ 36 M$ | 2024-12-10 | -98,8 % | ≈ 417 k$ | rare | mort |
| `ainu-token` | Ainu | AINU | ≈ 36 M$ | 2021-10-17 | -99,1 % | ≈ 330 k$ | rare | mort |
| `n3on` | N3on | N3ON | ≈ 35 M$ | 2025-11-12 | -98,9 % | ≈ 386 k$ | rare | mort |
| `neiro-2` | Neiro | NEIRO | ≈ 35 M$ | 2024-07-28 | -99,2 % | ≈ 268 k$ | rare | copie ou ancienne version d'une carte; mort |
| `catgpt` | CatGPT | CATGPT | ≈ 35 M$ | 2024-04-25 | -99,2 % | ≈ 266 k$ | rare | mort |
| `what-if-3` | What IF | IF | ≈ 35 M$ | 2026-08-02 | -99,2 % | ≈ 263 k$ | rare | mort |
| `xiuxian` | 修仙 (XiuXian) | 修仙 | ≈ 35 M$ | 2025-10-13 | -98,5 % | ≈ 509 k$ | rare |  |
| `pup` | PUP | PUP | ≈ 35 M$ | 2025-10-08 | -99,4 % | ≈ 190 k$ | rare |  |
| `shifu` | Shifu | SHIFU | ≈ 34 M$ | 2024-12-20 | -99,1 % | ≈ 302 k$ | rare | mort |
| `degen-zoo` | Degen Zoo | DZOO | ≈ 34 M$ | 2023-03-16 | -99,2 % | ≈ 282 k$ | rare | mort |
| `alright-buddy` | alright buddy | BUDDY | ≈ 34 M$ | 2025-05-25 | -99,0 % | ≈ 355 k$ | rare | mort |
| `huhu-cat` | Huhu Cat | HUHU | ≈ 34 M$ | 2024-03-27 | -99,4 % | ≈ 190 k$ | rare | mort |
| `spinning-cat` | Spinning Cat | OIIAOIIA | ≈ 32 M$ | 2025-01-04 | -99,3 % | ≈ 221 k$ | rare | mort |
| `the-stonks-exchange` | The Stonks Exchange | STONKEX | ≈ 32 M$ | 2026-09-06 | -96,9 % | ≈ 990 k$ | rare |  |
| `fine` | FINE | FINE | ≈ 32 M$ | 2023-09-15 | -99,4 % | ≈ 184 k$ | rare | mort |
| `mcpepe-s` | McPepe's | PEPES | ≈ 32 M$ | 2024-04-28 | -99,2 % | ≈ 249 k$ | rare | mort |
| `daku-v2` | Daku V2 | DAKU | ≈ 31 M$ | 2025-10-05 | -98,9 % | ≈ 346 k$ | rare | mort |
| `dickbutt` | Dickbutt | DICKBUTT | ≈ 31 M$ | 2025-01-06 | -98,6 % | ≈ 414 k$ | rare | mort |
| `hami` | HAMI | $HAMI | ≈ 31 M$ | 2024-03-29 | -99,5 % | ≈ 153 k$ | rare | mort |
| `toby-toadgod` | Toby ToadGod | TOBY | ≈ 30 M$ | 2024-04-10 | -97,6 % | ≈ 725 k$ | rare | mort |
| `mystery-2` | Mystery | MYSTERY | ≈ 30 M$ | 2024-12-24 | -99,4 % | ≈ 174 k$ | rare |  |
| `luna-inu` | Luna Inu | LINU | ≈ 30 M$ | 2024-03-13 | -98,9 % | ≈ 337 k$ | rare | mort |
| `flybrain` | flybrain | FLYBRAIN | ≈ 29 M$ | 2026-09-11 | -99,3 % | ≈ 200 k$ | rare |  |
| `husky-avax` | Husky Avax | HUSKY | ≈ 29 M$ | 2021-10-28 | -99,5 % | ≈ 148 k$ | rare | mort |
| `catwifmask` | catwifmask | MASK | ≈ 29 M$ | 2025-06-11 | -96,9 % | ≈ 904 k$ | rare |  |
| `cocoro-2` | Cocoro | COCORO | ≈ 29 M$ | 2025-05-21 | -99,4 % | ≈ 184 k$ | rare | copie ou ancienne version d'une carte |
| `generational-wealth` | Generational Wealth | GEN | ≈ 29 M$ | 2023-05-18 | -99,5 % | ≈ 153 k$ | rare | mort |
| `nutcoin-meme` | NutCoin | NUT | ≈ 29 M$ | 2024-11-25 | -99,2 % | ≈ 233 k$ | rare |  |
| `aqua-goat` | Aqua Goat | AQUAGOAT | ≈ 29 M$ | 2021-10-10 | -99,3 % | ≈ 208 k$ | rare | mort |
| `smolcoin` | Smolcoin [OLD] | SMOL | ≈ 29 M$ | 2025-01-01 | -99,0 % | ≈ 274 k$ | rare | mort |
| `elonrwa` | ElonRWA | ELONRWA | ≈ 28 M$ | 2024-11-15 | -98,2 % | ≈ 522 k$ | rare | mort |
| `milady-wif-hat` | Milady Wif Hat | LADYF | ≈ 28 M$ | 2024-05-22 | -98,8 % | ≈ 346 k$ | rare | mort |
| `shikelang` | 屎壳郎 (Dung Beetle) | 屎壳郎 | ≈ 28 M$ | 2026-07-09 | -96,7 % | ≈ 925 k$ | rare | mort |
| `justanegg-2` | JustAnEgg | EGG | ≈ 28 M$ | 2024-04-04 | -99,0 % | ≈ 291 k$ | rare | mort |
| `wassie` | WASSIE | WASSIE | ≈ 27 M$ | 2024-03-13 | -99,1 % | ≈ 235 k$ | rare | mort |
| `business-coin` | Business Coin | BUSINESS | ≈ 27 M$ | 2025-01-31 | -99,4 % | ≈ 167 k$ | rare | mort |
| `sroomai-dao` | SroomAI DAO | SHR0 | ≈ 27 M$ | 2025-05-22 | -99,5 % | ≈ 140 k$ | rare | nature à vérifier; mort |
| `shibaai` | SHIBAAI | SHIBAAI | ≈ 27 M$ | 2024-03-06 | -99,4 % | ≈ 165 k$ | rare | mort |
| `cheese-3` | Cheese | CHEESE | ≈ 27 M$ | 2024-11-20 | -99,5 % | ≈ 144 k$ | rare | mort |
| `pepe-0x69-on-base` | PEPE 0x69 ON BASE | PEPE | ≈ 26 M$ | 2024-05-23 | -99,4 % | ≈ 154 k$ | rare |  |
| `manifest-on-sol` | Manifest | MANIFEST | ≈ 26 M$ | 2024-11-10 | -99,5 % | ≈ 139 k$ | rare | mort |
| `swag` | Swag | $SWAG | ≈ 26 M$ | 2024-11-13 | -99,5 % | ≈ 137 k$ | rare | mort |
| `robin-the-frog` | Robin the Frog | ROBIN | ≈ 26 M$ | 2026-09-06 | -98,7 % | ≈ 344 k$ | rare |  |
| `-5` | 🟥🟪🟦🟩🟨🟧 | 🟥🟩 | ≈ 26 M$ | 2024-11-19 | -99,0 % | ≈ 248 k$ | rare | mort |
| `ic-ghost` | IC Ghost | GHOST | ≈ 25 M$ | 2024-01-04 | -99,4 % | ≈ 152 k$ | rare | mort |
| `googles` | GOGGLES | GOGLZ | ≈ 25 M$ | 2025-02-20 | -99,5 % | ≈ 125 k$ | rare | mort |
| `parabolic-3` | Parabolic | PARAX | ≈ 25 M$ | 2025-05-30 | -99,5 % | ≈ 128 k$ | rare | mort |
| `noggles` | Noggles | NOGS | ≈ 25 M$ | 2024-04-23 | -99,3 % | ≈ 181 k$ | rare | mort |
| `russell` | RUSSELL | RUSSELL | ≈ 25 M$ | 2024-11-13 | -96,3 % | ≈ 902 k$ | rare | mort |
| `valhalla-index` | Odin Liquidity Network | ODIN | ≈ 24 M$ | 2024-12-03 | -98,7 % | ≈ 323 k$ | rare | nature à vérifier; mort |
| `chaos-2` | Chaos | CHAOS | ≈ 24 M$ | 2024-12-31 | -98,8 % | ≈ 277 k$ | rare | mort |
| `up-token-2` | uP Token | UP | ≈ 24 M$ | 2023-12-01 | -95,8 % | ≈ 986 k$ | rare | mort |
| `dork` | DORK | DORK | ≈ 23 M$ | 2023-11-04 | -99,4 % | ≈ 131 k$ | rare | mort |
| `peepo` | Peepo | PEEPO | ≈ 23 M$ | 2023-05-05 | -99,4 % | ≈ 144 k$ | rare | mort |
| `burnie-senders` | Burnie Senders | BURNIE | ≈ 23 M$ | 2026-04-26 | -98,7 % | ≈ 303 k$ | rare |  |
| `broccoli-4` | Broccoli | BROCCOLI | ≈ 23 M$ | 2025-02-19 | -96,9 % | ≈ 726 k$ | rare | copie ou ancienne version d'une carte |
| `bian-holder` | 币安Holder | BNBHOLDER | ≈ 23 M$ | 2025-10-14 | -97,8 % | ≈ 498 k$ | rare |  |
| `smiley-coin` | Smiley Coin | SMILEY | ≈ 23 M$ | 2024-01-16 | -98,8 % | ≈ 276 k$ | rare | mort |
| `red-hare-coin` | Red Hare Coin | RHC | ≈ 23 M$ | 2026-04-26 | -96,1 % | ≈ 883 k$ | rare | mort |
| `success-kid` | Success Kid | SKID | ≈ 23 M$ | 2024-03-18 | -99,5 % | ≈ 116 k$ | rare | mort |
| `haycoin` | HayCoin | HAY | ≈ 23 M$ | 2023-10-25 | -99,2 % | ≈ 173 k$ | rare | mort |
| `wifejak` | Wifejak | WIFE | ≈ 22 M$ | 2024-11-28 | -99,4 % | ≈ 133 k$ | rare | mort |
| `bird-dog` | Bird Dog | BIRDDOG | ≈ 22 M$ | 2024-06-10 | -99,0 % | ≈ 216 k$ | rare | mort |
| `toad-sol` | Toad (SOL) | $TOAD | ≈ 22 M$ | 2024-11-02 | -98,8 % | ≈ 256 k$ | rare | mort |
| `nobiko-coin` | Nobiko Coin | LONG | ≈ 22 M$ | 2025-10-13 | -99,1 % | ≈ 207 k$ | rare | mort |
| `888-token` | 888 | 888 | ≈ 22 M$ | 2024-11-30 | -99,2 % | ≈ 174 k$ | rare | mort |
| `mustaaaaaard` | MUSTAAAAAARD | MUSTARD | ≈ 22 M$ | 2024-11-27 | -99,4 % | ≈ 141 k$ | rare | mort |
| `pepe-token` | Pepe Community | PEPE | ≈ 22 M$ | 2023-08-28 | -99,3 % | ≈ 151 k$ | rare | mort |
| `catalorian` | Catalorian | CATALORIAN | ≈ 22 M$ | 2025-08-18 | -99,4 % | ≈ 138 k$ | rare | mort |
| `supercycle-real` | supercycle(real) | SUPERCYCLE | ≈ 22 M$ | 2024-11-13 | -99,0 % | ≈ 207 k$ | rare | mort |
| `landwolf-eth` | Landwolf | WOLF | ≈ 21 M$ | 2024-04-22 | -98,6 % | ≈ 306 k$ | rare | copie ou ancienne version d'une carte; mort |
| `sanin-inu` | Sanin Inu | SANI | ≈ 21 M$ | 2024-03-13 | -99,5 % | ≈ 113 k$ | rare | mort |
| `base-is-for-everyone` | Base is for everyone | BASEISFOREVERYONE | ≈ 21 M$ | 2025-04-16 | -99,0 % | ≈ 207 k$ | rare | mort |
| `lets-bonk` | Let's BONK | LETSBONK | ≈ 21 M$ | 2025-04-26 | -99,1 % | ≈ 186 k$ | rare |  |
| `yolo-2` | YOLO | YOLO | ≈ 21 M$ | 2026-08-30 | -98,3 % | ≈ 364 k$ | rare | mort |
| `baby-pepe-3` | Baby Pepe | BABYPEPE | ≈ 21 M$ | 2024-11-13 | -98,5 % | ≈ 313 k$ | rare | mort |
| `popdog` | POPDOG | POPDOG | ≈ 21 M$ | 2024-09-25 | -98,5 % | ≈ 304 k$ | rare | mort |
| `oscar` | OSCAR | OSCAR | ≈ 20 M$ | 2024-10-21 | -97,9 % | ≈ 427 k$ | rare | mort |
| `bcoq-inu` | BCOQ INU | BCOQ | ≈ 20 M$ | 2024-03-13 | -99,4 % | ≈ 127 k$ | rare |  |
| `babysnek` | BabySNEK | BBSNEK | ≈ 20 M$ | 2024-12-11 | -97,7 % | ≈ 450 k$ | rare | mort |
| `ribbit-2` | RIBBIT | RBT | ≈ 20 M$ | 2024-09-24 | -98,7 % | ≈ 258 k$ | rare | mort |
| `pepa-inu` | Pepa Inu | PEPA | ≈ 20 M$ | 2023-04-21 | -99,2 % | ≈ 166 k$ | rare | mort |
| `meowcoin` | Meowcoin | MEWC | ≈ 20 M$ | 2022-10-09 | -99,2 % | ≈ 161 k$ | rare | mort |
| `shibwifhatcoin` | Shibwifhatcoin | SHIB | ≈ 19 M$ | 2024-03-11 | -98,7 % | ≈ 258 k$ | rare | mort |
| `catgpt-3` | CATGPT | CATGPT | ≈ 19 M$ | 2026-09-12 | -98,2 % | ≈ 350 k$ | rare | mort |
| `stonks-9` | Stonks | STONKS | ≈ 19 M$ | 2026-09-06 | -99,3 % | ≈ 143 k$ | rare | copie ou ancienne version d'une carte |
| `mars-2` | Mars | MARS | ≈ 19 M$ | 2024-09-30 | -99,5 % | ≈ 100 k$ | rare |  |
| `dna` | DNA | DNA | ≈ 19 M$ | 2024-12-06 | -99,1 % | ≈ 165 k$ | rare | mort |
| `kira-the-injective-cat` | Kira the Injective Cat | KIRA | ≈ 19 M$ | 2024-03-13 | -98,6 % | ≈ 255 k$ | rare | mort |
| `walter-dog-solana` | Walter | WALTER | ≈ 19 M$ | 2024-06-01 | -99,3 % | ≈ 138 k$ | rare | mort |
| `baby-doge-cash` | Baby Doge Cash | BABYDOGECASH | ≈ 19 M$ | 2021-07-04 | -97,7 % | ≈ 436 k$ | rare | mort |
| `kabosu-inu` | Kabosu Inu | KABOSU | ≈ 19 M$ | 2024-05-23 | -99,4 % | ≈ 109 k$ | rare | mort |
| `bitcoin-2-0` | Bitcoin 2.0 | BTC2.0 | ≈ 19 M$ | 2023-07-16 | -98,7 % | ≈ 238 k$ | rare | mort |
| `flying-avocado-cat` | Flying Avocado Cat | FAC | ≈ 19 M$ | 2024-09-20 | -99,3 % | ≈ 124 k$ | rare | mort |
| `asteroid-the-space-shiba-inu` | Asteroid The Space Shiba Inu | ASTEROID | ≈ 19 M$ | 2026-05-13 | -98,7 % | ≈ 248 k$ | rare | mort |
| `leopard` | Leopard | LEOPARD | ≈ 18 M$ | 2021-10-16 | -98,6 % | ≈ 249 k$ | rare | mort |
| `luffy-inu` | Luffy | LUFFY | ≈ 18 M$ | 2024-12-13 | -99,0 % | ≈ 174 k$ | rare | mort |
| `orc` | ORC | ORC | ≈ 18 M$ | 2024-07-21 | -99,4 % | ≈ 116 k$ | rare | mort |
| `build-5` | build | BUILD | ≈ 18 M$ | 2026-09-09 | -99,4 % | ≈ 105 k$ | rare | mort |
| `coal-2` | COAL | COAL | ≈ 18 M$ | 2025-11-09 | -98,9 % | ≈ 192 k$ | rare | mort |
| `echelon-token` | Echelon Token | ELON | ≈ 18 M$ | 2026-02-02 | -97,0 % | ≈ 530 k$ | rare | mort |
| `perry` | Perry | PERRY | ≈ 18 M$ | 2025-02-19 | -99,4 % | ≈ 108 k$ | rare | mort |
| `haha` | HAHA | HAHA | ≈ 17 M$ | 2023-05-06 | -99,2 % | ≈ 137 k$ | rare | mort |
| `young-peezy-aka-pepe` | Young Peezy AKA Pepe | PEEZY | ≈ 17 M$ | 2024-04-27 | -98,6 % | ≈ 248 k$ | rare | mort |
| `pepe-trump` | Pepe Trump | PTRUMP | ≈ 17 M$ | 2024-05-28 | -99,0 % | ≈ 170 k$ | rare | mort |
| `groyper` | Groyper | GROYPER | ≈ 17 M$ | 2024-05-28 | -99,1 % | ≈ 156 k$ | rare | copie ou ancienne version d'une carte; mort |
| `lord-of-sol` | Lord Of SOL | LOS | ≈ 17 M$ | 2024-05-10 | -99,3 % | ≈ 122 k$ | rare | mort |
| `copper-inu-2` | Copper (inu) | COPPERINU | ≈ 17 M$ | 2026-08-29 | -99,4 % | ≈ 110 k$ | rare |  |
| `bober` | BOBER | BOBER | ≈ 17 M$ | 2024-03-25 | -98,6 % | ≈ 232 k$ | rare | mort |
| `gemini-2` | Gemini | GEMINI | ≈ 17 M$ | 2024-12-15 | -99,2 % | ≈ 131 k$ | rare | mort |
| `baby-neiro-2` | Baby Neiro | BABYNEIRO | ≈ 17 M$ | 2024-11-19 | -99,5 % | ≈ 86 k$ | rare | mort |
| `chadimir-putni` | Chadimir Putni | PUTNI | ≈ 17 M$ | 2024-03-25 | -98,8 % | ≈ 200 k$ | rare | mort |
| `floppa-cat` | Floppa | FLOPPA | ≈ 17 M$ | 2024-11-15 | -99,5 % | ≈ 86 k$ | rare | mort |
| `velvet-unicorn-by-virtuals` | Velvet Unicorn by Virtuals | VU | ≈ 17 M$ | 2024-12-31 | -99,3 % | ≈ 122 k$ | rare | mort |
| `onecow` | OneCOW |  1COW | ≈ 17 M$ | 2026-09-27 | -97,1 % | ≈ 480 k$ | rare | mort |
| `shit-piss-skin-can` | Shit Piss Skin Can | SPSC | ≈ 17 M$ | 2026-01-02 | -99,1 % | ≈ 153 k$ | rare |  |
| `toad-killer` | Toad Killer | $TOAD | ≈ 17 M$ | 2023-08-16 | -98,2 % | ≈ 300 k$ | rare | mort |
| `fish-n-chips` | Fish N Chips | CHIPPY | ≈ 16 M$ | 2024-05-19 | -98,0 % | ≈ 330 k$ | rare | mort |
| `fishkoin` | Fishkoin | KOIN | ≈ 16 M$ | 2024-03-24 | -99,4 % | ≈ 100 k$ | rare | mort |
| `pmx500` | PMX500 | PMX | ≈ 16 M$ | 2025-08-23 | -97,9 % | ≈ 345 k$ | rare | mort |
| `little-ugly-duck` | Little Ugly Duck | LUD | ≈ 16 M$ | 2021-08-17 | -97,7 % | ≈ 375 k$ | rare | mort |
| `galaxy-fox` | Galaxy Fox | GFOX | ≈ 16 M$ | 2024-05-08 | -99,5 % | ≈ 88 k$ | rare | mort |
| `nikepig` | Nikepig | NIKEPIG | ≈ 16 M$ | 2024-06-26 | -98,2 % | ≈ 291 k$ | rare | mort |
| `hachi` | Hachi | HACHI | ≈ 16 M$ | 2024-04-21 | -98,9 % | ≈ 173 k$ | rare | mort |
| `nsdq420` | NSDQ420 | NSDQ | ≈ 16 M$ | 2025-01-06 | -99,4 % | ≈ 89 k$ | rare | mort |
| `shi-gong-mao` | 施工猫 (Construction Cat) | SUE | ≈ 16 M$ | 2026-09-06 | -99,1 % | ≈ 149 k$ | rare |  |
| `dogecoin20` | Dogecoin20 | DOGE20 | ≈ 16 M$ | 2024-05-07 | -98,9 % | ≈ 171 k$ | rare | mort |
| `mellow-man` | Mellow Man | MELLOW | ≈ 16 M$ | 2024-08-21 | -98,0 % | ≈ 317 k$ | rare | mort |
| `sparta-2` | SPARTA | SPARTA | ≈ 16 M$ | 2025-09-12 | -98,0 % | ≈ 321 k$ | rare | mort |
| `rat-escape` | RAT Escape | RAT | ≈ 16 M$ | 2024-12-12 | -99,5 % | ≈ 86 k$ | rare | mort |
| `jester` | Jester | JEST | ≈ 16 M$ | 2024-08-22 | -96,9 % | ≈ 489 k$ | rare | mort |
| `lc-shib` | LC SHIB | LC | ≈ 16 M$ | 2025-12-22 | -95,9 % | ≈ 633 k$ | rare |  |
| `build-4` | BUILD | BUILD | ≈ 16 M$ | 2025-01-15 | -98,5 % | ≈ 241 k$ | rare | mort |
| `raydium-cat` | Raydium Cat | RAYCAT | ≈ 15 M$ | 2026-09-11 | -98,5 % | ≈ 232 k$ | rare | mort |
| `snibbu` | Snibbu | SNIBBU | ≈ 15 M$ | 2024-04-01 | -99,4 % | ≈ 94 k$ | rare | mort |
| `italian-brainrot` | Italian Brainrot | ITALIANROT | ≈ 15 M$ | 2025-05-23 | -99,5 % | ≈ 77 k$ | rare |  |
| `nitefeeder` | Nitefeeder | NITEFEEDER | ≈ 15 M$ | 2024-07-18 | -98,8 % | ≈ 191 k$ | rare | mort |
| `aped` | Aped | APED | ≈ 15 M$ | 2024-11-14 | -99,5 % | ≈ 79 k$ | rare | mort |
| `memelinked` | Memelinked | MK | ≈ 15 M$ | 2025-05-08 | -97,2 % | ≈ 423 k$ | rare | mort |
| `baby-floki` | Baby Floki | BABYFLOKI | ≈ 15 M$ | 2021-11-01 | -99,0 % | ≈ 154 k$ | rare | mort |
| `gdog` | GDOG | GDOG | ≈ 15 M$ | 2024-10-28 | -99,5 % | ≈ 77 k$ | rare | mort |
| `biden-coin` | Biden Coin | BIDEN | ≈ 15 M$ | 2025-07-06 | -99,1 % | ≈ 141 k$ | rare | mort |
| `draggy-cto` | Draggy CTO | DRAGGY | ≈ 15 M$ | 2024-07-12 | -99,5 % | ≈ 77 k$ | rare | mort |
| `gasspas` | Gasspas | GASS | ≈ 15 M$ | 2025-06-10 | -98,5 % | ≈ 229 k$ | rare |  |
| `fofar` | Fofar | FOFAR | ≈ 15 M$ | 2024-06-02 | -99,5 % | ≈ 74 k$ | rare | copie ou ancienne version d'une carte; mort |
| `all-will-retire` | All Will Retire | AWR | ≈ 15 M$ | 2025-01-25 | -97,2 % | ≈ 412 k$ | rare | mort |
| `tabbypos` | TabbyPOS | TABBY | ≈ 15 M$ | 2023-10-04 | -98,4 % | ≈ 227 k$ | rare | mort |
| `asteroid-3` | ASTEROID | ASTEROID | ≈ 14 M$ | 2026-09-10 | -98,4 % | ≈ 237 k$ | rare | mort |
| `agrippa` | Agrippa | AGRIPPA | ≈ 14 M$ | 2026-09-25 | -98,6 % | ≈ 205 k$ | rare |  |
| `treat-token` | Treat Token | TREAT | ≈ 14 M$ | 2024-03-06 | -99,2 % | ≈ 116 k$ | rare | mort |
| `good-in-the-hood` | Good In The Hood | GOOD | ≈ 14 M$ | 2026-08-27 | -97,1 % | ≈ 409 k$ | rare | mort |
| `trash-coin` | Trash Coin | TRASH | ≈ 14 M$ | 2025-07-23 | -98,9 % | ≈ 162 k$ | rare | mort |
| `amocucinare` | Amocucinare | AMORE | ≈ 14 M$ | 2024-11-25 | -98,5 % | ≈ 217 k$ | rare | mort |
| `brent-on-sol` | Brent on SOL | BRENT | ≈ 14 M$ | 2026-04-17 | -97,5 % | ≈ 353 k$ | rare | mort |
| `gigachad-eth` | GigaChad | GIGACHAD | ≈ 14 M$ | 2024-10-07 | -99,5 % | ≈ 77 k$ | rare | copie ou ancienne version d'une carte; mort |
| `spyro` | SPYRO | SPYRO | ≈ 14 M$ | 2024-02-15 | -99,5 % | ≈ 74 k$ | rare | mort |
| `bananacat` | BananaCat | BCAT | ≈ 14 M$ | 2024-11-28 | -97,6 % | ≈ 335 k$ | rare | mort |
| `whale-2` | Whale | WHALE | ≈ 14 M$ | 2025-01-15 | -99,1 % | ≈ 125 k$ | rare | copie ou ancienne version d'une carte; mort |
| `knot-diffie-hellman` | Knot Diffie-Hellman | KNOT | ≈ 14 M$ | 2024-12-10 | -99,4 % | ≈ 80 k$ | rare | mort |
| `fartstrategy` | FartStrategy | FSTR | ≈ 14 M$ | 2025-01-30 | -99,1 % | ≈ 128 k$ | rare | mort |
| `kittycake` | KittyCake | KCAKE | ≈ 14 M$ | 2021-07-28 | -98,7 % | ≈ 176 k$ | rare | mort |
| `capybara-token` | Capybara Token | CAPY | ≈ 13 M$ | 2023-05-09 | -99,1 % | ≈ 120 k$ | rare | mort |
| `dork-lord` | DORK LORD (ETH) | DORKL | ≈ 13 M$ | 2023-09-08 | -99,3 % | ≈ 98 k$ | rare | mort |
| `remilio` | remilio | REMILIO | ≈ 13 M$ | 2024-05-07 | -99,4 % | ≈ 77 k$ | rare | mort |
| `babykitty` | BabyKitty | BABYKITTY | ≈ 13 M$ | 2021-12-30 | -97,6 % | ≈ 315 k$ | rare | mort |
| `what-s-updog` | What’s Updog? | UPDOG | ≈ 13 M$ | 2024-03-06 | -99,4 % | ≈ 76 k$ | rare | mort |
| `barbiecrashbandicootrfk88` | BarbieCrashBandicootRFK88 | SOLANA | ≈ 13 M$ | 2023-10-26 | -98,9 % | ≈ 147 k$ | rare | mort |
| `mindcoin-2` | MindCoin | MIND | ≈ 13 M$ | 2024-08-13 | -99,2 % | ≈ 101 k$ | rare | mort |
| `hot-doge` | HotDoge [OLD] | HOTDOGE | ≈ 13 M$ | 2021-05-11 | -96,5 % | ≈ 456 k$ | rare | mort |
| `baby-shiba-inu-erc` | Baby Shiba Inu | BABYSHIB | ≈ 13 M$ | 2023-08-24 | -99,2 % | ≈ 106 k$ | rare | copie ou ancienne version d'une carte; mort |
| `bonkwifhat` | bonkwifhat | BIF | ≈ 13 M$ | 2024-03-06 | -99,4 % | ≈ 78 k$ | rare | mort |
| `bonk-on-base` | Bonk On Base | BONK | ≈ 13 M$ | 2024-04-22 | -99,5 % | ≈ 70 k$ | rare | mort |
| `satoshai` | SatoshAI | SAI | ≈ 13 M$ | 2026-08-01 | -97,3 % | ≈ 350 k$ | rare | mort |
| `hua-hua` | HUA HUA | HUAHUA | ≈ 13 M$ | 2024-12-04 | -99,5 % | ≈ 69 k$ | rare | mort |
| `sol-cat` | CAT | CAT | ≈ 13 M$ | 2024-05-27 | -99,2 % | ≈ 97 k$ | rare | mort |
| `shiba-classic-2` | Shiba Classic | SHIBC | ≈ 13 M$ | 2024-11-14 | -99,1 % | ≈ 113 k$ | rare | mort |
| `pika-to-piko` | PIKA to PIKO ピカとピコ | PIKA | ≈ 13 M$ | 2024-10-16 | -98,5 % | ≈ 196 k$ | rare | mort |
| `doyr` | DOYR | DOYR | ≈ 13 M$ | 2025-12-07 | -98,0 % | ≈ 251 k$ | rare |  |
| `didi-bam-bam` | Didi Bam Bam | DDBAM | ≈ 13 M$ | 2024-12-02 | -98,9 % | ≈ 141 k$ | rare | mort |
| `biaocoin` | Biaocoin | BIAO | ≈ 12 M$ | 2023-05-31 | -98,9 % | ≈ 140 k$ | rare | mort |
| `pengus-wife` | Polly | POLLY | ≈ 12 M$ | 2025-08-04 | -98,4 % | ≈ 193 k$ | rare | mort |
| `dons` | The Dons | DONS | ≈ 12 M$ | 2023-05-17 | -98,9 % | ≈ 133 k$ | rare | mort |
| `gluteus-maximus-by-virtuals` | Gluteus Maximus by Virtuals | GLUTEU | ≈ 12 M$ | 2025-01-15 | -99,0 % | ≈ 125 k$ | rare | mort |
| `estee` | Estee | ESTEE | ≈ 12 M$ | 2024-09-30 | -99,2 % | ≈ 92 k$ | rare | mort |
| `fartgirl` | FARTGIRL | FARTGIRL | ≈ 12 M$ | 2025-02-17 | -96,3 % | ≈ 451 k$ | rare | mort |
| `fefe-on-eth` | Fefe | FEFE | ≈ 12 M$ | 2024-10-17 | -99,3 % | ≈ 84 k$ | rare | mort |
| `gondola` | Gondola | GONDOLA | ≈ 12 M$ | 2024-10-15 | -98,7 % | ≈ 154 k$ | rare | mort |
| `wen-lambo-2` | Wen Lambo | WEN | ≈ 12 M$ | 2026-07-12 | -99,2 % | ≈ 93 k$ | rare | mort |
| `golden-goose-2` | Golden Goose | GG | ≈ 12 M$ | 2026-08-30 | -98,8 % | ≈ 142 k$ | rare | mort |
| `ucan-fix-life-in1day` | Ucan fix life in1day | 1 | ≈ 12 M$ | 2026-01-21 | -97,5 % | ≈ 303 k$ | rare |  |
| `scam-altman` | Scam Altman | SCAM | ≈ 12 M$ | 2026-04-28 | -99,2 % | ≈ 100 k$ | rare | mort |
| `arbidoge` | ArbiDoge | ADOGE | ≈ 12 M$ | 2024-03-08 | -97,2 % | ≈ 330 k$ | rare | mort |
| `pistacio` | Pistacio | PISTACIO | ≈ 12 M$ | 2026-08-26 | -99,2 % | ≈ 89 k$ | rare | mort |
| `beamcat` | BEAMCAT | BCAT | ≈ 12 M$ | 2024-03-11 | -97,1 % | ≈ 336 k$ | rare | mort |
| `baby-asteroid-2` | Baby Asteroid | BABYASTEROID | ≈ 12 M$ | 2026-05-04 | -98,9 % | ≈ 127 k$ | rare | mort |
| `paper-plane` | Paper Plane | PLANE | ≈ 12 M$ | 2024-04-17 | -97,6 % | ≈ 277 k$ | rare | mort |
| `token6900` | Token6900 | T6900 | ≈ 12 M$ | 2025-09-04 | -98,0 % | ≈ 235 k$ | rare | mort |
| `artificial-gooner-intelligence` | artificial gooner intelligence | AGI | ≈ 12 M$ | 2026-09-06 | -98,6 % | ≈ 159 k$ | rare | mort |
| `signal-2` | Signal | SIGNAL | ≈ 11 M$ | 2026-10-05 | -97,4 % | ≈ 302 k$ | rare | mort |
| `harrypottertrumphomersimpson777inu` | HarryPotterTrumpHomerSimpson777Inu | ETHEREUM | ≈ 11 M$ | 2024-03-03 | -99,4 % | ≈ 65 k$ | rare | mort |
| `binance-super-cycle` | Binance Super Cycle | BSC | ≈ 11 M$ | 2025-10-08 | -99,2 % | ≈ 86 k$ | rare | mort |
| `are-ya-winning-son` | ARE YA WINNING, SON? | SON | ≈ 11 M$ | 2025-08-13 | -99,1 % | ≈ 101 k$ | rare | mort |
| `dork-lord-2` | Dork Lord | DORKY | ≈ 11 M$ | 2026-08-01 | -98,1 % | ≈ 216 k$ | rare | mort |
| `hund` | Hund | HUND | ≈ 11 M$ | 2024-04-02 | -99,2 % | ≈ 90 k$ | rare | mort |
| `disclaimercoin` | DisclaimerCoin | DONT | ≈ 11 M$ | 2026-01-23 | -98,8 % | ≈ 136 k$ | rare | mort |
| `coq-ai` | COQ AI | COQAI | ≈ 11 M$ | 2025-01-11 | -99,2 % | ≈ 88 k$ | rare | nature à vérifier; mort |
| `mommy-doge` | Mommy Doge | MOMMYDOGE | ≈ 11 M$ | 2021-07-11 | -96,7 % | ≈ 373 k$ | rare | mort |
| `sweep-token` | Sweep Token | SWEEP | ≈ 11 M$ | 2023-02-18 | -96,6 % | ≈ 370 k$ | rare | mort |
| `all-your-base-2` | All Your Base | AYB | ≈ 11 M$ | 2024-03-29 | -97,3 % | ≈ 292 k$ | rare | mort |
| `transhuman-coin` | Transhuman Coin | THC | ≈ 11 M$ | 2021-11-14 | -97,6 % | ≈ 255 k$ | rare | mort |
| `mubarakah` | Mubarakah | MUBARAKAH | ≈ 11 M$ | 2025-03-21 | -96,4 % | ≈ 386 k$ | rare |  |
| `ada-the-dog` | TOLY'S DOG | ADA | ≈ 11 M$ | 2024-03-29 | -99,4 % | ≈ 67 k$ | rare | mort |
| `mark-2-marquette` | Mark-2-Marquette | M2M | ≈ 11 M$ | 2026-04-25 | -99,2 % | ≈ 89 k$ | rare | mort |
| `wishbone` | WISHBONE | WISHBONE | ≈ 11 M$ | 2026-07-14 | -97,6 % | ≈ 255 k$ | rare | mort |
| `based-2` | BASED | BASED | ≈ 11 M$ | 2024-08-13 | -99,4 % | ≈ 68 k$ | rare | mort |
| `vibe-cat-3` | Vibe Cat | VIBE | ≈ 11 M$ | 2025-06-19 | -99,2 % | ≈ 85 k$ | rare | mort |
| `all-in-dollo` | All in Dollo | DOLLO | ≈ 10 M$ | 2025-08-14 | -99,4 % | ≈ 67 k$ | rare | mort |
| `cali` | CALI | CALI | ≈ 10 M$ | 2026-09-27 | -98,9 % | ≈ 111 k$ | rare | mort |
| `smolcoin-2` | SMOL | SMOL | ≈ 10 M$ | 2025-02-04 | -98,6 % | ≈ 149 k$ | rare | mort |
| `matt-0x79` | Matt Furie | MATT | ≈ 10 M$ | 2024-07-15 | -99,4 % | ≈ 62 k$ | rare | mort |
| `gboy` | GBOY | GBOY | ≈ 10 M$ | 2026-01-15 | -95,6 % | ≈ 455 k$ | rare | mort |
| `preme-token` | PREME Token | PREME | ≈ 10 M$ | 2026-06-29 | -98,1 % | ≈ 191 k$ | rare | mort |
| `wagmi-coin` | Wagmi Coin | WAGMI | ≈ 10 M$ | 2023-05-24 | -99,4 % | ≈ 66 k$ | rare | mort |
| `assdaq` | ASSDAQ | ASSDAQ | ≈ 10 M$ | 2025-08-05 | -99,2 % | ≈ 85 k$ | rare | mort |
| `king-of-meme` | King Of Meme | LION | ≈ 10 M$ | 2024-06-18 | -99,3 % | ≈ 67 k$ | rare | mort |
| `wojak-3` | Wojak | WOJAK | ≈ 10 M$ | 2025-08-28 | -98,7 % | ≈ 134 k$ | rare | copie ou ancienne version d'une carte; mort |
| `pepoclown` | Pepoclown | HONK | ≈ 10 M$ | 2024-10-20 | -98,4 % | ≈ 158 k$ | rare | mort |

### C2. Estimation fragile (écart ≤ -99,5 %, pic estimé < 1 Md$)

Rareté indicative abaissée d'un cran, comme en (b).

| CoinGecko id | Nom | Ticker | Pic estimé | Date du plus haut | Écart | Rareté v2 indicative | Remarque |
|---|---|---|---|---|---|---|---|
| `meow` | MEOW | MEOW | ≈ 977 M$ | 2025-02-20 | -99,97 % | rare | mort |
| `beardy-dragon` | Bearded Dragon | BEARDY | ≈ 943 M$ | 2024-04-03 | -100,00 % | rare | mort |
| `akuma-inu` | Akuma Inu | AKUMA | ≈ 905 M$ | 2025-01-09 | -100,00 % | rare | mort |
| `angryb` | Angryb | ANB | ≈ 848 M$ | 2021-07-25 | -99,96 % | rare | mort |
| `catgirl` | Catgirl | CATGIRL | ≈ 807 M$ | 2021-11-01 | -99,98 % | rare | mort |
| `get-ai` | Get AI | GET | ≈ 799 M$ | 2025-02-13 | -99,96 % | rare | nature à vérifier; mort |
| `levana-protocol` | Levana | LVN | ≈ 718 M$ | 2023-12-19 | -99,94 % | rare | mort |
| `suibeaver` | suibeaver | DAM | ≈ 699 M$ | 2026-03-27 | -100,00 % | rare | mort |
| `solordi` | Solordi | SOLO | ≈ 692 M$ | 2026-04-01 | -100,00 % | rare | mort |
| `lumoscoin` | Lumos | LUMOS | ≈ 691 M$ | 2026-04-11 | -99,97 % | rare | mort |
| `sponge-2` | Sponge | SPONGE | ≈ 633 M$ | 2024-03-09 | -99,96 % | rare | mort |
| `ket` | Ket | KET | ≈ 617 M$ | 2025-05-28 | -99,89 % | rare | copie ou ancienne version d'une carte; mort |
| `mononoke-inu` | Mononoke Inu | MONONOKE-INU | ≈ 603 M$ | 2021-10-29 | -99,96 % | rare | mort |
| `sanshu-inu` | Sanshu Inu (OLD) | SANSHU | ≈ 602 M$ | 2021-05-11 | -99,98 % | rare | mort |
| `shmeegus` | Shmeegus | SHMEEGUS | ≈ 584 M$ | 2026-01-21 | -100,00 % | rare | mort |
| `pepe-unchained` | Pepe Unchained [OLD] | PEPU | ≈ 544 M$ | 2024-12-12 | -99,97 % | rare | copie ou ancienne version d'une carte; nature à vérifier; mort |
| `department-of-government-efficiency` | Department Of Government Efficiency | DOGE | ≈ 502 M$ | 2024-11-13 | -99,92 % | rare |  |
| `we-love-t` | We Love Tits | TITS | ≈ 484 M$ | 2024-11-24 | -99,98 % | rare | mort |
| `maga-trump` | MAGA Trump | MAGATRUMP | ≈ 481 M$ | 2025-02-14 | -99,99 % | rare | mort |
| `harambe-ai` | Harambe AI | HARAMBEAI | ≈ 469 M$ | 2024-07-17 | -99,97 % | rare | nature à vérifier; mort |
| `milk` | Cool Cats Milk | MILK | ≈ 461 M$ | 2022-02-15 | -99,98 % | rare | mort |
| `bitshiba` | BitShiba | SHIBA | ≈ 383 M$ | 2021-11-13 | -99,93 % | rare | mort |
| `gameswift` | GameSwift | GSWIFT | ≈ 382 M$ | 2024-03-04 | -99,95 % | rare | nature à vérifier; mort |
| `unix` | UniX | UNIX | ≈ 361 M$ | 2021-11-30 | -100,00 % | rare | mort |
| `shiro-neko-2` | Shiro Neko | SHIRO | ≈ 354 M$ | 2024-12-08 | -99,91 % | rare | mort |
| `neon-neko` | NeonNeko | NEKO | ≈ 340 M$ | 2025-07-22 | -100,00 % | rare | mort |
| `k9-finance-dao` | K9 Finance DAO | KNINE | ≈ 328 M$ | 2024-03-10 | -99,94 % | rare | nature à vérifier; mort |
| `michicoin` | michi [OLD] | $MICHI | ≈ 327 M$ | 2024-05-16 | -99,92 % | rare | copie ou ancienne version d'une carte; mort |
| `lambo-0fcbf0f7-1a8f-470d-ba09-797d5e95d836` | LAMBO | LAMBO | ≈ 309 M$ | 2024-03-19 | -99,97 % | rare | mort |
| `first-convicted-raccon` | First Convicted RACCON | FRED | ≈ 303 M$ | 2024-11-13 | -99,91 % | rare |  |
| `freedom-coin` | FREEdom coin | FREE | ≈ 302 M$ | 2019-03-03 | -99,95 % | rare | mort |
| `american-coin` | American Coin | USA | ≈ 296 M$ | 2025-01-19 | -99,64 % | rare |  |
| `puff-the-dragon` | Puff The Dragon | PUFF | ≈ 294 M$ | 2024-04-08 | -99,68 % | rare | mort |
| `memes` | MEMES | MEMES | ≈ 283 M$ | 2024-12-20 | -100,00 % | rare | mort |
| `mumu-the-bull-3` | MUMU THE BULL [OLD] | MUMU | ≈ 280 M$ | 2024-07-29 | -99,96 % | rare | copie ou ancienne version d'une carte; mort |
| `dog-collar` | Dog Collar | COLLAR | ≈ 263 M$ | 2021-11-02 | -99,94 % | rare | mort |
| `kuma-inu` | Kuma Inu | KUMA | ≈ 251 M$ | 2021-10-12 | -99,82 % | rare | mort |
| `catton-ai` | Catton AI | CATTON | ≈ 249 M$ | 2025-02-06 | -99,98 % | rare | nature à vérifier; mort |
| `rifampicin` | Rifampicin | $RIF | ≈ 248 M$ | 2024-11-18 | -99,93 % | rare | mort |
| `elon4afd` | Elon4AfD | ELON4AFD | ≈ 247 M$ | 2025-02-03 | -99,82 % | rare | mort |
| `mongcoin` | MongCoin | MONG | ≈ 247 M$ | 2023-05-05 | -99,88 % | rare | mort |
| `chonky` | CHONKY [OLD] | CHONKY | ≈ 233 M$ | 2026-04-01 | -99,98 % | rare | mort |
| `pacmoon` | PacMoon | PAC | ≈ 225 M$ | 2024-06-04 | -99,95 % | rare | mort |
| `wall-street-bets-dapp` | WallStreetBets DApp | WSB | ≈ 225 M$ | 2021-05-05 | -99,92 % | rare | mort |
| `million` | Million | MM | ≈ 223 M$ | 2021-07-13 | -99,55 % | rare | mort |
| `the-real-landwolf` | LandWolf | WOLF | ≈ 223 M$ | 2024-06-21 | -99,88 % | rare | copie ou ancienne version d'une carte; mort |
| `peng` | Peng | PENG | ≈ 214 M$ | 2024-03-14 | -99,93 % | rare | mort |
| `burp` | Burp | BURP | ≈ 214 M$ | 2021-07-26 | -99,97 % | rare | mort |
| `analos` | analoS | ANALOS | ≈ 214 M$ | 2023-12-25 | -99,97 % | rare | mort |
| `normie-2` | NORMIE | NORMIE | ≈ 212 M$ | 2024-03-25 | -99,95 % | rare | copie ou ancienne version d'une carte; mort |
| `minidoge-5` | Minidoge | MINIDOGE | ≈ 211 M$ | 2025-10-05 | -99,76 % | rare | mort |
| `baby-myro` | Baby Myro | BABYMYRO | ≈ 209 M$ | 2024-01-17 | -99,97 % | rare | mort |
| `omnicat` | OmniCat | OMNI | ≈ 208 M$ | 2023-12-23 | -99,88 % | rare | mort |
| `max-2` | MAX | MAX | ≈ 208 M$ | 2025-01-07 | -99,96 % | rare | mort |
| `dasha` | Dasha | VVAIFU | ≈ 207 M$ | 2024-11-18 | -99,92 % | rare | mort |
| `gotti-token` | Gotti Token | GOTTI | ≈ 207 M$ | 2024-07-02 | -99,97 % | rare | mort |
| `shih-tzu` | Shih Tzu | SHIH | ≈ 207 M$ | 2021-05-11 | -99,97 % | rare | mort |
| `fartful` | FARTFUL | FARTFUL | ≈ 205 M$ | 2025-08-28 | -100,00 % | rare | mort |
| `water-coin` | WATER Coin | WATER | ≈ 203 M$ | 2024-06-26 | -99,87 % | rare | mort |
| `ibiza-final-boss` | Ibiza Final Boss | BOSS | ≈ 203 M$ | 2026-05-25 | -99,98 % | rare | mort |
| `the-soldog` | LAIKA the Cosmodog | LAIKA | ≈ 199 M$ | 2024-06-13 | -99,94 % | rare | mort |
| `coshi-inu` | CoShi Inu | COSHI | ≈ 193 M$ | 2021-05-10 | -99,92 % | rare | mort |
| `banana-tape-wall` | Banana Tape Wall | BTW | ≈ 192 M$ | 2026-06-20 | -99,98 % | rare | mort |
| `doge-floki-coin` | Doge Floki Coin [OLD] | DOFI | ≈ 185 M$ | 2021-10-28 | -99,97 % | rare | mort |
| `lovebit` | LoveBit | LB | ≈ 183 M$ | 2024-07-11 | -99,99 % | rare | mort |
| `numogram` | Numogram | GNON | ≈ 182 M$ | 2024-10-19 | -99,94 % | rare | mort |
| `gummy` | GUMMY | GUMMY | ≈ 180 M$ | 2024-04-22 | -99,91 % | rare | mort |
| `foxy` | Foxy | FOXY | ≈ 178 M$ | 2024-06-06 | -99,81 % | rare | mort |
| `solchat` | Solchat | CHAT | ≈ 174 M$ | 2024-03-17 | -99,89 % | rare | mort |
| `altcoin-2` | Altcoin | ALT | ≈ 173 M$ | 2025-07-13 | -99,97 % | rare | mort |
| `dechat` | Dechat | DECHAT | ≈ 172 M$ | 2024-03-11 | -99,99 % | rare | mort |
| `alpha-4` | Alpha | ALPHA | ≈ 172 M$ | 2025-02-04 | -99,92 % | rare |  |
| `papa-trump` | PAPA Trump | PPT | ≈ 171 M$ | 2024-07-02 | -100,00 % | rare | mort |
| `oob` | Oob | OOB | ≈ 170 M$ | 2026-03-26 | -100,00 % | rare | mort |
| `just-a-frog` | just a frog | FROG | ≈ 169 M$ | 2026-01-19 | -99,98 % | rare | mort |
| `eliza` | Eliza | ELIZA | ≈ 166 M$ | 2024-12-31 | -99,94 % | rare | mort |
| `silly-dragon` | Silly Dragon | SILLY | ≈ 159 M$ | 2023-12-26 | -99,96 % | rare | mort |
| `zyncoin-2` | ZynCoin | ZYN | ≈ 157 M$ | 2024-03-11 | -99,79 % | rare | mort |
| `litecoin-mascot` | Litecoin Mascot | LESTER | ≈ 154 M$ | 2024-11-15 | -99,91 % | rare | mort |
| `justice-for-pnut-and-fred` | Justice for Pnut and Fred | JUSTICE | ≈ 152 M$ | 2024-11-25 | -99,99 % | rare | mort |
| `bob-token` | BOB Token | BOB | ≈ 151 M$ | 2023-05-06 | -99,71 % | rare |  |
| `lil-shrub` | Lil' Shrub | SHRUB | ≈ 148 M$ | 2026-09-04 | -100,00 % | rare | mort |
| `der-daku` | Daku | DAKU | ≈ 148 M$ | 2025-05-23 | -99,97 % | rare | mort |
| `shiba-armstrong` | Shiba Armstrong | SHIBA | ≈ 146 M$ | 2024-05-20 | -99,89 % | rare | mort |
| `smoking-chicken-fish` | Smoking Chicken Fish | SCF | ≈ 145 M$ | 2024-10-14 | -99,78 % | rare | mort |
| `urolithin-a` | Urolithin A | $URO | ≈ 144 M$ | 2024-11-18 | -99,91 % | rare | mort |
| `large-language-model` | Large Language Model | LLM | ≈ 144 M$ | 2025-01-09 | -99,94 % | rare |  |
| `baby-bnb` | Baby BNB | BABYBNB | ≈ 143 M$ | 2024-09-30 | -99,97 % | rare | mort |
| `luci` | LUCI | LUCI | ≈ 141 M$ | 2026-04-01 | -99,95 % | rare | mort |
| `characcon` | characcon | CHARACCON | ≈ 141 M$ | 2026-05-17 | -100,00 % | rare | mort |
| `dinger-token` | Dinger | DINGER | ≈ 135 M$ | 2021-10-28 | -99,74 % | rare | mort |
| `shiryo-inu` | Shiryo | SHIRYO-INU | ≈ 135 M$ | 2021-11-20 | -99,95 % | rare | mort |
| `retard-finder-coin` | Retard Finder Coin | RFC | ≈ 133 M$ | 2025-04-13 | -99,89 % | rare | mort |
| `bad-idea-ai` | Bad Idea AI | BAD | ≈ 133 M$ | 2023-08-12 | -99,67 % | rare | nature à vérifier; mort |
| `tooker-kurlson` | tooker kurlson | TOOKER | ≈ 132 M$ | 2024-05-03 | -99,94 % | rare | mort |
| `tsuki-inu` | Tsuki Inu | TKINU | ≈ 131 M$ | 2021-05-21 | -99,83 % | rare | mort |
| `wifedoge` | Wifedoge | WIFEDOGE | ≈ 130 M$ | 2021-09-06 | -99,90 % | rare | mort |
| `catwifbag` | catwifbag | BAG | ≈ 130 M$ | 2024-03-25 | -99,93 % | rare | mort |
| `freerossdao` | FreeRossDAO | FREE | ≈ 129 M$ | 2021-12-15 | -99,88 % | rare | nature à vérifier; mort |
| `ansem-s-cat` | Ansem's Cat | HOBBES | ≈ 128 M$ | 2024-04-03 | -99,94 % | rare |  |
| `kedaenge` | Kedaenge | KEDAENGE | ≈ 128 M$ | 2026-05-03 | -100,00 % | rare | mort |
| `baby-shark-meme` | Baby Shark Meme | BABYSHARK | ≈ 125 M$ | 2025-01-10 | -99,99 % | rare | mort |
| `pythia` | PYTHIA | PYTHIA | ≈ 125 M$ | 2025-08-27 | -99,90 % | rare | mort |
| `city-boy` | City Boy | CITYBOY | ≈ 124 M$ | 2026-03-10 | -100,00 % | rare | mort |
| `pup-token` | PUP Token | PUP | ≈ 123 M$ | 2025-09-17 | -99,72 % | rare | mort |
| `look` | LOOK | LOOK | ≈ 121 M$ | 2025-11-01 | -99,88 % | rare | mort |
| `dogeai-2` | DOGEai | $DOGEAI | ≈ 119 M$ | 2025-01-23 | -99,98 % | rare | mort |
| `catbal` | Catbal | CATBAL | ≈ 116 M$ | 2024-12-08 | -99,59 % | rare | mort |
| `w-coin` | W coin | W | ≈ 111 M$ | 2025-07-02 | -100,00 % | rare | mort |
| `hot-mom` | Hot Mom | HOTMOM | ≈ 110 M$ | 2025-05-14 | -99,99 % | rare | mort |
| `befe` | BEFE | BEFE | ≈ 110 M$ | 2023-12-27 | -99,70 % | rare | mort |
| `kitten-haimer` | Kitten Haimer | KHAI | ≈ 105 M$ | 2024-04-11 | -99,95 % | rare | mort |
| `harrypotterobamapacman8inu` | HarryPotterObamaPacMan8Inu | XRP | ≈ 105 M$ | 2023-08-19 | -99,84 % | rare | mort |
| `degen-spartan-ai` | Degen Spartan AI | DEGENAI | ≈ 105 M$ | 2025-01-02 | -99,92 % | rare | nature à vérifier; mort |
| `top-hat` | Top Hat | HAT | ≈ 105 M$ | 2025-01-02 | -99,96 % | rare | mort |
| `kiki-2` | KIKICat | KIKI | ≈ 103 M$ | 2024-12-26 | -99,96 % | rare | mort |
| `zack-morris` | Zack Morris | ZACK | ≈ 102 M$ | 2024-05-23 | -99,96 % | rare | mort |
| `project89` | Project89 [OLD] | PROJECT89 | ≈ 101 M$ | 2024-11-22 | -99,95 % | rare | mort |
| `chaos-and-disorder` | chaos and disorder | CHAOS | ≈ 100 M$ | 2024-11-22 | -99,96 % | rare | mort |
| `ronaldinho-coin` | Ronaldinho Coin | STAR10 | ≈ 100 M$ | 2025-03-02 | -99,99 % | rare | mort |
| `enjoy` | Enjoy | ENJOY | ≈ 98 M$ | 2024-04-04 | -99,97 % | commune | mort |
| `farm-2` | FARM | FARM | ≈ 98 M$ | 2025-01-03 | -99,97 % | commune | mort |
| `aicell` | AICell | AICELL | ≈ 98 M$ | 2024-12-29 | -99,70 % | commune | mort |
| `doglibre` | DogLibre | DOGL | ≈ 98 M$ | 2024-12-12 | -99,92 % | commune | mort |
| `pepe-in-a-memes-world` | pepe in a memes world | PEW | ≈ 97 M$ | 2024-05-31 | -99,83 % | commune | mort |
| `realgoat` | RealGoat | RGOAT | ≈ 97 M$ | 2024-07-18 | -99,97 % | commune | mort |
| `salvator-mundi` | Salvator Mundi | MUNDI | ≈ 97 M$ | 2024-12-01 | -99,93 % | commune | mort |
| `jen-hsun-huang` | JHH | JHH | ≈ 96 M$ | 2024-10-01 | -99,96 % | commune | mort |
| `bobacat` | Boba Cat | BOBA | ≈ 94 M$ | 2024-03-29 | -99,71 % | commune | mort |
| `rizznet` | RZTO | RZTO | ≈ 94 M$ | 2025-10-29 | -99,93 % | commune | mort |
| `baby` | Baby | BABY | ≈ 93 M$ | 2024-04-15 | -99,97 % | commune | mort |
| `major-frog` | Major Frog | MAJOR | ≈ 93 M$ | 2024-11-15 | -99,98 % | commune | mort |
| `coco-coin` | COCO COIN | COCO | ≈ 92 M$ | 2025-01-01 | -99,87 % | commune | mort |
| `deep-worm` | Deep Worm | WORM | ≈ 92 M$ | 2024-11-19 | -99,96 % | commune | mort |
| `aimonica-brands` | Aimonica Brands | AIMONICA | ≈ 92 M$ | 2025-01-02 | -99,96 % | commune | mort |
| `andy-4` | Andy BSC | ANDY | ≈ 92 M$ | 2025-01-11 | -99,90 % | commune | mort |
| `strategic-bitcoin-reserve` | Strategic Bitcoin Reserve | SBR | ≈ 91 M$ | 2024-11-14 | -99,70 % | commune | mort |
| `department-of-gov-efficiency` | Department of Gov Efficiency | DOGE | ≈ 91 M$ | 2024-11-13 | -99,90 % | commune | mort |
| `rnt-token` | RNT | RNT | ≈ 90 M$ | 2024-06-07 | -99,54 % | commune | mort |
| `nomnom` | nomnom | NOMNOM | ≈ 90 M$ | 2024-11-16 | -99,83 % | commune | mort |
| `evil-larry` | Evil Larry | LARRY | ≈ 89 M$ | 2025-09-21 | -99,90 % | commune | mort |
| `harambe-2` | Harambe on Solana | HARAMBE | ≈ 88 M$ | 2024-11-13 | -99,72 % | commune | mort |
| `based-fartcoin` | Based Fartcoin | FARTCOIN | ≈ 88 M$ | 2025-01-17 | -99,68 % | commune | mort |
| `dolan-duck` | Dolan Duck | DOLAN | ≈ 88 M$ | 2024-10-18 | -99,79 % | commune | mort |
| `terminal-of-fun` | terminal of fun | FUN | ≈ 88 M$ | 2026-05-08 | -99,98 % | commune | mort |
| `nobody-sausage` | Nobody Sausage | NOBODY | ≈ 87 M$ | 2025-09-07 | -99,69 % | commune | mort |
| `commander-vrax-3` | Commander VRAX | VRAX | ≈ 87 M$ | 2026-10-02 | -100,00 % | commune | copie ou ancienne version d'une carte; mort |
| `ani-grok-companion` | Ani Grok Companion | ANI | ≈ 87 M$ | 2025-07-22 | -99,82 % | commune |  |
| `official-zuno` | OFFICIAL ZUNO | ZUNO | ≈ 86 M$ | 2025-11-11 | -99,88 % | commune | mort |
| `mut` | MUT | MUT | ≈ 86 M$ | 2024-12-06 | -100,00 % | commune | mort |
| `grumpy-cat-coin` | Grumpy Cat Coin | GRUMPY | ≈ 86 M$ | 2024-11-21 | -99,83 % | commune | mort |
| `shibgf` | SHIBGF | SHIBGF | ≈ 86 M$ | 2021-11-01 | -99,78 % | commune | mort |
| `dark-maga` | Dark MAGA | DMAGA | ≈ 85 M$ | 2024-07-22 | -99,94 % | commune | mort |
| `solly` | SOLLY | SOLLY | ≈ 85 M$ | 2024-06-13 | -99,99 % | commune | mort |
| `doge-eat-doge` | Doge Eat Doge | OMNOM | ≈ 85 M$ | 2024-03-31 | -99,93 % | commune | mort |
| `evan-2` | Evan | EVAN | ≈ 85 M$ | 2024-12-08 | -99,98 % | commune | mort |
| `koala-ai` | KOALA AI | KOKO | ≈ 85 M$ | 2024-10-22 | -99,82 % | commune | nature à vérifier; mort |
| `anita-max-wynn` | Anita Max Wynn | WYNN | ≈ 84 M$ | 2024-01-21 | -99,92 % | commune | mort |
| `patriot` | Patriot | PATRIOT | ≈ 84 M$ | 2025-01-11 | -99,76 % | commune | mort |
| `cheyenne` | Cheyenne | CHEYENNE | ≈ 84 M$ | 2024-11-16 | -99,95 % | commune | mort |
| `dogeverse` | DogeVerse | DOGEVERSE | ≈ 83 M$ | 2024-06-08 | -99,64 % | commune | mort |
| `hemule` | Hemule | HEMULE | ≈ 83 M$ | 2024-03-11 | -99,56 % | commune | mort |
| `magaverse` | Magaverse | MVRS | ≈ 82 M$ | 2025-01-16 | -99,98 % | commune | mort |
| `fight-to-maga` | Fight to MAGA | FIGHT | ≈ 81 M$ | 2024-07-16 | -99,75 % | commune | mort |
| `ginnan-the-cat` | Ginnan The Cat | GINNAN | ≈ 81 M$ | 2024-08-07 | -99,75 % | commune | mort |
| `wolfwifballz` | WolfWifBallz | BALLZ | ≈ 81 M$ | 2024-03-17 | -99,98 % | commune | mort |
| `blub-2` | Blub | BLUB | ≈ 79 M$ | 2025-03-06 | -99,97 % | commune | copie ou ancienne version d'une carte; mort |
| `axol` | AXOL | AXOL | ≈ 79 M$ | 2024-12-15 | -99,66 % | commune | mort |
| `sentio-protocol` | Sentio AI | SEN | ≈ 79 M$ | 2025-01-06 | -99,96 % | commune | nature à vérifier; mort |
| `neiro` | Neiro | NEIRO | ≈ 79 M$ | 2024-07-29 | -99,83 % | commune | copie ou ancienne version d'une carte |
| `catana` | Catana | CATANA | ≈ 79 M$ | 2024-11-27 | -99,92 % | commune | mort |
| `top-g` | Top G | TOPG | ≈ 78 M$ | 2024-06-08 | -99,81 % | commune | mort |
| `solmail` | SolMail | MAIL | ≈ 78 M$ | 2024-03-27 | -99,85 % | commune | mort |
| `cat-dog` | Cat-Dog | CATDOG | ≈ 78 M$ | 2024-08-08 | -99,95 % | commune | mort |
| `just-buy-1-worth-of-this-coin` | just buy $1 worth of this coin | $1 | ≈ 78 M$ | 2024-11-27 | -99,54 % | commune |  |
| `autonomous-virtual-beings` | Autonomous Virtual Beings | AVB | ≈ 77 M$ | 2025-01-10 | -99,72 % | commune | mort |
| `sad-hamster` | SAD HAMSTER | HAMMY | ≈ 77 M$ | 2024-05-07 | -99,77 % | commune | mort |
| `scrat` | Scrat | SCRAT | ≈ 77 M$ | 2024-06-27 | -99,93 % | commune | mort |
| `pino` | PINO | PINO | ≈ 77 M$ | 2024-12-13 | -99,52 % | commune | mort |
| `skibidi-toilet-2` | Skibidi Toilet | SKBDI | ≈ 77 M$ | 2024-11-15 | -99,73 % | commune | mort |
| `dongo-ai` | Dongo AI | DONGO | ≈ 76 M$ | 2024-03-29 | -99,92 % | commune | nature à vérifier; mort |
| `phil` | Phil | PHIL | ≈ 75 M$ | 2024-08-30 | -99,77 % | commune | mort |
| `woof-token` | WOOF | WOOF | ≈ 75 M$ | 2021-11-06 | -99,75 % | commune | mort |
| `ben-the-dog` | Ben the Dog | BENDOG | ≈ 75 M$ | 2024-06-05 | -99,91 % | commune | mort |
| `donkey-2` | Donkey | DONKEY | ≈ 74 M$ | 2025-08-24 | -99,84 % | commune | mort |
| `uranus-4` | Uranus | URANUS | ≈ 73 M$ | 2025-07-30 | -99,59 % | commune | mort |
| `musk-it` | Musk It | MUSKIT | ≈ 73 M$ | 2025-01-31 | -99,90 % | commune | mort |
| `duko` | DUKO | DUKO | ≈ 73 M$ | 2024-03-24 | -99,71 % | commune |  |
| `u-s-oil` | U.S Oil | USOR | ≈ 72 M$ | 2026-01-20 | -99,51 % | commune | mort |
| `dog-with-apple-in-mouth` | dog with apple in mouth | APPLE | ≈ 72 M$ | 2024-12-15 | -99,92 % | commune | mort |
| `forest` | FOREST | FOREST | ≈ 72 M$ | 2024-11-16 | -99,87 % | commune | mort |
| `international-meme-fund` | International Meme Fund | IMF | ≈ 71 M$ | 2025-07-14 | -99,95 % | commune | mort |
| `mad-2` | MAD | MAD | ≈ 71 M$ | 2024-11-22 | -99,66 % | commune |  |
| `plankton-in-pain` | Plankton in Pain | AAAHHM | ≈ 70 M$ | 2024-12-19 | -99,99 % | commune | mort |
| `faml` | FAML | FAML | ≈ 70 M$ | 2024-11-27 | -99,99 % | commune | mort |
| `giko-cat` | Giko Cat | GIKO | ≈ 69 M$ | 2024-10-06 | -99,68 % | commune | mort |
| `nailong` | Nailong | NAILONG | ≈ 69 M$ | 2024-11-16 | -99,82 % | commune | mort |
| `flavia-is-online` | Flavia Is Online | FLAVIA | ≈ 68 M$ | 2024-10-23 | -99,97 % | commune | mort |
| `tcc` | TCC | TCC | ≈ 68 M$ | 2026-07-05 | -99,91 % | commune | mort |
| `fins` | FINS | FINS | ≈ 68 M$ | 2026-06-25 | -99,99 % | commune | mort |
| `ethervista` | Ethervista | VISTA | ≈ 67 M$ | 2024-11-01 | -99,72 % | commune |  |
| `aishiba` | AiShiba | SHIBAI | ≈ 65 M$ | 2023-04-20 | -99,96 % | commune | mort |
| `gen-z-quant` | Gen Z Quant | QUANT | ≈ 65 M$ | 2024-11-20 | -99,82 % | commune | mort |
| `kween` | KWEEN | KWEEN | ≈ 65 M$ | 2024-12-16 | -99,81 % | commune | mort |
| `tetsuo-coin` | Tetsuo Coin | TETSUO | ≈ 65 M$ | 2025-01-11 | -99,77 % | commune | mort |
| `degecoin` | DegeCoin | $DEGE | ≈ 64 M$ | 2025-07-18 | -99,94 % | commune | mort |
| `illusion-of-life` | Illusion of Life | SPARK | ≈ 64 M$ | 2025-08-11 | -99,90 % | commune |  |
| `rocky-on-base` | ROCKY | $ROCKY | ≈ 64 M$ | 2024-05-03 | -99,79 % | commune | mort |
| `hahayes` | HahaYes | RIZO | ≈ 64 M$ | 2024-11-18 | -99,63 % | commune | mort |
| `bitcoin-cats` | Bitcoin Cats | 1CAT | ≈ 63 M$ | 2023-12-28 | -99,63 % | commune | mort |
| `theydontloveyoulikeiloveyou` | theydontloveyoulikeiloveyou | WAIT | ≈ 63 M$ | 2024-11-20 | -99,98 % | commune | mort |
| `tema` | Tema | TEMA | ≈ 63 M$ | 2024-12-26 | -99,94 % | commune | mort |
| `npcs-ai` | NPCS AI | XNPCS | ≈ 62 M$ | 2025-04-30 | -99,82 % | commune | nature à vérifier; mort |
| `optimus-ai` | Optimus AI | OPTI | ≈ 62 M$ | 2024-03-09 | -99,61 % | commune | nature à vérifier; mort |
| `big-pharmai` | Big Pharmai | DRUGS | ≈ 61 M$ | 2025-01-01 | -99,98 % | commune | mort |
| `spore` | Spore | SPORE | ≈ 61 M$ | 2021-04-30 | -99,63 % | commune | mort |
| `fpi-bank` | FPI Bank | FPIBANK | ≈ 61 M$ | 2025-02-06 | -99,89 % | commune | mort |
| `fight` | FIGHT | FIGHT | ≈ 61 M$ | 2025-01-19 | -99,69 % | commune | mort |
| `stonks-5` | STONKS | STONKS | ≈ 60 M$ | 2025-03-02 | -99,90 % | commune | copie ou ancienne version d'une carte; mort |
| `zeus-4` | Zeus | ZEUS | ≈ 59 M$ | 2025-05-29 | -99,92 % | commune | mort |
| `unfk` | UNFK | $UNFK | ≈ 59 M$ | 2024-11-15 | -99,60 % | commune | mort |
| `just-a-black-rock-on-base` | Just a Black Rock on Base | ROCK | ≈ 59 M$ | 2024-03-29 | -99,91 % | commune | mort |
| `costco-hot-dog` | Cost Hot Dog | COST | ≈ 59 M$ | 2024-04-15 | -99,80 % | commune | mort |
| `shroom` | Shroom | SHROOM | ≈ 58 M$ | 2024-03-19 | -99,67 % | commune | mort |
| `she-rises` | Akasha | AKA | ≈ 58 M$ | 2025-01-07 | -99,85 % | commune | mort |
| `biao-on-sol` | BIAO on SOL | BIAO | ≈ 58 M$ | 2024-12-04 | -99,78 % | commune | mort |
| `landwolf-on-avax` | Landwolf on AVAX | WOLF | ≈ 58 M$ | 2024-03-14 | -99,70 % | commune | mort |
| `macrohard` | MacroHard | MHRD | ≈ 58 M$ | 2025-08-14 | -99,96 % | commune | mort |
| `markkacy` | markkacy | KACY | ≈ 57 M$ | 2024-11-26 | -99,93 % | commune | mort |
| `tsotchke` | Tsotchke | TSOTCHKE | ≈ 57 M$ | 2024-12-28 | -99,81 % | commune | mort |
| `lambo-4` | LAMBO | LAMBO | ≈ 57 M$ | 2025-06-16 | -99,91 % | commune | mort |
| `boomer` | Boomer | BOOMER | ≈ 57 M$ | 2024-05-04 | -99,71 % | commune | mort |
| `trust-the-process` | Trust The Process | TRUST | ≈ 56 M$ | 2024-12-18 | -99,84 % | commune | mort |
| `gui-inu` | Gui Inu | GUI | ≈ 56 M$ | 2024-03-16 | -99,85 % | commune | mort |
| `habibi-sol` | Habibi (Sol) | HABIBI | ≈ 55 M$ | 2024-05-22 | -99,90 % | commune | mort |
| `seiyan` | SEIYAN | SEIYAN | ≈ 55 M$ | 2024-01-01 | -99,85 % | commune | mort |
| `just-memecoin` | just memecoin | MEMECOIN | ≈ 55 M$ | 2025-07-25 | -99,94 % | commune | mort |
| `babybonk` | BabyBonk [OLD] | BABYBONK | ≈ 55 M$ | 2024-03-10 | -99,90 % | commune | copie ou ancienne version d'une carte; mort |
| `bozo-hybrid` | Bozo Benk | BOZO | ≈ 54 M$ | 2024-01-29 | -99,85 % | commune | mort |
| `aintivirus-2` | AIntivirus | AINTI | ≈ 54 M$ | 2025-01-23 | -99,96 % | commune | mort |
| `banana-for-scale` | Banana for Scale | BANANA | ≈ 54 M$ | 2024-11-15 | -99,95 % | commune | copie ou ancienne version d'une carte; mort |
| `spike` | Spike | SPIKE | ≈ 54 M$ | 2024-06-10 | -99,91 % | commune | mort |
| `elon` | Eloncoin | ELON | ≈ 53 M$ | 2024-06-04 | -99,78 % | commune | mort |
| `golazo-world` | Golazo.world | GOL | ≈ 53 M$ | 2024-05-21 | -99,96 % | commune | mort |
| `scottyai` | ScottyTheAi | SCOTTY | ≈ 53 M$ | 2024-03-26 | -99,91 % | commune | mort |
| `bitcoin20` | Bitcoin20 | BTC20 | ≈ 53 M$ | 2023-08-16 | -99,79 % | commune | mort |
| `kasper` | Kasper | KASPER | ≈ 52 M$ | 2024-10-21 | -99,63 % | commune | mort |
| `klaus` | KLAUS | KLAUS | ≈ 52 M$ | 2024-10-16 | -99,92 % | commune | mort |
| `enkryptedai` | EnKryptedAI | KRAI | ≈ 52 M$ | 2025-07-29 | -100,00 % | commune | mort |
| `financial-freedom` | 財務自由 (Financial Freedom) | 財務自由 | ≈ 52 M$ | 2025-10-08 | -99,87 % | commune |  |
| `biaoqing` | Biaoqing | BIAO | ≈ 51 M$ | 2024-06-19 | -99,86 % | commune | mort |
| `flovi-inu` | Flovi Inu | FLOVI | ≈ 51 M$ | 2024-04-08 | -99,97 % | commune | mort |
| `dinolfg` | DinoLFG | DINO | ≈ 51 M$ | 2023-05-07 | -99,88 % | commune | mort |
| `integrity-dao` | Integrity DAO | ID | ≈ 51 M$ | 2025-06-06 | -99,97 % | commune | nature à vérifier; mort |
| `ski-mask-cat` | SKI MASK CAT | SKICAT | ≈ 51 M$ | 2024-12-10 | -99,84 % | commune | mort |
| `crogecoin` | Crogecoin | CROGE | ≈ 51 M$ | 2022-04-07 | -99,52 % | commune | mort |
| `omega-2` | Omega | OMEGA | ≈ 50 M$ | 2024-11-22 | -99,95 % | commune | mort |
| `tn100x` | TN100x | TN100X | ≈ 50 M$ | 2024-05-07 | -99,92 % | commune | mort |
| `super-inu-force` | Super Inu Force | SIF | ≈ 50 M$ | 2026-10-06 | -99,99 % | commune | mort |
| `high-af` | High AF | ATH | ≈ 50 M$ | 2024-12-02 | -99,99 % | commune | mort |
| `super-iguana` | Super Iguana | SI | ≈ 50 M$ | 2026-10-04 | -99,99 % | commune | mort |
| `oggy-inu` | Oggy Inu | OGGY | ≈ 50 M$ | 2023-05-07 | -99,79 % | commune | mort |
| `cute-cat-token` | Cute Cat Candle | CCC | ≈ 49 M$ | 2024-04-10 | -99,94 % | commune | mort |
| `pepe-bundle` | Pepe Bundle | PUNDLE | ≈ 49 M$ | 2025-08-01 | -99,99 % | commune | mort |
| `bucky-2` | Bucky | BUCKY | ≈ 49 M$ | 2025-08-06 | -99,82 % | commune | mort |
| `dogshit-2` | DOGSHIT | DOGSHIT | ≈ 49 M$ | 2025-09-14 | -99,88 % | commune | mort |
| `startup` | Startup | STARTUP | ≈ 49 M$ | 2025-07-02 | -99,93 % | commune | mort |
| `griffain-new-hedge-fund` | Griffain New Hedge Fund | CITADAIL | ≈ 49 M$ | 2025-01-08 | -99,93 % | commune | mort |
| `moss` | MOSS AI | MOSS | ≈ 49 M$ | 2025-01-03 | -99,89 % | commune | nature à vérifier; mort |
| `iq50` | IQ50 | IQ50 | ≈ 49 M$ | 2024-03-20 | -99,63 % | commune | mort |
| `punch-2` | パンチ (Punch) | PUNCH | ≈ 48 M$ | 2026-02-22 | -99,50 % | commune |  |
| `andy-on-sol` | Andy on SOL | ANDY | ≈ 48 M$ | 2024-03-14 | -99,90 % | commune | mort |
| `meme-trumpcoin` | Meme TrumpCoin | TRUMP | ≈ 48 M$ | 2025-01-20 | -99,99 % | commune | mort |
| `bobo` | Bobo | BOBO | ≈ 48 M$ | 2023-07-30 | -99,72 % | commune | copie ou ancienne version d'une carte; mort |
| `goats-2` | GOATS | GOATS | ≈ 48 M$ | 2024-12-05 | -99,67 % | commune | mort |
| `meme-moguls` | Meme Moguls | MGLS | ≈ 48 M$ | 2024-03-13 | -99,87 % | commune | mort |
| `sci-hub` | sci-hub | SCIHUB | ≈ 48 M$ | 2024-11-20 | -99,91 % | commune | mort |
| `harold` | Harold | HAROLD | ≈ 48 M$ | 2024-04-02 | -99,94 % | commune | copie ou ancienne version d'une carte; mort |
| `u` | U | U | ≈ 47 M$ | 2025-08-14 | -99,93 % | commune | mort |
| `tiger-shark` | Tiger Shark | TIGERSHARK | ≈ 47 M$ | 2025-05-28 | -99,99 % | commune | mort |
| `sage-universe` | Sage Universe | SAGE | ≈ 47 M$ | 2024-07-04 | -99,93 % | commune | mort |
| `spike-2` | Spike | SPIKE | ≈ 47 M$ | 2024-07-11 | -99,96 % | commune | mort |
| `spurdo-on-eth` | SPURDO ON ETH | SPURDO | ≈ 47 M$ | 2024-07-26 | -99,89 % | commune | mort |
| `meta-monopoly` | Meta Monopoly | MONOPOLY | ≈ 47 M$ | 2024-09-21 | -99,98 % | commune | mort |
| `culo` | CULO | CULO | ≈ 47 M$ | 2024-03-14 | -99,99 % | commune | mort |
| `schizo-terminal` | Mindscraft | MINDS | ≈ 46 M$ | 2025-01-12 | -99,97 % | commune | mort |
| `tech` | NumberGoUpTech | TECH | ≈ 46 M$ | 2024-03-11 | -99,94 % | commune | mort |
| `earl` | earl | EARL | ≈ 46 M$ | 2024-11-15 | -99,97 % | commune | mort |
| `fu` | FU | FU | ≈ 46 M$ | 2024-10-07 | -99,83 % | commune | mort |
| `bretter-brett` | Bretter Brett | BRETT | ≈ 46 M$ | 2024-06-12 | -99,70 % | commune | mort |
| `regent` | REGENT | REGENT | ≈ 46 M$ | 2025-01-24 | -99,94 % | commune | mort |
| `iq6900` | IQ6900 [OLD] | IQ | ≈ 46 M$ | 2025-01-07 | -99,95 % | commune | mort |
| `abster` | Abster | ABSTER | ≈ 46 M$ | 2025-08-09 | -99,97 % | commune | mort |
| `satozhi` | Satozhi | SATOZ | ≈ 46 M$ | 2021-05-09 | -99,82 % | commune | mort |
| `sonic-the-goat` | Sonic The Goat | GOAT | ≈ 46 M$ | 2024-05-07 | -99,84 % | commune | mort |
| `obi-pnut-kenobi` | Obi PNut Kenobi | OPK | ≈ 46 M$ | 2024-11-13 | -99,92 % | commune | mort |
| `speedy-2` | Speedy | SPEEDY | ≈ 46 M$ | 2024-10-31 | -99,75 % | commune | mort |
| `kango` | KANGO | KANGO | ≈ 46 M$ | 2024-11-22 | -99,87 % | commune | mort |
| `ndq666` | NDQ666 | NDQ | ≈ 46 M$ | 2025-10-08 | -99,96 % | commune | mort |
| `hood-inu` | Hood Inu | HI | ≈ 45 M$ | 2026-10-05 | -99,99 % | commune | mort |
| `trillions` | Trillions | TRILLIONS | ≈ 45 M$ | 2025-09-27 | -99,61 % | commune | mort |
| `lifedog` | lifedog | LFDOG | ≈ 44 M$ | 2024-12-04 | -99,98 % | commune | mort |
| `dogecast` | Dogecast | DOGECAST | ≈ 44 M$ | 2025-01-15 | -99,93 % | commune | mort |
| `shibaken-finance` | Shibaken Finance | SHIBAKEN | ≈ 44 M$ | 2021-05-11 | -99,65 % | commune | nature à vérifier; mort |
| `fat-choi` | fat choi | 发财 | ≈ 44 M$ | 2026-05-25 | -99,99 % | commune | mort |
| `balls-of-fate` | Balls of Fate | BOF | ≈ 44 M$ | 2024-09-21 | -99,98 % | commune | mort |
| `tardi` | Tardi | TARDI | ≈ 44 M$ | 2024-12-16 | -99,72 % | commune | mort |
| `what-in-tarnation` | What in Tarnation? | WIT | ≈ 43 M$ | 2024-04-11 | -99,96 % | commune | mort |
| `dogey-inu` | Dogey-Inu | DINU | ≈ 43 M$ | 2021-11-15 | -99,80 % | commune | mort |
| `aiwithdaddyissues` | Aiwithdaddyissues | SHEGEN | ≈ 43 M$ | 2024-10-26 | -99,85 % | commune | mort |
| `bamboo-on-base` | Bamboo on Base | BAMBOO | ≈ 43 M$ | 2024-07-21 | -99,93 % | commune | mort |
| `wai-combinator-by-virtuals` | WAI Combinator by Virtuals | WAI | ≈ 43 M$ | 2025-01-02 | -99,97 % | commune | mort |
| `elon-trump-fart` | Elon Trump Fart | ETF500 | ≈ 43 M$ | 2025-01-26 | -99,80 % | commune | mort |
| `petunia` | Petunia | PETUNIA | ≈ 43 M$ | 2024-11-14 | -99,96 % | commune |  |
| `invest-zone` | Invest Zone | IVFUN | ≈ 43 M$ | 2024-08-27 | -99,73 % | commune | mort |
| `chili` | CHILI | CHILI | ≈ 42 M$ | 2023-01-06 | -100,00 % | commune | mort |
| `fatcoin-2` | FATCOIN | FATCOIN | ≈ 42 M$ | 2026-09-04 | -99,67 % | commune |  |
| `ai16zeliza` | ai16zeliza | ELIZA | ≈ 42 M$ | 2024-11-19 | -99,81 % | commune | mort |
| `crazyfootball-token` | CrazyFootball token | FOOTBALL | ≈ 42 M$ | 2025-12-06 | -100,00 % | commune | mort |
| `mimany` | MIMANY | MIMANY | ≈ 42 M$ | 2024-04-09 | -99,95 % | commune | mort |
| `believe-in-something-2` | believe in something | DTF | ≈ 42 M$ | 2024-12-03 | -99,78 % | commune | mort |
| `bop-cat` | Bop Cat | BOP | ≈ 42 M$ | 2024-11-18 | -99,84 % | commune | mort |
| `neversol` | neversol | NEVER | ≈ 41 M$ | 2024-03-14 | -99,97 % | commune | mort |
| `bubb` | Bubb | BUBB | ≈ 41 M$ | 2025-03-21 | -99,92 % | commune | mort |
| `apes-2` | APES [OLD] | APES | ≈ 41 M$ | 2024-08-29 | -99,97 % | commune | copie ou ancienne version d'une carte; mort |
| `ghiblification` | Ghiblification | GHIBLI | ≈ 41 M$ | 2025-03-27 | -99,80 % | commune | mort |
| `stonks-on-eth` | Stonks on ETH | STONKS | ≈ 41 M$ | 2024-06-12 | -99,75 % | commune | mort |
| `drpepe-ai` | DrPepe.ai | BRYAN | ≈ 41 M$ | 2025-01-03 | -99,98 % | commune | nature à vérifier; mort |
| `lol-3` | LOL | LOL | ≈ 41 M$ | 2024-11-14 | -99,85 % | commune | mort |
| `kokok-the-roach` | KoKoK The Roach | KOKOK | ≈ 41 M$ | 2025-06-05 | -99,77 % | commune | mort |
| `3lon` | 3lon | 3LON | ≈ 40 M$ | 2026-06-19 | -100,00 % | commune | mort |
| `kolin-2` | Kolin | KOLIN | ≈ 40 M$ | 2025-01-15 | -99,83 % | commune | mort |
| `rocky-the-rock` | Rocky | ROCKY | ≈ 40 M$ | 2024-07-11 | -99,88 % | commune | mort |
| `coinye-west` | Coinye West | COINYE | ≈ 40 M$ | 2024-04-01 | -99,69 % | commune | mort |
| `suwi` | suwi | SUWI | ≈ 40 M$ | 2024-11-13 | -99,93 % | commune | mort |
| `upside-down-meme` | WEWECOIN | WEWE | ≈ 40 M$ | 2024-07-21 | -99,81 % | commune | mort |
| `seamania` | SEAMANIA | SEAMANIA | ≈ 39 M$ | 2025-01-23 | -99,89 % | commune | mort |
| `agent-cat` | Agent Cat | AGENTCAT | ≈ 39 M$ | 2026-10-05 | -99,99 % | commune | nature à vérifier; mort |
| `cat-terminal` | CAT Terminal | CAT | ≈ 39 M$ | 2025-10-06 | -99,92 % | commune | mort |
| `blinkdotfun` | blinkdotfun | BLINK | ≈ 39 M$ | 2024-12-16 | -99,90 % | commune | mort |
| `american-shiba` | American Shiba | USHIBA | ≈ 39 M$ | 2021-06-04 | -99,62 % | commune | mort |
| `abi` | Abi | ABI | ≈ 39 M$ | 2024-11-13 | -99,99 % | commune | mort |
| `a-gently-used-2001-honda` | A Gently Used 2001 Honda | USEDCAR | ≈ 39 M$ | 2023-12-29 | -99,70 % | commune | mort |
| `wap` | WAP | WAP | ≈ 39 M$ | 2024-10-12 | -99,94 % | commune | mort |
| `agent-s` | Agent S | S | ≈ 39 M$ | 2025-01-08 | -99,75 % | commune | nature à vérifier; mort |
| `candle-tv` | Candle TV | CANDLE | ≈ 38 M$ | 2025-05-29 | -99,79 % | commune | mort |
| `centience` | Centience | CENTS | ≈ 38 M$ | 2024-11-23 | -99,89 % | commune | mort |
| `baby-shark` | Baby Shark | SHARK | ≈ 38 M$ | 2021-06-03 | -99,86 % | commune | mort |
| `jam-cat` | jam cat | JAM | ≈ 38 M$ | 2024-11-14 | -99,85 % | commune | mort |
| `max-on-eth` | Max on ETH | MAXETH | ≈ 38 M$ | 2024-12-11 | -99,62 % | commune | mort |
| `bitcat-3` | Bitcat | BITCAT | ≈ 38 M$ | 2024-11-16 | -99,89 % | commune | mort |
| `flowerai` | FlowerAI | FLOWER | ≈ 37 M$ | 2024-11-23 | -99,94 % | commune | mort |
| `black-unicorn-corp` | Black Unicorn Corp. | MOON | ≈ 37 M$ | 2024-12-18 | -99,90 % | commune | mort |
| `booze` | Booze | BOOZE | ≈ 37 M$ | 2026-09-05 | -99,84 % | commune | mort |
| `uni` | Uni | UNI | ≈ 37 M$ | 2024-11-14 | -99,84 % | commune | mort |
| `satoshitcoin` | SatoshitCoin | SATOSHIT | ≈ 37 M$ | 2025-08-20 | -99,99 % | commune | mort |
| `based-bunny` | Based Bunny | BUNNY | ≈ 37 M$ | 2024-04-25 | -99,97 % | commune | mort |
| `effective-accelerationism` | Effective accelerationism | E/ACC | ≈ 37 M$ | 2024-11-11 | -99,89 % | commune | mort |
| `meme-anarchic-numismatic-asset` | Meme Anarchic Numismatic Asset | MANA | ≈ 37 M$ | 2024-12-15 | -99,91 % | commune | mort |
| `super-inu-accelerationism` | Super Inu Accelerationism | SI/ACC | ≈ 37 M$ | 2026-09-28 | -99,99 % | commune | mort |
| `bnb-meme-szn` | BNB MEME SZN | SZN | ≈ 37 M$ | 2025-10-08 | -99,81 % | commune |  |
| `daram` | Daram | DARAM | ≈ 36 M$ | 2024-10-19 | -99,94 % | commune | mort |
| `littlemanyu` | littlemanyu | MANYU | ≈ 36 M$ | 2024-10-07 | -99,82 % | commune | mort |
| `flork-cto` | FLORK CTO | FLORK | ≈ 36 M$ | 2025-01-07 | -99,91 % | commune | mort |
| `ribbit-meme` | Ribbit Meme | RIBBIT | ≈ 36 M$ | 2023-05-06 | -99,69 % | commune | mort |
| `mist-2` | MIST | 霞 | ≈ 36 M$ | 2024-11-13 | -99,94 % | commune | mort |
| `pepesol` | PepeSol | PEPE | ≈ 36 M$ | 2024-03-09 | -99,54 % | commune | mort |
| `yellow-pepe-2` | Yellow Pepe | YEPE | ≈ 36 M$ | 2025-10-08 | -99,77 % | commune | mort |
| `magnetix` | Magnetix | MAG | ≈ 36 M$ | 2025-03-23 | -99,85 % | commune | mort |
| `gochujangcoin` | Gochujangcoin | GOCHU | ≈ 36 M$ | 2025-05-30 | -99,78 % | commune | mort |
| `maya` | Maya | MAYA | ≈ 36 M$ | 2024-11-14 | -99,96 % | commune | mort |
| `space-troll` | SPACE TROLL | SPCTROLL | ≈ 36 M$ | 2026-05-17 | -99,99 % | commune | mort |
| `69420` | 69420 | 69420 | ≈ 36 M$ | 2025-07-21 | -99,90 % | commune | mort |
| `elon-goat` | Elon GOAT | EGT | ≈ 35 M$ | 2022-02-12 | -99,75 % | commune | mort |
| `gtf` | GTF | GTF | ≈ 35 M$ | 2025-11-08 | -99,98 % | commune | mort |
| `charles-the-chad` | Charles the Chad | CHAD | ≈ 35 M$ | 2024-12-06 | -99,79 % | commune | mort |
| `rato-the-rat` | Rato The Rat | RATO | ≈ 35 M$ | 2025-05-11 | -99,75 % | commune | mort |
| `don-t-buy-inu` | Don't Buy Inu | DBI | ≈ 35 M$ | 2023-03-09 | -99,89 % | commune | mort |
| `priceless-2` | priceless | PRICELESS | ≈ 35 M$ | 2025-10-07 | -99,55 % | commune |  |
| `4` | 4 | FOUR | ≈ 35 M$ | 2024-08-23 | -99,94 % | commune | copie ou ancienne version d'une carte; mort |
| `monkey-taken-by-police` | Monkey Taken By Police | JORGIE | ≈ 35 M$ | 2024-11-14 | -99,94 % | commune | mort |
| `ordinal-doge` | Ordinal Doge | ODOGE | ≈ 35 M$ | 2023-03-06 | -99,86 % | commune | mort |
| `baby-tiger` | Baby Tiger | $BBT | ≈ 35 M$ | 2024-11-23 | -99,97 % | commune | mort |
| `virgen` | Virgen | VIRGEN | ≈ 34 M$ | 2025-05-28 | -99,59 % | commune | mort |
| `pajamas-cat` | Pajamas Cat | PAJAMAS | ≈ 34 M$ | 2024-05-30 | -99,65 % | commune | mort |
| `conan-2` | Conan | CONAN | ≈ 34 M$ | 2024-04-23 | -99,77 % | commune | mort |
| `aintivirus` | AIntivirus | AINTI | ≈ 34 M$ | 2025-05-01 | -99,97 % | commune | mort |
| `debtcoin` | DebtCoin | DEBT | ≈ 34 M$ | 2025-07-29 | -99,90 % | commune | mort |
| `sompi` | Sompi | SOMPI | ≈ 34 M$ | 2026-04-21 | -100,00 % | commune | mort |
| `xing-xing` | Xing Xing | XING | ≈ 34 M$ | 2024-11-22 | -99,77 % | commune | mort |
| `ethereum-is-good` | ETHEREUM IS GOOD | EBULL | ≈ 34 M$ | 2024-08-31 | -99,61 % | commune | mort |
| `zuzalu-inu` | Zuzalu Inu | ZUZALU | ≈ 34 M$ | 2024-01-16 | -99,80 % | commune | mort |
| `shiva-inu` | Shiva Inu | SHIV | ≈ 34 M$ | 2024-03-28 | -99,69 % | commune | mort |
| `mumu` | Mumu | MUMU | ≈ 34 M$ | 2024-04-01 | -99,79 % | commune | mort |
| `sympson-ai` | Sympson by Virtuals | $SYMP | ≈ 34 M$ | 2025-01-16 | -99,90 % | commune | mort |
| `mongy` | Mongy | MONGY | ≈ 33 M$ | 2024-07-19 | -99,96 % | commune | mort |
| `yak` | YAK | YAK | ≈ 33 M$ | 2024-03-15 | -99,95 % | commune | mort |
| `avarik-saga` | Avarik Saga | AVRK | ≈ 33 M$ | 2025-01-07 | -99,78 % | commune | mort |
| `pockemy` | Pockemy | PKM | ≈ 33 M$ | 2025-09-29 | -99,95 % | commune | mort |
| `identity-md-6900` | Identity.md 6900 | IMD6900 | ≈ 33 M$ | 2026-10-12 | -99,99 % | commune | mort |
| `horsecoin-2` | HorseCoin | 马币 | ≈ 33 M$ | 2026-04-07 | -99,91 % | commune | mort |
| `hana` | Hana | HANA | ≈ 33 M$ | 2024-09-30 | -99,85 % | commune | mort |
| `united-states-water-reserve` | United States Water Reserve | USWR | ≈ 33 M$ | 2026-07-25 | -99,58 % | commune | mort |
| `red-pill-2` | Red Pill | RPILL | ≈ 33 M$ | 2024-01-01 | -99,73 % | commune | mort |
| `yousim` | YouSim | YOUSIM | ≈ 33 M$ | 2024-11-14 | -99,89 % | commune | mort |
| `sealwifhat` | sealwifhat | SI | ≈ 32 M$ | 2024-03-14 | -99,95 % | commune | mort |
| `tate-terminal` | Tate Terminal | TATE | ≈ 32 M$ | 2024-10-29 | -99,90 % | commune | mort |
| `maga-vp` | MAGA VP | MVP | ≈ 32 M$ | 2024-05-17 | -99,93 % | commune | mort |
| `limbo` | LIMBO | LIMBO | ≈ 32 M$ | 2025-01-26 | -99,87 % | commune | mort |
| `lucky-dog` | Lucky Dog | LUCKY | ≈ 32 M$ | 2024-11-11 | -99,84 % | commune | mort |
| `make-eth-great-again` | Make ETH Great Again | MEGA | ≈ 32 M$ | 2024-06-10 | -99,84 % | commune | mort |
| `doge-pepe-3` | Doge Pepe | DOPE | ≈ 32 M$ | 2026-10-18 | -99,99 % | commune | copie ou ancienne version d'une carte; mort |
| `thales-ai` | Thales AI | THALES | ≈ 31 M$ | 2025-01-10 | -99,96 % | commune | nature à vérifier; mort |
| `pumpkin-4` | Pumpkin | PKIN | ≈ 31 M$ | 2025-02-10 | -99,76 % | commune | mort |
| `kakaxa` | Kakaxa | KAKAXA | ≈ 31 M$ | 2024-04-25 | -99,94 % | commune | mort |
| `trump-derangement-syndrome` | Trump Derangement Syndrome | TDS | ≈ 31 M$ | 2024-11-11 | -99,92 % | commune | mort |
| `wat` | Wat | WAT | ≈ 31 M$ | 2024-07-09 | -99,73 % | commune | mort |
| `fur-nancial-advisor` | Fur-nancial advisor | FUR | ≈ 31 M$ | 2024-11-18 | -99,96 % | commune | mort |
| `principals-network` | Principals Network | PNET | ≈ 31 M$ | 2024-12-15 | -99,96 % | commune | nature à vérifier; mort |
| `blinks-gg` | Blinks.gg | BGG1 | ≈ 31 M$ | 2024-12-12 | -99,82 % | commune | mort |
| `terry-in-the-trenches` | Terry In The Trenches | TERRY | ≈ 31 M$ | 2024-11-25 | -99,95 % | commune | mort |
| `bunker-mode` | Bunker Mode | BUNKER | ≈ 31 M$ | 2026-10-12 | -99,98 % | commune | mort |
| `christ-is-king` | Christ Is King | CIK | ≈ 31 M$ | 2025-05-21 | -99,87 % | commune | mort |
| `quantum-inu` | Quantum Inu | QI | ≈ 31 M$ | 2026-10-11 | -99,99 % | commune | mort |
| `satoshi-ai-agent-by-virtuals` | Satoshi AI agent by Virtuals | SAINT | ≈ 31 M$ | 2024-12-03 | -99,83 % | commune | nature à vérifier; mort |
| `frox` | Frox | FROX | ≈ 30 M$ | 2024-12-20 | -99,98 % | commune | mort |
| `cloudyheart` | cloudyheart | CLOUDY | ≈ 30 M$ | 2025-02-03 | -99,93 % | commune | mort |
| `vibe-cat-2` | Vibe Cat | VIBE | ≈ 30 M$ | 2024-11-20 | -99,83 % | commune | mort |
| `dogc` | DOGC | DOGC | ≈ 30 M$ | 2024-12-02 | -99,57 % | commune | mort |
| `silly-goose` | Silly Goose | GOO | ≈ 30 M$ | 2024-03-16 | -99,77 % | commune | mort |
| `vectorchat-ai` | VectorChat.ai | CHAT | ≈ 30 M$ | 2025-01-20 | -99,85 % | commune | nature à vérifier; mort |
| `marvin-inu` | Marvin Inu | MARVIN | ≈ 30 M$ | 2022-04-03 | -99,90 % | commune | mort |
| `hyperpigmentation` | Hyperpigmentation | $HYPER | ≈ 30 M$ | 2025-07-19 | -99,92 % | commune | mort |
| `rizo` | Rizo | RIZO | ≈ 30 M$ | 2024-03-24 | -99,78 % | commune | mort |
| `mowcat` | MowCat | MOW | ≈ 30 M$ | 2026-08-18 | -99,85 % | commune |  |
| `time` | TIME | TIME | ≈ 30 M$ | 2024-07-27 | -99,75 % | commune | mort |
| `hulvin` | HULVIN | HULVIN | ≈ 30 M$ | 2024-04-16 | -99,88 % | commune | mort |
| `flokifork` | FlokiFork | FORK | ≈ 30 M$ | 2024-03-08 | -99,93 % | commune | mort |
| `landwolf-2` | Landwolf | WOLF | ≈ 29 M$ | 2024-03-11 | -99,59 % | commune | copie ou ancienne version d'une carte; mort |
| `buttcoin-4` | Buttcoin | BUTTCOIN | ≈ 29 M$ | 2025-04-11 | -99,62 % | commune | copie ou ancienne version d'une carte |
| `soulguy` | SOULGUY | SOULGUY | ≈ 29 M$ | 2026-01-29 | -99,96 % | commune | mort |
| `rocky-the-dog` | Rocky the dog | ROCKY | ≈ 29 M$ | 2024-01-13 | -99,92 % | commune | mort |
| `beenz` | BEENZ | BEENZ | ≈ 29 M$ | 2025-01-28 | -99,87 % | commune | mort |
| `trust-me-bros-by-virtuals` | $TRUST ME BROs by Virtuals | TRUST | ≈ 29 M$ | 2025-01-04 | -99,96 % | commune | mort |
| `zeus-3` | ZEUS | ZEUS | ≈ 29 M$ | 2025-01-11 | -99,98 % | commune | mort |
| `keke-terminal` | KEKE Terminal | KEKE | ≈ 29 M$ | 2024-12-30 | -99,96 % | commune | mort |
| `magic-internet-cash` | Magic Internet Cash | MIC | ≈ 29 M$ | 2024-03-06 | -99,96 % | commune | mort |
| `sonic-snipe-bot` | Sonic Snipe Bot | SONIC | ≈ 29 M$ | 2024-12-13 | -99,58 % | commune | mort |
| `slop` | Slop | SLOP | ≈ 29 M$ | 2024-10-23 | -99,87 % | commune | mort |
| `ava-chiang-mai-night-safari-ava` | AVA Chiang Mai Night Safari (AVA) | AVA | ≈ 29 M$ | 2024-11-27 | -99,96 % | commune | mort |
| `meow-meow-meow-meow` | meow meow meow meow | MEOW | ≈ 29 M$ | 2024-12-19 | -99,94 % | commune | mort |
| `zeek-coin` | Zeek Coin | MEOW | ≈ 28 M$ | 2024-03-06 | -99,92 % | commune | mort |
| `kangal` | Kangal | KANGAL | ≈ 28 M$ | 2021-04-20 | -99,80 % | commune | mort |
| `unicorn-3` | Unicorn [OLD] | UWU | ≈ 28 M$ | 2024-08-13 | -99,77 % | commune | mort |
| `winter-arc` | Winter Arc | WINTER | ≈ 28 M$ | 2024-11-20 | -99,81 % | commune | mort |
| `lets-get-this-bread` | Lets Get This Bread | LGTB | ≈ 28 M$ | 2024-12-15 | -99,93 % | commune | mort |
| `catownkimono` | catownkimono | COK | ≈ 28 M$ | 2024-06-10 | -99,63 % | commune | mort |
| `moonwolf-io` | moonwolf.io | WOLF | ≈ 28 M$ | 2024-07-22 | -99,96 % | commune | mort |
| `weird-medieval-memes` | Weird Medieval Memes | WMM | ≈ 28 M$ | 2024-11-14 | -99,87 % | commune | mort |
| `moe-4` | MOE | MOE | ≈ 28 M$ | 2025-01-06 | -99,84 % | commune | mort |
| `jak` | JAK | JAK | ≈ 28 M$ | 2024-11-28 | -99,87 % | commune | mort |
| `sheep-wif-hat` | Sheep Wif Hat | SWIF | ≈ 28 M$ | 2025-08-12 | -99,78 % | commune | mort |
| `agentaigo` | CLAWLETT | CLAWLETT | ≈ 28 M$ | 2025-01-02 | -99,58 % | commune | mort |
| `baby-samo-coin` | Baby Samo Coin | BABY | ≈ 28 M$ | 2021-11-13 | -99,94 % | commune | mort |
| `monkeyhaircut` | monkeyhaircut | MONK | ≈ 28 M$ | 2024-05-09 | -99,75 % | commune | mort |
| `melon-dog` | Melon Dog | MELON | ≈ 28 M$ | 2024-03-13 | -99,88 % | commune | mort |
| `super-cat` | Super Cat | SC | ≈ 28 M$ | 2026-10-02 | -99,95 % | commune | mort |
| `bullballs-coin` | Bullballs Coin | BULLBALLS | ≈ 27 M$ | 2026-08-20 | -99,98 % | commune | mort |
| `soldoge` | SolDoge | SDOGE | ≈ 27 M$ | 2021-11-01 | -99,95 % | commune | mort |
| `doge-pepe` | Doge Pepe | DOPE | ≈ 27 M$ | 2026-10-14 | -99,92 % | commune | copie ou ancienne version d'une carte; mort |
| `slopfather` | Slopfather | FATHA | ≈ 27 M$ | 2024-12-01 | -99,86 % | commune | mort |
| `cato` | CATO | CATO | ≈ 27 M$ | 2021-08-21 | -99,85 % | commune | mort |
| `doge` | @DOGE | @DOGE | ≈ 27 M$ | 2024-11-15 | -99,90 % | commune | mort |
| `uranus-sol` | URANUS (SOL) | ANUS | ≈ 27 M$ | 2024-03-31 | -99,85 % | commune | mort |
| `the-professor` | The Professor | LAB | ≈ 27 M$ | 2024-06-11 | -99,96 % | commune | mort |
| `doggo-3` | Doggo | DOGGO | ≈ 27 M$ | 2024-10-02 | -99,72 % | commune | mort |
| `buu` | BUU | BUU | ≈ 27 M$ | 2024-11-12 | -99,83 % | commune | mort |
| `baked` | Baked | BAKED | ≈ 27 M$ | 2024-09-30 | -99,67 % | commune | mort |
| `pandu-pandas` | Pandu Pandas [OLD] | PANDU | ≈ 27 M$ | 2025-10-05 | -99,75 % | commune | mort |
| `glp1` | GLP1 | GLP1 | ≈ 27 M$ | 2024-11-24 | -99,96 % | commune | mort |
| `super-inu` | Super Inu | SI | ≈ 27 M$ | 2026-09-26 | -99,97 % | commune | copie ou ancienne version d'une carte; mort |
| `kwantxbt` | kwantxbt | KWANT | ≈ 27 M$ | 2025-01-02 | -99,94 % | commune | mort |
| `usacoin` | USAcoin | USACOIN | ≈ 27 M$ | 2024-12-21 | -99,73 % | commune | mort |
| `book-of-billionaires` | BOOK OF BILLIONAIRES | BOBE | ≈ 27 M$ | 2024-05-02 | -99,96 % | commune | mort |
| `catamoto` | Catamoto | CATA | ≈ 26 M$ | 2024-04-22 | -99,93 % | commune | mort |
| `vibing-cat` | Vibing Cat | VCAT | ≈ 26 M$ | 2024-03-14 | -99,90 % | commune | mort |
| `pump` | Pump | PUMP | ≈ 26 M$ | 2024-03-05 | -99,74 % | commune | mort |
| `based` | BASED | BASED | ≈ 26 M$ | 2024-11-13 | -99,82 % | commune | mort |
| `arc-chan` | Arc Chan | ARCHAN | ≈ 26 M$ | 2026-09-27 | -99,99 % | commune | mort |
| `moon-doge-coin` | Moon Doge Coin | MOONDOGECOIN | ≈ 26 M$ | 2026-07-31 | -99,98 % | commune | mort |
| `zorro` | Zorro | ZORRO | ≈ 26 M$ | 2024-03-31 | -99,90 % | commune | mort |
| `marvin-inu-2` | Marvin Inu | MARVIN | ≈ 26 M$ | 2024-11-17 | -99,83 % | commune | mort |
| `jaihoz` | Jaihoz by Virtuals | JAIHOZ | ≈ 26 M$ | 2025-01-10 | -99,68 % | commune | mort |
| `chuck` | Chuck | CHUCK | ≈ 25 M$ | 2024-05-09 | -99,63 % | commune | mort |
| `dogecoin-2` | Dogecoin 2.0 | DOGE2 | ≈ 25 M$ | 2021-09-03 | -100,00 % | commune | mort |
| `gpu-ai-rich` | GPU ai Rich | RICH | ≈ 25 M$ | 2025-01-09 | -99,92 % | commune | nature à vérifier; mort |
| `psyopcoin` | PsyopCoin | PSYOP | ≈ 25 M$ | 2025-07-21 | -99,96 % | commune | mort |
| `zoomer-sol` | Zoomer | ZOOMER | ≈ 25 M$ | 2024-07-26 | -99,92 % | commune | mort |
| `end-federal-reserve` | End Federal Reserve | EFR | ≈ 25 M$ | 2024-11-23 | -99,97 % | commune | mort |
| `noot-noot` | Noot Noot | NOOT | ≈ 25 M$ | 2025-03-28 | -99,91 % | commune | mort |
| `lea-ai` | LEA AI | LEA | ≈ 25 M$ | 2025-01-25 | -99,69 % | commune | nature à vérifier; mort |
| `briun-armstrung` | Briun Armstrung | BRIUN | ≈ 25 M$ | 2024-03-20 | -99,86 % | commune | mort |
| `taylor-swift-s-cat` | Taylor Swift's Cat Benji | BENJI | ≈ 25 M$ | 2024-03-09 | -99,90 % | commune | mort |
| `world-collective-oil-reserve` | World Collective Oil Reserve | WCOR | ≈ 25 M$ | 2026-05-19 | -99,72 % | commune | mort |
| `andy-2` | Andy | ANDY | ≈ 25 M$ | 2024-06-30 | -99,87 % | commune | copie ou ancienne version d'une carte; mort |
| `ligma-node` | Ligma Node | LIGMA | ≈ 25 M$ | 2024-04-03 | -99,96 % | commune | mort |
| `sbrsol` | Strategic Bitcoin Reserve | SBR | ≈ 25 M$ | 2025-01-19 | -99,76 % | commune | mort |
| `inu-wif-sword` | inu wif sword | SWORDINU | ≈ 25 M$ | 2026-10-07 | -99,99 % | commune | mort |
| `goatindex-ai` | GoatIndex.ai | AIAI | ≈ 25 M$ | 2025-01-23 | -99,57 % | commune | nature à vérifier; mort |
| `eye-earn` | Smilek [OLD] | SMILEK | ≈ 25 M$ | 2024-04-17 | -99,95 % | commune | mort |
| `beercoin2` | Beercoin 2 | BEER2 | ≈ 25 M$ | 2025-05-30 | -99,83 % | commune | mort |
| `emotional-support-alligator` | Emotional Support Alligator | WALLY | ≈ 25 M$ | 2024-11-25 | -99,93 % | commune | mort |
| `real-fast` | real fast | SPEED | ≈ 25 M$ | 2024-05-29 | -99,69 % | commune | mort |
| `pepe-the-king-prawn` | Pepe the King Prawn | PRAWN | ≈ 25 M$ | 2024-12-08 | -99,88 % | commune | mort |
| `bazinga-2` | Bazinga | BAZINGA | ≈ 25 M$ | 2024-06-02 | -99,89 % | commune | mort |
| `defiant-2` | Defiant | DEFIANT | ≈ 25 M$ | 2025-04-17 | -99,98 % | commune | nature à vérifier; mort |
| `elon-s-space-cat` | Elon's Space Cat | CATALORIAN | ≈ 25 M$ | 2026-08-24 | -99,98 % | commune | mort |
| `pelfort` | PELFORT | PELF | ≈ 25 M$ | 2024-03-11 | -99,75 % | commune | mort |
| `puffy` | Puffy | PUFFY | ≈ 25 M$ | 2024-10-11 | -99,90 % | commune | mort |
| `peanie` | peanie | PEANIE | ≈ 25 M$ | 2024-05-20 | -99,84 % | commune | mort |
| `stream-until-100m-mc` | Stream until 100M MC | LIVE | ≈ 25 M$ | 2024-11-22 | -99,68 % | commune | mort |
| `le-chonk` | Le Chonk | CHONK | ≈ 25 M$ | 2026-10-06 | -99,99 % | commune | mort |
| `bubbles-2` | BUBBLES | BUBBLES | ≈ 25 M$ | 2024-10-06 | -99,84 % | commune | mort |
| `wall-street-baby-on-solana` | Wall Street Baby On Solana | WSB | ≈ 24 M$ | 2024-04-12 | -99,95 % | commune | mort |
| `rawr` | Rawr | XD | ≈ 24 M$ | 2024-10-14 | -99,79 % | commune | mort |
| `pulse-inu-2` | Pulse Inu | PINU | ≈ 24 M$ | 2026-08-24 | -99,91 % | commune | mort |
| `catzcoin` | CatzCoin | CATZ | ≈ 24 M$ | 2021-05-16 | -99,72 % | commune | mort |
| `67coin` | 67COIN | 67 | ≈ 24 M$ | 2025-09-09 | -99,89 % | commune | mort |
| `urmom-3` | urmom | URMOM | ≈ 24 M$ | 2026-08-24 | -99,92 % | commune | mort |
| `snake-wif-hat` | Snake wif Hat | SSSSS | ≈ 24 M$ | 2024-11-26 | -99,94 % | commune | mort |
| `outlaw-crypto-games` | OUTLAW Crypto Games | OUTLAW | ≈ 24 M$ | 2025-09-12 | -99,91 % | commune | nature à vérifier; mort |
| `astropepex` | AstroPepeX | APX | ≈ 24 M$ | 2024-11-18 | -99,78 % | commune | mort |
| `hyperskids` | $HYPERSKIDS | HYPERSKIDS | ≈ 24 M$ | 2025-02-22 | -99,77 % | commune | mort |
| `jeje` | JEJE | JJ | ≈ 24 M$ | 2024-05-30 | -99,66 % | commune | mort |
| `robot-2` | ROBOT | ROBOT | ≈ 24 M$ | 2025-05-24 | -99,98 % | commune | mort |
| `fomo-3d` | FOMO 3D | FOMO3D.FUN | ≈ 24 M$ | 2024-12-31 | -99,96 % | commune | mort |
| `white-boy-summer` | White Boy Summer | WBS | ≈ 24 M$ | 2024-05-22 | -99,88 % | commune | mort |
| `ducky` | Ducky [OLD] | DUCKY | ≈ 24 M$ | 2024-11-15 | -99,89 % | commune | mort |
| `fottie` | Fottie | FOTTIE | ≈ 24 M$ | 2024-03-09 | -99,80 % | commune | mort |
| `poop` | Poop | POOP | ≈ 24 M$ | 2025-08-14 | -99,88 % | commune | mort |
| `sora-ai` | Sora AI | SORA | ≈ 24 M$ | 2024-02-18 | -99,70 % | commune | nature à vérifier; mort |
| `okayeg` | Okayeg | OKAYEG | ≈ 23 M$ | 2024-05-21 | -99,58 % | commune | mort |
| `erha` | Erha | 二哈 | ≈ 23 M$ | 2025-08-26 | -99,99 % | commune | mort |
| `andy70b` | ANDY70B | ANDY70B | ≈ 23 M$ | 2024-12-21 | -99,94 % | commune | mort |
| `rex-3` | Rex | REX | ≈ 23 M$ | 2024-11-17 | -99,93 % | commune | mort |
| `claudia-4` | Claudia | CLAUDIA | ≈ 23 M$ | 2026-10-13 | -99,99 % | commune | copie ou ancienne version d'une carte; mort |
| `cat-token` | Mooncat CAT | CAT | ≈ 23 M$ | 2021-11-01 | -99,88 % | commune | mort |
| `ropirito` | Ropirito | ROPIRITO | ≈ 23 M$ | 2024-11-21 | -99,92 % | commune | mort |
| `bolt-on-base` | BOLT on Base | BOLT | ≈ 23 M$ | 2024-06-09 | -99,85 % | commune | mort |
| `rugman` | RUGMAN | $RUG | ≈ 23 M$ | 2024-12-08 | -99,88 % | commune | mort |
| `jungledoge` | JungleDoge | JUNGLE | ≈ 23 M$ | 2024-05-29 | -99,86 % | commune | mort |
| `hodl-6` | HODL | HODL | ≈ 23 M$ | 2025-10-07 | -99,89 % | commune | copie ou ancienne version d'une carte; mort |
| `shrub-2` | Shrub | $SHRUB | ≈ 23 M$ | 2024-11-13 | -99,86 % | commune | copie ou ancienne version d'une carte; mort |
| `lily-s-coin` | Lily's Coin | LILY | ≈ 23 M$ | 2024-11-12 | -99,97 % | commune | mort |
| `latina-language-model` | Latina Language Model | LLM | ≈ 23 M$ | 2025-08-25 | -99,97 % | commune | mort |
| `arie-the-sealion` | Arie The Sealion | ARIE | ≈ 23 M$ | 2024-11-19 | -99,95 % | commune | mort |
| `watcoin` | WATCoin | WAT | ≈ 23 M$ | 2024-09-23 | -99,89 % | commune | mort |
| `maga-pepe-2` | MAGA Pepe | MAPE | ≈ 23 M$ | 2024-07-17 | -99,92 % | commune | mort |
| `degenerative-sitcom` | degenerative SITCOM | $SITCOM | ≈ 23 M$ | 2024-12-01 | -99,60 % | commune | mort |
| `xenopus-laevis` | Xenopus laevis | XENO | ≈ 23 M$ | 2024-12-30 | -99,85 % | commune | mort |
| `hungarian-vizsla-inu` | Hungarian Vizsla Inu | HVI | ≈ 23 M$ | 2021-08-11 | -99,72 % | commune | mort |
| `manlet` | manlet | MANLET | ≈ 23 M$ | 2026-07-04 | -99,88 % | commune | mort |
| `larp-detective-agency` | Larp Detective Agency | $AGENCY | ≈ 23 M$ | 2025-01-02 | -99,95 % | commune | mort |
| `curtis` | Curtis | CURTIS | ≈ 23 M$ | 2024-10-24 | -99,63 % | commune | mort |
| `won-chang` | Won Chang | USDWON | ≈ 23 M$ | 2025-09-17 | -99,96 % | commune | mort |
| `koto-2` | Koto | KOTO | ≈ 22 M$ | 2024-11-14 | -99,90 % | commune | mort |
| `r-snoofi` | r/snoofi | R/SNOOFI | ≈ 22 M$ | 2024-11-15 | -99,73 % | commune | mort |
| `1-squirrel` | OG Peanut | PEANUT | ≈ 22 M$ | 2024-11-25 | -99,62 % | commune | mort |
| `blobana-pet` | Blobana pet | BLOB | ≈ 22 M$ | 2024-11-24 | -99,92 % | commune | mort |
| `gou` | Gou | GOU | ≈ 22 M$ | 2024-09-25 | -99,83 % | commune | mort |
| `altai-the-tiger` | Altai the Tiger | ALTAI | ≈ 22 M$ | 2026-10-15 | -99,99 % | commune | mort |
| `no-crying-in-the-casino` | no crying in the casino | CASINO | ≈ 22 M$ | 2026-10-15 | -99,99 % | commune | mort |
| `h2w6gm6jz` | h2w6gm6jz | H2W6GM6JZ | ≈ 22 M$ | 2024-12-20 | -99,94 % | commune | mort |
| `blaze` | Blaze | BLAZE | ≈ 22 M$ | 2025-07-01 | -99,81 % | commune | mort |
| `babylong` | BABYLONG | $BABYLONG | ≈ 22 M$ | 2024-05-17 | -99,60 % | commune | mort |
| `baby-wen` | Baby Wen | BWEN | ≈ 22 M$ | 2024-11-05 | -99,88 % | commune | mort |
| `billionhappiness` | BillionHappiness | BHC | ≈ 22 M$ | 2021-04-06 | -99,95 % | commune | mort |
| `hot-doge-2` | Hot Doge | HOTDOGE | ≈ 22 M$ | 2024-12-13 | -99,97 % | commune | mort |
| `goodboy` | GoodBoy | GOODBOY | ≈ 22 M$ | 2024-12-22 | -99,97 % | commune | mort |
| `long-5` | 龙Long | 龙LONG | ≈ 22 M$ | 2025-10-13 | -99,90 % | commune | mort |
| `super-shiba-2` | Super Shiba | SS | ≈ 22 M$ | 2026-10-06 | -99,99 % | commune | mort |
| `naitzsche` | Naitzsche | NAI | ≈ 22 M$ | 2024-12-15 | -99,92 % | commune | mort |
| `america-party` | America Party | AP | ≈ 22 M$ | 2025-07-05 | -99,63 % | commune | copie ou ancienne version d'une carte; mort |
| `hex-com-diamond` | HEX.COM DIAMOND | DMND | ≈ 22 M$ | 2026-08-21 | -99,90 % | commune | mort |
| `sword-inu` | Sword Inu | SI | ≈ 21 M$ | 2026-10-14 | -99,99 % | commune | mort |
| `bepe` | BEPE | BEPE | ≈ 21 M$ | 2024-12-12 | -99,95 % | commune | mort |
| `bork-2` | Bork | BORK | ≈ 21 M$ | 2024-03-08 | -99,80 % | commune | mort |
| `belief` | BELIEF | BELIEF | ≈ 21 M$ | 2026-04-22 | -99,97 % | commune | mort |
| `american-ai-fund` | American AI Fund | AAIF | ≈ 21 M$ | 2026-07-25 | -99,93 % | commune | nature à vérifier; mort |
| `plebz` | Plebz | PLEB | ≈ 21 M$ | 2024-03-31 | -99,96 % | commune | mort |
| `cheeseball` | Cheeseball | CB | ≈ 21 M$ | 2024-10-10 | -99,87 % | commune | mort |
| `devin-on-solana` | Devin | DEVIN | ≈ 21 M$ | 2024-06-03 | -99,54 % | commune | mort |
| `ton-cat` | Ton Cat | TCAT | ≈ 21 M$ | 2024-07-06 | -99,76 % | commune | mort |
| `cat-wif-hood` | cat wif hood | HOODCAT | ≈ 21 M$ | 2026-10-11 | -99,99 % | commune | mort |
| `based-shiba-inu` | Based Shiba Inu | BSHIB | ≈ 21 M$ | 2024-03-20 | -99,88 % | commune | mort |
| `super-suiyan` | Super Suiyan | SUIYAN | ≈ 21 M$ | 2025-05-23 | -99,91 % | commune | mort |
| `useless-stonk` | USELESS STONK | STONKLESS | ≈ 21 M$ | 2026-09-09 | -99,99 % | commune | mort |
| `vorta-markets` | Vorta Markets | VORTA | ≈ 21 M$ | 2026-10-10 | -99,99 % | commune | mort |
| `baby-pepe-2` | Baby Pepe | BABYPEPE | ≈ 21 M$ | 2024-06-04 | -99,78 % | commune | mort |
| `brett` | Brett | BRETT | ≈ 21 M$ | 2024-03-10 | -99,61 % | commune | copie ou ancienne version d'une carte; mort |
| `solcat` | SOLCAT | SOLCAT | ≈ 21 M$ | 2024-11-26 | -99,95 % | commune | mort |
| `drip` | DRIP | $DRIP | ≈ 21 M$ | 2024-11-09 | -99,54 % | commune | mort |
| `kira-3` | KIRA | KIRA | ≈ 21 M$ | 2024-11-19 | -99,92 % | commune | mort |
| `dogwifnohat` | DogWifNoHat | NOHAT | ≈ 21 M$ | 2024-05-13 | -99,80 % | commune | mort |
| `happi-cat` | happi cat | HAPPI | ≈ 20 M$ | 2024-05-07 | -99,95 % | commune | mort |
| `cat-girl` | cat girl | CATGF | ≈ 20 M$ | 2024-10-23 | -99,90 % | commune | mort |
| `meowcat-2` | MeowCat | MEOW | ≈ 20 M$ | 2024-04-11 | -99,92 % | commune | mort |
| `stix` | STIX | STIX | ≈ 20 M$ | 2024-12-16 | -99,88 % | commune | mort |
| `trumpius-maximus` | Trumpius Maximus | TRUMPIUS | ≈ 20 M$ | 2025-01-03 | -99,82 % | commune | mort |
| `bozo-collective` | Bozo Collective | BOZO | ≈ 20 M$ | 2024-03-18 | -99,93 % | commune | mort |
| `moin-2` | meme + coin = | MOIN | ≈ 20 M$ | 2026-09-28 | -99,76 % | commune | mort |
| `jerry-the-turtle-by-matt-furie` | Jerry The Turtle By Matt Furie | JYAI | ≈ 20 M$ | 2025-08-19 | -99,57 % | commune |  |
| `ai-inu` | AI INU | AIINU | ≈ 20 M$ | 2024-06-05 | -99,63 % | commune | nature à vérifier; mort |
| `dodo-2` | DODO | DODO | ≈ 20 M$ | 2024-04-01 | -99,67 % | commune | mort |
| `carlo` | Carlo | CARLO | ≈ 20 M$ | 2024-06-12 | -99,66 % | commune | mort |
| `myra` | Myra | MYRA | ≈ 20 M$ | 2024-01-20 | -99,80 % | commune | mort |
| `flat-earth` | Flat Earth | FLAT | ≈ 20 M$ | 2026-08-01 | -99,92 % | commune | mort |
| `size` | SIZE | SIZE | ≈ 20 M$ | 2024-11-28 | -99,79 % | commune | mort |
| `go-fu-k-yourself` | go fu*k yourself. | GFY | ≈ 20 M$ | 2023-12-03 | -99,75 % | commune | mort |
| `coby` | coby | COBY | ≈ 20 M$ | 2024-11-11 | -99,85 % | commune | mort |
| `cupsey` | CUPSEY [OLD] | CUPSEY | ≈ 20 M$ | 2024-11-15 | -99,77 % | commune | mort |
| `tongue-cat` | Tongue Cat | LUIS | ≈ 20 M$ | 2024-04-07 | -99,93 % | commune | mort |
| `strategic-oil-supply` | Strategic Oil Supply | SOS | ≈ 20 M$ | 2026-03-10 | -99,85 % | commune | mort |
| `kekius-maximus-2` | Kekius Maximus | KM | ≈ 20 M$ | 2024-12-31 | -99,78 % | commune | copie ou ancienne version d'une carte; mort |
| `bnb-card` | BNB Card | BNBCARD | ≈ 20 M$ | 2025-03-21 | -99,83 % | commune | mort |
| `fungi` | Fungi | FUNGI | ≈ 20 M$ | 2024-04-05 | -99,73 % | commune | mort |
| `mechafolio` | MECHAFOLIO | FOLIO | ≈ 20 M$ | 2026-10-17 | -99,99 % | commune | mort |
| `commander-vrax-4` | Commander Vrax | VRAX | ≈ 20 M$ | 2026-10-16 | -99,99 % | commune | copie ou ancienne version d'une carte; mort |
| `pepedex` | Pepedex | PPDEX | ≈ 20 M$ | 2021-03-06 | -99,96 % | commune | mort |
| `reverse-unit-bias` | Reverse Unit Bias | RUB | ≈ 20 M$ | 2025-09-15 | -99,90 % | commune | mort |
| `poncho` | Poncho | PONCHO | ≈ 20 M$ | 2024-03-26 | -99,81 % | commune | mort |
| `bitcoin-inu` | Bitcoin Inu | BTCINU | ≈ 20 M$ | 2024-01-26 | -99,82 % | commune | mort |
| `baby-cali` | Baby Cali | BABYCALI | ≈ 20 M$ | 2026-09-28 | -99,99 % | commune | mort |
| `akio` | Akio | AKIO | ≈ 20 M$ | 2025-04-21 | -99,89 % | commune | mort |
| `based-turbo` | Based Turbo | TURBO | ≈ 20 M$ | 2024-12-22 | -99,71 % | commune | mort |
| `percy-verence` | Percy Verence | PERCY | ≈ 20 M$ | 2025-01-07 | -99,85 % | commune | mort |
| `bitfloki` | bitFloki | BFLOKI | ≈ 20 M$ | 2024-04-11 | -99,95 % | commune | mort |
| `flying-ketamine-horse` | Flying Ketamine Horse | FKH | ≈ 19 M$ | 2025-12-31 | -99,87 % | commune | mort |
| `aurora-terminal` | Aurora | AURORA | ≈ 19 M$ | 2024-11-18 | -99,94 % | commune | mort |
| `solana-shib` | Solana Shib  | SSHIB | ≈ 19 M$ | 2023-12-25 | -99,63 % | commune | mort |
| `pillzumi` | Pillzumi | PILLZUMI | ≈ 19 M$ | 2024-12-16 | -99,94 % | commune | mort |
| `cat-wif-sword-3` | cat wif sword | SWORDCAT | ≈ 19 M$ | 2026-10-09 | -99,99 % | commune | copie ou ancienne version d'une carte; mort |
| `kaka` | KAKA | KAKA | ≈ 19 M$ | 2025-05-25 | -99,94 % | commune | mort |
| `print-protocol` | Print Protocol | PRINT | ≈ 19 M$ | 2024-01-31 | -99,94 % | commune | nature à vérifier; mort |
| `dogpad-finance` | DogPad Finance | DOGPAD | ≈ 19 M$ | 2023-03-04 | -99,75 % | commune | nature à vérifier; mort |
| `believe-in-something` | Believe In Something | BIS | ≈ 19 M$ | 2024-10-14 | -99,62 % | commune | mort |
| `lanlan-cat` | LanLan Cat | LANLAN | ≈ 19 M$ | 2025-05-27 | -99,87 % | commune | mort |
| `you-looked` | You Looked | CIRCLE | ≈ 19 M$ | 2024-03-07 | -99,84 % | commune | mort |
| `jackpot-on-solana` | Jackpot on Solana | JACKPOT | ≈ 19 M$ | 2024-07-21 | -99,98 % | commune | mort |
| `apewifhat` | ApeWifHat | APEWIFHAT | ≈ 19 M$ | 2024-03-15 | -99,78 % | commune | mort |
| `yeeti` | YEETI 液体 | YEETI | ≈ 19 M$ | 2024-12-14 | -99,59 % | commune | mort |
| `ponk` | Ponk | PONK | ≈ 19 M$ | 2023-12-17 | -99,90 % | commune | mort |
| `eggdog` | Eggdog | EGG | ≈ 19 M$ | 2023-12-26 | -99,81 % | commune | mort |
| `smol-bun` | Smol Bun | BUN | ≈ 19 M$ | 2026-09-09 | -99,96 % | commune | mort |
| `poopcoin-poop` | Poopcoin | POOP | ≈ 19 M$ | 2024-03-31 | -99,59 % | commune | mort |
| `degenerator-project` | Degenerator Project | GNRT | ≈ 19 M$ | 2025-01-08 | -99,97 % | commune | mort |
| `ada-peepos` | FREN | FREN | ≈ 19 M$ | 2023-12-26 | -99,60 % | commune | mort |
| `urmom-2` | urmom | URMOM | ≈ 19 M$ | 2025-05-07 | -99,76 % | commune | mort |
| `my-dog-is-the-dev` | MY DOG IS THE DEV | DEV | ≈ 19 M$ | 2024-09-13 | -99,95 % | commune | mort |
| `dividend-hound` | Dividend Hound | HOUND | ≈ 19 M$ | 2026-10-13 | -99,99 % | commune | mort |
| `pedro-the-raccoon` | Pedro the Raccoon | PEDRO | ≈ 19 M$ | 2024-05-07 | -99,91 % | commune | mort |
| `goblincoin` | GoblinCoin | GOBLIN | ≈ 19 M$ | 2026-05-11 | -99,73 % | commune | mort |
| `noodle` | Noodle | NOODLE | ≈ 19 M$ | 2025-05-13 | -99,90 % | commune | mort |
| `aicrostrategy` | AicroStrategy [Old] | AISTR | ≈ 19 M$ | 2024-12-30 | -99,98 % | commune | mort |
| `asteroid` | ASTEROID | ASTEROID | ≈ 19 M$ | 2026-05-13 | -99,80 % | commune | mort |
| `chuan-pu` | Chuan Pu | CHUANPU | ≈ 19 M$ | 2024-06-20 | -99,93 % | commune | mort |
| `valentine-grok-companion` | Valentine Grok Companion | VALENTINE | ≈ 18 M$ | 2025-07-17 | -99,94 % | commune | mort |
| `buy-the-hat` | BUY THE HAT | BTH | ≈ 18 M$ | 2025-08-09 | -99,70 % | commune | mort |
| `memes-will-continue` | memes will continue | MEMES | ≈ 18 M$ | 2026-01-25 | -99,68 % | commune | mort |
| `soylanamanletcaptainz` | SoylanaManletCaptainZ | ANSEM | ≈ 18 M$ | 2024-03-31 | -99,86 % | commune | mort |
| `yotoshi` | Yotoshi | YOTO | ≈ 18 M$ | 2023-12-25 | -99,87 % | commune | mort |
| `the-theory-of-gravity` | Theory Of Gravity | THOG | ≈ 18 M$ | 2024-04-08 | -99,82 % | commune | mort |
| `doodipals` | DOODiPALS | DOODI | ≈ 18 M$ | 2025-10-02 | -99,84 % | commune | mort |
| `nothing-4` | Nothing | VOID | ≈ 18 M$ | 2024-12-04 | -99,83 % | commune | mort |
| `boblles` | Boblles | BOBLS | ≈ 18 M$ | 2024-12-03 | -99,92 % | commune | mort |
| `trump-47` | TRUMP 47 | 47 | ≈ 18 M$ | 2024-10-29 | -99,56 % | commune | mort |
| `yeti-2` | YETI | YETI | ≈ 18 M$ | 2025-06-30 | -99,92 % | commune | mort |
| `dogei` | Dogei | DOGEI | ≈ 18 M$ | 2024-12-03 | -99,93 % | commune | mort |
| `tobi` | tobi | TOBI | ≈ 18 M$ | 2024-11-13 | -99,87 % | commune | mort |
| `bucky` | Bucky | BUCKY | ≈ 18 M$ | 2024-06-29 | -99,97 % | commune | mort |
| `rudi` | rudi | RUDI | ≈ 18 M$ | 2025-07-16 | -99,89 % | commune | mort |
| `bird-dog-on-sol` | Bird Dog on SOL | BIRDDOG | ≈ 18 M$ | 2024-06-21 | -99,76 % | commune | mort |
| `kai-ken` | Kai Ken | KAI | ≈ 18 M$ | 2024-06-21 | -99,54 % | commune | mort |
| `chinese-doge-wow` | Chinese Doge Wow | CHIDO | ≈ 18 M$ | 2024-12-04 | -99,55 % | commune | mort |
| `super-model` | Super Model | SM | ≈ 18 M$ | 2026-10-05 | -99,99 % | commune | mort |
| `children-of-the-sky` | Children Of The Sky | COTS | ≈ 18 M$ | 2025-07-21 | -99,96 % | commune | mort |
| `new-baby-elephant-houston-zoo` | New Baby Elephant Houston Zoo | KIRBY | ≈ 18 M$ | 2024-11-19 | -99,95 % | commune | mort |
| `naval-ai` | Patchwork Naval | NAVAL | ≈ 18 M$ | 2024-11-16 | -99,94 % | commune | mort |
| `puppers` | PUPPERS | PUPPERS | ≈ 18 M$ | 2026-08-21 | -99,93 % | commune | mort |
| `toescoin` | TOESCOIN | TOES | ≈ 18 M$ | 2026-06-20 | -99,75 % | commune | mort |
| `guanciale` | Guanciale by Virtuals | GUAN | ≈ 18 M$ | 2025-01-04 | -99,88 % | commune | mort |
| `spike-4` | SPIKE | SPIKE | ≈ 18 M$ | 2026-04-26 | -99,86 % | commune | mort |
| `liquid-solana-derivative` | Liquid Solana Derivative | LSD | ≈ 18 M$ | 2024-10-08 | -99,79 % | commune | mort |
| `loafcat` | LOAFCAT | LOAFCAT | ≈ 17 M$ | 2024-11-23 | -99,52 % | commune | mort |
| `make-no-mistakes-2` | Make No Mistakes | MISTAKE | ≈ 17 M$ | 2026-10-04 | -99,97 % | commune | mort |
| `stash-inu` | Stash Inu | STASH | ≈ 17 M$ | 2024-04-10 | -99,67 % | commune | mort |
| `bee` | Bee | BEE | ≈ 17 M$ | 2024-10-01 | -99,95 % | commune | mort |
| `boysclubbase` | Boysclubbase | $BOYS | ≈ 17 M$ | 2024-06-04 | -99,97 % | commune | mort |
| `charles-2` | Charles | KING | ≈ 17 M$ | 2025-05-25 | -99,89 % | commune | mort |
| `prick` | Prick | PRICK | ≈ 17 M$ | 2024-06-11 | -99,90 % | commune | mort |
| `chinese-oil-asset-reserve` | Chinese Oil Asset Reserve | COAR | ≈ 17 M$ | 2026-05-19 | -99,95 % | commune | mort |
| `tinhatcat` | TinHatCat | THC | ≈ 17 M$ | 2024-10-15 | -99,70 % | commune | mort |
| `goatcoin-2` | Goatcoin | GOAT | ≈ 17 M$ | 2025-08-27 | -99,78 % | commune | mort |
| `landlord-roland` | Landlord Ronald | $LANDLORD | ≈ 17 M$ | 2024-07-06 | -99,79 % | commune | mort |
| `calicoin-2` | Calicoin | CALICO | ≈ 17 M$ | 2025-02-05 | -99,88 % | commune | mort |
| `anime-token` | Anime | ANI | ≈ 17 M$ | 2021-03-11 | -99,94 % | commune | mort |
| `dogecast-2` | dogecast | DOGECAST | ≈ 17 M$ | 2025-01-19 | -99,89 % | commune | mort |
| `autism-2` | autism | AUTISM | ≈ 17 M$ | 2024-10-22 | -99,74 % | commune | mort |
| `normilio` | Normilio | NORMILIO | ≈ 17 M$ | 2024-04-17 | -99,80 % | commune | mort |
| `leia` | Leia | LEIA | ≈ 17 M$ | 2024-03-15 | -99,95 % | commune | mort |
| `aigov` | AIGOV | OLIVIA | ≈ 17 M$ | 2025-05-29 | -99,96 % | commune | mort |
| `autist` | Autist | AUTIST | ≈ 17 M$ | 2024-12-08 | -99,75 % | commune | mort |
| `achi` | achi | ACHI | ≈ 17 M$ | 2024-05-25 | -99,80 % | commune | mort |
| `minidoge-4` | MiniDoge | MINIDOGE | ≈ 16 M$ | 2025-03-07 | -99,91 % | commune | mort |
| `pepeinatux` | Pepeinatux | $INA | ≈ 16 M$ | 2025-01-22 | -99,69 % | commune | mort |
| `breaking` | Breaking | BREAKING | ≈ 16 M$ | 2026-08-27 | -99,98 % | commune | mort |
| `solgoat` | SolGoat | SOLGOAT | ≈ 16 M$ | 2024-03-26 | -99,92 % | commune | mort |
| `andy-3` | Andy | ANDY | ≈ 16 M$ | 2024-07-18 | -99,86 % | commune | copie ou ancienne version d'une carte; mort |
| `zen-2` | ZEN | ZEN | ≈ 16 M$ | 2026-04-01 | -99,92 % | commune | mort |
| `dogeball` | DOGEBALL | DOGEBALL | ≈ 16 M$ | 2026-10-13 | -99,98 % | commune | mort |
| `groggo-by-matt-furie` | Groggo By Matt Furie | GROGGO | ≈ 16 M$ | 2024-11-08 | -99,76 % | commune | mort |
| `brat` | Brat | BRAT | ≈ 16 M$ | 2025-02-16 | -99,93 % | commune | mort |
| `horny` | $horny | $HORNY | ≈ 16 M$ | 2024-12-11 | -99,76 % | commune | mort |
| `janet` | Janet | JANET | ≈ 16 M$ | 2024-10-22 | -99,82 % | commune | mort |
| `jobiess` | JobIess | JOBIESS | ≈ 16 M$ | 2025-09-18 | -99,76 % | commune | mort |
| `fuku-2` | Fuku | FUKU | ≈ 16 M$ | 2025-01-05 | -99,97 % | commune | mort |
| `weirdo-2` | Weirdo | WEIRDO | ≈ 16 M$ | 2024-05-23 | -99,64 % | commune | mort |
| `dork-lord-coin` | DORK LORD COIN | DLORD | ≈ 16 M$ | 2024-05-01 | -99,95 % | commune | mort |
| `dream-2` | DREAM | DREAM | ≈ 16 M$ | 2024-11-28 | -99,93 % | commune | mort |
| `america-pac` | America Pac | PAC | ≈ 16 M$ | 2024-10-08 | -99,68 % | commune | mort |
| `apes-go-bananas` | Apes Go Bananas | AGB | ≈ 16 M$ | 2023-05-29 | -99,79 % | commune | mort |
| `smiling-dolphin` | Smiling Dolphin | MIHARU | ≈ 16 M$ | 2024-10-11 | -99,68 % | commune | mort |
| `memecoin-3` | Memecoin | MEMECOIN | ≈ 16 M$ | 2026-04-29 | -99,78 % | commune | copie ou ancienne version d'une carte; mort |
| `darkpino` | DarkPino | DPINO | ≈ 16 M$ | 2025-08-30 | -99,75 % | commune | mort |
| `this-will-make-ur-monthly-salary` | This will make ur monthly salary | SALARY | ≈ 16 M$ | 2025-08-07 | -99,89 % | commune | mort |
| `cope-3` | Cope | COPE | ≈ 16 M$ | 2025-08-29 | -99,56 % | commune | mort |
| `x-community` | X Community | X | ≈ 16 M$ | 2025-01-17 | -99,75 % | commune | mort |
| `sentai-2` | SENTAI | SENTAI | ≈ 16 M$ | 2025-01-11 | -99,96 % | commune | mort |
| `vida-global-cto` | Vida Global CTO | CTO | ≈ 16 M$ | 2026-09-08 | -99,92 % | commune | mort |
| `let-him-cook` | Let Him Cook | $COOK | ≈ 16 M$ | 2024-11-19 | -99,66 % | commune | mort |
| `russian-oil-asset-fund` | Russian Oil Asset Fund | ROAF | ≈ 16 M$ | 2026-05-09 | -99,92 % | commune | mort |
| `pou` | Pou | POU | ≈ 16 M$ | 2024-03-15 | -99,92 % | commune | mort |
| `blackrack` | BlackRack | RACKS | ≈ 16 M$ | 2025-01-07 | -99,96 % | commune | mort |
| `holy-coin` | Holy Coin | HOLY | ≈ 16 M$ | 2025-09-29 | -99,90 % | commune | mort |
| `good-gensler` | Good Gensler | GENSLR | ≈ 16 M$ | 2023-05-06 | -99,65 % | commune | mort |
| `wally` | Wally | WALLY | ≈ 15 M$ | 2024-11-13 | -99,91 % | commune | mort |
| `schrodinger` | Schrodinger | MEOW | ≈ 15 M$ | 2021-12-08 | -99,73 % | commune | mort |
| `daumenfrosch` | Daumenfrosch | DAUMEN | ≈ 15 M$ | 2024-03-09 | -99,60 % | commune | mort |
| `dark-cheems` | Dark Cheems | TOTAKEKE | ≈ 15 M$ | 2025-07-26 | -99,75 % | commune | mort |
| `gib-3` | gib | GIB | ≈ 15 M$ | 2025-05-25 | -99,83 % | commune | mort |
| `fuku-kun` | Fuku-Kun | FUKU | ≈ 15 M$ | 2024-08-09 | -99,70 % | commune | mort |
| `keydog` | KEYDOG | $KEYDOG | ≈ 15 M$ | 2024-11-01 | -99,86 % | commune | mort |
| `sugar-bush` | SUGAR BUSH | SUGR | ≈ 15 M$ | 2024-11-25 | -99,83 % | commune | mort |
| `ruri-truth-terminal-s-crush` | Ruri - Truth Terminal's Crush | RURI | ≈ 15 M$ | 2024-11-30 | -99,93 % | commune | mort |
| `styro-steve` | Styro Steve | SS | ≈ 15 M$ | 2024-12-29 | -99,92 % | commune | mort |
| `valor-2` | VALOR | VALOR | ≈ 15 M$ | 2025-10-31 | -99,84 % | commune | mort |
| `one-unchill-gal` | one unchill gal | GAL | ≈ 15 M$ | 2024-11-26 | -99,87 % | commune | mort |
| `valentine-grok-companion-3` | Valentine Grok Companion | VALENTINE | ≈ 15 M$ | 2025-07-19 | -99,78 % | commune | mort |
| `pepo` | PEPO | PEPO | ≈ 15 M$ | 2025-02-01 | -99,63 % | commune | mort |
| `goatseus-maximus-on-eth` | Goatseus Maximus | GOAT | ≈ 15 M$ | 2024-10-24 | -99,73 % | commune | copie ou ancienne version d'une carte; mort |
| `reflections-of-dissonance-ai` | Reflections of Dissonance AI | AIKA | ≈ 15 M$ | 2024-11-18 | -99,92 % | commune | nature à vérifier; mort |
| `doogle` | Doogle | DOOGLE | ≈ 15 M$ | 2024-07-08 | -99,90 % | commune | mort |
| `kekistan` | Kekistan | KEK | ≈ 15 M$ | 2025-01-01 | -99,53 % | commune | mort |
| `actual` | ACTUAL | ACTUAL | ≈ 15 M$ | 2025-01-21 | -99,96 % | commune | mort |
| `mona-arcane` | Mona Arcane | MONA | ≈ 15 M$ | 2024-11-27 | -99,90 % | commune | mort |
| `official-crypto-nostra` | Official Crypto Nostra | OCN | ≈ 15 M$ | 2025-06-06 | -99,79 % | commune | mort |
| `fartcat` | Fartcat | FARTCAT | ≈ 15 M$ | 2025-06-15 | -99,66 % | commune | mort |
| `onigiri-2` | Onigiri | ONI | ≈ 15 M$ | 2024-08-06 | -99,67 % | commune | mort |
| `beth` | Beth | $BETH | ≈ 15 M$ | 2024-12-25 | -99,94 % | commune | mort |
| `ghibli-kapibala` | Ghibli Kapibala | KAPIBALA | ≈ 15 M$ | 2025-04-20 | -99,96 % | commune | mort |
| `doge-jones-industrial-average` | Doge Jones Industrial Average | DJI | ≈ 15 M$ | 2024-11-22 | -99,88 % | commune | mort |
| `csi888` | CSI888 | CSI | ≈ 15 M$ | 2024-10-08 | -99,82 % | commune | mort |
| `suiboxer` | SUIBoxer | SBOX | ≈ 15 M$ | 2025-05-23 | -99,92 % | commune | mort |
| `inferno-2` | INFERNO | INF | ≈ 15 M$ | 2025-01-23 | -99,79 % | commune | mort |
| `lingyan` | Lingyan | LINGYAN | ≈ 15 M$ | 2024-11-14 | -99,93 % | commune | mort |
| `law-of-attraction` | Law of Attraction | LOA | ≈ 15 M$ | 2024-05-23 | -99,84 % | commune | mort |
| `degen-capital-by-virtuals` | Degen Capital by Virtuals | DEGENC | ≈ 15 M$ | 2024-12-31 | -99,89 % | commune | mort |
| `the-blinking-ai-cat-catfather` | The Blinking AI Cat - Catfather | CATF | ≈ 15 M$ | 2025-01-04 | -99,94 % | commune | nature à vérifier; mort |
| `gugo` | Gugo | GUGO | ≈ 15 M$ | 2025-08-13 | -99,97 % | commune | mort |
| `land-wu` | Land Wu | LANDWU | ≈ 15 M$ | 2024-06-13 | -99,78 % | commune | mort |
| `nyx-by-virtuals` | Nyx by Virtuals | NYX | ≈ 14 M$ | 2025-02-13 | -99,94 % | commune | mort |
| `duckyduck` | DuckyDuck | DUCKY | ≈ 14 M$ | 2024-07-30 | -99,92 % | commune | mort |
| `libra-4` | Libra | LIBRA | ≈ 14 M$ | 2025-02-17 | -99,57 % | commune | copie ou ancienne version d'une carte; mort |
| `vulgar-penguin` | 三维威廉泰尔企鹅 (Vulgar Penguin) | 恶俗企鹅 | ≈ 14 M$ | 2025-12-02 | -99,59 % | commune |  |
| `dog-shit-going-nowhere` | Dog shit going nowhere | DOGSHIT2 | ≈ 14 M$ | 2025-02-05 | -99,62 % | commune | mort |
| `the-anthropic-order` | The Anthropic Order | TAO | ≈ 14 M$ | 2024-12-04 | -99,93 % | commune | mort |
| `fluffington` | Fluffington | FLUFFI | ≈ 14 M$ | 2024-08-16 | -99,80 % | commune | mort |
| `sumi` | SUMI | SUMI | ≈ 14 M$ | 2024-11-17 | -99,95 % | commune | mort |
| `babysol` | BabySOL | BABYSOL | ≈ 14 M$ | 2024-03-17 | -99,90 % | commune | mort |
| `mind-zero` | Mind Zero | MIND | ≈ 14 M$ | 2024-11-29 | -99,95 % | commune | mort |
| `zoo-world` | Zoo World | ZOO | ≈ 14 M$ | 2025-01-28 | -99,98 % | commune | mort |
| `santa-hat` | SANTA HAT | SANTAHAT | ≈ 14 M$ | 2024-11-30 | -99,82 % | commune | mort |
| `dog-emoji-on-solana` | Dog Emoji On Solana | 🐕 | ≈ 14 M$ | 2024-10-13 | -99,71 % | commune | mort |
| `suicy-the-seal` | Suicy the Seal | SUICY | ≈ 14 M$ | 2024-12-14 | -99,93 % | commune | mort |
| `crashout` | Crashout | CRASHOUT | ≈ 14 M$ | 2024-11-28 | -99,79 % | commune | mort |
| `binance-yellow-robot` | Binance Yellow Robot | BINA | ≈ 14 M$ | 2025-10-08 | -99,86 % | commune | mort |
| `shitcoin-2` | Shitcoin | SHIT | ≈ 14 M$ | 2024-09-24 | -99,80 % | commune | mort |
| `flappy` | Flappy | FLAPPY | ≈ 14 M$ | 2024-07-12 | -99,72 % | commune | mort |
| `ratomilton` | ratomilton | MILTON | ≈ 14 M$ | 2025-01-29 | -99,91 % | commune | mort |
| `zenith-protocol` | Zenith Protocol | ZTH | ≈ 14 M$ | 2026-09-09 | -99,82 % | commune | nature à vérifier; mort |
| `moomoo-the-bull` | MOOMOO THE BULL | MOOMOO | ≈ 14 M$ | 2025-07-11 | -99,96 % | commune | mort |
| `iiii-lovvv-youuuu` | iiii lovvvv youuuu | ILY | ≈ 14 M$ | 2024-11-21 | -99,58 % | commune | mort |
| `arbuz` | ARBUZ | ARBUZ | ≈ 14 M$ | 2024-03-23 | -99,52 % | commune | mort |
| `dawg-coin` | Dawg Coin | DAWG | ≈ 14 M$ | 2023-12-04 | -99,84 % | commune | mort |
| `mochicat` | MOCHICAT | MOCHICAT | ≈ 14 M$ | 2024-04-02 | -99,95 % | commune | mort |
| `moonbag` | MoonBag | MBAG | ≈ 14 M$ | 2024-10-15 | -99,62 % | commune | mort |
| `chatgpt-s-mascot` | ChatGPT's Mascot | CHATTY | ≈ 14 M$ | 2024-11-18 | -99,58 % | commune | mort |
| `powsche` | POWSCHE | POWSCHE | ≈ 14 M$ | 2024-12-04 | -99,57 % | commune | mort |
| `snibbu-the-crab` | Snibbu the Crab | SNIBBU | ≈ 14 M$ | 2024-07-30 | -99,97 % | commune | mort |
| `lizard-2` | Lizard | LIZARD | ≈ 13 M$ | 2025-08-06 | -99,69 % | commune | mort |
| `britt` | Britt | BRITT | ≈ 13 M$ | 2024-04-22 | -99,84 % | commune | mort |
| `babypepe` | BabyPepe | BABYPEPE | ≈ 13 M$ | 2023-05-05 | -99,71 % | commune | mort |
| `next-gen-pepe` | Next Gen PEPE | PEPE | ≈ 13 M$ | 2024-06-12 | -99,94 % | commune | mort |
| `canwifhat` | Canwifhat | CAN | ≈ 13 M$ | 2024-03-25 | -99,93 % | commune | mort |
| `sui-trump` | SUITRUMP | SUITRUMP | ≈ 13 M$ | 2025-05-23 | -99,53 % | commune | mort |
| `based-usa` | Based USA | USA | ≈ 13 M$ | 2024-05-22 | -99,74 % | commune | mort |
| `john-the-coin` | John the Coin | JOHN | ≈ 13 M$ | 2024-10-14 | -99,79 % | commune | mort |
| `helloworld` | HELLOWORLD | HELLOWORLD | ≈ 13 M$ | 2025-06-04 | -99,58 % | commune | mort |
| `spike-on-eth` | Spike | SPIKE | ≈ 13 M$ | 2024-07-08 | -99,51 % | commune | mort |
| `golden-celestial-ratio` | Golden Celestial Ratio | GCR | ≈ 13 M$ | 2024-10-18 | -99,62 % | commune | mort |
| `repost-dog` | Repost Dog | RDOG | ≈ 13 M$ | 2024-09-30 | -99,92 % | commune | mort |
| `deer-seized-by-us-government` | Deer Seized by US Government | BABY | ≈ 13 M$ | 2025-03-02 | -99,87 % | commune | mort |
| `matt-furie-s-boys-club` | Matt Furie's Boys Club | BOYSCLUB | ≈ 13 M$ | 2024-06-12 | -99,68 % | commune | mort |
| `pi-network-dog` | Pi Network Dog | PIDOG | ≈ 13 M$ | 2025-02-18 | -99,56 % | commune | nature à vérifier; mort |
| `commander-vrax` | Commander Vrax | VRAX | ≈ 13 M$ | 2026-09-30 | -99,98 % | commune | copie ou ancienne version d'une carte; mort |
| `doge-mascot-shibu` | Shibu | SHIBU | ≈ 13 M$ | 2024-10-30 | -99,70 % | commune | mort |
| `dividend-dog-head` | 分红狗头 (Dividend Dog Head) | 分红狗头 | ≈ 13 M$ | 2026-01-30 | -99,91 % | commune | mort |
| `nibbles` | Nibbles | NIBBLES | ≈ 13 M$ | 2025-01-30 | -99,95 % | commune | mort |
| `moon-inu` | MOON INU | MOON | ≈ 13 M$ | 2024-03-31 | -99,86 % | commune | mort |
| `djcat` | DJCAT | DJCAT | ≈ 13 M$ | 2024-05-19 | -99,84 % | commune | mort |
| `cat-wif-sword` | cat wif sword | SWORDCAT | ≈ 13 M$ | 2026-09-29 | -99,95 % | commune | copie ou ancienne version d'une carte; mort |
| `don-t-burn-capital` | Don't Burn Capital | DBC | ≈ 13 M$ | 2025-07-05 | -99,62 % | commune | mort |
| `z-3` | Z | Z | ≈ 13 M$ | 2026-08-19 | -99,84 % | commune | mort |
| `just-need-some-rest` | Just need some rest | REST | ≈ 13 M$ | 2025-09-03 | -99,98 % | commune | mort |
| `i-dont-know` | i dont know | IDK | ≈ 13 M$ | 2024-03-20 | -99,76 % | commune | mort |
| `darksun` | darksun | BINARY | ≈ 13 M$ | 2024-12-08 | -99,91 % | commune | mort |
| `chill-family` | Chill Family | CHILLFAM | ≈ 13 M$ | 2024-11-22 | -99,88 % | commune | mort |
| `magnet-2` | Magnet | MAGNET | ≈ 13 M$ | 2024-10-12 | -99,77 % | commune | mort |
| `half-orange-drinking-lemonade` | Half Orange Drinking Lemonade | HODL | ≈ 13 M$ | 2024-10-15 | -99,92 % | commune | mort |
| `fleabone` | FLEABONE | BONE | ≈ 13 M$ | 2024-12-13 | -99,83 % | commune | mort |
| `baba` | BABA | BABA | ≈ 13 M$ | 2024-03-18 | -99,90 % | commune | mort |
| `antitoken` | Antitoken | ANTI | ≈ 13 M$ | 2025-05-02 | -99,88 % | commune | mort |
| `cheepepe` | cheepepe | CHEEPEPE | ≈ 13 M$ | 2024-05-18 | -99,96 % | commune | mort |
| `imagine-2` | IMAGINE | IMAGINE | ≈ 13 M$ | 2025-08-02 | -99,88 % | commune | mort |
| `bnb-wallstreet-bull` | BNB Wallstreet Bull | WBULL | ≈ 13 M$ | 2025-10-09 | -99,90 % | commune | mort |
| `rainbowfish` | rainbowfish | FISH | ≈ 12 M$ | 2026-01-07 | -99,69 % | commune | mort |
| `trenchai` | TrenchAI | TRENCHAI | ≈ 12 M$ | 2025-01-03 | -99,76 % | commune | mort |
| `strategic-hub-for-innovation-in-blockchain` | Strategic Hub for Innovation in Blockchain | SHIB | ≈ 12 M$ | 2024-11-09 | -99,92 % | commune | nature à vérifier; mort |
| `trackedbio` | TrackedBio | TRACKEDBIO | ≈ 12 M$ | 2024-12-08 | -99,78 % | commune | mort |
| `bubba` | Bubba | BUBBA | ≈ 12 M$ | 2024-06-04 | -99,89 % | commune | mort |
| `meta-doge` | Meta Doge | METADOGE | ≈ 12 M$ | 2021-12-08 | -99,94 % | commune | mort |
| `morti` | Morti | MORTI | ≈ 12 M$ | 2024-10-01 | -99,94 % | commune | mort |
| `kabosu-kabosucoin-erc` | Kabosu | KABOSU | ≈ 12 M$ | 2024-10-17 | -99,79 % | commune | copie ou ancienne version d'une carte; mort |
| `dook` | Dook | DOOK | ≈ 12 M$ | 2024-06-12 | -99,78 % | commune | mort |
| `maga-pepe` | MAGA PEPE | MAGAPEPE | ≈ 12 M$ | 2024-05-27 | -99,77 % | commune | mort |
| `protoken` | Protoken | PRO | ≈ 12 M$ | 2025-05-02 | -99,89 % | commune | mort |
| `paradox-3` | PARADOX | PARADOX | ≈ 12 M$ | 2024-11-16 | -99,84 % | commune | mort |
| `national-trust-fund-system` | National Trust Fund System | NTFS | ≈ 12 M$ | 2026-07-25 | -99,76 % | commune | mort |
| `alpha-3` | Reject Modernity | ALPHA | ≈ 12 M$ | 2024-11-09 | -99,75 % | commune | mort |
| `khaokheowzoo` | khaokheowzoo | KHEOWZOO | ≈ 12 M$ | 2024-12-15 | -99,86 % | commune | mort |
| `shanghai-inu` | Shanghai Inu | SHANG | ≈ 12 M$ | 2023-05-23 | -99,55 % | commune | mort |
| `living-the-dream` | Living the Dream | LTD | ≈ 12 M$ | 2024-08-31 | -99,94 % | commune | mort |
| `brainrot` | brainrot | ROT | ≈ 12 M$ | 2024-11-17 | -99,77 % | commune | mort |
| `baby-trump-bsc` | Baby Trump (BSC) | BABYTRUMP | ≈ 12 M$ | 2024-05-29 | -99,67 % | commune | mort |
| `hantavirus` | Hantavirus | HANTA | ≈ 12 M$ | 2026-05-08 | -99,81 % | commune | mort |
| `lol-5` | LOL | LOL | ≈ 12 M$ | 2026-04-03 | -99,50 % | commune | mort |
| `duckcoin` | DuckCoin | DUCK | ≈ 12 M$ | 2024-05-09 | -99,63 % | commune | mort |
| `mewing-coin` | Mewing Coin | MEWING | ≈ 12 M$ | 2024-05-06 | -99,80 % | commune | mort |
| `beeg-blue-whale` | Beeg Blue Whale | BEEG | ≈ 12 M$ | 2025-05-23 | -99,82 % | commune | mort |
| `quitcoin` | Quitcoin | QC | ≈ 12 M$ | 2025-08-22 | -99,87 % | commune | mort |
| `mindfak-by-matt-furie` | Mindfak By Matt Furie | MINDFAK | ≈ 12 M$ | 2025-08-22 | -99,53 % | commune | mort |
| `bitcoin-second-chance` | Bitcoin Second Chance | BTC | ≈ 12 M$ | 2025-12-30 | -99,73 % | commune | mort |
| `fartless-coin` | FARTLESS COIN | FARTLESS | ≈ 12 M$ | 2025-08-05 | -99,82 % | commune | mort |
| `retardcoin` | retardcoin | RETARD | ≈ 12 M$ | 2025-05-23 | -99,77 % | commune | mort |
| `forky-2` | Forky | FORKY | ≈ 12 M$ | 2025-01-16 | -99,92 % | commune | mort |
| `sol-the-trophy-tomato` | Sol The Trophy Tomato | SOL | ≈ 12 M$ | 2026-01-25 | -99,73 % | commune | mort |
| `kanye` | Kanye | YE | ≈ 12 M$ | 2025-02-02 | -99,64 % | commune | mort |
| `kekius-maximus-4` | Kekius Maximus | KM | ≈ 12 M$ | 2025-01-11 | -99,68 % | commune | copie ou ancienne version d'une carte; mort |
| `infinite-backrooms` | infinite backrooms | IB | ≈ 12 M$ | 2024-10-31 | -99,79 % | commune | mort |
| `albemarle-meme-token` | Albemarle Meme Token | ALBEMARLE | ≈ 12 M$ | 2024-03-13 | -99,90 % | commune | mort |
| `real-smurf-cat-2` | Real Smurf Cat-шайлушай | SMURF | ≈ 12 M$ | 2024-03-09 | -99,94 % | commune | mort |
| `peanut-3` | Peanut | PNUT | ≈ 12 M$ | 2024-11-13 | -99,60 % | commune | mort |
| `fomo-bull-club` | FOMO BULL CLUB | FOMO | ≈ 11 M$ | 2024-04-15 | -99,89 % | commune | mort |
| `toga` | TOGA | TOGA | ≈ 11 M$ | 2024-11-10 | -99,87 % | commune | mort |
| `yachts-coin` | Yachts Coin | YTC | ≈ 11 M$ | 2025-03-26 | -99,95 % | commune | mort |
| `koku-the-shikoku` | Koku The Shikoku | $KOKU | ≈ 11 M$ | 2025-02-15 | -99,93 % | commune | mort |
| `doge-2-0` | Doge 2.0 | DOGE2.0 | ≈ 11 M$ | 2023-07-07 | -99,71 % | commune | mort |
| `save-the-seals-2` | Save The Seals | SEALS | ≈ 11 M$ | 2026-10-14 | -99,95 % | commune | mort |
| `joram-poowel` | JORAM POOWEL | POOWEL | ≈ 11 M$ | 2024-04-29 | -99,96 % | commune | mort |
| `live-on-toilet-until-50m` | Live On Toilet Until 50M | SHITCOIN | ≈ 11 M$ | 2024-11-22 | -99,90 % | commune | mort |
| `terminalius-maximus` | Terminalius Maximus | BARON | ≈ 11 M$ | 2024-11-24 | -99,52 % | commune | mort |
| `pnut-s-dog` | Pnut's Dog | TUCKER | ≈ 11 M$ | 2024-11-19 | -99,91 % | commune | mort |
| `el-gato` | el gato | ELGATO | ≈ 11 M$ | 2024-03-10 | -99,59 % | commune | mort |
| `buttholes` | Buttholes | BHOLE | ≈ 11 M$ | 2025-01-05 | -99,81 % | commune | mort |
| `zenith-3` | Zenith | ZEN | ≈ 11 M$ | 2025-01-06 | -99,84 % | commune | mort |
| `smolano` | SmoLanO | SLO | ≈ 11 M$ | 2024-01-01 | -99,80 % | commune | mort |
| `sendor` | Sendor | SENDOR | ≈ 11 M$ | 2024-11-28 | -99,85 % | commune | mort |
| `muzki` | Muzki | MUZKI | ≈ 11 M$ | 2024-05-17 | -99,90 % | commune | mort |
| `limitless` | LIMITLESS | LIMITLESS | ≈ 11 M$ | 2025-01-15 | -99,90 % | commune | mort |
| `ceiling-cat` | Ceiling Cat | CEICAT | ≈ 11 M$ | 2024-04-02 | -99,92 % | commune | mort |
| `dogcoin-2` | Dogcoin | DCOIN | ≈ 11 M$ | 2025-01-24 | -99,87 % | commune | mort |
| `bomo-on-base` | BOMO on Base | BOMO | ≈ 11 M$ | 2025-08-30 | -99,87 % | commune | mort |
| `karmacoin-2` | Karmacoin | KARMA | ≈ 11 M$ | 2025-09-02 | -99,82 % | commune | mort |
| `bull-5` | Bull | BULL | ≈ 11 M$ | 2026-04-15 | -99,69 % | commune | mort |
| `colon` | Colon | COLON | ≈ 11 M$ | 2024-08-17 | -99,59 % | commune | mort |
| `star-cat` | STAR CAT | SC | ≈ 11 M$ | 2024-06-29 | -99,62 % | commune | mort |
| `chimerica` | CHIMERICA | CHIMERICA | ≈ 11 M$ | 2026-05-16 | -99,97 % | commune | mort |
| `boochie-by-matt-furie` | Boochie by Matt Furie | BOOCHIE | ≈ 11 M$ | 2025-05-22 | -99,62 % | commune | mort |
| `boopa` | Boopa | BOOPA | ≈ 11 M$ | 2025-05-02 | -99,86 % | commune | mort |
| `poppy` | Poppy | POPPY | ≈ 11 M$ | 2025-01-06 | -99,84 % | commune | mort |
| `ethereum-doge` | Ethereum Doge | EDOGE | ≈ 11 M$ | 2024-09-25 | -99,78 % | commune | mort |
| `patton` | Patton | PATTON | ≈ 11 M$ | 2024-05-11 | -99,73 % | commune | mort |
| `terminus-3` | Terminus | TERMINUS | ≈ 11 M$ | 2024-10-15 | -99,52 % | commune | mort |
| `bonk-2-0-sol` | Bonk 2.0 (Sol) | BONK2.0 | ≈ 11 M$ | 2024-03-09 | -99,74 % | commune | mort |
| `lehman-brothers` | Lehman Brothers | LEH | ≈ 11 M$ | 2024-03-22 | -99,93 % | commune | mort |
| `aejo` | Aejo | AEJO | ≈ 11 M$ | 2024-11-29 | -99,84 % | commune | mort |
| `cramer-coin` | Cramer Coin | $CRAMER | ≈ 11 M$ | 2024-03-05 | -99,64 % | commune | mort |
| `pnut-s-sister` | Pnut's Sister | CHLOE | ≈ 10 M$ | 2024-11-13 | -99,95 % | commune | mort |
| `xenomorph` | XENOMORPH | XENO | ≈ 10 M$ | 2024-11-22 | -99,95 % | commune | mort |
| `kitsune` | Kitsune | KIT | ≈ 10 M$ | 2024-03-17 | -99,94 % | commune | mort |
| `synthesizer-dog` | Synthesizer Dog | SYNDOG | ≈ 10 M$ | 2024-12-08 | -99,88 % | commune | mort |
| `action-figure` | Action Figure | FIGURE | ≈ 10 M$ | 2025-04-14 | -99,85 % | commune | mort |
| `hispanic-pepe` | hispanic pepe | CONCHO | ≈ 10 M$ | 2025-01-15 | -99,61 % | commune | mort |
| `peanut-2` | Peanut [OLD] | PEANUT | ≈ 10 M$ | 2024-11-05 | -99,59 % | commune | mort |
| `strawberry-in-bloom` | Strawberry In Bloom | BERRY | ≈ 10 M$ | 2025-05-13 | -99,61 % | commune | mort |
| `moondoge` | MOONDOGE | MOONDOGE | ≈ 10 M$ | 2025-07-13 | -99,81 % | commune | mort |
| `first-reply` | first reply | SIRIUS | ≈ 10 M$ | 2024-10-01 | -99,61 % | commune | mort |
| `breakout-bro-by-virtuals` | Breakout Bro by Virtuals | BOB | ≈ 10 M$ | 2025-01-01 | -99,88 % | commune | mort |
| `self-aware-meme-2` | Self-Aware Meme | SAM | ≈ 10 M$ | 2026-10-06 | -99,94 % | commune | mort |
| `wife-changing-money-2` | Wife Changing Money | WIFE | ≈ 10 M$ | 2025-06-18 | -99,93 % | commune | mort |
| `dogai-wtf` | DOGAI | DOGAI | ≈ 10 M$ | 2024-10-27 | -99,74 % | commune | mort |
| `hachikosolana` | HachikoSolana | HACHI | ≈ 10 M$ | 2024-04-01 | -99,94 % | commune | mort |
| `jiffpom` | Jiffpom | JIFF | ≈ 10 M$ | 2024-11-26 | -99,94 % | commune | mort |
| `fih` | fih | FIH | ≈ 10 M$ | 2026-08-02 | -99,81 % | commune | mort |
| `joeing737` | Joeing737 | JEOING737 | ≈ 10 M$ | 2024-06-05 | -99,87 % | commune | mort |
| `sora-oracle` | Sora Oracle | SORA | ≈ 10 M$ | 2025-10-30 | -99,73 % | commune | mort |
| `wibwob` | WibWob | WIBWOB | ≈ 10 M$ | 2024-11-29 | -99,91 % | commune | mort |
| `basedmilio` | Basedmilio | BASED | ≈ 10 M$ | 2024-07-15 | -99,67 % | commune | mort |
| `zygo-the-frog` | Zygo The Frog | ZYGO | ≈ 10 M$ | 2025-07-25 | -99,95 % | commune | mort |
| `smoking-giraffe` | Smoking Giraffe | GRAF | ≈ 10 M$ | 2024-05-22 | -99,84 % | commune | mort |
