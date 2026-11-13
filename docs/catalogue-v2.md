# Catalogue v2 des cartes Memaster

**Date :** 11/11/2026. Généré par `docs/recherche-v2/consolider.py` : ne pas éditer à la main, relancer le script. Ce document n'est pas un conseil en investissement.

**Total : 1649 cartes** (dont 3 mythiques scellés), plus 101 jetons « À décider » hors total.

## Sources

- `docs/catalogue-final.md` (v1) ; `docs/recherche-v2/r5-audit-catalogue.md` (audit, doublons, candidats C1/C2) ; `docs/data/coingecko-meme-2026-11-11.csv` (état des jetons rapprochés).
- `docs/recherche-v2/r1-2013-2018.md` : 125 nouveaux jetons lus, 16 corrections.
- `docs/recherche-v2/r2-2019-2022.md` : 155 nouveaux jetons lus, 0 corrections.
- `docs/recherche-v2/r3-2023-2026.md` : 185 nouveaux jetons lus, 151 corrections.
- `docs/recherche-v2/r4-autres-chaines.md` : 265 nouveaux jetons lus, 11 corrections.

## Règles appliquées

- **100 % mèmes** : les 66 retraits de l'audit R5 sont appliqués (annexe 6). Aucun retrait pour disponibilité ou liquidité.
- **Doublons** : nom et ticker normalisés (casse, accents, †, [OLD], parenthèses, suffixe inu/coin/token) et chaîne compatible, ou même id CoinGecko ; doublons cités par R5 fusionnés. Pic retenu : sourcé > estimé > inconnu, puis la source la plus récente (v1 < R5 < r1 < r2 < r3 < r4). Une borne basse sourcée (« ≥ ») est remplacée par une estimation plus haute. Annexe 1.
- **Rareté v2** : mythique = 3 jetons scellés ; légendaire = pic sourcé ≥ 1 Md$ ou histoire légendaire signalée ; épique = pic ≥ 100 M$ (un pic ≥ 1 Md$ seulement estimé reste épique) ; rare = 10 à 100 M$ et pas mort ; commune = le reste (morts au pic < 100 M$, petits, inconnus). « Mort » = état commençant par « mort ». Bas de fourchette retenu. Écarts : annexe 2.
- **Pics aberrants** : un pic seulement estimé et ≥ 1 Md$ compte comme inconnu pour la rareté, ou comme son plancher sourcé s'il en a un (annexe 5). **Surclassements manuels** appliqués en dernier (annexe 4).
- **Drapeaux** gardés en colonne, carte gardée. Pour v1 et les candidats C1 (sources sans colonne Drapeau), drapeau déduit du nom par mots-clés (34 cartes, `drapeau_auto` dans le JSON).
- **Burn** : `à définir` partout (financement non décidé).
- **Candidats R5** : C1 ajoutés s'ils ne sont pas déjà venus par v1 ou r1-r4 ; C2 en réserve (annexe 3).
- Colonne Lancement : date de lancement des chercheurs ; pour v1, la « période de gloire » ; pour C1, la date du plus haut (époque approximative). Histoire vide quand aucune source n'en donne.

## Cartes

3 mythiques scellés : nom et visuel remplacés par « ? ».

| N° | Nom | Ticker | Chaîne | Lancement | Pic | Nature du pic | État | Histoire | Rareté | Rareté proposée | Drapeau | Burn | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | ? | ? | ? | ? | ? | ? | ? | ? | mythique | mythique |  | à définir | ? |
| M2 | ? | ? | ? | ? | ? | ? | ? | ? | mythique | mythique |  | à définir | ? |
| M3 | ? | ? | ? | ? | ? | ? | ? | ? | mythique | mythique |  | à définir | ? |
| 1 | Bonk | BONK | Solana | 2022 | ≈ 5,13 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 10 ; correction r3 ; CG `bonk` |
| 2 | dogwifhat † | WIF | Solana | 2023 | ≈ 4,82 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 7 ; correction r3 ; CG `dogwifcoin` |
| 3 | Memecoin † | MEME | Ethereum | 2023 | ≈ 3,6 Md$ le 04/03/2024 (ATH 0,0563 $ × 64,8 Md en circulation, estimé) | estimé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 669 ; correction r3 ; CG `memecoin-2` ; https://www.coingecko.com/en/coins/memecoin-2 |
| 4 | Floki | FLOKI | Ethereum, BNB Chain | 2021 | ≈ 3,32 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin |  | légendaire | légendaire |  | à définir | v1 n° 32 ; CG `floki` ; connaissance générale, à vérifier |
| 5 | Fartcoin | FARTCOIN | Solana | 2024 | ≈ 2,48 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 17 ; correction r3 ; CG `fartcoin` |
| 6 | Brett † | BRETT | Base | 2024 | ≈ 2,32 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 13 ; correction r3 ; CG `based-brett` |
| 7 | Pudgy Penguins | PENGU | Solana | 2024 | ≈ 2,30 Md$ (sourcé) | sourcé | en déclin |  | légendaire | légendaire |  | à définir | v1 n° 12 ; correction r3 ; CG `pudgy-penguins` |
| 8 | Ordinals | ORDI | Bitcoin (BRC-20) | 2023 | ≈ 2,01 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 27 ; CG `ordinals` |
| 9 | SPX6900 | SPX | Ethereum | 2023 † | ≈ 2,00 Md$ (sourcé) | sourcé | en déclin |  | légendaire | légendaire |  | à définir | v1 n° 15 ; correction r3 ; CG `spx6900` |
| 10 | Sats | SATS (1000SATS) | Bitcoin (BRC-20) | 2023 | ≈ 1,94 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 28 ; CG `sats-ordinals` |
| 11 | Peanut the Squirrel | PNUT | Solana | 2024 | ≈ 1,7 à 2,4 Md$, nov. 2024 (estimé : prix record de 1,72 à 2,44 $ déjà cité par la carte × ≈ 1 Md de jetons) (au-dessus de la borne sourcée ≥ 0,6 Md$ (source peu fiable) ; prix record de 1,72 à 2,44 $ selon les sources) | estimé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 42 ; correction r3 ; CG `peanut-the-squirrel` ; connaissance générale, à vérifier |
| 12 | Popcat † | POPCAT | Solana | 2023 | ≈ 1,70 Md$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 16 ; correction r3 ; CG `popcat` |
| 13 | Book of Meme | BOME | Solana | 2024 | ≈ 1,50 Md$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 21 ; correction r3 ; CG `book-of-meme` |
| 14 | Goatseus Maximus | GOAT | Solana | 2024 | ≈ 1,35 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 26 ; correction r3 ; CG `goatseus-maximus` |
| 15 | Neiro † | NEIRO | Ethereum | 2024 | ≈ 1,2 Md$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 695 ; correction r3 ; CG `neiro-3` ; connaissance générale, à vérifier |
| 16 | cat in a dogs world † | MEW | Solana | 2024 | ≈ 1,15 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | légendaire | épique |  | à définir | v1 n° 79 ; correction r3 ; CG `cat-in-a-dogs-world` ; connaissance générale, à vérifier |
| 17 | DOG•GO•TO•THE•MOON | DOG | Bitcoin (Runes) | 2024 | ≈ 1,13 Md$ (sourcé) | sourcé | en déclin |  | légendaire | légendaire |  | à définir | v1 n° 22 ; CG `dog-go-to-the-moon-rune` |
| 18 | Dogelon Mars | ELON | Ethereum | 2021 | ≈ 1,00 Md$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 25 ; CG `dogelon-mars` |
| 19 | EverGrow | EGC | BSC | sept. 2021 | > 1 Md$ (nov. 2021) ; ≈ 1,44 Md$ en FDV (01/11/2021) | sourcé | mort | Fork reflection sur BSC (sept. 2021) qui reversait 8 % des transactions en BUSD ; annoncé au-delà de 1 Md$ et 60 000 détenteurs en novembre 2021, avant une panique liée à une erreur de données CMC et l'effondrement. | légendaire | légendaire |  | à définir | r2 ; https://www.pymnts.com/cryptocurrency/2021/evergrow-tops-60k-holders-and-1b-market-capitalization/ ; https://kalkinemedia.com/news/cryptocurrency/why-is-evergrow-egc-crypto-getting-attention |
| 20 | Turbo | TURBO | Ethereum | 2023 | ≈ 0,99 Md$ le 11/12/2024 (ATH 0,01432 $ × 69 Md, estimé) (au-dessus de la borne sourcée > 70 M$, mai 2023 (pic réel à vérifier)) | estimé | en déclin (-95 % ou pire) |  | légendaire | légendaire |  | à définir | v1 n° 190 ; correction r3 ; CG `turbo` ; https://www.coingecko.com/en/coins/turbo |
| 21 | analoS | ANALOS | Solana | déc. 2023 | ≈ 170 M$ (24 déc. 2023) | estimé | mort | Lancé le 20/12/2023 ; Lookonchain a suivi un portefeuille passé de 12 SOL (~900 $) à 3,47 M$ (×3 800) et un autre de 30 SOL à 5,7 M$ ; il vaut aujourd'hui ~60 k$. | légendaire | légendaire |  | à définir | r3 ; https://coinmarketcap.com/currencies/analos/ ; https://dexscreener.com/solana/7iT1GRYYhEop2nV1dyCwK2MGyLmPHq47WhPGSwiqcUg5 |
| 22 | Degen † | DEGEN | Base | 2024 | ≈ 2,32 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 51 ; correction r3 ; CG `degen-base` |
| 23 | Baby Doge Coin | BABYDOGE | BNB Chain | 2021 | ≈ 1,20 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | légendaire |  | à définir | v1 n° 66 ; CG `baby-doge-coin` |
| 24 | Loaded Lions | LION | à vérifier | août 2025 | ≈ 971 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 23 ; CG `loaded-lions` |
| 25 | Act I : The AI Prophecy † | ACT | Solana | 2024 | ≈ 970 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 530 ; correction r3 ; CG `act-i-the-ai-prophecy` |
| 26 | The Truth (UFO) | UFO | Ethereum | juin 2021 | ≈ 960 M$ (02/12/2021) | sourcé | mort | Jeton « ovni » lancé sur Ethereum en juin 2021, devenu UFO Gaming ; près de 1 Md$ de capitalisation début décembre 2021 selon CMC, puis -99,9 %. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/the-truth/ |
| 27 | Toshi † | TOSHI | Base | 2023 | ≈ 950 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 74 ; correction r3 ; CG `toshi` |
| 28 | ConstitutionDAO | PEOPLE | Ethereum | 2021 | ≈ 937 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 57 ; CG `constitutiondao` |
| 29 | Monacoin † | MONA | Monacoin (blockchain propre) | 2014 | ≈ 928 M$, 06/12/2017 | sourcé | en déclin (3,8 M$ le 06/11/2026, -99,6 %) |  | épique | épique |  | à définir | v1 n° 680 ; correction r1 ; CG `monacoin` ; https://coinmarketcap.com/currencies/monacoin/historical-data/ |
| 30 | My Paqman Coin | MPC | à vérifier | avr. 2025 | ≈ 920 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 30 ; CG `my-paqman-coin` |
| 31 | Pippin † | PIPPIN | Solana | 2024 | ≈ 895 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 31 ; correction r3 ; CG `pippin` |
| 32 | Dogs † | DOGS | TON | 2024 | ≈ 844 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 607 ; CG `dogs-2` |
| 33 | Just a chill guy † | CHILLGUY | Solana | 2024 | ≈ 840 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 650 ; correction r3 ; CG `chill-guy` |
| 34 | GEKKO | GEKKO | à vérifier | mars 2024 | ≈ 822 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 34 ; CG `gekko` |
| 35 | Gigachad † | GIGA | Solana | 2024 | ≈ 820 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 626 ; correction r3 ; CG `gigachad-2` |
| 36 | Big Dog Fink | BINK | à vérifier | nov. 2024 | ≈ 769 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 24 ; CG `big-dog-fink` |
| 37 | BUILDon | B | BNB Chain | 2025 | ≈ 763 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 37 ; correction r3 ; CG `build-on` |
| 38 | PepeCoin | PEPECOIN | à vérifier | avr. 2024 | ≈ 761 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 29 ; CG `pepecoin-2` |
| 39 | would | WOULD | à vérifier | avr. 2025 | ≈ 701 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 47 ; CG `would` |
| 40 | monKEYS | MONKEYS | à vérifier | mars 2025 | ≈ 700 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 683 ; CG `monkeys-2` |
| 41 | Snek † | SNEK | Cardano | 2023 | ≈ 669 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 752 ; CG `snek` |
| 42 | CateCoin † | CATE | BNB Chain | 2021 | ≈ 658 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 574 ; CG `catecoin` |
| 43 | Slerf | SLERF | Solana | 2024 | ≈ 612 M$ (sourcé) | sourcé | en déclin |  | épique | épique |  | à définir | v1 n° 40 ; correction r3 ; CG `slerf-2` |
| 44 | Moo Deng † | MOODENG | Solana | 2024 | ≈ 610 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 684 ; correction r3 ; CG `moo-deng` |
| 45 | Australian Safe Shepherd | ASS | BSC | avr. 2021 | ≈ 600 M$ en FDV (11/05/2021) | estimé | en déclin | Clone SafeMoon « Australian Safe Shepherd » sur BSC (avr. 2021), connu pour son ticker ASS et cité par Cointelegraph parmi les dogcoins de 2021 ; pic le 11/05/2021, aujourd'hui -98,9 %. | épique | épique | obscène | à définir | r2 ; https://cointelegraph.com/magazine/meme-tokens-and-dogcoins-flood-the-market-as-price-wars-heat-up ; https://coinmarketcap.com/currencies/australian-safe-shepherd/ |
| 46 | Rekt | REKT | à vérifier | août 2025 | ≈ 594 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 43 ; CG `rekt-4` |
| 47 | Banana For Scale | BANANAS31 | BNB Chain | 2025 † | ≈ 590 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 549 ; correction r3 ; CG `banana-for-scale-2` |
| 48 | Dora | DORA | BNB Chain | janv. 2026 | ≈ 576 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 314 ; correction r3 ; CG `dora-2` |
| 49 | The Doge NFT / Own The Doge | DOG | Ethereum, Arbitrum, Polygon | 2021 | ≈ 575 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 412 ; CG `the-doge-nft` |
| 50 | Mononoke Inu | Mononoke-Inu | Ethereum | oct. 2021 | ≈ 533 M$ en FDV (29/10/2021) | estimé | mort | Jeton « Inu » à thème anime sur Ethereum, lancé en oct. 2021 ; pic vers le 29/10/2021 ; aujourd'hui -99,96 %. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/mononoke-inu/ |
| 51 | Non-Playable Coin | NPC | à vérifier | 2024 (à vérifier) | ≈ 530 M$ (estimation CoinGecko de l'annexe 3) | estimé | actif |  | épique | épique |  | à définir | v1 n° 697 ; correction r3 ; CG `non-playable-coin` |
| 52 | Binance Life (币安人生) | 币安人生 | BNB Chain | 2025 | ≈ 524 M$ (sourcé) | sourcé | actif |  | épique | épique |  | à définir | v1 n° 48 ; correction r3 ; CG `bianrensheng` |
| 53 | Ryoshis Vision | RYOSHI | Ethereum | août 2021 | ≈ 522 M$ en FDV (09/11/2021) | estimé | mort | Hommage à Ryoshi, fondateur anonyme de SHIB (août 2021) : chaque transaction brûlait des SHIB et en reversait aux stakers de ShibaSwap ; pic le 09/11/2021, puis abandon. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/ryoshis-vision/ |
| 54 | Simon's Cat | CAT | BNB Chain | 2024-2025 | ≈ 511 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 283 ; correction r3 ; CG `simon-s-cat` |
| 55 | Beercoin | BEER | à vérifier | juin 2024 | ≈ 507 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 559 ; CG `beercoin-2` |
| 56 | Test | TST | BNB Chain | 2025 | ≈ 500 M$ (sourcé) | sourcé | en déclin (≈ 11 M$, -97,7 %, encore du volume) |  | épique | épique |  | à définir | v1 n° 50 ; correction r3 ; CG `test-3` ; https://coinmarketcap.com/currencies/test-token-bsc/ |
| 57 | catgirl | CATGIRL | BSC | mai 2021 | ≈ 476 M$ en FDV (02/11/2021) | estimé | mort | Mème « catgirl » d'anime sur BSC (2021), reconverti ensuite en NFT ; pic le 02/11/2021 au sommet de la saison des chiens, aujourd'hui -99,96 %. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/catgirl/ |
| 58 | Onyx Arches | OXA | à vérifier | juin 2026 | ≈ 470 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 103 ; CG `onyx-arches` |
| 59 | Unicorn Fart Dust | UFD | Solana | Printemps 2025 | ≈ 460 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 780 ; correction r3 ; CG `unicorn-fart-dust` |
| 60 | Believe | BELIEVE | à vérifier | mai 2025 | ≈ 457 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 560 ; CG `ben-pasternak` |
| 61 | Coq Inu † | COQ | Avalanche | 2023 | ≈ 447 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 100 ; CG `coq-inu` |
| 62 | Ponke † | PONKE | Solana | 2023 | ≈ 440 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 716 ; correction r3 ; CG `ponke` |
| 63 | Useless Coin | USELESS | Solana | 2025 † | ≈ 435 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | actif |  | épique | épique |  | à définir | v1 n° 78 ; correction r3 ; CG `useless-3` |
| 64 | Bonfire | BONFIRE | BSC | mai 2021 | ≈ 425 M$ en FDV (09/05/2021) | estimé | en déclin | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) sur BSC, lancé en mai 2021 ; pic vers le 09/05/2021 ; aujourd'hui -98,73 %. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/bonfire/ |
| 65 | Myro † | MYRO | Solana | 2023 | ≈ 418 M$ (8 mars 2024 ; capitalisation CMC ≈ 395 M$) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 694 ; correction r3 ; CG `myro` ; https://coinmarketcap.com/currencies/myro/ |
| 66 | Safemars | SAFEMARS | BSC | mars 2021 | ≈ 417 M$ en FDV (11/05/2021) | estimé | mort | Copie la plus connue de SafeMoon (BSC, 13/03/2021), taxe de 4 % reversée et auto-liquidité ; plus haut le 19/04/2021 selon CMC, citée par InvestorPlace parmi les copies de SafeMoon ; aujourd'hui -99,7 %. | épique | épique |  | à définir | r2 ; https://investorplace.com/?p=1942063 ; https://coinmarketcap.com/currencies/safemars/ |
| 67 | PondCoin | PNDC | à vérifier | sept. 2023 | ≈ 415 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 44 ; CG `pond-coin` |
| 68 | Purr | PURR | Hyperliquid | 2024 | ≈ 410 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 723 ; CG `purr-2` |
| 69 | RSIC•GENESIS•RUNE | RSIC | Bitcoin (Runes) | 2024 | ≈ 406 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 89 ; CG `runecoin` |
| 70 | CZ's Dog | BROCCOLI (BROCCOLI714) | BNB Chain | 2025 | ≈ 400 M$ (sourcé) | sourcé | en déclin |  | épique | épique |  | à définir | v1 n° 55 ; correction r3 ; CG `czs-dog` |
| 71 | HarryPotterObamaSonic10Inu | BITCOIN | Ethereum | 2023 | ≈ 400 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 635 ; correction r3 ; CG `harrypotterobamasonic10in` |
| 72 | Mog Coin | MOG | Ethereum | 2023 | ≈ 400 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 56 ; correction r3 ; CG `mog-coin` |
| 73 | Ronaldinho | STAR10 | BNB Chain | 3 mars 2025 | ≈ 397 M$ de FDV (3 mars 2025) ; ≈ 31 M$ en circulation selon CoinGecko | sourcé | mort (capitalisation ≈ 8 k$) | Le jeton officiel de Ronaldinho, avec 35 % de l'offre aux initiés, s'effondre dès le premier jour. | épique | épique | personne réelle | à définir | r3 ; https://coinmarketcap.com/academy/article/ronaldinhos-star10-meme-coin-launches-with-controversy-reaches-dollar397-million-market-cap-before-dropping ; https://www.coingecko.com/en/coins/ronaldinho-coin |
| 74 | PepeFork | PORK | à vérifier | févr. 2024 | ≈ 387 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 52 ; CG `pepefork` |
| 75 | Artificial Inu | AI | à vérifier | sept. 2026 | ≈ 382 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 53 ; CG `artificial-inu-3` |
| 76 | Kekius Maximus | KEKIUS | Ethereum | déc. 2024 - janv. 2025 | ≈ 380 M$ (sourcé) | sourcé | actif |  | épique | épique |  | à définir | v1 n° 58 ; correction r3 ; CG `kekius-maximus-6` |
| 77 | Milady Meme Coin | LADYS | Ethereum | 2023 | ≈ 380 M$ le 13/03/2024 (ATH 4,28e-7 $ × 888 T, estimé) (au-dessus de la borne sourcée ≥ 197 M$ sur la chaîne (photo sans date)) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 95 ; correction r3 ; CG `milady-meme-coin` ; https://www.coingecko.com/en/coins/milady-meme-coin |
| 78 | Comedian † | BAN | Solana | 2024 | ≈ 370 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 584 ; correction r3 ; CG `comedian` |
| 79 | Hoge Finance | HOGE | Ethereum | 2021 | ≈ 367 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 641 ; CG `hoge-finance` |
| 80 | Milady Cult Coin | CULT | à vérifier | déc. 2024 | ≈ 362 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 60 ; CG `milady-cult-coin` |
| 81 | Fwog † | FWOG | Solana | 2024 | ≈ 360 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 621 ; correction r3 ; CG `fwog` |
| 82 | Katana Inu | KATA | à vérifier | déc. 2021 | ≈ 359 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 652 ; CG `katana-inu` |
| 83 | coco | COCO | à vérifier | mai 2026 | ≈ 355 M$ (estimé CG) | estimé | actif |  | épique | épique |  | à définir | v1 n° 61 ; CG `coco-2` |
| 84 | ANDY ETH | ANDY | à vérifier | déc. 2024 | ≈ 352 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 54 ; CG `andy-the-wisguy` |
| 85 | Wen † | WEN | Solana | 2024 | ≈ 352 M$ (27 mars 2024, capitalisation CMC) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 788 ; correction r3 ; CG `wen-4` ; https://coinmarketcap.com/currencies/wen/ |
| 86 | Barsik | BARSIK | Solana | 2024-2025 | ≈ 340 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 552 ; CG `hasbulla-s-cat` |
| 87 | Luckycoin | LKY | à vérifier | nov. 2024 | ≈ 338 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 664 ; CG `luckycoin` |
| 88 | DogeKing | DOGEKING | à vérifier | févr. 2022 | ≈ 333 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 62 ; CG `dogeking` |
| 89 | UNCOMMON•GOODS | UNCOMMONGOODS | à vérifier | juin 2024 | ≈ 333 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 90 ; CG `uncommon-goods` |
| 90 | CrazyBunny | CRAZYBUNNY | à vérifier | mars 2024 | ≈ 332 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 108 ; CG `crazybunny` |
| 91 | Osaka Protocol | OSAK | Avalanche, Ethereum | à vérifier | ≈ 332 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 309 ; correction r3 ; CG `osaka-protocol` |
| 92 | Apu Apustaja | APU | Ethereum | 2024 | ≈ 320 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 540 ; correction r3 ; CG `apu-s-club` |
| 93 | Luce † | LUCE | Solana | 2024 | ≈ 319 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 662 ; CG `offcial-mascot-of-the-holy-year` |
| 94 | Sundog | SUNDOG | Tron | 2024 † | ≈ 316 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 64 ; CG `sundog` |
| 95 | Cash Cat | CASHCAT | Robinhood Chain | sept. 2026 | ≈ 310 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 67 ; CG `cash-cat` |
| 96 | 龙虾 (Lobster) | 龙虾 | à vérifier | sept. 2026 | ≈ 309 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 70 ; CG `lobster-2` |
| 97 | Baby Shark Universe | BSU | à vérifier | sept. 2025 | ≈ 304 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 547 ; CG `baby-shark-universe` |
| 98 | PepeCoin on Solana | PEPE | à vérifier | févr. 2024 | ≈ 297 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 708 ; CG `pepecoin-on-solana` |
| 99 | Puff The Dragon | PUFF | Mantle | à vérifier (sommet le 8 avr. 2024) | ≈ 294 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Puff, dragon mème phare de Mantle (printemps 2024) ; pic le 8 avril 2024. | épique | épique |  | à définir | r4 ; https://www.coingecko.com/en/coins/puff-the-dragon |
| 100 | TDCCP | TDCCP | à vérifier | sept. 2025 | ≈ 282 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 68 ; CG `tdccp` |
| 101 | AMATERASU OMIKAMI | OMIKAMI | à vérifier | juin 2024 | ≈ 274 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 87 ; CG `amaterasu-omikami` |
| 102 | Kuma Inu | KUMA | Ethereum | mai 2021 | ≈ 274 M$ en FDV (12/10/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en mai 2021 ; pic vers le 12/10/2021 ; aujourd'hui -99,80 %. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/kuma-inu/ |
| 103 | Kendu | KENDU | à vérifier | juin 2024 | ≈ 270 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 102 ; CG `kendu-inu` |
| 104 | ClassicDoge | XDOGE | BSC | nov. 2021 | ≈ 269 M$ en FDV (19/11/2021) | estimé | mort | Clone de Dogecoin sur BSC, lancé en nov. 2021 ; pic vers le 19/11/2021 ; aujourd'hui plus coté. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/classicdoge-io/ |
| 105 | BitShiba | SHIBA | BSC | nov. 2021 | ≈ 268 M$ en FDV (13/11/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en nov. 2021 ; pic vers le 13/11/2021 ; aujourd'hui -99,90 %. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/bitshiba-token/ |
| 106 | mfercoin | MFER | Base | 2024 | ≈ 264 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 671 ; CG `mfercoin` |
| 107 | Apollo Inu | APOLLO | Ethereum | janv. 2022 | ≈ 253 M$ en FDV (26/02/2022) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en janv. 2022 ; pic vers le 26/02/2022 ; aujourd'hui plus coté. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/apollo-inu/ |
| 108 | Cheems | CHEEMS | BNB Chain | nov. 2024 | ≈ 250 M$ (sourcé) | sourcé | mort |  | épique | épique |  | à définir | v1 n° 75 ; correction r3 ; CG `cheems` |
| 109 | Jelly-My-Jelly | JELLYJELLY | Solana | 2025 | ≈ 250 M$ (sourcé) | sourcé | en déclin |  | épique | épique |  | à définir | v1 n° 76 ; correction r3 ; CG `jelly-my-jelly` |
| 110 | Landwolf | WOLF | Ethereum | 2024 | ≈ 250 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 77 ; correction r3 ; CG `landwolf-0x67` |
| 111 | Hokkaidu Inu | HOKK | Ethereum | avr. 2021 | ≈ 249 M$ en FDV (13/11/2021) | estimé | mort | Clone SHIB sur Ethereum (avr. 2021) ; pic le 13/11/2021 au sommet de la saison des chiens, puis reconversion en oracle « Telegraph » ; plus coté. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/hokkaido-inu/ |
| 112 | Wiki Cat | WKC | à vérifier | août 2025 | ≈ 248 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 84 ; CG `wiki-cat` |
| 113 | Mumu the Bull † | MUMU | Solana | 2024 | ≈ 245 M$ (29 juil. 2024 ; capitalisation CMC ≈ 209 M$) | sourcé | mort |  | épique | épique |  | à définir | v1 n° 691 ; correction r3 ; CG `mumu-the-bull-4` ; https://coinmarketcap.com/currencies/mumu-ing/ |
| 114 | 4 | 4 / FOUR | BNB Chain | oct. 2025 | ≈ 243 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 80 ; correction r3 ; CG `4-2` |
| 115 | Shrub | SHRUB | à vérifier | nov. 2024 | ≈ 243 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 129 ; CG `shrub` |
| 116 | Mother Iggy | MOTHER | Solana | 2024 | ≈ 240 M$ (sourcé) | sourcé | mort |  | épique | épique |  | à définir | v1 n° 83 ; correction r3 ; CG `mother-iggy` ; https://coinmarketcap.com/academy/article/from-jenner-to-azalea-the-rise-of-celebrity-memecoins |
| 117 | Vine Coin | VINE | Solana | 2025 | ≈ 240 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 86 ; correction r3 ; CG `vine` |
| 118 | SafeBitcoin | SAFEBTC | BSC | mars 2021 | ≈ 232 M$ en FDV (20/04/2021) | estimé | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) sur BSC, lancé en mars 2021 ; pic vers le 20/04/2021 ; aujourd'hui plus coté. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/safebtc/ |
| 119 | Wise Monkey | MONKY | BNB Chain | 2025 | ≈ 232 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 791 ; CG `wise-monkey` |
| 120 | Aura | AURA | Solana | 2024, puis juin 2025 | ≈ 231 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 184 ; correction r3 ; CG `aura-on-sol` |
| 121 | Tutorial | TUT | BNB Chain | 2025 † | ≈ 230 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 778 ; correction r3 ; CG `tutorial` |
| 122 | Zombie Inu | ZINU | Ethereum | oct. 2021 | ≈ 230 M$ en FDV (17/11/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en oct. 2021 ; pic vers le 17/11/2021 ; aujourd'hui plus coté. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/zombie-inu/ |
| 123 | Bellscoin | BELLS | blockchain propre (scrypt) | lancé le 28/11/2013 par Billy Markus, huit jours avant Dogecoin, dont il est l'ancêtre | ≈ 228 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | relancé en déc. 2023. Rareté épique défendable pour l'histoire | épique | épique |  | à définir | v1 n° 125 ; correction r1 ; CG `bellscoin` ; https://hackernoon.com/bellscoin-the-oldest-memecoin-ever-brought-back-from-the-dead |
| 124 | Billy † | BILLY | Solana | 2024 | ≈ 228 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 563 ; CG `billy` |
| 125 | Shiba Predator | QOM | à vérifier | avr. 2022 | ≈ 228 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 741 ; CG `shiba-predator` |
| 126 | DogeGF | DOGEGF | à vérifier | oct. 2021 | ≈ 226 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 602 ; CG `dogegf` |
| 127 | PacMoon | PAC | Blast | à vérifier (sommet le 4 juin 2024) | ≈ 225 M$ (juin 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | PacMoon, Pac-Man de Blast (le L2 de Pacman, fondateur de Blur), lancé avec un airdrop aux utilisateurs de Blast en mars 2024 ; pic en juin 2024, -99,95 %. | épique | épique |  | à définir | r4 ; https://www.coingecko.com/en/coins/pacmoon |
| 128 | DogeBonk | DOBO | à vérifier | nov. 2021 | ≈ 224 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 81 ; CG `dogebonk` |
| 129 | GME (Solana) | GME | Solana | 2024 | ≈ 220 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 134 ; correction r3 ; CG `gme` |
| 130 | Stool Prisondente | JAILSTOOL | Solana | févr. 2025 | ≈ 218 M$ (9 févr. 2025) | sourcé | mort (FDV ≈ 0,89 M$) | Dave Portnoy (Barstool) l'achète, le revend « par erreur », promet de tenir jusqu'à 1 Md$, puis le jeton fond. | épique | épique | personne réelle | à définir | r3 ; https://decrypt.co/305323/dave-portnoy-solana-meme-coin-jailstool ; https://www.coingecko.com/en/coins/stool-prisondente |
| 131 | Luffy Inu | LUFFY | Ethereum | sept. 2021 | ≈ 216 M$ en FDV (13/11/2021) | estimé | mort | Jeton « Inu » à thème One Piece sur Ethereum, lancé en sept. 2021 ; pic vers le 13/11/2021 ; aujourd'hui plus coté. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/luffy-inu/ |
| 132 | Mubarak | MUBARAK | BNB Chain | 2025 | ≈ 216 M$ (18/03/2025, ATH CMC × 1 Md) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 689 ; correction r3 ; CG `mubarak` ; https://coinmarketcap.com/currencies/mubarak/ |
| 133 | Nacho the Kat | NACHO | à vérifier | déc. 2024 | ≈ 216 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 73 ; CG `nacho-the-kat` |
| 134 | Sudeng | HIPPO | Sui | 2024 † | ≈ 216 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 88 ; CG `sudeng` |
| 135 | Stonks | STNK | à vérifier | déc. 2024 | ≈ 215 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 85 ; CG `stonks-4` |
| 136 | Maneki † | MANEKI | Solana | 2024 | ≈ 206 M$ (25 avr. 2024 ; capitalisation CMC ≈ 164 M$) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 667 ; correction r3 ; CG `maneki` ; https://coinmarketcap.com/currencies/maneki-coin/ |
| 137 | McDull (Meme) | MCDULL | à vérifier | janv. 2025 | ≈ 206 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 93 ; CG `mcdull` |
| 138 | Asteroid Shiba | ASTEROID | à vérifier | avr. 2026 | ≈ 202 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 96 ; CG `asteroid-shiba` |
| 139 | BasedHype | BASEDHYPE | à vérifier | oct. 2025 | ≈ 200 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 91 ; correction r3 ; CG `basedhype` |
| 140 | MongCoin | MONG | Ethereum | 26/04/2023 | ≈ 200-250 M$ (05/05/2023) | estimé | mort | Copie de Pepe de la vague d'avril 2023, +7 800 % en trois jours, puis effondrement. | épique | épique |  | à définir | r3 ; https://www.coingecko.com/en/coins/mongcoin ; https://dexscreener.com/ethereum/0x1ce270557C1f68Cfb577b856766310Bf8B47FD9C |
| 141 | MORI COIN | MORI | à vérifier | juil. 2025 | ≈ 200 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 72 ; CG `mori-coin` |
| 142 | Pepe Unchained | PEPU | Ethereum, puis chaîne propre | déc. 2024 | ≈ 200 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 94 ; correction r3 ; CG `pepe-unchained-2` ; https://www.coingecko.com/en/coins/pepe-unchained |
| 143 | Clifford Inu | CLIFF | Ethereum | déc. 2021 | ≈ 198 M$ en FDV (18/12/2021) | estimé | mort | Jeton « Inu » inspiré de Clifford, le gros chien rouge sur Ethereum, lancé en déc. 2021 ; pic vers le 18/12/2021 ; aujourd'hui plus coté. | épique | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/clifford-inu/ |
| 144 | Conscious | CONSCIOUS | BNB Chain | oct. 2025 | ≈ 198 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 585 ; CG `conscious-token` |
| 145 | WhiteWhale | WHITEWHALE | Solana | Début 2026 | ≈ 198 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 151 ; correction r3 ; CG `the-white-whale` |
| 146 | BULLA | BULLA | à vérifier | févr. 2026 | ≈ 195 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 97 ; CG `bulla-3` |
| 147 | Fartboy | FARTBOY | à vérifier | févr. 2025 | ≈ 194 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 92 ; CG `fartboy` |
| 148 | GreenHood | HOOD | à vérifier | sept. 2026 | ≈ 191 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 632 ; CG `greenhood` |
| 149 | Bert | BERT | Solana | 2024 | ≈ 190 M$ (estimation CoinGecko de l'annexe 3) | estimé | mort |  | épique | épique |  | à définir | v1 n° 562 ; correction r3 ; CG `bert` |
| 150 | MiniDOGE | MINIDOGE | BSC | juil. 2021 | ≈ 190 M$ en FDV (08/07/2021) | estimé | mort | Clone de Dogecoin en version reflection sur BSC, lancé en juil. 2021 ; pic vers le 08/07/2021 ; aujourd'hui plus coté. | épique | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/minidoge/ |
| 151 | Ski Mask Dog † | SKI | Base | 2024 | ≈ 190 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 746 ; correction r3 ; CG `ski-mask-dog` |
| 152 | MarsMi | MARSMI | à vérifier | juil. 2025 | ≈ 188 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 98 ; CG `marsmi` |
| 153 | SATOSHI•NAKAMOTO | SATOSHI | Bitcoin (Runes) | 2024 | ≈ 188 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 737 ; CG `satoshi-nakamoto-rune` |
| 154 | 360noscope420blazeit | MLG | à vérifier | févr. 2025 | ≈ 187 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 528 ; CG `360noscope420blazeit` |
| 155 | Pepecoin | PEP | à vérifier | déc. 2024 | ≈ 187 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 99 ; v1 n° 709 ; CG `pepecoin-network` |
| 156 | Giggle Academy | GIGGLE | BNB Chain | oct. 2025 | ≈ 186 M$ (26 oct. 2025), sourcé | sourcé | en déclin |  | épique | épique |  | à définir | v1 n° 627 ; correction r3 ; CG `giggle-fund` ; https://coinmarketcap.com/currencies/giggle-fund/ |
| 157 | Happy | HAPPY | Solana | janv. 2026 | ≈ 186 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 633 ; CG `happycat-2` |
| 158 | Shark Cat | SC | Solana | mars 2024 | ≈ 186 M$ en FDV (6 avr. 2024 ; capitalisation CMC ≈ 52 M$) | estimé | mort |  | épique | épique |  | à définir | v1 n° 740 ; correction r3 ; CG `shark-cat` ; https://coinmarketcap.com/currencies/shark-cat/ |
| 159 | The Black Bull | ANSEM | à vérifier | juil. 2026 | ≈ 186 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 105 ; CG `the-black-bull` |
| 160 | Trollface | TROLL | Solana | 2025-2026 | ≈ 186 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 110 ; correction r3 ; CG `troll-face` |
| 161 | Marshall Rogan Inu | MRI | Ethereum | févr. 2022 | ≈ 185 M$ en FDV (04/03/2022) | estimé | mort | Jeton « Inu » nommé d'après Marshall, le chien de Joe Rogan sur Ethereum, lancé en févr. 2022 ; pic vers le 04/03/2022 ; aujourd'hui plus coté. | épique | rare | personne réelle | à définir | r2 ; https://coinmarketcap.com/currencies/marshall-rogan-inu/ |
| 162 | Based Pepe | PEPE | Base | 2024 | ≈ 184 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 557 ; CG `based-pepe` |
| 163 | Bertram The Pomeranian | BERT | à vérifier | à vérifier (sommet le 2024-11-15) | ≈ 184 M$, 2024-11-15 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | épique | épique |  | à définir | R5 C1 `bertram-the-pomeranian` ; https://www.coingecko.com/en/coins/bertram-the-pomeranian |
| 164 | Shiba Samurai | SHIBURAI | Ethereum | déc. 2021 | ≈ 184 M$ en FDV (02/02/2022) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en déc. 2021 ; pic vers le 02/02/2022 ; aujourd'hui plus coté. | épique | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/shiba-samurai/ |
| 165 | NikolAI | NIKO | TON | 2024-2026 | ≈ 181 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | épique | rare |  | à définir | v1 n° 513 ; CG `nikolai` |
| 166 | Mooncoin † | MOON | Mooncoin (blockchain propre) | 2013 | ≈ 179 M$, 07/01/2018 (≈ 3,5 M$ dès le 26/01/2014) | sourcé | à vérifier (homonyme sur CoinGecko, non rapproché) | Mooncoin : mème de l'ère 2013-2014 | épique | épique |  | à définir | v1 n° 686 ; correction r1 ; https://coinmarketcap.com/historical/20180107/ ; https://www.financemagnates.com/cryptocurrency/news/mooncoin-blasts-off-gains-50/ |
| 167 | Foxy | FOXY | Linea | avr. 2024 (ajout CMC) | ≈ 178 M$ (juin 2024) ; ATH CoinGecko × offre en circulation actuelle (CMC ne publie qu'à partir de plus tard : ≈ 10 M$ le 26 oct. 2025) | estimé | mort | Foxy, renard mascotte non officiel de Linea (le L2 de Consensys, comme le renard MetaMask), avril 2024 ; -99,8 %. | épique | épique |  | à définir | r4 ; https://coinmarketcap.com/currencies/foxy/ ; https://www.coingecko.com/en/coins/foxy |
| 168 | ElonXCat | EXC | à vérifier | avr. 2025 | ≈ 176 M$ (estimé CG) | estimé | en déclin |  | épique | épique | personne réelle | à définir | v1 n° 101 ; CG `elonxcat` |
| 169 | "　" | "　" | à vérifier | à vérifier (sommet le 2024-12-07) | ≈ 174 M$, 2024-12-07 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | épique | épique |  | à définir | R5 C1 `-6` ; https://www.coingecko.com/en/coins/-6 |
| 170 | Shoggoth | SHOGGOTH | à vérifier | nov. 2024 | ≈ 173 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 744 ; CG `shoggoth` |
| 171 | Anonymous Cat | ZCAT | à vérifier | sept. 2026 | ≈ 170 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 107 ; CG `anonymous-cat` |
| 172 | GME (Ethereum) | GME | à vérifier | déc. 2024 | ≈ 170 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 115 ; correction r3 ; CG `game-stop` |
| 173 | Penguin (à ne pas confondre avec Pudgy Penguins) | PENGUIN | Solana | 2026 | ≈ 170 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 109 ; correction r3 ; CG `nietzschean-penguin` |
| 174 | Peng | PENG | Solana | mars 2024 | ≈ 169 M$ (14 mars 2024) | estimé | mort | Pingouin de la folie de mars 2024 ; il monte à ~170 M$ en une semaine puis s'efface. | épique | épique |  | à définir | r3 ; https://coinmarketcap.com/currencies/peng-sol/ ; https://dexscreener.com/solana/A3eME5CetyZPBoWbRUwY3tSe25S6tb18ba9ZPbWk9eFJ |
| 175 | PeiPei | PEIPEI | Ethereum | 2024 | ≈ 165 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 188 ; correction r3 ; CG `peipeicoin-vip` |
| 176 | Tron Bull | BULL | Tron | août-sept. 2024 | ≈ 164 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 774 ; CG `tron-bull` |
| 177 | Buff Doge Coin | DOGECOIN | BSC | sept. 2021 | ≈ 163 M$ en FDV (01/11/2021) | estimé | mort | Mème du « Buff Doge » (Doge bodybuildé) sur BSC, lancé en sept. 2021 ; pic vers le 01/11/2021 ; aujourd'hui -99,01 %. | épique | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/buff-doge-coin/ |
| 178 | 牛来 (Niu Lai) | 牛来 | à vérifier | sept. 2026 | ≈ 162 M$ (estimé CG) | estimé | actif |  | épique | épique |  | à définir | v1 n° 113 ; CG `niu-lai` |
| 179 | WHY | WHY | à vérifier | nov. 2024 | ≈ 161 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 790 ; CG `why` |
| 180 | Grok | GROK | Ethereum | nov. 2023 - 2024 | ≈ 160 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 112 ; correction r3 ; CG `grok-2` |
| 181 | Keyboard Cat (Base) | KEYCAT | à vérifier | à vérifier (sommet le 2024-11-15) | ≈ 158 M$, 2024-11-15 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | épique | épique |  | à définir | R5 C1 `keyboard-cat-base` ; https://www.coingecko.com/en/coins/keyboard-cat-base |
| 182 | Dejitaru Tsuka | TSUKA | Ethereum | 2022 | ≈ 157 M$ (estimé CG) | estimé | mort |  | épique | épique |  | à définir | v1 n° 596 ; CG `dejitaru-tsuka` |
| 183 | GUMMY | GUMMY | Solana | avr. 2024 | ≈ 157 M$ (22 avr. 2024) | estimé | mort | Ours en gélatine lancé le 22/04/2024 ; record dès le premier jour, puis chute continue. | épique | épique |  | à définir | r3 ; https://coinmarketcap.com/currencies/gummy/ ; https://dexscreener.com/solana/H7bTHGb5Cvo5fGe5jBDNDPUv8KykQnzyZA3qZ8sH7yxw |
| 184 | ZynCoin | ZYN | Ethereum | 27/11/2023 | ≈ 157 M$ (11/03/2024) | estimé | mort | Mème des sachets de nicotine Zyn, porté par la culture « zoomer » début 2024, puis abandon. | épique | épique |  | à définir | r3 ; https://www.coingecko.com/en/coins/zyncoin-2 ; https://dexscreener.com/ethereum/0x58cB30368ceB2d194740b144EAB4c2da8a917Dcb |
| 185 | Sigma | SIGMA | Solana | juil. 2024 | ≈ 155 M$ (date inconnue) | estimé | en déclin (≈ 0,98 M$) | Le mème du « sigma male » passe au-dessus de 100 M$, puis perd 99 %. | épique | épique |  | à définir | r3 ; https://www.coingecko.com/en/coins/sigma ; https://dexscreener.com/solana/424kbbjyt6vksn7gekt9vh5yetutr1sbeyoya2nmbjpw |
| 186 | Billy (Bitcoin) | BILLY | à vérifier | nov. 2024 | ≈ 154 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 111 ; CG `billion-dollar-cat-runes` |
| 187 | Rich Quack | QUACK | BNB Chain | nov. 2021 | ≈ 153 M$ (12 déc. 2021), sourcé | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 730 ; correction r4 ; CG `richquack` ; https://coinmarketcap.com/currencies/richquack-com/ |
| 188 | Wall Street Memes | WSM | Ethereum | 2023 | ≈ 153 M$ le 29/09/2023 (ATH 0,077 $ × 1,99 Md en circulation, estimé) | estimé | mort |  | épique | épique |  | à définir | v1 n° 786 ; correction r3 ; CG `wall-street-memes` ; https://www.coingecko.com/en/coins/wall-street-memes |
| 189 | A Meme Coin | AMC | à vérifier | sept. 2026 | ≈ 151 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 124 ; CG `a-meme-coin` |
| 190 | Miggles † | MIGGLES | Base | 2024 | ≈ 151 M$ (17 nov. 2024), sourcé (Mr Miggles, Base) | sourcé | mort |  | épique | épique |  | à définir | v1 n° 674 ; correction r4 ; CG `mister-miggles` ; https://coinmarketcap.com/currencies/mr-miggles/ |
| 191 | BILLION•DOLLAR•CAT | BDC | Bitcoin (Runes) | nov. 2024 | ≈ 150 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | épique | épique |  | à définir | v1 n° 114 |
| 192 | Bob † | BOB | Ethereum | -99,7 % | ≈ 150 M$ le 06/05/2023 (ATH 2,18e-4 $ × 690 Md, estimé) | estimé | mort |  | épique | épique |  | à définir | v1 n° 567 ; correction r3 ; CG `bob-3` ; https://www.coingecko.com/en/coins/bob-token |
| 193 | Husky | HUSKY | Ethereum | avr. 2021 | ≈ 150 M$ en FDV (10/05/2021) | estimé | mort | Clone SHIB sur Ethereum (avr. 2021) : moitié de l'offre envoyée à Vitalik Buterin, moitié bloquée sur Uniswap ; pic le 10/05/2021, plus coté. | épique | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/husky/ |
| 194 | Mongoose | MONGOOSE | à vérifier | déc. 2021 | ≈ 149 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 682 ; CG `mongoose` |
| 195 | GOHOME | GOHOME | à vérifier | mars 2025 | ≈ 146 M$ (estimé CG) | estimé | actif |  | épique | épique |  | à définir | v1 n° 119 ; CG `gohome` |
| 196 | Welsh Corgi Coin † | WELSH | Stacks | 2021 | ≈ 146 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 787 ; CG `welsh-corgi-coin` |
| 197 | 4Chan | 4CHAN | à vérifier | juil. 2023 | ≈ 145 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 123 ; CG `4chan` |
| 198 | Smoking Chicken Fish | SCF | Solana (pump.fun) | juil. 2024 | ≈ 145 M$ (date inconnue) | estimé | mort (≈ 0,32 M$) | Un mème absurde de pump.fun passé au-dessus de 100 M$, puis abandonné. | épique | épique |  | à définir | r3 ; https://www.coingecko.com/en/coins/smoking-chicken-fish ; https://dexscreener.com/solana/6uspebbn94duylui4a2wo3azdcyozon1plgyu27jzpkx |
| 199 | Bongo | BONGO | Solana | Hackathon IA, janv. 2025 | ≈ 143 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | épique | rare |  | à définir | v1 n° 291 ; correction r3 ; CG `bongo-cat` |
| 200 | Wojak Coin | WOJAK | Ethereum | 2023 | ≈ 143 M$ le 25/11/2024 (ATH 0,002056 $ × 69,42 Md, estimé) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 792 ; correction r3 ; CG `wojak` ; https://www.coingecko.com/en/coins/wojak |
| 201 | Hoppy | HOPPY | Ethereum | 2024 | ≈ 142 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | rare |  | à définir | v1 n° 368 ; correction r3 ; CG `hoppy-meme` |
| 202 | Keyboard Cat † | KEYCAT | Base | 2024 | ≈ 140 M$ (estimation CoinGecko de l'annexe 3) | estimé | mort |  | épique | épique |  | à définir | v1 n° 656 ; correction r3 ; CG `keyboard-cat` |
| 203 | RyuJin | RYU | à vérifier | juin 2024 | ≈ 140 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 104 ; CG `ryujin` |
| 204 | Silly Dragon | SILLY | Solana | déc. 2023 | ≈ 140 M$ (27 déc. 2023) | sourcé | mort | Dragon inspiré du déguisement d'Anatoly Yakovenko à Breakpoint 2023 ; un acheteur a changé 1,5 SOL en ~2 M$ (Lookonchain) ; il vaut ~60 k$. | épique | épique |  | à définir | r3 ; https://coinmarketcap.com/currencies/silly-dragon/ ; https://dexscreener.com/solana/7EYnhQoR9YM3N7UoaKRoA44Uy8JeaZV3qyouov87awMs |
| 205 | 币安Holder (BNBHolder) | BNBHOLDER | BNB Chain | 09/10/2025 (four.meme) | ≈ 140 M$ (09/10/2025) ; ATH CMC × 1 Md ≈ 162 M$ | sourcé | mort (≈ 0,5 M$) | Lancé le jour de Meme Rush, 85 M$ en 15 min ; un portefeuille a fait 5 245 $ → 2,16 M$ en 40 min et 13 portefeuilles ont gagné plus d'1 M$ (Lookonchain). | épique | épique |  | à définir | r3 ; https://atomicwallet.io/academy/articles/top-5-bnb-chain-memecoins-october-2025-season ; https://www.cryptopolitan.com/trader-turns-5k-into-2-16m-with-trade-trick/ |
| 206 | Resistance Dog | REDO | TON | 2024 | ≈ 138 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 728 ; CG `resistance-dog` |
| 207 | Moonbirds | BIRB | à vérifier | févr. 2026 | ≈ 136 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 120 ; CG `moonbirds` |
| 208 | Miu | MIU | Sui | 2026 | ≈ 135 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 422 ; CG `miu-2` |
| 209 | FEED EVERY GORILLA | FEG | à vérifier | janv. 2024 | ≈ 134 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 127 ; CG `feg-token-2` |
| 210 | Bad Idea AI | BAD | Ethereum | 05/05/2023 | ≈ 133 M$ (12/08/2023) | estimé | mort | Mème « sans utilité » lié à la sphère Shibarium, +580 % en août 2023, puis oubli. | épique | épique |  | à définir | r3 ; https://www.coingecko.com/en/coins/bad-idea-ai ; https://dexscreener.com/ethereum/0x32b86b99441480a7E5BD3A26c124ec2373e3F015 |
| 211 | Goose Token | GOOSE | à vérifier | août 2026 | ≈ 133 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 143 ; CG `goose-token` |
| 212 | PURPLE PEPE | PURPE | à vérifier | nov. 2024 | ≈ 133 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 139 ; CG `purple-pepe` |
| 213 | Star Wars Cat | SWCAT | BNB Chain | nov. 2021 (ajout CMC) | ≤ 133 M$ en FDV (28 nov. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Chat Star Wars de nov. 2021, mème BSC à FDV gonflée ; plus coté après mars 2023. | épique | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/star-wars-cat/ ; https://coinmarketcap.com/historical/20211128/ |
| 214 | WATER | WATER | Solana | juin 2024 | ≈ 133 à 243 M$ (25-30 juin 2024) | estimé | mort | Jeton « WATER » lancé fin juin 2024 ; pic le jour même, puis plus aucun volume. | épique | épique |  | à définir | r3 ; https://coinmarketcap.com/currencies/water/ ; https://dexscreener.com/solana/B6h248NJkAcBAkaCnji889a26tCiGXGN8cxhEJ4dX391 |
| 215 | Hatch | HATCH | à vérifier | mai 2025 | ≈ 132 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 637 ; CG `hatch-2` |
| 216 | FarmerDoge | CROP | BSC | août 2021 | ≈ 131 M$ en FDV (19/11/2021) | estimé | mort | Clone de Dogecoin à dividendes sur BSC, lancé en août 2021 ; pic vers le 19/11/2021 ; aujourd'hui plus coté. | épique | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/farmerdoge/ |
| 217 | ArbDoge AI † | AIDOGE | Arbitrum | 2023 | ≈ 130 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 541 ; correction r3 ; CG `arbdoge-ai` |
| 218 | Doginme † | DOGINME | Base | 2024 | ≈ 130 M$ (estimation CoinGecko de l'annexe 3) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 605 ; correction r3 ; CG `doginme` |
| 219 | Gork | GORK | Solana | Mai 2025 | ≈ 130 M$ (sourcé) | sourcé | mort |  | épique | épique |  | à définir | v1 n° 128 ; correction r3 ; CG `gork-2` |
| 220 | Jeff | JEFF | à vérifier | déc. 2024 | ≈ 130 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 144 ; CG `jeff-3` |
| 221 | Fred the Convicted Raccoon | FRED | Solana | Animaux, nov. 2024 | ≈ 129 M$ (sourcé) | sourcé | mort |  | épique | épique |  | à définir | v1 n° 130 ; correction r3 ; CG `first-convicted-raccoon` |
| 222 | Troll | TROLL | à vérifier | à vérifier (sommet le 2024-01-16) | ≈ 129 M$, 2024-01-16 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | épique | épique |  | à définir | R5 C1 `troll` ; https://www.coingecko.com/en/coins/troll |
| 223 | TEDDY BEAR | BEAR | à vérifier | déc. 2024 | ≈ 128 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 121 ; CG `teddy-bear` |
| 224 | BABY WHITE HAMSTER | BWH | BNB Chain | nov. 2021 (ajout CMC) | ≤ 126 M$ en FDV (21 nov. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Hamster blanc « Baby » de nov. 2021, mème BSC éphémère ; deux semaines au classement CMC. | épique | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/baby-white-hamster/ ; https://coinmarketcap.com/historical/20211121/ |
| 225 | Kitty Inu | Kitty | Ethereum | oct. 2021 | ≈ 124 M$ en FDV (07/11/2021) | estimé | mort | Mème chat « Inu » sur Ethereum, lancé en oct. 2021 ; pic vers le 07/11/2021 ; aujourd'hui plus coté. | épique | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/kitty-inu/ |
| 226 | Pain | PAIN | à vérifier | févr. 2025 | ≈ 122 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 150 ; CG `pain` |
| 227 | Torch of Liberty | LIBERTY | BNB Chain | juin 2025 (ajout CMC) | ≈ 122 M$ (31 août 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Flambeau de la statue de la Liberté, mème BSC de juin 2025 monté à ≈ 120 M$ fin août 2025, puis -99 %. | épique | épique |  | à définir | r4 ; https://coinmarketcap.com/currencies/torch-of-liberty/ ; https://www.coingecko.com/en/coins/torch-of-liberty |
| 228 | MEME HORSE | MHORSE | à vérifier | juin 2026 | ≈ 121 M$ (estimé CG) | estimé | actif |  | épique | épique |  | à définir | v1 n° 137 ; CG `meme-horse` |
| 229 | Housecoin | HOUSE | Solana | Printemps 2025 | ≈ 120 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 142 ; correction r3 ; CG `housecoin-2` |
| 230 | Marscoin | MARSCOIN | BNB Chain | sept. 2026 | ≈ 120 M$ (sourcé) | sourcé | en déclin |  | épique | épique |  | à définir | v1 n° 136 ; correction r3 ; CG `marscoin-4` |
| 231 | moonpig | MOONPIG | Solana (pump.fun) | mai 2025 | ≈ 120 M$ (date inconnue) | estimé | mort (≈ 90 k$, volume nul) | Le cochon de la saison 2025 de pump.fun dépasse 100 M$, puis s'éteint. | épique | épique |  | à définir | r3 ; https://www.coingecko.com/en/coins/moonpig ; https://dexscreener.com/solana/f8r9okkt8pvygkz6bcimxelyb2kun9e3fddugferuyjw |
| 232 | Palu | PALU | BNB Chain | oct. 2025 | ≈ 120 M$ (07/10/2025, ATH CMC × 1 Md) | estimé | mort (≈ 0,85 M$), -99,3 % → épique |  | épique | épique |  | à définir | v1 n° 703 ; correction r3 ; CG `palu` ; https://coinmarketcap.com/currencies/palu/ |
| 233 | EGL1 | EGL1 | à vérifier | juil. 2025 | ≈ 117 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 126 ; CG `egl1` |
| 234 | Koma Inu | KOMA | à vérifier | déc. 2024 | ≈ 117 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 135 ; CG `koma-inu` |
| 235 | Loser Coin | LOWB | Ethereum / BSC | avr. 2021 | ≈ 117 M$ (11/05/2021) | sourcé | mort | « LOWB », mème chinois lancé par « deux pauvres types » (un père de village et un programmeur à 60 h par semaine) ; ≈ 117 M$ de capitalisation le 11/05/2021 selon CMC, aujourd'hui -99,98 %. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/loser-coin/ |
| 236 | Catbal | CATBAL | Hyperliquid (HIP-1) | à vérifier (sommet le 8 déc. 2024) | ≈ 116,3 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | en déclin | Mème né sur Hypurr Fun, l'un des premiers tickers HIP-1 vendus aux enchères ; record le 8 déc. 2024 au sommet de la folie HYPE, puis -99,6 %. | épique | épique |  | à définir | r4 ; https://www.coingecko.com/en/coins/catbal ; https://chaincatcher.com/en/article/2157030 |
| 237 | Bitcoin Bull | BTCBULL | à vérifier | juil. 2025 | ≈ 115 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 132 ; CG `bitcoin-bull-2` |
| 238 | Lock In | LOCKIN | Solana | 2024 | ≈ 115 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 661 ; CG `lock-in` |
| 239 | Crow with Knife | CAW | Ethereum (cité dans des listes Base) | 2024 | ≈ 114 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 588 ; CG `crow-with-knife` |
| 240 | Higher † | HIGHER | Base | 2024 | ≈ 114 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 640 ; CG `higher` |
| 241 | tooker kurlson | TOOKER | Solana | avr. 2024 | ≈ 114 M$ (3 mai 2024) | estimé | mort | Parodie mal orthographiée de Tucker Carlson, de la vague « Tremp/Boden » ; plus de 110 M$ début mai 2024. | épique | épique | politique, personne réelle | à définir | r3 ; https://coinmarketcap.com/currencies/tooker-kurlson/ ; https://dexscreener.com/solana/9EYScpiysGnEimnQPzazr7Jn9GVfxFYzgTEj85hV9L6U |
| 242 | Pikaboss | PIKA | à vérifier | nov. 2024 | ≈ 113 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 146 ; CG `pikaboss` |
| 243 | ANSEM | ANSEM | Solana | 2026 | ≈ 112 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | épique | épique |  | à définir | v1 n° 141 ; correction r3 |
| 244 | XRP ARMY | ARMY | à vérifier | janv. 2025 | ≈ 112 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 140 ; CG `army-3` |
| 245 | Broccoli | BROCCOLI | à vérifier | avr. 2025 | ≈ 111 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 133 ; CG `broccoli-3` |
| 246 | dogi | DOGI | à vérifier | déc. 2023 | ≈ 111 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 156 ; CG `dogi` |
| 247 | AstroElon | ELONONE | à vérifier | 2021 | ≈ 109 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° 544 ; CG `astroelon` |
| 248 | Shiba Inu Treat | TREAT | à vérifier | janv. 2025 | ≈ 109 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 159 ; CG `shiba-inu-treat` |
| 249 | Meme Kombat | MK | Ethereum | prévente 2023, DEX 04/03/2024 | ≈ 108 M$ (09/03/2024) | estimé | mort | Prévente « mèmes qui se battent » très promue en 2023, écrasée dès sa cotation. Pic de 108 M$ suspect, laissé en rare. | épique | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/meme-kombat ; https://dexscreener.com/ethereum/0x9FDFb933Ee990955D3219d4F892FD1F786b47C9B |
| 250 | Zack Morris | ZACK | Solana | mai 2024 | ≈ 106 M$ (23 mai 2024) | estimé | mort | Mème du personnage Zack Morris (« Sauvés par le gong ») ; plus de 100 M$ deux jours après son lancement en mai 2024. | épique | épique |  | à définir | r3 ; https://coinmarketcap.com/currencies/zack-morris/ ; https://dexscreener.com/solana/8vCAUbxejdtaxn6jnX5uaQTyTZLmXALg9u1bvFCAjtx7 |
| 251 | Refund | RFD | à vérifier | mai 2023 | ≈ 105 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 116 ; CG `refund` |
| 252 | SNAP | NAP | Solana | mars 2024 | ≈ 103 M$ en clôture le jour du lancement (17 mars 2024) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° 71 ; correction r3 ; CG `snap-kero` ; https://coinmarketcap.com/currencies/snap-sol/ |
| 253 | FART COIN | FRTC | à vérifier | mai 2024 | ≈ 102 M$ (estimé CG) | estimé | en déclin |  | épique | épique |  | à définir | v1 n° 152 ; CG `fart-coin` |
| 254 | Hamster | HAM | BSC | mai 2021 | ≈ 102 M$ (04/11/2021) | sourcé | mort | Mème hamster sur BSC, lancé en mai 2021 ; pic vers le 04/11/2021 ; aujourd'hui -99,84 %. | épique | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/hamster/ |
| 255 | Kiba Inu | KIBA | Ethereum | oct. 2021 | ≈ 100 M$ (à deux reprises, 2021-2022) | sourcé | mort | Jeton « Inu » inspiré de Kiba (Naruto), lancé sur Ethereum en oct. 2021 ; a atteint 100 M$ de capitalisation à deux reprises selon CoinDesk, puis relance de contrat et déclin. | épique | épique |  | à définir | r2 ; https://www.coindesk.com/price/kiba ; https://coinmarketcap.com/currencies/kiba-inu/ |
| 256 | Moltbook | à vérifier | Base | 2026 | ≈ 100 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | commune |  | à définir | v1 n° 678 ; CG `moltbook` |
| 257 | LOBO•THE•WOLF•PUP | LOBO | Bitcoin (Runes) | 2024 | ≈ 3,59 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | rare | épique |  | à définir | v1 n° 181 ; CG `lobo-the-wolf-pup-runes` |
| 258 | lmeow | LMEOW | à vérifier | nov. 2024 | ≈ 99 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 157 ; CG `lmeow-2` |
| 259 | Monkey Pox | POX | à vérifier | sept. 2024 | ≈ 99 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 145 ; CG `monkey-pox` |
| 260 | Official FO | FO | à vérifier | sept. 2025 | ≈ 97 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 149 ; CG `official-fo` |
| 261 | Slothana | SLOTH | Solana | 2024 | ≈ 97 M$ en FDV (13 mai 2024 ; capitalisation CMC ≈ 47 M$) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 748 ; correction r3 ; CG `slothana` ; https://coinmarketcap.com/currencies/slothana/ |
| 262 | Lucidum | LUCIC | à vérifier | nov. 2025 | ≈ 94 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 154 ; CG `lucidum` |
| 263 | Smole | SMOLE | Solana | Mars 2024 | ≈ 94 M$ en clôture le jour du lancement (21 mars 2024) | sourcé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 751 ; correction r3 ; CG `smolecoin` ; https://coinmarketcap.com/currencies/smolecoin/ |
| 264 | DogBull | DOGO | à vérifier | août 2026 | ≈ 93 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 147 ; CG `dogbull` |
| 265 | Baby Claw | BABYCLAW | à vérifier | févr. 2026 | ≈ 91 M$ (plancher : capitalisation actuelle) | estimé | actif |  | rare | rare |  | à définir | v1 n° 546 ; CG `baby-claw` |
| 266 | PePeonTron | PEPEONTRON | Tron | juil. 2025 | ≈ 90 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 710 ; CG `pepeontron` |
| 267 | PooCoin | POOCOIN | à vérifier | mai 2021 | ≈ 89 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 138 ; CG `poocoin` |
| 268 | 哈基米 (Hakimi, Hajimi) | 哈基米 | BNB Chain | oct.-déc. 2025 | ≈ 88 M$ (06/09/2026, ATH CMC × 1 Md) (au-dessus de la borne sourcée ≥ 37 M$ (BingX, 2026 ; 10 à 12,7 M$ ailleurs)) | estimé | en déclin (≈ 16 M$), -81 % |  | rare | rare |  | à définir | v1 n° 281 ; correction r3 ; CG `hakimi` ; https://coinmarketcap.com/currencies/hajimi/ |
| 269 | Jesus Coin | JESUS | Ethereum | 25/04/2023 | ≈ 87 M$ le 01/12/2023 (ATH 5,59e-7 $ × 156,5 T en circulation ; ≈ 435 M$ sur l'offre totale) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 148 ; correction r3 ; CG `jesus-coin` ; https://www.coingecko.com/en/coins/jesus-coin |
| 270 | Nobody Sausage | NOBODY | Solana | avr. 2025 | ≈ 87 M$ (date inconnue) | estimé | en déclin (≈ 0,27 M$) | La saucisse qui danse, un mème viral de 2025, perd presque toute sa valeur. | rare | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/nobody-sausage ; https://dexscreener.com/solana/7rqd8fhc1rimv3v9edcrz6rnfsjn1puxm9umjaurjrnj |
| 271 | DOWGE | DJI6930 | à vérifier | juil. 2025 | ≈ 85 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 164 ; CG `dowge` |
| 272 | mini | MINI | à vérifier | à vérifier (sommet le 2024-10-13) | ≈ 85 M$, 2024-10-13 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `minimini` ; https://www.coingecko.com/en/coins/minimini |
| 273 | Daddy Doge | DADDYDOGE | à vérifier | juil. 2021 | ≈ 83 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 153 ; CG `daddy-doge` |
| 274 | GeorgePlaysClashRoyale | CLASH | à vérifier | oct. 2025 | ≈ 82 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 162 ; CG `georgeplaysclashroyale` |
| 275 | Kabosu | KABOSU | à vérifier | mai 2021 | ≈ 82 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 178 ; CG `kabosu` |
| 276 | SquidGrow | SQGROW | à vérifier | déc. 2024 | ≈ 82 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 171 ; CG `squidgrow-2` |
| 277 | Mochi † | MOCHI | Base | 2024 | ≈ 81 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 197 ; correction r3 ; CG `mochi-thecatcoin` |
| 278 | Yummy | YUMMY | à vérifier | mai 2021 | ≈ 81 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 176 ; CG `yummy` |
| 279 | 4Stock | 4STOCK | BNB Chain | sept. 2026 | ≈ 80 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 165 ; correction r3 ; CG `4stock` |
| 280 | AXOL | AXOL | Sui | à vérifier (sommet le 15 déc. 2024) | ≈ 79,0 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | en déclin | Axolotl de Sui : +266 % en deux jours et record le 15 déc. 2024, pendant le record du SUI, puis -99 %. | rare | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/axol ; https://www.tradingview.com/chart/AXOLUSDT/Jng15GKf-AXOL-Surges-266-to-a-New-All-Time-High-in-Just-2-Days |
| 281 | Basecat | BASECAT | à vérifier | sept. 2026 | ≈ 79 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 173 ; correction r3 ; CG `basecat` |
| 282 | Qkacoin | QKA | à vérifier | juil. 2025 | ≈ 79 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 168 ; CG `qkacoin` |
| 283 | 8-Bit Coin | COIN | à vérifier | sept. 2024 | ≈ 78 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 155 ; CG `8-bit-coin` |
| 284 | Book of Ethereum | BOOE | à vérifier | oct. 2024 | ≈ 78 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 169 ; correction r3 ; CG `book-of-ethereum` |
| 285 | Moolah | MOOLAH | à vérifier | oct. 2026 | ≈ 78 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 170 ; CG `moolah` |
| 286 | APES | APES | à vérifier | sept. 2026 | ≈ 77 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 172 ; CG `apes-2-2` |
| 287 | Harambe | HARAMBE | Solana | « MartyrFi », 2024 | ≈ 76 M$ (13 nov. 2024) | sourcé | en déclin |  | rare | rare |  | à définir | v1 n° 634 ; correction r3 ; CG `harambe` ; https://coinmarketcap.com/currencies/harambe-on-solana/ |
| 288 | The Spirit of Gambling | TOKABU | à vérifier | août 2025 | ≈ 76 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 213 ; CG `the-spirit-of-gambling` |
| 289 | Joe Coin | JOE | à vérifier | juin 2025 | ≈ 75 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 186 ; CG `joe-coin` |
| 290 | Solama | SOLAMA | Solana | Mars 2024 | ≈ 75 M$ (11 mars 2024 ; capitalisation CMC ≈ 73 M$) | sourcé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 754 ; correction r3 ; CG `solama` ; https://coinmarketcap.com/currencies/solama/ |
| 291 | Unstable Coin | USDUC | à vérifier | sept. 2025 | ≈ 75 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 160 ; CG `unstable-coin` |
| 292 | MSTR2100 | MSTR | à vérifier | à vérifier (sommet le 2024-11-08) | ≈ 72 M$, 2024-11-08 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `mstr2100` ; https://www.coingecko.com/en/coins/mstr2100 |
| 293 | Feisty Doge NFT | NFD | Ethereum | août 2021 | ≈ 71,2 M$ en FDV (28/10/2021) | estimé | en déclin | Fraction du NFT original de la photo Doge (Kabosu), découpé en jetons sur Ethereum (août 2021) ; pic le 28/10/2021, aujourd'hui -95,8 %. | rare | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/feisty-doge-nft/ |
| 294 | Froggie | FROGGIE | à vérifier | sept. 2025 | ≈ 71 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 177 ; CG `froggie` |
| 295 | Manyu | MANYU | à vérifier | sept. 2025 | ≈ 70 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 192 ; CG `manyu-2` |
| 296 | Wownero | WOW | blockchain propre (fork de Monero) | avril 2018 | ≈ 70 M$ (2 mai 2021) ; CMC, relevé hebdomadaire | sourcé | à vérifier | Wownero, fork « mème » de Monero (2018) à mascotte Doge ; ≈ 70 M$ au pic de mai 2021. | rare | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/wownero/ ; https://coinmarketcap.com/historical/20210502/ |
| 297 | Milo Inu | MILO | à vérifier | avr. 2022 | ≈ 68 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 196 ; CG `milo-inu` |
| 298 | ZZZ | ZZZ | à vérifier | sept. 2026 | ≈ 68 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 198 ; CG `zzz-2` |
| 299 | Cocoro | COCORO | à vérifier | mars 2025 | ≈ 66 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 222 ; CG `cocoro` |
| 300 | Vita Inu | VINU | à vérifier | déc. 2024 | ≈ 66 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 242 ; CG `vita-inu` |
| 301 | pipedog | PIPEDOG | à vérifier | juil. 2026 | ≈ 65 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 193 ; CG `pipedog` |
| 302 | PiP | PIP | à vérifier | déc. 2024 | ≈ 64 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 225 ; CG `pip-3` |
| 303 | Utya | UTYA | à vérifier | mai 2026 | ≈ 63 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 199 ; CG `utya` |
| 304 | Wall Street Pepe | WEPE | à vérifier | à vérifier (sommet le 2025-02-17) | ≈ 63 M$, 2025-02-17 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `wall-street-pepe` ; https://www.coingecko.com/en/coins/wall-street-pepe |
| 305 | Byte | BYTE | à vérifier | mars 2024 | ≈ 61 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 195 ; CG `byte` |
| 306 | Crob Mob | CROB | à vérifier | avr. 2024 | ≈ 61 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 201 ; CG `crob-mob` |
| 307 | Dessa | DESSA | à vérifier | nov. 2026 | ≈ 59 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 216 ; CG `dessa` |
| 308 | Boss | BOSS | à vérifier | nov. 2021 | ≈ 58 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 194 ; CG `boss` |
| 309 | Build On BNB | BOB | à vérifier | juin 2025 | ≈ 58 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 200 ; correction r3 ; CG `build-on-bnb` |
| 310 | Kori | KORI | à vérifier | juil. 2025 | ≈ 58 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 219 ; CG `kori` |
| 311 | USCR | USCR | à vérifier | janv. 2026 | ≈ 58 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 191 ; CG `uscr` |
| 312 | Chump Coin | CHUMP | à vérifier | sept. 2026 | ≈ 57 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 229 ; CG `chump-coin` |
| 313 | Gorbagana | GOR | à vérifier | à vérifier (sommet le 2025-06-21) | ≈ 57 M$, 2025-06-21 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `gorbagana` ; https://www.coingecko.com/en/coins/gorbagana |
| 314 | MUSHROOM | SHROOM | à vérifier | sept. 2026 | ≈ 57 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 223 ; CG `mushroom-2` |
| 315 | Not in Employment, Education, or Training | NEET | à vérifier | sept. 2026 | ≈ 56 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 221 ; CG `neet` |
| 316 | Dogz | DOGZ | à vérifier | avr. 2019 | ≈ 55 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 202 ; CG `dogz` |
| 317 | CREPE | CREPE | à vérifier | oct. 2025 | ≈ 54 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 218 ; CG `crepe-2` |
| 318 | HoodPork | PORKU | à vérifier | oct. 2026 | ≈ 53 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 227 ; CG `hoodpork` |
| 319 | Pwease | PWEASE | à vérifier | mars 2025 | ≈ 53 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 230 ; CG `pwease` |
| 320 | wojak | WOJAK | à vérifier | juin 2026 | ≈ 53 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 228 ; CG `wojak-5` |
| 321 | Bullish Degen | BULLISH | à vérifier | à vérifier (sommet le 2025-11-29) | ≈ 52 M$, 2025-11-29 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `bullish-degen` ; https://www.coingecko.com/en/coins/bullish-degen |
| 322 | noice | NOICE | à vérifier | oct. 2025 | ≈ 52 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 167 ; CG `noice` |
| 323 | Baby Shiba Inu | BABYSHIBAINU | à vérifier | oct. 2021 | ≈ 51 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 232 ; CG `baby-shiba-inu` |
| 324 | CaptainBNB | CaptainBNB | BNB Chain | 10/02/2025 | ≈ 51 M$ (12/02/2025) | estimé | en déclin (≈ 1,7 M$, volume nul) | Mascotte née d'une image postée par le compte X de BNB Chain au tout début de la vague CZ ; flambée en deux jours, puis oubli. | rare | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/captainbnb/ |
| 325 | Hege | HEGE | à vérifier | nov. 2024 | ≈ 51 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 209 ; CG `hege` |
| 326 | Hosky † | HOSKY | Cardano | 2021 | ≥ 50 M$ (5 janv. 2025), sourcé (borne basse : CMC ne publie la capitalisation que depuis 2022 ; l'estimation CoinGecko de r5, ≈ 368 M$, paraît gonflée) | sourcé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 642 ; correction r4 ; CG `hosky` ; https://coinmarketcap.com/currencies/hosky-token/ |
| 327 | IlluminatiCoin | NATI | à vérifier | sept. 2024 | ≈ 50 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 244 ; CG `illuminaticoin` |
| 328 | Lofi | LOFI | Sui | 2025 † | ≈ 50 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 240 ; CG `lofi-2` |
| 329 | TEH EPIK DUCK | EPIK | à vérifier | avr. 2024 | ≈ 50 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 241 ; CG `teh-epik-duck` |
| 330 | WUFFI | WUF | WAX | avr. 2024 (ajout CMC) | ≈ 50 M$ (12 janv. 2025) ; CMC, relevé hebdomadaire | sourcé | à vérifier | WUFFI, chien mème de la blockchain WAX (2024) ; ≈ 50 M$ selon CMC le 12 janv. 2025, -99 % depuis. | rare | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/wuffi/ ; https://coinmarketcap.com/historical/20250112/ |
| 331 | Buttcoin | BUTTCOIN | Solana | janv. 2026 | ≈ 49 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin |  | rare | rare | obscène | à définir | v1 n° 460 ; CG `buttcoin-7` |
| 332 | I love puppies | PUPPIES | à vérifier | sept. 2025 | ≈ 49 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 238 ; CG `i-love-puppies` |
| 333 | KNOTS | KNOTS | à vérifier | sept. 2026 | ≈ 49 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 250 ; CG `knots` |
| 334 | Pandacoin | PND | blockchain propre | févr. 2014 | ≈ 49,0 M$, 14/01/2018 (CMC, relevé hebdomadaire) | sourcé | en déclin | Fork de Dogecoin à panda, passé en preuve d'enjeu ; ≈ 1,4 M$ en 2014, ≈ 49 M$ en janv. 2018, encore listé sur CoinGecko à valeur infime. | rare | rare |  | à définir | r1 ; https://coinmarketcap.com/historical/20180114/ ; https://www.coingecko.com/en/coins/pandacoin |
| 335 | Sosana | SOSANA | Solana | 2024 | ≈ 49 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 758 ; CG `sosana` |
| 336 | XDOG | XDOG | à vérifier | sept. 2025 | ≈ 49 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 243 ; CG `xdog` |
| 337 | 客服小何 (Customer Service Xiao He) | 客服小何 | à vérifier | à vérifier (sommet le 2025-10-09) | ≈ 49 M$, 2025-10-09 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `customer-service-xiao-he` ; https://www.coingecko.com/en/coins/customer-service-xiao-he |
| 338 | Dingocoin | DINGO | à vérifier | août 2021 | ≈ 48 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 247 ; CG `dingocoin` |
| 339 | KiboShib | KIBSHI | à vérifier | nov. 2024 | ≈ 48 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 239 ; CG `kiboshib` |
| 340 | Manifesting | MANIFEST | à vérifier | juin 2026 | ≈ 48 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 248 ; CG `manifesting` |
| 341 | The Bitcoin Bull | TBB | à vérifier | juil. 2026 | ≈ 48 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 231 ; CG `the-bitcoin-bull` |
| 342 | Blub | BLUB | Sui | 2024 † | ≈ 47 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 246 ; CG `blub` |
| 343 | Everybody | HOLD | à vérifier | juil. 2025 | ≈ 46 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 252 ; CG `everybody` |
| 344 | Froge | FROGE | à vérifier | déc. 2024 | ≈ 46 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 208 ; CG `frogevip` |
| 345 | Aura Final Boss | KIMCHI | à vérifier | oct. 2026 | ≈ 45 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 233 ; CG `aura-final-boss-2` |
| 346 | microduck | MICRODUCK | à vérifier | sept. 2026 | ≈ 45 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 261 ; CG `microduck` |
| 347 | Pundu | PUNDU | Solana | juin 2024 | ≈ 45 M$ (28 mars 2024) | sourcé | en déclin |  | rare | rare |  | à définir | v1 n° 352 ; correction r3 ; CG `pundu` ; https://coinmarketcap.com/currencies/pundu/ |
| 348 | XDOGE | XDOGE | à vérifier | à vérifier (sommet le 2024-11-21) | ≈ 45 M$, 2024-11-21 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `xdoge-2` ; https://www.coingecko.com/en/coins/xdoge-2 |
| 349 | Coding Dino | DINO | à vérifier | à vérifier (sommet le 2025-05-21) | ≈ 44 M$, 2025-05-21 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `coding-dino` ; https://www.coingecko.com/en/coins/coding-dino |
| 350 | Doge KaKi | KAKI | à vérifier | avr. 2023 | ≈ 44 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 257 ; CG `doge-kaki` |
| 351 | The Official 67 Coin | 67 | à vérifier | nov. 2025 | ≈ 44 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 270 ; CG `the-official-67-coin` |
| 352 | BabyCashCat | BABY | à vérifier | oct. 2026 | ≈ 43 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 249 ; CG `babycashcat` |
| 353 | Memory cow Moo | MOO | à vérifier | sept. 2026 | ≈ 43 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 268 ; CG `memory-cow-moo` |
| 354 | Moochii | MOOCHII | à vérifier | mai 2021 | ≈ 43 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 255 ; CG `moochii` |
| 355 | NYC | NYC | à vérifier | janv. 2026 | ≈ 43 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 259 ; CG `nyc-token` |
| 356 | 1 Coin Can Change Your Life | 1-COIN-CAN-CHANGE-YOUR-LIFE | à vérifier | à vérifier (sommet le 2025-11-05) | ≈ 42 M$, 2025-11-05 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `1-coin-can-change-your-life` ; https://www.coingecko.com/en/coins/1-coin-can-change-your-life |
| 357 | Jimothy The Raccoon | JIMOTHY | Solana | 16/07/2026 | ≈ 42-47 M$ (22/07/2026) | estimé | en déclin (≈ 1,1 M$) | Un vrai raton laveur de Seattle au corps très court, devenu viral ; 42 M$ en six jours. | rare | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/jimothy-the-raccoon/ |
| 358 | DebtReliefBot | DRB | Base | à vérifier | ≈ 41 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 593 ; CG `debtreliefbot` |
| 359 | Jager Hunter | JAGER | à vérifier | mai 2025 | ≈ 40 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 260 ; CG `jager-hunter` |
| 360 | StupidCoin | STUPID | à vérifier | à vérifier (sommet le 2025-01-27) | ≈ 40 M$, 2025-01-27 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `stupidcoin-2` ; https://www.coingecko.com/en/coins/stupidcoin-2 |
| 361 | TENDIES | TENDIES | à vérifier | sept. 2026 | ≈ 40 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 262 ; CG `tendies-2` |
| 362 | ubik | UBIK | à vérifier | sept. 2026 | ≈ 40 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 272 ; CG `ubik` |
| 363 | apeonfone | FONE | à vérifier | août 2026 | ≈ 39 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 286 ; CG `apeonfone` |
| 364 | Araracoin | ARARA | à vérifier | juin 2025 | ≈ 39 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 264 ; CG `araracoin` |
| 365 | Claude Crab | CRABAI | à vérifier | juin 2026 | ≈ 39 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 274 ; CG `claude-crab` |
| 366 | KiraKuru | KRA | à vérifier | déc. 2024 | ≈ 39 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 275 ; CG `kirakuru` |
| 367 | BonkEarn | BERN | à vérifier | à vérifier (sommet le 2023-11-23) | ≈ 38 M$, 2023-11-23 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `bonkearn` ; https://www.coingecko.com/en/coins/bonkearn |
| 368 | Fuzzybear | FUZZY | à vérifier | juil. 2025 | ≈ 38 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 280 ; CG `fuzzybear` |
| 369 | Most Wanted | MOST | à vérifier | août 2025 | ≈ 38 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 284 ; CG `most-wanted-2` |
| 370 | Thinking Cat | HMM | à vérifier | août 2026 | ≈ 38 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 277 ; CG `thinking-cat` |
| 371 | PornRocket | PORNROCKET | BSC | mai 2021 | ≈ 35,0 M$ (19/01/2022) | sourcé | en déclin | Mème sur BSC, lancé en mai 2021 ; pic vers le 19/01/2022 ; aujourd'hui -98,16 %. | rare | rare | obscène | à définir | r2 ; https://coinmarketcap.com/currencies/pornrocket/ |
| 372 | SIXSEVEN | 67 | à vérifier | août 2026 | ≈ 35 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 290 ; CG `sixseven` |
| 373 | Buy the DIP | DIP | à vérifier | avr. 2024 | ≈ 34 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 292 ; CG `buy-the-dip` |
| 374 | Gstock | GSTOCK | à vérifier | sept. 2026 | ≈ 34 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 288 ; CG `gstock` |
| 375 | Cets On Gold | CETS | à vérifier | août 2026 | ≈ 32 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 279 ; CG `cets-on-gold` |
| 376 | FLORK | FLORK | à vérifier | sept. 2026 | ≈ 32 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 301 ; CG `flork-3` |
| 377 | Giggle Mascot | MAX | à vérifier | sept. 2026 | ≈ 32 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 302 ; CG `giggle-mascot` |
| 378 | IKUN | IKUN | Solana | letsbonk, 2025 | ≈ 32 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | commune |  | à définir | v1 n° 646 ; CG `ikun` |
| 379 | Pofu | POFU | à vérifier | oct. 2025 | ≈ 32 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 293 ; CG `pofu` |
| 380 | PUMPSTOP | XCAT | à vérifier | nov. 2026 | ≈ 32 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 294 ; CG `pumpstop` |
| 381 | The Stonks Exchange | STONKEX | à vérifier | à vérifier (sommet le 2026-09-06) | ≈ 32 M$, 2026-09-06 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `the-stonks-exchange` ; https://www.coingecko.com/en/coins/the-stonks-exchange |
| 382 | KarenCoin | KAREN | à vérifier | juin 2021 | ≈ 31 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 295 ; CG `karencoin` |
| 383 | Little John | JOHN | à vérifier | juil. 2026 | ≈ 31 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 297 ; CG `little-john` |
| 384 | Dickbutt | DICKBUTT | Base | déc. 2024 | ~30,6 M$ (date inconnue) | estimé | en déclin | Vieux mème Dickbutt lancé par le bot Clanker sur Farcaster en décembre 2024, LP verrouillée jusqu'en 2100, il reste à 0,4 M$. | rare | rare | obscène | à définir | r3 ; https://www.coingecko.com/en/coins/dickbutt |
| 385 | Harold | HAROLD | à vérifier | janv. 2025 | ≈ 30 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 304 ; CG `haroldonsol` |
| 386 | Luxxcoin | LUX | à vérifier | août 2026 | ≈ 30 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 308 ; CG `luxxcoin` |
| 387 | Memetern | MXT | à vérifier | sept. 2025 | ≈ 30 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 312 ; CG `memetern` |
| 388 | Volt Inu | VOLT | Ethereum | 2021-2024 | ≈ 30 M$ (sourcé) | sourcé | actif |  | rare | rare |  | à définir | v1 n° 331 ; correction r3 ; CG `volt-inu-3` |
| 389 | Yee Token | YEE | à vérifier | janv. 2026 | ≈ 30 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 299 ; CG `yee-token` |
| 390 | catwifmask | MASK | à vérifier | à vérifier (sommet le 2025-06-11) | ≈ 29 M$, 2025-06-11 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `catwifmask` ; https://www.coingecko.com/en/coins/catwifmask |
| 391 | Chill House | CHILLHOUSE | Solana | Été 2025 | ≈ 29 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 325 ; correction r3 ; CG `chill-house` |
| 392 | NutCoin | NUT | à vérifier | à vérifier (sommet le 2024-11-25) | ≈ 29 M$, 2024-11-25 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `nutcoin-meme` ; https://www.coingecko.com/en/coins/nutcoin-meme |
| 393 | Salute | SLT | à vérifier | janv. 2025 | ≈ 29 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 296 ; CG `salute` |
| 394 | Super Inu | SI | à vérifier | oct. 2026 | ≈ 29 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 313 ; CG `super-inu-3` |
| 395 | 401jK | 401JK | à vérifier | nov. 2025 | ≈ 28 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 335 ; CG `401jk` |
| 396 | ALLINU | ALLINU | à vérifier | sept. 2026 | ≈ 28 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 315 ; CG `allinu` |
| 397 | Dacity Coin | DACITY | à vérifier | nov. 2026 | ≈ 28 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 321 ; CG `dacity-coin-4` |
| 398 | GIVEBACK | GBACK | à vérifier | déc. 2025 | ≈ 28 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 316 ; CG `giveback` |
| 399 | Chomolon Joff | JOFF | à vérifier | août 2026 | ≈ 27 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 320 ; CG `chomolon-joff` |
| 400 | Tung Tung | TRIPLET | Solana (à confirmer) | Brainrot italien, 2025-2026 | ≈ 27 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 776 ; CG `tung-tung-tung-sahur-2` |
| 401 | Bear Champ | BCHAMP | à vérifier | oct. 2026 | ≈ 26 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 323 ; CG `bear-champ` |
| 402 | BORGY | BORGY | à vérifier | oct. 2025 | ≈ 26 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 319 ; CG `borgy` |
| 403 | PEPE 0x69 ON BASE | PEPE | à vérifier | à vérifier (sommet le 2024-05-23) | ≈ 26 M$, 2024-05-23 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `pepe-0x69-on-base` ; https://www.coingecko.com/en/coins/pepe-0x69-on-base |
| 404 | Pepes Dog | ZEUS | à vérifier | juin 2025 | ≈ 26 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 339 ; CG `pepes-dog` |
| 405 | PulseChain Peacock | PCOCK | à vérifier | avr. 2026 | ≈ 26 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 328 ; CG `pulsechain-peacock` |
| 406 | Robin the Frog | ROBIN | à vérifier | à vérifier (sommet le 2026-09-06) | ≈ 26 M$, 2026-09-06 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `robin-the-frog` ; https://www.coingecko.com/en/coins/robin-the-frog |
| 407 | BLUE CHIP | BLUECHIP | à vérifier | sept. 2026 | ≈ 25 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 324 ; CG `blue-chip-4` |
| 408 | CyberLeek | CYBERLEEK | à vérifier | août 2026 | ≈ 25 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 333 ; CG `cyberleek` |
| 409 | RUSSELL | RUSSELL | Base | oct. 2024 | ~24,6 M$ (nov. 2024 ?, non sourcé) | estimé | en déclin | Mème du chien de Brian Armstrong (Coinbase), lancé en octobre 2024, il reste à moins de 1 M$. | rare | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/russell ; https://dexscreener.com/base/0xEA8B7ED6170E0ea3703DdE6B496B065A8eCECd7B |
| 410 | Bobo | BOBO | à vérifier | mai 2026 | ≈ 24 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 332 ; CG `bobo-coin-2` |
| 411 | Bundle Cat | BUN | à vérifier | sept. 2026 | ≈ 24 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 326 ; CG `bundle-cat` |
| 412 | Buy The Cat | BTC | à vérifier | sept. 2026 | ≈ 24 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 327 ; CG `buy-the-cat` |
| 413 | Pup Doge | PUPDOGE | à vérifier | août 2021 | ≈ 24 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 341 ; CG `pup-doge` |
| 414 | Theros | THEROS | à vérifier | sept. 2026 | ≈ 24 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 330 ; CG `theros` |
| 415 | Tsuki | TSUKI | à vérifier | déc. 2024 | ≈ 24 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 344 ; CG `tsuki` |
| 416 | Burnie Senders | BURNIE | à vérifier | à vérifier (sommet le 2026-04-26) | ≈ 23 M$, 2026-04-26 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare | politique | à définir | R5 C1 `burnie-senders` ; https://www.coingecko.com/en/coins/burnie-senders |
| 417 | FOMO人生 | FOMO人生 | à vérifier | oct. 2026 | ≈ 23 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 336 ; CG `fomo-life` |
| 418 | Hachiko | HACHI | à vérifier | janv. 2026 | ≈ 23 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 337 ; CG `hachiko-3` |
| 419 | HUNDRED | HUNDRED | à vérifier | sept. 2026 | ≈ 23 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 338 ; CG `hundred` |
| 420 | 旺柴 (WangChai) | 旺柴 | BNB Chain | 17/09/2026 | ≈ 23-24 M$ (13-14/10/2026) | estimé | en déclin (≈ 1,7 M$) | L'émoji « chien qui ricane » de l'internet chinois en jeton ; 23 M$ un mois après le lancement, puis -93 %. | rare | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/wangchai/ |
| 421 | Freedom of Money | FREEDOM OF MONEY | à vérifier | avr. 2026 | ≈ 22 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 346 ; CG `freedom-of-money` |
| 422 | MyOnion.fun | ONION | à vérifier | juin 2026 | ≈ 22 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 693 ; CG `myonion-fun` |
| 423 | NEFE COIN | NEFE | à vérifier | oct. 2026 | ≈ 22 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 348 ; CG `nefe-coin` |
| 424 | The Toad Pepe | TOAD | à vérifier | août 2026 | ≈ 22 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 343 ; CG `the-toad-pepe` |
| 425 | CROCAT | CROCAT | à vérifier | oct. 2026 | ≈ 21 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 350 ; CG `crocat` |
| 426 | Icy | IC | à vérifier | avr. 2023 | ≈ 21 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 347 ; CG `icy` |
| 427 | Let's BONK | LETSBONK | à vérifier | à vérifier (sommet le 2025-04-26) | ≈ 21 M$, 2025-04-26 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `lets-bonk` ; https://www.coingecko.com/en/coins/lets-bonk |
| 428 | The Juggernaut | JUGGERNAUT | à vérifier | sept. 2026 | ≈ 21 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 353 ; CG `the-juggernaut` |
| 429 | BCOQ INU | BCOQ | à vérifier | à vérifier (sommet le 2024-03-13) | ≈ 20 M$, 2024-03-13 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `bcoq-inu` ; https://www.coingecko.com/en/coins/bcoq-inu |
| 430 | CRONUS | CRONUS | à vérifier | sept. 2026 | ≈ 20 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 355 ; CG `cronus-2` |
| 431 | DROP | DROP | à vérifier | janv. 2025 | ≈ 20 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 351 ; CG `drop-2` |
| 432 | The Bitcoin Mascot | BITTY | à vérifier | sept. 2025 | ≈ 20 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 349 ; CG `the-bitcoin-mascot` |
| 433 | The Last Play | RETIRE | à vérifier | oct. 2025 | ≈ 20 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 354 ; CG `the-last-play` |
| 434 | 金蝶圣甲 (Golden Butterfly Sacred Armor) | 金蝶圣甲 | à vérifier | juil. 2026 | ≈ 20 M$ (estimé CG) | estimé | en déclin |  | rare | rare | obscène | à définir | v1 n° 362 ; CG `golden-butterfly-sacred-armor` |
| 435 | Cryptocurrency Coin | CRYPTO | à vérifier | juin 2025 | ≈ 19 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 363 ; CG `cryptocurrency-coin` |
| 436 | Ket | KET | Solana | 2024 | ≈ 19 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 655 ; CG `ket-3` |
| 437 | Mars | MARS | à vérifier | à vérifier (sommet le 2024-09-30) | ≈ 19 M$, 2024-09-30 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `mars-2` ; https://www.coingecko.com/en/coins/mars-2 |
| 438 | Xavier: Renegade Angel | XAVIER | à vérifier | juin 2025 | ≈ 19 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 366 ; CG `xavier-renegade-angel` |
| 439 | donotfomoew | MOEW | Base | déc. 2024 | ≈ 18,4 M$ (29 déc. 2024), sourcé | sourcé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 317 ; correction r4 ; CG `moew` ; https://coinmarketcap.com/currencies/donotfomoew/ |
| 440 | JOBCOIN | JOBCOIN | à vérifier | janv. 2026 | ≈ 18 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 365 ; CG `jobcoin-2` |
| 441 | memestock | MEMESTOCK | à vérifier | sept. 2026 | ≈ 18 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 356 ; CG `memestock-3` |
| 442 | Rain Coin | RAIN | à vérifier | févr. 2024 | ≈ 18 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 361 ; CG `rain-coin` |
| 443 | PHNIX | PHNIX | XRP Ledger | déc. 2024 | ≈ 17,5 M$ (20 juil. 2025), sourcé (FDV CMC max ≈ 55 M$) | sourcé | en déclin |  | rare | rare |  | à définir | v1 n° 179 ; correction r4 ; CG `phnix` ; https://coinmarketcap.com/currencies/phoenix-xrp/ |
| 444 | Copper (inu) | COPPERINU | à vérifier | à vérifier (sommet le 2026-08-29) | ≈ 17 M$, 2026-08-29 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `copper-inu-2` ; https://www.coingecko.com/en/coins/copper-inu-2 |
| 445 | Shit Piss Skin Can | SPSC | à vérifier | à vérifier (sommet le 2026-01-02) | ≈ 17 M$, 2026-01-02 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare | obscène | à définir | R5 C1 `shit-piss-skin-can` ; https://www.coingecko.com/en/coins/shit-piss-skin-can |
| 446 | frong | FRONG | à vérifier | sept. 2026 | ≈ 16 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 369 ; CG `frong` |
| 447 | LC SHIB | LC | à vérifier | à vérifier (sommet le 2025-12-22) | ≈ 16 M$, 2025-12-22 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `lc-shib` ; https://www.coingecko.com/en/coins/lc-shib |
| 448 | V2EX | V2EX | à vérifier | sept. 2025 | ≈ 16 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 373 ; CG `v2ex` |
| 449 | 施工猫 (Construction Cat) | SUE | à vérifier | à vérifier (sommet le 2026-09-06) | ≈ 16 M$, 2026-09-06 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `shi-gong-mao` ; https://www.coingecko.com/en/coins/shi-gong-mao |
| 450 | 老子 | 老子 | BNB Chain | janv. 2026 | ≈ 16 M$ (11/01/2026, ATH CMC × 1 Md ; PANews : près de 20 M$) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 801 ; correction r3 ; CG `laozi` ; https://coinmarketcap.com/currencies/laozi/ |
| 451 | Gasspas | GASS | à vérifier | à vérifier (sommet le 2025-06-10) | ≈ 15 M$, 2025-06-10 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `gasspas` ; https://www.coingecko.com/en/coins/gasspas |
| 452 | GOATED | GOATED | à vérifier | sept. 2025 | ≈ 15 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 378 ; CG `goated-2` |
| 453 | Italian Brainrot | ITALIANROT | à vérifier | à vérifier (sommet le 2025-05-23) | ≈ 15 M$, 2025-05-23 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `italian-brainrot` ; https://www.coingecko.com/en/coins/italian-brainrot |
| 454 | Jean Phil | JEANPHIL | à vérifier | oct. 2026 | ≈ 15 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 384 ; CG `jean-phil` |
| 455 | Loaf Token | LOAF | à vérifier | août 2025 | ≈ 15 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 379 ; CG `loaf-token` |
| 456 | LUCKY | LUCKY | à vérifier | nov. 2025 | ≈ 15 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 370 ; CG `lucky` |
| 457 | Real World AI | RWA | à vérifier | janv. 2025 | ≈ 15 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 372 ; CG `real-world-ai` |
| 458 | Agrippa | AGRIPPA | à vérifier | à vérifier (sommet le 2026-09-25) | ≈ 14 M$, 2026-09-25 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `agrippa` ; https://www.coingecko.com/en/coins/agrippa |
| 459 | Barking Puppy | BP | à vérifier | févr. 2026 | ≈ 14 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 383 ; CG `barking-puppy` |
| 460 | Jotchua | JOTCHUA | à vérifier | juin 2026 | ≈ 14 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 385 ; CG `jotchua` |
| 461 | Nya | NYA | Avalanche | 2024 | ≈ 14 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 517 ; CG `nya` |
| 462 | Stairway to gold | GOLD | à vérifier | oct. 2026 | ≈ 14 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 386 ; CG `stairway-to-gold` |
| 463 | The Original Doge | OGDOGE | à vérifier | juin 2026 | ≈ 14 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 381 ; CG `the-original-doge` |
| 464 | 雪球 (Snowball) | 雪球 | BNB Chain | janv. 2026 | ≈ 14 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare |  | à définir | v1 n° 802 ; CG `xuequi` |
| 465 | 1000PEPPER | 1000PEPPER | à vérifier | janv. 2026 | ≈ 13 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 389 ; CG `1000pepper` |
| 466 | ALD | ALD | à vérifier | août 2026 | ≈ 13 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 390 ; CG `ald` |
| 467 | ALLINDOGE | ALLINDOGE | à vérifier | août 2025 | ≈ 13 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 395 ; CG `allindoge` |
| 468 | BEARXRPL | BEAR | à vérifier | févr. 2025 | ≈ 13 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 391 ; CG `bearxrpl` |
| 469 | BORED | BORED | à vérifier | avr. 2024 | ≈ 13 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 396 ; CG `edison-bored` |
| 470 | GongFu | GF | à vérifier | oct. 2026 | ≈ 13 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 392 ; CG `gongfu` |
| 471 | SCHIFFY | SCHIFFY | à vérifier | sept. 2026 | ≈ 13 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 403 ; CG `schiffy` |
| 472 | Z李REAL SUPER COIN | ZREAL | à vérifier | janv. 2026 | ≈ 13 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 388 ; CG `zreal-super-coin` |
| 473 | dopameme | DOPAMEME | à vérifier | août 2026 | ≈ 12 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 398 ; CG `dopameme-2` |
| 474 | PEPECAT | PEPECAT | à vérifier | juin 2025 | ≈ 12 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 402 ; CG `pepecat-2` |
| 475 | Quq | QUQ | BNB Chain | 21/03/2025 | ≈ 12 M$ (22/03/2025) | estimé | en déclin (≈ 1,6 M$, mais volume farmé énorme) | Mème emoji « quq » ; en oct. 2025 il était n° 1 en volume sur BNB (354 M$/24 h) pour seulement 2,7 M$ de valorisation. | rare | rare |  | à définir | r3 ; https://atomicwallet.io/academy/articles/top-5-bnb-chain-memecoins-october-2025-season ; https://coinmarketcap.com/currencies/quq/ |
| 476 | Strategy Coin | STRATEGY | à vérifier | sept. 2026 | ≈ 12 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 393 ; CG `strategy-coin` |
| 477 | ༼ つ ◕_◕ ༽つ | GIB | à vérifier | mars 2026 | ≈ 12 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 410 ; CG `_` |
| 478 | Baby Floki | BABYFLOKI | BSC | sept. 2021 | ≈ 11,9 M$ en FDV (01/11/2021) | estimé | en déclin | Jeton né du chien Floki d'Elon Musk (tweet du 25/06/2021) sur BSC, lancé en sept. 2021 ; pic vers le 01/11/2021 ; aujourd'hui -98,71 %. | rare | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/baby-floki/ |
| 479 | Garlicoin | GRLC | Garlicoin (fork de Litecoin) | 2018 | ≈ 11,8 M$, 13/05/2021 (≈ 1,5 M$ le 01/02/2018) | sourcé | en déclin (0,52 M$ le 06/11/2026) | Garlicoin : mème culte de 2018 (pain à l'ail) | rare | rare |  | à définir | v1 n° 623 ; correction r1 ; CG `garlicoin` ; https://coinmarketcap.com/currencies/garlicoin/historical-data/ |
| 480 | Paper Plane | PLANE | TON | à vérifier (sommet le 17 avr. 2024) | ≈ 11,6 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation | estimé | en déclin | L'avion en papier du logo Telegram, mème TON, record avril 2024, -97,6 %. | rare | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/paper-plane |
| 481 | Claudia | CLAUDIA | à vérifier | oct. 2026 | ≈ 11 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 406 ; CG `claudia-2` |
| 482 | FATCAT | FATCAT | à vérifier | nov. 2026 | ≈ 11 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 407 ; CG `fatcat-4` |
| 483 | LOULOU | LOULOU | à vérifier | oct. 2024 | ≈ 11 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 399 ; CG `loulou` |
| 484 | WolfSafePoorPeople | WSPP | à vérifier | oct. 2026 | ≈ 11 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 409 ; CG `wolfsafepoorpeople` |
| 485 | what the hook? | WTH | à vérifier | oct. 2026 | ≈ 10 M$ (estimé CG) | estimé | actif |  | rare | rare |  | à définir | v1 n° 416 ; CG `what-the-hook` |
| 486 | 中国人能飞火箭 | 中国人能飞 | à vérifier | sept. 2026 | ≈ 10 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° 417 ; CG `zhong-guo-ren-neng-fei` |
| 487 | ShibaDoge | SHIBDOGE | à vérifier | juil. 2022 | ≈ 12769,26 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare |  | à définir | v1 n° 742 ; CG `shibadoge` |
| 488 | BNB Tiger OG | BNBTIGEROG | à vérifier | oct. 2023 | ≈ 3351,98 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare |  | à définir | v1 n° 565 ; CG `bnbtiger` |
| 489 | Pitbull | PIT | à vérifier | août 2021 | ≈ 5,81 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare |  | à définir | v1 n° 713 ; CG `pitbull` |
| 490 | Anon Inu | AINU | à vérifier | juil. 2021 | ≈ 5,18 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | mort |  | commune | rare |  | à définir | v1 n° 539 ; CG `anon-inu` |
| 491 | AI XOVIA | AIX | à vérifier | août 2025 | ≈ 4,50 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare |  | à définir | v1 n° 531 ; CG `ai-xovia` |
| 492 | YooShi | YOOSHI | à vérifier | oct. 2021 | ≈ 4,19 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare |  | à définir | v1 n° 798 ; CG `yooshi` |
| 493 | Pups † | PUPS | Bitcoin | 2024 | ≈ 3,87 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare |  | à définir | v1 n° 722 ; CG `rune-pups` |
| 494 | Pig Finance | PIG | BSC | janv. 2021 | ≈ 3,70 Md$ en FDV (10/05/2021) — estimation aberrante, à vérifier | estimé | mort | Fork reflection de SafeMoon à mascotte cochon sur BSC ; au sommet de la vague SafeMoon le 10/05/2021, CMC affichait plus de 1 Md$ de volume quotidien (douteux) ; aujourd'hui -99,6 %. | commune | épique |  | à définir | r2 ; https://coinmarketcap.com/currencies/pig-finance/ |
| 495 | PEPPER | PEPPER | à vérifier | oct. 2024 | ≈ 2,56 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare |  | à définir | v1 n° 711 ; CG `pepper` |
| 496 | Capybara Nation | BARA | à vérifier | nov. 2024 | ≈ 2,21 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare |  | à définir | v1 n° 573 ; CG `capybara-nation` |
| 497 | Rosa Inu | ROSA | à vérifier | juil. 2024 | ≈ 2,20 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare |  | à définir | v1 n° 734 ; CG `rosa-inu` |
| 498 | Kishu Inu | KISHU | Ethereum | 2021 | ≈ 1,69 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | Kishu Inu : « tueur de Doge » de 2021, pic estimé fragile | commune | épique |  | à définir | v1 n° 657 ; CG `kishu-inu` |
| 499 | CorgiAI | CORGIAI | à vérifier | mars 2024 | ≈ 1,53 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | épique |  | à définir | v1 n° 33 ; CG `corgiai` |
| 500 | Bezoge Earth | BEZOGE | Ethereum | mai 2021 | ≈ 1,52 Md$ en FDV (22/11/2021) — estimation aberrante, à vérifier | estimé | mort | Mème Jeff Bezos + Doge sur Ethereum (mai 2021) ; pic le 22/11/2021, ≈ 1,5 Md$ en FDV sur 100 billiards de jetons (≈ 40 % en circulation, donc capitalisation réelle plus faible) ; aujourd'hui -99,98 %. | commune | épique | personne réelle | à définir | r2 ; https://coinmarketcap.com/currencies/bezoge-earth/ |
| 501 | Ape and Pepe | APEPE | à vérifier | nov. 2024 | ≈ 1,45 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin |  | commune | épique |  | à définir | v1 n° 18 ; CG `ape-and-pepe` |
| 502 | catwifhat | CWIF | Solana | 2024 | ≈ 1,4 Md$ (estimation CoinGecko de l'annexe 3) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | légendaire |  | à définir | v1 n° 577 ; correction r3 ; CG `catwifhat-2` |
| 503 | Samoyedcoin † | SAMO | Solana | 2021 | ≈ 1,36 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare |  | à définir | v1 n° 736 ; CG `samoyedcoin` |
| 504 | Solid X | SOLIDX | à vérifier | juin 2024 | ≈ 1,14 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare |  | à définir | v1 n° 757 ; CG `solid-x` |
| 505 | OSK | OSK | à vérifier | févr. 2022 | ≈ 1,05 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | épique |  | à définir | v1 n° 19 ; CG `osk` |
| 506 | CAT | CAT | Avalanche | déc. 2021 (ajout CMC) | ≤ 99 M$ en FDV (2 janv. 2022) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | CAT, mème chat d'Avalanche apparu fin 2021, quand la chaîne vivait sa première saison de mèmes ; sorti du classement CMC en avril 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/cat/ ; https://coinmarketcap.com/historical/20220102/ |
| 507 | catwifbag | BAG | Solana | mars 2024 | ≈ 99 M$ (25 mars 2024) | estimé | mort | Chat avec un sac, variante de la mode des « wif » ; ~99 M$ le 25/03/2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/catwifbag/ ; https://dexscreener.com/solana/D8r8XTuCrUhLheWeGXSwC3G92RhASficV3YA7B2XWcLv |
| 508 | Doge Token | DOGET | à vérifier | mai 2019 | ≈ 98,5 M$ (09/05/2021) | sourcé | mort | Doge Token (DOGET), « version verte » de Dogecoin lancée en 2019 ; ≈ 98,5 M$ de capitalisation le 09/05/2021, au lendemain du passage de Musk au SNL ; plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/doge-token/ |
| 509 | Shibnobi | SHINJA | Ethereum | nov. 2021 | ≈ 98,1 M$ (21/11/2021) | sourcé | mort | Clone SHIB « ninja » sur Ethereum (nov. 2021) ; ≈ 98 M$ (CMC) trois jours après son listing, puis migration en V2 et déclin. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/shibnobi/ |
| 510 | BUBCAT | BUB | BNB Chain | avr. 2024 (ajout CMC) | ≈ 92 M$ (8 déc. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Chat BUB de BSC, monté à près de 100 M$ début déc. 2024 avant de sortir du classement CMC un mois plus tard. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/bubcat/ ; https://coinmarketcap.com/historical/20241208/ |
| 511 | Rizzmas | RIZZMAS | Solana | Noël 2024 | ≈ 91 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 731 ; CG `rizzmas` |
| 512 | MEMDEX100 | MEMDEX | à vérifier | févr. 2025 | ≈ 90 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 187 ; CG `memdex100` |
| 513 | Sponge | SPONGE | Ethereum | 04/05/2023 | ≈ 90 M$ (08/05/2023) | sourcé | mort | Jeton Bob l'éponge sans prévente : de 2 M$ à 90 M$ en quatre jours en pleine folie Pepe, puis chute. | commune | rare |  | à définir | r3 ; https://bitcoinist.com/sponge-goes-from-2m-to-90m-market-cap-in-four-days-learn-why-this-is-the-new-pepe-in-town/amp/ ; https://www.coingecko.com/en/coins/sponge-2 |
| 514 | Chomp | CHOMP | Base | juin 2024 | ≈ 89 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 582 ; CG `chompcoin` |
| 515 | Banano † | BAN | Banano (fork de Nano) | 2018 | ≈ 88 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 551 ; CG `banano` |
| 516 | Dontplaywithkitty | DPK | BNB Chain | oct. 2021 (ajout CMC) | ≤ 88 M$ en FDV (14 nov. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Mème chat (« ne joue pas avec le chaton ») de la fin 2021 sur BSC ; plus coté après mars 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/dontplaywithkitty/ ; https://coinmarketcap.com/historical/20211114/ |
| 517 | SHKOOBY INU | SHKOOBY | Ethereum | nov. 2021 | ≈ 87,1 M$ en FDV (07/11/2021) | estimé | mort | Jeton « Inu » parodie de Scooby-Doo sur Ethereum, lancé en nov. 2021 ; pic vers le 07/11/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/shkooby-inu/ |
| 518 | Base God | TYBG | à vérifier | mars 2024 | ≈ 86 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 185 ; v1 n° 558 ; CG `base-god` |
| 519 | Tipinu | TIPINU | BNB Chain | oct. 2021 (ajout CMC) | ≤ 86 M$ en FDV (7 nov. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Inu « pourboire » d'oct. 2021 sur BSC ; coté deux mois puis abandonné. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/tipinu/ ; https://coinmarketcap.com/historical/20211107/ |
| 520 | 客服小何 (Customer Xiaohe) | KEFU | BNB Chain | oct. 2025 | ≈ 86 M$ (08/10/2025, ATH CMC × 1 Md ; BingX cite 349 M$, non confirmé) | estimé | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 800 ; correction r3 ; https://coinmarketcap.com/currencies/kefuxiaohe/ ; https://bingx.com/en/learn/article/bnb-meme-season-key-metrics-and-what-you-need-to-know |
| 521 | Doge Eat Doge | OMNOM | Dogechain | août 2022 (ajout CMC) | ≈ 85 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle (CMC ne publie qu'à partir de plus tard : ≈ 31 M$ le 10 nov. 2024) | estimé | mort | OMNOM, le premier grand mème de Dogechain (août 2022) ; ≈ 31 M$ selon CMC en nov. 2024, -99,9 % depuis. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/doge-eat-doge/ ; https://www.coingecko.com/en/coins/doge-eat-doge |
| 522 | Gen Z Quant | QUANT | Solana (pump.fun) | 19 nov. 2024 | ≈ 85 M$ (20 nov. 2024) | sourcé | mort (≈ 0,11 M$) | Un adolescent vend tout en direct pour 30 k$, puis la foule fait monter le jeton à 85 M$ par vengeance. | commune | épique | arnaque avérée | à définir | r3 ; https://decrypt.co/292594/this-child-made-30k-rugging-a-solana-meme-coin-then-crypto-degens-got-revenge ; https://www.coingecko.com/en/coins/gen-z-quant |
| 523 | Rare Pepe Cash † | PEPECASH | Counterparty (Bitcoin) | 2016 | ≈ 84 M$, 07/01/2018 | sourcé | mort (absent de CoinGecko) | Rare Pepe Cash : premiers mèmes en NFT (Counterparty, 2016) | commune | rare |  | à définir | v1 n° 724 ; correction r1 ; https://coinmarketcap.com/historical/20180107/ ; https://rightclicksave.com/article/a-brief-history-of-rare-pepe |
| 524 | Scrat | SCRAT | Solana | juin 2024 | ≈ 84 M$ (25 juin 2024) | estimé | mort | L'écureuil de « L'Âge de glace » ; ~84 M$ fin juin 2024, quelques jours après son lancement. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/scrat/ ; https://dexscreener.com/solana/3GEznP41VaAGv9yRdBiuYdA8zkffNc8b7DzNJgFbH4Kh |
| 525 | SHIBA BSC | SHIBSC | à vérifier | mai 2021 | ≈ 84 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 212 ; CG `shiba-bsc` |
| 526 | DogeVerse | DOGEVERSE | Ethereum (multichaîne) | 05/06/2024 | ≈ 83 M$ (08/06/2024) | estimé | mort | Prévente Doge multichaîne de 2024, sommet trois jours après la cotation, puis dégringolade. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/dogeverse ; https://dexscreener.com/ethereum/0x62F03b52c377FeA3EB71D451a95ad86C818755D1 |
| 527 | POOH | POOH | à vérifier | à vérifier (sommet le 2023-05-06) | ≈ 82 M$, 2023-05-06 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `pooh` ; https://www.coingecko.com/en/coins/pooh |
| 528 | Pepe on SOL | PEPE | à vérifier | mai 2024 | ≈ 81 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 211 ; CG `pepe-sol` |
| 529 | Dolos The Bully | BULLY | Solana | Agents d'IA, janv. 2025 | ≈ 80 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 166 ; correction r3 ; CG `dolos-the-bully` |
| 530 | Luminous | LUM | Base | nov. 2024 | ≈ 80 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 220 ; correction r3 ; CG `luminous` |
| 531 | PolyDoge | POLYDOGE | Polygon | 2021 | ≈ 80 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 715 ; CG `polydoge` |
| 532 | Ansem's Cat | HOBBES | Solana | avr. 2024 | ≈ 79 M$ (3 avr. 2024) | estimé | mort | « Le chat d'Ansem », l'influenceur Solana ; ~79 M$ le jour du lancement (03/04/2024), puis -99,9 %. | commune | rare | personne réelle | à définir | r3 ; https://coinmarketcap.com/currencies/ansems-cat/ ; https://dexscreener.com/solana/6n7Janary9fqzxKaJVrhL9TG2F61VbAtwUMu1YZscaQS |
| 533 | Costco Hot Dog | COST | Solana | avr. 2024 | ≈ 79 M$ (10 avr. 2024) | estimé | mort | Le hot-dog à 1,50 $ de Costco ; ~79 M$ le jour du lancement (10/04/2024). | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/costco-hot-dog/ ; https://dexscreener.com/solana/Av6qVigkb7USQyPXJkUvAEm4f599WTRvd75PUWBA9eNm |
| 534 | Ping | PING | à vérifier | à vérifier (sommet le 2025-10-25) | ≈ 79 M$, 2025-10-25 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `ping` ; https://www.coingecko.com/en/coins/ping |
| 535 | Catana | CATANA | Solana (pump.fun) | oct. 2024 | ≈ 78 M$ (date inconnue) | estimé | mort (≈ 61 k$, volume nul) | Chat au sabre abandonné par son créateur, relancé par la communauté, puis oublié. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/catana ; https://dexscreener.com/solana/3oefnixw6csxtymen7wtcjeeaivgsabniwcmgqczb6ik |
| 536 | GOUT | GOUT | à vérifier | nov. 2024 | ≈ 77 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 237 ; CG `gout` |
| 537 | FedoraCoin | TIPS | blockchain propre | déc. 2013 | ≈ 76,7 M$, 07/12/2017 (CMC, relevé quotidien) | sourcé | mort | Mème du fedora (« m'lady ») pour les pourboires Reddit ; ≈ 2,5 M$ en janv. 2014, ressorti à ≈ 77 M$ en déc. 2017, puis échangé contre « Fedora Gold ». | commune | rare |  | à définir | r1 ; https://coinmarketcap.com/currencies/fedoracoin/historical-data/ |
| 538 | Hosico Cat | HOSICO | Solana | juil. 2025 | ≈ 75 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | commune | rare |  | à définir | v1 n° 226 ; correction r3 ; CG `hosico-cat` |
| 539 | SafeMoon Inu | SMI | à vérifier | oct. 2021 | ≈ 73 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 174 ; CG `safemoon-inu` |
| 540 | AEROBUD | AEROBUD | Base | mai 2024 | ~72,9 M$ (date inconnue) | estimé | mort | Chien mascotte « charity » né autour d'Aerodrome en mai 2024, il est tombé à 0,47 M$. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/aerobud |
| 541 | Forgive Me Father | PURGE | NEAR | juil. 2025 | ≈ 71 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 206 ; CG `forgive-me-father` |
| 542 | Sillynubcat | NUB | Solana | 2024 | ≈ 71 M$ (24 avr. 2024) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 745 ; correction r3 ; CG `sillynubcat` ; https://coinmarketcap.com/currencies/nubcat/ |
| 543 | Snowdog | SDOG | Avalanche | nov. 2021 | ≈ 70,9 M$ en FDV (21/11/2021) | estimé | mort | Premier memecoin d'Avalanche (nov. 2021), fork d'Olympus monté jusqu'à ~54 000 $ le jeton lors du rachat, puis -90 % en un jour ; jusqu'à 30 M$ de pertes, rug documenté que l'équipe conteste. | commune | épique | arnaque avérée | à définir | r2 ; https://rekt.news/snowdog-rekt ; https://cryptoslate.com/avalanches-first-memecoin-sdog-ends-in-a-30m-rugpull/ |
| 544 | Ani | ANI | Solana | Juillet 2025 | ≈ 70 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 183 ; correction r3 |
| 545 | Moutai | MOUTAI | Solana | avr. 2024 | ≈ 70 M$ (14 avr. 2024) | estimé | mort | Mème de l'alcool chinois Kweichow Moutai, porté par la communauté sinophone ; ~70 M$ mi-avril 2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/moutai/ ; https://dexscreener.com/solana/45EgCwcPXYagBC7KqBin4nCFgEZWN7f3Y6nACwxqMCWX |
| 546 | Wakanda Inu | WKD | Ethereum | nov. 2021 | ≈ 69,0 M$ en FDV (11/11/2021) | estimé | mort | Jeton « Inu » à thème Wakanda (Black Panther) sur Ethereum, lancé en nov. 2021 ; pic vers le 11/11/2021 ; aujourd'hui -99,97 %. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/wakanda-inu/ |
| 547 | Nailong | NAILONG | Solana | oct. 2024 | ≈ 68 M$ (≈ 16 nov. 2024) | estimé | mort (≈ 0,12 M$) | Dragon jaune des mèmes chinois ; il monte à l'automne 2024, puis disparaît. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/nailong ; https://coincodex.com/crypto/nailong |
| 548 | Goku | GOKU | Ethereum | août 2021 | ≈ 67,6 M$ en FDV (02/11/2021) | estimé | mort | Jeton à thème Dragon Ball sur Ethereum, lancé en août 2021 ; pic vers le 02/11/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/goku/ |
| 549 | Donkey (DONKEY_BSC_MEME) | DONKEY | BNB Chain | mai 2025 (ajout CMC) | ≈ 67 M$ (24 août 2025) ; CMC, relevé hebdomadaire | sourcé | mort | « Donkey », mème âne BSC de mai 2025 passé par ≈ 67 M$ fin août 2025, puis mort. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/donkey-bsc/ ; https://www.coingecko.com/en/coins/donkey-2 |
| 550 | Doggy | DOGGY | à vérifier | oct. 2021 | ≈ 66 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 604 ; CG `doggy` |
| 551 | DUKO | DUKO | Solana | févr. 2024 | ≈ 66 M$ (24 mars 2024) | estimé | mort | Chien lancé mi-février 2024 ; il touche ~66 M$ le 24/03/2024, pendant la folie des préventes. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/duko/ ; https://dexscreener.com/solana/HLptm5e6rTgh4EKgDpYFrnRHbjpkMyVdEeREEa2G7rf9 |
| 552 | EvilSquidGame | EVILSQUID | BSC | nov. 2021 | ≈ 66,0 M$ en FDV (20/11/2021) | estimé | mort | Jeton de la vague Squid Game (automne 2021) sur BSC, lancé en nov. 2021 ; pic vers le 20/11/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/evilsquidgame/ |
| 553 | ROCKY | ROCKY | Base | avr. 2024 | ~64,2 M$ (date inconnue) | estimé | mort | Chien de la saison Base 2024, à 0 $ de volume, il pèse 0,13 M$ (pic à confirmer : possible mèche). | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/rocky-on-base |
| 554 | Anita Max Wynn | WYNN | Solana | janv. 2024 | ≈ 64 M$ (21 janv. 2024) | estimé | mort | « Anita Max Wynn », l'alter ego de Drake devenu mème ; ~64 M$ en janvier 2024. | commune | rare | personne réelle | à définir | r3 ; https://coinmarketcap.com/currencies/anita-max-wynn/ ; https://dexscreener.com/solana/4vqYQTjmKjxrWGtbL2tVkbAU1EVAz9JwcYtd2VE3PbVU |
| 555 | Guacamole | GUAC | à vérifier | à vérifier (sommet le 2024-03-08) | ≈ 64 M$, 2024-03-08 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `guacamole` ; https://www.coingecko.com/en/coins/guacamole |
| 556 | SelfieDogCoin | SELFIE | Solana | 2024-2025 | ≈ 64 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 738 ; CG `selfiedogcoin` |
| 557 | Gizmo | GIZMO | Bitcoin (Runes) | 2024 | ≈ 63 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 629 ; CG `gizmo-imaginary-kitten-runes` |
| 558 | BabyCake | BC2.1 | BSC | juil. 2021 | ≈ 62,8 M$ en FDV (22/07/2021) | estimé | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs), versant des CAKE sur BSC, lancé en juil. 2021 ; pic vers le 22/07/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/baby-cake/ |
| 559 | Anon | ANON | Base | fin 2024 | ≈ 62 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | commune | rare |  | à définir | v1 n° 256 ; correction r3 ; CG `super-anon` |
| 560 | Dupe | DUPE | à vérifier | mai 2025 | ≈ 62 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 236 ; CG `dupe` |
| 561 | Bonk On Base | BONK | Base | avr. 2024 | ~61,3 M$ (date inconnue) | estimé | mort | Copie de BONK sur Base en avril 2024 (différente du BONK Solana du catalogue), elle vaut 70 k$. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/bonk-on-base ; https://dexscreener.com/base/0x176567c44342EDda7AAE629f7CECaB246f22F69a |
| 562 | Spore | SPORE | Avalanche / BNB Chain | à vérifier (sommet le 30 avr. 2021) | ≈ 61 M$ (avr. 2021) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Spore, mème « NFT » lancé sur Avalanche et BSC, parti en flèche fin avril 2021 ; -99,6 % depuis. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/spore |
| 563 | Luigi Mangione | LUIGI | Solana (pump.fun) | 9 déc. 2024 | ≈ 60-77 M$ (10 déc. 2024) | sourcé | mort (≈ 0,23 M$) | Jeton lancé le jour de l'arrestation du suspect du meurtre du PDG d'UnitedHealthcare ; il s'effondre en quelques jours. | commune | rare | personne réelle | à définir | r3 ; https://crypto.news/after-murder-arrest-luigis-market-cap-climbs-to-60m/ ; https://news.bitcoin.com/luigi-mangione-gains-memecoin-infamy |
| 564 | SAD HAMSTER | HAMMY | Solana | mai 2024 | ≈ 60 M$ (17 mai 2024) | estimé | mort | Le hamster triste des vidéos TikTok ; ~60 M$ en mai 2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/sad-hamster/ ; https://dexscreener.com/solana/26KMQVgDUoB6rEfnJ51yAABWWJND8uMtpnQgsHQ64Udr |
| 565 | Shikoku | SHIK | à vérifier | à vérifier (sommet le 2023-01-04) | ≈ 59 M$, 2023-01-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `shikoku` ; https://www.coingecko.com/en/coins/shikoku |
| 566 | Tiger King | TKING | à vérifier | oct. 2021 | ≈ 59 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 215 |
| 567 | Zelda Inu | ZLDA | BSC | janv. 2022 | ≈ 58,4 M$ en FDV (10/01/2022) | estimé | mort | Jeton « Inu » à thème Zelda sur BSC, lancé en janv. 2022 ; pic vers le 10/01/2022 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/zelda-inu/ |
| 568 | Basenji | BENJI | Base | juin 2024 | ≈ 57 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 217 ; correction r3 ; CG `basenji` |
| 569 | Woman Yelling at Cat | WYAC | Solana (à vérifier) | fin 2024 | ≈ 57 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 794 ; CG `woman-yelling-at-cat` |
| 570 | Boomer | BOOMER | Base | mars 2024 | ~56,6 M$ (date inconnue) | estimé | mort | Wojak « boomer » de la saison Base du printemps 2024, cité dans les rallyes Base de juin 2024 avec BRETT et KEYCAT, il vaut 160 k$. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/boomer ; https://www.fxstreet.com/cryptocurrencies/news/base-meme-coins-rally-leave-solana-based-daddy-tate-to-bite-the-dust-202406162200 |
| 571 | Gui Inu | GUI | Aptos | à vérifier (sommet le 16 mars 2024) | ≈ 56,3 M$ (mars 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Le « mème OG » d'Aptos, lancé déc. 2023 : valorisation x7 en mars 2024, record le 16 mars, puis -99,9 %. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/gui-inu ; https://www.gncrypto.news/news/the-surge-of-meme-coins-you-may-have-overlooked/ |
| 572 | DYZilla | DYZILLA | à vérifier | déc. 2022 | ≈ 55 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 203 ; CG `dyzilla` |
| 573 | Habibi (Sol) | HABIBI | Solana | mars 2024 | ≈ 55 M$ (22 mai 2024) | estimé | mort (≈ 54 k$) | Chat mème du printemps 2024, monté à 55 M$ en deux mois, puis éteint. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/habibi-sol ; https://dexscreener.com/solana/2ukgjdc99nk34rfrjwjcohauqltlnz8tlcbrdqk3f2ay |
| 574 | Lets Go Brandon | LETSGO | à vérifier | à vérifier (sommet le 2022-03-02) | ≈ 55 M$, 2022-03-02 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare | politique | à définir | R5 C1 `lets-go-brandon` ; https://www.coingecko.com/en/coins/lets-go-brandon |
| 575 | SEIYAN | SEIYAN | Sei | à vérifier (sommet le 1 janv. 2024) | ≈ 55 M$ (janv. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Seiyan, le premier mème de Sei (fin 2023, jeu de mots Saiyan) ; pic le 1er janv. 2024. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/seiyan |
| 576 | Brainlet | BRAINLET | à vérifier | 2024 (à vérifier) | ≈ 54 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 572 ; CG `brainlet-2` |
| 577 | Sharpei | SHAR | Solana | 23 oct. 2024 | ≈ 54 M$ (23 oct. 2024) | sourcé | mort (absent de DexScreener) | Un lot de plus de 100 portefeuilles vend 60 % de l'offre d'un coup, environ 3,4 M$ empochés. | commune | rare | arnaque avérée | à définir | r3 ; https://decrypt.co/288160/solana-meme-coin-sharpei-epic-rug-pull |
| 578 | Moonshot | MSHOT | BSC | mars 2021 | ≈ 53,6 M$ en FDV (12/05/2021) | estimé | mort | Fork de SafeMoon sur BSC qui a affolé les réseaux en mai 2021 malgré une capitalisation affichée de 11 430 $ par CMC selon InvestorPlace ; pic le 12/05/2021, plus coté. | commune | rare |  | à définir | r2 ; https://investorplace.com/2021/05/moonshot-crypto-11-things-to-know-about-the-new-token-driving-social-media-chatter/ ; https://coinmarketcap.com/currencies/moonshot/ |
| 579 | Bitcoin20 | BTC20 | Ethereum | 10/08/2023 | ≈ 53 M$ (16/08/2023) | estimé | mort | Prévente « Bitcoin version ERC-20 » de 21 M jetons, pic la première semaine, puis plus rien. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/bitcoin20 ; https://dexscreener.com/ethereum/0xE86DF1970055e9CaEe93Dae9B7D5fD71595d0e18 |
| 580 | Deez Nuts | DEEZNUTS | BNB Chain | mai 2021 (ajout CMC) | ≤ 53 M$ en FDV (6 juin 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Mème potache de la saison SafeMoon (mai 2021), un des jetons « reflection » listés à la hâte par CMC ; disparu du classement début 2022. | commune | commune | obscène | à définir | r4 ; https://coinmarketcap.com/currencies/deez-nuts/ ; https://coinmarketcap.com/historical/20210606/ |
| 581 | Andy BSC | ANDY | BNB Chain | janv. 2025 (ajout CMC) | ≈ 52 M$ (26 janv. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Copie BSC d'Andy (le compagnon de Pepe dans Boys' Club), janv. 2025 ; ≈ 50 M$ fin janv. puis effondrement. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/andytoken-bsc/ ; https://www.coingecko.com/en/coins/andy-4 |
| 582 | Kasper | KASPER | Kaspa (KRC-20) | à vérifier (sommet le 21 oct. 2024) | ≈ 52 M$ (oct. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Kasper, fantôme mascotte, un des premiers mèmes KRC-20 au lancement de Kasplex (sept. 2024) ; pic le 21 oct. 2024. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/kasper |
| 583 | 財務自由 (Liberté financière) | 財務自由 | BNB Chain | 08/10/2025 | ≈ 52 M$ (09/10/2025) | estimé | mort (≈ 66 k$) | Slogan chinois « liberté financière » de la saison des mèmes en chinois ; 52 M$ en un jour, puis quasi zéro. | commune | rare |  | à définir | r3 ; https://bingx.com/en/learn/article/bnb-meme-season-key-metrics-and-what-you-need-to-know ; https://coinmarketcap.com/currencies/caiwuziyou/ |
| 584 | SpaceGrime | GRIMEX | BSC | mai 2021 | ≈ 51,5 M$ en FDV (30/10/2021) | estimé | mort | Mème Grimes + SpaceX sur BSC, lancé en mai 2021 ; pic vers le 30/10/2021 ; aujourd'hui plus coté. | commune | rare | personne réelle | à définir | r2 ; https://coinmarketcap.com/currencies/spacegrime/ |
| 585 | Ski Mask Cat | SKICAT | Base | nov. 2024 | ~51,1 M$ (date inconnue) | estimé | mort | Version chat de Ski Mask Dog, à la fin 2024, elle vaut 79 k$ (pic à confirmer : possible mèche). | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/ski-mask-cat |
| 586 | Any Inu | AI | à vérifier | à vérifier (sommet le 2024-03-04) | ≈ 51 M$, 2024-03-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `any-inu` ; https://www.coingecko.com/en/coins/any-inu |
| 587 | The Next 100x Memecoin on Base | TN100X | Base | févr. 2024 | ~50,6 M$ (date inconnue) | estimé | mort | Jeton de l'écosystème Farcaster qui s'appelait lui-même « le prochain x100 », il ne pèse plus que 39 k$. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/tn100x ; https://dexscreener.com/base/0x6B93950a9B589Bc32B82a5df4e5148f98A7FAe27 |
| 588 | Hina Inu | HINA | Ethereum | mai 2021 | ≈ 50,3 M$ en FDV (23/10/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en mai 2021 ; pic vers le 23/10/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/hina-inu/ |
| 589 | AVAX Lambo | LAMBO | Avalanche | juin 2025 | ≈ 50 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 234 |
| 590 | Kimbo | KIMBO | Avalanche | 2024 | ≈ 50 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | commune | rare |  | à définir | v1 n° 306 ; CG `kimbo` |
| 591 | Shina Inu | SHI | à vérifier | févr. 2023 | ≈ 50 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 189 ; CG `shina-inu` |
| 592 | TON FISH MEMECOIN | FISH | à vérifier | à vérifier (sommet le 2024-03-17) | ≈ 50 M$, 2024-03-17 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `ton-fish-memecoin` ; https://www.coingecko.com/en/coins/ton-fish-memecoin |
| 593 | WenMoon | WENMOON | BNB Chain | avr. 2021 (ajout CMC) | ≤ 50 M$ en FDV (25 avr. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | « Wen moon ? », la question rituelle des détenteurs, transformée en jeton reflection BSC en avril 2021 ; sorti du classement à l'automne 2021. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/wenmoon/ ; https://coinmarketcap.com/historical/20210425/ |
| 594 | Shakita Inu | SHAK | BSC | août 2021 | ≈ 49,7 M$ en FDV (29/10/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en août 2021 ; pic vers le 29/10/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/shakita-inu/ |
| 595 | Shiba Floki Inu | FLOKI | BSC | juin 2021 | ≈ 49,5 M$ en FDV (06/10/2021) | estimé | mort | Né du tweet de Musk sur son chien Floki (25/06/2021) : +1 309 % en trois heures selon CoinGecko ; pic en oct. 2021, puis mort. À ne pas confondre avec Floki Inu. | commune | rare |  | à définir | r2 ; https://forklog.com/en/shiba-floki-token-jumps-about-1300-after-elon-musks-latest-tweet/ ; https://coinmarketcap.com/currencies/shiba-floki/ |
| 596 | Pigcoin | PIG | Polygon | avr. 2024 (ajout CMC) | ≤ 49 M$ en FDV (21 avr. 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Cochon de Polygon, avril 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/pigcoin/ ; https://coinmarketcap.com/historical/20240421/ |
| 597 | Trog | TROG | à vérifier | à vérifier (sommet le 2024-06-05) | ≈ 49 M$, 2024-06-05 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `trog` ; https://www.coingecko.com/en/coins/trog |
| 598 | Pissing Cat | PEECAT | Ethereum | sept. 2021 | ≈ 48,8 M$ en FDV (24/07/2022) | estimé | mort | Mème chat sur Ethereum, lancé en sept. 2021 ; pic vers le 24/07/2022 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/pissing-cat/ |
| 599 | Apetos | APE | Aptos | à vérifier (sommet le 4 oct. 2024) | ≈ 48,1 M$ (oct. 2024) ; ATH CoinGecko × offre totale | estimé | mort | Singe « Ape + Aptos » des parieurs d'Aptos, record oct. 2024, plus de volume. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/apetos |
| 600 | AVAX Has No Chill | NOCHILL | Avalanche | 2024 | ≈ 48 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | commune | rare |  | à définir | v1 n° 498 ; CG `avax-has-no-chill` |
| 601 | Bagwork | BAGWORK | Solana (pump.fun) | sept. 2025 | ≈ 48 M$ (date inconnue) | estimé | mort (≈ 82 k$) | Mème du « travail pour le sac » de la fin 2025 sur pump.fun, retombé à presque zéro. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/bagwork ; https://dexscreener.com/solana/fbzsqpaygqjpmrt8l33qngwv6bcatx6xcjmtpvcw3gdz |
| 602 | Chickencoin | CHKN | à vérifier | à vérifier (sommet le 2024-04-02) | ≈ 48 M$, 2024-04-02 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `chickencoin` ; https://www.coingecko.com/en/coins/chickencoin |
| 603 | GoldenBoys | GOLD | à vérifier | à vérifier (sommet le 2024-07-28) | ≈ 48 M$, 2024-07-28 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `goldenboys` ; https://www.coingecko.com/en/coins/goldenboys |
| 604 | Terminus | TERMINUS | à vérifier | à vérifier (sommet le 2024-09-23) | ≈ 48 M$, 2024-09-23 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `terminus-2` ; https://www.coingecko.com/en/coins/terminus-2 |
| 605 | The Balkan Dwarf | KEKEC | à vérifier | à vérifier (sommet le 2024-11-06) | ≈ 48 M$, 2024-11-06 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `the-balkan-dwarf` ; https://www.coingecko.com/en/coins/the-balkan-dwarf |
| 606 | UWON | UWON | à vérifier | mars 2024 | ≈ 48 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 273 ; CG `uwon` |
| 607 | Boop | BOOP | à vérifier | avr. 2024 | ≈ 47 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 235 ; CG `boop-2` |
| 608 | Flybrain | FLYBRAIN | Robinhood Chain (L2 Ethereum) | 10/09/2026 | ≈ 47 M$ (11/09/2026) | estimé | mort (≈ 0,2 M$) | « Le connectome d'une mouche du vinaigre qui vit sur internet », financé par son propre mème ; 47 M$ en un jour sur la nouvelle chaîne de Robinhood. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/flybrain/ |
| 609 | Prince Floki V2 | PrinceFloki | BNB Chain | nov. 2021 (ajout CMC) | ≤ 47 M$ en FDV (5 déc. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Version 2 d'un « Prince Floki », dérivé du chien d'Elon Musk, nov. 2021 ; coté un mois. | commune | commune | personne réelle | à définir | r4 ; https://coinmarketcap.com/currencies/princefloki-v2/ ; https://coinmarketcap.com/historical/20211205/ |
| 610 | Andy † | ANDY | Base | 2024 | ≈ 46 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 538 ; CG `andy-on-base` |
| 611 | KANGO | KANGO | Kaspa (KRC-20) | à vérifier (sommet le 22 nov. 2024) | ≈ 46 M$ (nov. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Kango, kangourou KRC-20 de la vague de mint de nov. 2024. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/kango |
| 612 | NumberGoUpTech | TECH | Avalanche | mars 2024 (ajout CMC) | ≈ 46 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | « Number Go Up Tech », satire du culte du prix sur Avalanche (mars 2024). | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/numbergouptech/ ; https://www.coingecko.com/en/coins/tech |
| 613 | Brett (ETH) | BRETT | à vérifier | à vérifier (sommet le 2024-09-26) | ≈ 45 M$, 2024-09-26 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `brett-memecoin` ; https://www.coingecko.com/en/coins/brett-memecoin |
| 614 | Pepe 2.0 | PEPE2.0 | Ethereum | juil. 2023 | ≈ 45 M$ (sourcé) | sourcé | mort (≈ 0,26 M$, -99,8 %) |  | commune | épique |  | à définir | v1 n° 251 ; correction r3 ; CG `pepe-2-0` ; https://www.coingecko.com/en/coins/pepe-2-0 |
| 615 | SHIRO INU | SHIR | BNB Chain | janv. 2022 (ajout CMC) | ≤ 45 M$ en FDV (16 janv. 2022) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Inu blanc (shiro en japonais) de janv. 2022, une des dernières vagues de clones Shiba ; mort en mars 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/shiro-inu/ ; https://coinmarketcap.com/historical/20220116/ |
| 616 | WAR | WAR | à vérifier | mars 2026 | ≈ 45 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 214 ; CG `war-2` |
| 617 | Bubb | BUBB | BNB Chain | 20/03/2025 (four.meme) | ≈ 44 M$ (21/03/2025) | estimé | mort (≈ 30 k$) | Mème dessiné à la main : ×10 en une nuit après une interaction de Yi He sur X, puis évaporé. | commune | rare |  | à définir | r3 ; https://www.odaily.news/en/post/5202475 ; https://coinmarketcap.com/currencies/bubb/ |
| 618 | 修仙 (Xiuxian) | 修仙 | BNB Chain | 09/10/2025 | ≈ 44 M$ (10/10/2025) | estimé | mort (≈ 0,5 M$) | Mème sur la « culture de l'immortel » des romans web chinois, né dans le sillage de Yi He et de 币安人生. | commune | rare |  | à définir | r3 ; https://www.10100.com/article/57767548 ; https://coinmarketcap.com/currencies/xiuxian/ |
| 619 | Tardi | TARDI | Sui | à vérifier (sommet le 16 déc. 2024) | ≈ 43,6 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Tardigrade « indestructible » de Sui, sommet le 16 déc. 2024 avec la saison Sui ; il n'a pas survécu (-99,7 %). | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/tardi |
| 620 | Shiba Inu Mother | SHIBM | HECO | mars 2022 | ≈ 43,1 M$ en FDV (04/03/2022) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur HECO, lancé en mars 2022 ; pic vers le 04/03/2022 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/shiba-inu-mother/ |
| 621 | Bitcoin Wizards | WZRD | Bitcoin (BRC-20, migration vers Runes) | 2024 | ≈ 43 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 254 |
| 622 | Bob (Monad) | BOB | Monad | 2025 | ≈ 43 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 566 ; CG `bob-3` |
| 623 | FourCoin | FOUR | à vérifier | à vérifier (sommet le 2023-05-09) | ≈ 43 M$, 2023-05-09 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `fourcoin` ; https://www.coingecko.com/en/coins/fourcoin |
| 624 | Shiryo Inu | SHIRYO | Ethereum | nov. 2021 | ≈ 43,0 M$ (20/01/2022) | sourcé | mort | Clone de Shiba Inu (jeton « Inu ») promettant un jeu de cartes sur Ethereum, lancé en nov. 2021 ; pic vers le 20/01/2022 ; aujourd'hui -99,94 %. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/shiryo-inu/ |
| 625 | LabraCoin | LABRA | Ethereum | avr. 2021 | ≈ 42,9 M$ en FDV (18/05/2021) | estimé | mort | Mème labrador reflection sur Ethereum, lancé en avr. 2021 ; pic vers le 18/05/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/labra-finance/ |
| 626 | Ponyo Inu | PONYO | Ethereum | oct. 2021 | ≈ 42,8 M$ en FDV (09/11/2021) | estimé | mort | Jeton « Inu » à thème Ponyo (Ghibli) sur Ethereum, lancé en oct. 2021 ; pic vers le 09/11/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/ponyo-inu/ |
| 627 | Invest Zone | IVFUN | Tron (SunPump) | à vérifier (sommet le 27 août 2024) | ≈ 42,6 M$ (août 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Mème « CIS » de la vague SunPump d'août 2024, parmi les jetons poussés vers une cotation HTX, puis abandonné. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/invest-zone ; https://www.kucoin.com/learn/crypto/top-tron-memecoins-to-watch |
| 628 | Simmi Token | SIMMI | à vérifier | à vérifier (sommet le 2024-12-04) | ≈ 42 M$, 2024-12-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `simmi-token` ; https://www.coingecko.com/en/coins/simmi-token |
| 629 | Waffles | WAFFLES | à vérifier | à vérifier (sommet le 2024-06-07) | ≈ 42 M$, 2024-06-07 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `waffles` ; https://www.coingecko.com/en/coins/waffles |
| 630 | 人生K线 (« K-line de la vie ») | à vérifier | BNB Chain | janv. 2026 | ≈ 42 M$ début janv. 2026 (PANews), ATH CMC × 1 Md ≈ 28 M$ le 10/01/2026 | estimé | mort (≈ 0,5 M$, -98 %) |  | commune | rare |  | à définir | v1 n° 658 ; correction r3 ; https://www.panewslab.com/zh/articles/b77d5603-6827-44b6-b75b-de051186d2c3 ; https://coinmarketcap.com/currencies/life-destiny-k-line/ |
| 631 | Captain Inu | CPTINU | Ethereum | déc. 2021 | ≈ 41,1 M$ en FDV (18/12/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en déc. 2021 ; pic vers le 18/12/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/captain-inu/ |
| 632 | Crob Coin | CROB | Cronos | avr. 2024 (ajout CMC) | ≤ 41 M$ en FDV (14 avr. 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Crob, mème corbeau de Cronos (avril 2024). | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/crob-coin/ ; https://coinmarketcap.com/historical/20240414/ |
| 633 | Dog Wif Nunchucks | NINJA | à vérifier | déc. 2023 | ≈ 41 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 287 ; CG `dog-wif-nuchucks` |
| 634 | DOGE-1 Satellite | DOGE-1 | à vérifier | à vérifier (sommet le 2025-09-15) | ≈ 41 M$, 2025-09-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `doge-1-satellite` ; https://www.coingecko.com/en/coins/doge-1-satellite |
| 635 | Dogecolony | DOGECO | BNB Chain | févr. 2022 (ajout CMC) | ≤ 41 M$ en FDV (6 févr. 2022) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Colonie de Doge de févr. 2022 sur BSC ; disparu en avril 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/dogecolony/ ; https://coinmarketcap.com/historical/20220206/ |
| 636 | Fair and Free | FAIR3 | à vérifier | août 2025 | ≈ 41 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 204 ; CG `fair-and-free` |
| 637 | Momo | MOMO | Solana | Interdiction de TikTok, janv. 2025 | ≈ 41 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 679 ; CG `momo-3` |
| 638 | Swasticoin | YZY | à vérifier | à vérifier (sommet le 2025-03-15) | ≈ 41 M$, 2025-03-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare | obscène | à définir | R5 C1 `swasticoin` ; https://www.coingecko.com/en/coins/swasticoin |
| 639 | 114514 | 114514 | Solana | Vague récente (date à vérifier) | ≈ 40 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 263 |
| 640 | BIBI | BIBI | à vérifier | à vérifier (sommet le 2024-03-06) | ≈ 40 M$, 2024-03-06 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `bibi` ; https://www.coingecko.com/en/coins/bibi |
| 641 | Catcoin | CAT | à vérifier | nov. 2024 | ≈ 40 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 265 ; CG `catcoin` |
| 642 | CatSlap | SLAP | à vérifier | déc. 2024 | ≈ 40 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 266 ; CG `catslap` |
| 643 | Clawd | CLAWD | Base | janv. 2026 | ≈ 40 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 267 ; correction r3 |
| 644 | FourBook | FB | à vérifier | oct. 2025 | ≈ 40 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 207 ; CG `fourbook` |
| 645 | MemeWars | MWAR | BNB Chain | nov. 2021 (ajout CMC) | ≤ 40 M$ en FDV (14 nov. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Jeu de cartes de mèmes promis fin 2021 sur BSC, jamais décollé ; plus coté en janv. 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/memewars/ ; https://coinmarketcap.com/historical/20211114/ |
| 646 | Roaring Kitty | KITTY | Solana | GameStop, mai 2024 | ≈ 40 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 269 ; correction r3 ; CG `roaring-kitty-solana` |
| 647 | Tralalero Tralala | à vérifier | Solana (à confirmer) | Brainrot italien, 2025-2026 | ≈ 40 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 271 ; correction r3 ; CG `tralalero-tralala` |
| 648 | WSB Coin | WSB | à vérifier | mai 2024 | ≈ 40 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 795 ; CG `wsb-coin` |
| 649 | WEWECOIN (ex-Upside Down Meme) | WEWE | Base | juil. 2024 | ~39,7 M$ (date inconnue) | estimé | mort | Mème « upside down » renommé WEWECOIN, GoPlus signale que le créateur peut bloquer les ventes, il vaut 75 k$. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/upside-down-meme |
| 650 | DeFrogs | DEFROGS | Ethereum (ERC-404) | févr. 2024 | ≈ 39 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 595 ; CG `defrogs` |
| 651 | Doge Raca | DOCA | BNB Chain | déc. 2021 (ajout CMC) | ≤ 39 M$ en FDV (5 déc. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Croisement Doge × Radio Caca (RACA) de déc. 2021 ; mort en janv. 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/doge-raca/ ; https://coinmarketcap.com/historical/20211205/ |
| 652 | Fofar | FOFAR | Tron | 2024 | ≈ 39 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 618 ; CG `fofar-2` |
| 653 | FUD the Pug † | FUD | Sui | 2023 | ≈ 39 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 276 ; CG `fud-the-pug` |
| 654 | Hehe | HEHE | Solana (à vérifier) | 2024 | ≈ 39 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 638 ; CG `hehecat` |
| 655 | Honk | HONK | à vérifier | à vérifier (sommet le 2024-03-09) | ≈ 39 M$, 2024-03-09 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `honk` ; https://www.coingecko.com/en/coins/honk |
| 656 | MOAI | MOAI | à vérifier | à vérifier (sommet le 2024-11-05) | ≈ 39 M$, 2024-11-05 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `moai` ; https://www.coingecko.com/en/coins/moai |
| 657 | NPC On Solana | NPCS | à vérifier | à vérifier (sommet le 2024-10-17) | ≈ 39 M$, 2024-10-17 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `npc-on-solana` ; https://www.coingecko.com/en/coins/npc-on-solana |
| 658 | Priceless | PRICELESS | BNB Chain | 08/09/2025 | ≈ 39 M$ (08/10/2025) | estimé | mort (≈ 0,16 M$) | Mème « sans prix » qui a culminé en pleine saison d'octobre, puis a été repris par une CTO. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/priceless/ |
| 659 | Real Smurf Cat (шайлушай) | SMURFCAT | Ethereum | 13/09/2023 | ≈ 39 M$ (27/10/2023) | estimé | mort | Mème russe du « chat schtroumpf » devenu viral sur TikTok à l'automne 2023, puis éteint. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/real-smurf-cat ; https://dexscreener.com/ethereum/0xfF836A5821E69066c87E268bC51b849FaB94240C |
| 660 | STAN | STAN | à vérifier | à vérifier (sommet le 2024-05-04) | ≈ 39 M$, 2024-05-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `stanley-cup-coin` ; https://www.coingecko.com/en/coins/stanley-cup-coin |
| 661 | Sundae The Dog | SUNDAE | Arbitrum | oct. 2023 (ajout CMC) | ≤ 39 M$ en FDV (12 nov. 2023) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Sundae, chien d'Arbitrum (oct. 2023). | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/sundae-the-dog/ ; https://coinmarketcap.com/historical/20231112/ |
| 662 | AU79 | AU79 | à vérifier | à vérifier (sommet le 2025-09-13) | ≈ 38 M$, 2025-09-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `au79` ; https://www.coingecko.com/en/coins/au79 |
| 663 | MAGIC•INTERNET•MONEY | MIM | Bitcoin (Runes) | début 2025 | ≈ 38 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 278 |
| 664 | TAO INU | TAONU | à vérifier | à vérifier (sommet le 2024-03-17) | ≈ 38 M$, 2024-03-17 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `tao-inu` ; https://www.coingecko.com/en/coins/tao-inu |
| 665 | τDoge | TDOGE | à vérifier | à vérifier (sommet le 2021-06-03) | ≈ 38 M$, 2021-06-03 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `tdoge` ; https://www.coingecko.com/en/coins/tdoge |
| 666 | Crash On Base | CRASH | Base | 2024 | ≈ 37 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 587 ; CG `crash-on-base` |
| 667 | Poodl | POODL | BSC | mars 2021 | ≈ 37,0 M$ en FDV (20/04/2021) | estimé | mort | Mème caniche reflection sur BSC, lancé en mars 2021 ; pic vers le 20/04/2021 ; aujourd'hui -99,87 %. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/poodle/ |
| 668 | Real Nigger Tate | RNT | Solana | juin 2024 | ≈ 37 M$ (9 juin 2024) | estimé | mort | Mème raciste sur Andrew Tate lancé le 09/06/2024 ; ~37 M$ le jour même. | commune | rare | obscène, personne réelle | à définir | r3 ; https://coinmarketcap.com/currencies/real-nigger-tate/ ; https://dexscreener.com/solana/2fUFhZyd47Mapv9wcfXh5gnQwFXtqcYu9xAN4THBpump |
| 669 | San Chan | SAN | à vérifier | à vérifier (sommet le 2025-02-02) | ≈ 37 M$, 2025-02-02 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `san-chan` ; https://www.coingecko.com/en/coins/san-chan |
| 670 | Sun Wukong | SUNWUKONG | Tron | 2024 | ≈ 37 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 762 ; CG `sunwukong` |
| 671 | Ainu | AINU | à vérifier | à vérifier (sommet le 2021-10-17) | ≈ 36 M$, 2021-10-17 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `ainu-token` ; https://www.coingecko.com/en/coins/ainu-token |
| 672 | FRIC | FRIC | à vérifier | à vérifier (sommet le 2024-12-10) | ≈ 36 M$, 2024-12-10 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `fric` ; https://www.coingecko.com/en/coins/fric |
| 673 | CatGPT | CATGPT | à vérifier | à vérifier (sommet le 2024-04-25) | ≈ 35 M$, 2024-04-25 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `catgpt` ; https://www.coingecko.com/en/coins/catgpt |
| 674 | Dotcom | Y2K | à vérifier | janv. 2025 | ≈ 35 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 300 ; CG `dotcom` |
| 675 | N3on | N3ON | à vérifier | à vérifier (sommet le 2025-11-12) | ≈ 35 M$, 2025-11-12 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `n3on` ; https://www.coingecko.com/en/coins/n3on |
| 676 | What IF | IF | à vérifier | à vérifier (sommet le 2026-08-02) | ≈ 35 M$, 2026-08-02 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `what-if-3` ; https://www.coingecko.com/en/coins/what-if-3 |
| 677 | Shar Pei | SHARPEI | BSC | nov. 2021 | ≈ 34,4 M$ en FDV (07/11/2021) | estimé | mort | Mème chien shar-pei sur BSC, lancé en nov. 2021 ; pic vers le 07/11/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/shar-pei/ |
| 678 | alright buddy | BUDDY | Hyperliquid (HIP-1) | à vérifier (sommet le 25 mai 2025) | ≈ 34,1 M$ (mai 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | Mème né d'un clash de KOL (« alright buddy »), record mai 2025, -99 %. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/alright-buddy |
| 679 | Zoro Inu | ZORO | BSC | mars 2022 | ≈ 34,1 M$ en FDV (25/03/2022) | estimé | mort | Jeton « Inu » à thème One Piece sur BSC, lancé en mars 2022 ; pic vers le 25/03/2022 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/zoro-inu/ |
| 680 | Cardi B (Wet Ass P***y) | WAP | Solana | oct. 2024 | ≈ 34-40 M$ (oct. 2024) | sourcé | mort (≈ 23 k$) | Jeton relayé par Cardi B, avec 60 % de l'offre groupée au lancement ; nouveau plongeon en juin 2025. | commune | rare | personne réelle, obscène | à définir | r3 ; https://decrypt.co/285099/cardi-b-wap-solana-meme-coin ; https://crypto.news/cardi-bs-wap-memecoin-pump-ends-in-another-rug-pull-again/ |
| 681 | Degen Zoo | DZOO | à vérifier | à vérifier (sommet le 2023-03-16) | ≈ 34 M$, 2023-03-16 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `degen-zoo` ; https://www.coingecko.com/en/coins/degen-zoo |
| 682 | Dust | DUST | BNB Chain | 19/09/2025 (four.meme) | ≈ 34 M$ (08/10/2025) | estimé | mort (≈ 0,17 M$) | Lutin-mascotte inventé autour d'Aster DEX ; c'est un mème, pas le jeton d'Aster ; il a suivi la vague d'Aster puis s'est éteint. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/dust/ |
| 683 | FU coin | FU | BNB Chain | sept. 2024 (ajout CMC) | ≈ 34 M$ (9 févr. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | « FU », mème d'insulte de sept. 2024 sur BSC ; pic en févr. 2025. | commune | rare | obscène | à définir | r4 ; https://coinmarketcap.com/currencies/fu-coin/ ; https://coinmarketcap.com/historical/20250209/ |
| 684 | Huhu Cat | HUHU | Merlin Chain | à vérifier (sommet le 27 mars 2024) | ≈ 34 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Huhu Cat, chat de Merlin Chain (L2 Bitcoin), mars 2024. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/huhu-cat |
| 685 | Shifu | SHIFU | à vérifier | à vérifier (sommet le 2024-12-20) | ≈ 34 M$, 2024-12-20 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `shifu` ; https://www.coingecko.com/en/coins/shifu |
| 686 | Justice For Ross | ROSS | Solana (pump.fun) | nov. 2024 | ≈ 33-40 M$ (21 janv. 2025) | sourcé | mort (≈ 1,4 k$) | Pari sur la grâce de Ross Ulbricht ; la nouvelle fait chuter le jeton de 90 %, et des portefeuilles liés à Ulbricht y perdent 12 M$. | commune | rare | personne réelle | à définir | r3 ; https://thedefiant.io/news/markets/ross-ulbricht-memecoins-tag-all-time-highs-on-commutation-bets ; https://dlnews.com/articles/defi/ross-ulbricht-wallets-lose-12-million-pump-fun |
| 687 | Saint Inu | SAINT | Arbitrum | nov. 2021 (ajout CMC) | ≤ 33 M$ en FDV (7 nov. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Saint Inu, un des tout premiers mèmes d'Arbitrum (nov. 2021, juste après l'ouverture du réseau) ; mort en 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/saint-inu/ ; https://coinmarketcap.com/historical/20211107/ |
| 688 | 吉祥马 | 吉祥马 | à vérifier | mai 2026 | ≈ 33 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 311 ; CG `jixiangma` |
| 689 | DisclaimerCoin | DONT | Solana | 22/01/2026 | ≈ 32-37 M$ (22/01/2026) | estimé | mort (≈ 0,4-0,6 M$) | Le jeton qui se dit « sans valeur, sans utilité, sans avenir » ; il a tenu parole le jour même de son pic. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/disclaimercoin/ |
| 690 | FINE | FINE | à vérifier | à vérifier (sommet le 2023-09-15) | ≈ 32 M$, 2023-09-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `fine` ; https://www.coingecko.com/en/coins/fine |
| 691 | Grimace Coin | GRIMACE | Dogechain | mai 2023 (ajout CMC) | ≤ 32 M$ en FDV (23 juil. 2023) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Grimace, monstre violet de McDonald's, a fait flamber Dogechain à l'été 2023 ; mort depuis. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/grimace-coin/ ; https://coinmarketcap.com/historical/20230723/ |
| 692 | henlo | HENLO | Berachain | 2025 | ≈ 32 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | commune | commune |  | à définir | v1 n° 508 ; CG `henlo-3` |
| 693 | Kaspy | KASPY | à vérifier | oct. 2024 | ≈ 32 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 322 ; CG `kaspy` |
| 694 | McPepe's | PEPES | à vérifier | à vérifier (sommet le 2024-04-28) | ≈ 32 M$, 2024-04-28 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `mcpepe-s` ; https://www.coingecko.com/en/coins/mcpepe-s |
| 695 | Spinning Cat | OIIAOIIA | à vérifier | à vérifier (sommet le 2025-01-04) | ≈ 32 M$, 2025-01-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `spinning-cat` ; https://www.coingecko.com/en/coins/spinning-cat |
| 696 | uPX | UPX | à vérifier | déc. 2023 | ≈ 32 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 310 ; CG `upx` |
| 697 | Genshin Floki Inu | GFloki | BSC | nov. 2021 | ≈ 31,7 M$ en FDV (21/11/2021) | estimé | mort | Jeton né du chien Floki d'Elon Musk (tweet du 25/06/2021) sur BSC, lancé en nov. 2021 ; pic vers le 21/11/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/genshinflokiinu-token/ |
| 698 | A Gently Used 2001 Honda Civic | USEDCAR | Solana | déc. 2023 | ≈ 31 M$ (30 déc. 2023) | estimé | mort | « Une Honda Civic 2001 légèrement usagée », mème absurde de la vague d'hiver ; ~31 M$ le 30/12/2023. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/a-gently-used-2001-honda-civic/ ; https://dexscreener.com/solana/9gwTegFJJErDpWJKjPfLr2g2zrE3nL1v5zpwbtsk3c6P |
| 699 | Daku V2 | DAKU | à vérifier | à vérifier (sommet le 2025-10-05) | ≈ 31 M$, 2025-10-05 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `daku-v2` ; https://www.coingecko.com/en/coins/daku-v2 |
| 700 | Goldn | GOLDN | à vérifier | sept. 2025 | ≈ 31 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 303 ; CG `goldn` |
| 701 | HAMI | HAMI | à vérifier | à vérifier (sommet le 2024-03-29) | ≈ 31 M$, 2024-03-29 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `hami` ; https://www.coingecko.com/en/coins/hami |
| 702 | TANUKI•WISDOM | TANUKI | Bitcoin (Runes) | 2024 | ≈ 31 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 298 |
| 703 | Gecko Inu | GEC | Avalanche | 2024 | ≈ 30 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 625 ; CG `gecko-inu` |
| 704 | LEO | LEO | à vérifier | mars 2024 | ≈ 30 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 307 ; CG `leopold` |
| 705 | Lion Cat | LCAT | BNB Chain | févr. 2025 (ajout CMC) | ≈ 30 M$ (9 mars 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Chat-lion de la première vague four.meme (mars 2025) ; ≈ 30 M$ au sommet. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/lion-cat/ ; https://coinmarketcap.com/historical/20250309/ |
| 706 | Luna Inu | LINU | à vérifier | à vérifier (sommet le 2024-03-13) | ≈ 30 M$, 2024-03-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `luna-inu` ; https://www.coingecko.com/en/coins/luna-inu |
| 707 | MoonRise | MOONRISE | BSC | juin 2021 | ≈ 30,0 M$ en FDV (10/07/2021) | estimé | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) sur BSC, lancé en juin 2021 ; pic vers le 10/07/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/moonrise/ |
| 708 | Safetesla | SAFETESLA | BSC | mars 2021 | ≈ 30,0 M$ en FDV (24/04/2021) | estimé | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) au nom de Tesla sur BSC, lancé en mars 2021 ; pic vers le 24/04/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/safetesla/ |
| 709 | SaylorMoon | SMOON | BSC | mai 2021 | ≈ 30,0 M$ en FDV (06/06/2021) | estimé | mort | Mème Michael Saylor reflection sur BSC, lancé en mai 2021 ; pic vers le 06/06/2021 ; aujourd'hui plus coté. | commune | rare | personne réelle | à définir | r2 ; https://coinmarketcap.com/currencies/saylormoon/ |
| 710 | Tbull | TBULL | Tron | 2024 | ≈ 30 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 768 ; CG `tron-bull-coin` |
| 711 | Toby ToadGod | TOBY | à vérifier | à vérifier (sommet le 2024-04-10) | ≈ 30 M$, 2024-04-10 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `toby-toadgod` ; https://www.coingecko.com/en/coins/toby-toadgod |
| 712 | WifeDoge | WIFEDOGE | BSC | juil. 2021 | ≈ 29,3 M$ en FDV (19/09/2021) | estimé | mort | Clone de Dogecoin sur BSC, lancé en juil. 2021 ; pic vers le 19/09/2021 ; aujourd'hui -99,55 %. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/wifedoge/ |
| 713 | Aqua Goat | AQUAGOAT | à vérifier | à vérifier (sommet le 2021-10-10) | ≈ 29 M$, 2021-10-10 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `aqua-goat` ; https://www.coingecko.com/en/coins/aqua-goat |
| 714 | BabyMatic | BABYMATIC | BNB Chain | juil. 2021 (ajout CMC) | ≤ 29 M$ en FDV (14 nov. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Jeton « Baby » de la mode de l'automne 2021 (BabyDoge, BabyCake…), versant des récompenses en MATIC ; mort en 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/babymatic/ ; https://coinmarketcap.com/historical/20211114/ |
| 715 | Generational Wealth | GEN | à vérifier | à vérifier (sommet le 2023-05-18) | ≈ 29 M$, 2023-05-18 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `generational-wealth` ; https://www.coingecko.com/en/coins/generational-wealth |
| 716 | Pesto the Baby King Penguin | PESTO | Solana | 2025 (à vérifier) | ≈ 29 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 712 ; CG `pesto-the-baby-king-penguin` |
| 717 | Pikachu Inu | PIKACHU | Ethereum | oct. 2021 | ≈ 28,3 M$ en FDV (28/10/2021) | estimé | mort | Jeton « Inu » à thème Pokémon sur Ethereum, lancé en oct. 2021 ; pic vers le 28/10/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/pikachu-inu/ |
| 718 | All Street Bets | BETS | à vérifier | 2021-2024 (à vérifier) | ≈ 28 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 534 ; CG `all-street-bets` |
| 719 | BOG | BOG | Solana | Préventes, mars 2024 | ≈ 28 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 568 ; CG `bog` |
| 720 | ElonRWA | ELONRWA | à vérifier | à vérifier (sommet le 2024-11-15) | ≈ 28 M$, 2024-11-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare | personne réelle | à définir | R5 C1 `elonrwa` ; https://www.coingecko.com/en/coins/elonrwa |
| 721 | Ghiblification | GHIBLI | Solana (pump.fun) | 26 mars 2025 | ≈ 28 M$ (mars 2025) ; ≈ 41 M$ selon l'ATH CoinGecko | sourcé | mort (≈ 80 k$) | Né de la vague d'images « style Ghibli » de ChatGPT, retombé avec la mode. | commune | rare |  | à définir | r3 ; https://decrypt.co/311958/ghiblification-ai-ghibli-solana-meme-coin-pumps ; https://www.coingecko.com/en/coins/ghiblification |
| 722 | JustAnEgg | EGG | à vérifier | à vérifier (sommet le 2024-04-04) | ≈ 28 M$, 2024-04-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `justanegg-2` ; https://www.coingecko.com/en/coins/justanegg-2 |
| 723 | Milady Wif Hat | LADYF | à vérifier | à vérifier (sommet le 2024-05-22) | ≈ 28 M$, 2024-05-22 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `milady-wif-hat` ; https://www.coingecko.com/en/coins/milady-wif-hat |
| 724 | Zeek Coin | MEOW | zkSync Era | janv. 2024 (ajout CMC) | ≈ 28 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Zeek, le chat mascotte de zkSync (MEOW), lancé début 2024 ; mort. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/zeek-coin/ ; https://www.coingecko.com/en/coins/zeek-coin |
| 725 | 屎壳郎 (Dung Beetle) | 屎壳郎 | à vérifier | à vérifier (sommet le 2026-07-09) | ≈ 28 M$, 2026-07-09 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `shikelang` ; https://www.coingecko.com/en/coins/shikelang |
| 726 | Husky Avax | HUSKY | Avalanche | mai 2021 | ≈ 27,9 M$ en FDV (28/10/2021) | estimé | mort | Dog coin d'Avalanche, lancé en douce le 12/05/2021 sur Avalanche, lancé en mai 2021 ; pic vers le 28/10/2021 ; aujourd'hui -99,39 %. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/husky-avax/ |
| 727 | Chuck | CHUCK | Base | mars 2024 | ~27,3 M$ (date inconnue) | estimé | mort | Chien « bien-être animal » de la saison Base 2024, il vaut moins de 100 k$. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/chuck |
| 728 | Business Coin | BUSINESS | à vérifier | à vérifier (sommet le 2025-01-31) | ≈ 27 M$, 2025-01-31 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `business-coin` ; https://www.coingecko.com/en/coins/business-coin |
| 729 | Cheese | CHEESE | à vérifier | à vérifier (sommet le 2024-11-20) | ≈ 27 M$, 2024-11-20 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `cheese-3` ; https://www.coingecko.com/en/coins/cheese-3 |
| 730 | SHIBAAI | SHIBAAI | à vérifier | à vérifier (sommet le 2024-03-06) | ≈ 27 M$, 2024-03-06 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `shibaai` ; https://www.coingecko.com/en/coins/shibaai |
| 731 | WASSIE | WASSIE | à vérifier | à vérifier (sommet le 2024-03-13) | ≈ 27 M$, 2024-03-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `wassie` ; https://www.coingecko.com/en/coins/wassie |
| 732 | WORLD CUP INU | WCI | Ethereum | sept. 2022 | ≈ 26,8 M$ en FDV (05/11/2022) | estimé | mort | Jeton « Inu » de la Coupe du monde 2022 sur Ethereum, lancé en sept. 2022 ; pic vers le 05/11/2022 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/world-cup-inu/ |
| 733 | 🟥🟪🟦🟩🟨🟧 | 🟥🟩 | à vérifier | à vérifier (sommet le 2024-11-19) | ≈ 26 M$, 2024-11-19 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `-5` ; https://www.coingecko.com/en/coins/-5 |
| 734 | Doge Universe | SPACEXDOGE | BNB Chain | sept. 2021 (ajout CMC) | ≤ 26 M$ en FDV (7 nov. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Doge « SpaceX » de l'automne 2021 (ticker SPACEXDOG), surfant sur les tweets d'Elon Musk ; coté quelques semaines seulement. | commune | commune | personne réelle | à définir | r4 ; https://coinmarketcap.com/currencies/doge-universe/ ; https://coinmarketcap.com/historical/20211107/ |
| 735 | Gochujangcoin | GOCHU | Base | août 2024 (ajout CMC) | ≈ 26 M$ (18 mai 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Mème du piment coréen gochujang sur Base (août 2024) ; ≈ 26 M$ en mai 2025, puis mort. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/gochujangcoin/ ; https://www.coingecko.com/en/coins/gochujangcoin |
| 736 | HeeeHeee | HEEHEE | à vérifier | avr. 2024 | ≈ 26 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 305 ; CG `heeeheee` |
| 737 | Ignore Fud | 4TOKEN | Core | mars 2023 (ajout CMC) | ≤ 26 M$ en FDV (7 mai 2023) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | « Ignore FUD », jeton-slogan de Core (avril 2023). | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/ignore-fud/ ; https://coinmarketcap.com/historical/20230507/ |
| 738 | Manifest | MANIFEST | à vérifier | à vérifier (sommet le 2024-11-10) | ≈ 26 M$, 2024-11-10 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `manifest-on-sol` ; https://www.coingecko.com/en/coins/manifest-on-sol |
| 739 | Mubarakah | MUBARAKAH | BNB Chain | 15/03/2025 | ≈ 26 M$ (18/03/2025) | estimé | mort (≈ 0,4 M$) | Version « féminine » de Mubarak, lancée en pleine frénésie Mubarak/CZ ; reprise ensuite par une communauté CTO. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/mubarakah/ |
| 740 | Swag | SWAG | à vérifier | à vérifier (sommet le 2024-11-13) | ≈ 26 M$, 2024-11-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `swag` ; https://www.coingecko.com/en/coins/swag |
| 741 | CumInu | CUMINU | Ethereum | mai 2021 | ≈ 25,9 M$ en FDV (05/07/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en mai 2021 ; pic vers le 05/07/2021 ; aujourd'hui plus coté. | commune | rare | obscène | à définir | r2 ; https://coinmarketcap.com/currencies/cuminu/ |
| 742 | Briun Armstrung | BRIUN | Base | mars 2024 | ~25,3 M$ (date inconnue) | estimé | mort | Parodie de Brian Armstrong, présentée comme le premier mème déflationniste de Base, elle vaut 35 k$. | commune | rare | personne réelle | à définir | r3 ; https://www.coingecko.com/en/coins/briun-armstrung |
| 743 | WOOF | WOOF | Solana | mai 2021 | ≈ 25,2 M$ (03/12/2021) | sourcé | mort | Un des premiers dog coins de Solana, airdropé à la communauté en mai 2021 ; plus haut le 06/11/2021, aujourd'hui -99,8 %. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/woof/ |
| 744 | ElonDoge | EDOGE | BSC | mai 2021 | ≈ 25,1 M$ en FDV (31/10/2021) | estimé | mort | Mème Elon Musk + Doge sur BSC, lancé en mai 2021 ; pic vers le 31/10/2021 ; aujourd'hui plus coté. | commune | rare | personne réelle | à définir | r2 ; https://coinmarketcap.com/currencies/elondoge/ |
| 745 | Baby BNB | BABY | BNB Chain | sept. 2024 (ajout CMC) | ≈ 25 M$ (13 oct. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | « Baby BNB », un des mèmes poussés pendant la remontée de BNB et la sortie de prison de CZ (sept.-oct. 2024). | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/baby-bnb/ ; https://www.coingecko.com/en/coins/baby-bnb |
| 746 | Defender of Doge | DOD | BNB Chain | déc. 2021 (ajout CMC) | ≤ 25 M$ en FDV (16 janv. 2022) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | « Défenseur de Doge », clone de fin 2021 ; coté trois semaines. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/defender-of-doge/ ; https://coinmarketcap.com/historical/20220116/ |
| 747 | IC Ghost | GHOST | à vérifier | à vérifier (sommet le 2024-01-04) | ≈ 25 M$, 2024-01-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `ic-ghost` ; https://www.coingecko.com/en/coins/ic-ghost |
| 748 | IQ50 | IQ50 | Solana | mars 2024 | ≈ 25 à 67 M$ (16-28 mars 2024) | estimé | mort | Mème du « QI de 50 » de la folie de mars 2024 ; retombé à ~180 k$. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/iq50/ ; https://dexscreener.com/solana/21rweMLGYeMNonHW7H3xa5py17X6ZFRcHirCp9inRBQA |
| 749 | LERNITAS | 2192 | Optimism | mars 2024 (ajout CMC) | ≤ 25 M$ en FDV (24 mars 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Lernitas, mème d'Optimism de mars 2024 ; disparu du classement en mai 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/lernitas/ ; https://coinmarketcap.com/historical/20240324/ |
| 750 | Nasdaq666 | NDQ | BNB Chain | juil. 2025 (ajout CMC) | ≈ 25 M$ (5 oct. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Parodie du Nasdaq (« 666 ») de juillet 2025 sur BSC ; ≈ 25 M$ début oct. 2025. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/nasdaq666/ ; https://coinmarketcap.com/historical/20251005/ |
| 751 | Parabolic | PARAX | à vérifier | à vérifier (sommet le 2025-05-30) | ≈ 25 M$, 2025-05-30 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `parabolic-3` ; https://www.coingecko.com/en/coins/parabolic-3 |
| 752 | Sugar Boy | SUGAR | Tron | 2024 | ≈ 25 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 760 ; CG `sugar-boy` |
| 753 | Noggles | NOGS | Base (aussi ETH, Polygon) | inconnu | ~24,6 M$ (date inconnue) | estimé | mort | Mème des lunettes Nouns, censé unir les communautés « nounish », il fait 0 $ de volume. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/noggles |
| 754 | BUBBLES (Bubbles Bean) | BUBBLES | Aptos | à vérifier (sommet le 6 oct. 2024) | ≈ 24,5 M$ (oct. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Haricot à bulles d'Aptos, record oct. 2024, plus aucun volume. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/bubbles-2 |
| 755 | Squid Moon | SQM | BSC | nov. 2021 | ≈ 24,3 M$ en FDV (18/11/2021) | estimé | mort | Jeton de la vague Squid Game (automne 2021) sur BSC, lancé en nov. 2021 ; pic vers le 18/11/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/squid-moon/ |
| 756 | AstroPepeX | APX | Ethereum | 2023 | ≈ 24 M$ (date CoinGecko 18/11/2024, à vérifier) | estimé | mort | Présenté comme le premier jeton créé et déployé par une IA (code autonome et API OpenAI). | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/astropepex ; https://dexpaprika.com/ethereum/token/0xed4e879087ebd0e8a77d66870012b5e0dffd0fa4 |
| 757 | Attention | ATTN | à vérifier | juil. 2025 | ≈ 24 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 318 ; CG `attention` |
| 758 | CATO | CATO | Solana | mai 2021 | ≈ 24,0 M$ en FDV (28/10/2021) | estimé | mort | Mème chat de Solana sur Solana, lancé en mai 2021 ; pic vers le 28/10/2021 ; aujourd'hui -99,71 %. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/cato/ |
| 759 | Chaos | CHAOS | à vérifier | à vérifier (sommet le 2024-12-31) | ≈ 24 M$, 2024-12-31 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `chaos-2` ; https://www.coingecko.com/en/coins/chaos-2 |
| 760 | LAMBO | LAMBO | Avalanche | juin 2025 (ajout CMC) | ≈ 24 M$ (29 juin 2025) ; CMC, relevé hebdomadaire | sourcé | mort | LAMBO, mème Lamborghini d'Avalanche (juin 2025) ; ≈ 24 M$ fin juin 2025. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/lambo/ ; https://www.coingecko.com/en/coins/lambo-4 |
| 761 | memes will continue | memes | BNB Chain | 21/01/2026 | ≈ 24 M$ (21/01/2026) | estimé | mort (≈ 58 k$) | Slogan « les mèmes continueront » : pic le jour même du lancement, puis chute de 99,8 %. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/memes-will-continue/ ; https://dexscreener.com/bsc/0xf74548802f4c700315f019fde17178b392ee4444 |
| 762 | Suncat | SUNCAT | Tron | août 2024 | ≈ 24 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | commune | rare |  | à définir | v1 n° 411 ; CG `suncat` |
| 763 | Windoge98 | EXE | à vérifier | juin 2024 | ≈ 24 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 345 ; CG `windoge98` |
| 764 | Waka Flocka Flame † | FLOCKA | Solana | 2024 | ≈ 23,8 M$ (estimé : -99 % jusqu'à 238 k$) | estimé | mort |  | commune | rare |  | à définir | v1 n° 784 ; correction r3 ; CG `waka-flocka` ; https://decrypt.co/298703/scene-2024-story-of-the-year-celebrity-meme-coins |
| 765 | Okayeg | OKAYEG | Base | avr. 2024 | ~23,6 M$ (date inconnue) | estimé | mort | Grenouille issue de 4chan et Twitch, lancée sur Base en avril 2024, elle vaut moins de 100 k$. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/okayeg |
| 766 | RUGMAN | RUG | Hyperliquid (HIP-1) | à vérifier (sommet le 8 déc. 2024) | ≈ 23,3 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Super-héros « anti-rug » de Hyperliquid, record le 8 déc. 2024, -99,9 %. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/rugman |
| 767 | Bloo | BLOO | Base | mars 2024 | ≈ 23 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 334 ; correction r3 |
| 768 | DORK | DORK | à vérifier | à vérifier (sommet le 2023-11-04) | ≈ 23 M$, 2023-11-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `dork` ; https://www.coingecko.com/en/coins/dork |
| 769 | Frodo the virtual samurai | FROG | BNB Chain | déc. 2024 (ajout CMC) | ≈ 23 M$ (29 déc. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Grenouille samouraï « virtuelle » de déc. 2024 sur BSC ; ≈ 23 M$ fin déc. 2024. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/frodo-the-virtual-samurai/ ; https://www.coingecko.com/en/coins/frodo-the-virtual-samurai |
| 770 | GAME•OF•BITCOIN | GAME | Bitcoin (Runes) | 2024 | ≈ 23 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 622 ; CG `game-of-bitcoin-rune` |
| 771 | HayCoin | HAY | à vérifier | à vérifier (sommet le 2023-10-25) | ≈ 23 M$, 2023-10-25 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `haycoin` ; https://www.coingecko.com/en/coins/haycoin |
| 772 | Peepo | PEEPO | Ethereum | avr.-mai 2023 | ≈ 23 M$ (05/05/2023) | estimé | mort | Variante Twitch de Pepe lancée dans la vague de mai 2023, sommet le jour du pic du marché des mèmes. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/peepo |
| 773 | Red Hare Coin | RHC | à vérifier | à vérifier (sommet le 2026-04-26) | ≈ 23 M$, 2026-04-26 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `red-hare-coin` ; https://www.coingecko.com/en/coins/red-hare-coin |
| 774 | Smiley Coin | SMILEY | à vérifier | à vérifier (sommet le 2024-01-16) | ≈ 23 M$, 2024-01-16 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `smiley-coin` ; https://www.coingecko.com/en/coins/smiley-coin |
| 775 | 888 | 888 | à vérifier | à vérifier (sommet le 2024-11-30) | ≈ 22 M$, 2024-11-30 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `888-token` ; https://www.coingecko.com/en/coins/888-token |
| 776 | Bird Dog | BIRDDOG | à vérifier | à vérifier (sommet le 2024-06-10) | ≈ 22 M$, 2024-06-10 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `bird-dog` ; https://www.coingecko.com/en/coins/bird-dog |
| 777 | Buftoad | BUF | Solana | avr. 2024 | ≈ 22 M$ (16 avr. 2024) | estimé | mort | Crapaud bodybuildé ; ~22 M$ le jour du lancement (16/04/2024). | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/buftoad/ ; https://dexscreener.com/solana/7TqzdYyHU8R48VTBJHASa6Ppbvyfx8LLfdBznwVNpEJQ |
| 778 | Catalorian | CATALORIAN | à vérifier | à vérifier (sommet le 2025-08-18) | ≈ 22 M$, 2025-08-18 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `catalorian` ; https://www.coingecko.com/en/coins/catalorian |
| 779 | Chihuahua | HUAHUA | Chihuahua (Cosmos) | janv. 2022 (ajout CMC) | ≥ 22 M$ (28 janv. 2024) ; CMC, relevé hebdomadaire ; FDV CMC max ≈ 468 M$ | sourcé | mort | Chihuahua, blockchain-mème du Cosmos lancée en nov. 2021 avec airdrop aux stakers ; CMC ne publie une capitalisation qu'à partir de 2024 (≈ 22 M$), l'estimation CoinGecko (≈ 1,1 Md$) est faussée par l'inflation. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/chihuahua-wtf/ |
| 780 | GOGGLES | GOGLZ | Fantom / Sonic | oct. 2024 (ajout CMC) | ≈ 22 M$ (1 déc. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | GOGGLES, mème lunettes de Fantom puis Sonic ; ≈ 22 M$ début déc. 2024. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/goggles/ ; https://www.coingecko.com/en/coins/googles |
| 781 | MUSTAAAAAARD | MUSTARD | à vérifier | à vérifier (sommet le 2024-11-27) | ≈ 22 M$, 2024-11-27 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `mustaaaaaard` ; https://www.coingecko.com/en/coins/mustaaaaaard |
| 782 | Nobiko Coin | LONG | à vérifier | à vérifier (sommet le 2025-10-13) | ≈ 22 M$, 2025-10-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `nobiko-coin` ; https://www.coingecko.com/en/coins/nobiko-coin |
| 783 | Pepe Community | PEPE | à vérifier | à vérifier (sommet le 2023-08-28) | ≈ 22 M$, 2023-08-28 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `pepe-token` ; https://www.coingecko.com/en/coins/pepe-token |
| 784 | Playdoge | PLAY | à vérifier | août 2024 | ≈ 22 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 340 ; CG `playdoge` |
| 785 | supercycle(real) | SUPERCYCLE | à vérifier | à vérifier (sommet le 2024-11-13) | ≈ 22 M$, 2024-11-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `supercycle-real` ; https://www.coingecko.com/en/coins/supercycle-real |
| 786 | Teddy Doge | TEDDY | BNB Chain | févr. 2022 (ajout CMC) | ≤ 22 M$ en FDV (3 avr. 2022) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Doge en peluche de févr. 2022 ; jeton BSC sans activité depuis. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/teddydoge/ ; https://coinmarketcap.com/historical/20220403/ |
| 787 | Toad (SOL) | TOAD | à vérifier | à vérifier (sommet le 2024-11-02) | ≈ 22 M$, 2024-11-02 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `toad-sol` ; https://www.coingecko.com/en/coins/toad-sol |
| 788 | Wall St. Bull | WBULL | BNB Chain | 07/10/2025 | ≈ 22 M$ (08/10/2025) | estimé | mort (≈ 13 k$, volume nul) | Le taureau de Wall Street version BNB ; pic au lendemain du lancement, puis rien. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/wall-st-bull/ |
| 789 | Wifejak | WIFE | à vérifier | à vérifier (sommet le 2024-11-28) | ≈ 22 M$, 2024-11-28 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `wifejak` ; https://www.coingecko.com/en/coins/wifejak |
| 790 | King Shiba | KINGSHIB | BSC | oct. 2021 | ≈ 21,9 M$ (16/12/2021) | sourcé | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en oct. 2021 ; pic vers le 16/12/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/king-shiba/ |
| 791 | Dogira | DOGIRA | Ethereum | févr. 2021 | ≈ 21,4 M$ en FDV (05/11/2021) | estimé | mort | Mème Doge + Godzilla sur Ethereum, lancé en févr. 2021 ; pic vers le 05/11/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/dogira-new/ |
| 792 | Base is for everyone | BASEISFOREVERYONE | Base (Zora) | avr. 2025 | ~21,1 M$ (date inconnue) | estimé | mort | Publication du compte officiel de Base transformée en coin Zora au printemps 2025, son envolée puis son effondrement ont fait scandale (récit de mémoire, à vérifier). Rareté ramenée à rare : histoire non sourcée. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/base-is-for-everyone |
| 793 | Baby Pepe | BABYPEPE | à vérifier | à vérifier (sommet le 2024-11-13) | ≈ 21 M$, 2024-11-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `baby-pepe-3` ; https://www.coingecko.com/en/coins/baby-pepe-3 |
| 794 | POPDOG | POPDOG | à vérifier | à vérifier (sommet le 2024-09-25) | ≈ 21 M$, 2024-09-25 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `popdog` ; https://www.coingecko.com/en/coins/popdog |
| 795 | Sanin Inu | SANI | à vérifier | à vérifier (sommet le 2024-03-13) | ≈ 21 M$, 2024-03-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `sanin-inu` ; https://www.coingecko.com/en/coins/sanin-inu |
| 796 | Skull of Pepe Token | SKOP | à vérifier | juin 2024 | ≈ 21 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 329 ; CG `skull-of-pepe-token` |
| 797 | YOLO | YOLO | à vérifier | à vérifier (sommet le 2026-08-30) | ≈ 21 M$, 2026-08-30 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `yolo-2` ; https://www.coingecko.com/en/coins/yolo-2 |
| 798 | Ton Cat | TCAT | TON | à vérifier (sommet le 6 juil. 2024) | ≈ 20,9 M$ (juil. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Chat de TON de l'été 2024, record le 6 juil. 2024, -99,8 %. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/ton-cat |
| 799 | Super Suiyan | SUIYAN | Sui | à vérifier (sommet le 23 mai 2025) | ≈ 20,8 M$ (mai 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | Parodie de Super Saiyan au corps en goutte d'eau (logo Sui), sommet mai 2025, mort depuis. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/super-suiyan |
| 800 | NEAT | NEAT | NEAR (inscription NRC-20) | à vérifier (sommet le 25 déc. 2023) | ≈ 20,7 M$ (déc. 2023) ; ATH CoinGecko × offre totale | estimé | mort | Première inscription « NRC-20 » de NEAR, mintée en masse fin 2023 ; record le 25 déc. 2023, -99,8 %. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/neat |
| 801 | Based Shiba Inu | BSHIB | Base | mars 2024 | ~20,6 M$ (date inconnue) | estimé | mort | Copie de SHIB sur Base en mars 2024, 2 $ de volume par jour. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/based-shiba-inu |
| 802 | SHIBAVAX | SHIBX | Avalanche | mai 2021 | ≈ 20,5 M$ (28/10/2021) | sourcé | mort | Clone de Shiba Inu sur Avalanche sur Avalanche, lancé en mai 2021 ; pic vers le 28/10/2021 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/shibavax/ |
| 803 | Carlo | CARLO | Base | avr. 2024 | ~20,2 M$ (date inconnue) | estimé | mort | Chien qui voulait « dominer Base » au printemps 2024, il fait 15 $ de volume par jour. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/carlo |
| 804 | Shibaken Finance | SHIBAKEN | Ethereum | avr. 2021 | ≈ 20,2 M$ en FDV (13/02/2023) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en avr. 2021 ; pic vers le 13/02/2023 ; aujourd'hui plus coté. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/shibaken-finance/ |
| 805 | BabySNEK | BBSNEK | Cardano | déc. 2024 (ajout CMC) | ≈ 20 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Bébé de SNEK, le serpent mème de Cardano (janv. 2024). | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/babysnek/ ; https://www.coingecko.com/en/coins/babysnek |
| 806 | DOYR | DOYR | BNB Chain | 06/12/2025 (four.meme) | ≈ 20 M$ (07/12/2025) | estimé | mort (≈ 0,25 M$) | Mème four.meme de décembre 2025, pic dès le lendemain du lancement ; nom proche de « DYOR », origine à vérifier. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/doyr/ |
| 807 | Meowcoin | MEWC | à vérifier | à vérifier (sommet le 2022-10-09) | ≈ 20 M$, 2022-10-09 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `meowcoin` ; https://www.coingecko.com/en/coins/meowcoin |
| 808 | OSCAR | OSCAR | à vérifier | à vérifier (sommet le 2024-10-21) | ≈ 20 M$, 2024-10-21 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `oscar` ; https://www.coingecko.com/en/coins/oscar |
| 809 | Peepo (Solana) | PEEP | Solana | nov. 2023 | ≈ 20 M$ (10 déc. 2023) | estimé | mort | Version Solana de la grenouille Peepo ; ~20 M$ en décembre 2023. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/peepo-sol/ ; https://dexscreener.com/solana/n54ZwXEcLnc3o7zK48nhrLV4KTU5wWD4iq7Gvdt5tik |
| 810 | Pepa Inu | PEPA | Ethereum | avr. 2023 | ≈ 20 M$ (21/04/2023) | estimé | mort | « Femme de Pepe », une des toutes premières copies d'avril 2023, morte en quelques semaines. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/pepa-inu |
| 811 | RIBBIT | RBT | à vérifier | à vérifier (sommet le 2024-09-24) | ≈ 20 M$, 2024-09-24 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `ribbit-2` ; https://www.coingecko.com/en/coins/ribbit-2 |
| 812 | Smolcoin | SMOL | Arbitrum | déc. 2023 (ajout CMC) | ≤ 20 M$ en FDV (5 janv. 2025) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Smolcoin, mème « smol brain » de l'écosystème Treasure/Smolverse sur Arbitrum ; pic début 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/smolcoin/ ; https://coinmarketcap.com/historical/20250105/ |
| 813 | Uranus (Solana) | ANUS | Solana | janv. 2024 | ≈ 20 M$ (31 mars 2024) | estimé | mort | Jeu de mots scatologique sur Uranus ; ~20 M$ fin mars 2024. | commune | rare | obscène | à définir | r3 ; https://coinmarketcap.com/currencies/uranus-sol/ ; https://dexscreener.com/solana/9hjZ8UTNrNWt3YUTHVpvzdQjNbp64NbKSDsbLqKR6BZc |
| 814 | Wolfi | WOLFI | Avalanche | 2025 | ≈ 20 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 358 ; CG `wolfi-2` |
| 815 | Poncho | PONCHO | Base | mars 2024 | ~19,6 M$ (date inconnue) | estimé | mort | Chat de Base à offre réduite (10 M), un pic à près de 2 $, il est aujourd'hui à 0,004 $. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/poncho |
| 816 | Based Turbo | TURBO | Base | inconnu | ~19,5 M$ (date inconnue) | estimé | mort | Hommage sur Base au TURBO d'Ethereum (le mème fait avec GPT-4), différent du TURBO du catalogue, il pèse 56 k$. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/based-turbo |
| 817 | BOOK OF BILLIONAIRES | BOBE | Solana | avr. 2024 | ≈ 19,3 M$ (2 mai 2024) | estimé | mort | « Book of Billionaires », un des suiveurs de BOME ; ~19 M$ début mai 2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/book-of-billionaires/ ; https://dexscreener.com/solana/VvgeRQNHRHdYubKC9K2GN567LXTzSVcB7mpu7b1VF4r |
| 818 | Bork | BORK | Solana | déc. 2023 | ≈ 19,1 M$ (8 mars 2024) | estimé | mort | Chien « Bork » de la vague d'hiver ; ~19 M$ en mars 2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/bork-token/ ; https://dexscreener.com/solana/4jZXkSNgTQKCDb36ECZ6a2aNzcUniGcDeXgTdtM2HxAX |
| 819 | MarsRise | MARSRISE | BSC | août 2021 | ≈ 19,1 M$ en FDV (05/11/2021) | estimé | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) sur BSC, lancé en août 2021 ; pic vers le 05/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/marsrise/ |
| 820 | Asteroid The Space Shiba Inu | ASTEROID | à vérifier | à vérifier (sommet le 2026-05-13) | ≈ 19 M$, 2026-05-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `asteroid-the-space-shiba-inu` ; https://www.coingecko.com/en/coins/asteroid-the-space-shiba-inu |
| 821 | Baby Doge Cash | BABYDOGECASH | à vérifier | à vérifier (sommet le 2021-07-04) | ≈ 19 M$, 2021-07-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `baby-doge-cash` ; https://www.coingecko.com/en/coins/baby-doge-cash |
| 822 | Based Chad | CHAD | Base | 2024 | ≈ 19 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 555 ; CG `based-chad` |
| 823 | Bitcoin 2.0 | BTC2.0 | Ethereum | 10/07/2023 | ≈ 19 M$ (16/07/2023) | estimé | mort | Produit de la mode des « 2.0 » de juillet 2023, sommet en six jours. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/bitcoin-2-0 ; https://dexscreener.com/ethereum/0x3FEB4fEA5132695542F8Ede5076Ac43296d17c6d |
| 824 | BNB Card | BNB CARD | BNB Chain | 18/03/2025 (four.meme) | ≈ 19 M$ (21/03/2025) | estimé | mort (≈ 33 k$, volume nul) | Mème sur la carte Binance : réaction de Yi He, 30 M$ de volume en 20 h, reprise CTO, puis zéro. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/bnb-card/ |
| 825 | CATGPT | CATGPT | à vérifier | à vérifier (sommet le 2026-09-12) | ≈ 19 M$, 2026-09-12 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `catgpt-3` ; https://www.coingecko.com/en/coins/catgpt-3 |
| 826 | CorgiCoin | à vérifier | Solana | 2021 | ≈ 19 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 586 ; CG `corgicoin` |
| 827 | DNA | DNA | à vérifier | à vérifier (sommet le 2024-12-06) | ≈ 19 M$, 2024-12-06 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `dna` ; https://www.coingecko.com/en/coins/dna |
| 828 | Fish | FISH | TON | 2024 | ≈ 19 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 359 |
| 829 | Flying Avocado Cat | FAC | à vérifier | à vérifier (sommet le 2024-09-20) | ≈ 19 M$, 2024-09-20 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `flying-avocado-cat` ; https://www.coingecko.com/en/coins/flying-avocado-cat |
| 830 | Flying Ketamine Horse | FKH | Solana | 25/11/2025 | ≈ 19 M$ (31/12/2025) | estimé | mort (≈ 25 k$, volume nul) | Cheval sous kétamine absurde, lancé sur la plateforme de Bonk ; pic à la Saint-Sylvestre juste avant l'année du Cheval, puis rien. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/flying-ketamine-horse/ |
| 831 | FREN | FREN | Cardano | mars 2024 (ajout CMC) | ≈ 19 M$ (déc. 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | FREN, mème Pepe/Peepos de Cardano. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/fren-ada-peepos/ ; https://www.coingecko.com/en/coins/ada-peepos |
| 832 | Kabosu Inu | KABOSU | à vérifier | à vérifier (sommet le 2024-05-23) | ≈ 19 M$, 2024-05-23 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `kabosu-inu` ; https://www.coingecko.com/en/coins/kabosu-inu |
| 833 | Kira the Injective Cat | KIRA | Injective | déc. 2023 (ajout CMC) | ≈ 19 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Kira, chat d'Injective (déc. 2023), premier mème de la chaîne. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/kira-the-injective-cat/ ; https://www.coingecko.com/en/coins/kira-the-injective-cat |
| 834 | Morning Routine | ROUTINE | Solana | Mars 2025 | ≈ 19 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 360 ; correction r3 ; CG `morning-routine` |
| 835 | PlutoPepe | PLUTO | BNB Chain | mai 2021 (ajout CMC) | ≤ 19 M$ en FDV (6 juin 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Pepe sur Pluton, mai 2021 : un Pepe BSC deux ans avant la folie PEPE ; coté un mois. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/plutopepe/ ; https://coinmarketcap.com/historical/20210606/ |
| 836 | Shibwifhatcoin | SHIB | à vérifier | à vérifier (sommet le 2024-03-11) | ≈ 19 M$, 2024-03-11 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `shibwifhatcoin` ; https://www.coingecko.com/en/coins/shibwifhatcoin |
| 837 | Success Kid (Solana) | SKID | Solana | mars 2024 | ≈ 19,0 M$ (20 mars 2024) | estimé | mort | Le bébé au poing serré du mème Success Kid ; ~19 M$ le 20/03/2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/success-kid-sol/ ; https://dexscreener.com/solana/9X2RHtKrBzw3SLYe9E88cBd1kz5RfU1f4JTSn4aRH43d |
| 838 | Tyler | TYLER | Base | 2024 | ≈ 19 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 779 ; CG `tyler-2` |
| 839 | Walter | WALTER | à vérifier | à vérifier (sommet le 2024-06-01) | ≈ 19 M$, 2024-06-01 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `walter-dog-solana` ; https://www.coingecko.com/en/coins/walter-dog-solana |
| 840 | YEETI 液体 | YEETI | Hyperliquid (HIP-1) | à vérifier (sommet le 14 déc. 2024) | ≈ 19,0 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Secte à lunettes Hyperliquid, record mi-déc. 2024, -99,6 %. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/yeeti |
| 841 | CatzCoin | CATZ | BSC | avr. 2021 | ≈ 18,4 M$ en FDV (18/05/2021) | estimé | mort | Mème chat sur BSC, lancé en avr. 2021 ; pic vers le 18/05/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/catzcoin/ |
| 842 | Akamaru Inu | AKAMARU | Ethereum | oct. 2021 | ≈ 18,3 M$ en FDV (01/11/2021) | estimé | mort | Jeton « Inu » inspiré d'Akamaru (Naruto) sur Ethereum, lancé en oct. 2021 ; pic vers le 01/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/akamaru-inu/ |
| 843 | build | BUILD | à vérifier | à vérifier (sommet le 2026-09-09) | ≈ 18 M$, 2026-09-09 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `build-5` ; https://www.coingecko.com/en/coins/build-5 |
| 844 | COAL | COAL | à vérifier | à vérifier (sommet le 2025-11-09) | ≈ 18 M$, 2025-11-09 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `coal-2` ; https://www.coingecko.com/en/coins/coal-2 |
| 845 | Echelon Token | ELON | à vérifier | à vérifier (sommet le 2026-02-02) | ≈ 18 M$, 2026-02-02 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `echelon-token` ; https://www.coingecko.com/en/coins/echelon-token |
| 846 | Elite (1337) | 1337 | blockchain propre | nov. 2015 | ≈ 18,0 M$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin au ticker « 1337 » (leet speak) ; ≈ 18 M$ début janvier 2018, puis fondu à quelques k$. | commune | rare |  | à définir | r1 ; https://coinmarketcap.com/historical/20180107/ ; https://coinmarketcap.com/currencies/1337coin/ |
| 847 | GLORP | GLORP | Solana (à confirmer) | Aliens, 2025-2026 | ≈ 18 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 364 ; correction r3 ; CG `glorp` |
| 848 | Leopard | LEOPARD | à vérifier | à vérifier (sommet le 2021-10-16) | ≈ 18 M$, 2021-10-16 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `leopard` ; https://www.coingecko.com/en/coins/leopard |
| 849 | Luffy | LUFFY | à vérifier | à vérifier (sommet le 2024-12-13) | ≈ 18 M$, 2024-12-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `luffy-inu` ; https://www.coingecko.com/en/coins/luffy-inu |
| 850 | ORC | ORC | à vérifier | à vérifier (sommet le 2024-07-21) | ≈ 18 M$, 2024-07-21 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `orc` ; https://www.coingecko.com/en/coins/orc |
| 851 | RealGOAT | RGOAT | Base | juin 2024 (ajout CMC) | ≈ 18 M$ (13 oct. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | « RealGOAT », chèvre de Base (juin 2024) ; ≈ 18 M$ mi-oct. 2024. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/real-goat/ ; https://www.coingecko.com/en/coins/realgoat |
| 852 | TOES | TOESCOIN | Solana | 19/05/2026 | ≈ 18 M$ (20/06/2026) | estimé | mort (≈ 45 k$) | Dix orteils pédicurés dans une bague en or : le mème « chic » de l'été 2026, effacé ensuite. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/toes/ |
| 853 | Dogecoin 2.0 | DOGE2 | BSC | avr. 2021 | ≈ 17,7 M$ en FDV (03/09/2021) | estimé | mort | « Dogecoin 2.0 » sur BSC (2021), désavoué publiquement par la Dogecoin Foundation pour usurpation de nom ; pic en sept. 2021, plus coté. | commune | commune |  | à définir | r2 ; https://cryptoslate.com/much-copy-so-deceive-dogecoin-foundation-warns-of-dogecoin-2-0-crypto-project/ ; https://coinmarketcap.com/currencies/dogecoin-2/ |
| 854 | Young Peezy AKA Pepe | PEEZY | Base | mars 2024 | ~17,5 M$ (date inconnue) | estimé | mort | Pepe version rappeur de la vague Base de mars 2024, il pèse 0,25 M$. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/young-peezy-aka-pepe |
| 855 | Myra | MYRA | Solana | janv. 2024 | ≈ 17,3 M$ (20 janv. 2024) | estimé | mort | Présentée comme la « sœur » de Myro ; ~17 M$ en janvier 2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/myra/ ; https://dexscreener.com/solana/H1aN3vcvB68eaFPbMkoAss3vnfi4AhP5C2dpnrZzdBc7 |
| 856 | AAA Cat | AAA | Sui | fin 2024 | ≈ 17 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 367 |
| 857 | Baby Neiro | BABYNEIRO | à vérifier | à vérifier (sommet le 2024-11-19) | ≈ 17 M$, 2024-11-19 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `baby-neiro-2` ; https://www.coingecko.com/en/coins/baby-neiro-2 |
| 858 | BOBER | BOBER | MultiversX | sept. 2024 (ajout CMC) | ≈ 17 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Bober, castor du mème polonais « bóbr », sur MultiversX (2024). | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/bober/ ; https://www.coingecko.com/en/coins/bober |
| 859 | BullDogito | BDOGITO | à vérifier | janv. 2025 | ≈ 17 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 376 ; CG `bulldogito` |
| 860 | Chadimir Putni | PUTNI | à vérifier | à vérifier (sommet le 2024-03-25) | ≈ 17 M$, 2024-03-25 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare | politique | à définir | R5 C1 `chadimir-putni` ; https://www.coingecko.com/en/coins/chadimir-putni |
| 861 | Coinye West | COINYE | Base | mars 2024 (ajout CMC) | ≈ 17 M$ (28 avr. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Coinye West, résurrection sur Base (mars 2024) du Coinye de 2014 qui moquait Kanye West ; ≈ 16 M$ fin avril 2024. | commune | rare | personne réelle | à définir | r4 ; https://coinmarketcap.com/currencies/coinye-west/ ; https://www.coingecko.com/en/coins/coinye-west |
| 862 | Floppa | FLOPPA | à vérifier | à vérifier (sommet le 2024-11-15) | ≈ 17 M$, 2024-11-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `floppa-cat` ; https://www.coingecko.com/en/coins/floppa-cat |
| 863 | Gemini | GEMINI | à vérifier | à vérifier (sommet le 2024-12-15) | ≈ 17 M$, 2024-12-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `gemini-2` ; https://www.coingecko.com/en/coins/gemini-2 |
| 864 | Grimace | GRIMACE | Arbitrum | mars 2024 (ajout CMC) | ≤ 17 M$ en FDV (24 mars 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Grimace, le monstre violet de McDonald's, version Arbitrum (mars 2024). | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/grimace-doge/ ; https://coinmarketcap.com/historical/20240324/ |
| 865 | HAHA | HAHA | à vérifier | à vérifier (sommet le 2023-05-06) | ≈ 17 M$, 2023-05-06 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `haha` ; https://www.coingecko.com/en/coins/haha |
| 866 | Lord Of SOL | LOS | à vérifier | à vérifier (sommet le 2024-05-10) | ≈ 17 M$, 2024-05-10 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `lord-of-sol` ; https://www.coingecko.com/en/coins/lord-of-sol |
| 867 | LOUD | LOUD | Solana | 2025 (à vérifier) | ≈ 17 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 807 ; CG `loud` |
| 868 | NearKat | NEARKAT | NEAR (aussi Solana) | sept. 2026 | ≈ 17 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 371 ; CG `nearkat-2` |
| 869 | OneCOW | 1COW | à vérifier | à vérifier (sommet le 2026-09-27) | ≈ 17 M$, 2026-09-27 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `onecow` ; https://www.coingecko.com/en/coins/onecow |
| 870 | Pepe Trump | PTRUMP | à vérifier | à vérifier (sommet le 2024-05-28) | ≈ 17 M$, 2024-05-28 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare | politique | à définir | R5 C1 `pepe-trump` ; https://www.coingecko.com/en/coins/pepe-trump |
| 871 | SPIKE | SPIKE | Solana | 08/04/2026 | ≈ 17 M$ (26/04/2026) | estimé | mort (≈ 29 k$) | Présenté comme le tout premier personnage de Matt Furie, avant Pepe ; promis « nouveau Pepe », mort en un mois. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/spikemattfurie/ |
| 872 | Strategic Super Reserve | SSR | à vérifier | sept. 2025 | ≈ 17 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 357 ; CG `strategic-solana-reserve` |
| 873 | Toad Killer | TOAD | à vérifier | à vérifier (sommet le 2023-08-16) | ≈ 17 M$, 2023-08-16 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `toad-killer` ; https://www.coingecko.com/en/coins/toad-killer |
| 874 | Ucan fix life in1day | 1 | BNB Chain | 18/01/2026 | ≈ 17-21 M$ (20/01/2026) | estimé | mort (≈ 0,3 M$) | « Réparer toute ta vie en un jour » : mème de développement personnel ; pic en deux jours. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/u-can-fix-life-in-1-day/ |
| 875 | Velvet Unicorn by Virtuals | VU | à vérifier | à vérifier (sommet le 2024-12-31) | ≈ 17 M$, 2024-12-31 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `velvet-unicorn-by-virtuals` ; https://www.coingecko.com/en/coins/velvet-unicorn-by-virtuals |
| 876 | Yeet | YEET | Berachain | 2025 | ≈ 17 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 796 ; CG `yeet` |
| 877 | Dogey-Inu | DINU | Ethereum | avr. 2021 | ≈ 16,7 M$ (15/11/2021) | sourcé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en avr. 2021 ; pic vers le 15/11/2021 ; aujourd'hui -99,81 %. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/dogey-inu/ |
| 878 | Normilio | NORMILIO | Base | inconnu | ~16,7 M$ (date inconnue) | estimé | mort | Le coin « le plus normal » de Base, il est tombé à 34 k$ avec 0,06 $ de volume par jour. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/normilio |
| 879 | Autist | AUTIST | Hyperliquid (HIP-1) | à vérifier (sommet le 8 déc. 2024) | ≈ 16,6 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Pepe autiste coiffé du logo Hyperliquid, record le 8 déc. 2024, mort. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/autist |
| 880 | CumStar | CUMSTAR | Ethereum | juil. 2021 | ≈ 16,4 M$ (18/11/2021) | sourcé | mort | Mème sur Ethereum, lancé en juil. 2021 ; pic vers le 18/11/2021 ; aujourd'hui plus coté. | commune | rare | obscène | à définir | r2 ; https://coinmarketcap.com/currencies/cumstar/ |
| 881 | Weirdo | WEIRDO | Base | mai 2024 | ~16,2 M$ (date inconnue) | estimé | mort | Mème « weirdo » du printemps 2024, migré vers un nouveau contrat, il fait 9 $ de volume par jour. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/weirdo-2 |
| 882 | Tiki Token | TIKI | BSC | juin 2021 | ≈ 16,1 M$ en FDV (07/07/2021) | estimé | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs), versant des BNB sur BSC, lancé en juin 2021 ; pic vers le 07/07/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/tiki-token/ |
| 883 | BUILD | BUILD | à vérifier | à vérifier (sommet le 2025-01-15) | ≈ 16 M$, 2025-01-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `build-4` ; https://www.coingecko.com/en/coins/build-4 |
| 884 | Dogecoin20 | DOGE20 | Ethereum | 2024 (prévente 2023-2024) | ≈ 16 M$ (07/05/2024) | estimé | mort | Prévente « Doge en ERC-20 avec staking », très promue, puis chute dès la cotation. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/dogecoin20 |
| 885 | Fish N Chips | CHIPPY | à vérifier | à vérifier (sommet le 2024-05-19) | ≈ 16 M$, 2024-05-19 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `fish-n-chips` ; https://www.coingecko.com/en/coins/fish-n-chips |
| 886 | Fishkoin | KOIN | à vérifier | à vérifier (sommet le 2024-03-24) | ≈ 16 M$, 2024-03-24 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `fishkoin` ; https://www.coingecko.com/en/coins/fishkoin |
| 887 | Galaxy Fox | GFOX | à vérifier | à vérifier (sommet le 2024-05-08) | ≈ 16 M$, 2024-05-08 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `galaxy-fox` ; https://www.coingecko.com/en/coins/galaxy-fox |
| 888 | Hachi | HACHI | à vérifier | à vérifier (sommet le 2024-04-21) | ≈ 16 M$, 2024-04-21 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `hachi` ; https://www.coingecko.com/en/coins/hachi |
| 889 | Jester | JEST | à vérifier | à vérifier (sommet le 2024-08-22) | ≈ 16 M$, 2024-08-22 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `jester` ; https://www.coingecko.com/en/coins/jester |
| 890 | Little Ugly Duck | LUD | à vérifier | à vérifier (sommet le 2021-08-17) | ≈ 16 M$, 2021-08-17 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `little-ugly-duck` ; https://www.coingecko.com/en/coins/little-ugly-duck |
| 891 | Mellow Man | MELLOW | à vérifier | à vérifier (sommet le 2024-08-21) | ≈ 16 M$, 2024-08-21 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `mellow-man` ; https://www.coingecko.com/en/coins/mellow-man |
| 892 | Nikepig | NIKEPIG | à vérifier | à vérifier (sommet le 2024-06-26) | ≈ 16 M$, 2024-06-26 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `nikepig` ; https://www.coingecko.com/en/coins/nikepig |
| 893 | NSDQ420 | NSDQ | à vérifier | à vérifier (sommet le 2025-01-06) | ≈ 16 M$, 2025-01-06 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `nsdq420` ; https://www.coingecko.com/en/coins/nsdq420 |
| 894 | PMX500 | PMX | à vérifier | à vérifier (sommet le 2025-08-23) | ≈ 16 M$, 2025-08-23 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `pmx500` ; https://www.coingecko.com/en/coins/pmx500 |
| 895 | Povel Durev | DUREV | TON | 2024 | ≈ 16 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 719 ; CG `povel-durev` |
| 896 | RAT Escape | RAT | à vérifier | à vérifier (sommet le 2024-12-12) | ≈ 16 M$, 2024-12-12 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `rat-escape` ; https://www.coingecko.com/en/coins/rat-escape |
| 897 | SPARTA | SPARTA | à vérifier | à vérifier (sommet le 2025-09-12) | ≈ 16 M$, 2025-09-12 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `sparta-2` ; https://www.coingecko.com/en/coins/sparta-2 |
| 898 | You Looked | CIRCLE | Solana | janv. 2024 | ≈ 16,0 M$ (8 mars 2024) | estimé | mort | Le jeu du cercle (« You looked ») ; ~16 M$ en mars 2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/you-looked/ ; https://dexscreener.com/solana/EkHr62PC6Y1axrLS7cR8YC4BZeW19mtHxQLCLMrf9vnq |
| 899 | Eggdog | EGG | Solana | déc. 2023 | ≈ 15,9 M$ (25 déc. 2023) | estimé | mort | Chien en forme d'œuf ; ~16 M$ à Noël 2023. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/eggdog/ ; https://dexscreener.com/solana/EXA537HSBVpsFijENbt6Muuy9AADUN8dUmYKD4oKbjJE |
| 900 | Santa Inu | SANINU | BSC | nov. 2021 | ≈ 15,9 M$ en FDV (21/11/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») de Noël sur BSC, lancé en nov. 2021 ; pic vers le 21/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/santa-inu/ |
| 901 | MetaDoge | METADOGEV2 | BSC | nov. 2021 | ≈ 15,6 M$ en FDV (19/12/2021) | estimé | mort | Clone de Dogecoin « métavers » sur BSC, lancé en nov. 2021 ; pic vers le 19/12/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/metadoge/ |
| 902 | All Will Retire | AWR | à vérifier | à vérifier (sommet le 2025-01-25) | ≈ 15 M$, 2025-01-25 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `all-will-retire` ; https://www.coingecko.com/en/coins/all-will-retire |
| 903 | Aped | APED | à vérifier | à vérifier (sommet le 2024-11-14) | ≈ 15 M$, 2024-11-14 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `aped` ; https://www.coingecko.com/en/coins/aped |
| 904 | Biden Coin | BIDEN | à vérifier | à vérifier (sommet le 2025-07-06) | ≈ 15 M$, 2025-07-06 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare | politique | à définir | R5 C1 `biden-coin` ; https://www.coingecko.com/en/coins/biden-coin |
| 905 | Bitcoin on Base | BTCB | à vérifier | déc. 2024 | ≈ 15 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 375 ; correction r3 ; CG `bitcoin-on-base` |
| 906 | DEBT | DEBT | Solana | letsbonk, 2025 | ≈ 15 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 382 ; correction r3 ; CG `debt` |
| 907 | Draggy CTO | DRAGGY | à vérifier | à vérifier (sommet le 2024-07-12) | ≈ 15 M$, 2024-07-12 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `draggy-cto` ; https://www.coingecko.com/en/coins/draggy-cto |
| 908 | GDOG | GDOG | à vérifier | à vérifier (sommet le 2024-10-28) | ≈ 15 M$, 2024-10-28 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `gdog` ; https://www.coingecko.com/en/coins/gdog |
| 909 | Lobstar | LOBSTAR | Solana | 20/02/2026 | ≈ 15-17 M$ (21-23/02/2026) | estimé | mort (≈ 44 k$) | Mème homard de la vague OpenClaw de fév. 2026, lié à un agent IA sur X (à vérifier) ; 15 M$ en trois jours, puis -99,7 %. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/lobstar/ ; https://dexscreener.com/solana/AVF9F4C4j8b1Kh4BmNHqybDaHgnZpJ7W7yLvL7hUpump |
| 910 | Memelinked | MK | à vérifier | à vérifier (sommet le 2025-05-08) | ≈ 15 M$, 2025-05-08 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `memelinked` ; https://www.coingecko.com/en/coins/memelinked |
| 911 | Nitefeeder | NITEFEEDER | à vérifier | à vérifier (sommet le 2024-07-18) | ≈ 15 M$, 2024-07-18 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `nitefeeder` ; https://www.coingecko.com/en/coins/nitefeeder |
| 912 | Pochi Inu | POCHI | Ethereum | févr. 2022 | ≈ 15,0 M$ en FDV (06/02/2022) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en févr. 2022 ; pic vers le 06/02/2022 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/pochi-inu/ |
| 913 | Raydium Cat | RAYCAT | à vérifier | à vérifier (sommet le 2026-09-11) | ≈ 15 M$, 2026-09-11 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `raydium-cat` ; https://www.coingecko.com/en/coins/raydium-cat |
| 914 | Snibbu | SNIBBU | à vérifier | à vérifier (sommet le 2024-04-01) | ≈ 15 M$, 2024-04-01 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `snibbu` ; https://www.coingecko.com/en/coins/snibbu |
| 915 | 黑马 (Cheval noir) | 黑马 | BNB Chain | 09/01/2026 | ≈ 15 M$ (13/01/2026) | estimé | mort (≈ 0,3 M$) | « Outsider » en chinois, lancé dans la vague des mèmes chinois et des mèmes cheval de janvier 2026 ; pic en quatre jours. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/darkhorse/ |
| 916 | DogeMoon | DGMOON | BSC | août 2021 | ≈ 14,8 M$ en FDV (14/05/2021) | estimé | mort | Clone de Dogecoin sur BSC, lancé en août 2021 ; pic vers le 14/05/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/dogemoon/ |
| 917 | Roost | ROOST | Base | mars 2024 | ≈ 14,8 M$ (23 juin 2024), sourcé (FDV max ≈ 68 M$) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 733 ; correction r4 ; CG `roost` ; https://coinmarketcap.com/currencies/roost-coin/ |
| 918 | BunnyCoin | BUN | blockchain propre | sept. 2014 | ≈ 14,7 M$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Clone scrypt « inspiré de Dogecoin » à lapin ; pic à ≈ 14,7 M$ en janv. 2018, puis inactif. | commune | rare |  | à définir | r1 ; https://coinmarketcap.com/historical/20180107/ ; https://coinmarketcap.com/currencies/bunnycoin/ |
| 919 | Crodie | CRODIE | Solana | mai 2024 | ≈ 14,7 M$ (10 mai 2024) | estimé | mort | Mème « Crodie » ; ~15 M$ le jour du lancement (10/05/2024). | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/crodie/ ; https://dexscreener.com/solana/GvcNXdSehfNSNyhDVDj27kc459LzFqWozt9CSJywMy6r |
| 920 | GhibliCZ | GHIBLI | BNB Chain | 27 mars 2025 | ≈ 14,6 M$ (mars 2025) | sourcé | mort (≈ 44 k$) | Version Ghibli de CZ sur BNB Chain, poussée sur les réseaux sociaux, puis abandonnée. | commune | rare | personne réelle | à définir | r3 ; https://coinmarketcap.com/academy/article/ghibli-style-ai-image-trend-triggers-40000percent-surge-in-solana-meme-coins ; https://www.coingecko.com/en/coins/ghiblicz |
| 921 | Mistery | MERY | Cronos (« Mistery On Cro ») | mai 2024 | ≈ 14,6 M$ (12 janv. 2025), sourcé | sourcé | mort |  | commune | rare |  | à définir | v1 n° 289 ; correction r4 ; CG `mistery` ; https://coinmarketcap.com/currencies/mistery-on-cro/ |
| 922 | Abble | AABL | Solana | avr. 2024 | ≈ 14,5 M$ (6 avr. 2024) | estimé | mort | Pomme « Abble » au dessin naïf ; ~14 M$ en avril 2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/abble/ ; https://dexscreener.com/solana/ENoD8J2J6wNHkcJkvVBkwq5JMiR1oNBfBZRkoHCQogyT |
| 923 | Amocucinare | AMORE | à vérifier | à vérifier (sommet le 2024-11-25) | ≈ 14 M$, 2024-11-25 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `amocucinare` ; https://www.coingecko.com/en/coins/amocucinare |
| 924 | ASTEROID | ASTEROID | à vérifier | à vérifier (sommet le 2026-09-10) | ≈ 14 M$, 2026-09-10 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `asteroid-3` ; https://www.coingecko.com/en/coins/asteroid-3 |
| 925 | Baby Neiro BNB | BABYNEIRO | BNB Chain | oct. 2024 (ajout CMC) | ≈ 14 M$ (24 nov. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Bébé Neiro sur BSC (oct. 2024), dérivé du chien Neiro devenu célèbre après la mort de Kabosu ; abandonné. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/baby-neiro-bnb/ ; https://coinmarketcap.com/historical/20241124/ |
| 926 | BananaCat | BCAT | à vérifier | à vérifier (sommet le 2024-11-28) | ≈ 14 M$, 2024-11-28 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `bananacat` ; https://www.coingecko.com/en/coins/bananacat |
| 927 | Belgian Malinois | BELG | BNB Chain | 05/10/2025 | ≈ 14 M$ (07/10/2025) | estimé | mort (≈ 33 k$) | Né d'une réponse de CZ : son chien n'est pas un shiba mais un malinois ; le dev affirme avoir donné 40 % de l'offre à Giggle Academy. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/belgian-malinois/ |
| 928 | Brent on SOL | BRENT | à vérifier | à vérifier (sommet le 2026-04-17) | ≈ 14 M$, 2026-04-17 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `brent-on-sol` ; https://www.coingecko.com/en/coins/brent-on-sol |
| 929 | FartStrategy | FSTR | à vérifier | à vérifier (sommet le 2025-01-30) | ≈ 14 M$, 2025-01-30 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `fartstrategy` ; https://www.coingecko.com/en/coins/fartstrategy |
| 930 | Good In The Hood | GOOD | à vérifier | à vérifier (sommet le 2026-08-27) | ≈ 14 M$, 2026-08-27 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `good-in-the-hood` ; https://www.coingecko.com/en/coins/good-in-the-hood |
| 931 | KittyCake | KCAKE | à vérifier | à vérifier (sommet le 2021-07-28) | ≈ 14 M$, 2021-07-28 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `kittycake` ; https://www.coingecko.com/en/coins/kittycake |
| 932 | Knot Diffie-Hellman | KNOT | à vérifier | à vérifier (sommet le 2024-12-10) | ≈ 14 M$, 2024-12-10 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `knot-diffie-hellman` ; https://www.coingecko.com/en/coins/knot-diffie-hellman |
| 933 | MoonDog AI | MDOGAI | à vérifier | janv. 2025 | ≈ 14 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 400 ; CG `moondog-ai` |
| 934 | SPYRO | SPYRO | à vérifier | à vérifier (sommet le 2024-02-15) | ≈ 14 M$, 2024-02-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `spyro` ; https://www.coingecko.com/en/coins/spyro |
| 935 | SZN | SZN | BNB Chain | 2025 | ≈ 14 M$ (sourcé) | sourcé | mort |  | commune | rare |  | à définir | v1 n° 387 ; correction r3 ; CG `szn` |
| 936 | Trash Coin | TRASH | à vérifier | à vérifier (sommet le 2025-07-23) | ≈ 14 M$, 2025-07-23 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `trash-coin` ; https://www.coingecko.com/en/coins/trash-coin |
| 937 | Treat Token | TREAT | à vérifier | à vérifier (sommet le 2024-03-06) | ≈ 14 M$, 2024-03-06 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `treat-token` ; https://www.coingecko.com/en/coins/treat-token |
| 938 | Jesus Coin (2017) | JC | Ethereum (ERC-20) | sept. 2017 | ≈ 13,9 M$, 18/02/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Parodie d'ICO « décentraliser Jésus », vente de sept. à déc. 2017 ; pic à ≈ 13,9 M$ à sa cotation en févr. 2018, -99 % fin 2018. Distinct du JESUS de 2023 (carte 148). | commune | rare |  | à définir | r1 ; https://coinmarketcap.com/historical/20180218/ ; https://thedailybeast.com/joke-cryptocurrencies-like-jesus-coin-are-making-serious-money |
| 939 | Suicy the Seal | SUICY | Sui | à vérifier (sommet le 14 déc. 2024) | ≈ 13,9 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Phoque mascotte de Sui, pic mi-déc. 2024, plus de volume. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/suicy-the-seal |
| 940 | BabyPepe | BABYPEPE | Ethereum | avr.-mai 2023 | ≈ 13,5 M$ (05/05/2023) | estimé | mort | Bébé Pepe de la première vague, même pic que tous les dérivés le 05/05/2023. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/babypepe |
| 941 | Lil Floki | LILFLOKI | BSC | sept. 2021 | ≈ 13,5 M$ en FDV (02/11/2021) | estimé | mort | Jeton né du chien Floki d'Elon Musk (tweet du 25/06/2021) sur BSC, lancé en sept. 2021 ; pic vers le 02/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/lil-floki/ |
| 942 | SUITRUMP | SUITRUMP | Sui | à vérifier (sommet le 23 mai 2025) | ≈ 13,4 M$ (mai 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | Trump version Sui, pic le 23 mai 2025 pendant le mini-rallye des mèmes Sui, puis -99 %. | commune | rare | politique | à définir | r4 ; https://www.coingecko.com/en/coins/sui-trump |
| 943 | Solana Shib | SSHIB | Solana | déc. 2023 | ≈ 13,3 M$ (24 déc. 2023) | estimé | mort | Copie Solana du Shiba Inu ; ~13 M$ à Noël 2023. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/solana-shib/ ; https://dexscreener.com/solana/6VHL2vMKgrF1YQFSv29Rs1pj9VCRK29bD11NtDqerqHA |
| 944 | BillionHappiness | BHC | BSC | sept. 2020 | ≈ 13,1 M$ (09/11/2021) | sourcé | mort | Mème « bonheur » de 2020 sur BSC, lancé en sept. 2020 ; pic vers le 09/11/2021 ; aujourd'hui -99,95 %. | commune | rare |  | à définir | r2 ; https://coinmarketcap.com/currencies/billionhappiness/ |
| 945 | Akitavax | AKITAX | Avalanche | déc. 2021 (ajout CMC) | ≤ 13 M$ en FDV (30 janv. 2022) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Akita d'Avalanche (janv. 2022), un des premiers mèmes chiens de la C-Chain. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/akitavax/ ; https://coinmarketcap.com/historical/20220130/ |
| 946 | ATEHUN | ATEHUN | à vérifier | déc. 2024 | ≈ 13 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 374 ; CG `atehun` |
| 947 | BabyKitty | BABYKITTY | à vérifier | à vérifier (sommet le 2021-12-30) | ≈ 13 M$, 2021-12-30 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `babykitty` ; https://www.coingecko.com/en/coins/babykitty |
| 948 | BarbieCrashBandicootRFK88 | SOLANA | à vérifier | à vérifier (sommet le 2023-10-26) | ≈ 13 M$, 2023-10-26 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `barbiecrashbandicootrfk88` ; https://www.coingecko.com/en/coins/barbiecrashbandicootrfk88 |
| 949 | BIG | BIG | Avalanche | déc. 2024 (ajout CMC) | ≈ 13 M$ (16 févr. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | BIG, mème Avalanche de déc. 2024 ; ≈ 13 M$ en févr. 2025. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/big/ ; https://coinmarketcap.com/historical/20250216/ |
| 950 | Capybara Token | CAPY | à vérifier | à vérifier (sommet le 2023-05-09) | ≈ 13 M$, 2023-05-09 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `capybara-token` ; https://www.coingecko.com/en/coins/capybara-token |
| 951 | CAT | CAT | à vérifier | à vérifier (sommet le 2024-05-27) | ≈ 13 M$, 2024-05-27 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `sol-cat` ; https://www.coingecko.com/en/coins/sol-cat |
| 952 | Didi Bam Bam | DDBAM | à vérifier | à vérifier (sommet le 2024-12-02) | ≈ 13 M$, 2024-12-02 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `didi-bam-bam` ; https://www.coingecko.com/en/coins/didi-bam-bam |
| 953 | DORK LORD | DORKL | Ethereum | 2023 | ≈ 13 M$ (08/09/2023) | estimé | mort | Mème du « seigneur des dorks » de l'univers Boy's Club, sommet en septembre 2023. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/dork-lord |
| 954 | HotDoge [OLD] | HOTDOGE | à vérifier | à vérifier (sommet le 2021-05-11) | ≈ 13 M$, 2021-05-11 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `hot-doge` ; https://www.coingecko.com/en/coins/hot-doge |
| 955 | HUA HUA | HUAHUA | à vérifier | à vérifier (sommet le 2024-12-04) | ≈ 13 M$, 2024-12-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `hua-hua` ; https://www.coingecko.com/en/coins/hua-hua |
| 956 | MindCoin | MIND | à vérifier | à vérifier (sommet le 2024-08-13) | ≈ 13 M$, 2024-08-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `mindcoin-2` ; https://www.coingecko.com/en/coins/mindcoin-2 |
| 957 | Mittens | MITTENS | TON | 2024-2026 | ≈ 13 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 675 ; CG `mittens-2` |
| 958 | NEKO | NEKO | NEAR | 2023 † | ≈ 13 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 696 ; CG `neko` |
| 959 | PIKA to PIKO ピカとピコ | PIKA | à vérifier | à vérifier (sommet le 2024-10-16) | ≈ 13 M$, 2024-10-16 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `pika-to-piko` ; https://www.coingecko.com/en/coins/pika-to-piko |
| 960 | remilio | REMILIO | à vérifier | à vérifier (sommet le 2024-05-07) | ≈ 13 M$, 2024-05-07 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `remilio` ; https://www.coingecko.com/en/coins/remilio |
| 961 | SatoshAI | SAI | à vérifier | à vérifier (sommet le 2026-08-01) | ≈ 13 M$, 2026-08-01 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `satoshai` ; https://www.coingecko.com/en/coins/satoshai |
| 962 | Señor Dip | DIP | Cronos | mai 2024 (ajout CMC) | ≤ 13 M$ en FDV (24 nov. 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Señor Dip, mème « buy the dip » de Cronos, mai 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/senor-dip/ ; https://coinmarketcap.com/historical/20241124/ |
| 963 | Shiba Classic | SHIBC | à vérifier | à vérifier (sommet le 2024-11-14) | ≈ 13 M$, 2024-11-14 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `shiba-classic-2` ; https://www.coingecko.com/en/coins/shiba-classic-2 |
| 964 | ShibKiller | SHIBKILLER | BSC | mars 2022 | ≈ 13,0 M$ en FDV (24/03/2022) | estimé | mort | Mème anti-SHIB sur BSC, lancé en mars 2022 ; pic vers le 24/03/2022 ; aujourd'hui -99,11 %. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/shibkiller/ |
| 965 | BOZO | BOZO | Solana | janv. 2024 | ≈ 12,8 M$ (20 janv. 2024) | estimé | mort | Clown « BOZO » ; ~13 M$ en janvier 2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/bozo/ ; https://dexscreener.com/solana/BoZoQQRAmYkr5iJhqo7DChAs7DPDwEZ5cv1vkYC9yzJG |
| 966 | ArbiDoge | ADOGE | Arbitrum | à vérifier (sommet le 8 mars 2024) | ≈ 12 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | ArbiDoge, Doge d'Arbitrum ; ressorti en mars 2024 avant de retomber. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/arbidoge |
| 967 | artificial gooner intelligence | AGI | à vérifier | à vérifier (sommet le 2026-09-06) | ≈ 12 M$, 2026-09-06 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare | obscène | à définir | R5 C1 `artificial-gooner-intelligence` ; https://www.coingecko.com/en/coins/artificial-gooner-intelligence |
| 968 | Baby Asteroid | BABYASTEROID | à vérifier | à vérifier (sommet le 2026-05-04) | ≈ 12 M$, 2026-05-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `baby-asteroid-2` ; https://www.coingecko.com/en/coins/baby-asteroid-2 |
| 969 | BEAMCAT | BCAT | Beam | à vérifier (sommet le 11 mars 2024) | ≈ 12 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | BEAMCAT, chat de la chaîne de jeu Beam, mars 2024. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/beamcat |
| 970 | Damoon Coin | DAMOON | Cronos | mai 2024 (ajout CMC) | ≤ 12 M$ en FDV (2 juin 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Damoon, mème lune de Cronos (mai 2024). | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/damoon-coin/ ; https://coinmarketcap.com/historical/20240602/ |
| 971 | Defi Tiger | DTG | à vérifier | août 2025 | ≈ 12 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 397 ; CG `defi-tiger` |
| 972 | DuckCoin | DUCK | TON | à vérifier (sommet le 9 mai 2024) | ≈ 12,0 M$ (mai 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Le canard, mascotte officielle de Telegram, en jeton TON ; annoncé top 20 de TON, record mai 2024, -99,6 %. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/duckcoin |
| 973 | Estee | ESTEE | à vérifier | à vérifier (sommet le 2024-09-30) | ≈ 12 M$, 2024-09-30 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `estee` ; https://www.coingecko.com/en/coins/estee |
| 974 | FARTGIRL | FARTGIRL | à vérifier | à vérifier (sommet le 2025-02-17) | ≈ 12 M$, 2025-02-17 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `fartgirl` ; https://www.coingecko.com/en/coins/fartgirl |
| 975 | Fefe | FEFE | à vérifier | à vérifier (sommet le 2024-10-17) | ≈ 12 M$, 2024-10-17 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `fefe-on-eth` ; https://www.coingecko.com/en/coins/fefe-on-eth |
| 976 | Gluteus Maximus by Virtuals | GLUTEU | à vérifier | à vérifier (sommet le 2025-01-15) | ≈ 12 M$, 2025-01-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `gluteus-maximus-by-virtuals` ; https://www.coingecko.com/en/coins/gluteus-maximus-by-virtuals |
| 977 | Golden Goose | GG | à vérifier | à vérifier (sommet le 2026-08-30) | ≈ 12 M$, 2026-08-30 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `golden-goose-2` ; https://www.coingecko.com/en/coins/golden-goose-2 |
| 978 | Gondola | GONDOLA | à vérifier | à vérifier (sommet le 2024-10-15) | ≈ 12 M$, 2024-10-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `gondola` ; https://www.coingecko.com/en/coins/gondola |
| 979 | LOL | LOL | Solana | 18/03/2026 | ≈ 12 M$ (01/04/2026) | estimé | mort (≈ 60 k$) | Mise en jeton du « LOL » universel ; pic le jour du poisson d'avril. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/lolonsol/ |
| 980 | Pistacio | PISTACIO | à vérifier | à vérifier (sommet le 2026-08-26) | ≈ 12 M$, 2026-08-26 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `pistacio` ; https://www.coingecko.com/en/coins/pistacio |
| 981 | Polly | POLLY | à vérifier | à vérifier (sommet le 2025-08-04) | ≈ 12 M$, 2025-08-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `pengus-wife` ; https://www.coingecko.com/en/coins/pengus-wife |
| 982 | Scam Altman | SCAM | à vérifier | à vérifier (sommet le 2026-04-28) | ≈ 12 M$, 2026-04-28 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare | personne réelle | à définir | R5 C1 `scam-altman` ; https://www.coingecko.com/en/coins/scam-altman |
| 983 | The Big Red | TD | Avalanche | mars 2024 (ajout CMC) | ≤ 12 M$ en FDV (24 mars 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | « The Big Red », mème rouge (couleur d'Avalanche), mars 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/the-big-red/ ; https://coinmarketcap.com/historical/20240324/ |
| 984 | Toby | TOBY | Base | à vérifier | ≈ 12 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 771 ; CG `toby-2` |
| 985 | Token6900 | T6900 | à vérifier | à vérifier (sommet le 2025-09-04) | ≈ 12 M$, 2025-09-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `token6900` ; https://www.coingecko.com/en/coins/token6900 |
| 986 | vankedisi | VANKEDISI | à vérifier | mai 2025 | ≈ 12 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 404 ; CG `vankedisi` |
| 987 | Wen Lambo | WEN | à vérifier | à vérifier (sommet le 2026-07-12) | ≈ 12 M$, 2026-07-12 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `wen-lambo-2` ; https://www.coingecko.com/en/coins/wen-lambo-2 |
| 988 | World Cup Coin | à vérifier | Solana | Mai 2026 | ≈ 12 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 394 ; correction r3 |
| 989 | Beeg Blue Whale | BEEG | Sui | à vérifier (sommet le 23 mai 2025) | ≈ 11,9 M$ (mai 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | Grosse baleine bleue de Sui, pic le 23 mai 2025, mort sans volume. | commune | rare |  | à définir | r4 ; https://www.coingecko.com/en/coins/beeg-blue-whale |
| 990 | Kermit (Solana) | KERMIT | Solana | mars 2024 | ≈ 11,8 M$ (20 mars 2024) | estimé | mort | Kermit la grenouille ; ~12 M$ le 20/03/2024, au lendemain de son lancement. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/kermit-frog/ ; https://dexscreener.com/solana/86AgpNnEbvBvqNocTrVLr4hg7gXpekp4BkjHYeHD6Nxm |
| 991 | Keisuke Inu | KEI | Ethereum | mai 2021 | ≈ 11,5 M$ en FDV (17/10/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en mai 2021 ; pic vers le 17/10/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/keisuke-inu/ |
| 992 | What in Tarnation? | WIT | Solana | avr. 2024 | ≈ 11,5 M$ (28 avr. 2024) | estimé | mort | Le mème western « What in tarnation? » ; ~11 M$ fin avril 2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/what-in-tarnation/ ; https://dexscreener.com/solana/Adq3wnAvtaXBNfy63xGV1YNkDiPKadDT469xF9uZPrqE |
| 993 | All Your Base | AYB | à vérifier | à vérifier (sommet le 2024-03-29) | ≈ 11 M$, 2024-03-29 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `all-your-base-2` ; https://www.coingecko.com/en/coins/all-your-base-2 |
| 994 | ARE YA WINNING, SON? | SON | à vérifier | à vérifier (sommet le 2025-08-13) | ≈ 11 M$, 2025-08-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `are-ya-winning-son` ; https://www.coingecko.com/en/coins/are-ya-winning-son |
| 995 | BASED | BASED | à vérifier | à vérifier (sommet le 2024-08-13) | ≈ 11 M$, 2024-08-13 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `based-2` ; https://www.coingecko.com/en/coins/based-2 |
| 996 | Binance Super Cycle | BSC | à vérifier | à vérifier (sommet le 2025-10-08) | ≈ 11 M$, 2025-10-08 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `binance-super-cycle` ; https://www.coingecko.com/en/coins/binance-super-cycle |
| 997 | Black Dragon | BLACKDRAGON | NEAR | 2024 † | ≈ 11 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | commune | rare |  | à définir | v1 n° 488 ; CG `black-dragon` |
| 998 | Doge 2.0 | DOGE2.0 | Ethereum | juil. 2023 | ≈ 11 M$ (07/07/2023) | estimé | mort | Copie « 2.0 » de Dogecoin dans le sillage de Pepe 2.0, morte en quelques jours. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/doge-2-0 |
| 999 | Dork Lord | DORKY | à vérifier | à vérifier (sommet le 2026-08-01) | ≈ 11 M$, 2026-08-01 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `dork-lord-2` ; https://www.coingecko.com/en/coins/dork-lord-2 |
| 1000 | HarryPotterTrumpHomerSimpson777Inu | ETHEREUM | à vérifier | à vérifier (sommet le 2024-03-03) | ≈ 11 M$, 2024-03-03 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `harrypottertrumphomersimpson777inu` ; https://www.coingecko.com/en/coins/harrypottertrumphomersimpson777inu |
| 1001 | Hund | HUND | à vérifier | à vérifier (sommet le 2024-04-02) | ≈ 11 M$, 2024-04-02 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `hund` ; https://www.coingecko.com/en/coins/hund |
| 1002 | Mark-2-Marquette | M2M | à vérifier | à vérifier (sommet le 2026-04-25) | ≈ 11 M$, 2026-04-25 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `mark-2-marquette` ; https://www.coingecko.com/en/coins/mark-2-marquette |
| 1003 | MEMENTO•MORI | MEMENTO | Bitcoin (Runes) | 2024 | ≈ 11 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° 408 |
| 1004 | Mommy Doge | MOMMYDOGE | à vérifier | à vérifier (sommet le 2021-07-11) | ≈ 11 M$, 2021-07-11 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `mommy-doge` ; https://www.coingecko.com/en/coins/mommy-doge |
| 1005 | PEPECASH | PECH | à vérifier | août 2025 | ≈ 11 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 401 ; CG `pepecash-3` |
| 1006 | Signal | SIGNAL | à vérifier | à vérifier (sommet le 2026-10-05) | ≈ 11 M$, 2026-10-05 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `signal-2` ; https://www.coingecko.com/en/coins/signal-2 |
| 1007 | Speedy | SPEEDY | Fantom | avr. 2024 (ajout CMC) | ≤ 11 M$ en FDV (21 avr. 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Speedy, mème de Fantom d'avril 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/speedy/ ; https://coinmarketcap.com/historical/20240421/ |
| 1008 | SquidGameToken | SGT | BSC | oct. 2021 | ≈ 11,0 M$ en FDV (30/10/2021) | estimé | mort | Copie du jeton SQUID sur BSC, tombée le même jour que l'original selon CoinDesk (01/11/2021) ; plus coté. | commune | commune |  | à définir | r2 ; https://www.coindesk.com/markets/2021/11/01/squid-game-token-crashes-developers-say-theyve-left-the-project/ ; https://coinmarketcap.com/currencies/squidgametoken/ |
| 1009 | Sweep Token | SWEEP | à vérifier | à vérifier (sommet le 2023-02-18) | ≈ 11 M$, 2023-02-18 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `sweep-token` ; https://www.coingecko.com/en/coins/sweep-token |
| 1010 | TOLY'S DOG | ADA | à vérifier | à vérifier (sommet le 2024-03-29) | ≈ 11 M$, 2024-03-29 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `ada-the-dog` ; https://www.coingecko.com/en/coins/ada-the-dog |
| 1011 | Transhuman Coin | THC | à vérifier | à vérifier (sommet le 2021-11-14) | ≈ 11 M$, 2021-11-14 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `transhuman-coin` ; https://www.coingecko.com/en/coins/transhuman-coin |
| 1012 | Vibe Cat | VIBE | à vérifier | à vérifier (sommet le 2025-06-19) | ≈ 11 M$, 2025-06-19 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `vibe-cat-3` ; https://www.coingecko.com/en/coins/vibe-cat-3 |
| 1013 | Viva | à vérifier | Solana | 2026 | ≈ 11 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 783 ; CG `viva-2` |
| 1014 | WISHBONE | WISHBONE | à vérifier | à vérifier (sommet le 2026-07-14) | ≈ 11 M$, 2026-07-14 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `wishbone` ; https://www.coingecko.com/en/coins/wishbone |
| 1015 | 雪球人生 (Vie boule de neige) | 雪球人生 | BNB Chain | 19/01/2026 | ≈ 11 M$ (23/04/2026) | estimé | mort (≈ 96 k$) | Clone « 人生 » de la lignée 币安人生, distinct de 雪球 ; un bref pic au printemps 2026. | commune | rare |  | à définir | r3 ; https://dexscreener.com/bsc/0x1a0d665fF8582fE135A8867BFd38b5e48bAF7777 |
| 1016 | AI Dragon | CHATGPT | Solana | févr. 2024 | ≈ 10,9 M$ (30 mars 2024) | estimé | mort | Dragon nommé « CHATGPT », suiveur de Silly Dragon ; ~11 M$ en mars 2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/ai-dragon/ ; https://dexscreener.com/solana/3J6ZAHwGvqhCYkBzeMjTBRhC56QnT7zcMPxYV4GAPjxu |
| 1017 | Pou | POU | Solana | mars 2024 | ≈ 10,8 M$ (15 mars 2024) | estimé | mort | La mascotte du jeu mobile Pou ; ~11 M$ le 15/03/2024. | commune | rare |  | à définir | r3 ; https://coinmarketcap.com/currencies/pou/ ; https://dexscreener.com/solana/PouWaap6bHZv1oT7T7rzRgQHTBD4nsWQRHGbB5hfDA6 |
| 1018 | All in Dollo | DOLLO | à vérifier | à vérifier (sommet le 2025-08-14) | ≈ 10 M$, 2025-08-14 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `all-in-dollo` ; https://www.coingecko.com/en/coins/all-in-dollo |
| 1019 | ASSDAQ | ASSDAQ | à vérifier | à vérifier (sommet le 2025-08-05) | ≈ 10 M$, 2025-08-05 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare | obscène | à définir | R5 C1 `assdaq` ; https://www.coingecko.com/en/coins/assdaq |
| 1020 | Bera Morning | BM | Berachain | 2025 | ≈ 10 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 561 ; CG `bm` |
| 1021 | Blue Kirby | KIRBY | Fantom | déc. 2023 (ajout CMC) | ≤ 10 M$ en FDV (17 mars 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Kirby bleu de Fantom, déc. 2023. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/blue-kirby/ ; https://coinmarketcap.com/historical/20240317/ |
| 1022 | CALI | CALI | à vérifier | à vérifier (sommet le 2026-09-27) | ≈ 10 M$, 2026-09-27 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `cali` ; https://www.coingecko.com/en/coins/cali |
| 1023 | Frog on ETH | FROG | Ethereum | 2024 (à vérifier) | ≈ 10 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 619 ; CG `frog-on-eth` |
| 1024 | Fronk | FRONK | Solana | 2024 | ≈ 10,0 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 620 ; CG `fronk` |
| 1025 | Froth | FROTH | à vérifier | oct. 2025 | ≈ 10 M$ (estimé CG) | estimé | mort |  | commune | rare |  | à définir | v1 n° 413 ; CG `froth` |
| 1026 | GBOY | GBOY | à vérifier | à vérifier (sommet le 2026-01-15) | ≈ 10 M$, 2026-01-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `gboy` ; https://www.coingecko.com/en/coins/gboy |
| 1027 | King Of Meme | LION | à vérifier | à vérifier (sommet le 2024-06-18) | ≈ 10 M$, 2024-06-18 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `king-of-meme` ; https://www.coingecko.com/en/coins/king-of-meme |
| 1028 | Matt Furie | MATT | à vérifier | à vérifier (sommet le 2024-07-15) | ≈ 10 M$, 2024-07-15 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `matt-0x79` ; https://www.coingecko.com/en/coins/matt-0x79 |
| 1029 | PREME Token | PREME | à vérifier | à vérifier (sommet le 2026-06-29) | ≈ 10 M$, 2026-06-29 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `preme-token` ; https://www.coingecko.com/en/coins/preme-token |
| 1030 | Puli Inu | PULI | BNB Chain | janv. 2022 (ajout CMC) | ≤ 10 M$ en FDV (10 avr. 2022) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Inu à l'effigie du puli hongrois, janv. 2022 ; mort depuis. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/puli-inu/ ; https://coinmarketcap.com/historical/20220410/ |
| 1031 | SurfMoon | SURFMOON | BSC | nov. 2021 | ≈ 10,0 M$ en FDV (14/11/2021) | estimé | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) sur BSC, lancé en nov. 2021 ; pic vers le 14/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/surfmoon/ |
| 1032 | Wagmi Coin | WAGMI | à vérifier | à vérifier (sommet le 2023-05-24) | ≈ 10 M$, 2023-05-24 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `wagmi-coin` ; https://www.coingecko.com/en/coins/wagmi-coin |
| 1033 | DOGWIFHOOD | WIF | TON | à vérifier (sommet le 1 avr. 2024) | ≈ 9,9 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Copie TON de dogwifhat (capuche), record le 1er avril 2024, -99,6 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/dogwifhood |
| 1034 | Official PPshow | PP | à vérifier | nov. 2025 | ≈ 9,9 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 414 ; CG `official-ppshow` |
| 1035 | Derp | DERP | Sonic | à vérifier (sommet le 28 févr. 2025) | ≈ 9,8 M$ (févr. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Derp, mème de Sonic (ex-Fantom), févr. 2025. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/derp-2 |
| 1036 | GameCow | GCOW | à vérifier | sept. 2026 | ≈ 9,8 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 418 ; CG `gamecow` |
| 1037 | PsyopAnime | PSYOPANIME | à vérifier | mars 2026 | ≈ 9,8 M$ (estimé CG) | estimé | en déclin |  | commune | commune |  | à définir | v1 n° 426 ; CG `psyopanime` |
| 1038 | Croakey | CROAK | Cronos | à vérifier (sommet le 3 mai 2024) | ≈ 9,7 M$ (mai 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Croakey, grenouille de Cronos, mai 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/croakey |
| 1039 | DooDoo | DOODOO | Aptos | à vérifier (sommet le 22 mars 2024) | ≈ 9,7 M$ (mars 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Mème caca d'Aptos, record à 2,25 $ le 22 mars 2024 pendant la saison des mèmes Aptos, -99 %. | commune | commune | obscène | à définir | r4 ; https://www.coingecko.com/en/coins/doodoo ; https://coinmarketcap.com/currencies/doodoo/ |
| 1040 | Shiba Inu Billionaire | SHIBIB | BSC | nov. 2021 | ≈ 9,7 M$ en FDV (15/11/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en nov. 2021 ; pic vers le 15/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/shiba-inu-billionaire/ |
| 1041 | Bingus Token | BINGUS | BNB Chain | avr. 2021 (ajout CMC) | ≤ 9,6 M$ en FDV (16 mai 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Hommage au chat sphynx Bingus, mème Internet de 2020, lancé pendant la ruée BSC d'avril-mai 2021 ; plus coté après sept. 2021. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/bingus-token/ ; https://coinmarketcap.com/historical/20210516/ |
| 1042 | CZ THE GOAT | CZGOAT | BNB Chain | 24/11/2023 | ≈ 9,6 M$ (12/12/2023) | estimé | mort (≈ 54 k$, volume nul) | Lancé trois jours après le plaider-coupable de CZ aux États-Unis, pour le sacrer « GOAT » ; mort après le pic de décembre. | commune | commune | personne réelle | à définir | r3 ; https://coinmarketcap.com/currencies/cz-the-goat/ |
| 1043 | Koreadoge | KDOGE | BSC | nov. 2021 | ≈ 9,6 M$ en FDV (12/11/2021) | estimé | mort | Clone de Dogecoin sur BSC, lancé en nov. 2021 ; pic vers le 12/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/koreadoge/ |
| 1044 | RONKE | RONKE | à vérifier | mars 2025 | ≈ 9,5 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 415 ; CG `ronke` |
| 1045 | AmazingDoge | ADOGE | BSC | mars 2022 | ≈ 9,4 M$ en FDV (30/04/2022) | estimé | mort | Clone de Dogecoin sur BSC, lancé en mars 2022 ; pic vers le 30/04/2022 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/amazingdoge/ |
| 1046 | Commander Vrax | VRAX | à vérifier | oct. 2026 | ≈ 9,4 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 419 ; CG `commander-vrax-2` |
| 1047 | Konan of Kaspa | KONAN | Kaspa (KRC-20) | à vérifier (sommet le 19 nov. 2024) | ≈ 9,4 M$ (nov. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Konan le Barbare version Kaspa, nov. 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/konan-of-kaspa |
| 1048 | Mars Inu | MARSINU | BSC | nov. 2021 | ≈ 9,4 M$ en FDV (16/11/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en nov. 2021 ; pic vers le 16/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/mars-inu/ |
| 1049 | LiteDoge | LDOGE | blockchain propre | 2014 | ≈ 9,3 M$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Fork « léger » de Dogecoin ; ≈ 9 M$ en janv. 2018, puis -99 %. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180107/ ; https://coinmarketcap.com/currencies/litedoge/ |
| 1050 | Beni | BENI | Base | mars 2024 | ~9,2 M$ (date inconnue) | estimé | mort | Mème du chien d'un dirigeant de Coinbase, lancé dans la ruée de mars 2024, il pèse 80 k$. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/beni |
| 1051 | Chinese Brett | CHRETT | Base | à vérifier (sommet le 11 juin 2024) | ≈ 9,2 M$ (juin 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | « Brett chinois », dérivé de BRETT (Boys' Club) sur Base, juin 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/chinese-brett |
| 1052 | DOGITA | DOGA | BNB Chain | à vérifier (sommet le 8 mai 2024) | ≈ 9,2 M$ (mai 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Doge « Dogita » de mai 2024 sur BSC ; pic le 8 mai 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/dogita |
| 1053 | DITGOLD | DITAU | à vérifier | sept. 2026 | ≈ 9,1 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 421 ; CG `ditgold` |
| 1054 | WONG | WONG | ApeChain | à vérifier (sommet le 2 janv. 2025) | ≈ 9,1 M$ (janv. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | WONG, mème d'ApeChain (janv. 2025). | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/wong |
| 1055 | bonkwifhat | BIF | Solana | févr. 2024 | ≈ 9,0 M$ (6 mars 2024) | estimé | mort | Croisement Bonk × dogwifhat ; ~9 M$ début mars 2024. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/bonkwifhat/ ; https://dexscreener.com/solana/BgQ2Tj4y4YQume4guQrkK8RWB8oRQtHYtAta1tXubL1G |
| 1056 | Hobbes [ancien contrat] | HOBBES | Ethereum | mars 2023 | ≈ 9 M$ (28/03/2023) | estimé | mort | Mème du tigre de Calvin et Hobbes, ancien contrat abandonné puis relancé en 2024. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/hobbes |
| 1057 | XRP20 | XRP20 | Ethereum | 2023 (prévente) | ≈ 9 M$ (24/08/2023) | estimé | mort | Prévente « XRP en ERC-20 », sortie à l'été 2023, volume quasi nul aujourd'hui. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/xrp20 |
| 1058 | Burt | BURT | Kaspa (KRC-20) | à vérifier (sommet le 24 oct. 2024) | ≈ 8,9 M$ (oct. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Burt, mème KRC-20 d'oct. 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/burt |
| 1059 | SHIBA ON BASE | SHIB | à vérifier | juil. 2025 | ≈ 8,9 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 424 ; CG `shiba-on-base` |
| 1060 | American Pepe | USPEPE | à vérifier | 2024 (à vérifier) | ≈ 8,8 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 536 ; CG `american-pepe` |
| 1061 | ANITA | ANITA | à vérifier | août 2025 | ≈ 8,8 M$ (estimé CG) | estimé | en déclin |  | commune | commune |  | à définir | v1 n° 420 ; CG `anita` |
| 1062 | B.H.A.D (Bhad Bhabie) | BHAD | Solana (pump.fun) | févr. 2025 | ≈ 8,8 M$ (févr. 2025) | sourcé | mort (≈ 9 k$) | La rappeuse lance son jeton « pour la recherche contre le cancer » ; il tombe vite à 365 k$, puis à presque rien. | commune | commune | personne réelle | à définir | r3 ; https://99bitcoins.com/news/watch-out-hawk-tuah-bhad-bhadie-launched-her-meme-coin/ ; https://www.coingecko.com/en/coins/b-h-a-d |
| 1063 | MILLI | MILLI | Sei | mars 2024 (ajout CMC) | ≈ 8,8 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle (CMC ne publie qu'à partir de plus tard : ≈ 4,1 M$ le 21 sept. 2025) | estimé | mort | MILLI, mème de Sei, mars 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/milli/ ; https://www.coingecko.com/en/coins/milli-coin |
| 1064 | PulseTrailerPark | PTP | PulseChain | à vérifier (sommet le 1 mars 2024) | ≈ 8,8 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | PulseTrailerPark, mème « camping-car » de PulseChain, mars 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/pulsetrailerpark |
| 1065 | Monkey Cult | MOLT | Solana | 19/02/2026 | ≈ 8,7 M$ (22/03/2026) | estimé | mort (≈ 75 k$, volume nul) | « Une secte qui se forme en public » : un singe qui reprend le ticker MOLT en pleine mode Moltbook. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/monkey-cult/ |
| 1066 | Perry | PERRY | BNB Chain | févr. 2025 (ajout CMC) | ≈ 8,7 M$ (23 févr. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Perry, mème de la vague four.meme de févr. 2025 lancée par CZ ; pic le 23 févr. 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/perry-bnb/ ; https://www.coingecko.com/en/coins/perry |
| 1067 | Suiman | SUIMAN | Sui | à vérifier (sommet le 12 oct. 2024) | ≈ 8,7 M$ (oct. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Super-héros de Sui lancé en 2024, cité parmi les mèmes Sui à suivre, record oct. 2024 puis -99,7 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/suiman ; https://www.kucoin.com/learn/crypto/top-sui-memecoins-to-watch |
| 1068 | The Resistance Cat | RECA | TON | à vérifier (sommet le 16 mai 2024) | ≈ 8,7 M$ (mai 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Chat de la « résistance » pro-Durov, dans le sillage de Resistance Dog, record mai 2024, -99 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/the-resistance-cat |
| 1069 | DOUBT | DOUBT | à vérifier | août 2025 | ≈ 8,6 M$ (estimé CG) | estimé | en déclin |  | commune | commune |  | à définir | v1 n° 429 ; CG `doubt` |
| 1070 | Egg | EGG | HyperEVM | 2025 | ≈ 8,6 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 612 ; CG `egg-3` |
| 1071 | WIN界 | WIN界 | à vérifier | oct. 2026 | ≈ 8,6 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 425 ; CG `win-jie` |
| 1072 | Normus | NORMUS | Base | inconnu | ~8,4 M$ (date inconnue) | estimé | mort | Satellite de NORMIE sur Base, 0 $ de volume, il vaut 9 k$. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/normus |
| 1073 | Sacabam | SCB | Sui | à vérifier (sommet le 2 janv. 2024) | ≈ 8,4 M$ (janv. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Le poisson fossile Sacabambaspis, mème viral de 2023, en jeton Sui ; record le 2 janv. 2024, l'un des premiers mèmes de Sui. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/sacabam |
| 1074 | Brett's cat | BALT | Base | inconnu | ~8,3 M$ (date inconnue) | estimé | mort | Le « chat de Brett », satellite de BRETT, est à 0 $ de volume pour 19 k$ de capitalisation. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/brett-s-cat |
| 1075 | Zen AI | ZAI | à vérifier | mars 2025 | ≈ 8,3 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 428 ; CG `zen-ai` |
| 1076 | GREEN MORNING | GM | à vérifier | nov. 2026 | ≈ 8,2 M$ | estimé | à vérifier (homonyme sur CoinGecko, non rapproché) |  | commune | commune |  | à définir | v1 n° 427 |
| 1077 | Marvin On Base | MOB | Base | inconnu | ~8,2 M$ (date inconnue) | estimé | mort | Mème qui promettait une appli pour sauver les jetons « coincés » par le gaz, il ne se négocie plus et GoPlus le signale. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/marvin-on-base |
| 1078 | QUEEN POOIE | QUEEN2 | PulseChain | à vérifier (sommet le 11 févr. 2025) | ≈ 8,2 M$ (févr. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Queen Pooie, mème de PulseChain (févr. 2025). | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/queen-pooie |
| 1079 | Silly Duck | DUCK | Solana | janv. 2024 | ≈ 8,2 M$ (22 févr. 2024) | estimé | mort | Canard dérivé de Silly Dragon ; ~8 M$ début 2024. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/silly-duck/ ; https://dexscreener.com/solana/A2PRwGdS4ho2WGfb2gbWFTXoVGoDBhLEhJ14bGouqbyZ |
| 1080 | Blast Pepe | BEPE | Blast | mars 2024 (ajout CMC) | ≈ 8,1 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Pepe de Blast, mars 2024, au lancement du réseau. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/blast-pepe/ ; https://www.coingecko.com/en/coins/blast-pepe |
| 1081 | BULLSHARK | BSHARK | Sui | à vérifier (sommet le 23 mai 2025) | ≈ 8,1 M$ (mai 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | Jeton tiré du NFT Suifren Bullshark, pic mai 2025, plus rien depuis. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/bullshark |
| 1082 | Brian | BRIAN | Base | oct. 2024 | ~8,0 M$ (date inconnue) | estimé | mort | « Hulk croisé avec Brett », mème communautaire de l'automne 2024, il pèse 200 k$. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/brian |
| 1083 | ChubbyAkita | CAKITA | BNB Chain | à vérifier (sommet le 17 mai 2021) | ≈ 8,0 M$ (mai 2021) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Akita joufflu de mai 2021, mème BSC de la saison SafeMoon ; pic le 17 mai 2021. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/chubbyakita |
| 1084 | JINDO INU | JIND | BSC | mai 2021 | ≈ 8,0 M$ en FDV (30/05/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en mai 2021 ; pic vers le 30/05/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/jindo-inu/ |
| 1085 | Pink | PINK | Moonbeam | avr. 2024 (ajout CMC) | ≤ 8,0 M$ en FDV (14 avr. 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Pink, mème de Moonbeam (Polkadot), avril 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/pink/ ; https://coinmarketcap.com/historical/20240414/ |
| 1086 | XFROG | XFROG | X Layer | à vérifier (sommet le 15 sept. 2025) | ≈ 8,0 M$ (sept. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | XFROG, grenouille de X Layer (le L2 d'OKX), sept. 2025. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/xfrog |
| 1087 | Chiliz Inu | CHZINU | Chiliz | à vérifier (sommet le 6 avr. 2024) | ≈ 7,9 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Chiliz Inu, Inu de la chaîne des fan tokens, avril 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/chiliz-inu |
| 1088 | Lovely Inu | LOVELY | Ethereum | juil. 2021 | ≈ 7,9 M$ (22/02/2023) | sourcé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en juil. 2021 ; pic vers le 22/02/2023 ; aujourd'hui -99,96 %. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/lovely-inu/ |
| 1089 | Peepo (2024) | PEPO | Ethereum | 02/06/2024 | ≈ 7,9 M$ (13/11/2024) | estimé | mort | Relance 2024 du mème Peepo, petit pic en novembre 2024, puis rien. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/peepo-eth ; https://dexscreener.com/ethereum/0xD1B89856D82F978D049116eBA8b7F9Df2f342fF3 |
| 1090 | Perpetual Bitcoin | PB | à vérifier | juin 2026 | ≈ 7,9 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 432 ; CG `perpetual-bitcoin` |
| 1091 | Ton Inu | à vérifier | TON | 2024 | ≈ 7,9 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 773 ; CG `ton-inu` |
| 1092 | Baby Trump | BABYTRUMP | BNB Chain | févr. 2024 (ajout CMC) | ≈ 7,8 M$ (2 juin 2024) ; CMC, relevé hebdomadaire | sourcé | mort | « Baby Trump » BSC de la campagne présidentielle 2024 ; pic en juin 2024. | commune | commune | politique | à définir | r4 ; https://coinmarketcap.com/currencies/baby-trump-bnb/ ; https://www.coingecko.com/en/coins/baby-trump-bsc |
| 1093 | Binance Cat | BNBCAT | BNB Chain | 22/08/2026 | ≈ 7,8 M$ (23/08/2026) | estimé | en déclin (≈ 0,5 M$) | Hommage communautaire à « tous les chats qui ont représenté BNB » ; pic dès le lendemain du lancement. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/binance-cat/ |
| 1094 | RALPH | RALPH | Solana | Vague récente (date à vérifier) | ≈ 7,8 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 431 |
| 1095 | World Cat | WORLD CAT | World Chain | à vérifier (sommet le 8 sept. 2025) | ≈ 7,8 M$ (sept. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | World Cat, chat de World Chain (le réseau de World/Worldcoin), sept. 2025. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/world-cat |
| 1096 | PETRO PENGUINS | PENGO | à vérifier | oct. 2025 | ≈ 7,7 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 433 ; CG `petro-penguins` |
| 1097 | UpDog | UPDOG | BNB Chain | à vérifier (sommet le 11 mai 2021) | ≈ 7,7 M$ (mai 2021) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | « What's updog ? », blague Internet devenue jeton BSC en mai 2021 ; pic le 11 mai 2021. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/updog |
| 1098 | AMC (Solana) | AMC | Solana (à vérifier) | mai 2024 | ≈ 7,6 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 535 ; CG `amc-3` |
| 1099 | Mooncat | MCAT | Solana | Moonshot | ≈ 7,6 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 685 ; CG `mooncat-2` |
| 1100 | Shikoku Inu | SHIKO | BNB Chain | à vérifier (sommet le 6 juil. 2021) | ≈ 7,6 M$ (juil. 2021) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Inu à l'effigie du shikoku japonais, juillet 2021 ; pic le 6 juillet 2021. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/shikoku-inu |
| 1101 | Biao | BIAO | BNB Chain | mars 2025 (ajout CMC) | ≈ 7,5 M$ (20 avr. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | « Biao » (émoticône) version BSC, mars 2025 ; distinct du Biaoqing de Tron. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/biaocoinbnb/ ; https://coinmarketcap.com/historical/20250420/ |
| 1102 | Hedgy the hedgehog | HEDGY | Sonic | à vérifier (sommet le 2 déc. 2024) | ≈ 7,5 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Hedgy, hérisson de Sonic (clin d'œil à Sonic le hérisson), déc. 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/hedgy-the-hedgehog |
| 1103 | AIDOGE Stellar | AIDOGEXLM | Stellar | mai 2023 (ajout CMC) | ≤ 7,4 M$ en FDV (13 août 2023) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | AIDOGE, rare mème de Stellar (juin 2023), copie de l'AiDoge d'Arbitrum. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/aidoge-stellar/ ; https://coinmarketcap.com/historical/20230813/ |
| 1104 | Andrea Von Speed | VONSPEED | Solana | déc. 2023 | ≈ 7,4 M$ (19 janv. 2024) | estimé | mort | « Andrea Von Speed », personnage du streamer IShowSpeed ; ~7 M$ en janvier 2024. | commune | commune | personne réelle | à définir | r3 ; https://coinmarketcap.com/currencies/andrea-von-speed/ ; https://dexscreener.com/solana/DVzrCErBzydh92bBzSJX1dKwVvb4omwhrvNz8CwRyxxV |
| 1105 | Binancedog | BINANCEDOG | BNB Chain | 22/08/2024 | ≈ 7,4 M$ (23/08/2024) | estimé | mort (≈ 56 k$, volume nul) | Chien dont la photo avait été postée plusieurs fois par le compte X de Binance ; le dev a vendu, CTO sans lendemain. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/binancedog-token/ |
| 1106 | BIRDSPING | PING | Kaia (ex-Klaytn) | à vérifier (sommet le 11 oct. 2024) | ≈ 7,4 M$ (oct. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | BIRDSPING, mème de Kaia, oct. 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/birdsping |
| 1107 | Shiba Inu Empire | SHIBEMP | BNB Chain | à vérifier (sommet le 11 nov. 2021) | ≈ 7,4 M$ (nov. 2021) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | « Empire » Shiba de nov. 2021 sur BSC ; pic le 11 nov. 2021. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/shiba-inu-empire |
| 1108 | STARKNET BROTHER | BROTHER | Starknet | à vérifier (sommet le 1 déc. 2024) | ≈ 7,4 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | « Starknet Brother », mème de Starknet, déc. 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/starknet-brother |
| 1109 | Toilet Dust | TOILET | Sui | à vérifier (sommet le 29 avr. 2025) | ≈ 7,4 M$ (avr. 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | Mème scatologique « flush » de Sui, pic avril 2025, -99 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/toilet-dust |
| 1110 | Danzo | DANZO | Cardano | à vérifier (sommet le 7 déc. 2024) | ≈ 7,3 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Danzo, mème de Cardano, déc. 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/danzo |
| 1111 | Market Dominance | MD | à vérifier | juin 2025 | ≈ 7,3 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 435 ; CG `market-dominance` |
| 1112 | Pepe The Frog | PEPEBNB | BNB Chain | avr. 2023 (ajout CMC) | ≤ 7,3 M$ en FDV (7 mai 2023) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Copie BSC de Pepe en mai 2023, deux semaines après l'explosion de PEPE sur Ethereum ; disparue en août 2023. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/pepe-the-frog/ ; https://coinmarketcap.com/historical/20230507/ |
| 1113 | The Final Form Bull | CZ | à vérifier | sept. 2026 | ≈ 7,3 M$ (estimé CG) | estimé | en déclin |  | commune | commune |  | à définir | v1 n° 434 ; CG `the-final-form-bull` |
| 1114 | Harmonic Agent | HARMONIC | à vérifier | oct. 2026 | ≈ 7,2 M$ (estimé CG) | estimé | en déclin |  | commune | commune |  | à définir | v1 n° 436 ; CG `harmonic-agent` |
| 1115 | Wednesday Inu | WED | BNB Chain | avr. 2023 (ajout CMC) | ≤ 7,2 M$ en FDV (7 mai 2023) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Inu du mercredi (« it is Wednesday my dudes »), mai 2023 ; mort en déc. 2023. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/wednesday-inu/ ; https://coinmarketcap.com/historical/20230507/ |
| 1116 | Based Bario | BARIO | Base | 2024 | ≈ 7,1 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 554 ; CG `based-bario` |
| 1117 | GRIND | GRIND | Abstract | à vérifier (sommet le 12 août 2025) | ≈ 7,1 M$ (août 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | GRIND, mème d'Abstract (le L2 de Pudgy Penguins), août 2025. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/grind |
| 1118 | DogWifJob | JOB | à vérifier | nov. 2026 | ≈ 7,0 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 437 ; CG `dogwifjob` |
| 1119 | Papu Token | PAPU | BNB Chain | mai 2024 (ajout CMC) | ≤ 7,0 M$ en FDV (2 juin 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Mème BSC de mai 2024 ; pic en juillet 2024 puis abandon. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/papu-token/ ; https://coinmarketcap.com/historical/20240602/ |
| 1120 | RONIN | RONIN | à vérifier | août 2026 | ≈ 7,0 M$ (estimé CG) | estimé | en déclin |  | commune | commune |  | à définir | v1 n° 438 ; CG `ronin-2` |
| 1121 | BabyBonk | BABYBONK | à vérifier | sept. 2025 | ≈ 6,9 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 442 ; CG `babybonk-3` |
| 1122 | PUMPCORN | PUMPCORN | TON | à vérifier (sommet le 17 déc. 2024) | ≈ 6,9 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Mème lancé sur le Memepad de Blum, porté par le média Telegram Popcorn Today, record déc. 2024, -99,7 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/pumpcorn |
| 1123 | Smudge Cat | SMUDCAT | Base | à vérifier (sommet le 8 août 2023) | ≈ 6,9 M$ (août 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Smudge, le chat du mème « femme qui crie sur un chat », jeton Base d'août 2023 : un des tout premiers mèmes de Base. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/smudge-cat |
| 1124 | What's Updog | UPDOG | Solana | mars 2024 | ≈ 6,9 M$ (13 juin 2024) | estimé | mort | La blague « What's Updog? » ; ~7 M$ (clôture), ~13 M$ en séance au lancement (mars 2024). | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/whats-updog/ ; https://dexscreener.com/solana/HJ39rRZ6ys22KdB3USxDgNsL7RKiQmsC3yL8AS3Suuku |
| 1125 | 世界和平 (Paix mondiale) | 世界和平 | BNB Chain | 21/10/2025 | ≈ 6,9 M$ (22/10/2025) | estimé | mort (≈ 34 k$, volume nul) | Mème « paix dans le monde » à la colombe, lancé en fin de saison chinoise ; un seul jour de gloire. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/shijieheping/ |
| 1126 | Doge CEO | DOGECEO | BNB Chain | à vérifier (sommet le 17 avr. 2023) | ≈ 6,8 M$ (avr. 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Doge PDG de la vague d'avril 2023, quand Musk a mis le logo Doge sur Twitter ; pic le 17 avril 2023. | commune | commune | personne réelle | à définir | r4 ; https://www.coingecko.com/en/coins/doge-ceo |
| 1127 | Grok Cat | GROKCAT | BNB Chain | à vérifier (sommet le 6 avr. 2024) | ≈ 6,8 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Chat Grok d'avril 2024, mème BSC ; pic le 6 avril 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/grok-cat |
| 1128 | Just The Tip | TIPS | Solana | mars 2024 | ≈ 6,8 M$ (22 mars 2024) | estimé | mort | « Just The Tip », sous-entendu grivois ; ~7 M$ en mars 2024. | commune | commune | obscène | à définir | r3 ; https://coinmarketcap.com/currencies/just-the-tip/ ; https://dexscreener.com/solana/AK87oZM8ovFU14bq8mu4ufi5zsCPDbqqVvh5b6WHbUdL |
| 1129 | PIGU | PIGU | Sui | à vérifier (sommet le 30 nov. 2024) | ≈ 6,8 M$ (nov. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Petit mème de Sui, pic fin nov. 2024, plus de volume. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/pigu |
| 1130 | Greatest Meme Ever | GME | à vérifier | sept. 2026 | ≈ 6,7 M$ (estimé CG) | estimé | en déclin |  | commune | commune |  | à définir | v1 n° 440 ; CG `greatest-meme-ever` |
| 1131 | 错版马 (Cheval à l'erreur d'impression) | 哭哭马 | BNB Chain | 10/01/2026 | ≈ 6,7 M$ (14/01/2026) | estimé | mort (≈ 0,11 M$) | « Cheval qui pleure », mème viral de janvier 2026 sur un cheval imprimé de travers (origine à vérifier) ; il a duré quatre jours. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/crying-horse/ |
| 1132 | Corgidoge real estate payment | CORGI | BNB Chain | mai 2021 (ajout CMC) | ≤ 6,6 M$ en FDV (14 nov. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Corgidoge, mème qui prétendait payer de l'immobilier (mai 2021) ; plus aucun volume. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/corgidoge-real-estate-payment/ ; https://coinmarketcap.com/historical/20211114/ |
| 1133 | Mystery | MYSTERY | Ethereum | 21/04/2026 | ≈ 6,6 M$ (28/04/2026) | estimé | mort (≈ 22 k$, volume nul) | La grenouille curieuse des Night Riders de Matt Furie, mise en jeton dans la vague des personnages de Furie ; une semaine de vie. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/mystery-ridereth/ |
| 1134 | Oh no | OHNO | à vérifier | mars 2024 | ≈ 6,6 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 445 ; CG `oh-no` |
| 1135 | Zoomer | ZOOMER | Ethereum | 30/06/2023 | ≈ 6,6 M$ (01/03/2024) | estimé | mort | Wojak « zoomer » de l'été 2023, dernier sursaut début 2024, puis abandon. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/zoomer ; https://dexscreener.com/ethereum/0x0D505C03d30e65f6e9b4Ef88855a47a89e4b7676 |
| 1136 | Rage Guy | RAGEGUY | à vérifier | oct. 2026 | ≈ 6,5 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 441 ; CG `rage-guy` |
| 1137 | TON DOG | TDOG | TON | à vérifier (sommet le 7 juil. 2024) | ≈ 6,5 M$ (juil. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Chien de TON, record le 7 juil. 2024, -99,9 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/ton-dog |
| 1138 | Distracted Dudes | DUDE | Base | à vérifier (sommet le 12 avr. 2024) | ≈ 6,4 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Mème du « petit ami distrait » sur Base, avril 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/distracted-dudes |
| 1139 | Magicaltux | TUX | Optimism | à vérifier (sommet le 27 déc. 2023) | ≈ 6,4 M$ (déc. 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | MagicalTux, pseudo de Mark Karpelès (patron de Mt. Gox), devenu jeton Optimism en déc. 2023. | commune | commune | personne réelle | à définir | r4 ; https://www.coingecko.com/en/coins/magicaltux |
| 1140 | Memeerkat | MKAT | TON | à vérifier (sommet le 14 déc. 2024) | ≈ 6,4 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Suricate lancé le 26 nov. 2024, record mi-déc., mort depuis. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/memeerkat |
| 1141 | The Dons | DONS | BNB Chain | mai 2023 (ajout CMC) | ≈ 6,4 M$ (21 mai 2023) ; CMC, relevé hebdomadaire | sourcé | mort | Mème BSC de mai 2023 lancé dans la vague Pepe ; pic le 21 mai 2023. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/the-dons/ ; https://www.coingecko.com/en/coins/dons |
| 1142 | BankerCoinAda | BANK | Cardano | mai 2023 (ajout CMC) | ≤ 6,3 M$ en FDV (4 juin 2023) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Bankercoin, mème du banquier sur Cardano (juin 2023). | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/bankercoinada/ ; https://coinmarketcap.com/historical/20230604/ |
| 1143 | BNB Frog Inu | BNBFROG | à vérifier | mai 2026 | ≈ 6,3 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 443 ; CG `bnb-frog-inu` |
| 1144 | Boshi | BOSHI | Base | avr. 2024 | ~6,3 M$ (date inconnue) | estimé | mort | Mème communautaire d'avril 2024, il vaut 13 k$. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/boshi |
| 1145 | DUMBMONEY | DUMBMONEY | Solana | 2026 | ≈ 6,3 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | commune | commune |  | à définir | v1 n° 516 ; CG `dumb-money-3` |
| 1146 | Minu | MINU | BNB Chain | janv. 2024 (ajout CMC) | ≈ 6,3 M$ (25 févr. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Mème BSC de janv. 2024 ; pic fin févr. 2024 puis oubli. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/minu/ ; https://coinmarketcap.com/historical/20240225/ |
| 1147 | sunpepe | SUNPEPE | Tron (SunPump) | à vérifier (sommet le 25 août 2024) | ≈ 6,3 M$ (août 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Pepe version Justin Sun, lancé pendant la ruée SunPump d'août 2024 ; sommet le 25 août puis plus aucun volume. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/sunpepe |
| 1148 | Vibing Cat Coin | VIBECOIN | à vérifier | août 2026 | ≈ 6,3 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 447 ; CG `vibing-cat-coin` |
| 1149 | Baby 4 | BABY4 | à vérifier | oct. 2025 | ≈ 6,2 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 439 ; CG `baby-4` |
| 1150 | BEPE | BEPE | Chia | à vérifier (sommet le 18 juin 2025) | ≈ 6,2 M$ (juin 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | BEPE, Pepe de Chia (CAT), juin 2025. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/bepe-2 |
| 1151 | Baby Grok (babygrok.ai) | BABYGROK | BNB Chain | juil. 2025 (ajout CMC) | ≈ 6,1 M$ (3 août 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Bébé Grok de juillet 2025 sur BSC ; pic début août 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/baby-grok-ai/ ; https://www.coingecko.com/en/coins/baby-grok-5 |
| 1152 | BNB Tiger Inu | BNBTIGER | à vérifier | sept. 2025 | ≈ 6,1 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 444 ; CG `bnb-tiger-inu` |
| 1153 | LIZARD | LIZARD | Avalanche | janv. 2024 (ajout CMC) | ≤ 6,1 M$ en FDV (28 janv. 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Lézard d'Avalanche, janv. 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/lizard/ ; https://coinmarketcap.com/historical/20240128/ |
| 1154 | Choo Choo | CHOO | à vérifier | nov. 2026 | ≈ 6,0 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 449 ; CG `choo-choo` |
| 1155 | Dogs of Elon | DOE | à vérifier | 2021-2022 | ≈ 6,0 M$ (estimé CG) | estimé | mort |  | commune | commune | personne réelle | à définir | v1 n° 606 ; CG `dogs-of-elon` |
| 1156 | HODL | HODL | à vérifier | mai 2026 | ≈ 6,0 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 448 ; CG `hodl-7` |
| 1157 | Zeal | ZEAL | à vérifier | sept. 2026 | ≈ 6,0 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 451 ; CG `zeal-2` |
| 1158 | Biaoqing TRON | BIAO | Tron (SunPump) | à vérifier (sommet le 27 août 2024) | ≈ 5,9 M$ (août 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Mème « émoticône » chinois (biaoqing) de la saison SunPump, pic fin août 2024, mort depuis. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/biaoqing-tron |
| 1159 | Cartoon Money | CBUCKS | à vérifier | nov. 2026 | ≈ 5,9 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 469 ; CG `cartoon-money` |
| 1160 | Dagknight Dog | DOGK | Kaspa (KRC-20), à vérifier | oct. 2024 (ajout CMC) | ≈ 5,9 M$ (3 nov. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Chien « DAGKnight », du nom du protocole de consensus de Kaspa (oct. 2024) ; sorti du classement fin 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/dagknight-dog/ ; https://coinmarketcap.com/historical/20241103/ |
| 1161 | Dino | DINO | Base | à vérifier | ≈ 5,9 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 598 ; CG `dino-2` |
| 1162 | Unicorn Meat | W🍖 | à vérifier | avr. 2026 | ≈ 5,9 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 446 ; CG `unicorn-meat` |
| 1163 | Resistance Girl | REGI | TON | à vérifier (sommet le 10 juil. 2024) | ≈ 5,8 M$ (juil. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Autre déclinaison de la famille Resistance Dog, record juil. 2024, -99,6 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/resistance-girl |
| 1164 | Feels Good Man | FEELSGOOD | Solana | Moonshot | ≈ 5,7 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 617 ; CG `feels-good-man-3` |
| 1165 | Ginnan | GINNAN | Solana | 2024-2025 | ≈ 5,7 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 628 ; CG `ginnan` |
| 1166 | Jambo (meme-cooking) | JAMBO | NEAR | nov. 2025 | ≈ 5,7 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 803 ; CG `jambo-2` |
| 1167 | MOTION | MOTION | à vérifier | août 2026 | ≈ 5,7 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 450 ; CG `motion-6` |
| 1168 | NianNian | 年年 | à vérifier | oct. 2026 | ≈ 5,7 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 454 ; CG `niannian-2` |
| 1169 | OFFICIAL K-POP | KPOP | à vérifier | juil. 2025 | ≈ 5,7 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 457 ; CG `official-k-pop` |
| 1170 | TON Cats Jetton | CATS | TON | à vérifier (sommet le 11 avr. 2024) | ≈ 5,7 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Jeton des chats de TON, record le 11 avril 2024 (pic des mèmes TON), -98 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/ton-cats-jetton |
| 1171 | 2131KOBUSHIDE | 21 | Solana | 09/01/2026 | ≈ 5,6 M$ (27/01/2026) | estimé | mort (≈ 17 k$) | Tiré d'une phrase culte de l'internet japonais (« 21 ans, avec mes poings ! ») ; mort en quelques semaines. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/2131kobushide/ |
| 1172 | cat wif sword | SWORDCAT | à vérifier | oct. 2026 | ≈ 5,6 M$ (estimé CG) | estimé | en déclin |  | commune | commune |  | à définir | v1 n° 461 ; CG `cat-wif-sword-2` |
| 1173 | DogeShrek | DOGESHREK | Dogechain | à vérifier (sommet le 16 août 2022) | ≈ 5,6 M$ (août 2022) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Shrek × Doge sur Dogechain, août 2022, au lancement du réseau. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/dogeshrek |
| 1174 | Mantle Inu | MINU | Mantle | juil. 2023 (ajout CMC) | ≤ 5,6 M$ en FDV (10 mars 2024) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | Inu de Mantle, août 2023, juste après le lancement du réseau. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/mantle-inu/ ; https://coinmarketcap.com/historical/20240310/ |
| 1175 | Yup | YUP | Abstract | à vérifier (sommet le 28 janv. 2025) | ≈ 5,6 M$ (janv. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Yup, mème d'Abstract au lancement du réseau (janv. 2025). | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/yup-2 |
| 1176 | CATAMOTO | CATA | BNB Chain | avr. 2024 (ajout CMC) | ≈ 5,5 M$ (22 sept. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Chat « Satoshi » de BSC, avril 2024 ; pic en sept. 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/catamoto-cat/ ; https://coinmarketcap.com/historical/20240922/ |
| 1177 | Chog | CHOG | Monad | 2025 † | ≈ 5,5 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 581 ; CG `chog` |
| 1178 | Keanu | KEANU | Solana | Fin 2024 | ≈ 5,5 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 654 ; CG `keanu` |
| 1179 | MMM | MMM | TON | à vérifier (sommet le 18 mai 2024) | ≈ 5,5 M$ (mai 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Parodie de la pyramide MMM de Mavrodi (mème russe), record mai 2024, -99,6 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/mmm |
| 1180 | Nekonium | NUKO | blockchain propre | déc. 2017 | ≈ 5,5 M$, 31/12/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Coin japonais à chat (neko), fork d'Ethereum ; ≈ 5,5 M$ fin décembre 2017, -99,8 % un an plus tard. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20171231/ ; https://coinmarketcap.com/currencies/nekonium/ |
| 1181 | New FIST | FIST | BNB Chain | 11/10/2025 | ≈ 5,5 M$ (28/10/2025) | estimé | mort (≈ 0,1 M$, volume quasi nul) | Relance en mème d'une vieille communauté chinoise (« Pangu ») pendant la saison chinoise ; retombé en un mois. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/fist-four/ |
| 1182 | WHISKEY | WHISKEY | à vérifier | sept. 2025 | ≈ 5,5 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 455 ; CG `whiskey` |
| 1183 | LOXI | LOXI | à vérifier | août 2026 | ≈ 5,4 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 464 ; CG `loxi-2` |
| 1184 | Shroomy | SHROOMY | Ink | à vérifier (sommet le 30 août 2025) | ≈ 5,4 M$ (août 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Shroomy, champignon d'Ink (le L2 de Kraken), août 2025. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/shroomy |
| 1185 | Soulja Boy | SBOY | Solana | Célébrités, 2024 | ≈ 5,4 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 759 ; CG `soulja-coin` |
| 1186 | Whyyoutouzhele | LI | à vérifier | févr. 2025 | ≈ 5,4 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 456 ; CG `whyyoutouzhele` |
| 1187 | Anthropig | ANTHROPIG | à vérifier | sept. 2026 | ≈ 5,3 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 459 ; CG `anthropig` |
| 1188 | Chow Chow | CHOW | Ethereum | févr. 2021 | ≈ 5,3 M$ en FDV (11/05/2021) | estimé | mort | Mème chien chow-chow sur Ethereum, lancé en févr. 2021 ; pic vers le 11/05/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/chow-chow/ |
| 1189 | Sauce Inu | SAUCEINU | Hedera | à vérifier (sommet le 5 janv. 2024) | ≈ 5,3 M$ (janv. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Sauce Inu, dérivé du DEX SaucerSwap sur Hedera (janv. 2024). | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/sauce-inu |
| 1190 | WHALE | WHALE | à vérifier | nov. 2026 | ≈ 5,3 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 458 ; CG `whale-4` |
| 1191 | Golden Dragon | GD | à vérifier | sept. 2026 | ≈ 5,2 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 631 ; CG `golden-dragon` |
| 1192 | Monko | MONKO | Algorand | à vérifier (sommet le 31 janv. 2025) | ≈ 5,2 M$ (janv. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Monko, singe d'Algorand (janv. 2025) ; -93 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/monko |
| 1193 | REKT 2.0 | REKT | Base | oct. 2023 (ajout CMC) | ≈ 5,2 M$ (10 mars 2024) ; CMC, relevé hebdomadaire | sourcé | mort | REKT 2.0, relance sur Base du mème « rekt » ; pic en mars 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/rektcoin-new/ ; https://coinmarketcap.com/historical/20240310/ |
| 1194 | Shitzu † | SHITZU | NEAR | 2024 | ≈ 5,2 M$ (estimé CG) | estimé | mort |  | commune | commune | obscène | à définir | v1 n° 743 ; CG `shitzu` |
| 1195 | KekCoin | KEK | à vérifier | 2017 | ≈ 5,1 M$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin du mème « Kek » (culte de Pepe sur 4chan) ; ≈ 5 M$ en janv. 2018, -95 % fin 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180107/ ; https://coinmarketcap.com/currencies/kekcoin/ |
| 1196 | Morfey | MORFEY | TON | à vérifier (sommet le 11 avr. 2024) | ≈ 5,1 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Le chat des frères Durov en jeton TON, record le 11 avril 2024, -99,9 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/morfey |
| 1197 | Anoncoin | ANONCOIN | à vérifier | sept. 2026 | ≈ 5,0 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 462 ; CG `anoncoin-2` |
| 1198 | BNBXBT | BNBXBT | BNB Chain | févr. 2025 (ajout CMC) | ≈ 5,0 M$ (23 févr. 2025) ; CMC, relevé hebdomadaire | sourcé | en déclin | Mème BSC de févr. 2025, pendant le premier emballement four.meme ; pic le 23 févr. 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/bnbxbt/ ; https://www.coingecko.com/en/coins/bnbxbt |
| 1199 | Dark Cheems | TOTAKEKE | BNB Chain | juil. 2025 (ajout CMC) | ≈ 5,0 M$ (31 août 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Cheems « sombre » (Totakeke), juillet 2025 ; pic fin août 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/dark-cheems/ ; https://www.coingecko.com/en/coins/dark-cheems |
| 1200 | Golden Doge | GDOGE | BSC | juil. 2021 | ≈ 5,0 M$ en FDV (30/10/2021) | estimé | mort | Clone de Dogecoin sur BSC, lancé en juil. 2021 ; pic vers le 30/10/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/golden-doge/ |
| 1201 | Lonk | LONK | NEAR | 2023 † | ≈ 4,9 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | commune | commune |  | à définir | v1 n° 503 ; CG `lonk-on-near` |
| 1202 | Michi † | MICHI | Solana | 2024 | ≈ 4,9 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 673 ; CG `michi` |
| 1203 | Wolfies | PACK | à vérifier | sept. 2026 | ≈ 4,9 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 467 ; CG `moonflow-2` |
| 1204 | Based Street Bets | BSB | Base | à vérifier (sommet le 27 avr. 2024) | ≈ 4,8 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Parodie de WallStreetBets sur Base, avril 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/based-street-bets |
| 1205 | Hachiko Inu | HACHIKO | à vérifier | févr. 2026 | ≈ 4,8 M$ (estimé CG) | estimé | en déclin |  | commune | commune |  | à définir | v1 n° 463 ; CG `hachiko-inu-2` |
| 1206 | Oggy Inu | OGGY | BNB Chain | avr. 2023 (ajout CMC) | ≈ 4,8 M$ (18 juin 2023) ; CMC, relevé hebdomadaire | sourcé | mort | Oggy, le chat du dessin animé « Oggy et les cafards », mème BSC d'avril 2023 ; pic en juin 2023. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/oggy-inu/ ; https://www.coingecko.com/en/coins/oggy-inu |
| 1207 | Patlu | PATLU | BNB Chain | 21/03/2025 | ≈ 4,8 M$ (22/03/2025) | estimé | mort (≈ 13 k$) | « Patlu, c'est CZ déguisé » : le héros chauve à lunettes du dessin animé indien Motu Patlu ; mort en un jour. | commune | commune | personne réelle | à définir | r3 ; https://coinmarketcap.com/currencies/patlu/ |
| 1208 | Sam Bankmeme-Fried | SBF | Solana | nov. 2023 | ≈ 4,8 M$ (5 mars 2024) | estimé | mort | Moquerie de Sam Bankman-Fried ; ~5 M$ en mars 2024. | commune | commune | personne réelle | à définir | r3 ; https://coinmarketcap.com/currencies/sam-bankmeme-fried/ ; https://dexscreener.com/solana/FkbWN4dcFQym2PgCELfThghQqLuA2e2jThMJyhZjfG4M |
| 1209 | TISM | TISM | Sui | à vérifier (sommet le 15 nov. 2024) | ≈ 4,8 M$ (nov. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Mème « autisme » de Sui, pic mi-nov. 2024, mort. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/tism |
| 1210 | Binance Mascot (Phil) | PHIL | BNB Chain | 13/04/2025 | ≈ 4,7 M$ (14/04/2025) | estimé | mort (≈ 26 k$, volume nul) | « Phil », mascotte officieuse et maladroite faite du logo Binance ; pic au lendemain du lancement. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/binance-mascot/ |
| 1211 | Doge Pepe | DOPE | à vérifier | oct. 2026 | ≈ 4,7 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 475 ; CG `doge-pepe-4` |
| 1212 | Dogs Rock | DOGSROCK | BNB Chain | à vérifier (sommet le 3 nov. 2023) | ≈ 4,7 M$ (nov. 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Mème chien BSC de nov. 2023 ; pic le 3 nov. 2023. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/dogs-rock |
| 1213 | FEFER | FEFER | à vérifier | août 2026 | ≈ 4,7 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 466 ; CG `fefer-2` |
| 1214 | FORTUNE FAVOURS THE BRAVE | FFTB | Cronos | à vérifier (sommet le 3 mai 2024) | ≈ 4,7 M$ (mai 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | « Fortune favours the brave », la pub Crypto.com de Matt Damon devenue mème sur Cronos (mai 2024). | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/fortune-favours-the-brave |
| 1215 | Grok Girl | GROKGIRL | BNB Chain | à vérifier (sommet le 18 déc. 2023) | ≈ 4,7 M$ (déc. 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Un des mèmes « Grok » nés après l'annonce du chatbot de xAI (déc. 2023) ; pic le 18 déc. 2023. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/grok-girl |
| 1216 | saucecoin | SAUCE | à vérifier | oct. 2026 | ≈ 4,7 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 468 ; CG `saucecoin` |
| 1217 | Shib Army | SHIBARMY | BNB Chain | à vérifier (sommet le 2 nov. 2021) | ≈ 4,7 M$ (nov. 2021) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Jeton à la gloire de la « Shib Army », la communauté SHIB, nov. 2021 ; pic le 2 nov. 2021. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/shib-army |
| 1218 | Suiba Inu | SUIB | Sui | à vérifier (sommet le 7 oct. 2024) | ≈ 4,7 M$ (oct. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Énième Shiba version Sui, pic oct. 2024, mort. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/suiba-inu |
| 1219 | ZenPandaCoin | ZPC | Arbitrum | à vérifier (sommet le 10 mai 2023) | ≈ 4,7 M$ (mai 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Panda zen d'Arbitrum, mai 2023. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/zenpandacoin |
| 1220 | BankerDoge | BANKER | BSC | sept. 2021 | ≈ 4,6 M$ (15/11/2021) | sourcé | mort | Clone de Dogecoin sur BSC, lancé en sept. 2021 ; pic vers le 15/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/bankerdoge/ |
| 1221 | Infinite Money Glitch | GLITCH | à vérifier | oct. 2026 | ≈ 4,6 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 470 ; CG `infinite-money-glitch-3` |
| 1222 | Kraken | KRAKEN | Ink | à vérifier (sommet le 20 déc. 2024) | ≈ 4,6 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Kraken, pieuvre d'Ink (déc. 2024). | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/kraken-ink |
| 1223 | NASDANQ | NASDANQ | à vérifier | août 2026 | ≈ 4,6 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 472 ; CG `nasdanq` |
| 1224 | Brett 2.0 | BRETT2.0 | Base | inconnu | ~4,5 M$ (date inconnue) | estimé | mort | Copie de BRETT migrée vers un nouveau contrat, il vaut 9 k$. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/brett-2-0 |
| 1225 | Dog With Purpose | DOPU | à vérifier | juil. 2025 | ≈ 4,5 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 474 ; CG `dog-with-purpose` |
| 1226 | FlareFox | FLX | Flare | à vérifier (sommet le 6 avr. 2024) | ≈ 4,5 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | FlareFox, renard de Flare, avril 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/flarefox |
| 1227 | Marvin | MARVIN | à vérifier | oct. 2026 | ≈ 4,5 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 471 ; CG `marvin-3` |
| 1228 | 42-coin | 42 | blockchain propre | janv. 2014 | ≈ 4,4 M$, 28/01/2018 (CMC, relevé quotidien) ; ≈ 8,7 M$ le 17/04/2021 | sourcé | mort | Clin d'œil au « 42 » du Guide du voyageur galactique, 42 unités seulement ; ≈ 4,4 M$ en janv. 2018, ≈ 8,7 M$ en avril 2021, capitalisation nulle aujourd'hui. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/currencies/42-coin/historical-data/ |
| 1229 | AudaCity | DACITYCOIN | à vérifier | oct. 2026 | ≈ 4,4 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 473 ; CG `audacity` |
| 1230 | ClipX | CLIPX | à vérifier | sept. 2026 | ≈ 4,4 M$ (estimé CG) | estimé | en déclin |  | commune | commune |  | à définir | v1 n° 478 ; CG `klipx-x-tips` |
| 1231 | Zhao Cai Mao | 招财猫 | à vérifier | oct. 2026 | ≈ 4,4 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 476 ; CG `zhao-cai-mao` |
| 1232 | 8Bit Doge | BITD | BSC | juin 2021 | ≈ 4,3 M$ (12/12/2021) | sourcé | mort | Clone de Dogecoin pixelisé sur BSC, lancé en juin 2021 ; pic vers le 12/12/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/8bit-doge/ |
| 1233 | BNB MEME SZN | SZN | BNB Chain | sept. 2025 (ajout CMC) | ≈ 4,3 M$ (12 oct. 2025) ; CMC, relevé hebdomadaire | sourcé | en déclin | « BNB meme szn », jeton-slogan de la frénésie des mèmes BNB d'oct. 2025 ; pic le 12 oct. 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/bnb-meme-szn/ ; https://www.coingecko.com/en/coins/bnb-meme-szn |
| 1234 | FlappyCoin | FLAP | blockchain propre | 14/02/2014 | ≈ 4,3 M$, 29/04/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Clone scrypt lancé en pleine folie Flappy Bird, deux équipes se disputant le nom ; relevé à ≈ 4,3 M$ en avril 2018 avant sa disparition de CMC. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180429/ ; https://www.pcr-online.biz/2014/02/17/flappy-bird-spawns-two-flappycoin-currencies/ |
| 1235 | OPEN Tony | OPEN | TON | à vérifier (sommet le 6 mai 2024) | ≈ 4,3 M$ (mai 2024) ; ATH CoinGecko × offre en circulation | estimé | en déclin | Mème TON au ticker OPEN, record mai 2024, -94 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/open-tony |
| 1236 | Optimus | OPTIMUS | à vérifier | oct. 2026 | ≈ 4,3 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 479 ; CG `optimus-2` |
| 1237 | Scamcoin | SCAM | à vérifier | sept. 2026 | ≈ 4,3 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 477 ; CG `scamcoin` |
| 1238 | BNBEE | BEE | BNB Chain | à vérifier (sommet le 4 janv. 2024) | ≈ 4,2 M$ (janv. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Abeille BNB de janv. 2024 ; pic le 4 janv. 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/bnbee |
| 1239 | DOGEMOB | DOGEMOB | BNB Chain | avr. 2024 (ajout CMC) | ≈ 4,2 M$ (14 juil. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Doge de la « mob » BSC d'avril 2024 ; pic en juillet 2024, sorti du classement en 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/dogemob/ ; https://coinmarketcap.com/historical/20240714/ |
| 1240 | Long Mao | LMAO | zkSync Era | à vérifier (sommet le 6 mars 2024) | ≈ 4,2 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Long Mao (« chat dragon ») de zkSync, mars 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/long-mao |
| 1241 | Whiskers | WHISK | TON | à vérifier (sommet le 13 mai 2024) | ≈ 4,2 M$ (mai 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Chat capricieux de TON, record mai 2024, -99,6 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/whiskers |
| 1242 | Aster Dog | ADOG | BNB Chain | 03/10/2025 | ≈ 4,1 M$ (04/10/2025) | estimé | mort (≈ 10 k$) | Présenté comme le premier mème apparié à Aster ; mort le lendemain de son pic. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/aster-dog/ |
| 1243 | Energy | NRG | à vérifier | avr. 2026 | ≈ 4,1 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 482 ; CG `energy-2` |
| 1244 | ShibaPoconk | CONK | Fantom / Sonic | à vérifier (sommet le 18 févr. 2023) | ≈ 4,1 M$ (févr. 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | ShibaPoconk, Shiba de Fantom ; pic en févr. 2023. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/shibapoconk |
| 1245 | World is Flat | WIF | à vérifier | août 2026 | ≈ 4,1 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 480 ; CG `world-is-flat` |
| 1246 | Chameleon | CHAMELEON | HyperEVM | 2025 | ≈ 4,0 M$ (sourcé) | sourcé | mort |  | commune | commune |  | à définir | v1 n° 481 ; CG `chameleon` |
| 1247 | Croak | CROAK | Linea | à vérifier (sommet le 18 mars 2025) | ≈ 4,0 M$ (mars 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Croak, grenouille de Linea, mars 2025. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/croak_on_linea |
| 1248 | FuckToken | FUCK | Ethereum (ERC-20) | juil. 2017 | ≈ 4,0 M$, 14/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Jeton ERC-20 au nom grossier assumé ; ≈ 4 M$ en janv. 2018, plus coté après avril 2018. | commune | commune | obscène | à définir | r1 ; https://coinmarketcap.com/historical/20180114/ ; https://coinmarketcap.com/currencies/fucktoken/ |
| 1249 | one life, its worth an attempt | WORTH | à vérifier | sept. 2026 | ≈ 4,0 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 485 ; CG `one-life-its-worth-an-attempt-2` |
| 1250 | Panana | PANANA | à vérifier | déc. 2024 | ≈ 4,0 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 483 ; CG `panana` |
| 1251 | THAT | THAT | à vérifier | sept. 2026 | ≈ 4,0 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 484 ; CG `that` |
| 1252 | 超级周期 (Supercycle) | 超级周期 | BNB Chain | 10/01/2026 | > 4 M$ (vers le 11/01/2026) | sourcé | mort (≈ 13 k$) | Né d'un post de CZ sur le « supercycle », où il admettait pouvoir se tromper ; retombé à 1,7 M$ en un jour. | commune | commune |  | à définir | r3 ; https://www.panewslab.com/zh/articles/b77d5603-6827-44b6-b75b-de051186d2c3 ; https://dexscreener.com/bsc/0x2433092b3554eefc154f5ee3a275ebf2a85f4444 |
| 1253 | puush da button | PUUSH | Cronos | à vérifier (sommet le 7 mai 2024) | ≈ 3,9 M$ (mai 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | « Puush da button », mème de Cronos, mai 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/puush-da-button |
| 1254 | Spice | SPICE | Osmosis (Cosmos) | à vérifier (sommet le 27 nov. 2024) | ≈ 3,9 M$ (nov. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Spice, mème Dune sur Osmosis, nov. 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/spice-2 |
| 1255 | AI PEPE KING | AIPEPE | Polygon | à vérifier (sommet le 28 mai 2024) | ≈ 3,8 M$ (mai 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Pepe roi « IA » sur Polygon, mai 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/ai-pepe-king |
| 1256 | CageCoin | CAGE | blockchain propre | avr. 2014 | ≈ 3,8 M$, 10/09/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Coin à l'effigie de Nicolas Cage ; pic tardif à ≈ 3,8 M$ en sept. 2017, retiré de CMC fin 2017. | commune | commune | personne réelle | à définir | r1 ; https://coinmarketcap.com/historical/20170910/ ; https://coinmarketcap.com/currencies/cagecoin/ |
| 1257 | CeramicLiberty.com | CL8Y | à vérifier | nov. 2025 | ≈ 3,8 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 486 ; CG `ceramicliberty-com` |
| 1258 | HOdlcoin | HODL | blockchain propre | mars 2016 | ≈ 3,8 M$, 21/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin bâti sur le mème « HODL » (faute de frappe de 2013) ; ≈ 3,8 M$ en janv. 2018, -97 % fin 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180121/ ; https://coinmarketcap.com/currencies/hodlcoin/ |
| 1259 | Shitcoin on TON | SHIT | TON | à vérifier (sommet le 22 mai 2024) | ≈ 3,8 M$ (mai 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Mème qui s'assume « shitcoin », record le 22 mai 2024, -99,4 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/shitcoin-on-ton |
| 1260 | Trollcoin | TROLL | blockchain propre | mars 2014 | ≈ 3,8 M$, 12/01/2018 (CMC, relevé quotidien) ; ≈ 9,0 M$ le 19/09/2020 | sourcé | mort | Parodie anonyme à la tête de troll ; ≈ 3,8 M$ en janv. 2018, sursaut isolé à ≈ 9 M$ en sept. 2020, puis -99 %. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/currencies/trollcoin/historical-data/ |
| 1261 | Scuba Dog | SCUBA | Sui | à vérifier (sommet le 23 sept. 2024) | ≈ 3,7 M$ (sept. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Chien plongeur communautaire de Sui, pic sept. 2024, mort. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/scuba-dog ; https://www.fxempire.com/crypto/scuba-dog/profile |
| 1262 | Beast | BEAST | à vérifier | sept. 2026 | ≈ 3,6 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 487 ; CG `beast` |
| 1263 | Buffy | BUFFY | TON | à vérifier (sommet le 15 avr. 2024) | ≈ 3,6 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Hommage à Buffy, le chien de Pavel Durov, record avril 2024, -99,8 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/buffy |
| 1264 | Clippy | CLIPPY | Solana | 19/01/2026 | ≈ 3,6 M$ (24/01/2026) | estimé | mort (≈ 26 k$) | Lancé par Kevan Atteberry, le dessinateur du trombone de Microsoft Office ; cinq jours de hausse, puis rien. | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/clippy-kevanjatt/ |
| 1265 | CZ on Hyperliquid | CZ | Hyperliquid (HIP-1) | à vérifier (sommet le 16 déc. 2024) | ≈ 3,6 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | en déclin | Mème au nom de CZ (Binance) sur Hyperliquid, record déc. 2024, -99,8 %. | commune | commune | personne réelle | à définir | r4 ; https://www.coingecko.com/en/coins/cz-on-hyperliquid |
| 1266 | PONGO | PONGO | XRP Ledger | janv. 2025 (ajout CMC) | ≈ 3,6 M$ (2 mars 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Pongo, singe de la vague des mèmes XRPL de début 2025 ; ≈ 3,6 M$ en mars 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/pongo-xrp/ ; https://www.coingecko.com/en/coins/pongo-3 |
| 1267 | Suimon | SUIMON | Sui | à vérifier (sommet le 22 mai 2025) | ≈ 3,6 M$ (mai 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | Mème de Sui, pic mai 2025, plus de volume. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/suimon |
| 1268 | Tonio | TONIO | TON | à vérifier (sommet le 22 août 2025) | ≈ 3,6 M$ (août 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | Petit mème TON, record août 2025, -99 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/tonio |
| 1269 | Hot Cherry | à vérifier | TON | 2026 | ≈ 3,5 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | actif |  | commune | commune |  | à définir | v1 n° 502 ; CG `hot-cherry` |
| 1270 | tomochi | TOMOCHI | à vérifier | août 2026 | ≈ 3,5 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 492 ; CG `tomochi` |
| 1271 | CRYPTO CLOUD | CLOUD | à vérifier | juin 2025 | ≈ 3,4 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 491 ; CG `crypto-clouds` |
| 1272 | Kittehcoin | MEOW | blockchain propre | janv. 2014 | ≈ 3,4 M$, 26/01/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Le « Dogecoin des chats » (MEOW) ; ≈ 3,4 M$ fin janvier 2014 en pleine fièvre des clones, mining abandonné dès sept. 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140126/ ; https://www.coinwarz.com/mining/kittehcoin/hashrate-chart |
| 1273 | Krex | KREX | Kaspa (KRC-20) | à vérifier (sommet le 26 nov. 2024) | ≈ 3,4 M$ (nov. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Krex, dinosaure KRC-20, nov. 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/krex |
| 1274 | Baby Brett on Base | BBRETT | Base | inconnu | ~3,3 M$ (date inconnue) | estimé | mort | « Bébé » de BRETT, 5 $ de volume par jour, il vaut 7 k$. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/baby-brett-on-base |
| 1275 | BabyCate | BABYCATE | BNB Chain | sept. 2024 (ajout CMC) | ≈ 3,3 M$ (13 oct. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Bébé de CateCoin (sept. 2024), relance d'un mème BSC de 2021 ; mort. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/babycate/ ; https://www.coingecko.com/en/coins/babycate |
| 1276 | daCat | DACAT | à vérifier | mars 2024 | ≈ 3,3 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 490 ; CG `dacat` |
| 1277 | Davido † | DAVIDO | Solana | 2024 | ≈ 3,3 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 592 ; CG `timeless-davido` |
| 1278 | Floki Musk | FLOKI | Ethereum | déc. 2021 | ≈ 3,3 M$ en FDV (10/02/2022) | estimé | mort | Jeton né du chien Floki d'Elon Musk (tweet du 25/06/2021) sur Ethereum, lancé en déc. 2021 ; pic vers le 10/02/2022 ; aujourd'hui plus coté. | commune | commune | personne réelle | à définir | r2 ; https://coinmarketcap.com/currencies/floki-musk/ |
| 1279 | Huebel Bolt | BOLT | TON | à vérifier (sommet le 16 mai 2024) | ≈ 3,3 M$ (mai 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | BOLT, « réseau de mèmes » de la communauté TON, record mai 2024, -97,6 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/huebel-bolt |
| 1280 | OciCat Token | OCICAT | BNB Chain | août 2025 | ≈ 3,3 M$ (14 sept. 2025), sourcé | sourcé | mort |  | commune | commune |  | à définir | v1 n° 452 ; correction r4 ; CG `ocicat-token` ; https://coinmarketcap.com/currencies/ocicat/ |
| 1281 | zuzalu | ZUZALU | à vérifier | juin 2024 | ≈ 3,3 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 497 ; CG `zuzalu` |
| 1282 | Bluzo | BLZ | à vérifier | oct. 2026 | ≈ 3,2 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 494 ; CG `bluzo` |
| 1283 | Frogonsol | FROG | à vérifier | mars 2024 | ≈ 3,2 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 495 ; CG `frogonsol` |
| 1284 | KOROMARU | KOROMARU | Ethereum | nov. 2021 | ≈ 3,2 M$ en FDV (13/11/2021) | estimé | mort | Jeton « Inu » inspiré de Koromaru (Persona 3) sur Ethereum, lancé en nov. 2021 ; pic vers le 13/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/koromaru/ |
| 1285 | Spacebucks | SBX | à vérifier | nov. 2024 | ≈ 3,2 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 489 ; CG `spacebucks` |
| 1286 | Tong | TONG | TON | à vérifier (sommet le 16 août 2024) | ≈ 3,2 M$ (août 2024) ; ATH CoinGecko × offre totale | estimé | mort | « Tong » = douleur : mème de ceux qui regardent les autres s'enrichir, record août 2024, -98 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/tong |
| 1287 | UNIVERSE | UNIVERSE | à vérifier | sept. 2026 | ≈ 3,2 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 493 ; CG `universe-3` |
| 1288 | Brett's Dog | BROGG | Base | à vérifier (sommet le 21 avr. 2024) | ≈ 3,1 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Le chien de Brett, dérivé de BRETT sur Base, avril 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/brett-s-dog |
| 1289 | DUMMY | DUMMY | à vérifier | juin 2023 | ≈ 3,1 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 501 ; CG `dummy` |
| 1290 | Giggle Panda | GIGL | BNB Chain | nov. 2025 (ajout CMC) | ≈ 3,1 M$ (4 janv. 2026) ; CMC, relevé hebdomadaire | sourcé | mort | Panda dérivé de Giggle Academy (l'école de CZ), nov. 2025 ; pic début janv. 2026. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/giggle-panda/ ; https://www.coingecko.com/en/coins/giggle-panda |
| 1291 | MIZU KAPPA | MIZU | à vérifier | août 2026 | ≈ 3,1 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 496 ; CG `mizu-kappa` |
| 1292 | Papa Doge | PAPADOGE | BNB Chain | à vérifier (sommet le 2 juil. 2021) | ≈ 3,1 M$ (juil. 2021) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | « Papa Doge », réponse aux Baby Doge de l'été 2021 ; pic le 2 juillet 2021. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/papa-doge |
| 1293 | Purple | PURPLE | Ink | à vérifier (sommet le 1 févr. 2025) | ≈ 3,1 M$ (févr. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Purple, mème violet (couleur d'Ink), févr. 2025. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/purple |
| 1294 | sunlion | SUNLION | Tron (SunPump) | à vérifier (sommet le 29 août 2024) | ≈ 3,1 M$ (août 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Lion solaire de la vague SunPump, pic le 29 août 2024, quelques jours avant l'effondrement de l'activité de la plateforme. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/sunlion ; https://thedefiant.io/sunpump-activity-plummets-as-trx-falls-out-of-top-10 |
| 1295 | TOGE | TOGE | TON | à vérifier (sommet le 15 avr. 2024) | ≈ 3,1 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | « Le DOGE de TON », record avril 2024, -99,8 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/toge |
| 1296 | Nads | NADS | Monad | nov. 2025 | ≈ 3,0 M$ (sourcé) | sourcé | mort |  | commune | commune |  | à définir | v1 n° 499 ; CG `nads` |
| 1297 | ShibaZilla | SHIBZ | BSC | oct. 2021 | ≈ 3,0 M$ en FDV (05/11/2021) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en oct. 2021 ; pic vers le 05/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/shibazilla/ |
| 1298 | The Corgi of PolkaBridge | CORGIB | BNB Chain | juin 2021 (ajout CMC) | ≈ 3,0 M$ (7 nov. 2021) ; CMC, relevé hebdomadaire | sourcé | mort | Mascotte corgi du launchpad PolkaBridge (juin 2021), qui a vécu sa vie de mème BSC ; pic en nov. 2021. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/the-corgi-of-polkabridge/ ; https://coinmarketcap.com/historical/20211107/ |
| 1299 | This Is Fine (ETH) | FINE | Ethereum | 07/10/2024 | ≈ 3 M$ (15/10/2024) | estimé | mort | Le chien qui boit son café dans l'incendie, sommet une semaine après le lancement. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/this-is-fine-ethereum ; https://dexscreener.com/ethereum/0x1634e10C9155BE623B5a52d6CA01C7A904D89b0a |
| 1300 | Where Did The ETH Go? (Pulsechain) | WHETH | PulseChain | à vérifier (sommet le 2 nov. 2023) | ≈ 3,0 M$ (nov. 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | « Où sont passés les ETH ? », pique au « sacrifice » PulseChain de Richard Heart (nov. 2023). | commune | commune | personne réelle | à définir | r4 ; https://www.coingecko.com/en/coins/where-did-the-eth-go-pulsechain |
| 1301 | xiao lang gou | XLG | Tron (SunPump) | à vérifier (sommet le 1 sept. 2024) | ≈ 3,0 M$ (sept. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | « Petit chien-loup » en chinois, mème SunPump de fin août 2024, à -99 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/xiao-lang-gou |
| 1302 | Crobinhood | CROBINHOOD | à vérifier | nov. 2026 | ≈ 2,9 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 500 ; CG `crobinhood` |
| 1303 | BabyDogeZilla | BABYDOGEZILLA | BSC | oct. 2021 | ≈ 2,8 M$ en FDV (26/10/2022) | estimé | mort | Clone de Dogecoin sur BSC, lancé en oct. 2021 ; pic vers le 26/10/2022 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/babydogezilla/ |
| 1304 | Funds Are Safu | SAFU | à vérifier | nov. 2026 | ≈ 2,8 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 504 ; CG `funds-are-safu-2` |
| 1305 | Internet Doge | IDOGE | Internet Computer | à vérifier (sommet le 6 déc. 2024) | ≈ 2,8 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Internet Doge, Doge de l'ICP, déc. 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/internet-doge |
| 1306 | Joe Hat | HAT | Avalanche | à vérifier (sommet le 8 déc. 2023) | ≈ 2,8 M$ (déc. 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Le chapeau de Joe, mascotte du DEX Trader Joe, devenu mème en déc. 2023. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/joe-hat-token |
| 1307 | Luca Netz's Dog | BANDIT | Abstract | à vérifier (sommet le 19 mai 2025) | ≈ 2,8 M$ (mai 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Le chien de Luca Netz, patron de Pudgy Penguins, mème d'Abstract (mai 2025). | commune | commune | personne réelle | à définir | r4 ; https://www.coingecko.com/en/coins/luca-netz-s-dog |
| 1308 | Make America Based Again | MABA | Base | mars 2024 (ajout CMC) | ≈ 2,8 M$ (6 oct. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Slogan MAGA détourné en « Make America Based Again » sur Base (mars 2024) ; pic en oct. 2024. | commune | commune | politique | à définir | r4 ; https://coinmarketcap.com/currencies/make-america-based-again/ ; https://coinmarketcap.com/historical/20241006/ |
| 1309 | Saudi Shiba Inu | SAUDISHIB | Ethereum | juil. 2022 | ≈ 2,8 M$ en FDV (08/08/2022) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en juil. 2022 ; pic vers le 08/08/2022 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/saudishibainu/ |
| 1310 | Solala (索拉拉) | 索拉拉 | Solana | Trends.fun, 2025-2026 | ≈ 2,8 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 753 ; CG `solala` |
| 1311 | Battle Inu | BINU | BSC | févr. 2022 | ≈ 2,7 M$ en FDV (26/02/2022) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en févr. 2022 ; pic vers le 26/02/2022 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/battle-inu/ |
| 1312 | DogeCube | DOGECUBE | Radix | à vérifier (sommet le 28 sept. 2022) | ≈ 2,7 M$ (sept. 2022) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | DogeCube, Doge de Radix (sept. 2022). | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/dogecube |
| 1313 | Nyancoin | NYAN | Nyancoin (blockchain propre) | 2014 | ≈ 2,7 M$, 07/01/2018 (plancher, relevé hebdomadaire) | sourcé | mort (absent de CoinGecko) | Nyancoin : mème de l'ère 2014 | commune | rare |  | à définir | v1 n° 699 ; correction r1 ; https://coinmarketcap.com/historical/20180107/ |
| 1314 | The Loonies | LOON | Aptos | à vérifier (sommet le 17 janv. 2025) | ≈ 2,7 M$ (janv. 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | Jeton communautaire de la collection NFT The Loonies, pic janv. 2025, mort. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/the-loonies |
| 1315 | Wobbles | WOBBLES | à vérifier | mai 2026 | ≈ 2,7 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 505 ; CG `wobbles` |
| 1316 | HoboNickels | HBN | blockchain propre | déc. 2013 | ≈ 2,6 M$, 14/01/2018 (CMC, relevé quotidien) | sourcé | mort | Clone de 2013 au thème « clochard », cité par Entrepreneur parmi les « wannabes » ; ≈ 2,6 M$ en janv. 2018, puis disparu. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/currencies/hobonickels/historical-data/ ; https://www.entrepreneur.com/money-finance/sexcoin-dogecoin-hobonickel-ripple-should-you-take/232078 |
| 1317 | Kroak on Kaspa | KROAK | Kaspa (KRC-20) | à vérifier (sommet le 25 déc. 2024) | ≈ 2,6 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Kroak, grenouille KRC-20, déc. 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/kroak-on-kaspa |
| 1318 | Long | LONG | zkSync Era | avr. 2024 (ajout CMC) | ≈ 2,6 M$ (9 juin 2024) ; CMC, relevé hebdomadaire | sourcé | mort | LONG, mème « long » de zkSync (mai 2024). | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/long-fun/ ; https://www.coingecko.com/en/coins/long-3 |
| 1319 | 赵长娥 | 赵长娥 | BNB Chain | 06/10/2025 | ≈ 2,6 M$ (06/10/2025) | estimé | mort (≈ 12 k$) | Jeu de mots entre 赵长鹏 (CZ) et Chang'e, déesse de la Lune, pour la fête de la Mi-Automne ; il n'a duré qu'une journée. | commune | commune | personne réelle | à définir | r3 ; https://coinmarketcap.com/currencies/zhaochange/ |
| 1320 | CorgiCoin (2014) | CORG | blockchain propre | févr. 2014 | ≈ 2,5 M$, 28/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Clone de Dogecoin au corgi ; ≈ 0,25 M$ en 2014, relevé à ≈ 2,5 M$ fin janvier 2018 avant retrait. Distinct du CorgiCoin Solana (carte 586). | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180128/ ; https://coinmarketcap.com/currencies/corgicoin/ |
| 1321 | HBARbarian | HBARBARIAN | Hedera | à vérifier (sommet le 12 mars 2024) | ≈ 2,5 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | HBARbarian, barbare de Hedera, mars 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/hbarbarian |
| 1322 | Liquid Cat | CAT | Hyperliquid (HIP-1) | à vérifier (sommet le 15 janv. 2025) | ≈ 2,5 M$ (janv. 2025) ; ATH CoinGecko × offre en circulation | estimé | en déclin | Chat né sur HypurrFUN (LCAT), pic janv. 2025, -95 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/cat-2 |
| 1323 | Poodlecoin | POODLE | Flare | à vérifier (sommet le 28 avr. 2024) | ≈ 2,5 M$ (avr. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Poodlecoin, caniche de Flare, avril 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/poodlecoin |
| 1324 | Saiyan PEPE | SPEPE | Polygon | à vérifier (sommet le 20 déc. 2023) | ≈ 2,5 M$ (déc. 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Pepe Super Saiyan sur Polygon, déc. 2023. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/saiyan-pepe |
| 1325 | 亮剑出击 | 亮剑出击 | à vérifier | oct. 2026 | ≈ 2,5 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 506 ; CG `liang-jian-chu-ji` |
| 1326 | BIRTHDAY | BIRTHDAY | à vérifier | oct. 2026 | ≈ 2,4 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 507 ; CG `birthday` |
| 1327 | Chonk The Cat | CHONK | BNB Chain | à vérifier (sommet le 27 mars 2024) | ≈ 2,4 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Chat obèse (chonk) de mars 2024 ; pic le 27 mars 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/chonk-the-cat |
| 1328 | GoldenRat | RATS | BNB Chain | oct. 2024 (ajout CMC) | ≈ 2,4 M$ (16 mars 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Rat doré BSC de nov. 2024 ; pic en mars 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/goldenrat/ ; https://www.coingecko.com/en/coins/goldenrat |
| 1329 | KarpelesCoin | KAR | blockchain propre | avr. 2014 | ≈ 2,4 M$, 06/04/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin moquant Mark Karpelès un mois après la faillite de Mt. Gox ; ≈ 2,4 M$ dès son entrée sur CMC, disparu en décembre 2014. | commune | commune | personne réelle | à définir | r1 ; https://coinmarketcap.com/historical/20140406/ ; https://coinmarketcap.com/currencies/karpelescoin/ |
| 1330 | Kishimoto Inu | KISHIMOTO | Ethereum | oct. 2021 | ≈ 2,4 M$ en FDV (02/02/2023) | estimé | mort | Jeton « Inu » nommé d'après Masashi Kishimoto (Naruto) sur Ethereum, lancé en oct. 2021 ; pic vers le 02/02/2023 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/kishimoto-inu/ |
| 1331 | Pizza | PIZZA | Bitcoin (BRC-20) | 2023-2024 | ≈ 2,4 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 714 ; CG `pizza` |
| 1332 | SAD MEOW | SADMEOW | TON | à vérifier (sommet le 19 oct. 2024) | ≈ 2,4 M$ (oct. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Chat triste de TON, record oct. 2024, -98,5 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/sad-meow |
| 1333 | The Nation Token | NATO | Base | déc. 2024 (ajout CMC) | ≈ 2,4 M$ (24 août 2025) ; CMC, relevé hebdomadaire | sourcé | mort | « NATO », mème géopolitique de Base (déc. 2024) ; pic en août 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/the-nation-token/ ; https://www.coingecko.com/en/coins/the-nation-token |
| 1334 | DogeCash | DOGEC | blockchain propre | janv. 2019 (ajout CMC) | ≈ 2,2 M$ (7 mars 2021) ; CMC, relevé hebdomadaire | sourcé | mort | DogeCash, coin à masternodes à thème Doge (2019) ; ≈ 2,2 M$ en mars 2021. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/dogecash/ ; https://coinmarketcap.com/historical/20210307/ |
| 1335 | DOPU The Dog with A Purpose | DOPU | XDC Network | juin 2024 (ajout CMC) | ≈ 2,2 M$ (26 oct. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | DOPU, « chien avec un but », mème de XDC (juin 2024). | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/dopu-the-dog-with-a-purpose/ ; https://coinmarketcap.com/historical/20251026/ |
| 1336 | Hestia | HESTIA | à vérifier | oct. 2025 | ≈ 2,2 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 509 ; CG `hestia` |
| 1337 | KanadeCoin | KNDC | Ethereum (ERC-20) | juil. 2018 | ≈ 2,2 M$, 27/07/2018 (CMC, relevé quotidien) ; ≈ 3,5 M$ le 15/11/2021 | sourcé | mort | Jeton japonais à mascotte d'anime ; ≈ 2,2 M$ en juil. 2018, sursaut à ≈ 3,5 M$ en nov. 2021, puis plus de capitalisation. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/currencies/kanadecoin/historical-data/ |
| 1338 | Lil Pump | LILPUMP | Solana | Célébrités, juin 2024 | ≈ 2,2 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 660 ; CG `lil-pump` |
| 1339 | meh on TON | MEH | TON | à vérifier (sommet le 10 mai 2024) | ≈ 2,2 M$ (mai 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Mème « meh » de TON, record mai 2024, -99 %. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/meh-on-ton |
| 1340 | ShibaKeanu | SHIBK | à vérifier | juin 2024 | ≈ 2,2 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 510 ; CG `shibakeanu` |
| 1341 | VIPER | VIPER | Cardano | à vérifier (sommet le 1 févr. 2025) | ≈ 2,2 M$ (févr. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Viper, serpent de Cardano, févr. 2025. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/viper-2 |
| 1342 | Chucky | CHUCKY | Cronos | à vérifier (sommet le 3 mai 2024) | ≈ 2,1 M$ (mai 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Chucky, la poupée tueuse, sur Cronos (mai 2024). | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/chucky |
| 1343 | DOGMI | DOGMI | Internet Computer | janv. 2024 (ajout CMC) | ≈ 2,1 M$ (22 déc. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | DOGMI, Doge de l'Internet Computer (janv. 2024). | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/dogmi/ ; https://coinmarketcap.com/historical/20241222/ |
| 1344 | Linpuss | LPUSS | Linea | à vérifier (sommet le 12 janv. 2025) | ≈ 2,1 M$ (janv. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Linpuss, chat de Linea, janv. 2025. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/linpuss |
| 1345 | LOBIN | LOBIN | à vérifier | nov. 2026 | ≈ 2,1 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 511 ; CG `lobin` |
| 1346 | NinjaCat | NINJACAT | à vérifier | sept. 2026 | ≈ 2,1 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 514 ; CG `ninjacat` |
| 1347 | ZenFrogs | ZEN | Sui | à vérifier (sommet le 19 nov. 2024) | ≈ 2,1 M$ (nov. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Grenouilles zen de Sui, pic nov. 2024, mort. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/zenfrogs |
| 1348 | Delivery Guy | DGUY | à vérifier | oct. 2026 | ≈ 2,0 M$ (estimé CG) | estimé | actif |  | commune | commune |  | à définir | v1 n° 512 ; CG `delivery-guy` |
| 1349 | GMONAD | GMONAD | Monad | à vérifier (sommet le 24 nov. 2025) | ≈ 2,0 M$ (nov. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | GMONAD, « gm » version Monad, nov. 2025, au lancement du réseau. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/gmonad-3 |
| 1350 | KOI | KOI | Sui | à vérifier (sommet le 20 oct. 2024) | ≈ 2,0 M$ (oct. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Carpe koï de Sui, pic oct. 2024, mort. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/koi-5 |
| 1351 | emo | EMO | Monad | 2025 † | ≈ 1,9 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 615 ; CG `emonad` |
| 1352 | UltCat | ULTCAT | à vérifier | oct. 2026 | ≈ 1,9 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 515 ; CG `ultcat` |
| 1353 | Bear Bull | BRB | XRP Ledger | à vérifier (sommet le 24 janv. 2025) | ≈ 1,8 M$ (janv. 2025) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Ours-taureau de l'XRPL, janv. 2025. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/bear-bull |
| 1354 | FOMO BULL CLUB | FOMO | Base | avr. 2024 (ajout CMC) | ≈ 1,8 M$ (7 juil. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Club de taureaux FOMO de Base (avril 2024) ; pic en juillet 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/fomo-bull-club/ ; https://www.coingecko.com/en/coins/fomo-bull-club |
| 1355 | Mao Zedong | MAO | blockchain propre | août 2017 | ≈ 1,8 M$, 05/11/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Coin à l'effigie de Mao ; ≈ 1,8 M$ en nov. 2017, -87 % fin 2018. | commune | commune | politique | à définir | r1 ; https://coinmarketcap.com/historical/20171105/ ; https://coinmarketcap.com/currencies/mao-zedong/ |
| 1356 | Meowcat | MEOW | Avalanche | mai 2024 (ajout CMC) | ≈ 1,8 M$ (28 juil. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | Meowcat, chat d'Avalanche de mai 2024. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/meowcat-xyz/ ; https://www.coingecko.com/en/coins/meowcat-2 |
| 1357 | PADAWAN | PADAWAN | MultiversX | à vérifier (sommet le 25 mars 2024) | ≈ 1,8 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Padawan, mème Star Wars de MultiversX, mars 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/padawan |
| 1358 | PSYOP † | PSYOP | Ethereum | 2023 | ≈ 1,8 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 720 ; correction r3 ; CG `psyop-2` ; https://www.coingecko.com/en/coins/psyop |
| 1359 | Zeekwifhat | ZWIF | zkSync Era | à vérifier (sommet le 10 juin 2024) | ≈ 1,8 M$ (juin 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Zeek avec un bonnet, croisement zkSync × dogwifhat (juin 2024). | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/zeekwifhat |
| 1360 | Book of Miggles | BOMI | Base | juil. 2024 | ~1,7 M$ (date inconnue) | estimé | en déclin | Copie « Book of » de Mister Miggles, le chat de Base, à l'été 2024, il pèse 0,14 M$. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/book-of-miggles |
| 1361 | Cat Wif Hands | CATWIF | Avalanche | à vérifier (sommet le 21 mars 2024) | ≈ 1,7 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | « Cat wif hands », dérivé de la mode « wif » (dogwifhat), Avalanche, mars 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/cat-wif-hands |
| 1362 | Neiro on Tron | NEIRO | Tron | à vérifier (sommet le 11 sept. 2024) | ≈ 1,7 M$ (sept. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Copie Tron de la chienne Neiro en pleine folie Neiro de septembre 2024 ; morte depuis. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/neiro-on-tron |
| 1363 | Walrus the tusk | TUSK | Sui | à vérifier (sommet le 21 oct. 2024) | ≈ 1,7 M$ (oct. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Morse mascotte (clin d'œil à Walrus, le stockage de Sui), pic oct. 2024, mort. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/walrus-the-tusk |
| 1364 | zkDoge | ZKDOGE | zkSync Era | à vérifier (sommet le 9 mars 2024) | ≈ 1,7 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Doge de zkSync, mars 2024. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/zkdoge |
| 1365 | 死了么 (T'es mort ?) | 死了么 | BNB Chain | 11/01/2026 | ≈ 1,7 M$ (14/01/2026) | estimé | mort (≈ 80 k$, volume nul) | « Un clic par jour pour dire que je suis encore là » : mème tiré d'une appli chinoise virale du même nom (lien à vérifier). | commune | commune |  | à définir | r3 ; https://coinmarketcap.com/currencies/sileme/ |
| 1366 | Based Coin | BASED | Base | 2024 | ≈ 1,6 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 556 ; CG `based-coin` |
| 1367 | Doge Base | DOGEBASE | Base | inconnu | ~1,6 M$ (date inconnue) | estimé | mort | Copie de DOGE sur Base, elle vaut 20 k$. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/doge-base |
| 1368 | 财富人生 | 财富人生 | à vérifier | oct. 2026 | ≈ 1,6 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 518 ; CG `cai-fu-ren-sheng` |
| 1369 | ChanCoin | CHAN | blockchain propre | juil. 2017 | ≈ 1,5 M$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin né sur 4chan (/biz/) ; ≈ 1,5 M$ en janv. 2018, -97 % à son retrait. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180107/ ; https://coinmarketcap.com/currencies/chancoin/ |
| 1370 | Resistance Duck | à vérifier | TON | 2024-2026 | ≈ 1,5 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 729 ; CG `resistance-duck` |
| 1371 | Sharbi | SHARBI | Ethereum (à vérifier) | début 2023 | ≈ 1,5 M$ (15/03/2023) | estimé | mort | Chien mème de l'orbite Shiba Inu, pic en mars 2023, puis oubli. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/sharbi |
| 1372 | SwagBucks | BUCKS | blockchain propre | janv. 2016 | ≈ 1,5 M$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « swag » ; ≈ 1,5 M$ en janv. 2018, retiré en mai 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180107/ ; https://coinmarketcap.com/currencies/swagbucks/ |
| 1373 | Evil Coin | EVIL | blockchain propre | janv. 2016 | ≈ 1,4 M$, 12/01/2018 (CMC, relevé quotidien) | sourcé | mort | Coin « maléfique » assumé ; ≈ 1,4 M$ le 12/01/2018, puis capitalisation nulle. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/currencies/evil-coin/historical-data/ |
| 1374 | EXCELLENCE | EOP | à vérifier | oct. 2026 | ≈ 1,4 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 520 ; CG `president-platy` |
| 1375 | Illuminati | ILUM | à vérifier | mars 2024 | ≈ 1,4 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 521 ; CG `illuminati` |
| 1376 | Just a peace guy | PEACEGUY | Solana (pump.fun) | juin 2025 | ≈ 1,4 M$ (date inconnue) | estimé | mort (≈ 40 k$) | Une copie tardive de « chill guy », jamais décollée. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/peace-guy ; https://dexscreener.com/solana/h6ulh57bvurltn4zepaxpr6e6afw8wnxzvfbzfyjzrgg |
| 1377 | PUGWIFHAT | PUGWIF | Sui | à vérifier (sommet le 12 sept. 2025) | ≈ 1,4 M$ (sept. 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | Carlin à bonnet, copie de dogwifhat sur Sui, pic sept. 2025, mort. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/pugwifhat |
| 1378 | Shekel | JEW | blockchain propre | févr. 2018 | ≈ 1,4 M$, 13/05/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Ticker « JEW » : nom et ticker à connotation antisémite ; ≈ 1,4 M$ en mai 2018, -95 % fin 2018. | commune | commune | obscène | à définir | r1 ; https://coinmarketcap.com/historical/20180513/ ; https://coinmarketcap.com/currencies/shekel/ |
| 1379 | To The Sun | SUNPUMP | Tron (SunPump) | à vérifier (sommet le 6 sept. 2024) | ≈ 1,4 M$ (sept. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Jeton au ticker SUNPUMP, mème d'hommage à la plateforme, sommet début sept. 2024 au moment où SunPump s'éteignait. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/to-the-sun |
| 1380 | Troll in Hood | TROLL | à vérifier | oct. 2026 | ≈ 1,4 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 519 ; CG `troll-in-hood` |
| 1381 | CULOSUI | CULO | Sui | à vérifier (sommet le 24 juil. 2025) | ≈ 1,3 M$ (juil. 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | « Culo » (fesses) sur Sui, pic juil. 2025, plus de volume. | commune | commune | obscène | à définir | r4 ; https://www.coingecko.com/en/coins/culosui |
| 1382 | Doge Killer † | LEASH | Ethereum | 2021 | ≈ 1,3 M$ (plancher : capitalisation actuelle) | estimé | en déclin (-95 % ou pire) |  | commune | commune |  | à définir | v1 n° 600 ; CG `leash` |
| 1383 | BabyUSDT | BABYUSDT | BNB Chain | août 2021 (ajout CMC) | ≈ 1,2 M$ (5 sept. 2021) ; CMC, relevé hebdomadaire | sourcé | mort | « BabyUSDT », jeton Baby versant des récompenses en USDT, sept. 2021 ; coté deux mois. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/babyusdt/ ; https://coinmarketcap.com/historical/20210905/ |
| 1384 | BBBPump.fun & Beny Bad Boy | BBB | XDC Network | juin 2024 (ajout CMC) | ≈ 1,2 M$ (26 oct. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Beny Bad Boy, mème de XDC lié au launchpad BBBPump (nov. 2024). | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/beny-bad-boy/ ; https://coinmarketcap.com/historical/20251026/ |
| 1385 | BERNcash | BERN | blockchain propre | avr. 2016 | ≈ 1,2 M$, 10/01/2018 (CMC, relevé quotidien) | sourcé | mort | Coin de la campagne Bernie Sanders 2016 ; ≈ 1,2 M$ en janv. 2018, puis plus de capitalisation. | commune | commune | politique | à définir | r1 ; https://coinmarketcap.com/currencies/berncash/historical-data/ |
| 1386 | Corgi Inu (corgibnb.com) | CORGI | BNB Chain | déc. 2024 (ajout CMC) | ≈ 1,2 M$ (5 janv. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | Corgi Inu BSC de fin déc. 2024 ; pic début janv. 2025. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/corgi-inu-bnb/ ; https://www.coingecko.com/en/coins/corgi-inu-2 |
| 1387 | TRON MASCOT | SUNTRON | à vérifier | sept. 2026 | ≈ 1,2 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 525 ; CG `tron-mascot` |
| 1388 | Dobermann | DOBERMANN | à vérifier | sept. 2026 | ≈ 1,1 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 522 ; CG `dobermann-2` |
| 1389 | GRIOT | GRIOT | à vérifier | sept. 2026 | ≈ 1,1 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 523 ; CG `griot` |
| 1390 | Infinite Sui Glitch | ISG | Sui | à vérifier (sommet le 28 avr. 2025) | ≈ 1,1 M$ (avr. 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | Parodie du « glitch d'argent infini », pic avril 2025, mort. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/infinite-sui-glitch |
| 1391 | Jelly Finance Baby | JFB | à vérifier | sept. 2026 | ≈ 1,1 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 524 ; CG `jelly-finance-baby` |
| 1392 | Sui Bull | BULL | Sui | à vérifier (sommet le 30 sept. 2024) | ≈ 1,1 M$ (sept. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | Taureau de Sui, pic sept. 2024, mort. | commune | commune |  | à définir | r4 ; https://www.coingecko.com/en/coins/sui-bull |
| 1393 | cats (BRC-20) | CATS | Bitcoin (BRC-20) | 2023-2024 | ≈ 1,0 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 575 ; CG `cats-3` |
| 1394 | Floyd Money Mayweather | FLOYD | Solana (Fomo) | 13 oct. 2026 | ≈ 1 M$ (oct. 2026) | sourcé | mort (≈ 6 k$) | Promu par les comptes de Mayweather, déjà lié par ZachXBT à plusieurs rugs ; il s'écroule dans l'après-midi. | commune | commune | personne réelle | à définir | r3 ; https://decrypt.co/380928/notorious-crypto-celeb-meme-coin-promoter-plots-second-wave-on-new-launchpad ; https://dexscreener.com/solana/7gf7cvxdhij7izwgxz3dbhavk7ztxi9eyrbzc1dy8ysx |
| 1395 | FuzzBalls | FUZZ | blockchain propre | mai 2016 | ≈ 1,0 M$, 12/01/2018 (CMC, relevé quotidien) | sourcé | mort | Coin « boules de poils » ; ≈ 1 M$ le 12/01/2018, puis plus de capitalisation. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/currencies/fuzzballs/historical-data/ |
| 1396 | Zoki | ZOKI | à vérifier | oct. 2026 | ≈ 1,0 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 526 ; CG `zoki` |
| 1397 | Catcoin (2013) | CAT | blockchain propre | déc. 2013 | ≈ 960 k$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Un des tout premiers clones « chat » de Dogecoin, cité par le Daily Beast ; ≈ 0,5 M$ fin 2013, ≈ 0,96 M$ en janv. 2018. Distinct du Catcoin de 2024 (carte 265). | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180107/ ; https://www.thedailybeast.com/dogecoin-coinye-and-catcoin-a-dummys-guide-to-cryptocurrencies/ |
| 1398 | SpacePenguin | PNGN | BNB Chain | avr. 2021 (ajout CMC) | ≈ 892 k$ (sept. 2021) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | Pingouin spatial de la saison SafeMoon (avril 2021), mème reflection à faible capitalisation ; mort depuis 2021. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/spacepenguin/ ; https://www.coingecko.com/en/coins/spacepenguin |
| 1399 | Hogdog | HOGDOG | Monad | nov. 2025 | ≈ 860 k$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 527 |
| 1400 | Akita Inu | AKITA | Ethereum | 2021 | ≈ 803 k$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° 533 ; CG `akita-inu-3` |
| 1401 | Rare Pepe Party | RAREPEPEP | Counterparty (Bitcoin) (à vérifier) | nov. 2016 | ≈ 739 k$, 18/06/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Jeton de l'écosystème Rare Pepe ; ≈ 0,74 M$ en juin 2017, retiré en sept. 2017. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20170618/ ; https://coinmarketcap.com/currencies/rare-pepe-party/ |
| 1402 | Blue Guy | BLUE | Base | inconnu | ~0,67 M$ (date inconnue) | estimé | mort | Personnage bleu, couleur de Base, à 0 $ de volume pour 8 k$. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/blue-guy |
| 1403 | Gavun Wud | WUD | à vérifier | avr. 2026 | ≈ 607 k$ (plancher : capitalisation actuelle) | estimé | mort |  | commune | commune |  | à définir | v1 n° 624 ; CG `gavun-wud` |
| 1404 | RonPaulCoin | RPC | blockchain propre | janv. 2014 | ≈ 559 k$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin hommage à Ron Paul, lancé avec la vague de janvier 2014 ; ≈ 0,56 M$ en janv. 2018, -95 %. | commune | commune | politique | à définir | r1 ; https://coinmarketcap.com/historical/20180107/ ; https://coinmarketcap.com/currencies/ronpaulcoin/ |
| 1405 | Based Mog Coin | MOG | Base | inconnu | ~0,54 M$ (date inconnue) | estimé | mort | Copie de MOG sur Base (différente du Mog Coin du catalogue), 2 $ de volume par jour. | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/based-mog-coin |
| 1406 | Bitcoin Adult | BTAD | blockchain propre | sept. 2018 | ≈ 493 k$, 13/10/2018 (CMC, relevé quotidien) | sourcé | mort | Fork « adulte » de Bitcoin ; ≈ 0,49 M$ en oct. 2018, puis capitalisation nulle. | commune | commune | obscène | à définir | r1 ; https://coinmarketcap.com/currencies/bitcoin-adult/historical-data/ |
| 1407 | Gold Pressed Latinum | GPL | blockchain propre | mai 2017 | ≈ 464 k$, 14/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Monnaie des Ferengis de Star Trek ; ≈ 0,46 M$ en janv. 2018, retiré fin 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180114/ ; https://coinmarketcap.com/currencies/gold-pressed-latinum/ |
| 1408 | XxXcoin | XXX | blockchain propre | juil. 2014 | ≈ 456 k$, 12/06/2016 (CMC, relevé hebdomadaire) | sourcé | mort | Coin pornographique ; ≈ 0,46 M$ en juin 2016 juste avant son retrait. | commune | commune | obscène | à définir | r1 ; https://coinmarketcap.com/historical/20160612/ ; https://coinmarketcap.com/currencies/xxxcoin/ |
| 1409 | MoonPirate | MOONPIRATE | BSC | févr. 2021 | ≈ 451 k$ en FDV (08/11/2021) | estimé | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) sur BSC, lancé en févr. 2021 ; pic vers le 08/11/2021 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/moonpirate/ |
| 1410 | WankCoin | WKC | blockchain propre | juin 2014 | ≈ 394 k$, 29/06/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin au nom grossier (argot britannique) ; ≈ 0,39 M$ à son entrée sur CMC, ≈ 1 k$ à son retrait en 2015. | commune | commune | obscène | à définir | r1 ; https://coinmarketcap.com/historical/20140629/ ; https://coinmarketcap.com/currencies/wankcoin/ |
| 1411 | CLANKTARDIO | CLANKTARDIO | Base | fin 2024 (Clanker) | ~0,37 M$ (date inconnue) | estimé | mort | Jeton d'art et de mèmes de Clanker World, il ne se négocie plus nulle part (0 $ de volume). | commune | commune |  | à définir | r3 ; https://www.coingecko.com/en/coins/clanktardio |
| 1412 | Theresa May Coin | MAY | blockchain propre | juin 2017 | ≈ 364 k$, 14/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin moquant la Première ministre britannique ; ≈ 0,36 M$ en janv. 2018, puis capitalisation nulle. | commune | commune | politique | à définir | r1 ; https://coinmarketcap.com/historical/20180114/ ; https://coinmarketcap.com/currencies/theresa-may-coin/ |
| 1413 | Useless Ethereum Token † | UET | Ethereum | 2017 | ≈ 0,31 M$, 28/01/2018 | sourcé | mort (absent de CoinGecko) | Useless Ethereum Token : parodie d'ICO culte de 2017 | commune | épique |  | à définir | v1 n° 781 ; correction r1 ; https://coinmarketcap.com/historical/20180128/ ; https://qz.com/1023501/ethereum-ico-people-invested-thousands-of-dollars-in-useless-ethereum-token-uet |
| 1414 | Rocket Bunny | BUNNY | Ethereum | févr. 2021 | ≈ 303 k$ en FDV (11/09/2022) | estimé | mort | Mème lapin reflection sur Ethereum, lancé en févr. 2021 ; pic vers le 11/09/2022 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/rocket-bunny/ |
| 1415 | Cthulhu Offerings | OFF | blockchain propre | juil. 2015 | ≈ 0,29 M$, 14/01/2018 | sourcé | mort (retiré de CMC en mai 2018) |  | commune | commune |  | à définir | v1 n° 589 ; correction r1 ; https://coinmarketcap.com/historical/20180114/ ; https://www.verdict.co.uk/alternatives-to-bitcoin-next-dogecoin/ |
| 1416 | Pepe MAGA | PEPE MAGA | à vérifier | 2024 (à vérifier) | ≈ 281 k$ (estimé CG) | estimé | mort |  | commune | commune | politique | à définir | v1 n° 705 ; CG `pepe-maga` |
| 1417 | BillaryCoin | BLRY | blockchain propre | mai 2016 | ≈ 238 k$, 11/06/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Coin de la campagne présidentielle 2016 (« Billary » = Bill + Hillary Clinton) ; ≈ 0,24 M$ en juin 2017, retiré en 2018. | commune | commune | politique | à définir | r1 ; https://coinmarketcap.com/historical/20170611/ ; https://coinmarketcap.com/currencies/billarycoin/ |
| 1418 | SHIBORG INU | SHIBORG | BSC | oct. 2021 | ≈ 222 k$ en FDV (22/08/2022) | estimé | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en oct. 2021 ; pic vers le 22/08/2022 ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/shiborg-inu/ |
| 1419 | Putin Classic | PUTIC | blockchain propre | juin 2017 | ≈ 214 k$, 09/07/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Fork parodique de PutinCoin ; ≈ 0,21 M$ en juil. 2017, retiré en oct. 2017. | commune | commune | politique | à définir | r1 ; https://coinmarketcap.com/historical/20170709/ ; https://coinmarketcap.com/currencies/putin-classic/ |
| 1420 | Wall Street Baby | WSB | Ethereum | une paire WSB « WALL STREET BABY » existe depuis le 21/04/2023 (même jeton à vérifier) | ≈ 196 k$ (plancher : capitalisation actuelle) | estimé | mort |  | commune | commune |  | à définir | v1 n° 785 ; correction r3 ; CG `wall-street-baby` ; https://dexscreener.com/ethereum/0x15F20f9DFDf96CCf6AC96653b7C0aBfe4A9C9f0f |
| 1421 | ShibeCoin | SHIBE | blockchain propre | mai 2014 | ≈ 186 k$, 11/05/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Clone de la race du chien Doge (shibe) ; ≈ 0,19 M$ en mai 2014, retiré en 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140511/ ; https://coinmarketcap.com/currencies/shibecoin/ |
| 1422 | Grumpycoin | GRUMP | blockchain propre | mars 2014 | ≈ 171 k$, 09/03/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin du mème Grumpy Cat ; ≈ 0,17 M$ en mars 2014, disparu en août 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140309/ ; https://coinmarketcap.com/currencies/grumpycoin/ |
| 1423 | Murraycoin | MRY | blockchain propre | janv. 2014 | ≈ 162 k$, 09/03/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Hommage non autorisé à Bill Murray, dons promis à la fondation des frères Murray ; ≈ 0,16 M$ en mars 2014, moins de 5 cents l'unité en oct. 2014. | commune | commune | personne réelle | à définir | r1 ; https://coinmarketcap.com/historical/20140309/ ; https://m.washingtontimes.com/news/2014/oct/29/bill-murray-bitcoin-changes-face-of-digital-curran/ |
| 1424 | Orlycoin | ORLY | blockchain propre | avr. 2016 | ≈ 152 k$, 14/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin du mème du hibou « O RLY? » ; ≈ 0,15 M$ en janv. 2018, retiré en avril 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180114/ ; https://coinmarketcap.com/currencies/orlycoin/ |
| 1425 | Pandacoin (PANDA) | PANDA | blockchain propre | févr. 2014 | ≈ 151 k$, 23/02/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Clone de Doge homonyme de PND, lancé le même mois ; ≈ 0,15 M$ en févr. 2014, disparu en sept. 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140223/ ; https://coinmarketcap.com/currencies/pandacoin-panda/ |
| 1426 | BadgerCoin | BDG | blockchain propre | mai 2014 | ≈ 144 k$, 11/05/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin à blaireau (clin d'œil probable au mème « honey badger » du Bitcoin, à vérifier) ; ≈ 0,14 M$ en mai 2014, disparu en août. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140511/ ; https://coinmarketcap.com/currencies/badgercoin/ |
| 1427 | Conspiracycoin | CYC | blockchain propre | juil. 2014 | ≈ 139 k$, 20/07/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « complot » ; ≈ 0,14 M$ en juil. 2014, retiré en 2016. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140720/ ; https://coinmarketcap.com/currencies/conspiracycoin/ |
| 1428 | GeertCoin | GEERT | blockchain propre | mars 2017 | ≈ 132 k$, 14/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin à l'effigie de Geert Wilders, sorti pendant les législatives néerlandaises ; ≈ 0,13 M$ en janv. 2018, -98 % fin 2018. | commune | commune | politique | à définir | r1 ; https://coinmarketcap.com/historical/20180114/ ; https://coinmarketcap.com/currencies/geertcoin/ |
| 1429 | YoloCash | YLC | Ethereum (ERC-20) | août 2018 | ≈ 123 k$, 23/10/2018 (CMC, relevé quotidien) | sourcé | mort | Jeton « YOLO » ; ≈ 0,12 M$ en oct. 2018, puis capitalisation nulle. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/currencies/yolocash/historical-data/ |
| 1430 | Ponzicoin | PONZI | blockchain propre (mai 2016) | 2014-2017 (à vérifier) | ≈ 0,12 M$, 28/01/2018 | sourcé | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 717 ; correction r1 ; https://coinmarketcap.com/currencies/ponzicoin/historical-data/ |
| 1431 | FAILCoin | FAIL | blockchain propre | juin 2014 | ≈ 105 k$, 12/07/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « échec » assumé ; ≈ 0,1 M$ en 2015, retiré en sept. 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20150712/ ; https://coinmarketcap.com/currencies/failcoin/ |
| 1432 | Penguincoin (old) | PENG | blockchain propre | févr. 2014 | ≈ 104 k$, 23/02/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Clone à pingouin de la vague Doge ; ≈ 0,1 M$ en févr. 2014, disparu en décembre. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140223/ ; https://coinmarketcap.com/currencies/penguincoin-old/ |
| 1433 | Heisenberg | HEX | blockchain propre | mars 2014 | ≈ 95 k$, 19/06/2016 (CMC, relevé hebdomadaire) | sourcé | mort | Coin au pseudonyme de Walter White (Breaking Bad) ; ≈ 95 k$, retiré en 2016. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20160619/ ; https://coinmarketcap.com/currencies/heisenberg/ |
| 1434 | 23 Skidoo | CHAO | blockchain propre | juil. 2015 | ≈ 91 k$, 09/07/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Coin tiré d'une vieille expression d'argot américain et d'un mème « discordien » (à vérifier) ; ≈ 91 k$ en juil. 2017, retiré en sept. 2017. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20170709/ ; https://coinmarketcap.com/currencies/23-skidoo/ |
| 1435 | RabbitCoin | RBBT | blockchain propre | août 2014 | ≈ 91 k$, 09/07/2015 (CMC, relevé quotidien) | sourcé | mort | Clone à lapin de 2014 ; ≈ 91 k$ en juil. 2015, capitalisation nulle aujourd'hui. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/currencies/rabbitcoin/historical-data/ |
| 1436 | BatCoin | BAT | blockchain propre | mars 2014 | ≈ 90 k$, 06/04/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin à chauve-souris (Batman, à vérifier) ; ≈ 90 k$ en avril 2014, retiré en 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140406/ ; https://coinmarketcap.com/currencies/batcoin/ |
| 1437 | DuckDuckCoin | DUCK | blockchain propre | mars 2014 | ≈ 81 k$, 16/03/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Clone à canard de la vague Doge ; ≈ 81 k$ en mars 2014, retiré en 2016. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140316/ ; https://coinmarketcap.com/currencies/duckduckcoin/ |
| 1438 | Cheesecoin | CHEESE | blockchain propre | oct. 2018 | ≈ 77 k$, 23/10/2018 (CMC, relevé quotidien) ; ≈ 672 k$ le 11/05/2021 | sourcé | mort | Coin « fromage » ; ≈ 67 k$ en oct. 2018, sursaut à ≈ 0,67 M$ en mai 2021, puis capitalisation nulle. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/currencies/cheesecoin/historical-data/ |
| 1439 | FCKBanksCoin | FCK | blockchain propre | mars 2014 | ≈ 63 k$, 06/04/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « f*ck les banques » ; ≈ 63 k$ en avril 2014, disparu le mois même. | commune | commune | obscène | à définir | r1 ; https://coinmarketcap.com/historical/20140406/ ; https://coinmarketcap.com/currencies/fckbankscoin/ |
| 1440 | X-Children | CHILD | blockchain propre | sept. 2014 | ≈ 63 k$, 12/10/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin au nom des X-Men (à vérifier) ; ≈ 63 k$ en oct. 2014, retiré en 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20141012/ ; https://coinmarketcap.com/currencies/x-children/ |
| 1441 | Dobbscoin | BOB | blockchain propre | août 2014 | ≈ 54 k$, 23/07/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Coin de la parodie religieuse Church of the SubGenius (« Bob » Dobbs, ticker BOB) ; ≈ 54 k$ en 2017, retiré en août 2017. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20170723/ ; https://coinmarketcap.com/currencies/dobbscoin/ |
| 1442 | DarkShibe | DSB | blockchain propre | oct. 2014 | ≈ 53 k$, 26/10/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Clone « sombre » de Doge, de la vague DogeCoinDark ; ≈ 53 k$ en oct. 2014, retiré en 2016. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20141026/ ; https://coinmarketcap.com/currencies/darkshibe/ |
| 1443 | EmotiCoin | EMO | blockchain propre | mars 2014 | ≈ 51 k$, 06/04/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin à émoticônes ; ≈ 51 k$ en avril 2014, disparu en août 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140406/ ; https://coinmarketcap.com/currencies/emoticoin/ |
| 1444 | Animecoin (2014) | ANI | blockchain propre | mars 2014 | ≈ 50 k$, 02/03/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin anime de la vague 2014 ; ≈ 50 k$ en mars 2014, sans valeur ensuite. Distinct d'Animecoin ANIME (carte 20). | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140302/ ; https://coinmarketcap.com/currencies/animecoin/ |
| 1445 | Gossipcoin | GOSS | blockchain propre | sept. 2018 | ≈ 48 k$, 28/10/2018 (CMC, relevé hebdomadaire) | sourcé | à vérifier | Coin « ragots » ; ≈ 48 k$ en oct. 2018, -47 % deux mois plus tard (état actuel à vérifier). | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20181028/ ; https://coinmarketcap.com/currencies/gossipcoin/ |
| 1446 | DolphinCoin | DOLP | blockchain propre | oct. 2014 | ≈ 36 k$, 26/10/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Clone à dauphin ; ≈ 36 k$, coté deux semaines seulement en 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20141026/ ; https://coinmarketcap.com/currencies/dolphincoin/ |
| 1447 | GorillaBucks | BUCKS | blockchain propre | juil. 2015 | ≈ 34 k$, 05/07/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin à gorille ; ≈ 34 k$ en juil. 2015, retiré en sept. 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20150705/ ; https://coinmarketcap.com/currencies/gorillabucks/ |
| 1448 | MugatuCoin | MUGA | blockchain propre | juin 2014 | ≈ 30 k$, 15/06/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin du méchant Mugatu (Zoolander) ; ≈ 30 k$ en juin 2014, retiré en mars 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140615/ ; https://coinmarketcap.com/currencies/mugatucoin/ |
| 1449 | Pyramids | PYRA | blockchain propre | août 2014 | ≈ 28 k$, 24/08/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « pyramide » (clin d'œil aux combines pyramidales, à vérifier) ; ≈ 28 k$ en août 2014, disparu en décembre. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140824/ ; https://coinmarketcap.com/currencies/pyramids/ |
| 1450 | Huskycoin | HC | blockchain propre | mai 2014 | ≈ 27 k$, 01/06/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Clone à husky de la vague Doge ; ≈ 27 k$ début juin 2014, disparu en juillet 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140601/ ; https://coinmarketcap.com/currencies/huskycoin/ |
| 1451 | Lycancoin | LYC | blockchain propre | avr. 2014 | ≈ 27 k$, 27/04/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin loup-garou ; ≈ 27 k$ en avril 2014, retiré en 2016. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140427/ ; https://coinmarketcap.com/currencies/lycancoin/ |
| 1452 | LemurCoin | LMR | blockchain propre | oct. 2014 | ≈ 25 k$, 12/10/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin à lémurien ; ≈ 25 k$ à son entrée sur CMC, retiré en 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20141012/ ; https://coinmarketcap.com/currencies/lemurcoin/ |
| 1453 | Aliencoin | ALN | blockchain propre | mars 2014 | ≈ 23 k$, 31/08/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin extraterrestre ; ≈ 23 k$ en août 2014, retiré en 2016. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140831/ ; https://coinmarketcap.com/currencies/aliencoin/ |
| 1454 | Selfiecoin | SLFI | blockchain propre | mars 2015 | ≈ 21 k$, 17/12/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Coin du selfie ; ≈ 21 k$ en déc. 2017, retiré en 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20171217/ ; https://coinmarketcap.com/currencies/selfiecoin/ |
| 1455 | CrackCoin | CRACK | blockchain propre | sept. 2014 | ≈ 20 k$, 21/09/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin au nom de la drogue ; ≈ 20 k$ en sept. 2014, retiré en 2016. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140921/ ; https://coinmarketcap.com/currencies/crackcoin/ |
| 1456 | Doomcoin | DOOM | blockchain propre | août 2014 | ≈ 19 k$, 03/08/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « Doom » ; ≈ 19 k$ en août 2014, disparu en septembre. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140803/ ; https://coinmarketcap.com/currencies/doomcoin/ |
| 1457 | BananaBits | NANAS | blockchain propre | juin 2015 | ≈ 17 k$, 21/06/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin banane (ticker NANAS) ; ≈ 17 k$ en juin 2015, retiré en sept. 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20150621/ ; https://coinmarketcap.com/currencies/bananabits/ |
| 1458 | Dougcoin | DOUG | blockchain propre | avr. 2014 | ≈ 14 k$, 20/04/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « Doug » (mème à vérifier) ; ≈ 14 k$ en avril 2014, disparu en mai. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140420/ ; https://coinmarketcap.com/currencies/dougcoin/ |
| 1459 | MtGoxCoin | GOX | blockchain propre | mars 2014 | ≈ 14 k$, 30/03/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin moquant la faillite de Mt. Gox ; ≈ 14 k$ en mars 2014, disparu en septembre. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140330/ ; https://coinmarketcap.com/currencies/mtgoxcoin/ |
| 1460 | NoodlyAppendageCoin | NDL | blockchain propre | 02/01/2014 | ≈ 14 k$, 23/03/2014 (CMC, relevé hebdomadaire) | sourcé | mort | « La pièce des pastafariens » (Monstre en spaghettis volant), annoncée sur Bitcointalk ; ≈ 14 k$ en mars 2014, disparue en avril. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140323/ ; https://bitcointalk.org/index.php?topic=396227 |
| 1461 | Fonziecoin | FONZ | blockchain propre | sept. 2015 | ≈ 13 k$, 11/10/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin du Fonz (Happy Days) ; ≈ 13 k$ en oct. 2015, sans valeur ensuite. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20151011/ ; https://coinmarketcap.com/currencies/fonziecoin/ |
| 1462 | Tomatocoin | TMT | blockchain propre | août 2014 | ≈ 13 k$, 03/08/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin tomate ; ≈ 13 k$ en août 2014, disparu en novembre. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140803/ ; https://coinmarketcap.com/currencies/tomatocoin/ |
| 1463 | Hobbitcoin | HBC | blockchain propre | juin 2014 | ≈ 11 k$, 29/06/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin hobbit ; ≈ 11 k$, coté un mois en 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140629/ ; https://coinmarketcap.com/currencies/hobbitcoin/ |
| 1464 | Isiscoin | ISIS | blockchain propre | juil. 2014 | ≈ 11 k$, 13/07/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin de 2014 au nom devenu celui de l'État islamique ; ≈ 11 k$, disparu en août 2014. | commune | commune | obscène | à définir | r1 ; https://coinmarketcap.com/historical/20140713/ ; https://coinmarketcap.com/currencies/isiscoin/ |
| 1465 | RipoffCoin | RIPO | blockchain propre | août 2014 | ≈ 10 k$, 07/09/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « arnaque » assumée dans le nom ; ≈ 10 k$ en sept. 2014, retiré en 2016. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140907/ ; https://coinmarketcap.com/currencies/ripoffcoin/ |
| 1466 | NewWorldOrderCoin | NWO | blockchain propre | sept. 2014 | ≈ 9 k$, 07/09/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin complotiste « Nouvel ordre mondial » ; ≈ 9 k$ en sept. 2014, disparu en décembre. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140907/ ; https://coinmarketcap.com/currencies/newworldordercoin/ |
| 1467 | TacoCoin | TCO | blockchain propre | juil. 2014 | ≈ 9 k$, 27/07/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin taco ; ≈ 9 k$ en juil. 2014, retiré en 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140727/ ; https://coinmarketcap.com/currencies/tacocoin/ |
| 1468 | Chococoin | CCC | blockchain propre | mars 2015 | ≈ 7 k$, 29/03/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin chocolat ; ≈ 7 k$ en mars 2015, retiré en mai 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20150329/ ; https://coinmarketcap.com/currencies/chococoin/ |
| 1469 | Fetish | FETISH | blockchain propre | oct. 2014 | ≈ 7 k$, 21/06/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « fétiche » ; ≈ 7 k$ en 2015, retiré fin 2015. | commune | commune | obscène | à définir | r1 ; https://coinmarketcap.com/historical/20150621/ ; https://coinmarketcap.com/currencies/fetish/ |
| 1470 | AnalCoin | ANAL | blockchain propre | mars 2015 | ≈ 6 k$, 12/04/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin au nom obscène ; ≈ 6 k$ en avril 2015, retiré en 2016. | commune | commune | obscène | à définir | r1 ; https://coinmarketcap.com/historical/20150412/ ; https://coinmarketcap.com/currencies/analcoin/ |
| 1471 | CandyCoin | YUM | blockchain propre | nov. 2014 | ≈ 6 k$, 16/11/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin bonbon (ticker YUM) ; ≈ 6 k$, retiré en mars 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20141116/ ; https://coinmarketcap.com/currencies/candycoin/ |
| 1472 | Unattainium | UNAT | blockchain propre | août 2014 | ≈ 6 k$, 17/08/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Parodie d'Unobtanium (le métal d'Avatar) ; ≈ 6 k$, retiré en 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140817/ ; https://coinmarketcap.com/currencies/unattainium/ |
| 1473 | CryptoMETH | METH | blockchain propre | juin 2014 | ≈ 5 k$, 01/06/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « méthamphétamine » ; ≈ 5 k$, disparu en sept. 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140601/ ; https://coinmarketcap.com/currencies/cryptometh/ |
| 1474 | Tamagucci | TAM | blockchain propre | juin 2015 | ≈ 5 k$, 08/11/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Jeu de mots Tamagotchi-Gucci ; ≈ 5 k$, retiré fin 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20151108/ ; https://coinmarketcap.com/currencies/tamagucci/ |
| 1475 | ColbertCoin | CC | blockchain propre | avr. 2014 | ≈ 4 k$, 27/04/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin à l'effigie de Stephen Colbert ; ≈ 4 k$, disparu en juil. 2014. | commune | commune | personne réelle | à définir | r1 ; https://coinmarketcap.com/historical/20140427/ ; https://coinmarketcap.com/currencies/colbertcoin/ |
| 1476 | DogeBlackCoin | DOGEBC | blockchain propre | oct. 2014 | ≈ 4 k$, 26/10/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Clone « noir » de Doge ; ≈ 4 k$, disparu fin 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20141026/ ; https://coinmarketcap.com/currencies/dogeblackcoin/ |
| 1477 | NopeCoin | NOPE | blockchain propre | oct. 2014 | ≈ 3 k$, 26/10/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin du mème « Nope » ; ≈ 3 k$, disparu en févr. 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20141026/ ; https://coinmarketcap.com/currencies/nopecoin/ |
| 1478 | SiameseCoin | SIS | blockchain propre | juil. 2014 | ≈ 3 k$, 13/07/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin chat siamois ; ≈ 3 k$, coté six semaines. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140713/ ; https://coinmarketcap.com/currencies/siamesecoin/ |
| 1479 | SJWCoin | SJW | blockchain propre | août 2015 | ≈ 3 k$, 22/11/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin moquant les « social justice warriors » ; ≈ 3 k$, sans valeur ensuite. | commune | commune | politique | à définir | r1 ; https://coinmarketcap.com/historical/20151122/ ; https://coinmarketcap.com/currencies/sjwcoin/ |
| 1480 | BDSM | BDSM | blockchain propre | oct. 2014 | ≈ 2 k$, 19/07/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin au nom sexuel ; ≈ 2 k$, retiré fin 2015. | commune | commune | obscène | à définir | r1 ; https://coinmarketcap.com/historical/20150719/ ; https://coinmarketcap.com/currencies/bdsm/ |
| 1481 | Frycoin | FRY | blockchain propre | mai 2014 | ≈ 2 k$, 18/05/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin frite (ou Fry de Futurama, à vérifier) ; ≈ 2 k$, sans valeur ensuite. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140518/ ; https://coinmarketcap.com/currencies/frycoin/ |
| 1482 | KimDotCoin | DOT | blockchain propre | sept. 2014 | ≈ 2 k$, 28/09/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin à l'effigie de Kim Dotcom ; ≈ 2,5 k$, disparu en déc. 2014. | commune | commune | personne réelle | à définir | r1 ; https://coinmarketcap.com/historical/20140928/ ; https://coinmarketcap.com/currencies/kimdotcoin/ |
| 1483 | LeproCoin | LPC | blockchain propre | mars 2014 | ≈ 2 k$, 16/03/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin farfadet (leprechaun) ; ≈ 2 k$, disparu en juin 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140316/ ; https://coinmarketcap.com/currencies/leprocoin/ |
| 1484 | Magic Internet Money | MIM | blockchain propre | mars 2014 | ≈ 2 k$, 23/03/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin du mème « magic internet money » (sorcier Bitcoin de Reddit) ; ≈ 2 k$, coté deux semaines en 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20140323/ ; https://coinmarketcap.com/currencies/magic-internet-money/ |
| 1485 | NineElevenTruthCoin | NTC | blockchain propre | févr. 2015 | ≈ 2 k$, 05/04/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin complotiste sur le 11-Septembre ; ≈ 2 k$, retiré en juin 2015. | commune | commune | politique | à définir | r1 ; https://coinmarketcap.com/historical/20150405/ ; https://coinmarketcap.com/currencies/nineeleventruthcoin/ |
| 1486 | PotatoCoin | SPUDS | blockchain propre | oct. 2014 | ≈ 2 k$, 19/10/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin patate (ticker SPUDS) ; ≈ 2 k$, retiré en mars 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20141019/ ; https://coinmarketcap.com/currencies/potatocoin/ |
| 1487 | ConfessionCoin | CFN | blockchain propre | déc. 2014 | ≈ 1 k$, 18/01/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « confession » ; ≈ 1 k$, retiré en 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20150118/ ; https://coinmarketcap.com/currencies/confessioncoin/ |
| 1488 | FistBump | FIST | blockchain propre | juin 2015 | ≈ 1 k$, 24/07/2016 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « check du poing » ; ≈ 1 k$, retiré en 2016. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20160724/ ; https://coinmarketcap.com/currencies/fistbump/ |
| 1489 | REKTcoin | REKT | blockchain propre | nov. 2014 | ≈ 1 k$, 16/11/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin du mème « rekt » ; ≈ 1 k$, coté six semaines fin 2014. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20141116/ ; https://coinmarketcap.com/currencies/rektcoin/ |
| 1490 | 100xCoin | 100X | BSC | avr. 2021 | inconnu | inconnu | mort | Mème « x100 » sur BSC, lancé en avr. 2021 ; volume record de 1,5 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/100xcoin/ |
| 1491 | ABG | ABG | NEAR | à vérifier | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 804 |
| 1492 | Andwu Tet | à vérifier | Solana | Noms mal orthographiés, 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 537 |
| 1493 | Arbi Pepe | PEPE (Arbitrum) | Arbitrum | à vérifier | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 542 |
| 1494 | Arbinu | ARBINU | Arbitrum | 2023 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 543 |
| 1495 | Baby Arbitrum | BARB | Arbitrum | 2023 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 545 |
| 1496 | Bananacoin | BCO | à vérifier | 2018 (à vérifier) | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 550 |
| 1497 | Base Baboon | BOON | Base | mars 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 553 |
| 1498 | Biebercoin | BRC | blockchain propre | juil. 2015 | inconnu (capitalisation non renseignée par CMC) | inconnu | mort | Coin à l'effigie de Justin Bieber ; capitalisation jamais renseignée par CMC, retiré en 2016. | commune | commune | personne réelle | à définir | r1 ; https://coinmarketcap.com/currencies/biebercoin/historical-data/ |
| 1499 | Big Dog Coin | BDOG | BNB Chain | nov. 2021 (ajout CMC) | inconnu (classé par CMC du 21 nov. 2021 au 27 févr. 2022, sans capitalisation publiée) | inconnu | mort | « Big Dog » de la vague de clones chiens de nov.-déc. 2021 ; sorti du classement en févr. 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/big-dog-coin/ |
| 1500 | BitCone | CONE | Polygon | sept. 2022 | inconnu (donnée CMC aberrante : 21 Md$ sans volume) | inconnu | mort | Jeton distribué gratuitement aux détenteurs des avatars Reddit « Cone Head » sur Polygon (20/09/2022), pourboires sur r/ConeHeads ; pic le 02/11/2022, aujourd'hui quasi nul. | commune | commune |  | à définir | r2 ; https://eulerpool.com/crypto/CONE ; https://coinmarketcap.com/currencies/bitcone/ |
| 1501 | blobs | BLOBS | Ethereum | 11/02/2024 | inconnu | inconnu | mort | Mème des « blobs » de la mise à jour Dencun (EIP-4844) de 2024. | commune | commune |  | à définir | r3 ; https://dexscreener.com/ethereum/0x39dE85301c78F4D623E5c05cDE2fD119a3a92cd9 |
| 1502 | Bombardiro | à vérifier | Solana (à confirmer) | Brainrot italien, 2025-2026 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 569 |
| 1503 | Bomeow | BOMEOW | Solana | Avril 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 570 |
| 1504 | Boom Shiba | BOOMSHIBA | BSC | nov. 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en nov. 2021 ; volume record de 2,9 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/boom-shiba/ |
| 1505 | Bugg Inu | BUGG | Ethereum | mai 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en mai 2021 ; volume record de 3,2 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/bugg-inu/ |
| 1506 | Captain Shibarrow | SHIBARROW | BSC | janv. 2022 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en janv. 2022 ; volume record de 3,1 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/captain-shibarrow/ |
| 1507 | CATS•IN•THE•SATS | CATS | Bitcoin (Runes) | 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 576 |
| 1508 | Cheems Inu | CINU | Ethereum | nov. 2021 | inconnu | inconnu | mort | Jeton « Inu » du mème Cheems sur Ethereum, lancé en nov. 2021 ; volume record de 6,4 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/cheems-inu/ |
| 1509 | ChillDeer | CHILLDEER | Solana | Noël 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 580 |
| 1510 | Christmas Floki X | CFloki X | BNB Chain | déc. 2021 (ajout CMC) | inconnu (classé par CMC du 5 déc. 2021 au 5 déc. 2021, sans capitalisation publiée) | inconnu | mort | Floki de Noël sorti en déc. 2021, au moment où la mode Floki battait son plein ; une seule semaine au classement. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/christmas-floki-x/ |
| 1511 | CoShi Inu | COSHI | Ethereum | mai 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en mai 2021 ; volume record de 27,9 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/coshi-inu/ |
| 1512 | CYPHER•GENESIS | CYPHER | Bitcoin (Runes) | 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 591 |
| 1513 | Dave Fartnoy | FARTNOY | Solana | 10 févr. 2025 | inconnu (≈ 4,4 M$ au moment de l'article) | inconnu | à vérifier (introuvable sur DexScreener) | Parodie de Portnoy, qui en achète 10 % « comme objet de collection ». | commune | commune | personne réelle, obscène | à définir | r3 ; https://decrypt.co/305323/dave-portnoy-solana-meme-coin-jailstool |
| 1514 | DED † | DED | Polkadot | 2023 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 594 |
| 1515 | Dink Doink | DINK | à vérifier | 2021 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 597 |
| 1516 | Doge Dash | DOGEDASH | à vérifier | fin 2021 (à vérifier) | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 599 |
| 1517 | Dogefather | DOGEFATHER | BSC | mai 2021 | inconnu | inconnu | mort | Mème Elon Musk (surnom « Dogefather ») sur BSC, lancé en mai 2021 ; aujourd'hui plus coté. | commune | commune | personne réelle | à définir | r2 ; https://coinmarketcap.com/currencies/dogefather/ |
| 1518 | DogeWarrior | DWR | BNB Chain | août 2021 (ajout CMC) | inconnu (classé par CMC du 29 août 2021 au 7 nov. 2021, sans capitalisation publiée) | inconnu | mort | Doge guerrier d'août 2021 sur BSC ; disparu en nov. 2021. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/dogewarrior/ |
| 1519 | DogeZilla | DOGEZILLA | BSC | oct. 2021 | inconnu | inconnu | mort | Mème Doge + Godzilla sur BSC, lancé en oct. 2021 ; volume record de 49,0 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/dogezilla/ |
| 1520 | DogWifCat | à vérifier | Solana | Mars 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 608 |
| 1521 | Doll (Ivana Knoll) | DOLL | Solana | 6 juin 2024 | inconnu | inconnu | mort (≈ 1,5 k$, volume nul) | Jeton du mannequin croate de la vague Sahil Arora de juin 2024, rattaché à la même adresse que RICH et SOULJA. | commune | commune | personne réelle | à définir | r3 ; https://www.theblock.co/post/298428/x-bans-alleged-celebrity-memecoin-scammer-sahil-arora ; https://dexscreener.com/solana/ashdmjl4ys74f7ebcg9kz5uns7zluvhnwnzqvcf9cnlc |
| 1522 | Dragon Sun | DRGN | Tron | août 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 610 |
| 1523 | DropArb | DROP | Arbitrum | à vérifier | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 611 |
| 1524 | Elon Buys Twitter | EBT | à vérifier | 2022 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune | personne réelle | à définir | v1 n° 613 |
| 1525 | ElonGate † | ELONGATE | BNB Chain | 2021 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune | personne réelle | à définir | v1 n° 614 |
| 1526 | ETHEREUM IS GOOD | EBULL | Ethereum | 21/08/2024 | inconnu | inconnu | mort | Taureau mème né d'un slogan pro-Ethereum de l'été 2024, volume résiduel. | commune | commune |  | à définir | r3 ; https://dexscreener.com/ethereum/0x71297312753EA7A2570a5a3278eD70D9a75F4f44 |
| 1527 | F*** Tristan | FTRISTAN | Solana | juin 2024 | inconnu | inconnu | mort (introuvable sur DexScreener) | Jeton d'Andrew Tate qui moque son frère Tristan, mort comme les autres. | commune | commune | personne réelle, obscène | à définir | r3 ; https://cointelegraph.com/news/andrew-tate-endorsed-memecoins-crashed-zero |
| 1528 | Fairmoon | FAIR | BSC | mars 2021 | inconnu | inconnu | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) sur BSC, lancé en mars 2021 ; volume record de 3,7 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/fairmoon/ |
| 1529 | Fantasy Pepe | FEPE | Polygon | 2025 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 616 |
| 1530 | Fantom Doge | RIP | Fantom | sept. 2021 (ajout CMC) | inconnu (classé par CMC du 19 sept. 2021 au 16 janv. 2022, sans capitalisation publiée) | inconnu | mort | Doge de Fantom (ticker RIP), sept. 2021, première saison DeFi de Fantom ; mort début 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/fantom-doge/ |
| 1531 | Floki Elon | FLOKIELON | BSC | oct. 2021 | inconnu | inconnu | mort | Jeton né du chien Floki d'Elon Musk (tweet du 25/06/2021) sur BSC, lancé en oct. 2021 ; volume record de 1,4 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune | personne réelle | à définir | r2 ; https://coinmarketcap.com/currencies/floki-elon/ |
| 1532 | Floki Shiba | FSHIB | BSC | juin 2021 | inconnu | inconnu | mort | Jeton né du chien Floki d'Elon Musk (tweet du 25/06/2021) sur BSC, lancé en juin 2021 ; volume record de 3,1 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/floki-shiba/ |
| 1533 | Flokinomics | FLOKIN | BSC | oct. 2021 | inconnu | inconnu | mort | Jeton né du chien Floki d'Elon Musk (tweet du 25/06/2021) sur BSC, lancé en oct. 2021 ; volume record de 6,1 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/flokinomics/ |
| 1534 | G-Unit (piratage de 50 Cent) | GUNIT | Solana (pump.fun) | 21 juin 2024 | inconnu (18,6 M$ échangés en 40 min) | inconnu | mort (≈ 150 k$ en juin 2024, absent aujourd'hui) | Un pirate prend le compte X de 50 Cent, promeut le jeton et repart avec environ 3 M$ selon le rappeur. | commune | commune | personne réelle, arnaque avérée | à définir | r3 ; https://decrypt.co/236572/50-cent-twitter-hacked-solana-meme-coin/ ; https://cointelegraph.com/news/rapper-50-cent-x-hacker-memecoin-rug-pull-scam |
| 1535 | Germany Token | GER | Solana | juin 2024 | inconnu | inconnu | mort | Jeton relayé par Tate ; Bubblemaps note une chute de 99 % deux mois après son premier achat. | commune | commune | personne réelle | à définir | r3 ; https://cointelegraph.com/news/andrew-tate-endorsed-memecoins-crashed-zero |
| 1536 | GloryDoge | GLORYD | BNB Chain | oct. 2021 (ajout CMC) | inconnu (classé par CMC du 31 oct. 2021 au 6 mars 2022, sans capitalisation publiée) | inconnu | mort | Doge « glorieux » d'oct. 2021, clone BSC à taxe ; disparu en mars 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/glorydoge/ |
| 1537 | GMEKitty | GMEKITTY | Solana (à vérifier) | mai 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 630 |
| 1538 | GNEAR | GNEAR | NEAR | à vérifier | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 805 |
| 1539 | Goldenloaf (Yanukovych coin) | GLY | blockchain propre (à vérifier) | 2014 | inconnu | inconnu | mort | Coin moquant la « miche en or » trouvée chez Viktor Ianoukovitch en 2014, classé par CoinDesk parmi les altcoins les plus étranges de l'année ; vendu sur C-CEX puis oublié. | commune | commune | politique | à définir | r1 ; https://www.coindesk.com/strangest-altcoins-2014/ ; https://www.coindesk.com/things-alt-dogecoins-future-prep-strange-gold-pegs-friendly-scam/ |
| 1540 | GotFomo | GTFO | blockchain propre | juin 2015 | ≈ 0 k$, 21/06/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin au ticker « GTFO » ; moins de 1 k$, retiré en 2016. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20150621/ ; https://coinmarketcap.com/currencies/gotfomo/ |
| 1541 | GREED (Dave Portnoy) | GREED | Solana (pump.fun) | févr. 2025 | inconnu | inconnu | mort (≈ 3 k$) | Portnoy lance GREED et vend tout en moins d'une heure, puis lance GREED2 ; la polémique le pousse vers JAILSTOOL. | commune | commune | personne réelle | à définir | r3 ; https://tribune.com.pk/story/2529818/entertainment ; https://dexscreener.com/solana/fdjkhuexhigvdsieuyykjxsnkddbvtmgrjg4zz5qmaak |
| 1542 | Green Shiba Inu | GINU | BSC | mai 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en mai 2021 ; volume record de 3,5 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/green-shiba-inu/ |
| 1543 | Grumpy Cat Coin | GRUMPY | Ethereum | mars 2021 | inconnu | inconnu | mort | Mème du chat Grumpy Cat (mars 2021) : +1 000 % en un jour, 70 000 $ levés pour un refuge selon Cointelegraph. | commune | commune |  | à définir | r2 ; https://www.mediaite.com/news/grumpy-cats-ghost-takes-over-crypto-as-grumpy-coin-surges-1000-in-a-day ; https://www.coingecko.com/en/coins/grumpy-cat-coin |
| 1544 | Hasbulla | HASBI | Solana | nov.-déc. 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 636 |
| 1545 | HeMa | à vérifier | BNB Chain | janv. 2026 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 639 |
| 1546 | HODL 2.0 | HODL | BNB Chain | août 2021 (ajout CMC) | inconnu (classé par CMC du 15 août 2021 au 7 nov. 2021, sans capitalisation publiée) | inconnu | mort | Relance « 2.0 » d'un jeton HODL (le mot fétiche des crypto-forums) en août 2021 ; sorti du classement trois mois plus tard. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/hodl-2-0/ |
| 1547 | I like this coin | LIKE | Solana | mars 2024 | inconnu (prévente de 52 220 SOL, ~7,7 M$) | inconnu | à vérifier (FDV DexScreener ≈ 3 M$, liquidité anormale) | Plus grosse prévente abandonnée relevée par ZachXBT : 52 220 SOL levés par pokeee.eth, -90 % en huit heures. | commune | commune | arnaque avérée | à définir | r3 ; https://cointelegraph.com/news/12-solana-presale-memecoins-abandoned-after-one-month ; https://cryptopotato.com/zachxbt-exposes-12-abandoned-solana-presale-meme-coin-projects/ |
| 1548 | I will poop it NFT | SHIT | Ethereum | juin 2022 | inconnu | inconnu | mort | Mème sur Ethereum, lancé en juin 2022 ; volume record de 25,1 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune | obscène | à définir | r2 ; https://coinmarketcap.com/currencies/i-will-poop-it-nft/ |
| 1549 | Intel (Intear) | INTEL | NEAR | à vérifier | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 647 |
| 1550 | International Squid Games | SQUIDGAMES | BSC | sept. 2021 | inconnu | inconnu | mort | Copie du jeton SQUID sur BSC, tombée le même jour que l'original selon CoinDesk (01/11/2021) ; plus coté. | commune | commune |  | à définir | r2 ; https://www.coindesk.com/markets/2021/11/01/squid-game-token-crashes-developers-say-theyve-left-the-project/ ; https://coinmarketcap.com/currencies/international-squid-games/ |
| 1551 | JaredFromSubway | JARED | Ethereum | 08/05/2023 | inconnu | inconnu | mort | Jeton moqueur du robot MEV « jaredfromsubway.eth » qui a sandwiché les acheteurs de PEPE en 2023. | commune | commune | personne réelle | à définir | r3 ; https://dexscreener.com/ethereum/0xbc2D206A5ecEA163d054B71ACBA2b1628f4ECBC1 |
| 1552 | Jindoge | JINDOGE | Ethereum | mai 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en mai 2021 ; volume record de 45,9 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/jindoge/ |
| 1553 | Kekec the Balkan Dwarf | KEKEC | Ethereum | 27/10/2023 | inconnu | inconnu | mort | Mème du nain du dessin animé slovène Kekec, petite communauté des Balkans. | commune | commune |  | à définir | r3 ; https://dexscreener.com/ethereum/0x8C7AC134ED985367EADC6F727d79E8295E11435c |
| 1554 | Kermit | KERMIT | Ethereum | 12/05/2023 | inconnu | inconnu | mort | Grenouille Kermit lancée en pleine saison Pepe de mai 2023, puis oubliée. | commune | commune |  | à définir | r3 ; https://dexscreener.com/ethereum/0xfe625Bb2D2a0f24aCE72aDc3365f203771495e39 |
| 1555 | Khamzat Chimaev | SMASH | Solana | juin 2024 | inconnu | inconnu | à vérifier | Le jeton du combattant UFC perd 94 % dès son premier jour. | commune | commune | personne réelle | à définir | r3 ; https://www.blocmates.com/articles/an-analysis-of-solanas-celebrity-memecoin-invasion |
| 1556 | Kilo Shiba Inu | KSHIB | à vérifier | janv. 2022 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur à vérifier, lancé en janv. 2022 ; volume record de 11,1 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/kilo-shiba-inu/ |
| 1557 | King Floki | KING | BSC | nov. 2021 | inconnu | inconnu | mort | Jeton né du chien Floki d'Elon Musk (tweet du 25/06/2021) sur BSC, lancé en nov. 2021 ; volume record de 4,8 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/king-floki/ |
| 1558 | Kurama Inu | KUNU | Ethereum | oct. 2021 | inconnu | inconnu | mort | Jeton « Inu » inspiré de Kurama (Naruto) sur Ethereum, lancé en oct. 2021 ; volume record de 1,2 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/kuramainu/ |
| 1559 | La Doge de Papel | LDDP | BNB Chain | nov. 2021 (ajout CMC) | inconnu (classé par CMC du 21 nov. 2021 au 27 mars 2022, sans capitalisation publiée) | inconnu | mort | Doge déguisé en braqueur de « La casa de papel », mème BSC de fin 2021 ; mort au printemps 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/la-doge-de-papel/ |
| 1560 | Ligo | LIGO | Bitcoin (BRC-20) | 2023-2024 | inconnu | inconnu | mort |  | commune | commune |  | à définir | v1 n° 659 ; CG `ligo-ordinals` |
| 1561 | Lucky Meow Coin | LMAO | Solana | TikTok, fin 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 663 |
| 1562 | MaskDoge | MASKDOGE | BNB Chain | sept. 2021 (ajout CMC) | inconnu (classé par CMC du 12 sept. 2021 au 10 avr. 2022, sans capitalisation publiée) | inconnu | mort | Doge masqué de sept. 2021, clone BSC parmi des centaines ; plus coté après avril 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/maskdoge/ |
| 1563 | Maxi Doge | MAXI | BNB Chain (à vérifier) | 2026 (à vérifier) | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 668 |
| 1564 | MEME•ECONOMICS | MEMERUNE | Bitcoin (Runes) | 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 670 |
| 1565 | Mice | MICE | Bitcoin (BRC-20) | 2023-2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 672 |
| 1566 | MileyCyrusCoin | MCC | blockchain propre | sept. 2014 | ≈ 0 k$, 21/09/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin à l'effigie de Miley Cyrus ; moins de 1 k$, disparu en déc. 2014. | commune | commune | personne réelle | à définir | r1 ; https://coinmarketcap.com/historical/20140921/ ; https://coinmarketcap.com/currencies/mileycyruscoin/ |
| 1567 | Mini Baby Doge | MINIBABYDOGE | BSC | juil. 2021 | inconnu | inconnu | mort | Clone de Dogecoin sur BSC, lancé en juil. 2021 ; volume record de 1,5 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/mini-baby-doge/ |
| 1568 | Mini Kishu | MINIKISHU | BSC | sept. 2021 | inconnu | inconnu | mort | Mini-clone de Kishu Inu sur BSC, lancé en sept. 2021 ; volume record de 1,6 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/mini-kishu/ |
| 1569 | Mini Shiba | MINISHIBA | BSC | juil. 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en juil. 2021 ; volume record de 12,9 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/mini-shiba/ |
| 1570 | Molandak | MOLANDAK | Monad | 2025 † | inconnu | inconnu | mort |  | commune | commune |  | à définir | v1 n° 677 ; CG `molandak-2` |
| 1571 | MONCAT | MONCAT | Monad | 2025 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 681 |
| 1572 | Moon Token | MOONTOKEN | BNB Chain | avr. 2021 (ajout CMC) | inconnu (classé par CMC du 25 avr. 2021 au 24 oct. 2021, sans capitalisation publiée) | inconnu | mort | Clone SafeMoon générique (« Moon ») d'avril 2021, au plus fort de la saison des jetons à taxe ; disparu fin 2021. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/moon-token/ |
| 1573 | MOONKE | MOONKE | Solana | mars 2024 | inconnu (prévente de 37 470 SOL, ~5,8 M$) | inconnu | mort | Prévente de RockyXBT, 2e plus grosse de la liste ZachXBT des projets abandonnés ; effondrée dès le lancement. | commune | commune | arnaque avérée | à définir | r3 ; https://cointelegraph.com/news/12-solana-presale-memecoins-abandoned-after-one-month ; https://coingape.com/solana-meme-coin-over-26m-sol-lost-in-rugged-presales/ |
| 1574 | MoonMoon | MOONMOON | BSC | avr. 2021 | inconnu | inconnu | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) sur BSC, lancé en avr. 2021 ; volume record de 4,3 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/moonmoon/ |
| 1575 | Mouch | à vérifier | Monad | 2025 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 687 |
| 1576 | Moyaki | à vérifier | Monad | 2025 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 688 |
| 1577 | Muncat | MUNCAT | Tron | 2024-2025 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 692 |
| 1578 | Nano Doge Token | NANODOGE | BSC | juil. 2021 | inconnu | inconnu | mort | Clone de Dogecoin sur BSC, lancé en juil. 2021 ; volume record de 5,7 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/nano-doge-token/ |
| 1579 | Nano Dogecoin | NDC | BNB Chain | août 2021 (ajout CMC) | inconnu (classé par CMC du 15 août 2021 au 9 janv. 2022, sans capitalisation publiée) | inconnu | mort | « Nano » Doge de l'été 2021, un des clones Doge à frais de transaction redistribués ; disparu en janv. 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/nano-dogecoin/ |
| 1580 | NOEAR | NOEAR | NEAR | à vérifier | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 806 |
| 1581 | Nostalgia | NOS | Solana | Préventes, mars 2024 | inconnu (≈ 6,7 M$ à l'époque) | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 698 |
| 1582 | Olen Mosk | à vérifier | Solana | Noms mal orthographiés, mars 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 700 |
| 1583 | Oxbt | OXBT | Bitcoin (BRC-20) | 2023-2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 702 |
| 1584 | Pepe 3.0 | PEPE3.0 | Ethereum | 21/08/2023 | inconnu | inconnu | mort | Tentative de prolonger Pepe 2.0, plusieurs copies concurrentes, toutes mortes. | commune | commune |  | à définir | r3 ; https://dexscreener.com/ethereum/0x310cca5009EaE9194985C830B4Eb83d36f9790A1 |
| 1585 | Pepe Inu | PEPEINU | Ethereum | 15/09/2023 | inconnu | inconnu | mort | Croisement Pepe × Inu de septembre 2023, quasi sans valeur aujourd'hui. | commune | commune |  | à définir | r3 ; https://dexscreener.com/ethereum/0xD69c5b95f07277947dE1cDE2f9F5cE1f385Fa47E |
| 1586 | Pepe on Monad | à vérifier | Monad | 2025 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 706 |
| 1587 | Pepe Ordinals | PEPE | Bitcoin (BRC-20) | 2023 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 707 |
| 1588 | Pepoclown | HONK | Ethereum | 01/06/2024 | inconnu | inconnu | mort | Pepe en clown (« honk honk ») de la vague Pepe de 2024, sans volume aujourd'hui. | commune | commune |  | à définir | r3 ; https://dexscreener.com/ethereum/0xD8E8438CF7bEEd13cFABC82F300Fb6573962c9e3 |
| 1589 | Poodlana | à vérifier | Solana | 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 718 |
| 1590 | Prodeum | PRO | Ethereum (ERC-20) | janv. 2018 | inconnu (levée de 43 ETH selon une enquête, chiffres de 11 $ à 970 ETH dans la presse) | inconnu | mort | ICO de « blockchain pour fruits et légumes » au faux fondateur ; fin janvier 2018, l'équipe disparaît et remplace son site par un seul mot, « penis » : symbole de la bulle des ICO. | commune | épique | arnaque avérée | à définir | r1 ; https://thenextweb.com/news/cryptocurrency-prodeum-scam-exit-penis ; https://medium.com/@baltic.fund/prodeum-scam-traces-are-linked-to-other-fraud-projects-and-have-nothing-to-do-with-lithuania-9fe11cf7ceea |
| 1591 | Proof of Weak Hands (PoWH 3D) | P3D | Ethereum | janv. 2018 | inconnu (contrat proche de 1 M$ selon une source) | inconnu | mort | Pyramide assumée née sur /biz/ (4chan) ; le premier contrat PoWH est vidé de 866 ETH par une faille début 2018, puis PoWH3D et Fomo3D saturent Ethereum à l'été 2018. | commune | rare | arnaque avérée | à définir | r1 ; https://medium.com/@ebanisadr/how-800k-evaporated-from-the-powh-coin-ponzi-scheme-overnight-1b025c33b530 ; https://news.bitcoin.com/46-million-of-ether-is-locked-in-a-pair-of-ponzi-dapps/ |
| 1592 | Punch | PUNCH | Solana | 2026 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 721 |
| 1593 | PUP | PUP | BNB Chain | 02/10/2025 | inconnu (≈ 7 M$ encore en avr. 2026) | inconnu | en déclin (≈ 0,19 M$) | Mème chien de la saison d'octobre, +200 % dès ses premières heures (BingX). | commune | commune |  | à définir | r3 ; https://bingx.com/en/learn/article/bnb-meme-season-key-metrics-and-what-you-need-to-know ; https://dexscreener.com/bsc/0x73b84F7E3901F39FC29F3704a03126D317Ab4444 |
| 1594 | Raptor Jesus | RAPTOR | Ethereum | 02/12/2023 | inconnu | inconnu | mort | Vieux mème Internet du raptor crucifié recyclé en jeton fin 2023. | commune | commune |  | à définir | r3 ; https://dexscreener.com/ethereum/0x45b5eF98d8035Ac4BA22f605386e0C3BFD57bac9 |
| 1595 | Rats † | RATS | Bitcoin (BRC-20) | 2023 | inconnu | inconnu | à vérifier (homonyme sur CoinGecko, non rapproché) |  | commune | commune |  | à définir | v1 n° 725 |
| 1596 | RED | RED | Solana | Préventes, mars 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 727 |
| 1597 | Rici Elon | RICI | BSC | nov. 2021 | inconnu | inconnu | mort | Mème Elon Musk sur BSC, lancé en nov. 2021 ; volume record de 1,1 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune | personne réelle | à définir | r2 ; https://coinmarketcap.com/currencies/rici-elon/ |
| 1598 | Roar | ROAR | Solana (à vérifier) | mai 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 732 |
| 1599 | Safe Star | SAFESTAR | BSC | mars 2021 | inconnu | inconnu | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) sur BSC, lancé en mars 2021 ; volume record de 6,3 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/safe-star/ |
| 1600 | SafeGalaxy | SAFEGALAXY | BSC | mars 2021 | inconnu | inconnu | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) sur BSC, lancé en mars 2021 ; volume record de 1,5 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/safegalaxy/ |
| 1601 | SAFEPLUTO69 | SAFEPLUTO | BSC | mai 2021 | inconnu | inconnu | mort | Fork « reflection » de SafeMoon (taxe reversée aux détenteurs) sur BSC, lancé en mai 2021 ; volume record de 11,2 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/safepluto69/ |
| 1602 | Saitama Inu † | SAITAMA | Ethereum | 2021 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 735 |
| 1603 | Sanshu Inu | SANSHU | Ethereum | avr. 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sans prévente sur Ethereum, lancé en avr. 2021 ; volume record de 7,2 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/sanshu-inu/ |
| 1604 | Santa Floki | HOHOHO | BSC | nov. 2021 | inconnu | inconnu | mort | Jeton né du chien Floki d'Elon Musk (tweet du 25/06/2021) sur BSC, lancé en nov. 2021 ; volume record de 10,8 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/santa-floki/ |
| 1605 | Save The Kids | KIDS | BSC | juin 2021 | inconnu | inconnu | mort | Jeton « caritatif » promu par des membres de FaZe Clan (juin 2021) : FaZe Kay revend presque tout en 24 h, -90 % en trois jours ; enquête de Coffeezilla, Kay exclu de FaZe. | commune | épique | arnaque avérée | à définir | r2 ; https://decrypt.co/75094/esports-team-faze-clan-punishes-players-crypto-scam ; https://protos.com/save-the-kids-faze-clan-kay-coffeezilla-proves-rug-pulls |
| 1606 | SEPPUKU•IN•MAY•AND•GO•AWAY | SEPPUKU | Bitcoin (Runes) | mai 2024 | inconnu | inconnu | actif |  | commune | commune |  | à définir | v1 n° 739 ; CG `seppuku` |
| 1607 | Sexyy Red | PRESI | Solana | juin 2024 | inconnu | inconnu | à vérifier | Jeton de la rappeuse dont 90 % de l'offre est raflée par des snipers au lancement. | commune | commune | personne réelle | à définir | r3 ; https://www.blocmates.com/articles/an-analysis-of-solanas-celebrity-memecoin-invasion |
| 1608 | Shib2.0 | SHIB2.0 | Ethereum | 06/07/2023 | inconnu | inconnu | mort | Une des copies « Shib 2.0 » de la mode des 2.0 (plusieurs contrats existent). | commune | commune |  | à définir | r3 ; https://dexscreener.com/ethereum/0xdfEf6416EA3e6Ce587ED42Aa7cb2E586362cbBFa ; https://decrypt.co/147889/pepe-leads-meme-coin-losses-fresh-token-launches-grab-traders-attention |
| 1609 | Shiba 2.0 | SHIBA 2.0 | Ethereum | 06/07/2023 | inconnu | inconnu | mort | Autre « Shiba 2.0 » lancé le même jour, liquidité presque vide. | commune | commune |  | à définir | r3 ; https://dexscreener.com/ethereum/0xBE77212A6c7f55567470c2C95AFf7B0B0E0C3Ef5 |
| 1610 | Shiba Lite | SHIBLITE | BNB Chain | nov. 2021 (ajout CMC) | inconnu (classé par CMC du 7 nov. 2021 au 3 mars 2024, sans capitalisation publiée) | inconnu | mort | Shiba « allégé » de nov. 2021 ; resté au classement jusqu'en 2024 sans volume. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/shiba-lite/ |
| 1611 | Shiba Monk | SHIBAMONK | BSC | nov. 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en nov. 2021 ; volume record de 2,5 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/shiba-monk/ |
| 1612 | SHIBA2K22 | SHIBA22 | BSC | janv. 2022 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en janv. 2022 ; volume record de 3,0 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/shiba2k22/ |
| 1613 | ShibaCash | SHIBACASH | BNB Chain | mai 2021 (ajout CMC) | inconnu (classé par CMC du 23 mai 2021 au 14 nov. 2021, sans capitalisation publiée) | inconnu | mort | Un des innombrables dérivés « Shiba » de mai 2021 sur BSC, né dans l'élan de SHIB ; disparu en nov. 2021. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/shibacash/ |
| 1614 | ShibaCorgi | SHICO | BSC | mai 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en mai 2021 ; aujourd'hui -100,00 %. | commune | commune |  | à définir | r2 ; https://cointelegraph.com/magazine/all-hail-the-shiba-rise-of-dogecoin-pretenders-fueled-by-meme-frenzy ; https://coinmarketcap.com/currencies/shibacorgi/ |
| 1615 | Shibanomics | SHIBIN | BSC | oct. 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en oct. 2021 ; volume record de 3,1 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/shibanomics/ |
| 1616 | ShibX | ShibX | BSC | oct. 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en oct. 2021 ; volume record de 3,7 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/shibx/ |
| 1617 | Sincere Doge | SDOGE | BSC | févr. 2022 | inconnu | inconnu | mort | Clone de Dogecoin sur BSC, lancé en févr. 2022 ; volume record de 15,3 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/sincere-doge/ |
| 1618 | Skibidi | à vérifier | Solana (à confirmer) | Brainrot, 2025-2026 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 747 |
| 1619 | SMLE | SMLE | Solana | Préventes, mars 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 749 |
| 1620 | Smog | SMOG | Solana (et Ethereum) | 2024 | inconnu | inconnu | mort |  | commune | commune |  | à définir | v1 n° 750 ; CG `smog` |
| 1621 | SolanaDoge | à vérifier | Solana | 2021 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 755 |
| 1622 | Solciety | à vérifier | Solana | 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 756 |
| 1623 | Son of Shib | SON | BNB Chain | nov. 2021 (ajout CMC) | inconnu (classé par CMC du 14 nov. 2021 au 16 oct. 2022, sans capitalisation publiée) | inconnu | mort | « Fils de Shib », dérivé BSC de nov. 2021, en plein pic de SHIB ; disparu fin 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/sonofshib/ |
| 1624 | SpaceCorgi | SCORGI | BNB Chain | mai 2021 (ajout CMC) | inconnu (classé par CMC du 30 mai 2021 au 19 sept. 2021, sans capitalisation publiée) | inconnu | mort | Corgi spatial de mai 2021, saison SafeMoon ; disparu en sept. 2021. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/spacecorgi/ |
| 1625 | Spooky Shiba | SpookyShiba | BSC | nov. 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en nov. 2021 ; volume record de 3,1 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/spooky-shiba/ |
| 1626 | Squid Pet | SQUIDPET | BSC | nov. 2021 | inconnu | inconnu | mort | Jeton de la vague Squid Game (automne 2021) sur BSC, lancé en nov. 2021 ; volume record de 4,0 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/squid-pet/ |
| 1627 | Squidanomics | SQUID | BSC | oct. 2021 | inconnu | inconnu | mort | Copie du jeton SQUID sur BSC, tombée le même jour que l'original selon CoinDesk (01/11/2021) ; plus coté. | commune | commune |  | à définir | r2 ; https://www.coindesk.com/markets/2021/11/01/squid-game-token-crashes-developers-say-theyve-left-the-project/ ; https://coinmarketcap.com/currencies/squidanomics/ |
| 1628 | Suijak | SUIJAK | Sui | sept. 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 761 |
| 1629 | Surge Inu | SURGE | BSC | oct. 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur BSC, lancé en oct. 2021 ; volume record de 3,4 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/surge-inu/ |
| 1630 | Tamadoge † | TAMA | Ethereum | 2022 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 765 |
| 1631 | Tata | TATA | Solana | janv. 2026 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 767 |
| 1632 | TikTok Memes | TIKTOK | Solana | TikTok | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 769 |
| 1633 | TJR | TJR | Solana | 2026 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 770 |
| 1634 | TOP G | TOPG | Solana | 7 juin 2024 | inconnu | inconnu | mort (≈ 62 k$, volume nul) | Autre jeton d'Andrew Tate en juin 2024, effondré comme les autres. | commune | commune | personne réelle | à définir | r3 ; https://cointelegraph.com/news/andrew-tate-endorsed-memecoins-crashed-zero ; https://dexscreener.com/solana/8qs2ye9viad5qemvq7mwbqvcxnjwecmkodzg6cvtanxp |
| 1635 | Tsuzuki Inu | TZKI | Ethereum | oct. 2021 | inconnu | inconnu | mort | Clone de Shiba Inu (jeton « Inu ») sur Ethereum, lancé en oct. 2021 ; volume record de 11,0 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/tsuzuki-inu/ |
| 1636 | TurtSat | TURT | Bitcoin (BRC-20) | 2023-2024 | inconnu (≈ 0,5 M$, sans date) | inconnu | à vérifier (homonyme sur CoinGecko, non rapproché) |  | commune | commune |  | à définir | v1 n° 777 |
| 1637 | Twerk Finance | TWERK | BSC | mai 2021 | inconnu | inconnu | mort | Mème « twerk » sur BSC, lancé en mai 2021 ; volume record de 1,4 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/twerk-finance/ |
| 1638 | Uncle Doge | UDOGE | BSC | juil. 2021 | inconnu | inconnu | mort | Clone de Dogecoin sur BSC, lancé en juil. 2021 ; volume record de 3,2 M$ sur une journée (CMC) ; aujourd'hui plus coté. | commune | commune |  | à définir | r2 ; https://coinmarketcap.com/currencies/uncle-doge/ |
| 1639 | UNIMOON | UNIMOON | BNB Chain | nov. 2021 (ajout CMC) | inconnu (classé par CMC du 14 nov. 2021 au 6 févr. 2022, sans capitalisation publiée) | inconnu | mort | Licorne-lune de nov. 2021 sur BSC, clone moonshot ; sorti en févr. 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/unimoon/ |
| 1640 | URF | URF | Solana | mars 2024 | inconnu (prévente de ~2 400 SOL, ~450 k$) | inconnu | mort | Prévente promue par l'influenceur Bryce Hall ; l'équipe part avec ~450 k$ de SOL moins de 24 h après le lancement (ZachXBT). | commune | commune | arnaque avérée, personne réelle | à définir | r3 ; https://crypto.news/solana-meme-token-rug-pull-urf/ |
| 1641 | Watcoin | WAT | blockchain propre (X11) | janv. 2014 | inconnu | inconnu | mort | Coin du mème de la vieille dame « WAT » (« In WAT we trust »), repris par sa communauté puis oublié. | commune | commune |  | à définir | r1 ; https://www.coindesk.com/world-cup-startcoin-crowdfunding-vertcoin-stealth-move/ ; https://www.coindesk.com/strangest-altcoins-2014/ |
| 1642 | Whale Fall | Whale | BNB Chain | juin 2021 (ajout CMC) | inconnu (classé par CMC du 4 juil. 2021 au 23 janv. 2022, sans capitalisation publiée) | inconnu | mort | Mème « chute de baleine » de l'été 2021 sur BSC, jeton reflection éphémère ; plus coté après janv. 2022. | commune | commune |  | à définir | r4 ; https://coinmarketcap.com/currencies/whale-fall/ |
| 1643 | WhitePepe | WHITEPEPE | Solana | janv. 2026 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 789 |
| 1644 | Wojak Finance | WOJ | à vérifier | 2024 (à vérifier) | inconnu (≈ 39,3 M$, mars 2026) | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 793 |
| 1645 | Yellow Ket | KET | Avalanche | 2025 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° 797 |
| 1646 | 川普 (四川普通话) | 川普 | BNB Chain | 10/01/2026 | inconnu (≈ 2 M$ le 12/01/2026) | inconnu | mort (≈ 20 k$) | Abréviation de « mandarin du Sichuan », qui s'écrit aussi comme « Trump » en chinois ; poussé par des traders, sans suite. | commune | commune |  | à définir | r3 ; https://www.panewslab.com/zh/articles/b77d5603-6827-44b6-b75b-de051186d2c3 ; https://dexscreener.com/bsc/0x6fafec4730e0102d8ac82b00de460b9f31f44444 |

## À décider (hors total)

Lignes « À décider » de v1 encore valides, jetons mis en doute par les chercheurs, candidats C1 de nature douteuse. Le porteur tranche. Une mention ici ne vaut pas accusation.

| N° | Nom | Ticker | Chaîne | Lancement | Pic | Nature du pic | État | Histoire | Rareté | Rareté proposée | Drapeau | Burn | Source  Motif |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AD1 | Official Trump | TRUMP | Solana | 2025 | ≈ 14,60 Md$ (corrigé) | sourcé | en déclin (-95 % ou pire) |  | légendaire | légendaire | politique | à définir | v1 n° D1 ; CG `official-trump` | Très forte chute, procès évoqués ; président en exercice représenté sur une carte. Pas d'arnaque établie |
| AD2 | SafeMoon | SFM (ex-SAFEMOON) | BNB Chain | 2021 | ≈ 6,00 Md$ (sourcé) | sourcé | mort |  | légendaire | légendaire | arnaque avérée | à définir | v1 n° D2 ; CG `safemoon-2` | Ancien PDG condamné à 100 mois de prison pour fraude (arnaque avérée) |
| AD3 | Libra | LIBRA | Solana | 2025 | ≈ 4,40 Md$ (sourcé) | sourcé | mort |  | légendaire | légendaire |  | à définir | v1 n° D3 ; correction r3 ; CG `libra-5` | Pertes massives et retraits documentés ; affaire classée en Argentine. Ne pas écrire « arnaque » |
| AD4 | Verge (ex-DogeCoinDark) | XVG | blockchain propre | oct. 2014 | ≈ 3,69 Md$, 24/12/2017 (CMC, relevé hebdomadaire) | sourcé | en déclin | Né en 2014 sous le nom DogeCoinDark, clone « sombre » de Doge, renommé Verge en 2016 ; tweet de John McAfee le 13/12/2017, pic à ≈ 3,7 Md$ fin décembre, puis -99 %. Origine mème, devenu « privacy coin » : à trancher. | légendaire | légendaire |  | à définir | r1 ; https://coinmarketcap.com/historical/20171224/ ; https://en.wikipedia.org/wiki/Verge_(cryptocurrency) | doute du chercheur (r1) : « à trancher » |
| AD5 | YZY | YZY | Solana | 2025 | ≈ 3,00 Md$ (sourcé) | sourcé | en déclin |  | légendaire | légendaire |  | à définir | v1 n° D4 ; CG `yzy` | Environ 52 000 portefeuilles en perte selon Bubblemaps ; offre aux mains d'initiés |
| AD6 | Melania Meme | MELANIA | Solana | 2025 | ≈ 2,00 Md$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | légendaire | légendaire | politique | à définir | v1 n° D6 ; CG `melania-meme` | Action collective visant des intermédiaires ; Melania Trump n'est pas mise en cause |
| AD7 | Squid Game | SQUID | BNB Chain | 2021 | ≈ 201 M$ (estimé CG) | estimé | mort | SQUID : x 80 000 en une semaine puis rug, épisode culte | légendaire | légendaire | arnaque avérée | à définir | v1 n° D10 ; CG `squid-game` | Arnaque avérée : créateurs partis avec environ 3,4 M$, faux lien avec Netflix |
| AD8 | MAGA | TRUMP (ERC-20) | Ethereum | 2023 † | ≈ 788 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | épique | épique | politique | à définir | v1 n° D65 ; CG `maga` | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 106) |
| AD9 | Akuma Inu | AKUMA | Base | déc. 2024 (ajout CMC) | ≈ 783 M$ (12 janv. 2025) ; CMC, relevé hebdomadaire (pic CMC douteux) | estimé | mort | Akuma Inu (« démon »), Base, déc. 2024 : CMC lui a affiché ≈ 780 M$ le 12 janv. 2025 (CoinGecko ≈ 900 M$ estimé), puis -99,99 % ; pic probablement artificiel, à vérifier. | épique | épique |  | à définir | r4 ; https://coinmarketcap.com/currencies/akuma-inu/ ; https://www.coingecko.com/en/coins/akuma-inu | r4 : capitalisation CMC probablement fondée sur une offre mal déclarée ; pic traité comme estimé |
| AD10 | Central African Republic Meme | CAR | à vérifier | févr. 2025 | ≈ 770 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | rare | politique | à définir | v1 n° D69 ; CG `central-african-republic-meme` | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 578) |
| AD11 | Jeo Boden | BODEN | Solana | 2024 | ≈ 654 M$ en FDV (10 avr. 2024) | estimé | mort |  | épique | épique | politique | à définir | v1 n° D73 ; correction r3 ; CG `jeo-boden` ; https://coinmarketcap.com/currencies/jeo-boden/ | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 648) |
| AD12 | America Party | AMERICA | à vérifier | juil. 2025 | ≈ 643 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique | politique | à définir | v1 n° D64 ; CG `america-party-5` | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 41) |
| AD13 | Hawk Tuah | HAWK | Solana | 2024 | ≈ 500 M$ (sourcé) | sourcé | mort |  | épique | épique | personne réelle | à définir | v1 n° D7 ; correction r3 ; CG `hawk-tuah` | Effondrement de plus de 90 %, action collective contre des partenaires de lancement |
| AD14 | Hatom | HTM | à vérifier | à vérifier (sommet le 2023-12-09) | ≈ 357 M$, 2023-12-09 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | épique | épique |  | à définir | R5 C1 `hatom` ; https://www.coingecko.com/en/coins/hatom | consolidation : protocole DeFi (MultiversX), pas un mème ? |
| AD15 | Ducky | DUCKY | BNB Chain | nov. 2024 (ajout CMC) | ≈ 341 M$ (10 mai 2026) ; CMC, relevé hebdomadaire (pic CMC douteux) | estimé | mort | Canard BSC listé fin 2024, porté à ≈ 340 M$ par CMC en mai 2026, puis -99 % ; chiffre CMC à vérifier. | épique | épique |  | à définir | r4 ; https://coinmarketcap.com/currencies/ducky/ ; https://www.coingecko.com/en/coins/ducky-2 | r4 : capitalisation CMC probablement fondée sur une offre mal déclarée ; pic traité comme estimé |
| AD16 | MAGA Hat | MAGA | à vérifier | 2024 † | ≈ 305 M$ (estimé CG) | estimé | mort |  | épique | rare | politique | à définir | v1 n° D75 ; CG `maga-hat` | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 666) |
| AD17 | AhaToken | AHT | à vérifier | à vérifier (sommet le 2021-04-02) | ≈ 284 M$, 2021-04-02 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | épique | épique |  | à définir | R5 C1 `ahatoken` ; https://www.coingecko.com/en/coins/ahatoken | consolidation : jeton utilitaire, pas un mème ? |
| AD18 | Retardio † | RETARDIO | Solana | 2024 | ≈ 242 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | rare | obscène | à définir | v1 n° D53 ; CG `retardio` | Nom insultant (signalé par catalogue.md) |
| AD19 | Aavegotchi | GHST | à vérifier | à vérifier (sommet le 2024-04-01) | ≈ 192 M$, 2024-04-01 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | épique | épique |  | à définir | R5 C1 `aavegotchi` ; https://www.coingecko.com/en/coins/aavegotchi | consolidation : jeu NFT / DeFi, pas un mème ? |
| AD20 | M3M3 | M3M3 | Solana | Fin 2024 | ≈ 187 M$ (estimé CG) | estimé | mort |  | épique | rare |  | à définir | v1 n° D50 ; CG `m3m3` | Allégations, sans condamnation trouvée : ne pas écrire « arnaque » sur une carte |
| AD21 | TrumpCoin | DJT | à vérifier | juin 2024 | ≈ 183 M$ (estimé CG) | estimé | mort (absent de CoinGecko) |  | épique | commune | politique | à définir | v1 n° D59 ; v1 n° D41 ; CG `trumpcoin` | Doute : même ticker et même mois que DJT ⚠ (rug pull rapporté) ; identité non établie |
| AD22 | Daddy Tate | DADDY | Solana | 2024 | ≈ 173 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | épique | personne réelle | à définir | v1 n° D40 ; CG `daddy-tate` | Accusations de manipulation ; image d'Andrew Tate |
| AD23 | HempCoin | THC | blockchain propre | juin 2014 | ≈ 160,8 M$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin cannabis de 2014 resté à quelques dizaines de k$ jusqu'en 2017, porté à ≈ 160 M$ en janvier 2018 par la vague « weed coins », puis -99,9 %. | épique | épique |  | à définir | r1 ; https://coinmarketcap.com/historical/20180107/ ; https://cryptoslate.com/coins/hempcoin/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD24 | Doland Tremp | TREMP | Solana | 2024 | ≈ 137 M$ (5 juin 2024) | sourcé | mort |  | épique | épique | politique | à définir | v1 n° D70 ; correction r3 ; CG `donald-tremp` ; https://coinmarketcap.com/currencies/doland-tremp/ | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 609) |
| AD25 | Butthole Coin | BUTTHOLE | Solana | à vérifier | ≈ 133 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | épique | rare | obscène | à définir | v1 n° D35 ; CG `butthole-coin` | Nom obscène ou sexuel |
| AD26 | MimboGameGroup | MGG | à vérifier | à vérifier (sommet le 2026-04-01) | ≈ 131 M$, 2026-04-01 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | épique | épique |  | à définir | R5 C1 `mimbogamegroup` ; https://www.coingecko.com/en/coins/mimbogamegroup | R5 C1 : nature à vérifier |
| AD27 | Normie | NORMIE | Base | 2024 | ≈ 130 M$ (sourcé) | sourcé | en déclin (-95 % ou pire) |  | épique | épique |  | à définir | v1 n° D8 ; CG `normie-6` | Pas une arnaque : faille exploitée le 26 mai 2024, détenteurs ruinés |
| AD28 | Bald | BALD | Base | 2023 | ≈ 100 M$ (sourcé) | sourcé | en déclin |  | épique | épique |  | à définir | v1 n° D11 ; CG `bald` | Retrait de liquidité documenté, perte de plus de 90 % ; le développeur conteste le terme de rug pull |
| AD29 | Boner Coin | BONER | à vérifier | sept. 2026 | ≈ 82 M$ (estimé CG) | estimé | en déclin |  | rare | rare | obscène | à définir | v1 n° D12 ; CG `boner-coin` | Nom obscène |
| AD30 | Trust | TRUST | Solana | Fin 2024 | ≈ 73 M$ (estimé CG) | estimé | en déclin |  | rare | rare |  | à définir | v1 n° D60 ; CG `trust-3` | Allégations, sans condamnation trouvée : ne pas écrire « arnaque » sur une carte |
| AD31 | Carrot by Puffer | CARROT | à vérifier | à vérifier (sommet le 2025-01-31) | ≈ 66 M$, 2025-01-31 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `carrot-by-puffer` ; https://www.coingecko.com/en/coins/carrot-by-puffer | consolidation : jeton DeFi (Puffer), pas un mème ? |
| AD32 | 我踏马来了 | 我踏马来了 | BNB Chain | janv. 2026 | ≈ 62 M$ (02/02/2026, ATH CMC × 1 Md ; PANews : ≈ 52 M$ début janv.) | estimé | en déclin (≈ 7,8 M$), -87 % → rare |  | rare | rare | obscène | à définir | v1 n° D63 ; correction r3 ; CG `wo-ta-ma-laile` ; https://coinmarketcap.com/currencies/wotamalaile/ | Nom familier et grossier en chinois |
| AD33 | Private Aviation Finance Token | CINO | à vérifier | à vérifier (sommet le 2025-08-13) | ≈ 53 M$, 2025-08-13 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `private-aviation-finance-token` ; https://www.coingecko.com/en/coins/private-aviation-finance-token | R5 C1 : nature à vérifier |
| AD34 | FTMTOKEN | FTMX | à vérifier | à vérifier (sommet le 2025-09-25) | ≈ 49 M$, 2025-09-25 (CoinGecko, ATH × offre actuelle) | estimé | en déclin (-95 % ou pire, CoinGecko 11/11) |  | rare | rare |  | à définir | R5 C1 `ftmtoken` ; https://www.coingecko.com/en/coins/ftmtoken | consolidation : jeton utilitaire, pas un mème ? |
| AD35 | Hawk | HAWK | à vérifier | janv. 2025 | ≈ 49 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare | personne réelle | à définir | v1 n° D16 ; CG `hawk-2` | Doute : même ticker et nom proche de Hawk Tuah ⚠ ; identité non établie |
| AD36 | Chudjak | CHUD | à vérifier | 2024 (à vérifier) | ≈ 32 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare | obscène | à définir | v1 n° D36 ; CG `chudjak` | Précaution : « chud » est une insulte de forums extrémistes ; non marqué ⚠ par la source |
| AD37 | Testicle | TESTICLE | Solana | à vérifier | ≈ 23 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) |  | rare | rare | obscène | à définir | v1 n° D57 ; CG `testicle` | Nom obscène ou sexuel |
| AD38 | Chonketha the Wet Beaver | CHONKETHA | à vérifier | août 2026 | ≈ 12 M$ (estimé CG) | estimé | en déclin |  | rare | rare | obscène | à définir | v1 n° D23 ; CG `chonketha-the-wet-beaver` | Nom à double sens sexuel |
| AD39 | Hunter Biden's Laptop | LAPTOP | à vérifier | sept. 2026 | ≈ 34,13 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) |  | commune | rare | politique | à définir | v1 n° D71 ; CG `hunter-biden-s-laptop-3` | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 643) |
| AD40 | ShibaBitcoin | SHIBTC | BNB Chain | avr. 2024 (ajout CMC) | ≈ 1,02 Md$ (9 févr. 2025) ; CMC, relevé hebdomadaire (pic CMC douteux) — estimation aberrante, à vérifier | estimé | mort | ShibaBitcoin (SHIBTC) : CMC lui a affiché ≈ 1 Md$ de capitalisation en févr. 2025 avec une FDV de 125 Md$, chiffres très douteux (offre auto-déclarée) ; le jeton est ensuite sorti du classement. | commune | rare |  | à définir | r4 ; https://coinmarketcap.com/currencies/shibabitcoin/ ; https://coinmarketcap.com/historical/20250209/ | r4 : capitalisation CMC ≈ 1 Md$ « très douteuse » (offre auto-déclarée) ; pic traité comme estimé |
| AD41 | Skibidi Toilet | SKBDI | Solana | déc. 2023 | ≈ 77 M$ (date inconnue) | estimé | mort (≈ 0,21 M$) | Le mème TikTok de la génération Alpha, monté vers 77 M$ puis délaissé. | commune | rare |  | à définir | r3 ; https://www.coingecko.com/en/coins/skibidi-toilet-2 ; https://dexscreener.com/solana/bnkdvqkwr7dwx9zmpcqtgcptfkm7wzp2ydzre218nrtv | r3 : peut-être la carte v1 n° 747 « Skibidi » (homonyme à vérifier) |
| AD42 | ArAIstotle | FACY | à vérifier | à vérifier (sommet le 2025-10-05) | ≈ 73 M$, 2025-10-05 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `araistotle` ; https://www.coingecko.com/en/coins/araistotle | consolidation : agent IA présenté comme produit ? |
| AD43 | Mates | MATES | Solana | 2024-2025 | ≈ 72 M$ (estimé CG) | estimé | mort |  | commune | commune |  | à définir | v1 n° D51 ; CG `mates` | Allégations, sans condamnation trouvée : ne pas écrire « arnaque » sur une carte |
| AD44 | Gooncoin | GOONC | Solana | Believe, mai 2025 | ≈ 68 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort |  | commune | rare | obscène | à définir | v1 n° D14 ; CG `gooncoin` | Nom obscène |
| AD45 | Super Trump | STRUMP | à vérifier | 2024 † | ≈ 68 M$ (estimé CG) | estimé | mort |  | commune | commune | politique | à définir | v1 n° D76 ; CG `super-trump` | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 763) |
| AD46 | Pussy Financial | PUSSY | à vérifier | oct. 2021 | ≈ 65 M$ (estimé CG) | estimé | mort |  | commune | rare | obscène | à définir | v1 n° D13 ; CG `pussy-financial` | Nom obscène |
| AD47 | RTR | RTR | Solana | Août 2024 | ≈ 45 M$ (estimé CG) | estimé | mort |  | commune | commune | politique | à définir | v1 n° D55 ; CG `restore-the-republic` | Chute de 95 %, faux lien avec les Trump |
| AD48 | Jenner | JENNER | Solana | 2024 | ≈ 44 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare | personne réelle | à définir | v1 n° D15 ; correction r3 ; https://decrypt.co/298703/scene-2024-story-of-the-year-celebrity-meme-coins | Effondrement et accusations relayés par la presse |
| AD49 | Opus Genesis | OPUS | à vérifier | à vérifier (sommet le 2024-11-28) | ≈ 42 M$, 2024-11-28 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `opus-2` ; https://www.coingecko.com/en/coins/opus-2 | consolidation : agent IA présenté comme produit ? |
| AD50 | AGENDA 47 | A47 | à vérifier | mars 2025 | ≈ 41 M$ (estimé CG) | estimé | mort |  | commune | rare | politique | à définir | v1 n° D66 ; CG `agenda-47` | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 285) |
| AD51 | Wolf | WOLF | Solana | mars 2025 | ≈ 40 M$ (sourcé) | sourcé | mort (≈ 0,53 M$ deux jours après le lancement du 08/03/2025) |  | commune | rare |  | à définir | v1 n° D17 ; correction r3 ; CG `wolf-2` ; https://www.theblock.co/post/346504/libra-token-facilitator-hayden-davis-connected-to-40-million-crash-of-wolf-memecoin-bubblemaps | Lien avec Hayden Davis établi par Bubblemaps, chute de 99 %, sans décision de justice |
| AD52 | Whoren | WHOREN | Solana | PolitiFi, 2024 | ≈ 38 M$ (estimé CG) | estimé | mort |  | commune | commune | obscène | à définir | v1 n° D62 ; CG `elizabath-whoren` | Nom injurieux |
| AD53 | Jason Derulo | JASON | Solana | 2024 | ≈ 35,6 M$ (estimé : -97,8 % jusqu'à 783 k$) | estimé | mort |  | commune | rare | personne réelle | à définir | v1 n° D48 ; correction r3 ; CG `jason-derulo` ; https://decrypt.co/298703/scene-2024-story-of-the-year-celebrity-meme-coins | Effondrement et accusations relayés par la presse |
| AD54 | GrokCoin | GROKCOIN | Solana | Mars 2025 | ≈ 34 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° D18 | Manipulation soupçonnée |
| AD55 | Ben Coin (BitBoy) | BEN | Ethereum (à vérifier) | mai-juin 2023 | ≈ 30 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare | personne réelle | à définir | v1 n° D19 | Qualifié de rug pull par David Schwartz ; BitBoy accusé d'avoir revendu |
| AD56 | DopeCoin | DOPE | blockchain propre | févr. 2014 | ≈ 27,2 M$, 31/12/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Coin « dope » (cannabis) de février 2014 ; endormi des années, pic à ≈ 27 M$ fin décembre 2017, puis plus de capitalisation suivie. | commune | rare |  | à définir | r1 ; https://coinmarketcap.com/historical/20171231/ ; https://coinmarketcap.com/currencies/dopecoin/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD57 | SroomAI DAO | SHR0 | à vérifier | à vérifier (sommet le 2025-05-22) | ≈ 27 M$, 2025-05-22 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `sroomai-dao` ; https://www.coingecko.com/en/coins/sroomai-dao | R5 C1 : nature à vérifier |
| AD58 | CannabisCoin | CANN | blockchain propre | août 2014 | ≈ 26,9 M$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin cannabis de 2014 ; ≈ 5 M$ en oct. 2014, ≈ 27 M$ en janv. 2018, puis -98 %. | commune | rare |  | à définir | r1 ; https://coinmarketcap.com/historical/20180107/ ; https://coinmarketcap.com/currencies/cannabiscoin/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD59 | Kamala Horris † | KAMA | Solana | 2024 | ≈ 26 M$ (26 juil. 2024, jour du lancement) | sourcé | mort |  | commune | rare | politique | à définir | v1 n° D74 ; correction r3 ; CG `kamala-horris` ; https://coinmarketcap.com/currencies/kamala-horris/ | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 651) |
| AD60 | Odin Liquidity Network | ODIN | à vérifier | à vérifier (sommet le 2024-12-03) | ≈ 24 M$, 2024-12-03 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `valhalla-index` ; https://www.coingecko.com/en/coins/valhalla-index | R5 C1 : nature à vérifier |
| AD61 | uP Token | UP | à vérifier | à vérifier (sommet le 2023-12-01) | ≈ 24 M$, 2023-12-01 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `up-token-2` ; https://www.coingecko.com/en/coins/up-token-2 | consolidation : jeton utilitaire, pas un mème ? |
| AD62 | Hulk Hogan | HULK | Solana | Célébrités, juin 2024 | ≈ 19 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare | personne réelle | à définir | v1 n° D20 ; correction r3 ; https://dailycoin.com/hulk-hogan-memecoin-wipes-17m/ | Pump-and-dump rapporté |
| AD63 | Hoodrat | HOODRAT | à vérifier | juil. 2026 | ≈ 17 M$ (estimé CG) | estimé | mort |  | commune | rare | obscène | à définir | v1 n° D21 ; CG `hoodrat-4` | Nom à connotation raciste et sexiste |
| AD64 | Danold Tromp | DANOLD | Solana | Noms mal orthographiés, mars 2024 | ≈ 15 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare | politique | à définir | v1 n° D67 | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 377) |
| AD65 | TabbyPOS | TABBY | à vérifier | à vérifier (sommet le 2023-10-04) | ≈ 15 M$, 2023-10-04 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `tabbypos` ; https://www.coingecko.com/en/coins/tabbypos | consolidation : jeton de paiement, pas un mème ? |
| AD66 | PutinCoin | PUT | PutinCoin (blockchain propre) | début 2018 | ≈ 12,1 M$, 08/01/2018 (confirme la rareté rare plutôt que commune) | sourcé | mort (absent de CoinGecko) |  | commune | rare | politique | à définir | v1 n° D68 ; correction r1 ; https://coinmarketcap.com/currencies/putincoin/historical-data/ | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 405) |
| AD67 | Red Kitten Crew | RKC | à vérifier | mai 2026 | ≈ 12 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare |  | à définir | v1 n° D26 ; v1 n° D24 ; CG `red-kitten-crew` | Doute : même ticker, même année et ordre de grandeur que RKC ⚠ ; identité non établie |
| AD68 | COQ AI | COQAI | à vérifier | à vérifier (sommet le 2025-01-11) | ≈ 11 M$, 2025-01-11 (CoinGecko, ATH × offre actuelle) | estimé | mort |  | commune | rare |  | à définir | R5 C1 `coq-ai` ; https://www.coingecko.com/en/coins/coq-ai | R5 C1 : nature à vérifier |
| AD69 | Wanko | WANKO | Bitcoin (Runes) | 2024 | ≈ 10 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | rare | obscène | à définir | v1 n° D25 | Nom obscène (WANKO•MANKO•RUNES) |
| AD70 | Fapcoin | FAPCOIN | à vérifier | déc. 2025 | ≈ 7,9 M$ (estimé CG) | estimé | en déclin |  | commune | commune | obscène | à définir | v1 n° D27 ; CG `fapcoin-4` | Nom obscène |
| AD71 | CockCardano | COCK | à vérifier | janv. 2025 | ≈ 7,4 M$ (estimé CG) | estimé | mort |  | commune | commune | obscène | à définir | v1 n° D28 ; CG `cockcardano` | Nom obscène |
| AD72 | TrumpCoin † | TRUMP | TrumpCoin (blockchain propre) | 2016 | ≈ 4,8 M$, 06/01/2018 (5,3 M$ au relevé hebdomadaire du 07/01/2018) | sourcé | mort |  | commune | rare | politique | à définir | v1 n° D77 ; correction r1 ; CG `trumpcoin` ; https://coinmarketcap.com/currencies/trumpcoin/historical-data/ | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 775) |
| AD73 | Hunter Boden | HUNTER | à vérifier | juin 2024 | ≈ 4,5 M$ (estimé CG) | estimé | mort |  | commune | commune | politique | à définir | v1 n° D72 ; CG `hunter-boden` | Jeton politique (personnalité ou campagne) : même règle que Official Trump et Melania (ex-carte n° 644) |
| AD74 | Groyper | GROYP | à vérifier | août 2026 | ≈ 4,1 M$ (estimé CG) | estimé | actif |  | commune | commune | obscène | à définir | v1 n° D29 ; CG `groyper-3` | Référence à un mouvement d'extrême droite raciste |
| AD75 | GanjaCoin | MRJA | blockchain propre | nov. 2014 | ≈ 3,1 M$, 04/03/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin cannabis ; ≈ 3,1 M$ en mars 2018, plus coté après mai 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180304/ ; https://coinmarketcap.com/currencies/ganjacoin/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD76 | LeafCoin | LEAF | blockchain propre | févr. 2014 | ≈ 2,4 M$, 04/03/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Clone scrypt à feuille de cannabis de la vague 2014 ; ≈ 1,4 M$ en févr. 2014, ≈ 2,4 M$ en mars 2018, puis retrait. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180304/ ; https://coinmarketcap.com/currencies/leafcoin/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD77 | CannaCoin | CCN | blockchain propre | avr. 2014 | ≈ 2,2 M$, 31/12/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Coin cannabis de 2014 ; ≈ 2,2 M$ fin 2017, -97 % ensuite. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20171231/ ; https://coinmarketcap.com/currencies/cannacoin/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD78 | MechaHitler | MECHAHITLER | Solana | Juillet 2025 | ≈ 2,2 M$ (sourcé) | sourcé | mort (absent de CoinGecko) |  | commune | commune | obscène | à définir | v1 n° D30 | Référence nazie, à écarter |
| AD79 | KushCoin | KUSH | blockchain propre | févr. 2017 | ≈ 1,7 M$, 14/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin cannabis ; ≈ 1,7 M$ en janv. 2018, retiré de CMC fin 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180114/ ; https://coinmarketcap.com/currencies/kushcoin/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD80 | HempCoin (HMP) | HMP | blockchain propre | févr. 2016 | ≈ 1,1 M$, 03/04/2016 (CMC, relevé hebdomadaire) | sourcé | mort | Second « HempCoin », homonyme de THC ; ≈ 1,1 M$ en avril 2016, retiré en 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20160403/ ; https://coinmarketcap.com/currencies/hempcoin-hmp/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD81 | Sativacoin | STV | blockchain propre | oct. 2014 | ≈ 781 k$, 17/12/2017 (CMC, relevé hebdomadaire) | sourcé | mort | Coin cannabis ; ≈ 0,78 M$ en déc. 2017, retiré fin 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20171217/ ; https://coinmarketcap.com/currencies/sativacoin/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD82 | Marijuanacoin | MAR | blockchain propre | févr. 2017 | ≈ 729 k$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | Coin cannabis ; ≈ 0,73 M$ en janv. 2018, -99 % fin 2018. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20180107/ ; https://coinmarketcap.com/currencies/marijuanacoin/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD83 | Darkkush | DANK | blockchain propre | nov. 2014 | ≈ 22 k$, 02/11/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Coin cannabis « dark » (ticker DANK) ; ≈ 22 k$ en nov. 2014, retiré en févr. 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20141102/ ; https://coinmarketcap.com/currencies/darkkush/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD84 | CannabisDarkcoin | CND | blockchain propre | oct. 2014 | ≈ 19 k$, 26/10/2014 (CMC, relevé hebdomadaire) | sourcé | mort | Croisement des vagues cannabis et « dark » ; ≈ 19 k$ en oct. 2014, retiré en 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20141026/ ; https://coinmarketcap.com/currencies/cannabisdarkcoin/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD85 | WeedTokens | WETK | blockchain propre | févr. 2015 | ≈ 19 k$, 12/04/2015 (CMC, relevé hebdomadaire) | sourcé | mort | Coin cannabis ; ≈ 19 k$ en avril 2015, retiré en juin 2015. | commune | commune |  | à définir | r1 ; https://coinmarketcap.com/historical/20150412/ ; https://coinmarketcap.com/currencies/weedtokens/ | coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher » |
| AD86 | AIAI | AIAI | Solana | Fin 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° D31 | Allégations, sans condamnation trouvée : ne pas écrire « arnaque » sur une carte |
| AD87 | Barron | BARRON | Solana | 2025 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune | arnaque avérée | à définir | v1 n° D32 | Faux compte |
| AD88 | Beratardio | à vérifier | Berachain | 2025 | inconnu (≈ 6 800 $, sans date) | inconnu | mort (absent de CoinGecko) |  | commune | commune | obscène | à définir | v1 n° D33 | Nom dérivé d'une insulte |
| AD89 | Coinye | COINYE | Coinye (fork de Litecoin) | 2014 | inconnu | inconnu | mort (absent de CoinGecko) | Coinye : premier rug et procès de Kanye West (2014) | commune | épique |  | à définir | v1 n° D9 | Présenté comme la première rug pull ; plainte pour contrefaçon de marque |
| AD90 | CR7 | CR7 | Solana (à confirmer) | 2025 | inconnu (143 M$ selon un résumé, mais le titre de CoinGape parle d'un pic à 5 M$ après un rug pull de 143 M$) | inconnu | mort (absent de CoinGecko) |  | commune | commune | arnaque avérée | à définir | v1 n° D37 | Faux jeton, chute de 98 % |
| AD91 | Doja | DOJA | Solana | Juin 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune | personne réelle | à définir | v1 n° D42 | Compte de Doja Cat piraté |
| AD92 | Elon Sperm | à vérifier | à vérifier | 2021-2022 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune | obscène | à définir | v1 n° D43 | Nom obscène ou sexuel |
| AD93 | Enron | ENRON | Solana | Fin 2024 - 2025 | inconnu (jeton attribué à Kelsier par des sources, sans jugement) | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° D44 | Jeton attribué à Kelsier par des enquêtes de presse, sans jugement |
| AD94 | EthereumMax | EMAX | Ethereum (à vérifier) | 2021 | inconnu (chute de plus de 99 %) | inconnu | mort |  | commune | commune | personne réelle | à définir | v1 n° D45 ; CG `ethereummax` | Kim Kardashian sanctionnée par la SEC pour promotion non déclarée |
| AD95 | Funky | FUNKY | Solana | 2025 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune | arnaque avérée | à définir | v1 n° D46 | Rug pull, Ben Askren |
| AD96 | Hood | HOOD | Solana | Fin 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune |  | à définir | v1 n° D47 | Allégations, sans condamnation trouvée : ne pas écrire « arnaque » sur une carte |
| AD97 | Jeton « Epstein » de McAfee | WHACKD | à vérifier | 2019 (à vérifier) | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune | personne réelle | à définir | v1 n° D49 | Référence à une affaire criminelle réelle |
| AD98 | Mbappé | MBAPPE | Solana | 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune | arnaque avérée | à définir | v1 n° D52 | Faux jeton, victime à 1 M$ |
| AD99 | Rich the Kid | RICH | Solana | Célébrités, 2024 | inconnu (≈ 61 000 $ après plus de 90 % de baisse) | inconnu | mort (absent de CoinGecko) |  | commune | commune | personne réelle | à définir | v1 n° D54 | Piratage et pump-and-dump allégués ; chute de plus de 90 % |
| AD100 | Sydney Sweeney | SWEENEY | Solana | Juillet 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune | personne réelle | à définir | v1 n° D56 | Compte piraté |
| AD101 | Vantard | VANTARD | Solana | Novembre 2024 | inconnu | inconnu | mort (absent de CoinGecko) |  | commune | commune | obscène | à définir | v1 n° D61 | Précaution : suffixe proche de l'insulte de Retardio et Beratardio ; non marqué ⚠ par la source |

## Décompte (catalogue, hors « À décider »)

### Par rareté

| Valeur | Cartes |
|---|---|
| mythique | 3 |
| légendaire | 21 |
| épique | 235 |
| rare | 230 |
| commune | 1160 |
| **Total** | **1649** |

### Par chaîne (première chaîne citée)

| Valeur | Cartes |
|---|---|
| à vérifier | 613 |
| BNB Chain | 236 |
| Solana | 199 |
| Ethereum | 133 |
| blockchain propre | 113 |
| Base | 75 |
| TON | 31 |
| Sui | 29 |
| Bitcoin | 26 |
| Avalanche | 23 |
| Tron | 17 |
| Arbitrum | 11 |
| NEAR | 11 |
| Monad | 11 |
| Hyperliquid | 10 |
| Cronos | 8 |
| Cardano | 7 |
| Kaspa | 7 |
| Polygon | 6 |
| Aptos | 5 |
| Zksync Era | 5 |
| Fantom | 5 |
| scellé (mythique) | 3 |
| Linea | 3 |
| Xrp Ledger | 3 |
| Dogechain | 3 |
| Berachain | 3 |
| Pulsechain | 3 |
| Abstract | 3 |
| Ink | 3 |
| Mantle | 2 |
| Blast | 2 |
| Counterparty (Bitcoin) | 2 |
| Sei | 2 |
| Optimism | 2 |
| Multiversx | 2 |
| Sonic | 2 |
| Hedera | 2 |
| Flare | 2 |
| Internet Computer | 2 |
| Xdc Network | 2 |
| Robinhood Chain | 1 |
| Stacks | 1 |
| Wax | 1 |
| Heco | 1 |
| Merlin Chain | 1 |
| Core | 1 |
| Chihuahua | 1 |
| Injective | 1 |
| Beam | 1 |
| Apechain | 1 |
| Moonbeam | 1 |
| X Layer | 1 |
| Chiliz | 1 |
| World Chain | 1 |
| Stellar | 1 |
| Kaia | 1 |
| Starknet | 1 |
| Chia | 1 |
| Algorand | 1 |
| Osmosis | 1 |
| Radix | 1 |
| Polkadot | 1 |
| **Total** | **1649** |

### Par état

| Valeur | Cartes |
|---|---|
| mort | 1154 |
| en déclin (-95 % ou pire) | 232 |
| en déclin | 155 |
| actif | 94 |
| à vérifier | 11 |
| scellé (mythique) | 3 |
| **Total** | **1649** |

### Par drapeau

| Valeur | Cartes |
|---|---|
| (aucun) | 1531 |
| personne réelle | 59 |
| obscène | 33 |
| politique | 20 |
| arnaque avérée | 10 |
| (hors mythiques ; une carte peut avoir plusieurs drapeaux) | |

### Par époque de lancement

| Valeur | Cartes |
|---|---|
| 2013-2018 | 123 |
| 2019-2022 | 278 |
| 2023-2026 | 1218 |
| inconnue | 27 |
| scellé (mythique) | 3 |
| **Total** | **1649** |

### « À décider » par rareté

| Valeur | Cartes |
|---|---|
| légendaire | 7 |
| épique | 21 |
| rare | 10 |
| commune | 63 |
| **Total** | **101** |

## Annexe 1 : fusions et doublons

| Carte gardée | Absorbé | Ticker | Origine absorbée | Raison |
|---|---|---|---|---|
| 155 Pepecoin | Pepecoin † | MEME | v1 n° 709 | R5 : même chaîne Pepecoin de 2016 (`pepecoin-network`) |
| 518 Base God | Based Tyler † | TYBG | v1 n° 558 | R5 : même ticker TYBG, même chaîne Base, un seul jeton CoinGecko (`base-god`) |
| AD21 TrumpCoin | DJT | DJT | v1 n° D41 | R5 : CoinGecko ne connaît que `trumpcoin` (ticker DJT) |
| AD67 Red Kitten Crew | RKC | RKC | v1 n° D24 | R5 : CoinGecko ne connaît que `red-kitten-crew` (ticker RKC) |

**Lignes non reprises** (doublons d'une carte déjà présente ou retirée) :

| Nom | Ticker | Origine | Raison |
|---|---|---|---|
| Slerf [OLD] | SLERF | R5 C1 `slerf` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| Kekius Maximus | KEKIUS | R5 C1 `kekius-maximus` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| MOO DENG | MOODENG | R5 C1 `moo-deng-2` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| Sigma | SIGMA | R5 C1 `sigma` | C1 déjà présent (même id CoinGecko) |
| Torch of Liberty | LIBERTY | R5 C1 `torch-of-liberty` | C1 déjà présent (même id CoinGecko) |
| WUFFI | WUF | R5 C1 `wuffi` | C1 déjà venu par r4 |
| AEROBUD | AEROBUD | R5 C1 `aerobud` | C1 déjà présent (même id CoinGecko) |
| WAR [OLD] | WAR | R5 C1 `war` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| Wojak | WOJAK | R5 C1 `wojak-4` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| Frodo the Virtual Samurai | FROG | R5 C1 `frodo-the-virtual-samurai` | C1 déjà présent (même id CoinGecko) |
| America Party | AP | R5 C1 `america-party-4` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| Real Smurf Cat | SMURFCAT | R5 C1 `real-smurf-cat` | C1 déjà présent (même id CoinGecko) |
| Neiro | NEIRO | R5 C1 `neiro-2` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| 修仙 (XiuXian) | 修仙 | R5 C1 `xiuxian` | C1 déjà venu par r3 |
| PUP | PUP | R5 C1 `pup` | C1 déjà venu par r3 |
| alright buddy | BUDDY | R5 C1 `alright-buddy` | C1 déjà présent (même id CoinGecko) |
| Huhu Cat | HUHU | R5 C1 `huhu-cat` | C1 déjà présent (même id CoinGecko) |
| Dickbutt | DICKBUTT | R5 C1 `dickbutt` | C1 déjà présent (même id CoinGecko) |
| Mystery | MYSTERY | R5 C1 `mystery-2` | C1 déjà venu par r3 |
| flybrain | FLYBRAIN | R5 C1 `flybrain` | C1 déjà venu par r3 |
| Husky Avax | HUSKY | R5 C1 `husky-avax` | C1 déjà venu par r2 |
| Cocoro | COCORO | R5 C1 `cocoro-2` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| Smolcoin [OLD] | SMOL | R5 C1 `smolcoin` | C1 déjà venu par r4 |
| GOGGLES | GOGLZ | R5 C1 `googles` | C1 déjà présent (même id CoinGecko) |
| Noggles | NOGS | R5 C1 `noggles` | C1 déjà présent (même id CoinGecko) |
| RUSSELL | RUSSELL | R5 C1 `russell` | C1 déjà présent (même id CoinGecko) |
| Peepo | PEEPO | R5 C1 `peepo` | C1 déjà présent (même id CoinGecko) |
| Broccoli | BROCCOLI | R5 C1 `broccoli-4` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| 币安Holder | BNBHOLDER | R5 C1 `bian-holder` | C1 déjà venu par r3 |
| Success Kid | SKID | R5 C1 `success-kid` | C1 déjà venu par r3 |
| Landwolf | WOLF | R5 C1 `landwolf-eth` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| Base is for everyone | BASEISFOREVERYONE | R5 C1 `base-is-for-everyone` | C1 déjà présent (même id CoinGecko) |
| BabySNEK | BBSNEK | R5 C1 `babysnek` | C1 déjà présent (même id CoinGecko) |
| Pepa Inu | PEPA | R5 C1 `pepa-inu` | C1 déjà présent (même id CoinGecko) |
| Stonks | STONKS | R5 C1 `stonks-9` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| Kira the Injective Cat | KIRA | R5 C1 `kira-the-injective-cat` | C1 déjà présent (même id CoinGecko) |
| Bitcoin 2.0 | BTC2.0 | R5 C1 `bitcoin-2-0` | C1 déjà présent (même id CoinGecko) |
| Perry | PERRY | R5 C1 `perry` | C1 déjà présent (même id CoinGecko) |
| Young Peezy AKA Pepe | PEEZY | R5 C1 `young-peezy-aka-pepe` | C1 déjà présent (même id CoinGecko) |
| Groyper | GROYPER | R5 C1 `groyper` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| BOBER | BOBER | R5 C1 `bober` | C1 déjà présent (même id CoinGecko) |
| Dogecoin20 | DOGE20 | R5 C1 `dogecoin20` | C1 déjà présent (même id CoinGecko) |
| Baby Floki | BABYFLOKI | R5 C1 `baby-floki` | C1 déjà venu par r2 |
| Fofar | FOFAR | R5 C1 `fofar` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| GigaChad | GIGACHAD | R5 C1 `gigachad-eth` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| Whale | WHALE | R5 C1 `whale-2` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| DORK LORD (ETH) | DORKL | R5 C1 `dork-lord` | C1 déjà présent (même id CoinGecko) |
| What’s Updog? | UPDOG | R5 C1 `what-s-updog` | C1 déjà venu par r3 |
| Baby Shiba Inu | BABYSHIB | R5 C1 `baby-shiba-inu-erc` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| bonkwifhat | BIF | R5 C1 `bonkwifhat` | C1 déjà venu par r3 |
| Bonk On Base | BONK | R5 C1 `bonk-on-base` | C1 déjà présent (même id CoinGecko) |
| DOYR | DOYR | R5 C1 `doyr` | C1 déjà venu par r3 |
| Biaocoin | BIAO | R5 C1 `biaocoin` | C1 déjà venu par r4 |
| The Dons | DONS | R5 C1 `dons` | C1 déjà présent (même id CoinGecko) |
| Ucan fix life in1day | 1 | R5 C1 `ucan-fix-life-in1day` | C1 déjà venu par r3 |
| ArbiDoge | ADOGE | R5 C1 `arbidoge` | C1 déjà présent (même id CoinGecko) |
| BEAMCAT | BCAT | R5 C1 `beamcat` | C1 déjà présent (même id CoinGecko) |
| Paper Plane | PLANE | R5 C1 `paper-plane` | C1 déjà présent (même id CoinGecko) |
| DisclaimerCoin | DONT | R5 C1 `disclaimercoin` | C1 déjà venu par r3 |
| Mubarakah | MUBARAKAH | R5 C1 `mubarakah` | C1 déjà venu par r3 |
| SMOL | SMOL | R5 C1 `smolcoin-2` | C1 déjà venu par r4 |
| Wojak | WOJAK | R5 C1 `wojak-3` | C1 : « copie ou ancienne version d'une carte » selon R5 |
| Pepoclown | HONK | R5 C1 `pepoclown` | C1 déjà venu par r3 |

**Homonymes gardés distincts** (même nom normalisé, ticker différent) :

| Nouveau | Ticker | Carte existante | Ticker |
|---|---|---|---|
| 938 Jesus Coin (2017) | JC | 269 Jesus Coin | JESUS |
| AD80 HempCoin (HMP) | HMP | AD23 HempCoin | THC |
| 1425 Pandacoin (PANDA) | PANDA | 334 Pandacoin | PND |
| 1008 SquidGameToken | SGT | AD7 Squid Game | SQUID |
| 1048 Mars Inu | MARSINU | 230 Marscoin | MARSCOIN |
| 823 Bitcoin 2.0 | BTC2.0 | 579 Bitcoin20 | BTC20 |
| 1089 Peepo (2024) | PEPO | 772 Peepo | PEEPO |
| 1579 Nano Dogecoin | NDC | 1578 Nano Doge Token | NANODOGE |
| 1189 Sauce Inu | SAUCEINU | 1216 saucecoin | SAUCE |

2 homonymes d'une mythique scellée, non listés pour ne pas révéler son nom.

**Corrections non appliquées** :

| Source | N° | Champ | Raison |
|---|---|---|---|
| r1 | 709 (Pepecoin MEME, « Memetic ») | Pic ; rareté ; état | carte 709 fusionnée dans 99 (R5) : correction non reportée, à revoir |
| r1 | 603 (Dogeparty) | Pic | carte 603 retirée par R5 (non-mème) |
| r1 | 158 (PotCoin) | État | carte 158 retirée par R5 (non-mème) |
| r1 | D22 (SexCoin) | Pic ; rareté | carte D22 retirée par R5 (non-mème) |
| r1 | D58 (Titcoin) | Pic ; chaîne | carte D58 retirée par R5 (non-mème) |
| r3 | 720 | Pic | pic jugé très douteux par la source, non appliqué |
| r3 | 669 / 11 | Pic / rareté | carte 11 retirée par R5 (non-mème) |
| r3 | 665 | Pic / rareté | carte 665 retirée par R5 (non-mème) |
| r3 | 676 | Pic / rareté | carte 676 retirée par R5 (non-mème) |
| r3 | 9 | Rareté | carte 9 retirée par R5 (non-mème) |
| r3 | 35 | Rareté | carte 35 retirée par R5 (non-mème) |
| r3 | 36 | Rareté | carte 36 retirée par R5 (non-mème) |
| r3 | 45 | Rareté | carte 45 retirée par R5 (non-mème) |
| r3 | 59 | Rareté | carte 59 retirée par R5 (non-mème) |
| r3 | 63 | Rareté | carte 63 retirée par R5 (non-mème) |
| r3 | 69 | Rareté | carte 69 retirée par R5 (non-mème) |
| r3 | 82 | Rareté | carte 82 retirée par R5 (non-mème) |
| r3 | 117 | Rareté | carte 117 retirée par R5 (non-mème) |
| r3 | 118 | Rareté | carte 118 retirée par R5 (non-mème) |
| r3 | 131 | Rareté | carte 131 retirée par R5 (non-mème) |
| r3 | 161 | Rareté | carte 161 retirée par R5 (non-mème) |
| r3 | 163 | Rareté | carte 163 retirée par R5 (non-mème) |
| r3 | 180 | Rareté | carte 180 retirée par R5 (non-mème) |
| r3 | 224 | Rareté | carte 224 retirée par R5 (non-mème) |
| r3 | 282 | Rareté | carte 282 retirée par R5 (non-mème) |
| r4 | 117 | Pic | carte 117 retirée par R5 (non-mème) |
| r4 | D39 | Pic | carte D39 retirée par R5 (non-mème) |

## Annexe 2 : écarts entre rareté v2 et rareté proposée

568 écarts. « Proposée » = rareté de la dernière source (chercheur, correction ou audit R5).

| N° | Nom | Ticker | Pic retenu | Nature | État | Proposée | v2 | Raison |
|---|---|---|---|---|---|---|---|---|
| 16 | cat in a dogs world † | MEW | ≈ 1,15 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) | épique | légendaire | surclassement manuel : pic ≥ 1 Md$ largement rapporté |
| 23 | Baby Doge Coin | BABYDOGE | ≈ 1,20 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) | légendaire | épique | pic estimé ≥ 1 Md$ non confirmé : rareté de la borne sourcée (310 M$) |
| 40 | monKEYS | MONKEYS | ≈ 700 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 48 | Dora | DORA | ≈ 576 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 54 | Simon's Cat | CAT | ≈ 511 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 55 | Beercoin | BEER | ≈ 507 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 58 | Onyx Arches | OXA | ≈ 470 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 60 | Believe | BELIEVE | ≈ 457 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 79 | Hoge Finance | HOGE | ≈ 367 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 82 | Katana Inu | KATA | ≈ 359 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 86 | Barsik | BARSIK | ≈ 340 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 87 | Luckycoin | LKY | ≈ 338 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 91 | Osaka Protocol | OSAK | ≈ 332 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 93 | Luce † | LUCE | ≈ 319 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 97 | Baby Shark Universe | BSU | ≈ 304 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 98 | PepeCoin on Solana | PEPE | ≈ 297 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 106 | mfercoin | MFER | ≈ 264 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 115 | Shrub | SHRUB | ≈ 243 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 119 | Wise Monkey | MONKY | ≈ 232 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 120 | Aura | AURA | ≈ 231 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 124 | Billy † | BILLY | ≈ 228 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 125 | Shiba Predator | QOM | ≈ 228 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 126 | DogeGF | DOGEGF | ≈ 226 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 143 | Clifford Inu | CLIFF | ≈ 198 M$ en FDV (18/12/2021) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 144 | Conscious | CONSCIOUS | ≈ 198 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 148 | GreenHood | HOOD | ≈ 191 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 150 | MiniDOGE | MINIDOGE | ≈ 190 M$ en FDV (08/07/2021) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 153 | SATOSHI•NAKAMOTO | SATOSHI | ≈ 188 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 154 | 360noscope420blazeit | MLG | ≈ 187 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 157 | Happy | HAPPY | ≈ 186 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 161 | Marshall Rogan Inu | MRI | ≈ 185 M$ en FDV (04/03/2022) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 164 | Shiba Samurai | SHIBURAI | ≈ 184 M$ en FDV (02/02/2022) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 165 | NikolAI | NIKO | ≈ 181 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 170 | Shoggoth | SHOGGOTH | ≈ 173 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 175 | PeiPei | PEIPEI | ≈ 165 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 177 | Buff Doge Coin | DOGECOIN | ≈ 163 M$ en FDV (01/11/2021) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 179 | WHY | WHY | ≈ 161 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 193 | Husky | HUSKY | ≈ 150 M$ en FDV (10/05/2021) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 194 | Mongoose | MONGOOSE | ≈ 149 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 199 | Bongo | BONGO | ≈ 143 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 201 | Hoppy | HOPPY | ≈ 142 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| 213 | Star Wars Cat | SWCAT | ≤ 133 M$ en FDV (28 nov. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | commune | épique | pic 100 M$ - 1 Md$ |
| 215 | Hatch | HATCH | ≈ 132 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 216 | FarmerDoge | CROP | ≈ 131 M$ en FDV (19/11/2021) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 224 | BABY WHITE HAMSTER | BWH | ≤ 126 M$ en FDV (21 nov. 2021) ; CMC hebdomadaire, prix × offre totale, capitalisation non publiée | estimé | mort | commune | épique | pic 100 M$ - 1 Md$ |
| 225 | Kitty Inu | Kitty | ≈ 124 M$ en FDV (07/11/2021) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 240 | Higher † | HIGHER | ≈ 114 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 247 | AstroElon | ELONONE | ≈ 109 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 249 | Meme Kombat | MK | ≈ 108 M$ (09/03/2024) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| 256 | Moltbook | à vérifier | ≈ 100 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | commune | épique | pic 100 M$ - 1 Md$ |
| 257 | LOBO•THE•WOLF•PUP | LOBO | ≈ 3,59 Md$ (estimé CG, au-dessus de la borne sourcée) | estimé | en déclin (-95 % ou pire) | épique | rare | pic estimé ≥ 1 Md$ non confirmé : rareté de la borne sourcée (71 M$) |
| 378 | IKUN | IKUN | ≈ 32 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | commune | rare | pic 10 - 100 M$, pas mort |
| 478 | Baby Floki | BABYFLOKI | ≈ 11,9 M$ en FDV (01/11/2021) | estimé | en déclin | commune | rare | pic 10 - 100 M$, pas mort |
| 487 | ShibaDoge | SHIBDOGE | ≈ 12769,26 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 488 | BNB Tiger OG | BNBTIGEROG | ≈ 3351,98 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 489 | Pitbull | PIT | ≈ 5,81 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 490 | Anon Inu | AINU | ≈ 5,18 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | mort | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 491 | AI XOVIA | AIX | ≈ 4,50 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 492 | YooShi | YOOSHI | ≈ 4,19 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 493 | Pups † | PUPS | ≈ 3,87 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 494 | Pig Finance | PIG | ≈ 3,70 Md$ en FDV (10/05/2021) — estimation aberrante, à vérifier | estimé | mort | épique | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 495 | PEPPER | PEPPER | ≈ 2,56 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 496 | Capybara Nation | BARA | ≈ 2,21 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 497 | Rosa Inu | ROSA | ≈ 2,20 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 498 | Kishu Inu | KISHU | ≈ 1,69 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | épique | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 499 | CorgiAI | CORGIAI | ≈ 1,53 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | épique | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 500 | Bezoge Earth | BEZOGE | ≈ 1,52 Md$ en FDV (22/11/2021) — estimation aberrante, à vérifier | estimé | mort | épique | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 501 | Ape and Pepe | APEPE | ≈ 1,45 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin | épique | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 502 | catwifhat | CWIF | ≈ 1,4 Md$ (estimation CoinGecko de l'annexe 3) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | légendaire | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 503 | Samoyedcoin † | SAMO | ≈ 1,36 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 504 | Solid X | SOLIDX | ≈ 1,14 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 505 | OSK | OSK | ≈ 1,05 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | épique | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| 507 | catwifbag | BAG | ≈ 99 M$ (25 mars 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 508 | Doge Token | DOGET | ≈ 98,5 M$ (09/05/2021) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 509 | Shibnobi | SHINJA | ≈ 98,1 M$ (21/11/2021) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 510 | BUBCAT | BUB | ≈ 92 M$ (8 déc. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 511 | Rizzmas | RIZZMAS | ≈ 91 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 512 | MEMDEX100 | MEMDEX | ≈ 90 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 513 | Sponge | SPONGE | ≈ 90 M$ (08/05/2023) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 515 | Banano † | BAN | ≈ 88 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 517 | SHKOOBY INU | SHKOOBY | ≈ 87,1 M$ en FDV (07/11/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 518 | Base God | TYBG | ≈ 86 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 521 | Doge Eat Doge | OMNOM | ≈ 85 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle (CMC ne publie qu'à partir de plus tard : ≈ 31 M$ le 10 nov. 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 522 | Gen Z Quant | QUANT | ≈ 85 M$ (20 nov. 2024) | sourcé | mort (≈ 0,11 M$) | épique | commune | mort au pic < 100 M$ |
| 523 | Rare Pepe Cash † | PEPECASH | ≈ 84 M$, 07/01/2018 | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 524 | Scrat | SCRAT | ≈ 84 M$ (25 juin 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 525 | SHIBA BSC | SHIBSC | ≈ 84 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 526 | DogeVerse | DOGEVERSE | ≈ 83 M$ (08/06/2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 527 | POOH | POOH | ≈ 82 M$, 2023-05-06 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 528 | Pepe on SOL | PEPE | ≈ 81 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 529 | Dolos The Bully | BULLY | ≈ 80 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 530 | Luminous | LUM | ≈ 80 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 532 | Ansem's Cat | HOBBES | ≈ 79 M$ (3 avr. 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 533 | Costco Hot Dog | COST | ≈ 79 M$ (10 avr. 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 534 | Ping | PING | ≈ 79 M$, 2025-10-25 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 535 | Catana | CATANA | ≈ 78 M$ (date inconnue) | estimé | mort (≈ 61 k$, volume nul) | rare | commune | mort au pic < 100 M$ |
| 536 | GOUT | GOUT | ≈ 77 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 537 | FedoraCoin | TIPS | ≈ 76,7 M$, 07/12/2017 (CMC, relevé quotidien) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 538 | Hosico Cat | HOSICO | ≈ 75 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 539 | SafeMoon Inu | SMI | ≈ 73 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 540 | AEROBUD | AEROBUD | ~72,9 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 541 | Forgive Me Father | PURGE | ≈ 71 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 542 | Sillynubcat | NUB | ≈ 71 M$ (24 avr. 2024) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 543 | Snowdog | SDOG | ≈ 70,9 M$ en FDV (21/11/2021) | estimé | mort | épique | commune | mort au pic < 100 M$ |
| 544 | Ani | ANI | ≈ 70 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 545 | Moutai | MOUTAI | ≈ 70 M$ (14 avr. 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 546 | Wakanda Inu | WKD | ≈ 69,0 M$ en FDV (11/11/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 547 | Nailong | NAILONG | ≈ 68 M$ (≈ 16 nov. 2024) | estimé | mort (≈ 0,12 M$) | rare | commune | mort au pic < 100 M$ |
| 548 | Goku | GOKU | ≈ 67,6 M$ en FDV (02/11/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 549 | Donkey (DONKEY_BSC_MEME) | DONKEY | ≈ 67 M$ (24 août 2025) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 551 | DUKO | DUKO | ≈ 66 M$ (24 mars 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 552 | EvilSquidGame | EVILSQUID | ≈ 66,0 M$ en FDV (20/11/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 553 | ROCKY | ROCKY | ~64,2 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 554 | Anita Max Wynn | WYNN | ≈ 64 M$ (21 janv. 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 555 | Guacamole | GUAC | ≈ 64 M$, 2024-03-08 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 558 | BabyCake | BC2.1 | ≈ 62,8 M$ en FDV (22/07/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 559 | Anon | ANON | ≈ 62 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 560 | Dupe | DUPE | ≈ 62 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 561 | Bonk On Base | BONK | ~61,3 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 562 | Spore | SPORE | ≈ 61 M$ (avr. 2021) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 563 | Luigi Mangione | LUIGI | ≈ 60-77 M$ (10 déc. 2024) | sourcé | mort (≈ 0,23 M$) | rare | commune | mort au pic < 100 M$ |
| 564 | SAD HAMSTER | HAMMY | ≈ 60 M$ (17 mai 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 565 | Shikoku | SHIK | ≈ 59 M$, 2023-01-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 566 | Tiger King | TKING | ≈ 59 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 567 | Zelda Inu | ZLDA | ≈ 58,4 M$ en FDV (10/01/2022) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 568 | Basenji | BENJI | ≈ 57 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 570 | Boomer | BOOMER | ~56,6 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 571 | Gui Inu | GUI | ≈ 56,3 M$ (mars 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 572 | DYZilla | DYZILLA | ≈ 55 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 573 | Habibi (Sol) | HABIBI | ≈ 55 M$ (22 mai 2024) | estimé | mort (≈ 54 k$) | rare | commune | mort au pic < 100 M$ |
| 574 | Lets Go Brandon | LETSGO | ≈ 55 M$, 2022-03-02 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 575 | SEIYAN | SEIYAN | ≈ 55 M$ (janv. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 577 | Sharpei | SHAR | ≈ 54 M$ (23 oct. 2024) | sourcé | mort (absent de DexScreener) | rare | commune | mort au pic < 100 M$ |
| 578 | Moonshot | MSHOT | ≈ 53,6 M$ en FDV (12/05/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 579 | Bitcoin20 | BTC20 | ≈ 53 M$ (16/08/2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 581 | Andy BSC | ANDY | ≈ 52 M$ (26 janv. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 582 | Kasper | KASPER | ≈ 52 M$ (oct. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 583 | 財務自由 (Liberté financière) | 財務自由 | ≈ 52 M$ (09/10/2025) | estimé | mort (≈ 66 k$) | rare | commune | mort au pic < 100 M$ |
| 584 | SpaceGrime | GRIMEX | ≈ 51,5 M$ en FDV (30/10/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 585 | Ski Mask Cat | SKICAT | ~51,1 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 586 | Any Inu | AI | ≈ 51 M$, 2024-03-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 587 | The Next 100x Memecoin on Base | TN100X | ~50,6 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 588 | Hina Inu | HINA | ≈ 50,3 M$ en FDV (23/10/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 589 | AVAX Lambo | LAMBO | ≈ 50 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 590 | Kimbo | KIMBO | ≈ 50 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 591 | Shina Inu | SHI | ≈ 50 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 592 | TON FISH MEMECOIN | FISH | ≈ 50 M$, 2024-03-17 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 594 | Shakita Inu | SHAK | ≈ 49,7 M$ en FDV (29/10/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 595 | Shiba Floki Inu | FLOKI | ≈ 49,5 M$ en FDV (06/10/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 597 | Trog | TROG | ≈ 49 M$, 2024-06-05 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 598 | Pissing Cat | PEECAT | ≈ 48,8 M$ en FDV (24/07/2022) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 599 | Apetos | APE | ≈ 48,1 M$ (oct. 2024) ; ATH CoinGecko × offre totale | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 600 | AVAX Has No Chill | NOCHILL | ≈ 48 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 601 | Bagwork | BAGWORK | ≈ 48 M$ (date inconnue) | estimé | mort (≈ 82 k$) | rare | commune | mort au pic < 100 M$ |
| 602 | Chickencoin | CHKN | ≈ 48 M$, 2024-04-02 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 603 | GoldenBoys | GOLD | ≈ 48 M$, 2024-07-28 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 604 | Terminus | TERMINUS | ≈ 48 M$, 2024-09-23 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 605 | The Balkan Dwarf | KEKEC | ≈ 48 M$, 2024-11-06 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 606 | UWON | UWON | ≈ 48 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 607 | Boop | BOOP | ≈ 47 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 608 | Flybrain | FLYBRAIN | ≈ 47 M$ (11/09/2026) | estimé | mort (≈ 0,2 M$) | rare | commune | mort au pic < 100 M$ |
| 610 | Andy † | ANDY | ≈ 46 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 611 | KANGO | KANGO | ≈ 46 M$ (nov. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 612 | NumberGoUpTech | TECH | ≈ 46 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 613 | Brett (ETH) | BRETT | ≈ 45 M$, 2024-09-26 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 614 | Pepe 2.0 | PEPE2.0 | ≈ 45 M$ (sourcé) | sourcé | mort (≈ 0,26 M$, -99,8 %) | épique | commune | mort au pic < 100 M$ |
| 616 | WAR | WAR | ≈ 45 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 617 | Bubb | BUBB | ≈ 44 M$ (21/03/2025) | estimé | mort (≈ 30 k$) | rare | commune | mort au pic < 100 M$ |
| 618 | 修仙 (Xiuxian) | 修仙 | ≈ 44 M$ (10/10/2025) | estimé | mort (≈ 0,5 M$) | rare | commune | mort au pic < 100 M$ |
| 619 | Tardi | TARDI | ≈ 43,6 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 620 | Shiba Inu Mother | SHIBM | ≈ 43,1 M$ en FDV (04/03/2022) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 621 | Bitcoin Wizards | WZRD | ≈ 43 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 622 | Bob (Monad) | BOB | ≈ 43 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 623 | FourCoin | FOUR | ≈ 43 M$, 2023-05-09 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 624 | Shiryo Inu | SHIRYO | ≈ 43,0 M$ (20/01/2022) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 625 | LabraCoin | LABRA | ≈ 42,9 M$ en FDV (18/05/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 626 | Ponyo Inu | PONYO | ≈ 42,8 M$ en FDV (09/11/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 627 | Invest Zone | IVFUN | ≈ 42,6 M$ (août 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 628 | Simmi Token | SIMMI | ≈ 42 M$, 2024-12-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 629 | Waffles | WAFFLES | ≈ 42 M$, 2024-06-07 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 630 | 人生K线 (« K-line de la vie ») | à vérifier | ≈ 42 M$ début janv. 2026 (PANews), ATH CMC × 1 Md ≈ 28 M$ le 10/01/2026 | estimé | mort (≈ 0,5 M$, -98 %) | rare | commune | mort au pic < 100 M$ |
| 631 | Captain Inu | CPTINU | ≈ 41,1 M$ en FDV (18/12/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 633 | Dog Wif Nunchucks | NINJA | ≈ 41 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 634 | DOGE-1 Satellite | DOGE-1 | ≈ 41 M$, 2025-09-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 636 | Fair and Free | FAIR3 | ≈ 41 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 638 | Swasticoin | YZY | ≈ 41 M$, 2025-03-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 639 | 114514 | 114514 | ≈ 40 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 640 | BIBI | BIBI | ≈ 40 M$, 2024-03-06 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 641 | Catcoin | CAT | ≈ 40 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 642 | CatSlap | SLAP | ≈ 40 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 643 | Clawd | CLAWD | ≈ 40 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 644 | FourBook | FB | ≈ 40 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 646 | Roaring Kitty | KITTY | ≈ 40 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 647 | Tralalero Tralala | à vérifier | ≈ 40 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 649 | WEWECOIN (ex-Upside Down Meme) | WEWE | ~39,7 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 653 | FUD the Pug † | FUD | ≈ 39 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 654 | Hehe | HEHE | ≈ 39 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 655 | Honk | HONK | ≈ 39 M$, 2024-03-09 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 656 | MOAI | MOAI | ≈ 39 M$, 2024-11-05 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 657 | NPC On Solana | NPCS | ≈ 39 M$, 2024-10-17 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 658 | Priceless | PRICELESS | ≈ 39 M$ (08/10/2025) | estimé | mort (≈ 0,16 M$) | rare | commune | mort au pic < 100 M$ |
| 659 | Real Smurf Cat (шайлушай) | SMURFCAT | ≈ 39 M$ (27/10/2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 660 | STAN | STAN | ≈ 39 M$, 2024-05-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 662 | AU79 | AU79 | ≈ 38 M$, 2025-09-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 663 | MAGIC•INTERNET•MONEY | MIM | ≈ 38 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 664 | TAO INU | TAONU | ≈ 38 M$, 2024-03-17 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 665 | τDoge | TDOGE | ≈ 38 M$, 2021-06-03 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 666 | Crash On Base | CRASH | ≈ 37 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 667 | Poodl | POODL | ≈ 37,0 M$ en FDV (20/04/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 668 | Real Nigger Tate | RNT | ≈ 37 M$ (9 juin 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 669 | San Chan | SAN | ≈ 37 M$, 2025-02-02 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 671 | Ainu | AINU | ≈ 36 M$, 2021-10-17 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 672 | FRIC | FRIC | ≈ 36 M$, 2024-12-10 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 673 | CatGPT | CATGPT | ≈ 35 M$, 2024-04-25 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 674 | Dotcom | Y2K | ≈ 35 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 675 | N3on | N3ON | ≈ 35 M$, 2025-11-12 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 676 | What IF | IF | ≈ 35 M$, 2026-08-02 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 677 | Shar Pei | SHARPEI | ≈ 34,4 M$ en FDV (07/11/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 678 | alright buddy | BUDDY | ≈ 34,1 M$ (mai 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 679 | Zoro Inu | ZORO | ≈ 34,1 M$ en FDV (25/03/2022) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 680 | Cardi B (Wet Ass P***y) | WAP | ≈ 34-40 M$ (oct. 2024) | sourcé | mort (≈ 23 k$) | rare | commune | mort au pic < 100 M$ |
| 681 | Degen Zoo | DZOO | ≈ 34 M$, 2023-03-16 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 682 | Dust | DUST | ≈ 34 M$ (08/10/2025) | estimé | mort (≈ 0,17 M$) | rare | commune | mort au pic < 100 M$ |
| 683 | FU coin | FU | ≈ 34 M$ (9 févr. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 684 | Huhu Cat | HUHU | ≈ 34 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 685 | Shifu | SHIFU | ≈ 34 M$, 2024-12-20 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 686 | Justice For Ross | ROSS | ≈ 33-40 M$ (21 janv. 2025) | sourcé | mort (≈ 1,4 k$) | rare | commune | mort au pic < 100 M$ |
| 688 | 吉祥马 | 吉祥马 | ≈ 33 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 689 | DisclaimerCoin | DONT | ≈ 32-37 M$ (22/01/2026) | estimé | mort (≈ 0,4-0,6 M$) | rare | commune | mort au pic < 100 M$ |
| 690 | FINE | FINE | ≈ 32 M$, 2023-09-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 693 | Kaspy | KASPY | ≈ 32 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 694 | McPepe's | PEPES | ≈ 32 M$, 2024-04-28 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 695 | Spinning Cat | OIIAOIIA | ≈ 32 M$, 2025-01-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 696 | uPX | UPX | ≈ 32 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 697 | Genshin Floki Inu | GFloki | ≈ 31,7 M$ en FDV (21/11/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 698 | A Gently Used 2001 Honda Civic | USEDCAR | ≈ 31 M$ (30 déc. 2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 699 | Daku V2 | DAKU | ≈ 31 M$, 2025-10-05 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 700 | Goldn | GOLDN | ≈ 31 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 701 | HAMI | HAMI | ≈ 31 M$, 2024-03-29 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 702 | TANUKI•WISDOM | TANUKI | ≈ 31 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 704 | LEO | LEO | ≈ 30 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 705 | Lion Cat | LCAT | ≈ 30 M$ (9 mars 2025) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 706 | Luna Inu | LINU | ≈ 30 M$, 2024-03-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 707 | MoonRise | MOONRISE | ≈ 30,0 M$ en FDV (10/07/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 708 | Safetesla | SAFETESLA | ≈ 30,0 M$ en FDV (24/04/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 709 | SaylorMoon | SMOON | ≈ 30,0 M$ en FDV (06/06/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 710 | Tbull | TBULL | ≈ 30 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 711 | Toby ToadGod | TOBY | ≈ 30 M$, 2024-04-10 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 712 | WifeDoge | WIFEDOGE | ≈ 29,3 M$ en FDV (19/09/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 713 | Aqua Goat | AQUAGOAT | ≈ 29 M$, 2021-10-10 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 715 | Generational Wealth | GEN | ≈ 29 M$, 2023-05-18 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 717 | Pikachu Inu | PIKACHU | ≈ 28,3 M$ en FDV (28/10/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 720 | ElonRWA | ELONRWA | ≈ 28 M$, 2024-11-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 721 | Ghiblification | GHIBLI | ≈ 28 M$ (mars 2025) ; ≈ 41 M$ selon l'ATH CoinGecko | sourcé | mort (≈ 80 k$) | rare | commune | mort au pic < 100 M$ |
| 722 | JustAnEgg | EGG | ≈ 28 M$, 2024-04-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 723 | Milady Wif Hat | LADYF | ≈ 28 M$, 2024-05-22 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 724 | Zeek Coin | MEOW | ≈ 28 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 725 | 屎壳郎 (Dung Beetle) | 屎壳郎 | ≈ 28 M$, 2026-07-09 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 726 | Husky Avax | HUSKY | ≈ 27,9 M$ en FDV (28/10/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 727 | Chuck | CHUCK | ~27,3 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 728 | Business Coin | BUSINESS | ≈ 27 M$, 2025-01-31 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 729 | Cheese | CHEESE | ≈ 27 M$, 2024-11-20 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 730 | SHIBAAI | SHIBAAI | ≈ 27 M$, 2024-03-06 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 731 | WASSIE | WASSIE | ≈ 27 M$, 2024-03-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 732 | WORLD CUP INU | WCI | ≈ 26,8 M$ en FDV (05/11/2022) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 733 | 🟥🟪🟦🟩🟨🟧 | 🟥🟩 | ≈ 26 M$, 2024-11-19 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 735 | Gochujangcoin | GOCHU | ≈ 26 M$ (18 mai 2025) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 736 | HeeeHeee | HEEHEE | ≈ 26 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 738 | Manifest | MANIFEST | ≈ 26 M$, 2024-11-10 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 739 | Mubarakah | MUBARAKAH | ≈ 26 M$ (18/03/2025) | estimé | mort (≈ 0,4 M$) | rare | commune | mort au pic < 100 M$ |
| 740 | Swag | SWAG | ≈ 26 M$, 2024-11-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 741 | CumInu | CUMINU | ≈ 25,9 M$ en FDV (05/07/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 742 | Briun Armstrung | BRIUN | ~25,3 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 743 | WOOF | WOOF | ≈ 25,2 M$ (03/12/2021) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 744 | ElonDoge | EDOGE | ≈ 25,1 M$ en FDV (31/10/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 745 | Baby BNB | BABY | ≈ 25 M$ (13 oct. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 747 | IC Ghost | GHOST | ≈ 25 M$, 2024-01-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 748 | IQ50 | IQ50 | ≈ 25 à 67 M$ (16-28 mars 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 750 | Nasdaq666 | NDQ | ≈ 25 M$ (5 oct. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 751 | Parabolic | PARAX | ≈ 25 M$, 2025-05-30 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 753 | Noggles | NOGS | ~24,6 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 754 | BUBBLES (Bubbles Bean) | BUBBLES | ≈ 24,5 M$ (oct. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 755 | Squid Moon | SQM | ≈ 24,3 M$ en FDV (18/11/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 756 | AstroPepeX | APX | ≈ 24 M$ (date CoinGecko 18/11/2024, à vérifier) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 757 | Attention | ATTN | ≈ 24 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 758 | CATO | CATO | ≈ 24,0 M$ en FDV (28/10/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 759 | Chaos | CHAOS | ≈ 24 M$, 2024-12-31 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 760 | LAMBO | LAMBO | ≈ 24 M$ (29 juin 2025) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 761 | memes will continue | memes | ≈ 24 M$ (21/01/2026) | estimé | mort (≈ 58 k$) | rare | commune | mort au pic < 100 M$ |
| 762 | Suncat | SUNCAT | ≈ 24 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 763 | Windoge98 | EXE | ≈ 24 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 764 | Waka Flocka Flame † | FLOCKA | ≈ 23,8 M$ (estimé : -99 % jusqu'à 238 k$) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 765 | Okayeg | OKAYEG | ~23,6 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 766 | RUGMAN | RUG | ≈ 23,3 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 767 | Bloo | BLOO | ≈ 23 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 768 | DORK | DORK | ≈ 23 M$, 2023-11-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 769 | Frodo the virtual samurai | FROG | ≈ 23 M$ (29 déc. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 770 | GAME•OF•BITCOIN | GAME | ≈ 23 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 771 | HayCoin | HAY | ≈ 23 M$, 2023-10-25 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 772 | Peepo | PEEPO | ≈ 23 M$ (05/05/2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 773 | Red Hare Coin | RHC | ≈ 23 M$, 2026-04-26 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 774 | Smiley Coin | SMILEY | ≈ 23 M$, 2024-01-16 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 775 | 888 | 888 | ≈ 22 M$, 2024-11-30 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 776 | Bird Dog | BIRDDOG | ≈ 22 M$, 2024-06-10 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 777 | Buftoad | BUF | ≈ 22 M$ (16 avr. 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 778 | Catalorian | CATALORIAN | ≈ 22 M$, 2025-08-18 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 780 | GOGGLES | GOGLZ | ≈ 22 M$ (1 déc. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 781 | MUSTAAAAAARD | MUSTARD | ≈ 22 M$, 2024-11-27 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 782 | Nobiko Coin | LONG | ≈ 22 M$, 2025-10-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 783 | Pepe Community | PEPE | ≈ 22 M$, 2023-08-28 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 784 | Playdoge | PLAY | ≈ 22 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 785 | supercycle(real) | SUPERCYCLE | ≈ 22 M$, 2024-11-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 787 | Toad (SOL) | TOAD | ≈ 22 M$, 2024-11-02 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 788 | Wall St. Bull | WBULL | ≈ 22 M$ (08/10/2025) | estimé | mort (≈ 13 k$, volume nul) | rare | commune | mort au pic < 100 M$ |
| 789 | Wifejak | WIFE | ≈ 22 M$, 2024-11-28 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 790 | King Shiba | KINGSHIB | ≈ 21,9 M$ (16/12/2021) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 791 | Dogira | DOGIRA | ≈ 21,4 M$ en FDV (05/11/2021) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 792 | Base is for everyone | BASEISFOREVERYONE | ~21,1 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 793 | Baby Pepe | BABYPEPE | ≈ 21 M$, 2024-11-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 794 | POPDOG | POPDOG | ≈ 21 M$, 2024-09-25 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 795 | Sanin Inu | SANI | ≈ 21 M$, 2024-03-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 796 | Skull of Pepe Token | SKOP | ≈ 21 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 797 | YOLO | YOLO | ≈ 21 M$, 2026-08-30 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 798 | Ton Cat | TCAT | ≈ 20,9 M$ (juil. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 799 | Super Suiyan | SUIYAN | ≈ 20,8 M$ (mai 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 800 | NEAT | NEAT | ≈ 20,7 M$ (déc. 2023) ; ATH CoinGecko × offre totale | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 801 | Based Shiba Inu | BSHIB | ~20,6 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 802 | SHIBAVAX | SHIBX | ≈ 20,5 M$ (28/10/2021) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 803 | Carlo | CARLO | ~20,2 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 804 | Shibaken Finance | SHIBAKEN | ≈ 20,2 M$ en FDV (13/02/2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 805 | BabySNEK | BBSNEK | ≈ 20 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 806 | DOYR | DOYR | ≈ 20 M$ (07/12/2025) | estimé | mort (≈ 0,25 M$) | rare | commune | mort au pic < 100 M$ |
| 807 | Meowcoin | MEWC | ≈ 20 M$, 2022-10-09 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 808 | OSCAR | OSCAR | ≈ 20 M$, 2024-10-21 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 809 | Peepo (Solana) | PEEP | ≈ 20 M$ (10 déc. 2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 810 | Pepa Inu | PEPA | ≈ 20 M$ (21/04/2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 811 | RIBBIT | RBT | ≈ 20 M$, 2024-09-24 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 813 | Uranus (Solana) | ANUS | ≈ 20 M$ (31 mars 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 814 | Wolfi | WOLFI | ≈ 20 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 815 | Poncho | PONCHO | ~19,6 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 816 | Based Turbo | TURBO | ~19,5 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 817 | BOOK OF BILLIONAIRES | BOBE | ≈ 19,3 M$ (2 mai 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 818 | Bork | BORK | ≈ 19,1 M$ (8 mars 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 820 | Asteroid The Space Shiba Inu | ASTEROID | ≈ 19 M$, 2026-05-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 821 | Baby Doge Cash | BABYDOGECASH | ≈ 19 M$, 2021-07-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 822 | Based Chad | CHAD | ≈ 19 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 823 | Bitcoin 2.0 | BTC2.0 | ≈ 19 M$ (16/07/2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 824 | BNB Card | BNB CARD | ≈ 19 M$ (21/03/2025) | estimé | mort (≈ 33 k$, volume nul) | rare | commune | mort au pic < 100 M$ |
| 825 | CATGPT | CATGPT | ≈ 19 M$, 2026-09-12 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 827 | DNA | DNA | ≈ 19 M$, 2024-12-06 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 828 | Fish | FISH | ≈ 19 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 829 | Flying Avocado Cat | FAC | ≈ 19 M$, 2024-09-20 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 830 | Flying Ketamine Horse | FKH | ≈ 19 M$ (31/12/2025) | estimé | mort (≈ 25 k$, volume nul) | rare | commune | mort au pic < 100 M$ |
| 831 | FREN | FREN | ≈ 19 M$ (déc. 2023) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 832 | Kabosu Inu | KABOSU | ≈ 19 M$, 2024-05-23 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 833 | Kira the Injective Cat | KIRA | ≈ 19 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 834 | Morning Routine | ROUTINE | ≈ 19 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 836 | Shibwifhatcoin | SHIB | ≈ 19 M$, 2024-03-11 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 837 | Success Kid (Solana) | SKID | ≈ 19,0 M$ (20 mars 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 839 | Walter | WALTER | ≈ 19 M$, 2024-06-01 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 840 | YEETI 液体 | YEETI | ≈ 19,0 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 843 | build | BUILD | ≈ 18 M$, 2026-09-09 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 844 | COAL | COAL | ≈ 18 M$, 2025-11-09 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 845 | Echelon Token | ELON | ≈ 18 M$, 2026-02-02 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 846 | Elite (1337) | 1337 | ≈ 18,0 M$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 847 | GLORP | GLORP | ≈ 18 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 848 | Leopard | LEOPARD | ≈ 18 M$, 2021-10-16 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 849 | Luffy | LUFFY | ≈ 18 M$, 2024-12-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 850 | ORC | ORC | ≈ 18 M$, 2024-07-21 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 851 | RealGOAT | RGOAT | ≈ 18 M$ (13 oct. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 852 | TOES | TOESCOIN | ≈ 18 M$ (20/06/2026) | estimé | mort (≈ 45 k$) | rare | commune | mort au pic < 100 M$ |
| 854 | Young Peezy AKA Pepe | PEEZY | ~17,5 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 855 | Myra | MYRA | ≈ 17,3 M$ (20 janv. 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 856 | AAA Cat | AAA | ≈ 17 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 857 | Baby Neiro | BABYNEIRO | ≈ 17 M$, 2024-11-19 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 858 | BOBER | BOBER | ≈ 17 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 859 | BullDogito | BDOGITO | ≈ 17 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 860 | Chadimir Putni | PUTNI | ≈ 17 M$, 2024-03-25 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 861 | Coinye West | COINYE | ≈ 17 M$ (28 avr. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 862 | Floppa | FLOPPA | ≈ 17 M$, 2024-11-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 863 | Gemini | GEMINI | ≈ 17 M$, 2024-12-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 865 | HAHA | HAHA | ≈ 17 M$, 2023-05-06 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 866 | Lord Of SOL | LOS | ≈ 17 M$, 2024-05-10 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 867 | LOUD | LOUD | ≈ 17 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 868 | NearKat | NEARKAT | ≈ 17 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 869 | OneCOW | 1COW | ≈ 17 M$, 2026-09-27 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 870 | Pepe Trump | PTRUMP | ≈ 17 M$, 2024-05-28 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 871 | SPIKE | SPIKE | ≈ 17 M$ (26/04/2026) | estimé | mort (≈ 29 k$) | rare | commune | mort au pic < 100 M$ |
| 872 | Strategic Super Reserve | SSR | ≈ 17 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 873 | Toad Killer | TOAD | ≈ 17 M$, 2023-08-16 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 874 | Ucan fix life in1day | 1 | ≈ 17-21 M$ (20/01/2026) | estimé | mort (≈ 0,3 M$) | rare | commune | mort au pic < 100 M$ |
| 875 | Velvet Unicorn by Virtuals | VU | ≈ 17 M$, 2024-12-31 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 877 | Dogey-Inu | DINU | ≈ 16,7 M$ (15/11/2021) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 878 | Normilio | NORMILIO | ~16,7 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 879 | Autist | AUTIST | ≈ 16,6 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 880 | CumStar | CUMSTAR | ≈ 16,4 M$ (18/11/2021) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 881 | Weirdo | WEIRDO | ~16,2 M$ (date inconnue) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 883 | BUILD | BUILD | ≈ 16 M$, 2025-01-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 884 | Dogecoin20 | DOGE20 | ≈ 16 M$ (07/05/2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 885 | Fish N Chips | CHIPPY | ≈ 16 M$, 2024-05-19 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 886 | Fishkoin | KOIN | ≈ 16 M$, 2024-03-24 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 887 | Galaxy Fox | GFOX | ≈ 16 M$, 2024-05-08 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 888 | Hachi | HACHI | ≈ 16 M$, 2024-04-21 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 889 | Jester | JEST | ≈ 16 M$, 2024-08-22 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 890 | Little Ugly Duck | LUD | ≈ 16 M$, 2021-08-17 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 891 | Mellow Man | MELLOW | ≈ 16 M$, 2024-08-21 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 892 | Nikepig | NIKEPIG | ≈ 16 M$, 2024-06-26 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 893 | NSDQ420 | NSDQ | ≈ 16 M$, 2025-01-06 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 894 | PMX500 | PMX | ≈ 16 M$, 2025-08-23 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 895 | Povel Durev | DUREV | ≈ 16 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 896 | RAT Escape | RAT | ≈ 16 M$, 2024-12-12 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 897 | SPARTA | SPARTA | ≈ 16 M$, 2025-09-12 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 898 | You Looked | CIRCLE | ≈ 16,0 M$ (8 mars 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 899 | Eggdog | EGG | ≈ 15,9 M$ (25 déc. 2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 902 | All Will Retire | AWR | ≈ 15 M$, 2025-01-25 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 903 | Aped | APED | ≈ 15 M$, 2024-11-14 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 904 | Biden Coin | BIDEN | ≈ 15 M$, 2025-07-06 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 905 | Bitcoin on Base | BTCB | ≈ 15 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 906 | DEBT | DEBT | ≈ 15 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 907 | Draggy CTO | DRAGGY | ≈ 15 M$, 2024-07-12 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 908 | GDOG | GDOG | ≈ 15 M$, 2024-10-28 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 909 | Lobstar | LOBSTAR | ≈ 15-17 M$ (21-23/02/2026) | estimé | mort (≈ 44 k$) | rare | commune | mort au pic < 100 M$ |
| 910 | Memelinked | MK | ≈ 15 M$, 2025-05-08 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 911 | Nitefeeder | NITEFEEDER | ≈ 15 M$, 2024-07-18 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 913 | Raydium Cat | RAYCAT | ≈ 15 M$, 2026-09-11 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 914 | Snibbu | SNIBBU | ≈ 15 M$, 2024-04-01 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 915 | 黑马 (Cheval noir) | 黑马 | ≈ 15 M$ (13/01/2026) | estimé | mort (≈ 0,3 M$) | rare | commune | mort au pic < 100 M$ |
| 917 | Roost | ROOST | ≈ 14,8 M$ (23 juin 2024), sourcé (FDV max ≈ 68 M$) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 918 | BunnyCoin | BUN | ≈ 14,7 M$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 919 | Crodie | CRODIE | ≈ 14,7 M$ (10 mai 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 920 | GhibliCZ | GHIBLI | ≈ 14,6 M$ (mars 2025) | sourcé | mort (≈ 44 k$) | rare | commune | mort au pic < 100 M$ |
| 921 | Mistery | MERY | ≈ 14,6 M$ (12 janv. 2025), sourcé | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 922 | Abble | AABL | ≈ 14,5 M$ (6 avr. 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 923 | Amocucinare | AMORE | ≈ 14 M$, 2024-11-25 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 924 | ASTEROID | ASTEROID | ≈ 14 M$, 2026-09-10 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 925 | Baby Neiro BNB | BABYNEIRO | ≈ 14 M$ (24 nov. 2024) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 926 | BananaCat | BCAT | ≈ 14 M$, 2024-11-28 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 927 | Belgian Malinois | BELG | ≈ 14 M$ (07/10/2025) | estimé | mort (≈ 33 k$) | rare | commune | mort au pic < 100 M$ |
| 928 | Brent on SOL | BRENT | ≈ 14 M$, 2026-04-17 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 929 | FartStrategy | FSTR | ≈ 14 M$, 2025-01-30 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 930 | Good In The Hood | GOOD | ≈ 14 M$, 2026-08-27 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 931 | KittyCake | KCAKE | ≈ 14 M$, 2021-07-28 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 932 | Knot Diffie-Hellman | KNOT | ≈ 14 M$, 2024-12-10 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 933 | MoonDog AI | MDOGAI | ≈ 14 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 934 | SPYRO | SPYRO | ≈ 14 M$, 2024-02-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 935 | SZN | SZN | ≈ 14 M$ (sourcé) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 936 | Trash Coin | TRASH | ≈ 14 M$, 2025-07-23 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 937 | Treat Token | TREAT | ≈ 14 M$, 2024-03-06 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 938 | Jesus Coin (2017) | JC | ≈ 13,9 M$, 18/02/2018 (CMC, relevé hebdomadaire) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 939 | Suicy the Seal | SUICY | ≈ 13,9 M$ (déc. 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 940 | BabyPepe | BABYPEPE | ≈ 13,5 M$ (05/05/2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 942 | SUITRUMP | SUITRUMP | ≈ 13,4 M$ (mai 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 943 | Solana Shib | SSHIB | ≈ 13,3 M$ (24 déc. 2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 944 | BillionHappiness | BHC | ≈ 13,1 M$ (09/11/2021) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 946 | ATEHUN | ATEHUN | ≈ 13 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 947 | BabyKitty | BABYKITTY | ≈ 13 M$, 2021-12-30 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 948 | BarbieCrashBandicootRFK88 | SOLANA | ≈ 13 M$, 2023-10-26 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 949 | BIG | BIG | ≈ 13 M$ (16 févr. 2025) ; CMC, relevé hebdomadaire | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| 950 | Capybara Token | CAPY | ≈ 13 M$, 2023-05-09 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 951 | CAT | CAT | ≈ 13 M$, 2024-05-27 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 952 | Didi Bam Bam | DDBAM | ≈ 13 M$, 2024-12-02 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 953 | DORK LORD | DORKL | ≈ 13 M$ (08/09/2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 954 | HotDoge [OLD] | HOTDOGE | ≈ 13 M$, 2021-05-11 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 955 | HUA HUA | HUAHUA | ≈ 13 M$, 2024-12-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 956 | MindCoin | MIND | ≈ 13 M$, 2024-08-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 957 | Mittens | MITTENS | ≈ 13 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 958 | NEKO | NEKO | ≈ 13 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 959 | PIKA to PIKO ピカとピコ | PIKA | ≈ 13 M$, 2024-10-16 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 960 | remilio | REMILIO | ≈ 13 M$, 2024-05-07 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 961 | SatoshAI | SAI | ≈ 13 M$, 2026-08-01 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 963 | Shiba Classic | SHIBC | ≈ 13 M$, 2024-11-14 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 965 | BOZO | BOZO | ≈ 12,8 M$ (20 janv. 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 966 | ArbiDoge | ADOGE | ≈ 12 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 967 | artificial gooner intelligence | AGI | ≈ 12 M$, 2026-09-06 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 968 | Baby Asteroid | BABYASTEROID | ≈ 12 M$, 2026-05-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 969 | BEAMCAT | BCAT | ≈ 12 M$ (mars 2024) ; ATH CoinGecko × offre en circulation actuelle | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 971 | Defi Tiger | DTG | ≈ 12 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 972 | DuckCoin | DUCK | ≈ 12,0 M$ (mai 2024) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 973 | Estee | ESTEE | ≈ 12 M$, 2024-09-30 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 974 | FARTGIRL | FARTGIRL | ≈ 12 M$, 2025-02-17 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 975 | Fefe | FEFE | ≈ 12 M$, 2024-10-17 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 976 | Gluteus Maximus by Virtuals | GLUTEU | ≈ 12 M$, 2025-01-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 977 | Golden Goose | GG | ≈ 12 M$, 2026-08-30 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 978 | Gondola | GONDOLA | ≈ 12 M$, 2024-10-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 979 | LOL | LOL | ≈ 12 M$ (01/04/2026) | estimé | mort (≈ 60 k$) | rare | commune | mort au pic < 100 M$ |
| 980 | Pistacio | PISTACIO | ≈ 12 M$, 2026-08-26 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 981 | Polly | POLLY | ≈ 12 M$, 2025-08-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 982 | Scam Altman | SCAM | ≈ 12 M$, 2026-04-28 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 984 | Toby | TOBY | ≈ 12 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 985 | Token6900 | T6900 | ≈ 12 M$, 2025-09-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 986 | vankedisi | VANKEDISI | ≈ 12 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 987 | Wen Lambo | WEN | ≈ 12 M$, 2026-07-12 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 988 | World Cup Coin | à vérifier | ≈ 12 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 989 | Beeg Blue Whale | BEEG | ≈ 11,9 M$ (mai 2025) ; ATH CoinGecko × offre en circulation | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 990 | Kermit (Solana) | KERMIT | ≈ 11,8 M$ (20 mars 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 992 | What in Tarnation? | WIT | ≈ 11,5 M$ (28 avr. 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 993 | All Your Base | AYB | ≈ 11 M$, 2024-03-29 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 994 | ARE YA WINNING, SON? | SON | ≈ 11 M$, 2025-08-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 995 | BASED | BASED | ≈ 11 M$, 2024-08-13 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 996 | Binance Super Cycle | BSC | ≈ 11 M$, 2025-10-08 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 997 | Black Dragon | BLACKDRAGON | ≈ 11 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 998 | Doge 2.0 | DOGE2.0 | ≈ 11 M$ (07/07/2023) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 999 | Dork Lord | DORKY | ≈ 11 M$, 2026-08-01 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1000 | HarryPotterTrumpHomerSimpson777Inu | ETHEREUM | ≈ 11 M$, 2024-03-03 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1001 | Hund | HUND | ≈ 11 M$, 2024-04-02 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1002 | Mark-2-Marquette | M2M | ≈ 11 M$, 2026-04-25 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1003 | MEMENTO•MORI | MEMENTO | ≈ 11 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| 1004 | Mommy Doge | MOMMYDOGE | ≈ 11 M$, 2021-07-11 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1005 | PEPECASH | PECH | ≈ 11 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1006 | Signal | SIGNAL | ≈ 11 M$, 2026-10-05 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1009 | Sweep Token | SWEEP | ≈ 11 M$, 2023-02-18 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1010 | TOLY'S DOG | ADA | ≈ 11 M$, 2024-03-29 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1011 | Transhuman Coin | THC | ≈ 11 M$, 2021-11-14 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1012 | Vibe Cat | VIBE | ≈ 11 M$, 2025-06-19 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1013 | Viva | à vérifier | ≈ 11 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1014 | WISHBONE | WISHBONE | ≈ 11 M$, 2026-07-14 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1015 | 雪球人生 (Vie boule de neige) | 雪球人生 | ≈ 11 M$ (23/04/2026) | estimé | mort (≈ 96 k$) | rare | commune | mort au pic < 100 M$ |
| 1016 | AI Dragon | CHATGPT | ≈ 10,9 M$ (30 mars 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1017 | Pou | POU | ≈ 10,8 M$ (15 mars 2024) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1018 | All in Dollo | DOLLO | ≈ 10 M$, 2025-08-14 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1019 | ASSDAQ | ASSDAQ | ≈ 10 M$, 2025-08-05 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1022 | CALI | CALI | ≈ 10 M$, 2026-09-27 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1025 | Froth | FROTH | ≈ 10 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1026 | GBOY | GBOY | ≈ 10 M$, 2026-01-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1027 | King Of Meme | LION | ≈ 10 M$, 2024-06-18 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1028 | Matt Furie | MATT | ≈ 10 M$, 2024-07-15 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1029 | PREME Token | PREME | ≈ 10 M$, 2026-06-29 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1032 | Wagmi Coin | WAGMI | ≈ 10 M$, 2023-05-24 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| 1313 | Nyancoin | NYAN | ≈ 2,7 M$, 07/01/2018 (plancher, relevé hebdomadaire) | sourcé | mort (absent de CoinGecko) | rare | commune | pic < 10 M$ |
| 1413 | Useless Ethereum Token † | UET | ≈ 0,31 M$, 28/01/2018 | sourcé | mort (absent de CoinGecko) | épique | commune | pic < 10 M$ |
| 1590 | Prodeum | PRO | inconnu (levée de 43 ETH selon une enquête, chiffres de 11 $ à 970 ETH dans la presse) | inconnu | mort | épique | commune | pic inconnu |
| 1591 | Proof of Weak Hands (PoWH 3D) | P3D | inconnu (contrat proche de 1 M$ selon une source) | inconnu | mort | rare | commune | pic inconnu |
| 1605 | Save The Kids | KIDS | inconnu | inconnu | mort | épique | commune | pic inconnu |
| AD10 | Central African Republic Meme | CAR | ≈ 770 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| AD16 | MAGA Hat | MAGA | ≈ 305 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| AD18 | Retardio † | RETARDIO | ≈ 242 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| AD20 | M3M3 | M3M3 | ≈ 187 M$ (estimé CG) | estimé | mort | rare | épique | pic 100 M$ - 1 Md$ |
| AD21 | TrumpCoin | DJT | ≈ 183 M$ (estimé CG) | estimé | mort (absent de CoinGecko) | commune | épique | pic 100 M$ - 1 Md$ |
| AD25 | Butthole Coin | BUTTHOLE | ≈ 133 M$ (estimé CG) | estimé | en déclin (-95 % ou pire) | rare | épique | pic 100 M$ - 1 Md$ |
| AD39 | Hunter Biden's Laptop | LAPTOP | ≈ 34,13 Md$ (estimé CG) — estimation aberrante, à vérifier | estimé | en déclin (-95 % ou pire) | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| AD40 | ShibaBitcoin | SHIBTC | ≈ 1,02 Md$ (9 févr. 2025) ; CMC, relevé hebdomadaire (pic CMC douteux) — estimation aberrante, à vérifier | estimé | mort | rare | commune | estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu |
| AD41 | Skibidi Toilet | SKBDI | ≈ 77 M$ (date inconnue) | estimé | mort (≈ 0,21 M$) | rare | commune | mort au pic < 100 M$ |
| AD42 | ArAIstotle | FACY | ≈ 73 M$, 2025-10-05 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD44 | Gooncoin | GOONC | ≈ 68 M$ (estimé CG, au-dessus de la borne sourcée) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD46 | Pussy Financial | PUSSY | ≈ 65 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD48 | Jenner | JENNER | ≈ 44 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| AD49 | Opus Genesis | OPUS | ≈ 42 M$, 2024-11-28 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD50 | AGENDA 47 | A47 | ≈ 41 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD51 | Wolf | WOLF | ≈ 40 M$ (sourcé) | sourcé | mort (≈ 0,53 M$ deux jours après le lancement du 08/03/2025) | rare | commune | mort au pic < 100 M$ |
| AD53 | Jason Derulo | JASON | ≈ 35,6 M$ (estimé : -97,8 % jusqu'à 783 k$) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD54 | GrokCoin | GROKCOIN | ≈ 34 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| AD55 | Ben Coin (BitBoy) | BEN | ≈ 30 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| AD56 | DopeCoin | DOPE | ≈ 27,2 M$, 31/12/2017 (CMC, relevé hebdomadaire) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| AD57 | SroomAI DAO | SHR0 | ≈ 27 M$, 2025-05-22 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD58 | CannabisCoin | CANN | ≈ 26,9 M$, 07/01/2018 (CMC, relevé hebdomadaire) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| AD59 | Kamala Horris † | KAMA | ≈ 26 M$ (26 juil. 2024, jour du lancement) | sourcé | mort | rare | commune | mort au pic < 100 M$ |
| AD60 | Odin Liquidity Network | ODIN | ≈ 24 M$, 2024-12-03 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD61 | uP Token | UP | ≈ 24 M$, 2023-12-01 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD62 | Hulk Hogan | HULK | ≈ 19 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| AD63 | Hoodrat | HOODRAT | ≈ 17 M$ (estimé CG) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD64 | Danold Tromp | DANOLD | ≈ 15 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| AD65 | TabbyPOS | TABBY | ≈ 15 M$, 2023-10-04 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD66 | PutinCoin | PUT | ≈ 12,1 M$, 08/01/2018 (confirme la rareté rare plutôt que commune) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| AD67 | Red Kitten Crew | RKC | ≈ 12 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| AD68 | COQ AI | COQAI | ≈ 11 M$, 2025-01-11 (CoinGecko, ATH × offre actuelle) | estimé | mort | rare | commune | mort au pic < 100 M$ |
| AD69 | Wanko | WANKO | ≈ 10 M$ (sourcé) | sourcé | mort (absent de CoinGecko) | rare | commune | mort au pic < 100 M$ |
| AD72 | TrumpCoin † | TRUMP | ≈ 4,8 M$, 06/01/2018 (5,3 M$ au relevé hebdomadaire du 07/01/2018) | sourcé | mort | rare | commune | pic < 10 M$ |
| AD89 | Coinye | COINYE | inconnu | inconnu | mort (absent de CoinGecko) | épique | commune | pic inconnu |

## Annexe 3 : réserve (candidats R5 C2, estimation fragile)

801 jetons non présents au catalogue, écart ≤ -99,5 % : pics estimés peu fiables. À reprendre un par un si le porteur veut grossir la masse des communes.

| CoinGecko id | Nom | Ticker | Pic estimé | Date du plus haut | Remarque |
|---|---|---|---|---|---|
| `meow` | MEOW | MEOW | ≈ 977 M$ | 2025-02-20 | mort |
| `beardy-dragon` | Bearded Dragon | BEARDY | ≈ 943 M$ | 2024-04-03 | mort |
| `angryb` | Angryb | ANB | ≈ 848 M$ | 2021-07-25 | mort |
| `get-ai` | Get AI | GET | ≈ 799 M$ | 2025-02-13 | nature à vérifier; mort |
| `levana-protocol` | Levana | LVN | ≈ 718 M$ | 2023-12-19 | mort |
| `suibeaver` | suibeaver | DAM | ≈ 699 M$ | 2026-03-27 | mort |
| `solordi` | Solordi | SOLO | ≈ 692 M$ | 2026-04-01 | mort |
| `lumoscoin` | Lumos | LUMOS | ≈ 691 M$ | 2026-04-11 | mort |
| `ket` | Ket | KET | ≈ 617 M$ | 2025-05-28 | copie ou ancienne version d'une carte; mort |
| `shmeegus` | Shmeegus | SHMEEGUS | ≈ 584 M$ | 2026-01-21 | mort |
| `department-of-government-efficiency` | Department Of Government Efficiency | DOGE | ≈ 502 M$ | 2024-11-13 |  |
| `we-love-t` | We Love Tits | TITS | ≈ 484 M$ | 2024-11-24 | mort |
| `maga-trump` | MAGA Trump | MAGATRUMP | ≈ 481 M$ | 2025-02-14 | mort |
| `harambe-ai` | Harambe AI | HARAMBEAI | ≈ 469 M$ | 2024-07-17 | nature à vérifier; mort |
| `milk` | Cool Cats Milk | MILK | ≈ 461 M$ | 2022-02-15 | mort |
| `gameswift` | GameSwift | GSWIFT | ≈ 382 M$ | 2024-03-04 | nature à vérifier; mort |
| `unix` | UniX | UNIX | ≈ 361 M$ | 2021-11-30 | mort |
| `shiro-neko-2` | Shiro Neko | SHIRO | ≈ 354 M$ | 2024-12-08 | mort |
| `neon-neko` | NeonNeko | NEKO | ≈ 340 M$ | 2025-07-22 | mort |
| `k9-finance-dao` | K9 Finance DAO | KNINE | ≈ 328 M$ | 2024-03-10 | nature à vérifier; mort |
| `michicoin` | michi [OLD] | $MICHI | ≈ 327 M$ | 2024-05-16 | copie ou ancienne version d'une carte; mort |
| `lambo-0fcbf0f7-1a8f-470d-ba09-797d5e95d836` | LAMBO | LAMBO | ≈ 309 M$ | 2024-03-19 | mort |
| `first-convicted-raccon` | First Convicted RACCON | FRED | ≈ 303 M$ | 2024-11-13 |  |
| `freedom-coin` | FREEdom coin | FREE | ≈ 302 M$ | 2019-03-03 | mort |
| `american-coin` | American Coin | USA | ≈ 296 M$ | 2025-01-19 |  |
| `memes` | MEMES | MEMES | ≈ 283 M$ | 2024-12-20 | mort |
| `mumu-the-bull-3` | MUMU THE BULL [OLD] | MUMU | ≈ 280 M$ | 2024-07-29 | copie ou ancienne version d'une carte; mort |
| `dog-collar` | Dog Collar | COLLAR | ≈ 263 M$ | 2021-11-02 | mort |
| `catton-ai` | Catton AI | CATTON | ≈ 249 M$ | 2025-02-06 | nature à vérifier; mort |
| `rifampicin` | Rifampicin | $RIF | ≈ 248 M$ | 2024-11-18 | mort |
| `elon4afd` | Elon4AfD | ELON4AFD | ≈ 247 M$ | 2025-02-03 | mort |
| `chonky` | CHONKY [OLD] | CHONKY | ≈ 233 M$ | 2026-04-01 | mort |
| `wall-street-bets-dapp` | WallStreetBets DApp | WSB | ≈ 225 M$ | 2021-05-05 | mort |
| `million` | Million | MM | ≈ 223 M$ | 2021-07-13 | mort |
| `the-real-landwolf` | LandWolf | WOLF | ≈ 223 M$ | 2024-06-21 | copie ou ancienne version d'une carte; mort |
| `burp` | Burp | BURP | ≈ 214 M$ | 2021-07-26 | mort |
| `normie-2` | NORMIE | NORMIE | ≈ 212 M$ | 2024-03-25 | copie ou ancienne version d'une carte; mort |
| `baby-myro` | Baby Myro | BABYMYRO | ≈ 209 M$ | 2024-01-17 | mort |
| `omnicat` | OmniCat | OMNI | ≈ 208 M$ | 2023-12-23 | mort |
| `max-2` | MAX | MAX | ≈ 208 M$ | 2025-01-07 | mort |
| `dasha` | Dasha | VVAIFU | ≈ 207 M$ | 2024-11-18 | mort |
| `gotti-token` | Gotti Token | GOTTI | ≈ 207 M$ | 2024-07-02 | mort |
| `shih-tzu` | Shih Tzu | SHIH | ≈ 207 M$ | 2021-05-11 | mort |
| `fartful` | FARTFUL | FARTFUL | ≈ 205 M$ | 2025-08-28 | mort |
| `ibiza-final-boss` | Ibiza Final Boss | BOSS | ≈ 203 M$ | 2026-05-25 | mort |
| `the-soldog` | LAIKA the Cosmodog | LAIKA | ≈ 199 M$ | 2024-06-13 | mort |
| `banana-tape-wall` | Banana Tape Wall | BTW | ≈ 192 M$ | 2026-06-20 | mort |
| `doge-floki-coin` | Doge Floki Coin [OLD] | DOFI | ≈ 185 M$ | 2021-10-28 | mort |
| `lovebit` | LoveBit | LB | ≈ 183 M$ | 2024-07-11 | mort |
| `numogram` | Numogram | GNON | ≈ 182 M$ | 2024-10-19 | mort |
| `solchat` | Solchat | CHAT | ≈ 174 M$ | 2024-03-17 | mort |
| `altcoin-2` | Altcoin | ALT | ≈ 173 M$ | 2025-07-13 | mort |
| `dechat` | Dechat | DECHAT | ≈ 172 M$ | 2024-03-11 | mort |
| `alpha-4` | Alpha | ALPHA | ≈ 172 M$ | 2025-02-04 |  |
| `papa-trump` | PAPA Trump | PPT | ≈ 171 M$ | 2024-07-02 | mort |
| `oob` | Oob | OOB | ≈ 170 M$ | 2026-03-26 | mort |
| `just-a-frog` | just a frog | FROG | ≈ 169 M$ | 2026-01-19 | mort |
| `eliza` | Eliza | ELIZA | ≈ 166 M$ | 2024-12-31 | mort |
| `litecoin-mascot` | Litecoin Mascot | LESTER | ≈ 154 M$ | 2024-11-15 | mort |
| `justice-for-pnut-and-fred` | Justice for Pnut and Fred | JUSTICE | ≈ 152 M$ | 2024-11-25 | mort |
| `lil-shrub` | Lil' Shrub | SHRUB | ≈ 148 M$ | 2026-09-04 | mort |
| `der-daku` | Daku | DAKU | ≈ 148 M$ | 2025-05-23 | mort |
| `shiba-armstrong` | Shiba Armstrong | SHIBA | ≈ 146 M$ | 2024-05-20 | mort |
| `urolithin-a` | Urolithin A | $URO | ≈ 144 M$ | 2024-11-18 | mort |
| `large-language-model` | Large Language Model | LLM | ≈ 144 M$ | 2025-01-09 |  |
| `luci` | LUCI | LUCI | ≈ 141 M$ | 2026-04-01 | mort |
| `characcon` | characcon | CHARACCON | ≈ 141 M$ | 2026-05-17 | mort |
| `dinger-token` | Dinger | DINGER | ≈ 135 M$ | 2021-10-28 | mort |
| `shiryo-inu` | Shiryo | SHIRYO-INU | ≈ 135 M$ | 2021-11-20 | mort |
| `retard-finder-coin` | Retard Finder Coin | RFC | ≈ 133 M$ | 2025-04-13 | mort |
| `tsuki-inu` | Tsuki Inu | TKINU | ≈ 131 M$ | 2021-05-21 | mort |
| `freerossdao` | FreeRossDAO | FREE | ≈ 129 M$ | 2021-12-15 | nature à vérifier; mort |
| `kedaenge` | Kedaenge | KEDAENGE | ≈ 128 M$ | 2026-05-03 | mort |
| `baby-shark-meme` | Baby Shark Meme | BABYSHARK | ≈ 125 M$ | 2025-01-10 | mort |
| `pythia` | PYTHIA | PYTHIA | ≈ 125 M$ | 2025-08-27 | mort |
| `city-boy` | City Boy | CITYBOY | ≈ 124 M$ | 2026-03-10 | mort |
| `look` | LOOK | LOOK | ≈ 121 M$ | 2025-11-01 | mort |
| `dogeai-2` | DOGEai | $DOGEAI | ≈ 119 M$ | 2025-01-23 | mort |
| `w-coin` | W coin | W | ≈ 111 M$ | 2025-07-02 | mort |
| `hot-mom` | Hot Mom | HOTMOM | ≈ 110 M$ | 2025-05-14 | mort |
| `befe` | BEFE | BEFE | ≈ 110 M$ | 2023-12-27 | mort |
| `kitten-haimer` | Kitten Haimer | KHAI | ≈ 105 M$ | 2024-04-11 | mort |
| `harrypotterobamapacman8inu` | HarryPotterObamaPacMan8Inu | XRP | ≈ 105 M$ | 2023-08-19 | mort |
| `degen-spartan-ai` | Degen Spartan AI | DEGENAI | ≈ 105 M$ | 2025-01-02 | nature à vérifier; mort |
| `top-hat` | Top Hat | HAT | ≈ 105 M$ | 2025-01-02 | mort |
| `kiki-2` | KIKICat | KIKI | ≈ 103 M$ | 2024-12-26 | mort |
| `project89` | Project89 [OLD] | PROJECT89 | ≈ 101 M$ | 2024-11-22 | mort |
| `chaos-and-disorder` | chaos and disorder | CHAOS | ≈ 100 M$ | 2024-11-22 | mort |
| `enjoy` | Enjoy | ENJOY | ≈ 98 M$ | 2024-04-04 | mort |
| `farm-2` | FARM | FARM | ≈ 98 M$ | 2025-01-03 | mort |
| `aicell` | AICell | AICELL | ≈ 98 M$ | 2024-12-29 | mort |
| `doglibre` | DogLibre | DOGL | ≈ 98 M$ | 2024-12-12 | mort |
| `pepe-in-a-memes-world` | pepe in a memes world | PEW | ≈ 97 M$ | 2024-05-31 | mort |
| `salvator-mundi` | Salvator Mundi | MUNDI | ≈ 97 M$ | 2024-12-01 | mort |
| `jen-hsun-huang` | JHH | JHH | ≈ 96 M$ | 2024-10-01 | mort |
| `bobacat` | Boba Cat | BOBA | ≈ 94 M$ | 2024-03-29 | mort |
| `rizznet` | RZTO | RZTO | ≈ 94 M$ | 2025-10-29 | mort |
| `baby` | Baby | BABY | ≈ 93 M$ | 2024-04-15 | mort |
| `major-frog` | Major Frog | MAJOR | ≈ 93 M$ | 2024-11-15 | mort |
| `coco-coin` | COCO COIN | COCO | ≈ 92 M$ | 2025-01-01 | mort |
| `deep-worm` | Deep Worm | WORM | ≈ 92 M$ | 2024-11-19 | mort |
| `aimonica-brands` | Aimonica Brands | AIMONICA | ≈ 92 M$ | 2025-01-02 | mort |
| `strategic-bitcoin-reserve` | Strategic Bitcoin Reserve | SBR | ≈ 91 M$ | 2024-11-14 | mort |
| `department-of-gov-efficiency` | Department of Gov Efficiency | DOGE | ≈ 91 M$ | 2024-11-13 | mort |
| `rnt-token` | RNT | RNT | ≈ 90 M$ | 2024-06-07 | mort |
| `nomnom` | nomnom | NOMNOM | ≈ 90 M$ | 2024-11-16 | mort |
| `evil-larry` | Evil Larry | LARRY | ≈ 89 M$ | 2025-09-21 | mort |
| `harambe-2` | Harambe on Solana | HARAMBE | ≈ 88 M$ | 2024-11-13 | mort |
| `based-fartcoin` | Based Fartcoin | FARTCOIN | ≈ 88 M$ | 2025-01-17 | mort |
| `dolan-duck` | Dolan Duck | DOLAN | ≈ 88 M$ | 2024-10-18 | mort |
| `terminal-of-fun` | terminal of fun | FUN | ≈ 88 M$ | 2026-05-08 | mort |
| `commander-vrax-3` | Commander VRAX | VRAX | ≈ 87 M$ | 2026-10-02 | copie ou ancienne version d'une carte; mort |
| `ani-grok-companion` | Ani Grok Companion | ANI | ≈ 87 M$ | 2025-07-22 |  |
| `official-zuno` | OFFICIAL ZUNO | ZUNO | ≈ 86 M$ | 2025-11-11 | mort |
| `mut` | MUT | MUT | ≈ 86 M$ | 2024-12-06 | mort |
| `shibgf` | SHIBGF | SHIBGF | ≈ 86 M$ | 2021-11-01 | mort |
| `dark-maga` | Dark MAGA | DMAGA | ≈ 85 M$ | 2024-07-22 | mort |
| `solly` | SOLLY | SOLLY | ≈ 85 M$ | 2024-06-13 | mort |
| `evan-2` | Evan | EVAN | ≈ 85 M$ | 2024-12-08 | mort |
| `koala-ai` | KOALA AI | KOKO | ≈ 85 M$ | 2024-10-22 | nature à vérifier; mort |
| `patriot` | Patriot | PATRIOT | ≈ 84 M$ | 2025-01-11 | mort |
| `cheyenne` | Cheyenne | CHEYENNE | ≈ 84 M$ | 2024-11-16 | mort |
| `hemule` | Hemule | HEMULE | ≈ 83 M$ | 2024-03-11 | mort |
| `magaverse` | Magaverse | MVRS | ≈ 82 M$ | 2025-01-16 | mort |
| `fight-to-maga` | Fight to MAGA | FIGHT | ≈ 81 M$ | 2024-07-16 | mort |
| `ginnan-the-cat` | Ginnan The Cat | GINNAN | ≈ 81 M$ | 2024-08-07 | mort |
| `wolfwifballz` | WolfWifBallz | BALLZ | ≈ 81 M$ | 2024-03-17 | mort |
| `blub-2` | Blub | BLUB | ≈ 79 M$ | 2025-03-06 | copie ou ancienne version d'une carte; mort |
| `sentio-protocol` | Sentio AI | SEN | ≈ 79 M$ | 2025-01-06 | nature à vérifier; mort |
| `neiro` | Neiro | NEIRO | ≈ 79 M$ | 2024-07-29 | copie ou ancienne version d'une carte |
| `solmail` | SolMail | MAIL | ≈ 78 M$ | 2024-03-27 | mort |
| `cat-dog` | Cat-Dog | CATDOG | ≈ 78 M$ | 2024-08-08 | mort |
| `just-buy-1-worth-of-this-coin` | just buy $1 worth of this coin | $1 | ≈ 78 M$ | 2024-11-27 |  |
| `autonomous-virtual-beings` | Autonomous Virtual Beings | AVB | ≈ 77 M$ | 2025-01-10 | mort |
| `pino` | PINO | PINO | ≈ 77 M$ | 2024-12-13 | mort |
| `dongo-ai` | Dongo AI | DONGO | ≈ 76 M$ | 2024-03-29 | nature à vérifier; mort |
| `ben-the-dog` | Ben the Dog | BENDOG | ≈ 75 M$ | 2024-06-05 | mort |
| `uranus-4` | Uranus | URANUS | ≈ 73 M$ | 2025-07-30 | mort |
| `musk-it` | Musk It | MUSKIT | ≈ 73 M$ | 2025-01-31 | mort |
| `u-s-oil` | U.S Oil | USOR | ≈ 72 M$ | 2026-01-20 | mort |
| `dog-with-apple-in-mouth` | dog with apple in mouth | APPLE | ≈ 72 M$ | 2024-12-15 | mort |
| `forest` | FOREST | FOREST | ≈ 72 M$ | 2024-11-16 | mort |
| `international-meme-fund` | International Meme Fund | IMF | ≈ 71 M$ | 2025-07-14 | mort |
| `mad-2` | MAD | MAD | ≈ 71 M$ | 2024-11-22 |  |
| `plankton-in-pain` | Plankton in Pain | AAAHHM | ≈ 70 M$ | 2024-12-19 | mort |
| `faml` | FAML | FAML | ≈ 70 M$ | 2024-11-27 | mort |
| `giko-cat` | Giko Cat | GIKO | ≈ 69 M$ | 2024-10-06 | mort |
| `flavia-is-online` | Flavia Is Online | FLAVIA | ≈ 68 M$ | 2024-10-23 | mort |
| `tcc` | TCC | TCC | ≈ 68 M$ | 2026-07-05 | mort |
| `fins` | FINS | FINS | ≈ 68 M$ | 2026-06-25 | mort |
| `ethervista` | Ethervista | VISTA | ≈ 67 M$ | 2024-11-01 |  |
| `aishiba` | AiShiba | SHIBAI | ≈ 65 M$ | 2023-04-20 | mort |
| `kween` | KWEEN | KWEEN | ≈ 65 M$ | 2024-12-16 | mort |
| `tetsuo-coin` | Tetsuo Coin | TETSUO | ≈ 65 M$ | 2025-01-11 | mort |
| `degecoin` | DegeCoin | $DEGE | ≈ 64 M$ | 2025-07-18 | mort |
| `illusion-of-life` | Illusion of Life | SPARK | ≈ 64 M$ | 2025-08-11 |  |
| `hahayes` | HahaYes | RIZO | ≈ 64 M$ | 2024-11-18 | mort |
| `bitcoin-cats` | Bitcoin Cats | 1CAT | ≈ 63 M$ | 2023-12-28 | mort |
| `theydontloveyoulikeiloveyou` | theydontloveyoulikeiloveyou | WAIT | ≈ 63 M$ | 2024-11-20 | mort |
| `tema` | Tema | TEMA | ≈ 63 M$ | 2024-12-26 | mort |
| `npcs-ai` | NPCS AI | XNPCS | ≈ 62 M$ | 2025-04-30 | nature à vérifier; mort |
| `optimus-ai` | Optimus AI | OPTI | ≈ 62 M$ | 2024-03-09 | nature à vérifier; mort |
| `big-pharmai` | Big Pharmai | DRUGS | ≈ 61 M$ | 2025-01-01 | mort |
| `fpi-bank` | FPI Bank | FPIBANK | ≈ 61 M$ | 2025-02-06 | mort |
| `fight` | FIGHT | FIGHT | ≈ 61 M$ | 2025-01-19 | mort |
| `stonks-5` | STONKS | STONKS | ≈ 60 M$ | 2025-03-02 | copie ou ancienne version d'une carte; mort |
| `zeus-4` | Zeus | ZEUS | ≈ 59 M$ | 2025-05-29 | mort |
| `unfk` | UNFK | $UNFK | ≈ 59 M$ | 2024-11-15 | mort |
| `just-a-black-rock-on-base` | Just a Black Rock on Base | ROCK | ≈ 59 M$ | 2024-03-29 | mort |
| `costco-hot-dog` | Cost Hot Dog | COST | ≈ 59 M$ | 2024-04-15 | mort |
| `shroom` | Shroom | SHROOM | ≈ 58 M$ | 2024-03-19 | mort |
| `she-rises` | Akasha | AKA | ≈ 58 M$ | 2025-01-07 | mort |
| `biao-on-sol` | BIAO on SOL | BIAO | ≈ 58 M$ | 2024-12-04 | mort |
| `landwolf-on-avax` | Landwolf on AVAX | WOLF | ≈ 58 M$ | 2024-03-14 | mort |
| `macrohard` | MacroHard | MHRD | ≈ 58 M$ | 2025-08-14 | mort |
| `markkacy` | markkacy | KACY | ≈ 57 M$ | 2024-11-26 | mort |
| `tsotchke` | Tsotchke | TSOTCHKE | ≈ 57 M$ | 2024-12-28 | mort |
| `trust-the-process` | Trust The Process | TRUST | ≈ 56 M$ | 2024-12-18 | mort |
| `just-memecoin` | just memecoin | MEMECOIN | ≈ 55 M$ | 2025-07-25 | mort |
| `babybonk` | BabyBonk [OLD] | BABYBONK | ≈ 55 M$ | 2024-03-10 | copie ou ancienne version d'une carte; mort |
| `bozo-hybrid` | Bozo Benk | BOZO | ≈ 54 M$ | 2024-01-29 | mort |
| `aintivirus-2` | AIntivirus | AINTI | ≈ 54 M$ | 2025-01-23 | mort |
| `banana-for-scale` | Banana for Scale | BANANA | ≈ 54 M$ | 2024-11-15 | copie ou ancienne version d'une carte; mort |
| `elon` | Eloncoin | ELON | ≈ 53 M$ | 2024-06-04 | mort |
| `golazo-world` | Golazo.world | GOL | ≈ 53 M$ | 2024-05-21 | mort |
| `scottyai` | ScottyTheAi | SCOTTY | ≈ 53 M$ | 2024-03-26 | mort |
| `klaus` | KLAUS | KLAUS | ≈ 52 M$ | 2024-10-16 | mort |
| `enkryptedai` | EnKryptedAI | KRAI | ≈ 52 M$ | 2025-07-29 | mort |
| `biaoqing` | Biaoqing | BIAO | ≈ 51 M$ | 2024-06-19 | mort |
| `flovi-inu` | Flovi Inu | FLOVI | ≈ 51 M$ | 2024-04-08 | mort |
| `dinolfg` | DinoLFG | DINO | ≈ 51 M$ | 2023-05-07 | mort |
| `integrity-dao` | Integrity DAO | ID | ≈ 51 M$ | 2025-06-06 | nature à vérifier; mort |
| `crogecoin` | Crogecoin | CROGE | ≈ 51 M$ | 2022-04-07 | mort |
| `omega-2` | Omega | OMEGA | ≈ 50 M$ | 2024-11-22 | mort |
| `super-inu-force` | Super Inu Force | SIF | ≈ 50 M$ | 2026-10-06 | mort |
| `high-af` | High AF | ATH | ≈ 50 M$ | 2024-12-02 | mort |
| `super-iguana` | Super Iguana | SI | ≈ 50 M$ | 2026-10-04 | mort |
| `cute-cat-token` | Cute Cat Candle | CCC | ≈ 49 M$ | 2024-04-10 | mort |
| `pepe-bundle` | Pepe Bundle | PUNDLE | ≈ 49 M$ | 2025-08-01 | mort |
| `bucky-2` | Bucky | BUCKY | ≈ 49 M$ | 2025-08-06 | mort |
| `dogshit-2` | DOGSHIT | DOGSHIT | ≈ 49 M$ | 2025-09-14 | mort |
| `startup` | Startup | STARTUP | ≈ 49 M$ | 2025-07-02 | mort |
| `griffain-new-hedge-fund` | Griffain New Hedge Fund | CITADAIL | ≈ 49 M$ | 2025-01-08 | mort |
| `moss` | MOSS AI | MOSS | ≈ 49 M$ | 2025-01-03 | nature à vérifier; mort |
| `andy-on-sol` | Andy on SOL | ANDY | ≈ 48 M$ | 2024-03-14 | mort |
| `meme-trumpcoin` | Meme TrumpCoin | TRUMP | ≈ 48 M$ | 2025-01-20 | mort |
| `bobo` | Bobo | BOBO | ≈ 48 M$ | 2023-07-30 | copie ou ancienne version d'une carte; mort |
| `goats-2` | GOATS | GOATS | ≈ 48 M$ | 2024-12-05 | mort |
| `meme-moguls` | Meme Moguls | MGLS | ≈ 48 M$ | 2024-03-13 | mort |
| `sci-hub` | sci-hub | SCIHUB | ≈ 48 M$ | 2024-11-20 | mort |
| `harold` | Harold | HAROLD | ≈ 48 M$ | 2024-04-02 | copie ou ancienne version d'une carte; mort |
| `u` | U | U | ≈ 47 M$ | 2025-08-14 | mort |
| `tiger-shark` | Tiger Shark | TIGERSHARK | ≈ 47 M$ | 2025-05-28 | mort |
| `sage-universe` | Sage Universe | SAGE | ≈ 47 M$ | 2024-07-04 | mort |
| `spurdo-on-eth` | SPURDO ON ETH | SPURDO | ≈ 47 M$ | 2024-07-26 | mort |
| `meta-monopoly` | Meta Monopoly | MONOPOLY | ≈ 47 M$ | 2024-09-21 | mort |
| `culo` | CULO | CULO | ≈ 47 M$ | 2024-03-14 | mort |
| `schizo-terminal` | Mindscraft | MINDS | ≈ 46 M$ | 2025-01-12 | mort |
| `earl` | earl | EARL | ≈ 46 M$ | 2024-11-15 | mort |
| `fu` | FU | FU | ≈ 46 M$ | 2024-10-07 | mort |
| `bretter-brett` | Bretter Brett | BRETT | ≈ 46 M$ | 2024-06-12 | mort |
| `regent` | REGENT | REGENT | ≈ 46 M$ | 2025-01-24 | mort |
| `iq6900` | IQ6900 [OLD] | IQ | ≈ 46 M$ | 2025-01-07 | mort |
| `abster` | Abster | ABSTER | ≈ 46 M$ | 2025-08-09 | mort |
| `satozhi` | Satozhi | SATOZ | ≈ 46 M$ | 2021-05-09 | mort |
| `sonic-the-goat` | Sonic The Goat | GOAT | ≈ 46 M$ | 2024-05-07 | mort |
| `obi-pnut-kenobi` | Obi PNut Kenobi | OPK | ≈ 46 M$ | 2024-11-13 | mort |
| `ndq666` | NDQ666 | NDQ | ≈ 46 M$ | 2025-10-08 | mort |
| `hood-inu` | Hood Inu | HI | ≈ 45 M$ | 2026-10-05 | mort |
| `trillions` | Trillions | TRILLIONS | ≈ 45 M$ | 2025-09-27 | mort |
| `lifedog` | lifedog | LFDOG | ≈ 44 M$ | 2024-12-04 | mort |
| `dogecast` | Dogecast | DOGECAST | ≈ 44 M$ | 2025-01-15 | mort |
| `fat-choi` | fat choi | 发财 | ≈ 44 M$ | 2026-05-25 | mort |
| `balls-of-fate` | Balls of Fate | BOF | ≈ 44 M$ | 2024-09-21 | mort |
| `aiwithdaddyissues` | Aiwithdaddyissues | SHEGEN | ≈ 43 M$ | 2024-10-26 | mort |
| `bamboo-on-base` | Bamboo on Base | BAMBOO | ≈ 43 M$ | 2024-07-21 | mort |
| `wai-combinator-by-virtuals` | WAI Combinator by Virtuals | WAI | ≈ 43 M$ | 2025-01-02 | mort |
| `elon-trump-fart` | Elon Trump Fart | ETF500 | ≈ 43 M$ | 2025-01-26 | mort |
| `petunia` | Petunia | PETUNIA | ≈ 43 M$ | 2024-11-14 |  |
| `chili` | CHILI | CHILI | ≈ 42 M$ | 2023-01-06 | mort |
| `fatcoin-2` | FATCOIN | FATCOIN | ≈ 42 M$ | 2026-09-04 |  |
| `ai16zeliza` | ai16zeliza | ELIZA | ≈ 42 M$ | 2024-11-19 | mort |
| `crazyfootball-token` | CrazyFootball token | FOOTBALL | ≈ 42 M$ | 2025-12-06 | mort |
| `mimany` | MIMANY | MIMANY | ≈ 42 M$ | 2024-04-09 | mort |
| `believe-in-something-2` | believe in something | DTF | ≈ 42 M$ | 2024-12-03 | mort |
| `bop-cat` | Bop Cat | BOP | ≈ 42 M$ | 2024-11-18 | mort |
| `neversol` | neversol | NEVER | ≈ 41 M$ | 2024-03-14 | mort |
| `apes-2` | APES [OLD] | APES | ≈ 41 M$ | 2024-08-29 | copie ou ancienne version d'une carte; mort |
| `stonks-on-eth` | Stonks on ETH | STONKS | ≈ 41 M$ | 2024-06-12 | mort |
| `drpepe-ai` | DrPepe.ai | BRYAN | ≈ 41 M$ | 2025-01-03 | nature à vérifier; mort |
| `kokok-the-roach` | KoKoK The Roach | KOKOK | ≈ 41 M$ | 2025-06-05 | mort |
| `3lon` | 3lon | 3LON | ≈ 40 M$ | 2026-06-19 | mort |
| `kolin-2` | Kolin | KOLIN | ≈ 40 M$ | 2025-01-15 | mort |
| `rocky-the-rock` | Rocky | ROCKY | ≈ 40 M$ | 2024-07-11 | mort |
| `suwi` | suwi | SUWI | ≈ 40 M$ | 2024-11-13 | mort |
| `seamania` | SEAMANIA | SEAMANIA | ≈ 39 M$ | 2025-01-23 | mort |
| `agent-cat` | Agent Cat | AGENTCAT | ≈ 39 M$ | 2026-10-05 | nature à vérifier; mort |
| `cat-terminal` | CAT Terminal | CAT | ≈ 39 M$ | 2025-10-06 | mort |
| `blinkdotfun` | blinkdotfun | BLINK | ≈ 39 M$ | 2024-12-16 | mort |
| `american-shiba` | American Shiba | USHIBA | ≈ 39 M$ | 2021-06-04 | mort |
| `abi` | Abi | ABI | ≈ 39 M$ | 2024-11-13 | mort |
| `a-gently-used-2001-honda` | A Gently Used 2001 Honda | USEDCAR | ≈ 39 M$ | 2023-12-29 | mort |
| `wap` | WAP | WAP | ≈ 39 M$ | 2024-10-12 | mort |
| `agent-s` | Agent S | S | ≈ 39 M$ | 2025-01-08 | nature à vérifier; mort |
| `candle-tv` | Candle TV | CANDLE | ≈ 38 M$ | 2025-05-29 | mort |
| `centience` | Centience | CENTS | ≈ 38 M$ | 2024-11-23 | mort |
| `baby-shark` | Baby Shark | SHARK | ≈ 38 M$ | 2021-06-03 | mort |
| `jam-cat` | jam cat | JAM | ≈ 38 M$ | 2024-11-14 | mort |
| `max-on-eth` | Max on ETH | MAXETH | ≈ 38 M$ | 2024-12-11 | mort |
| `bitcat-3` | Bitcat | BITCAT | ≈ 38 M$ | 2024-11-16 | mort |
| `flowerai` | FlowerAI | FLOWER | ≈ 37 M$ | 2024-11-23 | mort |
| `black-unicorn-corp` | Black Unicorn Corp. | MOON | ≈ 37 M$ | 2024-12-18 | mort |
| `booze` | Booze | BOOZE | ≈ 37 M$ | 2026-09-05 | mort |
| `uni` | Uni | UNI | ≈ 37 M$ | 2024-11-14 | mort |
| `satoshitcoin` | SatoshitCoin | SATOSHIT | ≈ 37 M$ | 2025-08-20 | mort |
| `based-bunny` | Based Bunny | BUNNY | ≈ 37 M$ | 2024-04-25 | mort |
| `effective-accelerationism` | Effective accelerationism | E/ACC | ≈ 37 M$ | 2024-11-11 | mort |
| `meme-anarchic-numismatic-asset` | Meme Anarchic Numismatic Asset | MANA | ≈ 37 M$ | 2024-12-15 | mort |
| `super-inu-accelerationism` | Super Inu Accelerationism | SI/ACC | ≈ 37 M$ | 2026-09-28 | mort |
| `daram` | Daram | DARAM | ≈ 36 M$ | 2024-10-19 | mort |
| `littlemanyu` | littlemanyu | MANYU | ≈ 36 M$ | 2024-10-07 | mort |
| `flork-cto` | FLORK CTO | FLORK | ≈ 36 M$ | 2025-01-07 | mort |
| `ribbit-meme` | Ribbit Meme | RIBBIT | ≈ 36 M$ | 2023-05-06 | mort |
| `mist-2` | MIST | 霞 | ≈ 36 M$ | 2024-11-13 | mort |
| `pepesol` | PepeSol | PEPE | ≈ 36 M$ | 2024-03-09 | mort |
| `yellow-pepe-2` | Yellow Pepe | YEPE | ≈ 36 M$ | 2025-10-08 | mort |
| `magnetix` | Magnetix | MAG | ≈ 36 M$ | 2025-03-23 | mort |
| `maya` | Maya | MAYA | ≈ 36 M$ | 2024-11-14 | mort |
| `space-troll` | SPACE TROLL | SPCTROLL | ≈ 36 M$ | 2026-05-17 | mort |
| `69420` | 69420 | 69420 | ≈ 36 M$ | 2025-07-21 | mort |
| `elon-goat` | Elon GOAT | EGT | ≈ 35 M$ | 2022-02-12 | mort |
| `gtf` | GTF | GTF | ≈ 35 M$ | 2025-11-08 | mort |
| `charles-the-chad` | Charles the Chad | CHAD | ≈ 35 M$ | 2024-12-06 | mort |
| `rato-the-rat` | Rato The Rat | RATO | ≈ 35 M$ | 2025-05-11 | mort |
| `don-t-buy-inu` | Don't Buy Inu | DBI | ≈ 35 M$ | 2023-03-09 | mort |
| `4` | 4 | FOUR | ≈ 35 M$ | 2024-08-23 | copie ou ancienne version d'une carte; mort |
| `monkey-taken-by-police` | Monkey Taken By Police | JORGIE | ≈ 35 M$ | 2024-11-14 | mort |
| `ordinal-doge` | Ordinal Doge | ODOGE | ≈ 35 M$ | 2023-03-06 | mort |
| `baby-tiger` | Baby Tiger | $BBT | ≈ 35 M$ | 2024-11-23 | mort |
| `virgen` | Virgen | VIRGEN | ≈ 34 M$ | 2025-05-28 | mort |
| `pajamas-cat` | Pajamas Cat | PAJAMAS | ≈ 34 M$ | 2024-05-30 | mort |
| `conan-2` | Conan | CONAN | ≈ 34 M$ | 2024-04-23 | mort |
| `aintivirus` | AIntivirus | AINTI | ≈ 34 M$ | 2025-05-01 | mort |
| `debtcoin` | DebtCoin | DEBT | ≈ 34 M$ | 2025-07-29 | mort |
| `sompi` | Sompi | SOMPI | ≈ 34 M$ | 2026-04-21 | mort |
| `xing-xing` | Xing Xing | XING | ≈ 34 M$ | 2024-11-22 | mort |
| `zuzalu-inu` | Zuzalu Inu | ZUZALU | ≈ 34 M$ | 2024-01-16 | mort |
| `shiva-inu` | Shiva Inu | SHIV | ≈ 34 M$ | 2024-03-28 | mort |
| `mumu` | Mumu | MUMU | ≈ 34 M$ | 2024-04-01 | mort |
| `sympson-ai` | Sympson by Virtuals | $SYMP | ≈ 34 M$ | 2025-01-16 | mort |
| `mongy` | Mongy | MONGY | ≈ 33 M$ | 2024-07-19 | mort |
| `yak` | YAK | YAK | ≈ 33 M$ | 2024-03-15 | mort |
| `avarik-saga` | Avarik Saga | AVRK | ≈ 33 M$ | 2025-01-07 | mort |
| `pockemy` | Pockemy | PKM | ≈ 33 M$ | 2025-09-29 | mort |
| `identity-md-6900` | Identity.md 6900 | IMD6900 | ≈ 33 M$ | 2026-10-12 | mort |
| `horsecoin-2` | HorseCoin | 马币 | ≈ 33 M$ | 2026-04-07 | mort |
| `hana` | Hana | HANA | ≈ 33 M$ | 2024-09-30 | mort |
| `united-states-water-reserve` | United States Water Reserve | USWR | ≈ 33 M$ | 2026-07-25 | mort |
| `red-pill-2` | Red Pill | RPILL | ≈ 33 M$ | 2024-01-01 | mort |
| `yousim` | YouSim | YOUSIM | ≈ 33 M$ | 2024-11-14 | mort |
| `sealwifhat` | sealwifhat | SI | ≈ 32 M$ | 2024-03-14 | mort |
| `tate-terminal` | Tate Terminal | TATE | ≈ 32 M$ | 2024-10-29 | mort |
| `maga-vp` | MAGA VP | MVP | ≈ 32 M$ | 2024-05-17 | mort |
| `limbo` | LIMBO | LIMBO | ≈ 32 M$ | 2025-01-26 | mort |
| `lucky-dog` | Lucky Dog | LUCKY | ≈ 32 M$ | 2024-11-11 | mort |
| `make-eth-great-again` | Make ETH Great Again | MEGA | ≈ 32 M$ | 2024-06-10 | mort |
| `doge-pepe-3` | Doge Pepe | DOPE | ≈ 32 M$ | 2026-10-18 | copie ou ancienne version d'une carte; mort |
| `thales-ai` | Thales AI | THALES | ≈ 31 M$ | 2025-01-10 | nature à vérifier; mort |
| `pumpkin-4` | Pumpkin | PKIN | ≈ 31 M$ | 2025-02-10 | mort |
| `kakaxa` | Kakaxa | KAKAXA | ≈ 31 M$ | 2024-04-25 | mort |
| `trump-derangement-syndrome` | Trump Derangement Syndrome | TDS | ≈ 31 M$ | 2024-11-11 | mort |
| `fur-nancial-advisor` | Fur-nancial advisor | FUR | ≈ 31 M$ | 2024-11-18 | mort |
| `principals-network` | Principals Network | PNET | ≈ 31 M$ | 2024-12-15 | nature à vérifier; mort |
| `blinks-gg` | Blinks.gg | BGG1 | ≈ 31 M$ | 2024-12-12 | mort |
| `terry-in-the-trenches` | Terry In The Trenches | TERRY | ≈ 31 M$ | 2024-11-25 | mort |
| `bunker-mode` | Bunker Mode | BUNKER | ≈ 31 M$ | 2026-10-12 | mort |
| `christ-is-king` | Christ Is King | CIK | ≈ 31 M$ | 2025-05-21 | mort |
| `quantum-inu` | Quantum Inu | QI | ≈ 31 M$ | 2026-10-11 | mort |
| `satoshi-ai-agent-by-virtuals` | Satoshi AI agent by Virtuals | SAINT | ≈ 31 M$ | 2024-12-03 | nature à vérifier; mort |
| `frox` | Frox | FROX | ≈ 30 M$ | 2024-12-20 | mort |
| `cloudyheart` | cloudyheart | CLOUDY | ≈ 30 M$ | 2025-02-03 | mort |
| `vibe-cat-2` | Vibe Cat | VIBE | ≈ 30 M$ | 2024-11-20 | mort |
| `dogc` | DOGC | DOGC | ≈ 30 M$ | 2024-12-02 | mort |
| `silly-goose` | Silly Goose | GOO | ≈ 30 M$ | 2024-03-16 | mort |
| `vectorchat-ai` | VectorChat.ai | CHAT | ≈ 30 M$ | 2025-01-20 | nature à vérifier; mort |
| `marvin-inu` | Marvin Inu | MARVIN | ≈ 30 M$ | 2022-04-03 | mort |
| `hyperpigmentation` | Hyperpigmentation | $HYPER | ≈ 30 M$ | 2025-07-19 | mort |
| `rizo` | Rizo | RIZO | ≈ 30 M$ | 2024-03-24 | mort |
| `mowcat` | MowCat | MOW | ≈ 30 M$ | 2026-08-18 |  |
| `time` | TIME | TIME | ≈ 30 M$ | 2024-07-27 | mort |
| `hulvin` | HULVIN | HULVIN | ≈ 30 M$ | 2024-04-16 | mort |
| `flokifork` | FlokiFork | FORK | ≈ 30 M$ | 2024-03-08 | mort |
| `landwolf-2` | Landwolf | WOLF | ≈ 29 M$ | 2024-03-11 | copie ou ancienne version d'une carte; mort |
| `buttcoin-4` | Buttcoin | BUTTCOIN | ≈ 29 M$ | 2025-04-11 | copie ou ancienne version d'une carte |
| `soulguy` | SOULGUY | SOULGUY | ≈ 29 M$ | 2026-01-29 | mort |
| `rocky-the-dog` | Rocky the dog | ROCKY | ≈ 29 M$ | 2024-01-13 | mort |
| `beenz` | BEENZ | BEENZ | ≈ 29 M$ | 2025-01-28 | mort |
| `trust-me-bros-by-virtuals` | $TRUST ME BROs by Virtuals | TRUST | ≈ 29 M$ | 2025-01-04 | mort |
| `zeus-3` | ZEUS | ZEUS | ≈ 29 M$ | 2025-01-11 | mort |
| `keke-terminal` | KEKE Terminal | KEKE | ≈ 29 M$ | 2024-12-30 | mort |
| `magic-internet-cash` | Magic Internet Cash | MIC | ≈ 29 M$ | 2024-03-06 | mort |
| `sonic-snipe-bot` | Sonic Snipe Bot | SONIC | ≈ 29 M$ | 2024-12-13 | mort |
| `slop` | Slop | SLOP | ≈ 29 M$ | 2024-10-23 | mort |
| `ava-chiang-mai-night-safari-ava` | AVA Chiang Mai Night Safari (AVA) | AVA | ≈ 29 M$ | 2024-11-27 | mort |
| `meow-meow-meow-meow` | meow meow meow meow | MEOW | ≈ 29 M$ | 2024-12-19 | mort |
| `kangal` | Kangal | KANGAL | ≈ 28 M$ | 2021-04-20 | mort |
| `unicorn-3` | Unicorn [OLD] | UWU | ≈ 28 M$ | 2024-08-13 | mort |
| `winter-arc` | Winter Arc | WINTER | ≈ 28 M$ | 2024-11-20 | mort |
| `lets-get-this-bread` | Lets Get This Bread | LGTB | ≈ 28 M$ | 2024-12-15 | mort |
| `catownkimono` | catownkimono | COK | ≈ 28 M$ | 2024-06-10 | mort |
| `moonwolf-io` | moonwolf.io | WOLF | ≈ 28 M$ | 2024-07-22 | mort |
| `weird-medieval-memes` | Weird Medieval Memes | WMM | ≈ 28 M$ | 2024-11-14 | mort |
| `moe-4` | MOE | MOE | ≈ 28 M$ | 2025-01-06 | mort |
| `jak` | JAK | JAK | ≈ 28 M$ | 2024-11-28 | mort |
| `sheep-wif-hat` | Sheep Wif Hat | SWIF | ≈ 28 M$ | 2025-08-12 | mort |
| `agentaigo` | CLAWLETT | CLAWLETT | ≈ 28 M$ | 2025-01-02 | mort |
| `baby-samo-coin` | Baby Samo Coin | BABY | ≈ 28 M$ | 2021-11-13 | mort |
| `monkeyhaircut` | monkeyhaircut | MONK | ≈ 28 M$ | 2024-05-09 | mort |
| `melon-dog` | Melon Dog | MELON | ≈ 28 M$ | 2024-03-13 | mort |
| `super-cat` | Super Cat | SC | ≈ 28 M$ | 2026-10-02 | mort |
| `bullballs-coin` | Bullballs Coin | BULLBALLS | ≈ 27 M$ | 2026-08-20 | mort |
| `soldoge` | SolDoge | SDOGE | ≈ 27 M$ | 2021-11-01 | mort |
| `doge-pepe` | Doge Pepe | DOPE | ≈ 27 M$ | 2026-10-14 | copie ou ancienne version d'une carte; mort |
| `slopfather` | Slopfather | FATHA | ≈ 27 M$ | 2024-12-01 | mort |
| `doge` | @DOGE | @DOGE | ≈ 27 M$ | 2024-11-15 | mort |
| `the-professor` | The Professor | LAB | ≈ 27 M$ | 2024-06-11 | mort |
| `doggo-3` | Doggo | DOGGO | ≈ 27 M$ | 2024-10-02 | mort |
| `buu` | BUU | BUU | ≈ 27 M$ | 2024-11-12 | mort |
| `baked` | Baked | BAKED | ≈ 27 M$ | 2024-09-30 | mort |
| `pandu-pandas` | Pandu Pandas [OLD] | PANDU | ≈ 27 M$ | 2025-10-05 | mort |
| `glp1` | GLP1 | GLP1 | ≈ 27 M$ | 2024-11-24 | mort |
| `super-inu` | Super Inu | SI | ≈ 27 M$ | 2026-09-26 | copie ou ancienne version d'une carte; mort |
| `kwantxbt` | kwantxbt | KWANT | ≈ 27 M$ | 2025-01-02 | mort |
| `usacoin` | USAcoin | USACOIN | ≈ 27 M$ | 2024-12-21 | mort |
| `vibing-cat` | Vibing Cat | VCAT | ≈ 26 M$ | 2024-03-14 | mort |
| `pump` | Pump | PUMP | ≈ 26 M$ | 2024-03-05 | mort |
| `based` | BASED | BASED | ≈ 26 M$ | 2024-11-13 | mort |
| `arc-chan` | Arc Chan | ARCHAN | ≈ 26 M$ | 2026-09-27 | mort |
| `moon-doge-coin` | Moon Doge Coin | MOONDOGECOIN | ≈ 26 M$ | 2026-07-31 | mort |
| `zorro` | Zorro | ZORRO | ≈ 26 M$ | 2024-03-31 | mort |
| `marvin-inu-2` | Marvin Inu | MARVIN | ≈ 26 M$ | 2024-11-17 | mort |
| `jaihoz` | Jaihoz by Virtuals | JAIHOZ | ≈ 26 M$ | 2025-01-10 | mort |
| `gpu-ai-rich` | GPU ai Rich | RICH | ≈ 25 M$ | 2025-01-09 | nature à vérifier; mort |
| `psyopcoin` | PsyopCoin | PSYOP | ≈ 25 M$ | 2025-07-21 | mort |
| `zoomer-sol` | Zoomer | ZOOMER | ≈ 25 M$ | 2024-07-26 | mort |
| `end-federal-reserve` | End Federal Reserve | EFR | ≈ 25 M$ | 2024-11-23 | mort |
| `noot-noot` | Noot Noot | NOOT | ≈ 25 M$ | 2025-03-28 | mort |
| `lea-ai` | LEA AI | LEA | ≈ 25 M$ | 2025-01-25 | nature à vérifier; mort |
| `taylor-swift-s-cat` | Taylor Swift's Cat Benji | BENJI | ≈ 25 M$ | 2024-03-09 | mort |
| `world-collective-oil-reserve` | World Collective Oil Reserve | WCOR | ≈ 25 M$ | 2026-05-19 | mort |
| `andy-2` | Andy | ANDY | ≈ 25 M$ | 2024-06-30 | copie ou ancienne version d'une carte; mort |
| `ligma-node` | Ligma Node | LIGMA | ≈ 25 M$ | 2024-04-03 | mort |
| `sbrsol` | Strategic Bitcoin Reserve | SBR | ≈ 25 M$ | 2025-01-19 | mort |
| `inu-wif-sword` | inu wif sword | SWORDINU | ≈ 25 M$ | 2026-10-07 | mort |
| `goatindex-ai` | GoatIndex.ai | AIAI | ≈ 25 M$ | 2025-01-23 | nature à vérifier; mort |
| `eye-earn` | Smilek [OLD] | SMILEK | ≈ 25 M$ | 2024-04-17 | mort |
| `beercoin2` | Beercoin 2 | BEER2 | ≈ 25 M$ | 2025-05-30 | mort |
| `emotional-support-alligator` | Emotional Support Alligator | WALLY | ≈ 25 M$ | 2024-11-25 | mort |
| `real-fast` | real fast | SPEED | ≈ 25 M$ | 2024-05-29 | mort |
| `pepe-the-king-prawn` | Pepe the King Prawn | PRAWN | ≈ 25 M$ | 2024-12-08 | mort |
| `bazinga-2` | Bazinga | BAZINGA | ≈ 25 M$ | 2024-06-02 | mort |
| `defiant-2` | Defiant | DEFIANT | ≈ 25 M$ | 2025-04-17 | nature à vérifier; mort |
| `elon-s-space-cat` | Elon's Space Cat | CATALORIAN | ≈ 25 M$ | 2026-08-24 | mort |
| `pelfort` | PELFORT | PELF | ≈ 25 M$ | 2024-03-11 | mort |
| `puffy` | Puffy | PUFFY | ≈ 25 M$ | 2024-10-11 | mort |
| `peanie` | peanie | PEANIE | ≈ 25 M$ | 2024-05-20 | mort |
| `stream-until-100m-mc` | Stream until 100M MC | LIVE | ≈ 25 M$ | 2024-11-22 | mort |
| `le-chonk` | Le Chonk | CHONK | ≈ 25 M$ | 2026-10-06 | mort |
| `wall-street-baby-on-solana` | Wall Street Baby On Solana | WSB | ≈ 24 M$ | 2024-04-12 | mort |
| `rawr` | Rawr | XD | ≈ 24 M$ | 2024-10-14 | mort |
| `pulse-inu-2` | Pulse Inu | PINU | ≈ 24 M$ | 2026-08-24 | mort |
| `67coin` | 67COIN | 67 | ≈ 24 M$ | 2025-09-09 | mort |
| `urmom-3` | urmom | URMOM | ≈ 24 M$ | 2026-08-24 | mort |
| `snake-wif-hat` | Snake wif Hat | SSSSS | ≈ 24 M$ | 2024-11-26 | mort |
| `outlaw-crypto-games` | OUTLAW Crypto Games | OUTLAW | ≈ 24 M$ | 2025-09-12 | nature à vérifier; mort |
| `hyperskids` | $HYPERSKIDS | HYPERSKIDS | ≈ 24 M$ | 2025-02-22 | mort |
| `jeje` | JEJE | JJ | ≈ 24 M$ | 2024-05-30 | mort |
| `robot-2` | ROBOT | ROBOT | ≈ 24 M$ | 2025-05-24 | mort |
| `fomo-3d` | FOMO 3D | FOMO3D.FUN | ≈ 24 M$ | 2024-12-31 | mort |
| `white-boy-summer` | White Boy Summer | WBS | ≈ 24 M$ | 2024-05-22 | mort |
| `ducky` | Ducky [OLD] | DUCKY | ≈ 24 M$ | 2024-11-15 | mort |
| `fottie` | Fottie | FOTTIE | ≈ 24 M$ | 2024-03-09 | mort |
| `poop` | Poop | POOP | ≈ 24 M$ | 2025-08-14 | mort |
| `sora-ai` | Sora AI | SORA | ≈ 24 M$ | 2024-02-18 | nature à vérifier; mort |
| `erha` | Erha | 二哈 | ≈ 23 M$ | 2025-08-26 | mort |
| `andy70b` | ANDY70B | ANDY70B | ≈ 23 M$ | 2024-12-21 | mort |
| `rex-3` | Rex | REX | ≈ 23 M$ | 2024-11-17 | mort |
| `claudia-4` | Claudia | CLAUDIA | ≈ 23 M$ | 2026-10-13 | copie ou ancienne version d'une carte; mort |
| `cat-token` | Mooncat CAT | CAT | ≈ 23 M$ | 2021-11-01 | mort |
| `ropirito` | Ropirito | ROPIRITO | ≈ 23 M$ | 2024-11-21 | mort |
| `bolt-on-base` | BOLT on Base | BOLT | ≈ 23 M$ | 2024-06-09 | mort |
| `jungledoge` | JungleDoge | JUNGLE | ≈ 23 M$ | 2024-05-29 | mort |
| `shrub-2` | Shrub | $SHRUB | ≈ 23 M$ | 2024-11-13 | copie ou ancienne version d'une carte; mort |
| `lily-s-coin` | Lily's Coin | LILY | ≈ 23 M$ | 2024-11-12 | mort |
| `latina-language-model` | Latina Language Model | LLM | ≈ 23 M$ | 2025-08-25 | mort |
| `arie-the-sealion` | Arie The Sealion | ARIE | ≈ 23 M$ | 2024-11-19 | mort |
| `maga-pepe-2` | MAGA Pepe | MAPE | ≈ 23 M$ | 2024-07-17 | mort |
| `degenerative-sitcom` | degenerative SITCOM | $SITCOM | ≈ 23 M$ | 2024-12-01 | mort |
| `xenopus-laevis` | Xenopus laevis | XENO | ≈ 23 M$ | 2024-12-30 | mort |
| `hungarian-vizsla-inu` | Hungarian Vizsla Inu | HVI | ≈ 23 M$ | 2021-08-11 | mort |
| `manlet` | manlet | MANLET | ≈ 23 M$ | 2026-07-04 | mort |
| `larp-detective-agency` | Larp Detective Agency | $AGENCY | ≈ 23 M$ | 2025-01-02 | mort |
| `curtis` | Curtis | CURTIS | ≈ 23 M$ | 2024-10-24 | mort |
| `won-chang` | Won Chang | USDWON | ≈ 23 M$ | 2025-09-17 | mort |
| `koto-2` | Koto | KOTO | ≈ 22 M$ | 2024-11-14 | mort |
| `r-snoofi` | r/snoofi | R/SNOOFI | ≈ 22 M$ | 2024-11-15 | mort |
| `1-squirrel` | OG Peanut | PEANUT | ≈ 22 M$ | 2024-11-25 | mort |
| `blobana-pet` | Blobana pet | BLOB | ≈ 22 M$ | 2024-11-24 | mort |
| `gou` | Gou | GOU | ≈ 22 M$ | 2024-09-25 | mort |
| `altai-the-tiger` | Altai the Tiger | ALTAI | ≈ 22 M$ | 2026-10-15 | mort |
| `no-crying-in-the-casino` | no crying in the casino | CASINO | ≈ 22 M$ | 2026-10-15 | mort |
| `h2w6gm6jz` | h2w6gm6jz | H2W6GM6JZ | ≈ 22 M$ | 2024-12-20 | mort |
| `blaze` | Blaze | BLAZE | ≈ 22 M$ | 2025-07-01 | mort |
| `babylong` | BABYLONG | $BABYLONG | ≈ 22 M$ | 2024-05-17 | mort |
| `baby-wen` | Baby Wen | BWEN | ≈ 22 M$ | 2024-11-05 | mort |
| `hot-doge-2` | Hot Doge | HOTDOGE | ≈ 22 M$ | 2024-12-13 | mort |
| `goodboy` | GoodBoy | GOODBOY | ≈ 22 M$ | 2024-12-22 | mort |
| `long-5` | 龙Long | 龙LONG | ≈ 22 M$ | 2025-10-13 | mort |
| `super-shiba-2` | Super Shiba | SS | ≈ 22 M$ | 2026-10-06 | mort |
| `naitzsche` | Naitzsche | NAI | ≈ 22 M$ | 2024-12-15 | mort |
| `america-party` | America Party | AP | ≈ 22 M$ | 2025-07-05 | copie ou ancienne version d'une carte; mort |
| `hex-com-diamond` | HEX.COM DIAMOND | DMND | ≈ 22 M$ | 2026-08-21 | mort |
| `sword-inu` | Sword Inu | SI | ≈ 21 M$ | 2026-10-14 | mort |
| `bepe` | BEPE | BEPE | ≈ 21 M$ | 2024-12-12 | mort |
| `belief` | BELIEF | BELIEF | ≈ 21 M$ | 2026-04-22 | mort |
| `american-ai-fund` | American AI Fund | AAIF | ≈ 21 M$ | 2026-07-25 | nature à vérifier; mort |
| `plebz` | Plebz | PLEB | ≈ 21 M$ | 2024-03-31 | mort |
| `cheeseball` | Cheeseball | CB | ≈ 21 M$ | 2024-10-10 | mort |
| `devin-on-solana` | Devin | DEVIN | ≈ 21 M$ | 2024-06-03 | mort |
| `cat-wif-hood` | cat wif hood | HOODCAT | ≈ 21 M$ | 2026-10-11 | mort |
| `useless-stonk` | USELESS STONK | STONKLESS | ≈ 21 M$ | 2026-09-09 | mort |
| `vorta-markets` | Vorta Markets | VORTA | ≈ 21 M$ | 2026-10-10 | mort |
| `baby-pepe-2` | Baby Pepe | BABYPEPE | ≈ 21 M$ | 2024-06-04 | mort |
| `brett` | Brett | BRETT | ≈ 21 M$ | 2024-03-10 | copie ou ancienne version d'une carte; mort |
| `solcat` | SOLCAT | SOLCAT | ≈ 21 M$ | 2024-11-26 | mort |
| `drip` | DRIP | $DRIP | ≈ 21 M$ | 2024-11-09 | mort |
| `kira-3` | KIRA | KIRA | ≈ 21 M$ | 2024-11-19 | mort |
| `dogwifnohat` | DogWifNoHat | NOHAT | ≈ 21 M$ | 2024-05-13 | mort |
| `happi-cat` | happi cat | HAPPI | ≈ 20 M$ | 2024-05-07 | mort |
| `cat-girl` | cat girl | CATGF | ≈ 20 M$ | 2024-10-23 | mort |
| `stix` | STIX | STIX | ≈ 20 M$ | 2024-12-16 | mort |
| `trumpius-maximus` | Trumpius Maximus | TRUMPIUS | ≈ 20 M$ | 2025-01-03 | mort |
| `bozo-collective` | Bozo Collective | BOZO | ≈ 20 M$ | 2024-03-18 | mort |
| `moin-2` | meme + coin = | MOIN | ≈ 20 M$ | 2026-09-28 | mort |
| `jerry-the-turtle-by-matt-furie` | Jerry The Turtle By Matt Furie | JYAI | ≈ 20 M$ | 2025-08-19 |  |
| `ai-inu` | AI INU | AIINU | ≈ 20 M$ | 2024-06-05 | nature à vérifier; mort |
| `dodo-2` | DODO | DODO | ≈ 20 M$ | 2024-04-01 | mort |
| `flat-earth` | Flat Earth | FLAT | ≈ 20 M$ | 2026-08-01 | mort |
| `size` | SIZE | SIZE | ≈ 20 M$ | 2024-11-28 | mort |
| `go-fu-k-yourself` | go fu*k yourself. | GFY | ≈ 20 M$ | 2023-12-03 | mort |
| `coby` | coby | COBY | ≈ 20 M$ | 2024-11-11 | mort |
| `cupsey` | CUPSEY [OLD] | CUPSEY | ≈ 20 M$ | 2024-11-15 | mort |
| `tongue-cat` | Tongue Cat | LUIS | ≈ 20 M$ | 2024-04-07 | mort |
| `strategic-oil-supply` | Strategic Oil Supply | SOS | ≈ 20 M$ | 2026-03-10 | mort |
| `kekius-maximus-2` | Kekius Maximus | KM | ≈ 20 M$ | 2024-12-31 | copie ou ancienne version d'une carte; mort |
| `fungi` | Fungi | FUNGI | ≈ 20 M$ | 2024-04-05 | mort |
| `mechafolio` | MECHAFOLIO | FOLIO | ≈ 20 M$ | 2026-10-17 | mort |
| `commander-vrax-4` | Commander Vrax | VRAX | ≈ 20 M$ | 2026-10-16 | copie ou ancienne version d'une carte; mort |
| `pepedex` | Pepedex | PPDEX | ≈ 20 M$ | 2021-03-06 | mort |
| `reverse-unit-bias` | Reverse Unit Bias | RUB | ≈ 20 M$ | 2025-09-15 | mort |
| `bitcoin-inu` | Bitcoin Inu | BTCINU | ≈ 20 M$ | 2024-01-26 | mort |
| `baby-cali` | Baby Cali | BABYCALI | ≈ 20 M$ | 2026-09-28 | mort |
| `akio` | Akio | AKIO | ≈ 20 M$ | 2025-04-21 | mort |
| `percy-verence` | Percy Verence | PERCY | ≈ 20 M$ | 2025-01-07 | mort |
| `bitfloki` | bitFloki | BFLOKI | ≈ 20 M$ | 2024-04-11 | mort |
| `aurora-terminal` | Aurora | AURORA | ≈ 19 M$ | 2024-11-18 | mort |
| `pillzumi` | Pillzumi | PILLZUMI | ≈ 19 M$ | 2024-12-16 | mort |
| `cat-wif-sword-3` | cat wif sword | SWORDCAT | ≈ 19 M$ | 2026-10-09 | copie ou ancienne version d'une carte; mort |
| `kaka` | KAKA | KAKA | ≈ 19 M$ | 2025-05-25 | mort |
| `print-protocol` | Print Protocol | PRINT | ≈ 19 M$ | 2024-01-31 | nature à vérifier; mort |
| `dogpad-finance` | DogPad Finance | DOGPAD | ≈ 19 M$ | 2023-03-04 | nature à vérifier; mort |
| `believe-in-something` | Believe In Something | BIS | ≈ 19 M$ | 2024-10-14 | mort |
| `lanlan-cat` | LanLan Cat | LANLAN | ≈ 19 M$ | 2025-05-27 | mort |
| `jackpot-on-solana` | Jackpot on Solana | JACKPOT | ≈ 19 M$ | 2024-07-21 | mort |
| `apewifhat` | ApeWifHat | APEWIFHAT | ≈ 19 M$ | 2024-03-15 | mort |
| `ponk` | Ponk | PONK | ≈ 19 M$ | 2023-12-17 | mort |
| `smol-bun` | Smol Bun | BUN | ≈ 19 M$ | 2026-09-09 | mort |
| `poopcoin-poop` | Poopcoin | POOP | ≈ 19 M$ | 2024-03-31 | mort |
| `degenerator-project` | Degenerator Project | GNRT | ≈ 19 M$ | 2025-01-08 | mort |
| `urmom-2` | urmom | URMOM | ≈ 19 M$ | 2025-05-07 | mort |
| `my-dog-is-the-dev` | MY DOG IS THE DEV | DEV | ≈ 19 M$ | 2024-09-13 | mort |
| `dividend-hound` | Dividend Hound | HOUND | ≈ 19 M$ | 2026-10-13 | mort |
| `pedro-the-raccoon` | Pedro the Raccoon | PEDRO | ≈ 19 M$ | 2024-05-07 | mort |
| `goblincoin` | GoblinCoin | GOBLIN | ≈ 19 M$ | 2026-05-11 | mort |
| `noodle` | Noodle | NOODLE | ≈ 19 M$ | 2025-05-13 | mort |
| `aicrostrategy` | AicroStrategy [Old] | AISTR | ≈ 19 M$ | 2024-12-30 | mort |
| `asteroid` | ASTEROID | ASTEROID | ≈ 19 M$ | 2026-05-13 | mort |
| `chuan-pu` | Chuan Pu | CHUANPU | ≈ 19 M$ | 2024-06-20 | mort |
| `valentine-grok-companion` | Valentine Grok Companion | VALENTINE | ≈ 18 M$ | 2025-07-17 | mort |
| `buy-the-hat` | BUY THE HAT | BTH | ≈ 18 M$ | 2025-08-09 | mort |
| `soylanamanletcaptainz` | SoylanaManletCaptainZ | ANSEM | ≈ 18 M$ | 2024-03-31 | mort |
| `yotoshi` | Yotoshi | YOTO | ≈ 18 M$ | 2023-12-25 | mort |
| `the-theory-of-gravity` | Theory Of Gravity | THOG | ≈ 18 M$ | 2024-04-08 | mort |
| `doodipals` | DOODiPALS | DOODI | ≈ 18 M$ | 2025-10-02 | mort |
| `nothing-4` | Nothing | VOID | ≈ 18 M$ | 2024-12-04 | mort |
| `boblles` | Boblles | BOBLS | ≈ 18 M$ | 2024-12-03 | mort |
| `trump-47` | TRUMP 47 | 47 | ≈ 18 M$ | 2024-10-29 | mort |
| `yeti-2` | YETI | YETI | ≈ 18 M$ | 2025-06-30 | mort |
| `dogei` | Dogei | DOGEI | ≈ 18 M$ | 2024-12-03 | mort |
| `tobi` | tobi | TOBI | ≈ 18 M$ | 2024-11-13 | mort |
| `bucky` | Bucky | BUCKY | ≈ 18 M$ | 2024-06-29 | mort |
| `rudi` | rudi | RUDI | ≈ 18 M$ | 2025-07-16 | mort |
| `bird-dog-on-sol` | Bird Dog on SOL | BIRDDOG | ≈ 18 M$ | 2024-06-21 | mort |
| `kai-ken` | Kai Ken | KAI | ≈ 18 M$ | 2024-06-21 | mort |
| `chinese-doge-wow` | Chinese Doge Wow | CHIDO | ≈ 18 M$ | 2024-12-04 | mort |
| `super-model` | Super Model | SM | ≈ 18 M$ | 2026-10-05 | mort |
| `children-of-the-sky` | Children Of The Sky | COTS | ≈ 18 M$ | 2025-07-21 | mort |
| `new-baby-elephant-houston-zoo` | New Baby Elephant Houston Zoo | KIRBY | ≈ 18 M$ | 2024-11-19 | mort |
| `naval-ai` | Patchwork Naval | NAVAL | ≈ 18 M$ | 2024-11-16 | mort |
| `puppers` | PUPPERS | PUPPERS | ≈ 18 M$ | 2026-08-21 | mort |
| `toescoin` | TOESCOIN | TOES | ≈ 18 M$ | 2026-06-20 | mort |
| `guanciale` | Guanciale by Virtuals | GUAN | ≈ 18 M$ | 2025-01-04 | mort |
| `liquid-solana-derivative` | Liquid Solana Derivative | LSD | ≈ 18 M$ | 2024-10-08 | mort |
| `loafcat` | LOAFCAT | LOAFCAT | ≈ 17 M$ | 2024-11-23 | mort |
| `make-no-mistakes-2` | Make No Mistakes | MISTAKE | ≈ 17 M$ | 2026-10-04 | mort |
| `stash-inu` | Stash Inu | STASH | ≈ 17 M$ | 2024-04-10 | mort |
| `bee` | Bee | BEE | ≈ 17 M$ | 2024-10-01 | mort |
| `boysclubbase` | Boysclubbase | $BOYS | ≈ 17 M$ | 2024-06-04 | mort |
| `charles-2` | Charles | KING | ≈ 17 M$ | 2025-05-25 | mort |
| `prick` | Prick | PRICK | ≈ 17 M$ | 2024-06-11 | mort |
| `chinese-oil-asset-reserve` | Chinese Oil Asset Reserve | COAR | ≈ 17 M$ | 2026-05-19 | mort |
| `tinhatcat` | TinHatCat | THC | ≈ 17 M$ | 2024-10-15 | mort |
| `goatcoin-2` | Goatcoin | GOAT | ≈ 17 M$ | 2025-08-27 | mort |
| `landlord-roland` | Landlord Ronald | $LANDLORD | ≈ 17 M$ | 2024-07-06 | mort |
| `calicoin-2` | Calicoin | CALICO | ≈ 17 M$ | 2025-02-05 | mort |
| `dogecast-2` | dogecast | DOGECAST | ≈ 17 M$ | 2025-01-19 | mort |
| `autism-2` | autism | AUTISM | ≈ 17 M$ | 2024-10-22 | mort |
| `leia` | Leia | LEIA | ≈ 17 M$ | 2024-03-15 | mort |
| `aigov` | AIGOV | OLIVIA | ≈ 17 M$ | 2025-05-29 | mort |
| `achi` | achi | ACHI | ≈ 17 M$ | 2024-05-25 | mort |
| `pepeinatux` | Pepeinatux | $INA | ≈ 16 M$ | 2025-01-22 | mort |
| `breaking` | Breaking | BREAKING | ≈ 16 M$ | 2026-08-27 | mort |
| `solgoat` | SolGoat | SOLGOAT | ≈ 16 M$ | 2024-03-26 | mort |
| `andy-3` | Andy | ANDY | ≈ 16 M$ | 2024-07-18 | copie ou ancienne version d'une carte; mort |
| `zen-2` | ZEN | ZEN | ≈ 16 M$ | 2026-04-01 | mort |
| `dogeball` | DOGEBALL | DOGEBALL | ≈ 16 M$ | 2026-10-13 | mort |
| `groggo-by-matt-furie` | Groggo By Matt Furie | GROGGO | ≈ 16 M$ | 2024-11-08 | mort |
| `brat` | Brat | BRAT | ≈ 16 M$ | 2025-02-16 | mort |
| `horny` | $horny | $HORNY | ≈ 16 M$ | 2024-12-11 | mort |
| `janet` | Janet | JANET | ≈ 16 M$ | 2024-10-22 | mort |
| `jobiess` | JobIess | JOBIESS | ≈ 16 M$ | 2025-09-18 | mort |
| `fuku-2` | Fuku | FUKU | ≈ 16 M$ | 2025-01-05 | mort |
| `dork-lord-coin` | DORK LORD COIN | DLORD | ≈ 16 M$ | 2024-05-01 | mort |
| `dream-2` | DREAM | DREAM | ≈ 16 M$ | 2024-11-28 | mort |
| `america-pac` | America Pac | PAC | ≈ 16 M$ | 2024-10-08 | mort |
| `apes-go-bananas` | Apes Go Bananas | AGB | ≈ 16 M$ | 2023-05-29 | mort |
| `smiling-dolphin` | Smiling Dolphin | MIHARU | ≈ 16 M$ | 2024-10-11 | mort |
| `memecoin-3` | Memecoin | MEMECOIN | ≈ 16 M$ | 2026-04-29 | copie ou ancienne version d'une carte; mort |
| `darkpino` | DarkPino | DPINO | ≈ 16 M$ | 2025-08-30 | mort |
| `this-will-make-ur-monthly-salary` | This will make ur monthly salary | SALARY | ≈ 16 M$ | 2025-08-07 | mort |
| `cope-3` | Cope | COPE | ≈ 16 M$ | 2025-08-29 | mort |
| `x-community` | X Community | X | ≈ 16 M$ | 2025-01-17 | mort |
| `sentai-2` | SENTAI | SENTAI | ≈ 16 M$ | 2025-01-11 | mort |
| `vida-global-cto` | Vida Global CTO | CTO | ≈ 16 M$ | 2026-09-08 | mort |
| `let-him-cook` | Let Him Cook | $COOK | ≈ 16 M$ | 2024-11-19 | mort |
| `russian-oil-asset-fund` | Russian Oil Asset Fund | ROAF | ≈ 16 M$ | 2026-05-09 | mort |
| `blackrack` | BlackRack | RACKS | ≈ 16 M$ | 2025-01-07 | mort |
| `holy-coin` | Holy Coin | HOLY | ≈ 16 M$ | 2025-09-29 | mort |
| `good-gensler` | Good Gensler | GENSLR | ≈ 16 M$ | 2023-05-06 | mort |
| `wally` | Wally | WALLY | ≈ 15 M$ | 2024-11-13 | mort |
| `schrodinger` | Schrodinger | MEOW | ≈ 15 M$ | 2021-12-08 | mort |
| `daumenfrosch` | Daumenfrosch | DAUMEN | ≈ 15 M$ | 2024-03-09 | mort |
| `gib-3` | gib | GIB | ≈ 15 M$ | 2025-05-25 | mort |
| `fuku-kun` | Fuku-Kun | FUKU | ≈ 15 M$ | 2024-08-09 | mort |
| `keydog` | KEYDOG | $KEYDOG | ≈ 15 M$ | 2024-11-01 | mort |
| `sugar-bush` | SUGAR BUSH | SUGR | ≈ 15 M$ | 2024-11-25 | mort |
| `ruri-truth-terminal-s-crush` | Ruri - Truth Terminal's Crush | RURI | ≈ 15 M$ | 2024-11-30 | mort |
| `styro-steve` | Styro Steve | SS | ≈ 15 M$ | 2024-12-29 | mort |
| `valor-2` | VALOR | VALOR | ≈ 15 M$ | 2025-10-31 | mort |
| `one-unchill-gal` | one unchill gal | GAL | ≈ 15 M$ | 2024-11-26 | mort |
| `valentine-grok-companion-3` | Valentine Grok Companion | VALENTINE | ≈ 15 M$ | 2025-07-19 | mort |
| `pepo` | PEPO | PEPO | ≈ 15 M$ | 2025-02-01 | mort |
| `goatseus-maximus-on-eth` | Goatseus Maximus | GOAT | ≈ 15 M$ | 2024-10-24 | copie ou ancienne version d'une carte; mort |
| `reflections-of-dissonance-ai` | Reflections of Dissonance AI | AIKA | ≈ 15 M$ | 2024-11-18 | nature à vérifier; mort |
| `doogle` | Doogle | DOOGLE | ≈ 15 M$ | 2024-07-08 | mort |
| `kekistan` | Kekistan | KEK | ≈ 15 M$ | 2025-01-01 | mort |
| `actual` | ACTUAL | ACTUAL | ≈ 15 M$ | 2025-01-21 | mort |
| `mona-arcane` | Mona Arcane | MONA | ≈ 15 M$ | 2024-11-27 | mort |
| `official-crypto-nostra` | Official Crypto Nostra | OCN | ≈ 15 M$ | 2025-06-06 | mort |
| `fartcat` | Fartcat | FARTCAT | ≈ 15 M$ | 2025-06-15 | mort |
| `onigiri-2` | Onigiri | ONI | ≈ 15 M$ | 2024-08-06 | mort |
| `beth` | Beth | $BETH | ≈ 15 M$ | 2024-12-25 | mort |
| `ghibli-kapibala` | Ghibli Kapibala | KAPIBALA | ≈ 15 M$ | 2025-04-20 | mort |
| `doge-jones-industrial-average` | Doge Jones Industrial Average | DJI | ≈ 15 M$ | 2024-11-22 | mort |
| `csi888` | CSI888 | CSI | ≈ 15 M$ | 2024-10-08 | mort |
| `suiboxer` | SUIBoxer | SBOX | ≈ 15 M$ | 2025-05-23 | mort |
| `inferno-2` | INFERNO | INF | ≈ 15 M$ | 2025-01-23 | mort |
| `lingyan` | Lingyan | LINGYAN | ≈ 15 M$ | 2024-11-14 | mort |
| `law-of-attraction` | Law of Attraction | LOA | ≈ 15 M$ | 2024-05-23 | mort |
| `degen-capital-by-virtuals` | Degen Capital by Virtuals | DEGENC | ≈ 15 M$ | 2024-12-31 | mort |
| `the-blinking-ai-cat-catfather` | The Blinking AI Cat - Catfather | CATF | ≈ 15 M$ | 2025-01-04 | nature à vérifier; mort |
| `gugo` | Gugo | GUGO | ≈ 15 M$ | 2025-08-13 | mort |
| `land-wu` | Land Wu | LANDWU | ≈ 15 M$ | 2024-06-13 | mort |
| `nyx-by-virtuals` | Nyx by Virtuals | NYX | ≈ 14 M$ | 2025-02-13 | mort |
| `duckyduck` | DuckyDuck | DUCKY | ≈ 14 M$ | 2024-07-30 | mort |
| `libra-4` | Libra | LIBRA | ≈ 14 M$ | 2025-02-17 | copie ou ancienne version d'une carte; mort |
| `vulgar-penguin` | 三维威廉泰尔企鹅 (Vulgar Penguin) | 恶俗企鹅 | ≈ 14 M$ | 2025-12-02 |  |
| `dog-shit-going-nowhere` | Dog shit going nowhere | DOGSHIT2 | ≈ 14 M$ | 2025-02-05 | mort |
| `the-anthropic-order` | The Anthropic Order | TAO | ≈ 14 M$ | 2024-12-04 | mort |
| `fluffington` | Fluffington | FLUFFI | ≈ 14 M$ | 2024-08-16 | mort |
| `sumi` | SUMI | SUMI | ≈ 14 M$ | 2024-11-17 | mort |
| `babysol` | BabySOL | BABYSOL | ≈ 14 M$ | 2024-03-17 | mort |
| `mind-zero` | Mind Zero | MIND | ≈ 14 M$ | 2024-11-29 | mort |
| `zoo-world` | Zoo World | ZOO | ≈ 14 M$ | 2025-01-28 | mort |
| `santa-hat` | SANTA HAT | SANTAHAT | ≈ 14 M$ | 2024-11-30 | mort |
| `dog-emoji-on-solana` | Dog Emoji On Solana | 🐕 | ≈ 14 M$ | 2024-10-13 | mort |
| `crashout` | Crashout | CRASHOUT | ≈ 14 M$ | 2024-11-28 | mort |
| `binance-yellow-robot` | Binance Yellow Robot | BINA | ≈ 14 M$ | 2025-10-08 | mort |
| `shitcoin-2` | Shitcoin | SHIT | ≈ 14 M$ | 2024-09-24 | mort |
| `flappy` | Flappy | FLAPPY | ≈ 14 M$ | 2024-07-12 | mort |
| `ratomilton` | ratomilton | MILTON | ≈ 14 M$ | 2025-01-29 | mort |
| `zenith-protocol` | Zenith Protocol | ZTH | ≈ 14 M$ | 2026-09-09 | nature à vérifier; mort |
| `moomoo-the-bull` | MOOMOO THE BULL | MOOMOO | ≈ 14 M$ | 2025-07-11 | mort |
| `iiii-lovvv-youuuu` | iiii lovvvv youuuu | ILY | ≈ 14 M$ | 2024-11-21 | mort |
| `arbuz` | ARBUZ | ARBUZ | ≈ 14 M$ | 2024-03-23 | mort |
| `dawg-coin` | Dawg Coin | DAWG | ≈ 14 M$ | 2023-12-04 | mort |
| `mochicat` | MOCHICAT | MOCHICAT | ≈ 14 M$ | 2024-04-02 | mort |
| `moonbag` | MoonBag | MBAG | ≈ 14 M$ | 2024-10-15 | mort |
| `chatgpt-s-mascot` | ChatGPT's Mascot | CHATTY | ≈ 14 M$ | 2024-11-18 | mort |
| `powsche` | POWSCHE | POWSCHE | ≈ 14 M$ | 2024-12-04 | mort |
| `snibbu-the-crab` | Snibbu the Crab | SNIBBU | ≈ 14 M$ | 2024-07-30 | mort |
| `britt` | Britt | BRITT | ≈ 13 M$ | 2024-04-22 | mort |
| `next-gen-pepe` | Next Gen PEPE | PEPE | ≈ 13 M$ | 2024-06-12 | mort |
| `canwifhat` | Canwifhat | CAN | ≈ 13 M$ | 2024-03-25 | mort |
| `based-usa` | Based USA | USA | ≈ 13 M$ | 2024-05-22 | mort |
| `john-the-coin` | John the Coin | JOHN | ≈ 13 M$ | 2024-10-14 | mort |
| `helloworld` | HELLOWORLD | HELLOWORLD | ≈ 13 M$ | 2025-06-04 | mort |
| `golden-celestial-ratio` | Golden Celestial Ratio | GCR | ≈ 13 M$ | 2024-10-18 | mort |
| `repost-dog` | Repost Dog | RDOG | ≈ 13 M$ | 2024-09-30 | mort |
| `deer-seized-by-us-government` | Deer Seized by US Government | BABY | ≈ 13 M$ | 2025-03-02 | mort |
| `matt-furie-s-boys-club` | Matt Furie's Boys Club | BOYSCLUB | ≈ 13 M$ | 2024-06-12 | mort |
| `pi-network-dog` | Pi Network Dog | PIDOG | ≈ 13 M$ | 2025-02-18 | nature à vérifier; mort |
| `commander-vrax` | Commander Vrax | VRAX | ≈ 13 M$ | 2026-09-30 | copie ou ancienne version d'une carte; mort |
| `doge-mascot-shibu` | Shibu | SHIBU | ≈ 13 M$ | 2024-10-30 | mort |
| `dividend-dog-head` | 分红狗头 (Dividend Dog Head) | 分红狗头 | ≈ 13 M$ | 2026-01-30 | mort |
| `nibbles` | Nibbles | NIBBLES | ≈ 13 M$ | 2025-01-30 | mort |
| `djcat` | DJCAT | DJCAT | ≈ 13 M$ | 2024-05-19 | mort |
| `cat-wif-sword` | cat wif sword | SWORDCAT | ≈ 13 M$ | 2026-09-29 | copie ou ancienne version d'une carte; mort |
| `don-t-burn-capital` | Don't Burn Capital | DBC | ≈ 13 M$ | 2025-07-05 | mort |
| `z-3` | Z | Z | ≈ 13 M$ | 2026-08-19 | mort |
| `just-need-some-rest` | Just need some rest | REST | ≈ 13 M$ | 2025-09-03 | mort |
| `i-dont-know` | i dont know | IDK | ≈ 13 M$ | 2024-03-20 | mort |
| `darksun` | darksun | BINARY | ≈ 13 M$ | 2024-12-08 | mort |
| `chill-family` | Chill Family | CHILLFAM | ≈ 13 M$ | 2024-11-22 | mort |
| `magnet-2` | Magnet | MAGNET | ≈ 13 M$ | 2024-10-12 | mort |
| `half-orange-drinking-lemonade` | Half Orange Drinking Lemonade | HODL | ≈ 13 M$ | 2024-10-15 | mort |
| `fleabone` | FLEABONE | BONE | ≈ 13 M$ | 2024-12-13 | mort |
| `baba` | BABA | BABA | ≈ 13 M$ | 2024-03-18 | mort |
| `antitoken` | Antitoken | ANTI | ≈ 13 M$ | 2025-05-02 | mort |
| `cheepepe` | cheepepe | CHEEPEPE | ≈ 13 M$ | 2024-05-18 | mort |
| `imagine-2` | IMAGINE | IMAGINE | ≈ 13 M$ | 2025-08-02 | mort |
| `bnb-wallstreet-bull` | BNB Wallstreet Bull | WBULL | ≈ 13 M$ | 2025-10-09 | mort |
| `rainbowfish` | rainbowfish | FISH | ≈ 12 M$ | 2026-01-07 | mort |
| `trenchai` | TrenchAI | TRENCHAI | ≈ 12 M$ | 2025-01-03 | mort |
| `strategic-hub-for-innovation-in-blockchain` | Strategic Hub for Innovation in Blockchain | SHIB | ≈ 12 M$ | 2024-11-09 | nature à vérifier; mort |
| `trackedbio` | TrackedBio | TRACKEDBIO | ≈ 12 M$ | 2024-12-08 | mort |
| `bubba` | Bubba | BUBBA | ≈ 12 M$ | 2024-06-04 | mort |
| `meta-doge` | Meta Doge | METADOGE | ≈ 12 M$ | 2021-12-08 | mort |
| `morti` | Morti | MORTI | ≈ 12 M$ | 2024-10-01 | mort |
| `kabosu-kabosucoin-erc` | Kabosu | KABOSU | ≈ 12 M$ | 2024-10-17 | copie ou ancienne version d'une carte; mort |
| `dook` | Dook | DOOK | ≈ 12 M$ | 2024-06-12 | mort |
| `maga-pepe` | MAGA PEPE | MAGAPEPE | ≈ 12 M$ | 2024-05-27 | mort |
| `protoken` | Protoken | PRO | ≈ 12 M$ | 2025-05-02 | mort |
| `paradox-3` | PARADOX | PARADOX | ≈ 12 M$ | 2024-11-16 | mort |
| `national-trust-fund-system` | National Trust Fund System | NTFS | ≈ 12 M$ | 2026-07-25 | mort |
| `alpha-3` | Reject Modernity | ALPHA | ≈ 12 M$ | 2024-11-09 | mort |
| `khaokheowzoo` | khaokheowzoo | KHEOWZOO | ≈ 12 M$ | 2024-12-15 | mort |
| `shanghai-inu` | Shanghai Inu | SHANG | ≈ 12 M$ | 2023-05-23 | mort |
| `living-the-dream` | Living the Dream | LTD | ≈ 12 M$ | 2024-08-31 | mort |
| `brainrot` | brainrot | ROT | ≈ 12 M$ | 2024-11-17 | mort |
| `hantavirus` | Hantavirus | HANTA | ≈ 12 M$ | 2026-05-08 | mort |
| `mewing-coin` | Mewing Coin | MEWING | ≈ 12 M$ | 2024-05-06 | mort |
| `quitcoin` | Quitcoin | QC | ≈ 12 M$ | 2025-08-22 | mort |
| `mindfak-by-matt-furie` | Mindfak By Matt Furie | MINDFAK | ≈ 12 M$ | 2025-08-22 | mort |
| `bitcoin-second-chance` | Bitcoin Second Chance | BTC | ≈ 12 M$ | 2025-12-30 | mort |
| `fartless-coin` | FARTLESS COIN | FARTLESS | ≈ 12 M$ | 2025-08-05 | mort |
| `retardcoin` | retardcoin | RETARD | ≈ 12 M$ | 2025-05-23 | mort |
| `forky-2` | Forky | FORKY | ≈ 12 M$ | 2025-01-16 | mort |
| `sol-the-trophy-tomato` | Sol The Trophy Tomato | SOL | ≈ 12 M$ | 2026-01-25 | mort |
| `kanye` | Kanye | YE | ≈ 12 M$ | 2025-02-02 | mort |
| `kekius-maximus-4` | Kekius Maximus | KM | ≈ 12 M$ | 2025-01-11 | copie ou ancienne version d'une carte; mort |
| `infinite-backrooms` | infinite backrooms | IB | ≈ 12 M$ | 2024-10-31 | mort |
| `albemarle-meme-token` | Albemarle Meme Token | ALBEMARLE | ≈ 12 M$ | 2024-03-13 | mort |
| `real-smurf-cat-2` | Real Smurf Cat-шайлушай | SMURF | ≈ 12 M$ | 2024-03-09 | mort |
| `peanut-3` | Peanut | PNUT | ≈ 12 M$ | 2024-11-13 | mort |
| `toga` | TOGA | TOGA | ≈ 11 M$ | 2024-11-10 | mort |
| `yachts-coin` | Yachts Coin | YTC | ≈ 11 M$ | 2025-03-26 | mort |
| `koku-the-shikoku` | Koku The Shikoku | $KOKU | ≈ 11 M$ | 2025-02-15 | mort |
| `save-the-seals-2` | Save The Seals | SEALS | ≈ 11 M$ | 2026-10-14 | mort |
| `joram-poowel` | JORAM POOWEL | POOWEL | ≈ 11 M$ | 2024-04-29 | mort |
| `live-on-toilet-until-50m` | Live On Toilet Until 50M | SHITCOIN | ≈ 11 M$ | 2024-11-22 | mort |
| `terminalius-maximus` | Terminalius Maximus | BARON | ≈ 11 M$ | 2024-11-24 | mort |
| `pnut-s-dog` | Pnut's Dog | TUCKER | ≈ 11 M$ | 2024-11-19 | mort |
| `el-gato` | el gato | ELGATO | ≈ 11 M$ | 2024-03-10 | mort |
| `buttholes` | Buttholes | BHOLE | ≈ 11 M$ | 2025-01-05 | mort |
| `zenith-3` | Zenith | ZEN | ≈ 11 M$ | 2025-01-06 | mort |
| `smolano` | SmoLanO | SLO | ≈ 11 M$ | 2024-01-01 | mort |
| `sendor` | Sendor | SENDOR | ≈ 11 M$ | 2024-11-28 | mort |
| `muzki` | Muzki | MUZKI | ≈ 11 M$ | 2024-05-17 | mort |
| `limitless` | LIMITLESS | LIMITLESS | ≈ 11 M$ | 2025-01-15 | mort |
| `ceiling-cat` | Ceiling Cat | CEICAT | ≈ 11 M$ | 2024-04-02 | mort |
| `dogcoin-2` | Dogcoin | DCOIN | ≈ 11 M$ | 2025-01-24 | mort |
| `bomo-on-base` | BOMO on Base | BOMO | ≈ 11 M$ | 2025-08-30 | mort |
| `karmacoin-2` | Karmacoin | KARMA | ≈ 11 M$ | 2025-09-02 | mort |
| `bull-5` | Bull | BULL | ≈ 11 M$ | 2026-04-15 | mort |
| `colon` | Colon | COLON | ≈ 11 M$ | 2024-08-17 | mort |
| `star-cat` | STAR CAT | SC | ≈ 11 M$ | 2024-06-29 | mort |
| `chimerica` | CHIMERICA | CHIMERICA | ≈ 11 M$ | 2026-05-16 | mort |
| `boochie-by-matt-furie` | Boochie by Matt Furie | BOOCHIE | ≈ 11 M$ | 2025-05-22 | mort |
| `boopa` | Boopa | BOOPA | ≈ 11 M$ | 2025-05-02 | mort |
| `poppy` | Poppy | POPPY | ≈ 11 M$ | 2025-01-06 | mort |
| `ethereum-doge` | Ethereum Doge | EDOGE | ≈ 11 M$ | 2024-09-25 | mort |
| `patton` | Patton | PATTON | ≈ 11 M$ | 2024-05-11 | mort |
| `terminus-3` | Terminus | TERMINUS | ≈ 11 M$ | 2024-10-15 | mort |
| `bonk-2-0-sol` | Bonk 2.0 (Sol) | BONK2.0 | ≈ 11 M$ | 2024-03-09 | mort |
| `lehman-brothers` | Lehman Brothers | LEH | ≈ 11 M$ | 2024-03-22 | mort |
| `aejo` | Aejo | AEJO | ≈ 11 M$ | 2024-11-29 | mort |
| `cramer-coin` | Cramer Coin | $CRAMER | ≈ 11 M$ | 2024-03-05 | mort |
| `pnut-s-sister` | Pnut's Sister | CHLOE | ≈ 10 M$ | 2024-11-13 | mort |
| `xenomorph` | XENOMORPH | XENO | ≈ 10 M$ | 2024-11-22 | mort |
| `kitsune` | Kitsune | KIT | ≈ 10 M$ | 2024-03-17 | mort |
| `synthesizer-dog` | Synthesizer Dog | SYNDOG | ≈ 10 M$ | 2024-12-08 | mort |
| `action-figure` | Action Figure | FIGURE | ≈ 10 M$ | 2025-04-14 | mort |
| `hispanic-pepe` | hispanic pepe | CONCHO | ≈ 10 M$ | 2025-01-15 | mort |
| `peanut-2` | Peanut [OLD] | PEANUT | ≈ 10 M$ | 2024-11-05 | mort |
| `strawberry-in-bloom` | Strawberry In Bloom | BERRY | ≈ 10 M$ | 2025-05-13 | mort |
| `moondoge` | MOONDOGE | MOONDOGE | ≈ 10 M$ | 2025-07-13 | mort |
| `first-reply` | first reply | SIRIUS | ≈ 10 M$ | 2024-10-01 | mort |
| `breakout-bro-by-virtuals` | Breakout Bro by Virtuals | BOB | ≈ 10 M$ | 2025-01-01 | mort |
| `self-aware-meme-2` | Self-Aware Meme | SAM | ≈ 10 M$ | 2026-10-06 | mort |
| `wife-changing-money-2` | Wife Changing Money | WIFE | ≈ 10 M$ | 2025-06-18 | mort |
| `dogai-wtf` | DOGAI | DOGAI | ≈ 10 M$ | 2024-10-27 | mort |
| `hachikosolana` | HachikoSolana | HACHI | ≈ 10 M$ | 2024-04-01 | mort |
| `jiffpom` | Jiffpom | JIFF | ≈ 10 M$ | 2024-11-26 | mort |
| `fih` | fih | FIH | ≈ 10 M$ | 2026-08-02 | mort |
| `joeing737` | Joeing737 | JEOING737 | ≈ 10 M$ | 2024-06-05 | mort |
| `sora-oracle` | Sora Oracle | SORA | ≈ 10 M$ | 2025-10-30 | mort |
| `wibwob` | WibWob | WIBWOB | ≈ 10 M$ | 2024-11-29 | mort |
| `basedmilio` | Basedmilio | BASED | ≈ 10 M$ | 2024-07-15 | mort |
| `zygo-the-frog` | Zygo The Frog | ZYGO | ≈ 10 M$ | 2025-07-25 | mort |
| `smoking-giraffe` | Smoking Giraffe | GRAF | ≈ 10 M$ | 2024-05-22 | mort |

## Annexe 4 : surclassements manuels (`docs/recherche-v2/surclassements.md`)

Appliqués en dernier, après la pyramide et la règle des pics aberrants.

| Nom | Ticker | Chaîne visée | Rareté forcée | Cartes visées | Rareté sans surclassement | Raison | Source |
|---|---|---|---|---|---|---|---|
| Floki | FLOKI | toutes | légendaire | 4 Floki | épique | pic ≥ 1 Md$ largement rapporté | connaissance générale, à vérifier |
| Peanut the Squirrel | PNUT | toutes | légendaire | 11 Peanut the Squirrel | épique | pic ≥ 1 Md$ largement rapporté | connaissance générale, à vérifier |
| cat in a dogs world | MEW | toutes | légendaire | 16 cat in a dogs world † | épique | pic ≥ 1 Md$ largement rapporté | connaissance générale, à vérifier |
| Neiro | NEIRO | Ethereum | légendaire | 15 Neiro † | commune | pic ≥ 1 Md$ largement rapporté | connaissance générale, à vérifier |
| Memecoin | MEME | toutes | légendaire | 3 Memecoin † | commune | pic ≥ 1 Md$ largement rapporté | connaissance générale, à vérifier |

## Annexe 5 : pics aberrants

21 cartes dont le pic n'est qu'estimé et atteint 1 Md$ ou plus, sans surclassement. Le chiffre est affiché avec la mention « estimation aberrante, à vérifier ». Pour la rareté, il compte comme un pic inconnu. 22 épiques retombent au total (pics aberrants et planchers ci-dessous).

| N° | Nom | Ticker | Pic estimé | Plancher sourcé | État | Rareté sans la règle | Rareté v2 |
|---|---|---|---|---|---|---|---|
| 487 | ShibaDoge | SHIBDOGE | ≈ 12769,26 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 488 | BNB Tiger OG | BNBTIGEROG | ≈ 3351,98 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 489 | Pitbull | PIT | ≈ 5,81 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 490 | Anon Inu | AINU | ≈ 5,18 Md$ (estimé CG) — estimation aberrante, à vérifier | — | mort | épique | commune |
| 491 | AI XOVIA | AIX | ≈ 4,50 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 492 | YooShi | YOOSHI | ≈ 4,19 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 493 | Pups † | PUPS | ≈ 3,87 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 494 | Pig Finance | PIG | ≈ 3,70 Md$ en FDV (10/05/2021) — estimation aberrante, à vérifier | — | mort | épique | commune |
| 495 | PEPPER | PEPPER | ≈ 2,56 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 496 | Capybara Nation | BARA | ≈ 2,21 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 497 | Rosa Inu | ROSA | ≈ 2,20 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 498 | Kishu Inu | KISHU | ≈ 1,69 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 499 | CorgiAI | CORGIAI | ≈ 1,53 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 500 | Bezoge Earth | BEZOGE | ≈ 1,52 Md$ en FDV (22/11/2021) — estimation aberrante, à vérifier | — | mort | épique | commune |
| 501 | Ape and Pepe | APEPE | ≈ 1,45 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin | épique | commune |
| 502 | catwifhat | CWIF | ≈ 1,4 Md$ (estimation CoinGecko de l'annexe 3) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 503 | Samoyedcoin † | SAMO | ≈ 1,36 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 504 | Solid X | SOLIDX | ≈ 1,14 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| 505 | OSK | OSK | ≈ 1,05 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| AD39 | Hunter Biden's Laptop | LAPTOP | ≈ 34,13 Md$ (estimé CG) — estimation aberrante, à vérifier | — | en déclin (-95 % ou pire) | épique | commune |
| AD40 | ShibaBitcoin | SHIBTC | ≈ 1,02 Md$ (9 févr. 2025) ; CMC, relevé hebdomadaire (pic CMC douteux) — estimation aberrante, à vérifier | — | mort | épique | commune |

**Estimations ≥ 1 Md$ au-dessus d'une borne sourcée** (10 cartes) : pas aberrantes, mais la rareté suit la borne sourcée, pas l'estimation.

| N° | Nom | Ticker | Pic estimé | Borne sourcée | Rareté sans la règle | Rareté v2 |
|---|---|---|---|---|---|---|
| 1 | Bonk | BONK | ≈ 5,13 Md$ (estimé CG, au-dessus de la borne sourcée) | 2600 M$ | légendaire | légendaire |
| 2 | dogwifhat † | WIF | ≈ 4,82 Md$ (estimé CG, au-dessus de la borne sourcée) | 3350 M$ | légendaire | légendaire |
| 5 | Fartcoin | FARTCOIN | ≈ 2,48 Md$ (estimé CG, au-dessus de la borne sourcée) | 1600 M$ | légendaire | légendaire |
| 6 | Brett † | BRETT | ≈ 2,32 Md$ (estimé CG, au-dessus de la borne sourcée) | 2000 M$ | légendaire | légendaire |
| 8 | Ordinals | ORDI | ≈ 2,01 Md$ (estimé CG, au-dessus de la borne sourcée) | 1000 M$ | légendaire | légendaire |
| 10 | Sats | SATS (1000SATS) | ≈ 1,94 Md$ (estimé CG, au-dessus de la borne sourcée) | 1000 M$ | légendaire | légendaire |
| 14 | Goatseus Maximus | GOAT | ≈ 1,35 Md$ (estimé CG, au-dessus de la borne sourcée) | 1000 M$ | légendaire | légendaire |
| 22 | Degen † | DEGEN | ≈ 2,32 Md$ (estimé CG, au-dessus de la borne sourcée) | 439 M$ | épique | épique |
| 23 | Baby Doge Coin | BABYDOGE | ≈ 1,20 Md$ (estimé CG, au-dessus de la borne sourcée) | 310 M$ | épique | épique |
| 257 | LOBO•THE•WOLF•PUP | LOBO | ≈ 3,59 Md$ (estimé CG, au-dessus de la borne sourcée) | 71 M$ | épique | rare |

## Annexe 6 : retraits de l'audit R5 (non-mèmes)

| N° v1 | Nom | Ticker | Motif |
|---|---|---|---|
| 4 | Pump.fun | PUMP | launchpad (Pump.fun) : jeton de plateforme, pas un mème |
| 5 | MemeCore | M | L1 (MemeCore) : chaîne propre, pas un mème |
| 6 | Virtuals Protocol | VIRTUAL | launchpad d'agents IA (Virtuals Protocol) |
| 8 | Notcoin | NOT | tap-to-earn Telegram (Notcoin) : jeu d'abord, mème ensuite |
| 9 | ai16z (ElizaOS) | AI16Z | agent IA / cadriciel ElizaOS (ai16z) ; parodie de a16z mais devenu jeton d'infrastructure |
| 11 | MEMETOON | MEME | jeton utilitaire d'une plateforme de BD (MEMETOON, BNB Chain) ; pic estimé aberrant |
| 20 | Animecoin | ANIME | jeton d'écosystème Azuki / Animechain (Animecoin), pas un mème |
| 35 | Zerebro | ZEREBRO | agent IA (Zerebro, cadriciel ZerePy) ; lancé sur pump.fun mais positionné agent |
| 36 | aixbt by Virtuals | AIXBT | agent IA d'analyse (aixbt by Virtuals) |
| 38 | Hamster Kombat | HMSTR | tap-to-earn Telegram (Hamster Kombat) |
| 39 | AI Companions | AIC | application de compagnons IA (AI Companions), jeton utilitaire |
| 45 | Griffain | GRIFFAIN | plateforme d'agents IA (Griffain) |
| 46 | The Grays Currency | PTGC | DAO de rachat et brûlage de LP sur PulseChain (The Grays Currency), DeFi |
| 49 | BurnedFi | BURN | protocole DeFi de brûlage avec jeton BUILD (BurnedFi) |
| 59 | Freysa | FAI | jeu / agent IA (Freysa) |
| 63 | GAME by Virtuals | GAME | cadriciel d'agents IA (GAME by Virtuals) |
| 65 | Ava AI | AVA | agent IA (Ava AI, Holoworld) |
| 69 | Arc | ARC | cadriciel d'agents IA Rig (Arc) |
| 82 | Launch Coin on Believe (ex-PASTERNAK) | LAUNCHCOIN | jeton du launchpad Believe (ex-PASTERNAK) : renommé en jeton de plateforme |
| 117 | Ribbita | TIBBIR | agent IA sur Virtuals (Ribbita by Virtuals) |
| 118 | Alchemist AI | ALCH | plateforme IA sans code (Alchemist AI) |
| 122 | Catizen | CATI | jeu Telegram (Catizen) |
| 131 | BankrCoin | BNKR | agent IA de trading / launchpad (BankrCoin) |
| 158 | PotCoin | POT | jeton PotCoin : monnaie de paiement cannabis (2014), utilitaire |
| 161 | Send | SEND | jeton de l'écosystème SendAI (Send), utilitaire |
| 163 | SwarmNode.ai | SNAI | plateforme d'agents IA (SwarmNode.ai) |
| 175 | Ninja Squad Token | NST | jeton utilitaire d'un écosystème NFT / outils de trading (Ninja Squad Token) |
| 180 | FXN | FXN | réseau d'agents IA (FXN) |
| 182 | Major | MAJOR | jeu Telegram (Major) |
| 205 | Finvesta | FINVESTA | jeton déflationniste DeFi PulseChain (Finvesta) |
| 210 | Mind of Pepe | MIND | prévente « agent IA » (Mind of Pepe) |
| 224 | Neur | NEUR | application d'agent IA (Neur) |
| 258 | Not Pixel | PX | jeu Telegram (Not Pixel) |
| 282 | ASSAI | ASSAI | agent IA de trading (ASSAI, Assisterr) |
| 342 | Snorter | SNORT | prévente de bot de trading Telegram (Snorter) |
| 430 | MemeFi | MEMEFI | tap-to-earn (MemeFi) |
| 453 | Yunai by Virtuals | YUNAI | agent IA sur Virtuals (Yunai by Virtuals) |
| 529 | Acolyte | à vérifier | plateforme de découverte d'agents IA (Acolyte by Virtuals) |
| 532 | AIFlow | AIFLOW | cadriciel d'agents IA sur BNB Chain (AIFlow) |
| 548 | Balaji (créateur Zora) | BALAJIS | creator coin Zora (Balaji), jeton de créateur |
| 564 | Blum | BLUM | application de trading / jeu Telegram (Blum) |
| 571 | Bone ShibaSwap † | BONE | jeton de gouvernance de ShibaSwap (Bone ShibaSwap) |
| 579 | ChatAI | CHATAI | jeu IA « play-to-earn » (ChatAI Town) |
| 583 | clank.fun | CLANKFUN | launchpad (clank.fun) |
| 590 | Cult DAO | CULT | DAO d'investissement (Cult DAO), DeFi |
| 601 | Dogechain † | DC | jeton de chaîne (Dogechain), L2 |
| 603 | Dogeparty | XDP | protocole (Dogeparty, fork de Counterparty) |
| 645 | Hypurr Fun | HFUN | launchpad Hyperliquid (Hypurr Fun) |
| 649 | Jesse (créateur Zora) | JESSE | creator coin Zora (Jesse), jeton de créateur |
| 653 | Kazonomics (créateur Zora) | KAZONOMICS | creator coin Zora (Kazonomics), jeton de créateur |
| 665 | Luna by Virtuals | LUNA | agent IA (Luna by Virtuals) |
| 676 | Moby AI | MOBY | agent IA de suivi de baleines (Moby AI) |
| 690 | MultiBit | MUBI | pont et protocole BRC-20 (MultiBit) |
| 701 | Ordiswap | ORDS | DEX BRC-20 (Ordiswap) |
| 704 | Pandora | PANDORA | jeton expérimental ERC-404 (Pandora), pas un mème |
| 726 | RAVE | RAVE | jeton d'une DAO d'événements (RaveDAO) |
| 764 | Swarms | SWARMS | cadriciel d'agents IA (Swarms) |
| 766 | TARS AI | TAI | agent IA (TARS AI) |
| 772 | tokenbot | CLANKER | bot launchpad Clanker (tokenbot) |
| 782 | VaderAI | VADER | DAO d'investissement agent IA (VaderAI) |
| D5 | Siren | SIREN | agent IA DeFAI (Siren) |
| D22 | SexCoin | SXC | monnaie de paiement de l'industrie adulte (SexCoin), utilitaire |
| D34 | Bitconnect | BCC | plateforme de prêt frauduleuse (Bitconnect), pas un mème |
| D38 | CryptoZoo | ZOO | jeu NFT (CryptoZoo), pas un mème |
| D39 | CumRocket † | CUMMIES | jeton d'une plateforme de contenus adultes (CumRocket), utilitaire |
| D58 | Titcoin | TIT | monnaie de paiement de l'industrie adulte (Titcoin), utilitaire |
