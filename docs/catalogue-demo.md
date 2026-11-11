# Catalogue de démo des cartes Memaster

**Date :** 11/11/2026. Généré par `python3 docs/recherche-v2/consolider.py --demo` à partir du catalogue v2 : ne pas éditer à la main. Ce document n'est pas un conseil en investissement.

**Total : 1530 cartes** (dont 3 mythiques scellées), **218 brûlables possibles** (objectif ≥ 150, dont au moins une commune ou une rare : atteint).

## Règles

- Base : section « catalogue » de `docs/data/catalogue-v2.json`. Aucune « À décider ».
- Exclues : toute carte à drapeau `politique`, `personne réelle`, `obscène` ou `arnaque avérée` ; toute carte sans drapeau dont le nom, le ticker ou l'histoire désigne un politicien (mots-clés du drapeau `politique`, plus RFK, Kennedy, 川普, etc.) ; tout état « arnaque avérée ».
- **Brûlable possible** (`brulable_possible` dans le JSON, raison dans `raison_brulable`) : état autre que « mort », et jeton rapproché dans `docs/data/coingecko-meme-2026-11-11.csv` avec volume 24 h ≥ 20 000 $ **et** capitalisation ≥ 1 M$ (valeurs dans `liquidite`). Mythiques : jamais brûlables. Une carte sans id CoinGecko rapproché n'est pas brûlable (liquidité non documentée).
- Si moins de 150 brûlables, ou aucune commune ni rare brûlable, les exclues brûlables reviennent par paliers : `personne réelle`, puis politicien sans drapeau, `politique`, `obscène`, « À décider » ; jamais `arnaque avérée`.
- N° et `id` : ceux du catalogue v2 (numérotation à trous, ids stables pour les visuels).

## Décompte

| Rareté | Cartes | Brûlables possibles |
|---|---|---|
| mythique | 3 | 0 |
| légendaire | 21 | 18 |
| épique | 228 | 84 |
| rare | 224 | 89 |
| commune | 1054 | 27 |
| **Total** | **1530** | **218** |

## Réintégrées (0)

Aucune : l'objectif est atteint sans réintégrer de carte exclue.

## Exclues (220)

| Motif | Cartes |
|---|---|
| à décider | 101 |
| personne réelle | 71 |
| obscène | 52 |
| politique | 38 |
| arnaque avérée | 16 |
| politicien (nom ou histoire, sans drapeau) | 5 |
| (une carte peut avoir plusieurs motifs) | |

### Politiciens sans drapeau (5)

| N° v2 | Nom | Ticker | Rareté | Brûlable si gardée |
|---|---|---|---|---|
| 71 | HarryPotterObamaSonic10Inu | BITCOIN | épique | oui |
| 948 | BarbieCrashBandicootRFK88 | SOLANA | commune | non |
| 1000 | HarryPotterTrumpHomerSimpson777Inu | ETHEREUM | commune | non |
| 1646 | 川普 (四川普通话) | 川普 | commune | non |
| AD87 | Barron | BARRON | commune | non |

### Liste complète

| N° v2 | Nom | Ticker | Rareté | Motifs | Brûlable si gardée |
|---|---|---|---|---|---|
| 45 | Australian Safe Shepherd | ASS | épique | obscène | non |
| 71 | HarryPotterObamaSonic10Inu | BITCOIN | épique | politicien (nom ou histoire, sans drapeau) | oui |
| 73 | Ronaldinho | STAR10 | épique | personne réelle | non |
| 130 | Stool Prisondente | JAILSTOOL | épique | personne réelle | non |
| 161 | Marshall Rogan Inu | MRI | épique | personne réelle | non |
| 168 | ElonXCat | EXC | épique | personne réelle | non |
| 241 | tooker kurlson | TOOKER | épique | politique, personne réelle | non |
| 331 | Buttcoin | BUTTCOIN | rare | obscène | oui |
| 371 | PornRocket | PORNROCKET | rare | obscène | non |
| 384 | Dickbutt | DICKBUTT | rare | obscène | non |
| 416 | Burnie Senders | BURNIE | rare | politique | non |
| 434 | 金蝶圣甲 (Golden Butterfly Sacred Armor) | 金蝶圣甲 | rare | obscène | oui |
| 445 | Shit Piss Skin Can | SPSC | rare | obscène | non |
| 500 | Bezoge Earth | BEZOGE | commune | personne réelle | non |
| 522 | Gen Z Quant | QUANT | commune | arnaque avérée | non |
| 532 | Ansem's Cat | HOBBES | commune | personne réelle | non |
| 543 | Snowdog | SDOG | commune | arnaque avérée | non |
| 554 | Anita Max Wynn | WYNN | commune | personne réelle | non |
| 563 | Luigi Mangione | LUIGI | commune | personne réelle | non |
| 574 | Lets Go Brandon | LETSGO | commune | politique | non |
| 577 | Sharpei | SHAR | commune | arnaque avérée | non |
| 580 | Deez Nuts | DEEZNUTS | commune | obscène | non |
| 584 | SpaceGrime | GRIMEX | commune | personne réelle | non |
| 609 | Prince Floki V2 | PrinceFloki | commune | personne réelle | non |
| 638 | Swasticoin | YZY | commune | obscène | non |
| 668 | Real Nigger Tate | RNT | commune | personne réelle, obscène | non |
| 680 | Cardi B (Wet Ass P***y) | WAP | commune | personne réelle, obscène | non |
| 683 | FU coin | FU | commune | obscène | non |
| 686 | Justice For Ross | ROSS | commune | personne réelle | non |
| 709 | SaylorMoon | SMOON | commune | personne réelle | non |
| 720 | ElonRWA | ELONRWA | commune | personne réelle | non |
| 734 | Doge Universe | SPACEXDOGE | commune | personne réelle | non |
| 741 | CumInu | CUMINU | commune | obscène | non |
| 742 | Briun Armstrung | BRIUN | commune | personne réelle | non |
| 744 | ElonDoge | EDOGE | commune | personne réelle | non |
| 813 | Uranus (Solana) | ANUS | commune | obscène | non |
| 860 | Chadimir Putni | PUTNI | commune | politique | non |
| 861 | Coinye West | COINYE | commune | personne réelle | non |
| 870 | Pepe Trump | PTRUMP | commune | politique | non |
| 880 | CumStar | CUMSTAR | commune | obscène | non |
| 904 | Biden Coin | BIDEN | commune | politique | non |
| 920 | GhibliCZ | GHIBLI | commune | personne réelle | non |
| 942 | SUITRUMP | SUITRUMP | commune | politique | non |
| 948 | BarbieCrashBandicootRFK88 | SOLANA | commune | politicien (nom ou histoire, sans drapeau) | non |
| 967 | artificial gooner intelligence | AGI | commune | obscène | non |
| 982 | Scam Altman | SCAM | commune | personne réelle | non |
| 1000 | HarryPotterTrumpHomerSimpson777Inu | ETHEREUM | commune | politicien (nom ou histoire, sans drapeau) | non |
| 1019 | ASSDAQ | ASSDAQ | commune | obscène | non |
| 1039 | DooDoo | DOODOO | commune | obscène | non |
| 1042 | CZ THE GOAT | CZGOAT | commune | personne réelle | non |
| 1062 | B.H.A.D (Bhad Bhabie) | BHAD | commune | personne réelle | non |
| 1092 | Baby Trump | BABYTRUMP | commune | politique | non |
| 1104 | Andrea Von Speed | VONSPEED | commune | personne réelle | non |
| 1126 | Doge CEO | DOGECEO | commune | personne réelle | non |
| 1128 | Just The Tip | TIPS | commune | obscène | non |
| 1139 | Magicaltux | TUX | commune | personne réelle | non |
| 1155 | Dogs of Elon | DOE | commune | personne réelle | non |
| 1194 | Shitzu † | SHITZU | commune | obscène | non |
| 1207 | Patlu | PATLU | commune | personne réelle | non |
| 1208 | Sam Bankmeme-Fried | SBF | commune | personne réelle | non |
| 1248 | FuckToken | FUCK | commune | obscène | non |
| 1256 | CageCoin | CAGE | commune | personne réelle | non |
| 1265 | CZ on Hyperliquid | CZ | commune | personne réelle | non |
| 1278 | Floki Musk | FLOKI | commune | personne réelle | non |
| 1300 | Where Did The ETH Go? (Pulsechain) | WHETH | commune | personne réelle | non |
| 1307 | Luca Netz's Dog | BANDIT | commune | personne réelle | non |
| 1308 | Make America Based Again | MABA | commune | politique | non |
| 1319 | 赵长娥 | 赵长娥 | commune | personne réelle | non |
| 1329 | KarpelesCoin | KAR | commune | personne réelle | non |
| 1355 | Mao Zedong | MAO | commune | politique | non |
| 1378 | Shekel | JEW | commune | obscène | non |
| 1381 | CULOSUI | CULO | commune | obscène | non |
| 1385 | BERNcash | BERN | commune | politique | non |
| 1394 | Floyd Money Mayweather | FLOYD | commune | personne réelle | non |
| 1404 | RonPaulCoin | RPC | commune | politique | non |
| 1406 | Bitcoin Adult | BTAD | commune | obscène | non |
| 1408 | XxXcoin | XXX | commune | obscène | non |
| 1410 | WankCoin | WKC | commune | obscène | non |
| 1412 | Theresa May Coin | MAY | commune | politique | non |
| 1416 | Pepe MAGA | PEPE MAGA | commune | politique | non |
| 1417 | BillaryCoin | BLRY | commune | politique | non |
| 1419 | Putin Classic | PUTIC | commune | politique | non |
| 1423 | Murraycoin | MRY | commune | personne réelle | non |
| 1428 | GeertCoin | GEERT | commune | politique | non |
| 1439 | FCKBanksCoin | FCK | commune | obscène | non |
| 1464 | Isiscoin | ISIS | commune | obscène | non |
| 1469 | Fetish | FETISH | commune | obscène | non |
| 1470 | AnalCoin | ANAL | commune | obscène | non |
| 1475 | ColbertCoin | CC | commune | personne réelle | non |
| 1479 | SJWCoin | SJW | commune | politique | non |
| 1480 | BDSM | BDSM | commune | obscène | non |
| 1482 | KimDotCoin | DOT | commune | personne réelle | non |
| 1485 | NineElevenTruthCoin | NTC | commune | politique | non |
| 1498 | Biebercoin | BRC | commune | personne réelle | non |
| 1513 | Dave Fartnoy | FARTNOY | commune | personne réelle, obscène | non |
| 1517 | Dogefather | DOGEFATHER | commune | personne réelle | non |
| 1521 | Doll (Ivana Knoll) | DOLL | commune | personne réelle | non |
| 1524 | Elon Buys Twitter | EBT | commune | personne réelle | non |
| 1525 | ElonGate † | ELONGATE | commune | personne réelle | non |
| 1527 | F*** Tristan | FTRISTAN | commune | personne réelle, obscène | non |
| 1531 | Floki Elon | FLOKIELON | commune | personne réelle | non |
| 1534 | G-Unit (piratage de 50 Cent) | GUNIT | commune | personne réelle, arnaque avérée | non |
| 1535 | Germany Token | GER | commune | personne réelle | non |
| 1539 | Goldenloaf (Yanukovych coin) | GLY | commune | politique | non |
| 1541 | GREED (Dave Portnoy) | GREED | commune | personne réelle | non |
| 1547 | I like this coin | LIKE | commune | arnaque avérée | non |
| 1548 | I will poop it NFT | SHIT | commune | obscène | non |
| 1551 | JaredFromSubway | JARED | commune | personne réelle | non |
| 1555 | Khamzat Chimaev | SMASH | commune | personne réelle | non |
| 1566 | MileyCyrusCoin | MCC | commune | personne réelle | non |
| 1573 | MOONKE | MOONKE | commune | arnaque avérée | non |
| 1590 | Prodeum | PRO | commune | arnaque avérée | non |
| 1591 | Proof of Weak Hands (PoWH 3D) | P3D | commune | arnaque avérée | non |
| 1597 | Rici Elon | RICI | commune | personne réelle | non |
| 1605 | Save The Kids | KIDS | commune | arnaque avérée | non |
| 1607 | Sexyy Red | PRESI | commune | personne réelle | non |
| 1634 | TOP G | TOPG | commune | personne réelle | non |
| 1640 | URF | URF | commune | personne réelle, arnaque avérée | non |
| 1646 | 川普 (四川普通话) | 川普 | commune | politicien (nom ou histoire, sans drapeau) | non |
| AD1 | Official Trump | TRUMP | légendaire | à décider, politique | oui |
| AD2 | SafeMoon | SFM (ex-SAFEMOON) | légendaire | à décider, arnaque avérée | non |
| AD3 | Libra | LIBRA | légendaire | à décider | non |
| AD4 | Verge (ex-DogeCoinDark) | XVG | légendaire | à décider | non |
| AD5 | YZY | YZY | légendaire | à décider | non |
| AD6 | Melania Meme | MELANIA | légendaire | à décider, politique | oui |
| AD7 | Squid Game | SQUID | légendaire | à décider, arnaque avérée | non |
| AD8 | MAGA | TRUMP (ERC-20) | épique | à décider, politique | non |
| AD9 | Akuma Inu | AKUMA | épique | à décider | non |
| AD10 | Central African Republic Meme | CAR | épique | à décider, politique | non |
| AD11 | Jeo Boden | BODEN | épique | à décider, politique | non |
| AD12 | America Party | AMERICA | épique | à décider, politique | non |
| AD13 | Hawk Tuah | HAWK | épique | à décider, personne réelle | non |
| AD14 | Hatom | HTM | épique | à décider | non |
| AD15 | Ducky | DUCKY | épique | à décider | non |
| AD16 | MAGA Hat | MAGA | épique | à décider, politique | non |
| AD17 | AhaToken | AHT | épique | à décider | oui |
| AD18 | Retardio † | RETARDIO | épique | à décider, obscène | non |
| AD19 | Aavegotchi | GHST | épique | à décider | non |
| AD20 | M3M3 | M3M3 | épique | à décider | non |
| AD21 | TrumpCoin | DJT | épique | à décider, politique | non |
| AD22 | Daddy Tate | DADDY | épique | à décider, personne réelle | oui |
| AD23 | HempCoin | THC | épique | à décider | non |
| AD24 | Doland Tremp | TREMP | épique | à décider, politique | non |
| AD25 | Butthole Coin | BUTTHOLE | épique | à décider, obscène | non |
| AD26 | MimboGameGroup | MGG | épique | à décider | non |
| AD27 | Normie | NORMIE | épique | à décider | non |
| AD28 | Bald | BALD | épique | à décider | non |
| AD29 | Boner Coin | BONER | rare | à décider, obscène | oui |
| AD30 | Trust | TRUST | rare | à décider | non |
| AD31 | Carrot by Puffer | CARROT | rare | à décider | non |
| AD32 | 我踏马来了 | 我踏马来了 | rare | à décider, obscène | oui |
| AD33 | Private Aviation Finance Token | CINO | rare | à décider | non |
| AD34 | FTMTOKEN | FTMX | rare | à décider | oui |
| AD35 | Hawk | HAWK | rare | à décider, personne réelle | non |
| AD36 | Chudjak | CHUD | rare | à décider, obscène | non |
| AD37 | Testicle | TESTICLE | rare | à décider, obscène | non |
| AD38 | Chonketha the Wet Beaver | CHONKETHA | rare | à décider, obscène | oui |
| AD39 | Hunter Biden's Laptop | LAPTOP | commune | à décider, politique | oui |
| AD40 | ShibaBitcoin | SHIBTC | commune | à décider | non |
| AD41 | Skibidi Toilet | SKBDI | commune | à décider | non |
| AD42 | ArAIstotle | FACY | commune | à décider | non |
| AD43 | Mates | MATES | commune | à décider | non |
| AD44 | Gooncoin | GOONC | commune | à décider, obscène | non |
| AD45 | Super Trump | STRUMP | commune | à décider, politique | non |
| AD46 | Pussy Financial | PUSSY | commune | à décider, obscène | non |
| AD47 | RTR | RTR | commune | à décider, politique | non |
| AD48 | Jenner | JENNER | commune | à décider, personne réelle | non |
| AD49 | Opus Genesis | OPUS | commune | à décider | non |
| AD50 | AGENDA 47 | A47 | commune | à décider, politique | non |
| AD51 | Wolf | WOLF | commune | à décider | non |
| AD52 | Whoren | WHOREN | commune | à décider, obscène | non |
| AD53 | Jason Derulo | JASON | commune | à décider, personne réelle | non |
| AD54 | GrokCoin | GROKCOIN | commune | à décider | non |
| AD55 | Ben Coin (BitBoy) | BEN | commune | à décider, personne réelle | non |
| AD56 | DopeCoin | DOPE | commune | à décider | non |
| AD57 | SroomAI DAO | SHR0 | commune | à décider | non |
| AD58 | CannabisCoin | CANN | commune | à décider | non |
| AD59 | Kamala Horris † | KAMA | commune | à décider, politique | non |
| AD60 | Odin Liquidity Network | ODIN | commune | à décider | non |
| AD61 | uP Token | UP | commune | à décider | non |
| AD62 | Hulk Hogan | HULK | commune | à décider, personne réelle | non |
| AD63 | Hoodrat | HOODRAT | commune | à décider, obscène | non |
| AD64 | Danold Tromp | DANOLD | commune | à décider, politique | non |
| AD65 | TabbyPOS | TABBY | commune | à décider | non |
| AD66 | PutinCoin | PUT | commune | à décider, politique | non |
| AD67 | Red Kitten Crew | RKC | commune | à décider | non |
| AD68 | COQ AI | COQAI | commune | à décider | non |
| AD69 | Wanko | WANKO | commune | à décider, obscène | non |
| AD70 | Fapcoin | FAPCOIN | commune | à décider, obscène | oui |
| AD71 | CockCardano | COCK | commune | à décider, obscène | non |
| AD72 | TrumpCoin † | TRUMP | commune | à décider, politique | non |
| AD73 | Hunter Boden | HUNTER | commune | à décider, politique | non |
| AD74 | Groyper | GROYP | commune | à décider, obscène | non |
| AD75 | GanjaCoin | MRJA | commune | à décider | non |
| AD76 | LeafCoin | LEAF | commune | à décider | non |
| AD77 | CannaCoin | CCN | commune | à décider | non |
| AD78 | MechaHitler | MECHAHITLER | commune | à décider, obscène | non |
| AD79 | KushCoin | KUSH | commune | à décider | non |
| AD80 | HempCoin (HMP) | HMP | commune | à décider | non |
| AD81 | Sativacoin | STV | commune | à décider | non |
| AD82 | Marijuanacoin | MAR | commune | à décider | non |
| AD83 | Darkkush | DANK | commune | à décider | non |
| AD84 | CannabisDarkcoin | CND | commune | à décider | non |
| AD85 | WeedTokens | WETK | commune | à décider | non |
| AD86 | AIAI | AIAI | commune | à décider | non |
| AD87 | Barron | BARRON | commune | à décider, arnaque avérée, politicien (nom ou histoire, sans drapeau) | non |
| AD88 | Beratardio | à vérifier | commune | à décider, obscène | non |
| AD89 | Coinye | COINYE | commune | à décider | non |
| AD90 | CR7 | CR7 | commune | à décider, arnaque avérée | non |
| AD91 | Doja | DOJA | commune | à décider, personne réelle | non |
| AD92 | Elon Sperm | à vérifier | commune | à décider, obscène | non |
| AD93 | Enron | ENRON | commune | à décider | non |
| AD94 | EthereumMax | EMAX | commune | à décider, personne réelle | non |
| AD95 | Funky | FUNKY | commune | à décider, arnaque avérée | non |
| AD96 | Hood | HOOD | commune | à décider | non |
| AD97 | Jeton « Epstein » de McAfee | WHACKD | commune | à décider, personne réelle | non |
| AD98 | Mbappé | MBAPPE | commune | à décider, arnaque avérée | non |
| AD99 | Rich the Kid | RICH | commune | à décider, personne réelle | non |
| AD100 | Sydney Sweeney | SWEENEY | commune | à décider, personne réelle | non |
| AD101 | Vantard | VANTARD | commune | à décider, obscène | non |

## Cartes

| N° v2 | Nom | Ticker | Chaîne | Rareté | État | Brûlable | Raison |
|---|---|---|---|---|---|---|---|
| M1 | ? | ? | ? | mythique | ? | non | mythique scellée : jamais brûlable |
| M2 | ? | ? | ? | mythique | ? | non | mythique scellée : jamais brûlable |
| M3 | ? | ? | ? | mythique | ? | non | mythique scellée : jamais brûlable |
| 1 | Bonk | BONK | Solana | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `bonk` : volume 24 h 23,9 M$, capitalisation 248,8 M$ |
| 2 | dogwifhat † | WIF | Solana | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `dogwifcoin` : volume 24 h 26,1 M$, capitalisation 157,9 M$ |
| 3 | Memecoin † | MEME | Ethereum | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `memecoin-2` : volume 24 h 4,8 M$, capitalisation 24,7 M$ |
| 4 | Floki | FLOKI | Ethereum | légendaire | en déclin | oui | achetable : état « en déclin », CoinGecko `floki` : volume 24 h 12,8 M$, capitalisation 202,5 M$ |
| 5 | Fartcoin | FARTCOIN | Solana | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `fartcoin` : volume 24 h 12,2 M$, capitalisation 115,4 M$ |
| 6 | Brett † | BRETT | Base | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `based-brett` : volume 24 h 2,5 M$, capitalisation 36,5 M$ |
| 7 | Pudgy Penguins | PENGU | Solana | légendaire | en déclin | oui | achetable : état « en déclin », CoinGecko `pudgy-penguins` : volume 24 h 64,0 M$, capitalisation 391,6 M$ |
| 8 | Ordinals | ORDI | Bitcoin | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `ordinals` : volume 24 h 7,7 M$, capitalisation 67,1 M$ |
| 9 | SPX6900 | SPX | Ethereum | légendaire | en déclin | oui | achetable : état « en déclin », CoinGecko `spx6900` : volume 24 h 7,5 M$, capitalisation 340,2 M$ |
| 10 | Sats | SATS (1000SATS) | Bitcoin | légendaire | en déclin (-95 % ou pire) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 11 | Peanut the Squirrel | PNUT | Solana | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `peanut-the-squirrel` : volume 24 h 5,3 M$, capitalisation 32,9 M$ |
| 12 | Popcat † | POPCAT | Solana | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `popcat` : volume 24 h 4,0 M$, capitalisation 33,5 M$ |
| 13 | Book of Meme | BOME | Solana | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `book-of-meme` : volume 24 h 7,1 M$, capitalisation 41,9 M$ |
| 14 | Goatseus Maximus | GOAT | Solana | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `goatseus-maximus` : volume 24 h 992 k$, capitalisation 12,6 M$ |
| 15 | Neiro † | NEIRO | Ethereum | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `neiro-3` : volume 24 h 3,5 M$, capitalisation 24,9 M$ |
| 16 | cat in a dogs world † | MEW | Solana | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `cat-in-a-dogs-world` : volume 24 h 2,3 M$, capitalisation 30,6 M$ |
| 17 | DOG•GO•TO•THE•MOON | DOG | Bitcoin | légendaire | en déclin | oui | achetable : état « en déclin », CoinGecko `dog-go-to-the-moon-rune` : volume 24 h 458 k$, capitalisation 74,9 M$ |
| 18 | Dogelon Mars | ELON | Ethereum | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `dogelon-mars` : volume 24 h 1,3 M$, capitalisation 21,8 M$ |
| 19 | EverGrow | EGC | BNB Chain | légendaire | mort | non | état « mort » |
| 20 | Turbo | TURBO | Ethereum | légendaire | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `turbo` : volume 24 h 4,2 M$, capitalisation 48,1 M$ |
| 21 | analoS | ANALOS | Solana | légendaire | mort | non | état « mort » |
| 22 | Degen † | DEGEN | Base | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `degen-base` : volume 24 h 7,0 M$, capitalisation 29,0 M$ |
| 23 | Baby Doge Coin | BABYDOGE | BNB Chain | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `baby-doge-coin` : volume 24 h 1,3 M$, capitalisation 54,0 M$ |
| 24 | Loaded Lions | LION | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `loaded-lions` : volume 24 h 37 k$, capitalisation 31,9 M$ |
| 25 | Act I : The AI Prophecy † | ACT | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `act-i-the-ai-prophecy` : volume 24 h 21,7 M$, capitalisation 9,2 M$ |
| 26 | The Truth (UFO) | UFO | Ethereum | épique | mort | non | état « mort » |
| 27 | Toshi † | TOSHI | Base | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `toshi` : volume 24 h 2,2 M$, capitalisation 37,9 M$ |
| 28 | ConstitutionDAO | PEOPLE | Ethereum | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `constitutiondao` : volume 24 h 5,5 M$, capitalisation 29,5 M$ |
| 29 | Monacoin † | MONA | blockchain propre | épique | en déclin (3,8 M$ le 06/11/2026, -99,6 %) | non | liquidité insuffisante (CoinGecko `monacoin` : volume 24 h 897 $, capitalisation 6,1 M$ ; seuils 20 k$ et 1 M$) |
| 30 | My Paqman Coin | MPC | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `my-paqman-coin` : volume 24 h 0 $, capitalisation 18,1 M$ ; seuils 20 k$ et 1 M$) |
| 31 | Pippin † | PIPPIN | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `pippin` : volume 24 h 695 k$, capitalisation 12,5 M$ |
| 32 | Dogs † | DOGS | TON | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `dogs-2` : volume 24 h 3,7 M$, capitalisation 16,5 M$ |
| 33 | Just a chill guy † | CHILLGUY | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `chill-guy` : volume 24 h 3,2 M$, capitalisation 8,3 M$ |
| 34 | GEKKO | GEKKO | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `gekko` : volume 24 h 91 k$, capitalisation 45,6 M$ |
| 35 | Gigachad † | GIGA | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `gigachad-2` : volume 24 h 1,7 M$, capitalisation 16,2 M$ |
| 36 | Big Dog Fink | BINK | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `big-dog-fink` : volume 24 h 15 $, capitalisation 9,8 M$ ; seuils 20 k$ et 1 M$) |
| 37 | BUILDon | B | BNB Chain | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `build-on` : volume 24 h 3,1 M$, capitalisation 117,0 M$ |
| 38 | PepeCoin | PEPECOIN | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `pepecoin-2` : volume 24 h 117 k$, capitalisation 10,0 M$ |
| 39 | would | WOULD | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `would` : volume 24 h 1 k$, capitalisation 10,8 M$ ; seuils 20 k$ et 1 M$) |
| 40 | monKEYS | MONKEYS | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `monkeys-2` : volume 24 h 0 $, capitalisation 1,1 M$ ; seuils 20 k$ et 1 M$) |
| 41 | Snek † | SNEK | Cardano | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `snek` : volume 24 h 753 k$, capitalisation 35,7 M$ |
| 42 | CateCoin † | CATE | BNB Chain | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `catecoin` : volume 24 h 55 $, capitalisation 3,6 M$ ; seuils 20 k$ et 1 M$) |
| 43 | Slerf | SLERF | Solana | épique | en déclin | non | liquidité insuffisante (CoinGecko `slerf-2` : volume 24 h 3 k$, capitalisation 1,7 M$ ; seuils 20 k$ et 1 M$) |
| 44 | Moo Deng † | MOODENG | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `moo-deng` : volume 24 h 4,4 M$, capitalisation 30,5 M$ |
| 46 | Rekt | REKT | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `rekt-4` : volume 24 h 59 k$, capitalisation 23,3 M$ |
| 47 | Banana For Scale | BANANAS31 | BNB Chain | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `banana-for-scale-2` : volume 24 h 2,7 M$, capitalisation 58,7 M$ |
| 48 | Dora | DORA | BNB Chain | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `dora-2` : volume 24 h 38 $, capitalisation 1,8 M$ ; seuils 20 k$ et 1 M$) |
| 49 | The Doge NFT / Own The Doge | DOG | Ethereum | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `the-doge-nft` : volume 24 h 12 k$, capitalisation 5,3 M$ ; seuils 20 k$ et 1 M$) |
| 50 | Mononoke Inu | Mononoke-Inu | Ethereum | épique | mort | non | état « mort » |
| 51 | Non-Playable Coin | NPC | à vérifier | épique | actif | oui | achetable : état « actif », CoinGecko `non-playable-coin` : volume 24 h 4,3 M$, capitalisation 109,5 M$ |
| 52 | Binance Life (币安人生) | 币安人生 | BNB Chain | épique | actif | oui | achetable : état « actif », CoinGecko `bianrensheng` : volume 24 h 3,2 M$, capitalisation 492,6 M$ |
| 53 | Ryoshis Vision | RYOSHI | Ethereum | épique | mort | non | état « mort » |
| 54 | Simon's Cat | CAT | BNB Chain | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `simon-s-cat` : volume 24 h 626 k$, capitalisation 12,7 M$ |
| 55 | Beercoin | BEER | à vérifier | épique | mort | non | état « mort » |
| 56 | Test | TST | BNB Chain | épique | en déclin (≈ 11 M$, -97,7 %, encore du volume) | oui | achetable : état « en déclin », CoinGecko `test-3` : volume 24 h 9,8 M$, capitalisation 11,3 M$ |
| 57 | catgirl | CATGIRL | BNB Chain | épique | mort | non | état « mort » |
| 58 | Onyx Arches | OXA | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `onyx-arches` : volume 24 h 0 $, capitalisation 1,8 M$ ; seuils 20 k$ et 1 M$) |
| 59 | Unicorn Fart Dust | UFD | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `unicorn-fart-dust` : volume 24 h 638 k$, capitalisation 4,6 M$ |
| 60 | Believe | BELIEVE | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `ben-pasternak` : volume 24 h 1,2 M$, capitalisation 1,9 M$ |
| 61 | Coq Inu † | COQ | Avalanche | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `coq-inu` : volume 24 h 1,9 M$, capitalisation 6,3 M$ |
| 62 | Ponke † | PONKE | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `ponke` : volume 24 h 2,0 M$, capitalisation 9,4 M$ |
| 63 | Useless Coin | USELESS | Solana | épique | actif | oui | achetable : état « actif », CoinGecko `useless-3` : volume 24 h 11,5 M$, capitalisation 138,6 M$ |
| 64 | Bonfire | BONFIRE | BNB Chain | épique | en déclin | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 65 | Myro † | MYRO | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `myro` : volume 24 h 150 k$, capitalisation 1,3 M$ |
| 66 | Safemars | SAFEMARS | BNB Chain | épique | mort | non | état « mort » |
| 67 | PondCoin | PNDC | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `pond-coin` : volume 24 h 7 k$, capitalisation 6,2 M$ ; seuils 20 k$ et 1 M$) |
| 68 | Purr | PURR | Hyperliquid | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `purr-2` : volume 24 h 993 k$, capitalisation 54,0 M$ |
| 69 | RSIC•GENESIS•RUNE | RSIC | Bitcoin | épique | en déclin (-95 % ou pire) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 70 | CZ's Dog | BROCCOLI (BROCCOLI714) | BNB Chain | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `czs-dog` : volume 24 h 3,4 M$, capitalisation 16,1 M$ |
| 72 | Mog Coin | MOG | Ethereum | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `mog-coin` : volume 24 h 3,9 M$, capitalisation 35,5 M$ |
| 74 | PepeFork | PORK | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `pepefork` : volume 24 h 11 k$, capitalisation 4,7 M$ ; seuils 20 k$ et 1 M$) |
| 75 | Artificial Inu | AI | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `artificial-inu-3` : volume 24 h 3,1 M$, capitalisation 29,2 M$ |
| 76 | Kekius Maximus | KEKIUS | Ethereum | épique | actif | non | liquidité insuffisante (CoinGecko `kekius-maximus-6` : volume 24 h 584 $, capitalisation 12,4 M$ ; seuils 20 k$ et 1 M$) |
| 77 | Milady Meme Coin | LADYS | Ethereum | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `milady-meme-coin` : volume 24 h 138 k$, capitalisation 4,3 M$ |
| 78 | Comedian † | BAN | Solana | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `comedian` : volume 24 h 1,1 M$, capitalisation 45,8 M$ |
| 79 | Hoge Finance | HOGE | Ethereum | épique | mort | non | état « mort » |
| 80 | Milady Cult Coin | CULT | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `milady-cult-coin` : volume 24 h 144 k$, capitalisation 7,0 M$ |
| 81 | Fwog † | FWOG | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `fwog` : volume 24 h 1,0 M$, capitalisation 3,6 M$ |
| 82 | Katana Inu | KATA | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `katana-inu` : volume 24 h 13 k$, capitalisation 1,2 M$ ; seuils 20 k$ et 1 M$) |
| 83 | coco | COCO | à vérifier | épique | actif | oui | achetable : état « actif », CoinGecko `coco-2` : volume 24 h 42 k$, capitalisation 140,1 M$ |
| 84 | ANDY ETH | ANDY | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `andy-the-wisguy` : volume 24 h 96 k$, capitalisation 11,5 M$ |
| 85 | Wen † | WEN | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `wen-4` : volume 24 h 104 k$, capitalisation 3,9 M$ |
| 86 | Barsik | BARSIK | Solana | épique | mort | non | état « mort » |
| 87 | Luckycoin | LKY | à vérifier | épique | mort | non | état « mort » |
| 88 | DogeKing | DOGEKING | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `dogeking` : volume 24 h 40 k$, capitalisation 3,2 M$ |
| 89 | UNCOMMON•GOODS | UNCOMMONGOODS | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `uncommon-goods` : volume 24 h 12 $, capitalisation 2,1 M$ ; seuils 20 k$ et 1 M$) |
| 90 | CrazyBunny | CRAZYBUNNY | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `crazybunny` : volume 24 h 5 $, capitalisation 1,7 M$ ; seuils 20 k$ et 1 M$) |
| 91 | Osaka Protocol | OSAK | Avalanche | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `osaka-protocol` : volume 24 h 57 k$, capitalisation 11,4 M$ |
| 92 | Apu Apustaja | APU | Ethereum | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `apu-s-club` : volume 24 h 37 k$, capitalisation 3,3 M$ |
| 93 | Luce † | LUCE | Solana | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `offcial-mascot-of-the-holy-year` : volume 24 h 25 k$, capitalisation 266 k$ ; seuils 20 k$ et 1 M$) |
| 94 | Sundog | SUNDOG | Tron | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `sundog` : volume 24 h 40 k$, capitalisation 781 k$ ; seuils 20 k$ et 1 M$) |
| 95 | Cash Cat | CASHCAT | Robinhood Chain | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `cash-cat` : volume 24 h 11,4 M$, capitalisation 60,3 M$ |
| 96 | 龙虾 (Lobster) | 龙虾 | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `lobster-2` : volume 24 h 1,1 M$, capitalisation 18,0 M$ |
| 97 | Baby Shark Universe | BSU | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `baby-shark-universe` : volume 24 h 105 k$, capitalisation 1,3 M$ |
| 98 | PepeCoin on Solana | PEPE | à vérifier | épique | mort | non | état « mort » |
| 99 | Puff The Dragon | PUFF | Mantle | épique | mort | non | état « mort » |
| 100 | TDCCP | TDCCP | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `tdccp` : volume 24 h 15 k$, capitalisation 12,4 M$ ; seuils 20 k$ et 1 M$) |
| 101 | AMATERASU OMIKAMI | OMIKAMI | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `amaterasu-omikami` : volume 24 h 8 k$, capitalisation 4,4 M$ ; seuils 20 k$ et 1 M$) |
| 102 | Kuma Inu | KUMA | Ethereum | épique | mort | non | état « mort » |
| 103 | Kendu | KENDU | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `kendu-inu` : volume 24 h 972 $, capitalisation 1,8 M$ ; seuils 20 k$ et 1 M$) |
| 104 | ClassicDoge | XDOGE | BNB Chain | épique | mort | non | état « mort » |
| 105 | BitShiba | SHIBA | BNB Chain | épique | mort | non | état « mort » |
| 106 | mfercoin | MFER | Base | épique | mort | non | état « mort » |
| 107 | Apollo Inu | APOLLO | Ethereum | épique | mort | non | état « mort » |
| 108 | Cheems | CHEEMS | BNB Chain | épique | mort | non | état « mort » |
| 109 | Jelly-My-Jelly | JELLYJELLY | Solana | épique | en déclin | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 110 | Landwolf | WOLF | Ethereum | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `landwolf-0x67` : volume 24 h 315 k$, capitalisation 8,3 M$ |
| 111 | Hokkaidu Inu | HOKK | Ethereum | épique | mort | non | état « mort » |
| 112 | Wiki Cat | WKC | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `wiki-cat` : volume 24 h 152 k$, capitalisation 27,0 M$ |
| 113 | Mumu the Bull † | MUMU | Solana | épique | mort | non | état « mort » |
| 114 | 4 | 4 / FOUR | BNB Chain | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `4-2` : volume 24 h 768 k$, capitalisation 9,1 M$ |
| 115 | Shrub | SHRUB | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `shrub` : volume 24 h 28 k$, capitalisation 1,2 M$ |
| 116 | Mother Iggy | MOTHER | Solana | épique | mort | non | état « mort » |
| 117 | Vine Coin | VINE | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `vine` : volume 24 h 4,9 M$, capitalisation 5,7 M$ |
| 118 | SafeBitcoin | SAFEBTC | BNB Chain | épique | mort | non | état « mort » |
| 119 | Wise Monkey | MONKY | BNB Chain | épique | mort | non | état « mort » |
| 120 | Aura | AURA | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `aura-on-sol` : volume 24 h 295 k$, capitalisation 5,6 M$ |
| 121 | Tutorial | TUT | BNB Chain | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `tutorial` : volume 24 h 2,3 M$, capitalisation 13,7 M$ |
| 122 | Zombie Inu | ZINU | Ethereum | épique | mort | non | état « mort » |
| 123 | Bellscoin | BELLS | blockchain propre | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `bellscoin` : volume 24 h 77 k$, capitalisation 1,3 M$ |
| 124 | Billy † | BILLY | Solana | épique | mort | non | état « mort » |
| 125 | Shiba Predator | QOM | à vérifier | épique | mort | non | état « mort » |
| 126 | DogeGF | DOGEGF | à vérifier | épique | mort | non | état « mort » |
| 127 | PacMoon | PAC | Blast | épique | mort | non | état « mort » |
| 128 | DogeBonk | DOBO | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `dogebonk` : volume 24 h 2 $, capitalisation 2,4 M$ ; seuils 20 k$ et 1 M$) |
| 129 | GME (Solana) | GME | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `gme` : volume 24 h 451 k$, capitalisation 2,3 M$ |
| 131 | Luffy Inu | LUFFY | Ethereum | épique | mort | non | état « mort » |
| 132 | Mubarak | MUBARAK | BNB Chain | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `mubarak` : volume 24 h 5,0 M$, capitalisation 36,9 M$ |
| 133 | Nacho the Kat | NACHO | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `nacho-the-kat` : volume 24 h 2 k$, capitalisation 2,3 M$ ; seuils 20 k$ et 1 M$) |
| 134 | Sudeng | HIPPO | Sui | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `sudeng` : volume 24 h 1,9 M$, capitalisation 793 k$ ; seuils 20 k$ et 1 M$) |
| 135 | Stonks | STNK | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `stonks-4` : volume 24 h 7 k$, capitalisation 2,3 M$ ; seuils 20 k$ et 1 M$) |
| 136 | Maneki † | MANEKI | Solana | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `maneki` : volume 24 h 27 k$, capitalisation 2,0 M$ |
| 137 | McDull (Meme) | MCDULL | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `mcdull` : volume 24 h 390 $, capitalisation 5,9 M$ ; seuils 20 k$ et 1 M$) |
| 138 | Asteroid Shiba | ASTEROID | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `asteroid-shiba` : volume 24 h 98 k$, capitalisation 3,7 M$ |
| 139 | BasedHype | BASEDHYPE | à vérifier | épique | en déclin | non | liquidité insuffisante (CoinGecko `basedhype` : volume 24 h 0 $, capitalisation 34,1 M$ ; seuils 20 k$ et 1 M$) |
| 140 | MongCoin | MONG | Ethereum | épique | mort | non | état « mort » |
| 141 | MORI COIN | MORI | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `mori-coin` : volume 24 h 90 k$, capitalisation 2,6 M$ |
| 142 | Pepe Unchained | PEPU | Ethereum | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `pepe-unchained-2` : volume 24 h 31 k$, capitalisation 363 k$ ; seuils 20 k$ et 1 M$) |
| 143 | Clifford Inu | CLIFF | Ethereum | épique | mort | non | état « mort » |
| 144 | Conscious | CONSCIOUS | BNB Chain | épique | mort | non | état « mort » |
| 145 | WhiteWhale | WHITEWHALE | Solana | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `the-white-whale` : volume 24 h 28 k$, capitalisation 787 k$ ; seuils 20 k$ et 1 M$) |
| 146 | BULLA | BULLA | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `bulla-3` : volume 24 h 674 k$, capitalisation 25,5 M$ |
| 147 | Fartboy | FARTBOY | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `fartboy` : volume 24 h 118 k$, capitalisation 18,1 M$ |
| 148 | GreenHood | HOOD | à vérifier | épique | mort | non | état « mort » |
| 149 | Bert | BERT | Solana | épique | mort | non | état « mort » |
| 150 | MiniDOGE | MINIDOGE | BNB Chain | épique | mort | non | état « mort » |
| 151 | Ski Mask Dog † | SKI | Base | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `ski-mask-dog` : volume 24 h 25 k$, capitalisation 2,0 M$ |
| 152 | MarsMi | MARSMI | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `marsmi` : volume 24 h 353 k$, capitalisation 11,2 M$ |
| 153 | SATOSHI•NAKAMOTO | SATOSHI | Bitcoin | épique | mort | non | état « mort » |
| 154 | 360noscope420blazeit | MLG | à vérifier | épique | mort | non | état « mort » |
| 155 | Pepecoin | PEP | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `pepecoin-network` : volume 24 h 90 k$, capitalisation 7,5 M$ |
| 156 | Giggle Academy | GIGGLE | BNB Chain | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `giggle-fund` : volume 24 h 2,6 M$, capitalisation 28,1 M$ |
| 157 | Happy | HAPPY | Solana | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `happycat-2` : volume 24 h 549 k$, capitalisation 309 k$ ; seuils 20 k$ et 1 M$) |
| 158 | Shark Cat | SC | Solana | épique | mort | non | état « mort » |
| 159 | The Black Bull | ANSEM | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `the-black-bull` : volume 24 h 2,7 M$, capitalisation 22,3 M$ |
| 160 | Trollface | TROLL | Solana | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `troll-face` : volume 24 h 0 $, capitalisation 1,5 M$ ; seuils 20 k$ et 1 M$) |
| 162 | Based Pepe | PEPE | Base | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `based-pepe` : volume 24 h 600 $, capitalisation 2,3 M$ ; seuils 20 k$ et 1 M$) |
| 163 | Bertram The Pomeranian | BERT | à vérifier | épique | en déclin (-95 % ou pire, CoinGecko 11/11) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `bertram-the-pomeranian` : volume 24 h 618 k$, capitalisation 9,0 M$ |
| 164 | Shiba Samurai | SHIBURAI | Ethereum | épique | mort | non | état « mort » |
| 165 | NikolAI | NIKO | TON | épique | mort | non | état « mort » |
| 166 | Mooncoin † | MOON | blockchain propre | épique | à vérifier (homonyme sur CoinGecko, non rapproché) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 167 | Foxy | FOXY | Linea | épique | mort | non | état « mort » |
| 169 | "　" | "　" | à vérifier | épique | mort | non | état « mort » |
| 170 | Shoggoth | SHOGGOTH | à vérifier | épique | mort | non | état « mort » |
| 171 | Anonymous Cat | ZCAT | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `anonymous-cat` : volume 24 h 2,3 M$, capitalisation 21,8 M$ |
| 172 | GME (Ethereum) | GME | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `game-stop` : volume 24 h 18 k$, capitalisation 3,1 M$ ; seuils 20 k$ et 1 M$) |
| 173 | Penguin (à ne pas confondre avec Pudgy Penguins) | PENGUIN | Solana | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `nietzschean-penguin` : volume 24 h 85 k$, capitalisation 373 k$ ; seuils 20 k$ et 1 M$) |
| 174 | Peng | PENG | Solana | épique | mort | non | état « mort » |
| 175 | PeiPei | PEIPEI | Ethereum | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `peipeicoin-vip` : volume 24 h 3 k$, capitalisation 1,4 M$ ; seuils 20 k$ et 1 M$) |
| 176 | Tron Bull | BULL | Tron | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `tron-bull` : volume 24 h 474 $, capitalisation 1,0 M$ ; seuils 20 k$ et 1 M$) |
| 177 | Buff Doge Coin | DOGECOIN | BNB Chain | épique | mort | non | état « mort » |
| 178 | 牛来 (Niu Lai) | 牛来 | à vérifier | épique | actif | oui | achetable : état « actif », CoinGecko `niu-lai` : volume 24 h 7,5 M$, capitalisation 57,7 M$ |
| 179 | WHY | WHY | à vérifier | épique | mort | non | état « mort » |
| 180 | Grok | GROK | Ethereum | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `grok-2` : volume 24 h 117 k$, capitalisation 2,2 M$ |
| 181 | Keyboard Cat (Base) | KEYCAT | à vérifier | épique | en déclin (-95 % ou pire, CoinGecko 11/11) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `keyboard-cat-base` : volume 24 h 48 k$, capitalisation 4,3 M$ |
| 182 | Dejitaru Tsuka | TSUKA | Ethereum | épique | mort | non | état « mort » |
| 183 | GUMMY | GUMMY | Solana | épique | mort | non | état « mort » |
| 184 | ZynCoin | ZYN | Ethereum | épique | mort | non | état « mort » |
| 185 | Sigma | SIGMA | Solana | épique | en déclin (≈ 0,98 M$) | non | liquidité insuffisante (CoinGecko `sigma` : volume 24 h 7 k$, capitalisation 986 k$ ; seuils 20 k$ et 1 M$) |
| 186 | Billy (Bitcoin) | BILLY | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `billion-dollar-cat-runes` : volume 24 h 7 k$, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 187 | Rich Quack | QUACK | BNB Chain | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `richquack` : volume 24 h 17 $, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 188 | Wall Street Memes | WSM | Ethereum | épique | mort | non | état « mort » |
| 189 | A Meme Coin | AMC | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `a-meme-coin` : volume 24 h 1,1 M$, capitalisation 3,8 M$ |
| 190 | Miggles † | MIGGLES | Base | épique | mort | non | état « mort » |
| 191 | BILLION•DOLLAR•CAT | BDC | Bitcoin | épique | mort (absent de CoinGecko) | non | état « mort » |
| 192 | Bob † | BOB | Ethereum | épique | mort | non | état « mort » |
| 193 | Husky | HUSKY | Ethereum | épique | mort | non | état « mort » |
| 194 | Mongoose | MONGOOSE | à vérifier | épique | mort | non | état « mort » |
| 195 | GOHOME | GOHOME | à vérifier | épique | actif | oui | achetable : état « actif », CoinGecko `gohome` : volume 24 h 220 k$, capitalisation 39,1 M$ |
| 196 | Welsh Corgi Coin † | WELSH | Stacks | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `welsh-corgi-coin` : volume 24 h 763 $, capitalisation 1,2 M$ ; seuils 20 k$ et 1 M$) |
| 197 | 4Chan | 4CHAN | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `4chan` : volume 24 h 420 $, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 198 | Smoking Chicken Fish | SCF | Solana | épique | mort (≈ 0,32 M$) | non | état « mort » |
| 199 | Bongo | BONGO | Solana | épique | mort | non | état « mort » |
| 200 | Wojak Coin | WOJAK | Ethereum | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `wojak` : volume 24 h 705 $, capitalisation 1,4 M$ ; seuils 20 k$ et 1 M$) |
| 201 | Hoppy | HOPPY | Ethereum | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `hoppy-meme` : volume 24 h 40 k$, capitalisation 959 k$ ; seuils 20 k$ et 1 M$) |
| 202 | Keyboard Cat † | KEYCAT | Base | épique | mort | non | état « mort » |
| 203 | RyuJin | RYU | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `ryujin` : volume 24 h 5 k$, capitalisation 1,8 M$ ; seuils 20 k$ et 1 M$) |
| 204 | Silly Dragon | SILLY | Solana | épique | mort | non | état « mort » |
| 205 | 币安Holder (BNBHolder) | BNBHOLDER | BNB Chain | épique | mort (≈ 0,5 M$) | non | état « mort » |
| 206 | Resistance Dog | REDO | TON | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `resistance-dog` : volume 24 h 84 k$, capitalisation 4,0 M$ |
| 207 | Moonbirds | BIRB | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `moonbirds` : volume 24 h 6,5 M$, capitalisation 22,8 M$ |
| 208 | Miu | MIU | Sui | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `miu-2` : volume 24 h 46 k$, capitalisation 1,0 M$ |
| 209 | FEED EVERY GORILLA | FEG | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `feg-token-2` : volume 24 h 207 k$, capitalisation 2,6 M$ |
| 210 | Bad Idea AI | BAD | Ethereum | épique | mort | non | état « mort » |
| 211 | Goose Token | GOOSE | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `goose-token` : volume 24 h 0 $, capitalisation 3,4 M$ ; seuils 20 k$ et 1 M$) |
| 212 | PURPLE PEPE | PURPE | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `purple-pepe` : volume 24 h 59 k$, capitalisation 3,5 M$ |
| 213 | Star Wars Cat | SWCAT | BNB Chain | épique | mort | non | état « mort » |
| 214 | WATER | WATER | Solana | épique | mort | non | état « mort » |
| 215 | Hatch | HATCH | à vérifier | épique | mort | non | état « mort » |
| 216 | FarmerDoge | CROP | BNB Chain | épique | mort | non | état « mort » |
| 217 | ArbDoge AI † | AIDOGE | Arbitrum | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `arbdoge-ai` : volume 24 h 63 k$, capitalisation 1,3 M$ |
| 218 | Doginme † | DOGINME | Base | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `doginme` : volume 24 h 96 k$, capitalisation 4,1 M$ |
| 219 | Gork | GORK | Solana | épique | mort | non | état « mort » |
| 220 | Jeff | JEFF | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `jeff-3` : volume 24 h 2 k$, capitalisation 2,2 M$ ; seuils 20 k$ et 1 M$) |
| 221 | Fred the Convicted Raccoon | FRED | Solana | épique | mort | non | état « mort » |
| 222 | Troll | TROLL | à vérifier | épique | mort | non | état « mort » |
| 223 | TEDDY BEAR | BEAR | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `teddy-bear` : volume 24 h 16 k$, capitalisation 2,7 M$ ; seuils 20 k$ et 1 M$) |
| 224 | BABY WHITE HAMSTER | BWH | BNB Chain | épique | mort | non | état « mort » |
| 225 | Kitty Inu | Kitty | Ethereum | épique | mort | non | état « mort » |
| 226 | Pain | PAIN | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `pain` : volume 24 h 61 $, capitalisation 2,0 M$ ; seuils 20 k$ et 1 M$) |
| 227 | Torch of Liberty | LIBERTY | BNB Chain | épique | mort | non | état « mort » |
| 228 | MEME HORSE | MHORSE | à vérifier | épique | actif | oui | achetable : état « actif », CoinGecko `meme-horse` : volume 24 h 775 k$, capitalisation 49,4 M$ |
| 229 | Housecoin | HOUSE | Solana | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `housecoin-2` : volume 24 h 67 k$, capitalisation 576 k$ ; seuils 20 k$ et 1 M$) |
| 230 | Marscoin | MARSCOIN | BNB Chain | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `marscoin-4` : volume 24 h 5,3 M$, capitalisation 41,7 M$ |
| 231 | moonpig | MOONPIG | Solana | épique | mort (≈ 90 k$, volume nul) | non | état « mort » |
| 232 | Palu | PALU | BNB Chain | épique | mort (≈ 0,85 M$), -99,3 % → épique | non | état « mort » |
| 233 | EGL1 | EGL1 | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `egl1` : volume 24 h 1,5 M$, capitalisation 10,2 M$ |
| 234 | Koma Inu | KOMA | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `koma-inu` : volume 24 h 1,6 M$, capitalisation 7,9 M$ |
| 235 | Loser Coin | LOWB | Ethereum | épique | mort | non | état « mort » |
| 236 | Catbal | CATBAL | Hyperliquid | épique | en déclin | non | liquidité insuffisante (CoinGecko `catbal` : volume 24 h 6 k$, capitalisation 477 k$ ; seuils 20 k$ et 1 M$) |
| 237 | Bitcoin Bull | BTCBULL | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `bitcoin-bull-2` : volume 24 h 524 $, capitalisation 2,3 M$ ; seuils 20 k$ et 1 M$) |
| 238 | Lock In | LOCKIN | Solana | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `lock-in` : volume 24 h 103 k$, capitalisation 815 k$ ; seuils 20 k$ et 1 M$) |
| 239 | Crow with Knife | CAW | Ethereum | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `crow-with-knife` : volume 24 h 11 k$, capitalisation 3,9 M$ ; seuils 20 k$ et 1 M$) |
| 240 | Higher † | HIGHER | Base | épique | mort | non | état « mort » |
| 242 | Pikaboss | PIKA | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `pikaboss` : volume 24 h 2 k$, capitalisation 5,5 M$ ; seuils 20 k$ et 1 M$) |
| 243 | ANSEM | ANSEM | Solana | épique | mort (absent de CoinGecko) | non | état « mort » |
| 244 | XRP ARMY | ARMY | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `army-3` : volume 24 h 12 k$, capitalisation 3,4 M$ ; seuils 20 k$ et 1 M$) |
| 245 | Broccoli | BROCCOLI | à vérifier | épique | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `broccoli-3` : volume 24 h 2,0 M$, capitalisation 4,8 M$ |
| 246 | dogi | DOGI | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `dogi` : volume 24 h 48 $, capitalisation 1,8 M$ ; seuils 20 k$ et 1 M$) |
| 247 | AstroElon | ELONONE | à vérifier | épique | mort | non | état « mort » |
| 248 | Shiba Inu Treat | TREAT | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `shiba-inu-treat` : volume 24 h 35 k$, capitalisation 834 k$ ; seuils 20 k$ et 1 M$) |
| 249 | Meme Kombat | MK | Ethereum | épique | mort | non | état « mort » |
| 250 | Zack Morris | ZACK | Solana | épique | mort | non | état « mort » |
| 251 | Refund | RFD | à vérifier | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `refund` : volume 24 h 2 $, capitalisation 1,5 M$ ; seuils 20 k$ et 1 M$) |
| 252 | SNAP | NAP | Solana | épique | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `snap-kero` : volume 24 h 32 $, capitalisation 2,8 M$ ; seuils 20 k$ et 1 M$) |
| 253 | FART COIN | FRTC | à vérifier | épique | en déclin | oui | achetable : état « en déclin », CoinGecko `fart-coin` : volume 24 h 35 k$, capitalisation 14,8 M$ |
| 254 | Hamster | HAM | BNB Chain | épique | mort | non | état « mort » |
| 255 | Kiba Inu | KIBA | Ethereum | épique | mort | non | état « mort » |
| 256 | Moltbook | à vérifier | Base | épique | en déclin (-95 % ou pire) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 257 | LOBO•THE•WOLF•PUP | LOBO | Bitcoin | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `lobo-the-wolf-pup-runes` : volume 24 h 5 k$, capitalisation 31,5 M$ ; seuils 20 k$ et 1 M$) |
| 258 | lmeow | LMEOW | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `lmeow-2` : volume 24 h 5 k$, capitalisation 1,8 M$ ; seuils 20 k$ et 1 M$) |
| 259 | Monkey Pox | POX | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `monkey-pox` : volume 24 h 28 $, capitalisation 1,1 M$ ; seuils 20 k$ et 1 M$) |
| 260 | Official FO | FO | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `official-fo` : volume 24 h 35 k$, capitalisation 5,9 M$ |
| 261 | Slothana | SLOTH | Solana | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `slothana` : volume 24 h 573 $, capitalisation 1,9 M$ ; seuils 20 k$ et 1 M$) |
| 262 | Lucidum | LUCIC | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `lucidum` : volume 24 h 22 k$, capitalisation 16,2 M$ |
| 263 | Smole | SMOLE | Solana | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `smolecoin` : volume 24 h 35 $, capitalisation 7,1 M$ ; seuils 20 k$ et 1 M$) |
| 264 | DogBull | DOGO | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `dogbull` : volume 24 h 0 $, capitalisation 3,0 M$ ; seuils 20 k$ et 1 M$) |
| 265 | Baby Claw | BABYCLAW | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `baby-claw` : volume 24 h 0 $, capitalisation 91,4 M$ ; seuils 20 k$ et 1 M$) |
| 266 | PePeonTron | PEPEONTRON | Tron | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `pepeontron` : volume 24 h 174 k$, capitalisation 1,2 M$ |
| 267 | PooCoin | POOCOIN | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `poocoin` : volume 24 h 6 $, capitalisation 1,2 M$ ; seuils 20 k$ et 1 M$) |
| 268 | 哈基米 (Hakimi, Hajimi) | 哈基米 | BNB Chain | rare | en déclin (≈ 16 M$), -81 % | oui | achetable : état « en déclin », CoinGecko `hakimi` : volume 24 h 1,2 M$, capitalisation 16,2 M$ |
| 269 | Jesus Coin | JESUS | Ethereum | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `jesus-coin` : volume 24 h 543 $, capitalisation 2,0 M$ ; seuils 20 k$ et 1 M$) |
| 270 | Nobody Sausage | NOBODY | Solana | rare | en déclin (≈ 0,27 M$) | non | liquidité insuffisante (CoinGecko `nobody-sausage` : volume 24 h 3 k$, capitalisation 272 k$ ; seuils 20 k$ et 1 M$) |
| 271 | DOWGE | DJI6930 | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `dowge` : volume 24 h 153 k$, capitalisation 3,7 M$ |
| 272 | mini | MINI | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `minimini` : volume 24 h 26 k$, capitalisation 472 k$ ; seuils 20 k$ et 1 M$) |
| 273 | Daddy Doge | DADDYDOGE | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `daddy-doge` : volume 24 h 2 $, capitalisation 1,9 M$ ; seuils 20 k$ et 1 M$) |
| 274 | GeorgePlaysClashRoyale | CLASH | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `georgeplaysclashroyale` : volume 24 h 386 k$, capitalisation 5,7 M$ |
| 275 | Kabosu | KABOSU | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `kabosu` : volume 24 h 20 $, capitalisation 2,9 M$ ; seuils 20 k$ et 1 M$) |
| 276 | SquidGrow | SQGROW | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `squidgrow-2` : volume 24 h 9 k$, capitalisation 4,8 M$ ; seuils 20 k$ et 1 M$) |
| 277 | Mochi † | MOCHI | Base | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `mochi-thecatcoin` : volume 24 h 54 k$, capitalisation 577 k$ ; seuils 20 k$ et 1 M$) |
| 278 | Yummy | YUMMY | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `yummy` : volume 24 h 2 $, capitalisation 2,2 M$ ; seuils 20 k$ et 1 M$) |
| 279 | 4Stock | 4STOCK | BNB Chain | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `4stock` : volume 24 h 2,8 M$, capitalisation 2,1 M$ |
| 280 | AXOL | AXOL | Sui | rare | en déclin | non | liquidité insuffisante (CoinGecko `axol` : volume 24 h 5 k$, capitalisation 268 k$ ; seuils 20 k$ et 1 M$) |
| 281 | Basecat | BASECAT | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `basecat` : volume 24 h 1,5 M$, capitalisation 6,0 M$ |
| 282 | Qkacoin | QKA | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `qkacoin` : volume 24 h 2 k$, capitalisation 15,2 M$ ; seuils 20 k$ et 1 M$) |
| 283 | 8-Bit Coin | COIN | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `8-bit-coin` : volume 24 h 80 k$, capitalisation 2,7 M$ |
| 284 | Book of Ethereum | BOOE | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `book-of-ethereum` : volume 24 h 31 k$, capitalisation 3,1 M$ |
| 285 | Moolah | MOOLAH | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `moolah` : volume 24 h 290 k$, capitalisation 56,5 M$ |
| 286 | APES | APES | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `apes-2-2` : volume 24 h 0 $, capitalisation 72,1 M$ ; seuils 20 k$ et 1 M$) |
| 287 | Harambe | HARAMBE | Solana | rare | en déclin | non | liquidité insuffisante (CoinGecko `harambe` : volume 24 h 0 $, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 288 | The Spirit of Gambling | TOKABU | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `the-spirit-of-gambling` : volume 24 h 83 k$, capitalisation 1,3 M$ |
| 289 | Joe Coin | JOE | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `joe-coin` : volume 24 h 31 k$, capitalisation 4,3 M$ |
| 290 | Solama | SOLAMA | Solana | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `solama` : volume 24 h 31 k$, capitalisation 497 k$ ; seuils 20 k$ et 1 M$) |
| 291 | Unstable Coin | USDUC | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `unstable-coin` : volume 24 h 43 k$, capitalisation 1,8 M$ |
| 292 | MSTR2100 | MSTR | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `mstr2100` : volume 24 h 58 k$, capitalisation 369 k$ ; seuils 20 k$ et 1 M$) |
| 293 | Feisty Doge NFT | NFD | Ethereum | rare | en déclin | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 294 | Froggie | FROGGIE | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `froggie` : volume 24 h 70 k$, capitalisation 13,7 M$ |
| 295 | Manyu | MANYU | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `manyu-2` : volume 24 h 374 k$, capitalisation 2,7 M$ |
| 296 | Wownero | WOW | blockchain propre | rare | à vérifier | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 297 | Milo Inu | MILO | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `milo-inu` : volume 24 h 495 $, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 298 | ZZZ | ZZZ | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `zzz-2` : volume 24 h 1,0 M$, capitalisation 3,5 M$ |
| 299 | Cocoro | COCORO | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `cocoro` : volume 24 h 445 $, capitalisation 1,1 M$ ; seuils 20 k$ et 1 M$) |
| 300 | Vita Inu | VINU | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `vita-inu` : volume 24 h 108 k$, capitalisation 521 k$ ; seuils 20 k$ et 1 M$) |
| 301 | pipedog | PIPEDOG | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `pipedog` : volume 24 h 1,6 M$, capitalisation 4,4 M$ |
| 302 | PiP | PIP | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `pip-3` : volume 24 h 6 k$, capitalisation 1,0 M$ ; seuils 20 k$ et 1 M$) |
| 303 | Utya | UTYA | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `utya` : volume 24 h 380 k$, capitalisation 18,1 M$ |
| 304 | Wall Street Pepe | WEPE | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `wall-street-pepe` : volume 24 h 24 k$, capitalisation 928 k$ ; seuils 20 k$ et 1 M$) |
| 305 | Byte | BYTE | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `byte` : volume 24 h 34 k$, capitalisation 1,4 M$ |
| 306 | Crob Mob | CROB | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `crob-mob` : volume 24 h 79 $, capitalisation 6,6 M$ ; seuils 20 k$ et 1 M$) |
| 307 | Dessa | DESSA | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `dessa` : volume 24 h 1,6 M$, capitalisation 10,3 M$ |
| 308 | Boss | BOSS | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `boss` : volume 24 h 1 k$, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 309 | Build On BNB | BOB | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `build-on-bnb` : volume 24 h 381 k$, capitalisation 2,3 M$ |
| 310 | Kori | KORI | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `kori` : volume 24 h 29 k$, capitalisation 1,7 M$ |
| 311 | USCR | USCR | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `uscr` : volume 24 h 2 k$, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 312 | Chump Coin | CHUMP | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `chump-coin` : volume 24 h 1,2 M$, capitalisation 2,3 M$ |
| 313 | Gorbagana | GOR | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `gorbagana` : volume 24 h 26 k$, capitalisation 429 k$ ; seuils 20 k$ et 1 M$) |
| 314 | MUSHROOM | SHROOM | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `mushroom-2` : volume 24 h 34 k$, capitalisation 1,1 M$ |
| 315 | Not in Employment, Education, or Training | NEET | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `neet` : volume 24 h 1,1 M$, capitalisation 27,4 M$ |
| 316 | Dogz | DOGZ | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `dogz` : volume 24 h 0 $, capitalisation 1,2 M$ ; seuils 20 k$ et 1 M$) |
| 317 | CREPE | CREPE | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `crepe-2` : volume 24 h 138 k$, capitalisation 5,1 M$ |
| 318 | HoodPork | PORKU | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `hoodpork` : volume 24 h 0 $, capitalisation 15,9 M$ ; seuils 20 k$ et 1 M$) |
| 319 | Pwease | PWEASE | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `pwease` : volume 24 h 80 k$, capitalisation 3,1 M$ |
| 320 | wojak | WOJAK | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `wojak-5` : volume 24 h 973 k$, capitalisation 13,0 M$ |
| 321 | Bullish Degen | BULLISH | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `bullish-degen` : volume 24 h 36 k$, capitalisation 302 k$ ; seuils 20 k$ et 1 M$) |
| 322 | noice | NOICE | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `noice` : volume 24 h 27 k$, capitalisation 764 k$ ; seuils 20 k$ et 1 M$) |
| 323 | Baby Shiba Inu | BABYSHIBAINU | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `baby-shiba-inu` : volume 24 h 336 $, capitalisation 6,0 M$ ; seuils 20 k$ et 1 M$) |
| 324 | CaptainBNB | CaptainBNB | BNB Chain | rare | en déclin (≈ 1,7 M$, volume nul) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 325 | Hege | HEGE | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `hege` : volume 24 h 1 k$, capitalisation 1,2 M$ ; seuils 20 k$ et 1 M$) |
| 326 | Hosky † | HOSKY | Cardano | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `hosky` : volume 24 h 2 k$, capitalisation 4,2 M$ ; seuils 20 k$ et 1 M$) |
| 327 | IlluminatiCoin | NATI | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `illuminaticoin` : volume 24 h 43 $, capitalisation 4,3 M$ ; seuils 20 k$ et 1 M$) |
| 328 | Lofi | LOFI | Sui | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `lofi-2` : volume 24 h 132 k$, capitalisation 8,4 M$ |
| 329 | TEH EPIK DUCK | EPIK | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `teh-epik-duck` : volume 24 h 675 k$, capitalisation 1,5 M$ |
| 330 | WUFFI | WUF | Wax | rare | à vérifier | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 332 | I love puppies | PUPPIES | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `i-love-puppies` : volume 24 h 439 k$, capitalisation 5,4 M$ |
| 333 | KNOTS | KNOTS | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `knots` : volume 24 h 975 k$, capitalisation 1,8 M$ |
| 334 | Pandacoin | PND | blockchain propre | rare | en déclin | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 335 | Sosana | SOSANA | Solana | rare | en déclin | non | liquidité insuffisante (CoinGecko `sosana` : volume 24 h 2 k$, capitalisation 4,4 M$ ; seuils 20 k$ et 1 M$) |
| 336 | XDOG | XDOG | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `xdog` : volume 24 h 544 k$, capitalisation 1,4 M$ |
| 337 | 客服小何 (Customer Service Xiao He) | 客服小何 | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `customer-service-xiao-he` : volume 24 h 426 k$, capitalisation 1,7 M$ |
| 338 | Dingocoin | DINGO | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `dingocoin` : volume 24 h 37 k$, capitalisation 1,4 M$ |
| 339 | KiboShib | KIBSHI | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `kiboshib` : volume 24 h 5 k$, capitalisation 1,5 M$ ; seuils 20 k$ et 1 M$) |
| 340 | Manifesting | MANIFEST | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `manifesting` : volume 24 h 186 k$, capitalisation 3,5 M$ |
| 341 | The Bitcoin Bull | TBB | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `the-bitcoin-bull` : volume 24 h 33 k$, capitalisation 1,9 M$ |
| 342 | Blub | BLUB | Sui | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `blub` : volume 24 h 2 k$, capitalisation 1,9 M$ ; seuils 20 k$ et 1 M$) |
| 343 | Everybody | HOLD | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `everybody` : volume 24 h 10 k$, capitalisation 3,1 M$ ; seuils 20 k$ et 1 M$) |
| 344 | Froge | FROGE | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `frogevip` : volume 24 h 33 k$, capitalisation 558 k$ ; seuils 20 k$ et 1 M$) |
| 345 | Aura Final Boss | KIMCHI | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `aura-final-boss-2` : volume 24 h 635 k$, capitalisation 2,2 M$ |
| 346 | microduck | MICRODUCK | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `microduck` : volume 24 h 1,1 M$, capitalisation 2,8 M$ |
| 347 | Pundu | PUNDU | Solana | rare | en déclin | non | liquidité insuffisante (CoinGecko `pundu` : volume 24 h 2 $, capitalisation 1,9 M$ ; seuils 20 k$ et 1 M$) |
| 348 | XDOGE | XDOGE | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `xdoge-2` : volume 24 h 895 $, capitalisation 1,1 M$ ; seuils 20 k$ et 1 M$) |
| 349 | Coding Dino | DINO | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `coding-dino` : volume 24 h 204 k$, capitalisation 1,2 M$ |
| 350 | Doge KaKi | KAKI | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `doge-kaki` : volume 24 h 4 $, capitalisation 1,6 M$ ; seuils 20 k$ et 1 M$) |
| 351 | The Official 67 Coin | 67 | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `the-official-67-coin` : volume 24 h 391 k$, capitalisation 1,2 M$ |
| 352 | BabyCashCat | BABY | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `babycashcat` : volume 24 h 0 $, capitalisation 3,6 M$ ; seuils 20 k$ et 1 M$) |
| 353 | Memory cow Moo | MOO | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `memory-cow-moo` : volume 24 h 971 k$, capitalisation 730 k$ ; seuils 20 k$ et 1 M$) |
| 354 | Moochii | MOOCHII | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `moochii` : volume 24 h 51 $, capitalisation 1,2 M$ ; seuils 20 k$ et 1 M$) |
| 355 | NYC | NYC | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `nyc-token` : volume 24 h 0 $, capitalisation 25,4 M$ ; seuils 20 k$ et 1 M$) |
| 356 | 1 Coin Can Change Your Life | 1-COIN-CAN-CHANGE-YOUR-LIFE | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `1-coin-can-change-your-life` : volume 24 h 341 k$, capitalisation 307 k$ ; seuils 20 k$ et 1 M$) |
| 357 | Jimothy The Raccoon | JIMOTHY | Solana | rare | en déclin (≈ 1,1 M$) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 358 | DebtReliefBot | DRB | Base | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `debtreliefbot` : volume 24 h 177 k$, capitalisation 7,9 M$ |
| 359 | Jager Hunter | JAGER | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `jager-hunter` : volume 24 h 11 k$, capitalisation 5,0 M$ ; seuils 20 k$ et 1 M$) |
| 360 | StupidCoin | STUPID | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `stupidcoin-2` : volume 24 h 36 k$, capitalisation 231 k$ ; seuils 20 k$ et 1 M$) |
| 361 | TENDIES | TENDIES | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `tendies-2` : volume 24 h 1,0 M$, capitalisation 3,0 M$ |
| 362 | ubik | UBIK | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `ubik` : volume 24 h 1,1 M$, capitalisation 5,3 M$ |
| 363 | apeonfone | FONE | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `apeonfone` : volume 24 h 1,3 M$, capitalisation 1,3 M$ |
| 364 | Araracoin | ARARA | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `araracoin` : volume 24 h 17 k$, capitalisation 16,2 M$ ; seuils 20 k$ et 1 M$) |
| 365 | Claude Crab | CRABAI | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `claude-crab` : volume 24 h 20 k$, capitalisation 14,8 M$ |
| 366 | KiraKuru | KRA | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `kirakuru` : volume 24 h 0 $, capitalisation 2,7 M$ ; seuils 20 k$ et 1 M$) |
| 367 | BonkEarn | BERN | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `bonkearn` : volume 24 h 1 k$, capitalisation 1,0 M$ ; seuils 20 k$ et 1 M$) |
| 368 | Fuzzybear | FUZZY | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `fuzzybear` : volume 24 h 107 k$, capitalisation 16,2 M$ |
| 369 | Most Wanted | MOST | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `most-wanted-2` : volume 24 h 2 k$, capitalisation 2,8 M$ ; seuils 20 k$ et 1 M$) |
| 370 | Thinking Cat | HMM | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `thinking-cat` : volume 24 h 1,3 M$, capitalisation 5,8 M$ |
| 372 | SIXSEVEN | 67 | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `sixseven` : volume 24 h 2 k$, capitalisation 9,0 M$ ; seuils 20 k$ et 1 M$) |
| 373 | Buy the DIP | DIP | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `buy-the-dip` : volume 24 h 128 $, capitalisation 2,3 M$ ; seuils 20 k$ et 1 M$) |
| 374 | Gstock | GSTOCK | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `gstock` : volume 24 h 1,3 M$, capitalisation 3,6 M$ |
| 375 | Cets On Gold | CETS | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `cets-on-gold` : volume 24 h 1,4 M$, capitalisation 1,4 M$ |
| 376 | FLORK | FLORK | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `flork-3` : volume 24 h 150 k$, capitalisation 1,7 M$ |
| 377 | Giggle Mascot | MAX | à vérifier | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `giggle-mascot` : volume 24 h 67 k$, capitalisation 1,5 M$ |
| 378 | IKUN | IKUN | Solana | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `ikun` : volume 24 h 26 k$, capitalisation 49 k$ ; seuils 20 k$ et 1 M$) |
| 379 | Pofu | POFU | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `pofu` : volume 24 h 6 $, capitalisation 5,2 M$ ; seuils 20 k$ et 1 M$) |
| 380 | PUMPSTOP | XCAT | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `pumpstop` : volume 24 h 23 k$, capitalisation 18,0 M$ |
| 381 | The Stonks Exchange | STONKEX | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `the-stonks-exchange` : volume 24 h 815 k$, capitalisation 990 k$ ; seuils 20 k$ et 1 M$) |
| 382 | KarenCoin | KAREN | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `karencoin` : volume 24 h 39 $, capitalisation 1,6 M$ ; seuils 20 k$ et 1 M$) |
| 383 | Little John | JOHN | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `little-john` : volume 24 h 0 $, capitalisation 17,2 M$ ; seuils 20 k$ et 1 M$) |
| 385 | Harold | HAROLD | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `haroldonsol` : volume 24 h 115 k$, capitalisation 15,2 M$ |
| 386 | Luxxcoin | LUX | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `luxxcoin` : volume 24 h 0 $, capitalisation 3,0 M$ ; seuils 20 k$ et 1 M$) |
| 387 | Memetern | MXT | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `memetern` : volume 24 h 0 $, capitalisation 5,0 M$ ; seuils 20 k$ et 1 M$) |
| 388 | Volt Inu | VOLT | Ethereum | rare | actif | non | liquidité insuffisante (CoinGecko `volt-inu-3` : volume 24 h 5 k$, capitalisation 2,7 M$ ; seuils 20 k$ et 1 M$) |
| 389 | Yee Token | YEE | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `yee-token` : volume 24 h 429 k$, capitalisation 4,0 M$ |
| 390 | catwifmask | MASK | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `catwifmask` : volume 24 h 28 k$, capitalisation 904 k$ ; seuils 20 k$ et 1 M$) |
| 391 | Chill House | CHILLHOUSE | Solana | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `chill-house` : volume 24 h 316 k$, capitalisation 655 k$ ; seuils 20 k$ et 1 M$) |
| 392 | NutCoin | NUT | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `nutcoin-meme` : volume 24 h 374 k$, capitalisation 233 k$ ; seuils 20 k$ et 1 M$) |
| 393 | Salute | SLT | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `salute` : volume 24 h 2 k$, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 394 | Super Inu | SI | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `super-inu-3` : volume 24 h 2,2 M$, capitalisation 16,9 M$ |
| 395 | 401jK | 401JK | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `401jk` : volume 24 h 25 k$, capitalisation 724 k$ ; seuils 20 k$ et 1 M$) |
| 396 | ALLINU | ALLINU | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `allinu` : volume 24 h 1,1 M$, capitalisation 2,3 M$ |
| 397 | Dacity Coin | DACITY | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `dacity-coin-4` : volume 24 h 2,1 M$, capitalisation 17,7 M$ |
| 398 | GIVEBACK | GBACK | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `giveback` : volume 24 h 13 k$, capitalisation 3,6 M$ ; seuils 20 k$ et 1 M$) |
| 399 | Chomolon Joff | JOFF | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `chomolon-joff` : volume 24 h 37 k$, capitalisation 5,3 M$ |
| 400 | Tung Tung | TRIPLET | Solana | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `tung-tung-tung-sahur-2` : volume 24 h 215 k$, capitalisation 2,6 M$ |
| 401 | Bear Champ | BCHAMP | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `bear-champ` : volume 24 h 2 k$, capitalisation 4,6 M$ ; seuils 20 k$ et 1 M$) |
| 402 | BORGY | BORGY | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `borgy` : volume 24 h 2 k$, capitalisation 1,9 M$ ; seuils 20 k$ et 1 M$) |
| 403 | PEPE 0x69 ON BASE | PEPE | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `pepe-0x69-on-base` : volume 24 h 24 k$, capitalisation 154 k$ ; seuils 20 k$ et 1 M$) |
| 404 | Pepes Dog | ZEUS | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `pepes-dog` : volume 24 h 24 k$, capitalisation 720 k$ ; seuils 20 k$ et 1 M$) |
| 405 | PulseChain Peacock | PCOCK | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `pulsechain-peacock` : volume 24 h 33 k$, capitalisation 6,7 M$ |
| 406 | Robin the Frog | ROBIN | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `robin-the-frog` : volume 24 h 115 k$, capitalisation 344 k$ ; seuils 20 k$ et 1 M$) |
| 407 | BLUE CHIP | BLUECHIP | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `blue-chip-4` : volume 24 h 411 k$, capitalisation 2,3 M$ |
| 408 | CyberLeek | CYBERLEEK | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `cyberleek` : volume 24 h 1,7 M$, capitalisation 1,6 M$ |
| 409 | RUSSELL | RUSSELL | Base | rare | en déclin | non | liquidité insuffisante (CoinGecko `russell` : volume 24 h 7 k$, capitalisation 902 k$ ; seuils 20 k$ et 1 M$) |
| 410 | Bobo | BOBO | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `bobo-coin-2` : volume 24 h 478 k$, capitalisation 5,0 M$ |
| 411 | Bundle Cat | BUN | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `bundle-cat` : volume 24 h 1,5 M$, capitalisation 6,1 M$ |
| 412 | Buy The Cat | BTC | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `buy-the-cat` : volume 24 h 21 k$, capitalisation 504 k$ ; seuils 20 k$ et 1 M$) |
| 413 | Pup Doge | PUPDOGE | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `pup-doge` : volume 24 h 42 $, capitalisation 1,6 M$ ; seuils 20 k$ et 1 M$) |
| 414 | Theros | THEROS | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `theros` : volume 24 h 15 k$, capitalisation 15,4 M$ ; seuils 20 k$ et 1 M$) |
| 415 | Tsuki | TSUKI | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `tsuki` : volume 24 h 44 k$, capitalisation 2,4 M$ |
| 417 | FOMO人生 | FOMO人生 | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `fomo-life` : volume 24 h 25 k$, capitalisation 12,9 M$ |
| 418 | Hachiko | HACHI | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `hachiko-3` : volume 24 h 32 k$, capitalisation 620 k$ ; seuils 20 k$ et 1 M$) |
| 419 | HUNDRED | HUNDRED | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `hundred` : volume 24 h 2 k$, capitalisation 21,6 M$ ; seuils 20 k$ et 1 M$) |
| 420 | 旺柴 (WangChai) | 旺柴 | BNB Chain | rare | en déclin (≈ 1,7 M$) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 421 | Freedom of Money | FREEDOM OF MONEY | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `freedom-of-money` : volume 24 h 50 k$, capitalisation 1,3 M$ |
| 422 | MyOnion.fun | ONION | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `myonion-fun` : volume 24 h 0 $, capitalisation 22,3 M$ ; seuils 20 k$ et 1 M$) |
| 423 | NEFE COIN | NEFE | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `nefe-coin` : volume 24 h 382 $, capitalisation 17,4 M$ ; seuils 20 k$ et 1 M$) |
| 424 | The Toad Pepe | TOAD | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `the-toad-pepe` : volume 24 h 378 k$, capitalisation 672 k$ ; seuils 20 k$ et 1 M$) |
| 425 | CROCAT | CROCAT | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `crocat` : volume 24 h 10 k$, capitalisation 2,5 M$ ; seuils 20 k$ et 1 M$) |
| 426 | Icy | IC | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `icy` : volume 24 h 43 $, capitalisation 1,1 M$ ; seuils 20 k$ et 1 M$) |
| 427 | Let's BONK | LETSBONK | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `lets-bonk` : volume 24 h 35 k$, capitalisation 186 k$ ; seuils 20 k$ et 1 M$) |
| 428 | The Juggernaut | JUGGERNAUT | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `the-juggernaut` : volume 24 h 1,1 M$, capitalisation 2,3 M$ |
| 429 | BCOQ INU | BCOQ | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `bcoq-inu` : volume 24 h 25 k$, capitalisation 127 k$ ; seuils 20 k$ et 1 M$) |
| 430 | CRONUS | CRONUS | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `cronus-2` : volume 24 h 6 k$, capitalisation 3,9 M$ ; seuils 20 k$ et 1 M$) |
| 431 | DROP | DROP | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `drop-2` : volume 24 h 13 k$, capitalisation 2,3 M$ ; seuils 20 k$ et 1 M$) |
| 432 | The Bitcoin Mascot | BITTY | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `the-bitcoin-mascot` : volume 24 h 39 k$, capitalisation 925 k$ ; seuils 20 k$ et 1 M$) |
| 433 | The Last Play | RETIRE | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `the-last-play` : volume 24 h 312 k$, capitalisation 2,2 M$ |
| 435 | Cryptocurrency Coin | CRYPTO | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `cryptocurrency-coin` : volume 24 h 7 k$, capitalisation 2,2 M$ ; seuils 20 k$ et 1 M$) |
| 436 | Ket | KET | Solana | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `ket-3` : volume 24 h 1,0 M$, capitalisation 1,9 M$ |
| 437 | Mars | MARS | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `mars-2` : volume 24 h 25 k$, capitalisation 100 k$ ; seuils 20 k$ et 1 M$) |
| 438 | Xavier: Renegade Angel | XAVIER | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `xavier-renegade-angel` : volume 24 h 5 k$, capitalisation 1,1 M$ ; seuils 20 k$ et 1 M$) |
| 439 | donotfomoew | MOEW | Base | rare | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `moew` : volume 24 h 157 k$, capitalisation 1,2 M$ |
| 440 | JOBCOIN | JOBCOIN | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `jobcoin-2` : volume 24 h 30 k$, capitalisation 4,5 M$ |
| 441 | memestock | MEMESTOCK | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `memestock-3` : volume 24 h 25 k$, capitalisation 1,1 M$ |
| 442 | Rain Coin | RAIN | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `rain-coin` : volume 24 h 8 k$, capitalisation 2,7 M$ ; seuils 20 k$ et 1 M$) |
| 443 | PHNIX | PHNIX | Xrp Ledger | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `phnix` : volume 24 h 93 k$, capitalisation 4,1 M$ |
| 444 | Copper (inu) | COPPERINU | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `copper-inu-2` : volume 24 h 25 k$, capitalisation 110 k$ ; seuils 20 k$ et 1 M$) |
| 446 | frong | FRONG | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `frong` : volume 24 h 91 k$, capitalisation 1,6 M$ |
| 447 | LC SHIB | LC | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `lc-shib` : volume 24 h 63 k$, capitalisation 633 k$ ; seuils 20 k$ et 1 M$) |
| 448 | V2EX | V2EX | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `v2ex` : volume 24 h 636 $, capitalisation 1,9 M$ ; seuils 20 k$ et 1 M$) |
| 449 | 施工猫 (Construction Cat) | SUE | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `shi-gong-mao` : volume 24 h 178 k$, capitalisation 149 k$ ; seuils 20 k$ et 1 M$) |
| 450 | 老子 | 老子 | BNB Chain | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `laozi` : volume 24 h 377 k$, capitalisation 396 k$ ; seuils 20 k$ et 1 M$) |
| 451 | Gasspas | GASS | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `gasspas` : volume 24 h 28 k$, capitalisation 229 k$ ; seuils 20 k$ et 1 M$) |
| 452 | GOATED | GOATED | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `goated-2` : volume 24 h 0 $, capitalisation 3,5 M$ ; seuils 20 k$ et 1 M$) |
| 453 | Italian Brainrot | ITALIANROT | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `italian-brainrot` : volume 24 h 33 k$, capitalisation 77 k$ ; seuils 20 k$ et 1 M$) |
| 454 | Jean Phil | JEANPHIL | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `jean-phil` : volume 24 h 995 k$, capitalisation 3,2 M$ |
| 455 | Loaf Token | LOAF | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `loaf-token` : volume 24 h 37 $, capitalisation 1,7 M$ ; seuils 20 k$ et 1 M$) |
| 456 | LUCKY | LUCKY | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `lucky` : volume 24 h 48 k$, capitalisation 1,5 M$ |
| 457 | Real World AI | RWA | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `real-world-ai` : volume 24 h 9 k$, capitalisation 1,4 M$ ; seuils 20 k$ et 1 M$) |
| 458 | Agrippa | AGRIPPA | à vérifier | rare | en déclin (-95 % ou pire, CoinGecko 11/11) | non | liquidité insuffisante (CoinGecko `agrippa` : volume 24 h 21 k$, capitalisation 205 k$ ; seuils 20 k$ et 1 M$) |
| 459 | Barking Puppy | BP | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `barking-puppy` : volume 24 h 55 k$, capitalisation 1,5 M$ |
| 460 | Jotchua | JOTCHUA | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `jotchua` : volume 24 h 889 k$, capitalisation 1,8 M$ |
| 461 | Nya | NYA | Avalanche | rare | en déclin | non | liquidité insuffisante (CoinGecko `nya` : volume 24 h 2 k$, capitalisation 1,6 M$ ; seuils 20 k$ et 1 M$) |
| 462 | Stairway to gold | GOLD | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `stairway-to-gold` : volume 24 h 12 k$, capitalisation 10,2 M$ ; seuils 20 k$ et 1 M$) |
| 463 | The Original Doge | OGDOGE | à vérifier | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `the-original-doge` : volume 24 h 83 k$, capitalisation 566 k$ ; seuils 20 k$ et 1 M$) |
| 464 | 雪球 (Snowball) | 雪球 | BNB Chain | rare | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `xuequi` : volume 24 h 100 k$, capitalisation 445 k$ ; seuils 20 k$ et 1 M$) |
| 465 | 1000PEPPER | 1000PEPPER | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `1000pepper` : volume 24 h 202 k$, capitalisation 4,1 M$ |
| 466 | ALD | ALD | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `ald` : volume 24 h 216 k$, capitalisation 4,6 M$ |
| 467 | ALLINDOGE | ALLINDOGE | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `allindoge` : volume 24 h 19 k$, capitalisation 1,7 M$ ; seuils 20 k$ et 1 M$) |
| 468 | BEARXRPL | BEAR | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `bearxrpl` : volume 24 h 5 k$, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 469 | BORED | BORED | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `edison-bored` : volume 24 h 0 $, capitalisation 1,5 M$ ; seuils 20 k$ et 1 M$) |
| 470 | GongFu | GF | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `gongfu` : volume 24 h 1 k$, capitalisation 2,1 M$ ; seuils 20 k$ et 1 M$) |
| 471 | SCHIFFY | SCHIFFY | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `schiffy` : volume 24 h 699 k$, capitalisation 2,1 M$ |
| 472 | Z李REAL SUPER COIN | ZREAL | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `zreal-super-coin` : volume 24 h 4 k$, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 473 | dopameme | DOPAMEME | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `dopameme-2` : volume 24 h 24 k$, capitalisation 669 k$ ; seuils 20 k$ et 1 M$) |
| 474 | PEPECAT | PEPECAT | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `pepecat-2` : volume 24 h 31 k$, capitalisation 5,7 M$ |
| 475 | Quq | QUQ | BNB Chain | rare | en déclin (≈ 1,6 M$, mais volume farmé énorme) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 476 | Strategy Coin | STRATEGY | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `strategy-coin` : volume 24 h 12 k$, capitalisation 1,9 M$ ; seuils 20 k$ et 1 M$) |
| 477 | ༼ つ ◕_◕ ༽つ | GIB | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `_` : volume 24 h 3 k$, capitalisation 1,7 M$ ; seuils 20 k$ et 1 M$) |
| 478 | Baby Floki | BABYFLOKI | BNB Chain | rare | en déclin | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 479 | Garlicoin | GRLC | blockchain propre | rare | en déclin (0,52 M$ le 06/11/2026) | non | liquidité insuffisante (CoinGecko `garlicoin` : volume 24 h 0 $, capitalisation 410 k$ ; seuils 20 k$ et 1 M$) |
| 480 | Paper Plane | PLANE | TON | rare | en déclin | non | liquidité insuffisante (CoinGecko `paper-plane` : volume 24 h 4 k$, capitalisation 277 k$ ; seuils 20 k$ et 1 M$) |
| 481 | Claudia | CLAUDIA | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `claudia-2` : volume 24 h 2,9 M$, capitalisation 4,9 M$ |
| 482 | FATCAT | FATCAT | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `fatcat-4` : volume 24 h 94 k$, capitalisation 3,4 M$ |
| 483 | LOULOU | LOULOU | à vérifier | rare | en déclin | non | liquidité insuffisante (CoinGecko `loulou` : volume 24 h 2 k$, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 484 | WolfSafePoorPeople | WSPP | à vérifier | rare | actif | non | liquidité insuffisante (CoinGecko `wolfsafepoorpeople` : volume 24 h 5 k$, capitalisation 3,3 M$ ; seuils 20 k$ et 1 M$) |
| 485 | what the hook? | WTH | à vérifier | rare | actif | oui | achetable : état « actif », CoinGecko `what-the-hook` : volume 24 h 179 k$, capitalisation 4,4 M$ |
| 486 | 中国人能飞火箭 | 中国人能飞 | à vérifier | rare | en déclin | oui | achetable : état « en déclin », CoinGecko `zhong-guo-ren-neng-fei` : volume 24 h 1,2 M$, capitalisation 1,4 M$ |
| 487 | ShibaDoge | SHIBDOGE | à vérifier | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `shibadoge` : volume 24 h 86 $, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 488 | BNB Tiger OG | BNBTIGEROG | à vérifier | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `bnbtiger` : volume 24 h 9 k$, capitalisation 6,4 M$ ; seuils 20 k$ et 1 M$) |
| 489 | Pitbull | PIT | à vérifier | commune | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `pitbull` : volume 24 h 62 k$, capitalisation 5,3 M$ |
| 490 | Anon Inu | AINU | à vérifier | commune | mort | non | état « mort » |
| 491 | AI XOVIA | AIX | à vérifier | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `ai-xovia` : volume 24 h 4 k$, capitalisation 20,0 M$ ; seuils 20 k$ et 1 M$) |
| 492 | YooShi | YOOSHI | à vérifier | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `yooshi` : volume 24 h 10 $, capitalisation 2,2 M$ ; seuils 20 k$ et 1 M$) |
| 493 | Pups † | PUPS | Bitcoin | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `rune-pups` : volume 24 h 6 k$, capitalisation 2,5 M$ ; seuils 20 k$ et 1 M$) |
| 494 | Pig Finance | PIG | BNB Chain | commune | mort | non | état « mort » |
| 495 | PEPPER | PEPPER | à vérifier | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `pepper` : volume 24 h 20 k$, capitalisation 4,0 M$ ; seuils 20 k$ et 1 M$) |
| 496 | Capybara Nation | BARA | à vérifier | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `capybara-nation` : volume 24 h 3 k$, capitalisation 7,1 M$ ; seuils 20 k$ et 1 M$) |
| 497 | Rosa Inu | ROSA | à vérifier | commune | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `rosa-inu` : volume 24 h 230 k$, capitalisation 7,7 M$ |
| 498 | Kishu Inu | KISHU | Ethereum | commune | en déclin (-95 % ou pire) | oui | achetable : état « en déclin (-95 % ou pire) », CoinGecko `kishu-inu` : volume 24 h 70 k$, capitalisation 4,8 M$ |
| 499 | CorgiAI | CORGIAI | à vérifier | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `corgiai` : volume 24 h 4 k$, capitalisation 8,5 M$ ; seuils 20 k$ et 1 M$) |
| 501 | Ape and Pepe | APEPE | à vérifier | commune | en déclin | oui | achetable : état « en déclin », CoinGecko `ape-and-pepe` : volume 24 h 15,9 M$, capitalisation 261,8 M$ |
| 502 | catwifhat | CWIF | Solana | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `catwifhat-2` : volume 24 h 3 k$, capitalisation 14,2 M$ ; seuils 20 k$ et 1 M$) |
| 503 | Samoyedcoin † | SAMO | Solana | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `samoyedcoin` : volume 24 h 8 k$, capitalisation 1,5 M$ ; seuils 20 k$ et 1 M$) |
| 504 | Solid X | SOLIDX | à vérifier | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `solid-x` : volume 24 h 1 k$, capitalisation 2,6 M$ ; seuils 20 k$ et 1 M$) |
| 505 | OSK | OSK | à vérifier | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `osk` : volume 24 h 2 $, capitalisation 13,5 M$ ; seuils 20 k$ et 1 M$) |
| 506 | CAT | CAT | Avalanche | commune | mort | non | état « mort » |
| 507 | catwifbag | BAG | Solana | commune | mort | non | état « mort » |
| 508 | Doge Token | DOGET | à vérifier | commune | mort | non | état « mort » |
| 509 | Shibnobi | SHINJA | Ethereum | commune | mort | non | état « mort » |
| 510 | BUBCAT | BUB | BNB Chain | commune | mort | non | état « mort » |
| 511 | Rizzmas | RIZZMAS | Solana | commune | mort | non | état « mort » |
| 512 | MEMDEX100 | MEMDEX | à vérifier | commune | mort | non | état « mort » |
| 513 | Sponge | SPONGE | Ethereum | commune | mort | non | état « mort » |
| 514 | Chomp | CHOMP | Base | commune | mort | non | état « mort » |
| 515 | Banano † | BAN | blockchain propre | commune | mort | non | état « mort » |
| 516 | Dontplaywithkitty | DPK | BNB Chain | commune | mort | non | état « mort » |
| 517 | SHKOOBY INU | SHKOOBY | Ethereum | commune | mort | non | état « mort » |
| 518 | Base God | TYBG | à vérifier | commune | mort | non | état « mort » |
| 519 | Tipinu | TIPINU | BNB Chain | commune | mort | non | état « mort » |
| 520 | 客服小何 (Customer Xiaohe) | KEFU | BNB Chain | commune | mort (absent de CoinGecko) | non | état « mort » |
| 521 | Doge Eat Doge | OMNOM | Dogechain | commune | mort | non | état « mort » |
| 523 | Rare Pepe Cash † | PEPECASH | Counterparty (Bitcoin) | commune | mort (absent de CoinGecko) | non | état « mort » |
| 524 | Scrat | SCRAT | Solana | commune | mort | non | état « mort » |
| 525 | SHIBA BSC | SHIBSC | à vérifier | commune | mort | non | état « mort » |
| 526 | DogeVerse | DOGEVERSE | Ethereum | commune | mort | non | état « mort » |
| 527 | POOH | POOH | à vérifier | commune | mort | non | état « mort » |
| 528 | Pepe on SOL | PEPE | à vérifier | commune | mort | non | état « mort » |
| 529 | Dolos The Bully | BULLY | Solana | commune | mort | non | état « mort » |
| 530 | Luminous | LUM | Base | commune | mort | non | état « mort » |
| 531 | PolyDoge | POLYDOGE | Polygon | commune | mort | non | état « mort » |
| 533 | Costco Hot Dog | COST | Solana | commune | mort | non | état « mort » |
| 534 | Ping | PING | à vérifier | commune | mort | non | état « mort » |
| 535 | Catana | CATANA | Solana | commune | mort (≈ 61 k$, volume nul) | non | état « mort » |
| 536 | GOUT | GOUT | à vérifier | commune | mort | non | état « mort » |
| 537 | FedoraCoin | TIPS | blockchain propre | commune | mort | non | état « mort » |
| 538 | Hosico Cat | HOSICO | Solana | commune | mort | non | état « mort » |
| 539 | SafeMoon Inu | SMI | à vérifier | commune | mort | non | état « mort » |
| 540 | AEROBUD | AEROBUD | Base | commune | mort | non | état « mort » |
| 541 | Forgive Me Father | PURGE | NEAR | commune | mort | non | état « mort » |
| 542 | Sillynubcat | NUB | Solana | commune | mort | non | état « mort » |
| 544 | Ani | ANI | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 545 | Moutai | MOUTAI | Solana | commune | mort | non | état « mort » |
| 546 | Wakanda Inu | WKD | Ethereum | commune | mort | non | état « mort » |
| 547 | Nailong | NAILONG | Solana | commune | mort (≈ 0,12 M$) | non | état « mort » |
| 548 | Goku | GOKU | Ethereum | commune | mort | non | état « mort » |
| 549 | Donkey (DONKEY_BSC_MEME) | DONKEY | BNB Chain | commune | mort | non | état « mort » |
| 550 | Doggy | DOGGY | à vérifier | commune | mort | non | état « mort » |
| 551 | DUKO | DUKO | Solana | commune | mort | non | état « mort » |
| 552 | EvilSquidGame | EVILSQUID | BNB Chain | commune | mort | non | état « mort » |
| 553 | ROCKY | ROCKY | Base | commune | mort | non | état « mort » |
| 555 | Guacamole | GUAC | à vérifier | commune | mort | non | état « mort » |
| 556 | SelfieDogCoin | SELFIE | Solana | commune | mort | non | état « mort » |
| 557 | Gizmo | GIZMO | Bitcoin | commune | mort | non | état « mort » |
| 558 | BabyCake | BC2.1 | BNB Chain | commune | mort | non | état « mort » |
| 559 | Anon | ANON | Base | commune | mort | non | état « mort » |
| 560 | Dupe | DUPE | à vérifier | commune | mort | non | état « mort » |
| 561 | Bonk On Base | BONK | Base | commune | mort | non | état « mort » |
| 562 | Spore | SPORE | Avalanche | commune | mort | non | état « mort » |
| 564 | SAD HAMSTER | HAMMY | Solana | commune | mort | non | état « mort » |
| 565 | Shikoku | SHIK | à vérifier | commune | mort | non | état « mort » |
| 566 | Tiger King | TKING | à vérifier | commune | mort (absent de CoinGecko) | non | état « mort » |
| 567 | Zelda Inu | ZLDA | BNB Chain | commune | mort | non | état « mort » |
| 568 | Basenji | BENJI | Base | commune | mort | non | état « mort » |
| 569 | Woman Yelling at Cat | WYAC | Solana | commune | mort | non | état « mort » |
| 570 | Boomer | BOOMER | Base | commune | mort | non | état « mort » |
| 571 | Gui Inu | GUI | Aptos | commune | mort | non | état « mort » |
| 572 | DYZilla | DYZILLA | à vérifier | commune | mort | non | état « mort » |
| 573 | Habibi (Sol) | HABIBI | Solana | commune | mort (≈ 54 k$) | non | état « mort » |
| 575 | SEIYAN | SEIYAN | Sei | commune | mort | non | état « mort » |
| 576 | Brainlet | BRAINLET | à vérifier | commune | mort | non | état « mort » |
| 578 | Moonshot | MSHOT | BNB Chain | commune | mort | non | état « mort » |
| 579 | Bitcoin20 | BTC20 | Ethereum | commune | mort | non | état « mort » |
| 581 | Andy BSC | ANDY | BNB Chain | commune | mort | non | état « mort » |
| 582 | Kasper | KASPER | Kaspa | commune | mort | non | état « mort » |
| 583 | 財務自由 (Liberté financière) | 財務自由 | BNB Chain | commune | mort (≈ 66 k$) | non | état « mort » |
| 585 | Ski Mask Cat | SKICAT | Base | commune | mort | non | état « mort » |
| 586 | Any Inu | AI | à vérifier | commune | mort | non | état « mort » |
| 587 | The Next 100x Memecoin on Base | TN100X | Base | commune | mort | non | état « mort » |
| 588 | Hina Inu | HINA | Ethereum | commune | mort | non | état « mort » |
| 589 | AVAX Lambo | LAMBO | Avalanche | commune | mort (absent de CoinGecko) | non | état « mort » |
| 590 | Kimbo | KIMBO | Avalanche | commune | mort | non | état « mort » |
| 591 | Shina Inu | SHI | à vérifier | commune | mort | non | état « mort » |
| 592 | TON FISH MEMECOIN | FISH | à vérifier | commune | mort | non | état « mort » |
| 593 | WenMoon | WENMOON | BNB Chain | commune | mort | non | état « mort » |
| 594 | Shakita Inu | SHAK | BNB Chain | commune | mort | non | état « mort » |
| 595 | Shiba Floki Inu | FLOKI | BNB Chain | commune | mort | non | état « mort » |
| 596 | Pigcoin | PIG | Polygon | commune | mort | non | état « mort » |
| 597 | Trog | TROG | à vérifier | commune | mort | non | état « mort » |
| 598 | Pissing Cat | PEECAT | Ethereum | commune | mort | non | état « mort » |
| 599 | Apetos | APE | Aptos | commune | mort | non | état « mort » |
| 600 | AVAX Has No Chill | NOCHILL | Avalanche | commune | mort | non | état « mort » |
| 601 | Bagwork | BAGWORK | Solana | commune | mort (≈ 82 k$) | non | état « mort » |
| 602 | Chickencoin | CHKN | à vérifier | commune | mort | non | état « mort » |
| 603 | GoldenBoys | GOLD | à vérifier | commune | mort | non | état « mort » |
| 604 | Terminus | TERMINUS | à vérifier | commune | mort | non | état « mort » |
| 605 | The Balkan Dwarf | KEKEC | à vérifier | commune | mort | non | état « mort » |
| 606 | UWON | UWON | à vérifier | commune | mort | non | état « mort » |
| 607 | Boop | BOOP | à vérifier | commune | mort | non | état « mort » |
| 608 | Flybrain | FLYBRAIN | Ethereum | commune | mort (≈ 0,2 M$) | non | état « mort » |
| 610 | Andy † | ANDY | Base | commune | mort | non | état « mort » |
| 611 | KANGO | KANGO | Kaspa | commune | mort | non | état « mort » |
| 612 | NumberGoUpTech | TECH | Avalanche | commune | mort | non | état « mort » |
| 613 | Brett (ETH) | BRETT | à vérifier | commune | mort | non | état « mort » |
| 614 | Pepe 2.0 | PEPE2.0 | Ethereum | commune | mort (≈ 0,26 M$, -99,8 %) | non | état « mort » |
| 615 | SHIRO INU | SHIR | BNB Chain | commune | mort | non | état « mort » |
| 616 | WAR | WAR | à vérifier | commune | mort | non | état « mort » |
| 617 | Bubb | BUBB | BNB Chain | commune | mort (≈ 30 k$) | non | état « mort » |
| 618 | 修仙 (Xiuxian) | 修仙 | BNB Chain | commune | mort (≈ 0,5 M$) | non | état « mort » |
| 619 | Tardi | TARDI | Sui | commune | mort | non | état « mort » |
| 620 | Shiba Inu Mother | SHIBM | Heco | commune | mort | non | état « mort » |
| 621 | Bitcoin Wizards | WZRD | Bitcoin | commune | mort (absent de CoinGecko) | non | état « mort » |
| 622 | Bob (Monad) | BOB | Monad | commune | mort | non | état « mort » |
| 623 | FourCoin | FOUR | à vérifier | commune | mort | non | état « mort » |
| 624 | Shiryo Inu | SHIRYO | Ethereum | commune | mort | non | état « mort » |
| 625 | LabraCoin | LABRA | Ethereum | commune | mort | non | état « mort » |
| 626 | Ponyo Inu | PONYO | Ethereum | commune | mort | non | état « mort » |
| 627 | Invest Zone | IVFUN | Tron | commune | mort | non | état « mort » |
| 628 | Simmi Token | SIMMI | à vérifier | commune | mort | non | état « mort » |
| 629 | Waffles | WAFFLES | à vérifier | commune | mort | non | état « mort » |
| 630 | 人生K线 (« K-line de la vie ») | à vérifier | BNB Chain | commune | mort (≈ 0,5 M$, -98 %) | non | état « mort » |
| 631 | Captain Inu | CPTINU | Ethereum | commune | mort | non | état « mort » |
| 632 | Crob Coin | CROB | Cronos | commune | mort | non | état « mort » |
| 633 | Dog Wif Nunchucks | NINJA | à vérifier | commune | mort | non | état « mort » |
| 634 | DOGE-1 Satellite | DOGE-1 | à vérifier | commune | mort | non | état « mort » |
| 635 | Dogecolony | DOGECO | BNB Chain | commune | mort | non | état « mort » |
| 636 | Fair and Free | FAIR3 | à vérifier | commune | mort | non | état « mort » |
| 637 | Momo | MOMO | Solana | commune | mort | non | état « mort » |
| 639 | 114514 | 114514 | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 640 | BIBI | BIBI | à vérifier | commune | mort | non | état « mort » |
| 641 | Catcoin | CAT | à vérifier | commune | mort | non | état « mort » |
| 642 | CatSlap | SLAP | à vérifier | commune | mort | non | état « mort » |
| 643 | Clawd | CLAWD | Base | commune | mort (absent de CoinGecko) | non | état « mort » |
| 644 | FourBook | FB | à vérifier | commune | mort | non | état « mort » |
| 645 | MemeWars | MWAR | BNB Chain | commune | mort | non | état « mort » |
| 646 | Roaring Kitty | KITTY | Solana | commune | mort | non | état « mort » |
| 647 | Tralalero Tralala | à vérifier | Solana | commune | mort | non | état « mort » |
| 648 | WSB Coin | WSB | à vérifier | commune | mort | non | état « mort » |
| 649 | WEWECOIN (ex-Upside Down Meme) | WEWE | Base | commune | mort | non | état « mort » |
| 650 | DeFrogs | DEFROGS | Ethereum | commune | mort | non | état « mort » |
| 651 | Doge Raca | DOCA | BNB Chain | commune | mort | non | état « mort » |
| 652 | Fofar | FOFAR | Tron | commune | mort | non | état « mort » |
| 653 | FUD the Pug † | FUD | Sui | commune | mort | non | état « mort » |
| 654 | Hehe | HEHE | Solana | commune | mort | non | état « mort » |
| 655 | Honk | HONK | à vérifier | commune | mort | non | état « mort » |
| 656 | MOAI | MOAI | à vérifier | commune | mort | non | état « mort » |
| 657 | NPC On Solana | NPCS | à vérifier | commune | mort | non | état « mort » |
| 658 | Priceless | PRICELESS | BNB Chain | commune | mort (≈ 0,16 M$) | non | état « mort » |
| 659 | Real Smurf Cat (шайлушай) | SMURFCAT | Ethereum | commune | mort | non | état « mort » |
| 660 | STAN | STAN | à vérifier | commune | mort | non | état « mort » |
| 661 | Sundae The Dog | SUNDAE | Arbitrum | commune | mort | non | état « mort » |
| 662 | AU79 | AU79 | à vérifier | commune | mort | non | état « mort » |
| 663 | MAGIC•INTERNET•MONEY | MIM | Bitcoin | commune | mort (absent de CoinGecko) | non | état « mort » |
| 664 | TAO INU | TAONU | à vérifier | commune | mort | non | état « mort » |
| 665 | τDoge | TDOGE | à vérifier | commune | mort | non | état « mort » |
| 666 | Crash On Base | CRASH | Base | commune | mort | non | état « mort » |
| 667 | Poodl | POODL | BNB Chain | commune | mort | non | état « mort » |
| 669 | San Chan | SAN | à vérifier | commune | mort | non | état « mort » |
| 670 | Sun Wukong | SUNWUKONG | Tron | commune | mort | non | état « mort » |
| 671 | Ainu | AINU | à vérifier | commune | mort | non | état « mort » |
| 672 | FRIC | FRIC | à vérifier | commune | mort | non | état « mort » |
| 673 | CatGPT | CATGPT | à vérifier | commune | mort | non | état « mort » |
| 674 | Dotcom | Y2K | à vérifier | commune | mort | non | état « mort » |
| 675 | N3on | N3ON | à vérifier | commune | mort | non | état « mort » |
| 676 | What IF | IF | à vérifier | commune | mort | non | état « mort » |
| 677 | Shar Pei | SHARPEI | BNB Chain | commune | mort | non | état « mort » |
| 678 | alright buddy | BUDDY | Hyperliquid | commune | mort | non | état « mort » |
| 679 | Zoro Inu | ZORO | BNB Chain | commune | mort | non | état « mort » |
| 681 | Degen Zoo | DZOO | à vérifier | commune | mort | non | état « mort » |
| 682 | Dust | DUST | BNB Chain | commune | mort (≈ 0,17 M$) | non | état « mort » |
| 684 | Huhu Cat | HUHU | Merlin Chain | commune | mort | non | état « mort » |
| 685 | Shifu | SHIFU | à vérifier | commune | mort | non | état « mort » |
| 687 | Saint Inu | SAINT | Arbitrum | commune | mort | non | état « mort » |
| 688 | 吉祥马 | 吉祥马 | à vérifier | commune | mort | non | état « mort » |
| 689 | DisclaimerCoin | DONT | Solana | commune | mort (≈ 0,4-0,6 M$) | non | état « mort » |
| 690 | FINE | FINE | à vérifier | commune | mort | non | état « mort » |
| 691 | Grimace Coin | GRIMACE | Dogechain | commune | mort | non | état « mort » |
| 692 | henlo | HENLO | Berachain | commune | mort | non | état « mort » |
| 693 | Kaspy | KASPY | à vérifier | commune | mort | non | état « mort » |
| 694 | McPepe's | PEPES | à vérifier | commune | mort | non | état « mort » |
| 695 | Spinning Cat | OIIAOIIA | à vérifier | commune | mort | non | état « mort » |
| 696 | uPX | UPX | à vérifier | commune | mort | non | état « mort » |
| 697 | Genshin Floki Inu | GFloki | BNB Chain | commune | mort | non | état « mort » |
| 698 | A Gently Used 2001 Honda Civic | USEDCAR | Solana | commune | mort | non | état « mort » |
| 699 | Daku V2 | DAKU | à vérifier | commune | mort | non | état « mort » |
| 700 | Goldn | GOLDN | à vérifier | commune | mort | non | état « mort » |
| 701 | HAMI | HAMI | à vérifier | commune | mort | non | état « mort » |
| 702 | TANUKI•WISDOM | TANUKI | Bitcoin | commune | mort (absent de CoinGecko) | non | état « mort » |
| 703 | Gecko Inu | GEC | Avalanche | commune | mort | non | état « mort » |
| 704 | LEO | LEO | à vérifier | commune | mort | non | état « mort » |
| 705 | Lion Cat | LCAT | BNB Chain | commune | mort | non | état « mort » |
| 706 | Luna Inu | LINU | à vérifier | commune | mort | non | état « mort » |
| 707 | MoonRise | MOONRISE | BNB Chain | commune | mort | non | état « mort » |
| 708 | Safetesla | SAFETESLA | BNB Chain | commune | mort | non | état « mort » |
| 710 | Tbull | TBULL | Tron | commune | mort | non | état « mort » |
| 711 | Toby ToadGod | TOBY | à vérifier | commune | mort | non | état « mort » |
| 712 | WifeDoge | WIFEDOGE | BNB Chain | commune | mort | non | état « mort » |
| 713 | Aqua Goat | AQUAGOAT | à vérifier | commune | mort | non | état « mort » |
| 714 | BabyMatic | BABYMATIC | BNB Chain | commune | mort | non | état « mort » |
| 715 | Generational Wealth | GEN | à vérifier | commune | mort | non | état « mort » |
| 716 | Pesto the Baby King Penguin | PESTO | Solana | commune | mort | non | état « mort » |
| 717 | Pikachu Inu | PIKACHU | Ethereum | commune | mort | non | état « mort » |
| 718 | All Street Bets | BETS | à vérifier | commune | mort | non | état « mort » |
| 719 | BOG | BOG | Solana | commune | mort | non | état « mort » |
| 721 | Ghiblification | GHIBLI | Solana | commune | mort (≈ 80 k$) | non | état « mort » |
| 722 | JustAnEgg | EGG | à vérifier | commune | mort | non | état « mort » |
| 723 | Milady Wif Hat | LADYF | à vérifier | commune | mort | non | état « mort » |
| 724 | Zeek Coin | MEOW | Zksync Era | commune | mort | non | état « mort » |
| 725 | 屎壳郎 (Dung Beetle) | 屎壳郎 | à vérifier | commune | mort | non | état « mort » |
| 726 | Husky Avax | HUSKY | Avalanche | commune | mort | non | état « mort » |
| 727 | Chuck | CHUCK | Base | commune | mort | non | état « mort » |
| 728 | Business Coin | BUSINESS | à vérifier | commune | mort | non | état « mort » |
| 729 | Cheese | CHEESE | à vérifier | commune | mort | non | état « mort » |
| 730 | SHIBAAI | SHIBAAI | à vérifier | commune | mort | non | état « mort » |
| 731 | WASSIE | WASSIE | à vérifier | commune | mort | non | état « mort » |
| 732 | WORLD CUP INU | WCI | Ethereum | commune | mort | non | état « mort » |
| 733 | 🟥🟪🟦🟩🟨🟧 | 🟥🟩 | à vérifier | commune | mort | non | état « mort » |
| 735 | Gochujangcoin | GOCHU | Base | commune | mort | non | état « mort » |
| 736 | HeeeHeee | HEEHEE | à vérifier | commune | mort | non | état « mort » |
| 737 | Ignore Fud | 4TOKEN | Core | commune | mort | non | état « mort » |
| 738 | Manifest | MANIFEST | à vérifier | commune | mort | non | état « mort » |
| 739 | Mubarakah | MUBARAKAH | BNB Chain | commune | mort (≈ 0,4 M$) | non | état « mort » |
| 740 | Swag | SWAG | à vérifier | commune | mort | non | état « mort » |
| 743 | WOOF | WOOF | Solana | commune | mort | non | état « mort » |
| 745 | Baby BNB | BABY | BNB Chain | commune | mort | non | état « mort » |
| 746 | Defender of Doge | DOD | BNB Chain | commune | mort | non | état « mort » |
| 747 | IC Ghost | GHOST | à vérifier | commune | mort | non | état « mort » |
| 748 | IQ50 | IQ50 | Solana | commune | mort | non | état « mort » |
| 749 | LERNITAS | 2192 | Optimism | commune | mort | non | état « mort » |
| 750 | Nasdaq666 | NDQ | BNB Chain | commune | mort | non | état « mort » |
| 751 | Parabolic | PARAX | à vérifier | commune | mort | non | état « mort » |
| 752 | Sugar Boy | SUGAR | Tron | commune | mort | non | état « mort » |
| 753 | Noggles | NOGS | Ethereum | commune | mort | non | état « mort » |
| 754 | BUBBLES (Bubbles Bean) | BUBBLES | Aptos | commune | mort | non | état « mort » |
| 755 | Squid Moon | SQM | BNB Chain | commune | mort | non | état « mort » |
| 756 | AstroPepeX | APX | Ethereum | commune | mort | non | état « mort » |
| 757 | Attention | ATTN | à vérifier | commune | mort | non | état « mort » |
| 758 | CATO | CATO | Solana | commune | mort | non | état « mort » |
| 759 | Chaos | CHAOS | à vérifier | commune | mort | non | état « mort » |
| 760 | LAMBO | LAMBO | Avalanche | commune | mort | non | état « mort » |
| 761 | memes will continue | memes | BNB Chain | commune | mort (≈ 58 k$) | non | état « mort » |
| 762 | Suncat | SUNCAT | Tron | commune | mort | non | état « mort » |
| 763 | Windoge98 | EXE | à vérifier | commune | mort | non | état « mort » |
| 764 | Waka Flocka Flame † | FLOCKA | Solana | commune | mort | non | état « mort » |
| 765 | Okayeg | OKAYEG | Base | commune | mort | non | état « mort » |
| 766 | RUGMAN | RUG | Hyperliquid | commune | mort | non | état « mort » |
| 767 | Bloo | BLOO | Base | commune | mort (absent de CoinGecko) | non | état « mort » |
| 768 | DORK | DORK | à vérifier | commune | mort | non | état « mort » |
| 769 | Frodo the virtual samurai | FROG | BNB Chain | commune | mort | non | état « mort » |
| 770 | GAME•OF•BITCOIN | GAME | Bitcoin | commune | mort | non | état « mort » |
| 771 | HayCoin | HAY | à vérifier | commune | mort | non | état « mort » |
| 772 | Peepo | PEEPO | Ethereum | commune | mort | non | état « mort » |
| 773 | Red Hare Coin | RHC | à vérifier | commune | mort | non | état « mort » |
| 774 | Smiley Coin | SMILEY | à vérifier | commune | mort | non | état « mort » |
| 775 | 888 | 888 | à vérifier | commune | mort | non | état « mort » |
| 776 | Bird Dog | BIRDDOG | à vérifier | commune | mort | non | état « mort » |
| 777 | Buftoad | BUF | Solana | commune | mort | non | état « mort » |
| 778 | Catalorian | CATALORIAN | à vérifier | commune | mort | non | état « mort » |
| 779 | Chihuahua | HUAHUA | Chihuahua | commune | mort | non | état « mort » |
| 780 | GOGGLES | GOGLZ | Fantom | commune | mort | non | état « mort » |
| 781 | MUSTAAAAAARD | MUSTARD | à vérifier | commune | mort | non | état « mort » |
| 782 | Nobiko Coin | LONG | à vérifier | commune | mort | non | état « mort » |
| 783 | Pepe Community | PEPE | à vérifier | commune | mort | non | état « mort » |
| 784 | Playdoge | PLAY | à vérifier | commune | mort | non | état « mort » |
| 785 | supercycle(real) | SUPERCYCLE | à vérifier | commune | mort | non | état « mort » |
| 786 | Teddy Doge | TEDDY | BNB Chain | commune | mort | non | état « mort » |
| 787 | Toad (SOL) | TOAD | à vérifier | commune | mort | non | état « mort » |
| 788 | Wall St. Bull | WBULL | BNB Chain | commune | mort (≈ 13 k$, volume nul) | non | état « mort » |
| 789 | Wifejak | WIFE | à vérifier | commune | mort | non | état « mort » |
| 790 | King Shiba | KINGSHIB | BNB Chain | commune | mort | non | état « mort » |
| 791 | Dogira | DOGIRA | Ethereum | commune | mort | non | état « mort » |
| 792 | Base is for everyone | BASEISFOREVERYONE | Base | commune | mort | non | état « mort » |
| 793 | Baby Pepe | BABYPEPE | à vérifier | commune | mort | non | état « mort » |
| 794 | POPDOG | POPDOG | à vérifier | commune | mort | non | état « mort » |
| 795 | Sanin Inu | SANI | à vérifier | commune | mort | non | état « mort » |
| 796 | Skull of Pepe Token | SKOP | à vérifier | commune | mort | non | état « mort » |
| 797 | YOLO | YOLO | à vérifier | commune | mort | non | état « mort » |
| 798 | Ton Cat | TCAT | TON | commune | mort | non | état « mort » |
| 799 | Super Suiyan | SUIYAN | Sui | commune | mort | non | état « mort » |
| 800 | NEAT | NEAT | NEAR | commune | mort | non | état « mort » |
| 801 | Based Shiba Inu | BSHIB | Base | commune | mort | non | état « mort » |
| 802 | SHIBAVAX | SHIBX | Avalanche | commune | mort | non | état « mort » |
| 803 | Carlo | CARLO | Base | commune | mort | non | état « mort » |
| 804 | Shibaken Finance | SHIBAKEN | Ethereum | commune | mort | non | état « mort » |
| 805 | BabySNEK | BBSNEK | Cardano | commune | mort | non | état « mort » |
| 806 | DOYR | DOYR | BNB Chain | commune | mort (≈ 0,25 M$) | non | état « mort » |
| 807 | Meowcoin | MEWC | à vérifier | commune | mort | non | état « mort » |
| 808 | OSCAR | OSCAR | à vérifier | commune | mort | non | état « mort » |
| 809 | Peepo (Solana) | PEEP | Solana | commune | mort | non | état « mort » |
| 810 | Pepa Inu | PEPA | Ethereum | commune | mort | non | état « mort » |
| 811 | RIBBIT | RBT | à vérifier | commune | mort | non | état « mort » |
| 812 | Smolcoin | SMOL | Arbitrum | commune | mort | non | état « mort » |
| 814 | Wolfi | WOLFI | Avalanche | commune | mort | non | état « mort » |
| 815 | Poncho | PONCHO | Base | commune | mort | non | état « mort » |
| 816 | Based Turbo | TURBO | Base | commune | mort | non | état « mort » |
| 817 | BOOK OF BILLIONAIRES | BOBE | Solana | commune | mort | non | état « mort » |
| 818 | Bork | BORK | Solana | commune | mort | non | état « mort » |
| 819 | MarsRise | MARSRISE | BNB Chain | commune | mort | non | état « mort » |
| 820 | Asteroid The Space Shiba Inu | ASTEROID | à vérifier | commune | mort | non | état « mort » |
| 821 | Baby Doge Cash | BABYDOGECASH | à vérifier | commune | mort | non | état « mort » |
| 822 | Based Chad | CHAD | Base | commune | mort | non | état « mort » |
| 823 | Bitcoin 2.0 | BTC2.0 | Ethereum | commune | mort | non | état « mort » |
| 824 | BNB Card | BNB CARD | BNB Chain | commune | mort (≈ 33 k$, volume nul) | non | état « mort » |
| 825 | CATGPT | CATGPT | à vérifier | commune | mort | non | état « mort » |
| 826 | CorgiCoin | à vérifier | Solana | commune | mort | non | état « mort » |
| 827 | DNA | DNA | à vérifier | commune | mort | non | état « mort » |
| 828 | Fish | FISH | TON | commune | mort (absent de CoinGecko) | non | état « mort » |
| 829 | Flying Avocado Cat | FAC | à vérifier | commune | mort | non | état « mort » |
| 830 | Flying Ketamine Horse | FKH | Solana | commune | mort (≈ 25 k$, volume nul) | non | état « mort » |
| 831 | FREN | FREN | Cardano | commune | mort | non | état « mort » |
| 832 | Kabosu Inu | KABOSU | à vérifier | commune | mort | non | état « mort » |
| 833 | Kira the Injective Cat | KIRA | Injective | commune | mort | non | état « mort » |
| 834 | Morning Routine | ROUTINE | Solana | commune | mort | non | état « mort » |
| 835 | PlutoPepe | PLUTO | BNB Chain | commune | mort | non | état « mort » |
| 836 | Shibwifhatcoin | SHIB | à vérifier | commune | mort | non | état « mort » |
| 837 | Success Kid (Solana) | SKID | Solana | commune | mort | non | état « mort » |
| 838 | Tyler | TYLER | Base | commune | mort | non | état « mort » |
| 839 | Walter | WALTER | à vérifier | commune | mort | non | état « mort » |
| 840 | YEETI 液体 | YEETI | Hyperliquid | commune | mort | non | état « mort » |
| 841 | CatzCoin | CATZ | BNB Chain | commune | mort | non | état « mort » |
| 842 | Akamaru Inu | AKAMARU | Ethereum | commune | mort | non | état « mort » |
| 843 | build | BUILD | à vérifier | commune | mort | non | état « mort » |
| 844 | COAL | COAL | à vérifier | commune | mort | non | état « mort » |
| 845 | Echelon Token | ELON | à vérifier | commune | mort | non | état « mort » |
| 846 | Elite (1337) | 1337 | blockchain propre | commune | mort | non | état « mort » |
| 847 | GLORP | GLORP | Solana | commune | mort | non | état « mort » |
| 848 | Leopard | LEOPARD | à vérifier | commune | mort | non | état « mort » |
| 849 | Luffy | LUFFY | à vérifier | commune | mort | non | état « mort » |
| 850 | ORC | ORC | à vérifier | commune | mort | non | état « mort » |
| 851 | RealGOAT | RGOAT | Base | commune | mort | non | état « mort » |
| 852 | TOES | TOESCOIN | Solana | commune | mort (≈ 45 k$) | non | état « mort » |
| 853 | Dogecoin 2.0 | DOGE2 | BNB Chain | commune | mort | non | état « mort » |
| 854 | Young Peezy AKA Pepe | PEEZY | Base | commune | mort | non | état « mort » |
| 855 | Myra | MYRA | Solana | commune | mort | non | état « mort » |
| 856 | AAA Cat | AAA | Sui | commune | mort (absent de CoinGecko) | non | état « mort » |
| 857 | Baby Neiro | BABYNEIRO | à vérifier | commune | mort | non | état « mort » |
| 858 | BOBER | BOBER | Multiversx | commune | mort | non | état « mort » |
| 859 | BullDogito | BDOGITO | à vérifier | commune | mort | non | état « mort » |
| 862 | Floppa | FLOPPA | à vérifier | commune | mort | non | état « mort » |
| 863 | Gemini | GEMINI | à vérifier | commune | mort | non | état « mort » |
| 864 | Grimace | GRIMACE | Arbitrum | commune | mort | non | état « mort » |
| 865 | HAHA | HAHA | à vérifier | commune | mort | non | état « mort » |
| 866 | Lord Of SOL | LOS | à vérifier | commune | mort | non | état « mort » |
| 867 | LOUD | LOUD | Solana | commune | mort | non | état « mort » |
| 868 | NearKat | NEARKAT | Solana | commune | mort | non | état « mort » |
| 869 | OneCOW | 1COW | à vérifier | commune | mort | non | état « mort » |
| 871 | SPIKE | SPIKE | Solana | commune | mort (≈ 29 k$) | non | état « mort » |
| 872 | Strategic Super Reserve | SSR | à vérifier | commune | mort | non | état « mort » |
| 873 | Toad Killer | TOAD | à vérifier | commune | mort | non | état « mort » |
| 874 | Ucan fix life in1day | 1 | BNB Chain | commune | mort (≈ 0,3 M$) | non | état « mort » |
| 875 | Velvet Unicorn by Virtuals | VU | à vérifier | commune | mort | non | état « mort » |
| 876 | Yeet | YEET | Berachain | commune | mort | non | état « mort » |
| 877 | Dogey-Inu | DINU | Ethereum | commune | mort | non | état « mort » |
| 878 | Normilio | NORMILIO | Base | commune | mort | non | état « mort » |
| 879 | Autist | AUTIST | Hyperliquid | commune | mort | non | état « mort » |
| 881 | Weirdo | WEIRDO | Base | commune | mort | non | état « mort » |
| 882 | Tiki Token | TIKI | BNB Chain | commune | mort | non | état « mort » |
| 883 | BUILD | BUILD | à vérifier | commune | mort | non | état « mort » |
| 884 | Dogecoin20 | DOGE20 | Ethereum | commune | mort | non | état « mort » |
| 885 | Fish N Chips | CHIPPY | à vérifier | commune | mort | non | état « mort » |
| 886 | Fishkoin | KOIN | à vérifier | commune | mort | non | état « mort » |
| 887 | Galaxy Fox | GFOX | à vérifier | commune | mort | non | état « mort » |
| 888 | Hachi | HACHI | à vérifier | commune | mort | non | état « mort » |
| 889 | Jester | JEST | à vérifier | commune | mort | non | état « mort » |
| 890 | Little Ugly Duck | LUD | à vérifier | commune | mort | non | état « mort » |
| 891 | Mellow Man | MELLOW | à vérifier | commune | mort | non | état « mort » |
| 892 | Nikepig | NIKEPIG | à vérifier | commune | mort | non | état « mort » |
| 893 | NSDQ420 | NSDQ | à vérifier | commune | mort | non | état « mort » |
| 894 | PMX500 | PMX | à vérifier | commune | mort | non | état « mort » |
| 895 | Povel Durev | DUREV | TON | commune | mort | non | état « mort » |
| 896 | RAT Escape | RAT | à vérifier | commune | mort | non | état « mort » |
| 897 | SPARTA | SPARTA | à vérifier | commune | mort | non | état « mort » |
| 898 | You Looked | CIRCLE | Solana | commune | mort | non | état « mort » |
| 899 | Eggdog | EGG | Solana | commune | mort | non | état « mort » |
| 900 | Santa Inu | SANINU | BNB Chain | commune | mort | non | état « mort » |
| 901 | MetaDoge | METADOGEV2 | BNB Chain | commune | mort | non | état « mort » |
| 902 | All Will Retire | AWR | à vérifier | commune | mort | non | état « mort » |
| 903 | Aped | APED | à vérifier | commune | mort | non | état « mort » |
| 905 | Bitcoin on Base | BTCB | à vérifier | commune | mort | non | état « mort » |
| 906 | DEBT | DEBT | Solana | commune | mort | non | état « mort » |
| 907 | Draggy CTO | DRAGGY | à vérifier | commune | mort | non | état « mort » |
| 908 | GDOG | GDOG | à vérifier | commune | mort | non | état « mort » |
| 909 | Lobstar | LOBSTAR | Solana | commune | mort (≈ 44 k$) | non | état « mort » |
| 910 | Memelinked | MK | à vérifier | commune | mort | non | état « mort » |
| 911 | Nitefeeder | NITEFEEDER | à vérifier | commune | mort | non | état « mort » |
| 912 | Pochi Inu | POCHI | Ethereum | commune | mort | non | état « mort » |
| 913 | Raydium Cat | RAYCAT | à vérifier | commune | mort | non | état « mort » |
| 914 | Snibbu | SNIBBU | à vérifier | commune | mort | non | état « mort » |
| 915 | 黑马 (Cheval noir) | 黑马 | BNB Chain | commune | mort (≈ 0,3 M$) | non | état « mort » |
| 916 | DogeMoon | DGMOON | BNB Chain | commune | mort | non | état « mort » |
| 917 | Roost | ROOST | Base | commune | mort | non | état « mort » |
| 918 | BunnyCoin | BUN | blockchain propre | commune | mort | non | état « mort » |
| 919 | Crodie | CRODIE | Solana | commune | mort | non | état « mort » |
| 921 | Mistery | MERY | Cronos | commune | mort | non | état « mort » |
| 922 | Abble | AABL | Solana | commune | mort | non | état « mort » |
| 923 | Amocucinare | AMORE | à vérifier | commune | mort | non | état « mort » |
| 924 | ASTEROID | ASTEROID | à vérifier | commune | mort | non | état « mort » |
| 925 | Baby Neiro BNB | BABYNEIRO | BNB Chain | commune | mort | non | état « mort » |
| 926 | BananaCat | BCAT | à vérifier | commune | mort | non | état « mort » |
| 927 | Belgian Malinois | BELG | BNB Chain | commune | mort (≈ 33 k$) | non | état « mort » |
| 928 | Brent on SOL | BRENT | à vérifier | commune | mort | non | état « mort » |
| 929 | FartStrategy | FSTR | à vérifier | commune | mort | non | état « mort » |
| 930 | Good In The Hood | GOOD | à vérifier | commune | mort | non | état « mort » |
| 931 | KittyCake | KCAKE | à vérifier | commune | mort | non | état « mort » |
| 932 | Knot Diffie-Hellman | KNOT | à vérifier | commune | mort | non | état « mort » |
| 933 | MoonDog AI | MDOGAI | à vérifier | commune | mort | non | état « mort » |
| 934 | SPYRO | SPYRO | à vérifier | commune | mort | non | état « mort » |
| 935 | SZN | SZN | BNB Chain | commune | mort | non | état « mort » |
| 936 | Trash Coin | TRASH | à vérifier | commune | mort | non | état « mort » |
| 937 | Treat Token | TREAT | à vérifier | commune | mort | non | état « mort » |
| 938 | Jesus Coin (2017) | JC | Ethereum | commune | mort | non | état « mort » |
| 939 | Suicy the Seal | SUICY | Sui | commune | mort | non | état « mort » |
| 940 | BabyPepe | BABYPEPE | Ethereum | commune | mort | non | état « mort » |
| 941 | Lil Floki | LILFLOKI | BNB Chain | commune | mort | non | état « mort » |
| 943 | Solana Shib | SSHIB | Solana | commune | mort | non | état « mort » |
| 944 | BillionHappiness | BHC | BNB Chain | commune | mort | non | état « mort » |
| 945 | Akitavax | AKITAX | Avalanche | commune | mort | non | état « mort » |
| 946 | ATEHUN | ATEHUN | à vérifier | commune | mort | non | état « mort » |
| 947 | BabyKitty | BABYKITTY | à vérifier | commune | mort | non | état « mort » |
| 949 | BIG | BIG | Avalanche | commune | mort | non | état « mort » |
| 950 | Capybara Token | CAPY | à vérifier | commune | mort | non | état « mort » |
| 951 | CAT | CAT | à vérifier | commune | mort | non | état « mort » |
| 952 | Didi Bam Bam | DDBAM | à vérifier | commune | mort | non | état « mort » |
| 953 | DORK LORD | DORKL | Ethereum | commune | mort | non | état « mort » |
| 954 | HotDoge [OLD] | HOTDOGE | à vérifier | commune | mort | non | état « mort » |
| 955 | HUA HUA | HUAHUA | à vérifier | commune | mort | non | état « mort » |
| 956 | MindCoin | MIND | à vérifier | commune | mort | non | état « mort » |
| 957 | Mittens | MITTENS | TON | commune | mort | non | état « mort » |
| 958 | NEKO | NEKO | NEAR | commune | mort | non | état « mort » |
| 959 | PIKA to PIKO ピカとピコ | PIKA | à vérifier | commune | mort | non | état « mort » |
| 960 | remilio | REMILIO | à vérifier | commune | mort | non | état « mort » |
| 961 | SatoshAI | SAI | à vérifier | commune | mort | non | état « mort » |
| 962 | Señor Dip | DIP | Cronos | commune | mort | non | état « mort » |
| 963 | Shiba Classic | SHIBC | à vérifier | commune | mort | non | état « mort » |
| 964 | ShibKiller | SHIBKILLER | BNB Chain | commune | mort | non | état « mort » |
| 965 | BOZO | BOZO | Solana | commune | mort | non | état « mort » |
| 966 | ArbiDoge | ADOGE | Arbitrum | commune | mort | non | état « mort » |
| 968 | Baby Asteroid | BABYASTEROID | à vérifier | commune | mort | non | état « mort » |
| 969 | BEAMCAT | BCAT | Beam | commune | mort | non | état « mort » |
| 970 | Damoon Coin | DAMOON | Cronos | commune | mort | non | état « mort » |
| 971 | Defi Tiger | DTG | à vérifier | commune | mort | non | état « mort » |
| 972 | DuckCoin | DUCK | TON | commune | mort | non | état « mort » |
| 973 | Estee | ESTEE | à vérifier | commune | mort | non | état « mort » |
| 974 | FARTGIRL | FARTGIRL | à vérifier | commune | mort | non | état « mort » |
| 975 | Fefe | FEFE | à vérifier | commune | mort | non | état « mort » |
| 976 | Gluteus Maximus by Virtuals | GLUTEU | à vérifier | commune | mort | non | état « mort » |
| 977 | Golden Goose | GG | à vérifier | commune | mort | non | état « mort » |
| 978 | Gondola | GONDOLA | à vérifier | commune | mort | non | état « mort » |
| 979 | LOL | LOL | Solana | commune | mort (≈ 60 k$) | non | état « mort » |
| 980 | Pistacio | PISTACIO | à vérifier | commune | mort | non | état « mort » |
| 981 | Polly | POLLY | à vérifier | commune | mort | non | état « mort » |
| 983 | The Big Red | TD | Avalanche | commune | mort | non | état « mort » |
| 984 | Toby | TOBY | Base | commune | mort | non | état « mort » |
| 985 | Token6900 | T6900 | à vérifier | commune | mort | non | état « mort » |
| 986 | vankedisi | VANKEDISI | à vérifier | commune | mort | non | état « mort » |
| 987 | Wen Lambo | WEN | à vérifier | commune | mort | non | état « mort » |
| 988 | World Cup Coin | à vérifier | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 989 | Beeg Blue Whale | BEEG | Sui | commune | mort | non | état « mort » |
| 990 | Kermit (Solana) | KERMIT | Solana | commune | mort | non | état « mort » |
| 991 | Keisuke Inu | KEI | Ethereum | commune | mort | non | état « mort » |
| 992 | What in Tarnation? | WIT | Solana | commune | mort | non | état « mort » |
| 993 | All Your Base | AYB | à vérifier | commune | mort | non | état « mort » |
| 994 | ARE YA WINNING, SON? | SON | à vérifier | commune | mort | non | état « mort » |
| 995 | BASED | BASED | à vérifier | commune | mort | non | état « mort » |
| 996 | Binance Super Cycle | BSC | à vérifier | commune | mort | non | état « mort » |
| 997 | Black Dragon | BLACKDRAGON | NEAR | commune | mort | non | état « mort » |
| 998 | Doge 2.0 | DOGE2.0 | Ethereum | commune | mort | non | état « mort » |
| 999 | Dork Lord | DORKY | à vérifier | commune | mort | non | état « mort » |
| 1001 | Hund | HUND | à vérifier | commune | mort | non | état « mort » |
| 1002 | Mark-2-Marquette | M2M | à vérifier | commune | mort | non | état « mort » |
| 1003 | MEMENTO•MORI | MEMENTO | Bitcoin | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1004 | Mommy Doge | MOMMYDOGE | à vérifier | commune | mort | non | état « mort » |
| 1005 | PEPECASH | PECH | à vérifier | commune | mort | non | état « mort » |
| 1006 | Signal | SIGNAL | à vérifier | commune | mort | non | état « mort » |
| 1007 | Speedy | SPEEDY | Fantom | commune | mort | non | état « mort » |
| 1008 | SquidGameToken | SGT | BNB Chain | commune | mort | non | état « mort » |
| 1009 | Sweep Token | SWEEP | à vérifier | commune | mort | non | état « mort » |
| 1010 | TOLY'S DOG | ADA | à vérifier | commune | mort | non | état « mort » |
| 1011 | Transhuman Coin | THC | à vérifier | commune | mort | non | état « mort » |
| 1012 | Vibe Cat | VIBE | à vérifier | commune | mort | non | état « mort » |
| 1013 | Viva | à vérifier | Solana | commune | mort | non | état « mort » |
| 1014 | WISHBONE | WISHBONE | à vérifier | commune | mort | non | état « mort » |
| 1015 | 雪球人生 (Vie boule de neige) | 雪球人生 | BNB Chain | commune | mort (≈ 96 k$) | non | état « mort » |
| 1016 | AI Dragon | CHATGPT | Solana | commune | mort | non | état « mort » |
| 1017 | Pou | POU | Solana | commune | mort | non | état « mort » |
| 1018 | All in Dollo | DOLLO | à vérifier | commune | mort | non | état « mort » |
| 1020 | Bera Morning | BM | Berachain | commune | mort | non | état « mort » |
| 1021 | Blue Kirby | KIRBY | Fantom | commune | mort | non | état « mort » |
| 1022 | CALI | CALI | à vérifier | commune | mort | non | état « mort » |
| 1023 | Frog on ETH | FROG | Ethereum | commune | mort | non | état « mort » |
| 1024 | Fronk | FRONK | Solana | commune | mort | non | état « mort » |
| 1025 | Froth | FROTH | à vérifier | commune | mort | non | état « mort » |
| 1026 | GBOY | GBOY | à vérifier | commune | mort | non | état « mort » |
| 1027 | King Of Meme | LION | à vérifier | commune | mort | non | état « mort » |
| 1028 | Matt Furie | MATT | à vérifier | commune | mort | non | état « mort » |
| 1029 | PREME Token | PREME | à vérifier | commune | mort | non | état « mort » |
| 1030 | Puli Inu | PULI | BNB Chain | commune | mort | non | état « mort » |
| 1031 | SurfMoon | SURFMOON | BNB Chain | commune | mort | non | état « mort » |
| 1032 | Wagmi Coin | WAGMI | à vérifier | commune | mort | non | état « mort » |
| 1033 | DOGWIFHOOD | WIF | TON | commune | mort | non | état « mort » |
| 1034 | Official PPshow | PP | à vérifier | commune | mort | non | état « mort » |
| 1035 | Derp | DERP | Sonic | commune | mort | non | état « mort » |
| 1036 | GameCow | GCOW | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `gamecow` : volume 24 h 13 k$, capitalisation 2,6 M$ ; seuils 20 k$ et 1 M$) |
| 1037 | PsyopAnime | PSYOPANIME | à vérifier | commune | en déclin | non | liquidité insuffisante (CoinGecko `psyopanime` : volume 24 h 54 k$, capitalisation 619 k$ ; seuils 20 k$ et 1 M$) |
| 1038 | Croakey | CROAK | Cronos | commune | mort | non | état « mort » |
| 1040 | Shiba Inu Billionaire | SHIBIB | BNB Chain | commune | mort | non | état « mort » |
| 1041 | Bingus Token | BINGUS | BNB Chain | commune | mort | non | état « mort » |
| 1043 | Koreadoge | KDOGE | BNB Chain | commune | mort | non | état « mort » |
| 1044 | RONKE | RONKE | à vérifier | commune | mort | non | état « mort » |
| 1045 | AmazingDoge | ADOGE | BNB Chain | commune | mort | non | état « mort » |
| 1046 | Commander Vrax | VRAX | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `commander-vrax-2` : volume 24 h 1,4 M$, capitalisation 2,8 M$ |
| 1047 | Konan of Kaspa | KONAN | Kaspa | commune | mort | non | état « mort » |
| 1048 | Mars Inu | MARSINU | BNB Chain | commune | mort | non | état « mort » |
| 1049 | LiteDoge | LDOGE | blockchain propre | commune | mort | non | état « mort » |
| 1050 | Beni | BENI | Base | commune | mort | non | état « mort » |
| 1051 | Chinese Brett | CHRETT | Base | commune | mort | non | état « mort » |
| 1052 | DOGITA | DOGA | BNB Chain | commune | mort | non | état « mort » |
| 1053 | DITGOLD | DITAU | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `ditgold` : volume 24 h 101 k$, capitalisation 5,0 M$ |
| 1054 | WONG | WONG | Apechain | commune | mort | non | état « mort » |
| 1055 | bonkwifhat | BIF | Solana | commune | mort | non | état « mort » |
| 1056 | Hobbes [ancien contrat] | HOBBES | Ethereum | commune | mort | non | état « mort » |
| 1057 | XRP20 | XRP20 | Ethereum | commune | mort | non | état « mort » |
| 1058 | Burt | BURT | Kaspa | commune | mort | non | état « mort » |
| 1059 | SHIBA ON BASE | SHIB | à vérifier | commune | mort | non | état « mort » |
| 1060 | American Pepe | USPEPE | à vérifier | commune | mort | non | état « mort » |
| 1061 | ANITA | ANITA | à vérifier | commune | en déclin | non | liquidité insuffisante (CoinGecko `anita` : volume 24 h 17 k$, capitalisation 1,2 M$ ; seuils 20 k$ et 1 M$) |
| 1063 | MILLI | MILLI | Sei | commune | mort | non | état « mort » |
| 1064 | PulseTrailerPark | PTP | Pulsechain | commune | mort | non | état « mort » |
| 1065 | Monkey Cult | MOLT | Solana | commune | mort (≈ 75 k$, volume nul) | non | état « mort » |
| 1066 | Perry | PERRY | BNB Chain | commune | mort | non | état « mort » |
| 1067 | Suiman | SUIMAN | Sui | commune | mort | non | état « mort » |
| 1068 | The Resistance Cat | RECA | TON | commune | mort | non | état « mort » |
| 1069 | DOUBT | DOUBT | à vérifier | commune | en déclin | non | liquidité insuffisante (CoinGecko `doubt` : volume 24 h 3 k$, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 1070 | Egg | EGG | Hyperliquid | commune | mort | non | état « mort » |
| 1071 | WIN界 | WIN界 | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `win-jie` : volume 24 h 32 k$, capitalisation 2,9 M$ |
| 1072 | Normus | NORMUS | Base | commune | mort | non | état « mort » |
| 1073 | Sacabam | SCB | Sui | commune | mort | non | état « mort » |
| 1074 | Brett's cat | BALT | Base | commune | mort | non | état « mort » |
| 1075 | Zen AI | ZAI | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `zen-ai` : volume 24 h 20 k$, capitalisation 2,4 M$ ; seuils 20 k$ et 1 M$) |
| 1076 | GREEN MORNING | GM | à vérifier | commune | à vérifier (homonyme sur CoinGecko, non rapproché) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 1077 | Marvin On Base | MOB | Base | commune | mort | non | état « mort » |
| 1078 | QUEEN POOIE | QUEEN2 | Pulsechain | commune | mort | non | état « mort » |
| 1079 | Silly Duck | DUCK | Solana | commune | mort | non | état « mort » |
| 1080 | Blast Pepe | BEPE | Blast | commune | mort | non | état « mort » |
| 1081 | BULLSHARK | BSHARK | Sui | commune | mort | non | état « mort » |
| 1082 | Brian | BRIAN | Base | commune | mort | non | état « mort » |
| 1083 | ChubbyAkita | CAKITA | BNB Chain | commune | mort | non | état « mort » |
| 1084 | JINDO INU | JIND | BNB Chain | commune | mort | non | état « mort » |
| 1085 | Pink | PINK | Moonbeam | commune | mort | non | état « mort » |
| 1086 | XFROG | XFROG | X Layer | commune | mort | non | état « mort » |
| 1087 | Chiliz Inu | CHZINU | Chiliz | commune | mort | non | état « mort » |
| 1088 | Lovely Inu | LOVELY | Ethereum | commune | mort | non | état « mort » |
| 1089 | Peepo (2024) | PEPO | Ethereum | commune | mort | non | état « mort » |
| 1090 | Perpetual Bitcoin | PB | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `perpetual-bitcoin` : volume 24 h 2 $, capitalisation 4,7 M$ ; seuils 20 k$ et 1 M$) |
| 1091 | Ton Inu | à vérifier | TON | commune | mort | non | état « mort » |
| 1093 | Binance Cat | BNBCAT | BNB Chain | commune | en déclin (≈ 0,5 M$) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 1094 | RALPH | RALPH | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1095 | World Cat | WORLD CAT | World Chain | commune | mort | non | état « mort » |
| 1096 | PETRO PENGUINS | PENGO | à vérifier | commune | mort | non | état « mort » |
| 1097 | UpDog | UPDOG | BNB Chain | commune | mort | non | état « mort » |
| 1098 | AMC (Solana) | AMC | Solana | commune | mort | non | état « mort » |
| 1099 | Mooncat | MCAT | Solana | commune | mort | non | état « mort » |
| 1100 | Shikoku Inu | SHIKO | BNB Chain | commune | mort | non | état « mort » |
| 1101 | Biao | BIAO | BNB Chain | commune | mort | non | état « mort » |
| 1102 | Hedgy the hedgehog | HEDGY | Sonic | commune | mort | non | état « mort » |
| 1103 | AIDOGE Stellar | AIDOGEXLM | Stellar | commune | mort | non | état « mort » |
| 1105 | Binancedog | BINANCEDOG | BNB Chain | commune | mort (≈ 56 k$, volume nul) | non | état « mort » |
| 1106 | BIRDSPING | PING | Kaia | commune | mort | non | état « mort » |
| 1107 | Shiba Inu Empire | SHIBEMP | BNB Chain | commune | mort | non | état « mort » |
| 1108 | STARKNET BROTHER | BROTHER | Starknet | commune | mort | non | état « mort » |
| 1109 | Toilet Dust | TOILET | Sui | commune | mort | non | état « mort » |
| 1110 | Danzo | DANZO | Cardano | commune | mort | non | état « mort » |
| 1111 | Market Dominance | MD | à vérifier | commune | mort | non | état « mort » |
| 1112 | Pepe The Frog | PEPEBNB | BNB Chain | commune | mort | non | état « mort » |
| 1113 | The Final Form Bull | CZ | à vérifier | commune | en déclin | oui | achetable : état « en déclin », CoinGecko `the-final-form-bull` : volume 24 h 675 k$, capitalisation 1,3 M$ |
| 1114 | Harmonic Agent | HARMONIC | à vérifier | commune | en déclin | oui | achetable : état « en déclin », CoinGecko `harmonic-agent` : volume 24 h 46 k$, capitalisation 1,3 M$ |
| 1115 | Wednesday Inu | WED | BNB Chain | commune | mort | non | état « mort » |
| 1116 | Based Bario | BARIO | Base | commune | mort | non | état « mort » |
| 1117 | GRIND | GRIND | Abstract | commune | mort | non | état « mort » |
| 1118 | DogWifJob | JOB | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `dogwifjob` : volume 24 h 932 k$, capitalisation 2,4 M$ |
| 1119 | Papu Token | PAPU | BNB Chain | commune | mort | non | état « mort » |
| 1120 | RONIN | RONIN | à vérifier | commune | en déclin | non | liquidité insuffisante (CoinGecko `ronin-2` : volume 24 h 2 k$, capitalisation 1,0 M$ ; seuils 20 k$ et 1 M$) |
| 1121 | BabyBonk | BABYBONK | à vérifier | commune | mort | non | état « mort » |
| 1122 | PUMPCORN | PUMPCORN | TON | commune | mort | non | état « mort » |
| 1123 | Smudge Cat | SMUDCAT | Base | commune | mort | non | état « mort » |
| 1124 | What's Updog | UPDOG | Solana | commune | mort | non | état « mort » |
| 1125 | 世界和平 (Paix mondiale) | 世界和平 | BNB Chain | commune | mort (≈ 34 k$, volume nul) | non | état « mort » |
| 1127 | Grok Cat | GROKCAT | BNB Chain | commune | mort | non | état « mort » |
| 1129 | PIGU | PIGU | Sui | commune | mort | non | état « mort » |
| 1130 | Greatest Meme Ever | GME | à vérifier | commune | en déclin | non | liquidité insuffisante (CoinGecko `greatest-meme-ever` : volume 24 h 50 k$, capitalisation 482 k$ ; seuils 20 k$ et 1 M$) |
| 1131 | 错版马 (Cheval à l'erreur d'impression) | 哭哭马 | BNB Chain | commune | mort (≈ 0,11 M$) | non | état « mort » |
| 1132 | Corgidoge real estate payment | CORGI | BNB Chain | commune | mort | non | état « mort » |
| 1133 | Mystery | MYSTERY | Ethereum | commune | mort (≈ 22 k$, volume nul) | non | état « mort » |
| 1134 | Oh no | OHNO | à vérifier | commune | mort | non | état « mort » |
| 1135 | Zoomer | ZOOMER | Ethereum | commune | mort | non | état « mort » |
| 1136 | Rage Guy | RAGEGUY | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `rage-guy` : volume 24 h 36 k$, capitalisation 2,6 M$ |
| 1137 | TON DOG | TDOG | TON | commune | mort | non | état « mort » |
| 1138 | Distracted Dudes | DUDE | Base | commune | mort | non | état « mort » |
| 1140 | Memeerkat | MKAT | TON | commune | mort | non | état « mort » |
| 1141 | The Dons | DONS | BNB Chain | commune | mort | non | état « mort » |
| 1142 | BankerCoinAda | BANK | Cardano | commune | mort | non | état « mort » |
| 1143 | BNB Frog Inu | BNBFROG | à vérifier | commune | mort | non | état « mort » |
| 1144 | Boshi | BOSHI | Base | commune | mort | non | état « mort » |
| 1145 | DUMBMONEY | DUMBMONEY | Solana | commune | mort | non | état « mort » |
| 1146 | Minu | MINU | BNB Chain | commune | mort | non | état « mort » |
| 1147 | sunpepe | SUNPEPE | Tron | commune | mort | non | état « mort » |
| 1148 | Vibing Cat Coin | VIBECOIN | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `vibing-cat-coin` : volume 24 h 8 k$, capitalisation 1,7 M$ ; seuils 20 k$ et 1 M$) |
| 1149 | Baby 4 | BABY4 | à vérifier | commune | mort | non | état « mort » |
| 1150 | BEPE | BEPE | Chia | commune | mort | non | état « mort » |
| 1151 | Baby Grok (babygrok.ai) | BABYGROK | BNB Chain | commune | mort | non | état « mort » |
| 1152 | BNB Tiger Inu | BNBTIGER | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `bnb-tiger-inu` : volume 24 h 584 $, capitalisation 1,4 M$ ; seuils 20 k$ et 1 M$) |
| 1153 | LIZARD | LIZARD | Avalanche | commune | mort | non | état « mort » |
| 1154 | Choo Choo | CHOO | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `choo-choo` : volume 24 h 1,2 M$, capitalisation 1,3 M$ |
| 1156 | HODL | HODL | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `hodl-7` : volume 24 h 1,4 M$, capitalisation 4,2 M$ |
| 1157 | Zeal | ZEAL | à vérifier | commune | mort | non | état « mort » |
| 1158 | Biaoqing TRON | BIAO | Tron | commune | mort | non | état « mort » |
| 1159 | Cartoon Money | CBUCKS | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `cartoon-money` : volume 24 h 670 k$, capitalisation 5,1 M$ |
| 1160 | Dagknight Dog | DOGK | Kaspa | commune | mort | non | état « mort » |
| 1161 | Dino | DINO | Base | commune | mort | non | état « mort » |
| 1162 | Unicorn Meat | W🍖 | à vérifier | commune | mort | non | état « mort » |
| 1163 | Resistance Girl | REGI | TON | commune | mort | non | état « mort » |
| 1164 | Feels Good Man | FEELSGOOD | Solana | commune | actif | non | liquidité insuffisante (CoinGecko `feels-good-man-3` : volume 24 h 417 $, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 1165 | Ginnan | GINNAN | Solana | commune | mort | non | état « mort » |
| 1166 | Jambo (meme-cooking) | JAMBO | NEAR | commune | mort | non | état « mort » |
| 1167 | MOTION | MOTION | à vérifier | commune | mort | non | état « mort » |
| 1168 | NianNian | 年年 | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `niannian-2` : volume 24 h 122 k$, capitalisation 1,3 M$ |
| 1169 | OFFICIAL K-POP | KPOP | à vérifier | commune | mort | non | état « mort » |
| 1170 | TON Cats Jetton | CATS | TON | commune | mort | non | état « mort » |
| 1171 | 2131KOBUSHIDE | 21 | Solana | commune | mort (≈ 17 k$) | non | état « mort » |
| 1172 | cat wif sword | SWORDCAT | à vérifier | commune | en déclin | non | liquidité insuffisante (CoinGecko `cat-wif-sword-2` : volume 24 h 239 k$, capitalisation 748 k$ ; seuils 20 k$ et 1 M$) |
| 1173 | DogeShrek | DOGESHREK | Dogechain | commune | mort | non | état « mort » |
| 1174 | Mantle Inu | MINU | Mantle | commune | mort | non | état « mort » |
| 1175 | Yup | YUP | Abstract | commune | mort | non | état « mort » |
| 1176 | CATAMOTO | CATA | BNB Chain | commune | mort | non | état « mort » |
| 1177 | Chog | CHOG | Monad | commune | mort | non | état « mort » |
| 1178 | Keanu | KEANU | Solana | commune | mort | non | état « mort » |
| 1179 | MMM | MMM | TON | commune | mort | non | état « mort » |
| 1180 | Nekonium | NUKO | blockchain propre | commune | mort | non | état « mort » |
| 1181 | New FIST | FIST | BNB Chain | commune | mort (≈ 0,1 M$, volume quasi nul) | non | état « mort » |
| 1182 | WHISKEY | WHISKEY | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `whiskey` : volume 24 h 1 k$, capitalisation 1,1 M$ ; seuils 20 k$ et 1 M$) |
| 1183 | LOXI | LOXI | à vérifier | commune | mort | non | état « mort » |
| 1184 | Shroomy | SHROOMY | Ink | commune | mort | non | état « mort » |
| 1185 | Soulja Boy | SBOY | Solana | commune | mort | non | état « mort » |
| 1186 | Whyyoutouzhele | LI | à vérifier | commune | mort | non | état « mort » |
| 1187 | Anthropig | ANTHROPIG | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `anthropig` : volume 24 h 0 $, capitalisation 2,5 M$ ; seuils 20 k$ et 1 M$) |
| 1188 | Chow Chow | CHOW | Ethereum | commune | mort | non | état « mort » |
| 1189 | Sauce Inu | SAUCEINU | Hedera | commune | mort | non | état « mort » |
| 1190 | WHALE | WHALE | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `whale-4` : volume 24 h 240 k$, capitalisation 3,0 M$ |
| 1191 | Golden Dragon | GD | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `golden-dragon` : volume 24 h 0 $, capitalisation 5,2 M$ ; seuils 20 k$ et 1 M$) |
| 1192 | Monko | MONKO | Algorand | commune | mort | non | état « mort » |
| 1193 | REKT 2.0 | REKT | Base | commune | mort | non | état « mort » |
| 1195 | KekCoin | KEK | à vérifier | commune | mort | non | état « mort » |
| 1196 | Morfey | MORFEY | TON | commune | mort | non | état « mort » |
| 1197 | Anoncoin | ANONCOIN | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `anoncoin-2` : volume 24 h 19 k$, capitalisation 1,8 M$ ; seuils 20 k$ et 1 M$) |
| 1198 | BNBXBT | BNBXBT | BNB Chain | commune | en déclin | non | liquidité insuffisante (CoinGecko `bnbxbt` : volume 24 h 25 k$, capitalisation 48 k$ ; seuils 20 k$ et 1 M$) |
| 1199 | Dark Cheems | TOTAKEKE | BNB Chain | commune | mort | non | état « mort » |
| 1200 | Golden Doge | GDOGE | BNB Chain | commune | mort | non | état « mort » |
| 1201 | Lonk | LONK | NEAR | commune | mort | non | état « mort » |
| 1202 | Michi † | MICHI | Solana | commune | actif | oui | achetable : état « actif », CoinGecko `michi` : volume 24 h 26 k$, capitalisation 1,9 M$ |
| 1203 | Wolfies | PACK | à vérifier | commune | mort | non | état « mort » |
| 1204 | Based Street Bets | BSB | Base | commune | mort | non | état « mort » |
| 1205 | Hachiko Inu | HACHIKO | à vérifier | commune | en déclin | non | liquidité insuffisante (CoinGecko `hachiko-inu-2` : volume 24 h 41 k$, capitalisation 682 k$ ; seuils 20 k$ et 1 M$) |
| 1206 | Oggy Inu | OGGY | BNB Chain | commune | mort | non | état « mort » |
| 1209 | TISM | TISM | Sui | commune | mort | non | état « mort » |
| 1210 | Binance Mascot (Phil) | PHIL | BNB Chain | commune | mort (≈ 26 k$, volume nul) | non | état « mort » |
| 1211 | Doge Pepe | DOPE | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `doge-pepe-4` : volume 24 h 434 k$, capitalisation 1,1 M$ |
| 1212 | Dogs Rock | DOGSROCK | BNB Chain | commune | mort | non | état « mort » |
| 1213 | FEFER | FEFER | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `fefer-2` : volume 24 h 0 $, capitalisation 1,6 M$ ; seuils 20 k$ et 1 M$) |
| 1214 | FORTUNE FAVOURS THE BRAVE | FFTB | Cronos | commune | mort | non | état « mort » |
| 1215 | Grok Girl | GROKGIRL | BNB Chain | commune | mort | non | état « mort » |
| 1216 | saucecoin | SAUCE | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `saucecoin` : volume 24 h 103 k$, capitalisation 3,8 M$ |
| 1217 | Shib Army | SHIBARMY | BNB Chain | commune | mort | non | état « mort » |
| 1218 | Suiba Inu | SUIB | Sui | commune | mort | non | état « mort » |
| 1219 | ZenPandaCoin | ZPC | Arbitrum | commune | mort | non | état « mort » |
| 1220 | BankerDoge | BANKER | BNB Chain | commune | mort | non | état « mort » |
| 1221 | Infinite Money Glitch | GLITCH | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `infinite-money-glitch-3` : volume 24 h 347 k$, capitalisation 2,2 M$ |
| 1222 | Kraken | KRAKEN | Ink | commune | mort | non | état « mort » |
| 1223 | NASDANQ | NASDANQ | à vérifier | commune | mort | non | état « mort » |
| 1224 | Brett 2.0 | BRETT2.0 | Base | commune | mort | non | état « mort » |
| 1225 | Dog With Purpose | DOPU | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `dog-with-purpose` : volume 24 h 133 k$, capitalisation 1,2 M$ |
| 1226 | FlareFox | FLX | Flare | commune | mort | non | état « mort » |
| 1227 | Marvin | MARVIN | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `marvin-3` : volume 24 h 11 k$, capitalisation 1,4 M$ ; seuils 20 k$ et 1 M$) |
| 1228 | 42-coin | 42 | blockchain propre | commune | mort | non | état « mort » |
| 1229 | AudaCity | DACITYCOIN | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `audacity` : volume 24 h 4,0 M$, capitalisation 2,4 M$ |
| 1230 | ClipX | CLIPX | à vérifier | commune | en déclin | non | liquidité insuffisante (CoinGecko `klipx-x-tips` : volume 24 h 34 k$, capitalisation 525 k$ ; seuils 20 k$ et 1 M$) |
| 1231 | Zhao Cai Mao | 招财猫 | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `zhao-cai-mao` : volume 24 h 64 k$, capitalisation 2,2 M$ |
| 1232 | 8Bit Doge | BITD | BNB Chain | commune | mort | non | état « mort » |
| 1233 | BNB MEME SZN | SZN | BNB Chain | commune | en déclin | non | liquidité insuffisante (CoinGecko `bnb-meme-szn` : volume 24 h 25 k$, capitalisation 70 k$ ; seuils 20 k$ et 1 M$) |
| 1234 | FlappyCoin | FLAP | blockchain propre | commune | mort | non | état « mort » |
| 1235 | OPEN Tony | OPEN | TON | commune | en déclin | non | liquidité insuffisante (CoinGecko `open-tony` : volume 24 h 0 $, capitalisation 243 k$ ; seuils 20 k$ et 1 M$) |
| 1236 | Optimus | OPTIMUS | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `optimus-2` : volume 24 h 17 k$, capitalisation 1,5 M$ ; seuils 20 k$ et 1 M$) |
| 1237 | Scamcoin | SCAM | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `scamcoin` : volume 24 h 25 k$, capitalisation 2,7 M$ |
| 1238 | BNBEE | BEE | BNB Chain | commune | mort | non | état « mort » |
| 1239 | DOGEMOB | DOGEMOB | BNB Chain | commune | mort | non | état « mort » |
| 1240 | Long Mao | LMAO | Zksync Era | commune | mort | non | état « mort » |
| 1241 | Whiskers | WHISK | TON | commune | mort | non | état « mort » |
| 1242 | Aster Dog | ADOG | BNB Chain | commune | mort (≈ 10 k$) | non | état « mort » |
| 1243 | Energy | NRG | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `energy-2` : volume 24 h 4 k$, capitalisation 1,2 M$ ; seuils 20 k$ et 1 M$) |
| 1244 | ShibaPoconk | CONK | Fantom | commune | mort | non | état « mort » |
| 1245 | World is Flat | WIF | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `world-is-flat` : volume 24 h 96 k$, capitalisation 1,3 M$ |
| 1246 | Chameleon | CHAMELEON | Hyperliquid | commune | mort | non | état « mort » |
| 1247 | Croak | CROAK | Linea | commune | mort | non | état « mort » |
| 1249 | one life, its worth an attempt | WORTH | à vérifier | commune | mort | non | état « mort » |
| 1250 | Panana | PANANA | à vérifier | commune | mort | non | état « mort » |
| 1251 | THAT | THAT | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `that` : volume 24 h 17 k$, capitalisation 3,7 M$ ; seuils 20 k$ et 1 M$) |
| 1252 | 超级周期 (Supercycle) | 超级周期 | BNB Chain | commune | mort (≈ 13 k$) | non | état « mort » |
| 1253 | puush da button | PUUSH | Cronos | commune | mort | non | état « mort » |
| 1254 | Spice | SPICE | Osmosis | commune | mort | non | état « mort » |
| 1255 | AI PEPE KING | AIPEPE | Polygon | commune | mort | non | état « mort » |
| 1257 | CeramicLiberty.com | CL8Y | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `ceramicliberty-com` : volume 24 h 37 $, capitalisation 1,4 M$ ; seuils 20 k$ et 1 M$) |
| 1258 | HOdlcoin | HODL | blockchain propre | commune | mort | non | état « mort » |
| 1259 | Shitcoin on TON | SHIT | TON | commune | mort | non | état « mort » |
| 1260 | Trollcoin | TROLL | blockchain propre | commune | mort | non | état « mort » |
| 1261 | Scuba Dog | SCUBA | Sui | commune | mort | non | état « mort » |
| 1262 | Beast | BEAST | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `beast` : volume 24 h 34 k$, capitalisation 958 k$ ; seuils 20 k$ et 1 M$) |
| 1263 | Buffy | BUFFY | TON | commune | mort | non | état « mort » |
| 1264 | Clippy | CLIPPY | Solana | commune | mort (≈ 26 k$) | non | état « mort » |
| 1266 | PONGO | PONGO | Xrp Ledger | commune | mort | non | état « mort » |
| 1267 | Suimon | SUIMON | Sui | commune | mort | non | état « mort » |
| 1268 | Tonio | TONIO | TON | commune | mort | non | état « mort » |
| 1269 | Hot Cherry | à vérifier | TON | commune | actif | non | liquidité insuffisante (CoinGecko `hot-cherry` : volume 24 h 15 k$, capitalisation 1,0 M$ ; seuils 20 k$ et 1 M$) |
| 1270 | tomochi | TOMOCHI | à vérifier | commune | mort | non | état « mort » |
| 1271 | CRYPTO CLOUD | CLOUD | à vérifier | commune | mort | non | état « mort » |
| 1272 | Kittehcoin | MEOW | blockchain propre | commune | mort | non | état « mort » |
| 1273 | Krex | KREX | Kaspa | commune | mort | non | état « mort » |
| 1274 | Baby Brett on Base | BBRETT | Base | commune | mort | non | état « mort » |
| 1275 | BabyCate | BABYCATE | BNB Chain | commune | mort | non | état « mort » |
| 1276 | daCat | DACAT | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `dacat` : volume 24 h 10 $, capitalisation 1,2 M$ ; seuils 20 k$ et 1 M$) |
| 1277 | Davido † | DAVIDO | Solana | commune | mort | non | état « mort » |
| 1279 | Huebel Bolt | BOLT | TON | commune | mort | non | état « mort » |
| 1280 | OciCat Token | OCICAT | BNB Chain | commune | mort | non | état « mort » |
| 1281 | zuzalu | ZUZALU | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `zuzalu` : volume 24 h 34 k$, capitalisation 1,1 M$ |
| 1282 | Bluzo | BLZ | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `bluzo` : volume 24 h 0 $, capitalisation 2,1 M$ ; seuils 20 k$ et 1 M$) |
| 1283 | Frogonsol | FROG | à vérifier | commune | mort | non | état « mort » |
| 1284 | KOROMARU | KOROMARU | Ethereum | commune | mort | non | état « mort » |
| 1285 | Spacebucks | SBX | à vérifier | commune | mort | non | état « mort » |
| 1286 | Tong | TONG | TON | commune | mort | non | état « mort » |
| 1287 | UNIVERSE | UNIVERSE | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `universe-3` : volume 24 h 299 $, capitalisation 2,7 M$ ; seuils 20 k$ et 1 M$) |
| 1288 | Brett's Dog | BROGG | Base | commune | mort | non | état « mort » |
| 1289 | DUMMY | DUMMY | à vérifier | commune | mort | non | état « mort » |
| 1290 | Giggle Panda | GIGL | BNB Chain | commune | mort | non | état « mort » |
| 1291 | MIZU KAPPA | MIZU | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `mizu-kappa` : volume 24 h 1 k$, capitalisation 1,6 M$ ; seuils 20 k$ et 1 M$) |
| 1292 | Papa Doge | PAPADOGE | BNB Chain | commune | mort | non | état « mort » |
| 1293 | Purple | PURPLE | Ink | commune | mort | non | état « mort » |
| 1294 | sunlion | SUNLION | Tron | commune | mort | non | état « mort » |
| 1295 | TOGE | TOGE | TON | commune | mort | non | état « mort » |
| 1296 | Nads | NADS | Monad | commune | mort | non | état « mort » |
| 1297 | ShibaZilla | SHIBZ | BNB Chain | commune | mort | non | état « mort » |
| 1298 | The Corgi of PolkaBridge | CORGIB | BNB Chain | commune | mort | non | état « mort » |
| 1299 | This Is Fine (ETH) | FINE | Ethereum | commune | mort | non | état « mort » |
| 1301 | xiao lang gou | XLG | Tron | commune | mort | non | état « mort » |
| 1302 | Crobinhood | CROBINHOOD | à vérifier | commune | actif | oui | achetable : état « actif », CoinGecko `crobinhood` : volume 24 h 25 k$, capitalisation 1,1 M$ |
| 1303 | BabyDogeZilla | BABYDOGEZILLA | BNB Chain | commune | mort | non | état « mort » |
| 1304 | Funds Are Safu | SAFU | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `funds-are-safu-2` : volume 24 h 409 k$, capitalisation 784 k$ ; seuils 20 k$ et 1 M$) |
| 1305 | Internet Doge | IDOGE | Internet Computer | commune | mort | non | état « mort » |
| 1306 | Joe Hat | HAT | Avalanche | commune | mort | non | état « mort » |
| 1309 | Saudi Shiba Inu | SAUDISHIB | Ethereum | commune | mort | non | état « mort » |
| 1310 | Solala (索拉拉) | 索拉拉 | Solana | commune | mort | non | état « mort » |
| 1311 | Battle Inu | BINU | BNB Chain | commune | mort | non | état « mort » |
| 1312 | DogeCube | DOGECUBE | Radix | commune | mort | non | état « mort » |
| 1313 | Nyancoin | NYAN | blockchain propre | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1314 | The Loonies | LOON | Aptos | commune | mort | non | état « mort » |
| 1315 | Wobbles | WOBBLES | à vérifier | commune | mort | non | état « mort » |
| 1316 | HoboNickels | HBN | blockchain propre | commune | mort | non | état « mort » |
| 1317 | Kroak on Kaspa | KROAK | Kaspa | commune | mort | non | état « mort » |
| 1318 | Long | LONG | Zksync Era | commune | mort | non | état « mort » |
| 1320 | CorgiCoin (2014) | CORG | blockchain propre | commune | mort | non | état « mort » |
| 1321 | HBARbarian | HBARBARIAN | Hedera | commune | mort | non | état « mort » |
| 1322 | Liquid Cat | CAT | Hyperliquid | commune | en déclin | non | liquidité insuffisante (CoinGecko `cat-2` : volume 24 h 111 $, capitalisation 116 k$ ; seuils 20 k$ et 1 M$) |
| 1323 | Poodlecoin | POODLE | Flare | commune | mort | non | état « mort » |
| 1324 | Saiyan PEPE | SPEPE | Polygon | commune | mort | non | état « mort » |
| 1325 | 亮剑出击 | 亮剑出击 | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `liang-jian-chu-ji` : volume 24 h 6 k$, capitalisation 1,7 M$ ; seuils 20 k$ et 1 M$) |
| 1326 | BIRTHDAY | BIRTHDAY | à vérifier | commune | mort | non | état « mort » |
| 1327 | Chonk The Cat | CHONK | BNB Chain | commune | mort | non | état « mort » |
| 1328 | GoldenRat | RATS | BNB Chain | commune | mort | non | état « mort » |
| 1330 | Kishimoto Inu | KISHIMOTO | Ethereum | commune | mort | non | état « mort » |
| 1331 | Pizza | PIZZA | Bitcoin | commune | mort | non | état « mort » |
| 1332 | SAD MEOW | SADMEOW | TON | commune | mort | non | état « mort » |
| 1333 | The Nation Token | NATO | Base | commune | mort | non | état « mort » |
| 1334 | DogeCash | DOGEC | blockchain propre | commune | mort | non | état « mort » |
| 1335 | DOPU The Dog with A Purpose | DOPU | Xdc Network | commune | mort | non | état « mort » |
| 1336 | Hestia | HESTIA | à vérifier | commune | mort | non | état « mort » |
| 1337 | KanadeCoin | KNDC | Ethereum | commune | mort | non | état « mort » |
| 1338 | Lil Pump | LILPUMP | Solana | commune | mort | non | état « mort » |
| 1339 | meh on TON | MEH | TON | commune | mort | non | état « mort » |
| 1340 | ShibaKeanu | SHIBK | à vérifier | commune | mort | non | état « mort » |
| 1341 | VIPER | VIPER | Cardano | commune | mort | non | état « mort » |
| 1342 | Chucky | CHUCKY | Cronos | commune | mort | non | état « mort » |
| 1343 | DOGMI | DOGMI | Internet Computer | commune | mort | non | état « mort » |
| 1344 | Linpuss | LPUSS | Linea | commune | mort | non | état « mort » |
| 1345 | LOBIN | LOBIN | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `lobin` : volume 24 h 48 k$, capitalisation 648 k$ ; seuils 20 k$ et 1 M$) |
| 1346 | NinjaCat | NINJACAT | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `ninjacat` : volume 24 h 9 k$, capitalisation 1,2 M$ ; seuils 20 k$ et 1 M$) |
| 1347 | ZenFrogs | ZEN | Sui | commune | mort | non | état « mort » |
| 1348 | Delivery Guy | DGUY | à vérifier | commune | actif | non | liquidité insuffisante (CoinGecko `delivery-guy` : volume 24 h 69 k$, capitalisation 735 k$ ; seuils 20 k$ et 1 M$) |
| 1349 | GMONAD | GMONAD | Monad | commune | mort | non | état « mort » |
| 1350 | KOI | KOI | Sui | commune | mort | non | état « mort » |
| 1351 | emo | EMO | Monad | commune | mort | non | état « mort » |
| 1352 | UltCat | ULTCAT | à vérifier | commune | mort | non | état « mort » |
| 1353 | Bear Bull | BRB | Xrp Ledger | commune | mort | non | état « mort » |
| 1354 | FOMO BULL CLUB | FOMO | Base | commune | mort | non | état « mort » |
| 1356 | Meowcat | MEOW | Avalanche | commune | mort | non | état « mort » |
| 1357 | PADAWAN | PADAWAN | Multiversx | commune | mort | non | état « mort » |
| 1358 | PSYOP † | PSYOP | Ethereum | commune | mort | non | état « mort » |
| 1359 | Zeekwifhat | ZWIF | Zksync Era | commune | mort | non | état « mort » |
| 1360 | Book of Miggles | BOMI | Base | commune | en déclin | non | liquidité insuffisante (CoinGecko `book-of-miggles` : volume 24 h 113 $, capitalisation 138 k$ ; seuils 20 k$ et 1 M$) |
| 1361 | Cat Wif Hands | CATWIF | Avalanche | commune | mort | non | état « mort » |
| 1362 | Neiro on Tron | NEIRO | Tron | commune | mort | non | état « mort » |
| 1363 | Walrus the tusk | TUSK | Sui | commune | mort | non | état « mort » |
| 1364 | zkDoge | ZKDOGE | Zksync Era | commune | mort | non | état « mort » |
| 1365 | 死了么 (T'es mort ?) | 死了么 | BNB Chain | commune | mort (≈ 80 k$, volume nul) | non | état « mort » |
| 1366 | Based Coin | BASED | Base | commune | mort | non | état « mort » |
| 1367 | Doge Base | DOGEBASE | Base | commune | mort | non | état « mort » |
| 1368 | 财富人生 | 财富人生 | à vérifier | commune | mort | non | état « mort » |
| 1369 | ChanCoin | CHAN | blockchain propre | commune | mort | non | état « mort » |
| 1370 | Resistance Duck | à vérifier | TON | commune | mort | non | état « mort » |
| 1371 | Sharbi | SHARBI | Ethereum | commune | mort | non | état « mort » |
| 1372 | SwagBucks | BUCKS | blockchain propre | commune | mort | non | état « mort » |
| 1373 | Evil Coin | EVIL | blockchain propre | commune | mort | non | état « mort » |
| 1374 | EXCELLENCE | EOP | à vérifier | commune | mort | non | état « mort » |
| 1375 | Illuminati | ILUM | à vérifier | commune | mort | non | état « mort » |
| 1376 | Just a peace guy | PEACEGUY | Solana | commune | mort (≈ 40 k$) | non | état « mort » |
| 1377 | PUGWIFHAT | PUGWIF | Sui | commune | mort | non | état « mort » |
| 1379 | To The Sun | SUNPUMP | Tron | commune | mort | non | état « mort » |
| 1380 | Troll in Hood | TROLL | à vérifier | commune | mort | non | état « mort » |
| 1382 | Doge Killer † | LEASH | Ethereum | commune | en déclin (-95 % ou pire) | non | liquidité insuffisante (CoinGecko `leash` : volume 24 h 576 $, capitalisation 1,3 M$ ; seuils 20 k$ et 1 M$) |
| 1383 | BabyUSDT | BABYUSDT | BNB Chain | commune | mort | non | état « mort » |
| 1384 | BBBPump.fun & Beny Bad Boy | BBB | Xdc Network | commune | mort | non | état « mort » |
| 1386 | Corgi Inu (corgibnb.com) | CORGI | BNB Chain | commune | mort | non | état « mort » |
| 1387 | TRON MASCOT | SUNTRON | à vérifier | commune | mort | non | état « mort » |
| 1388 | Dobermann | DOBERMANN | à vérifier | commune | mort | non | état « mort » |
| 1389 | GRIOT | GRIOT | à vérifier | commune | mort | non | état « mort » |
| 1390 | Infinite Sui Glitch | ISG | Sui | commune | mort | non | état « mort » |
| 1391 | Jelly Finance Baby | JFB | à vérifier | commune | mort | non | état « mort » |
| 1392 | Sui Bull | BULL | Sui | commune | mort | non | état « mort » |
| 1393 | cats (BRC-20) | CATS | Bitcoin | commune | mort | non | état « mort » |
| 1395 | FuzzBalls | FUZZ | blockchain propre | commune | mort | non | état « mort » |
| 1396 | Zoki | ZOKI | à vérifier | commune | mort | non | état « mort » |
| 1397 | Catcoin (2013) | CAT | blockchain propre | commune | mort | non | état « mort » |
| 1398 | SpacePenguin | PNGN | BNB Chain | commune | mort | non | état « mort » |
| 1399 | Hogdog | HOGDOG | Monad | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1400 | Akita Inu | AKITA | Ethereum | commune | mort | non | état « mort » |
| 1401 | Rare Pepe Party | RAREPEPEP | Counterparty (Bitcoin) | commune | mort | non | état « mort » |
| 1402 | Blue Guy | BLUE | Base | commune | mort | non | état « mort » |
| 1403 | Gavun Wud | WUD | à vérifier | commune | mort | non | état « mort » |
| 1405 | Based Mog Coin | MOG | Base | commune | mort | non | état « mort » |
| 1407 | Gold Pressed Latinum | GPL | blockchain propre | commune | mort | non | état « mort » |
| 1409 | MoonPirate | MOONPIRATE | BNB Chain | commune | mort | non | état « mort » |
| 1411 | CLANKTARDIO | CLANKTARDIO | Base | commune | mort | non | état « mort » |
| 1413 | Useless Ethereum Token † | UET | Ethereum | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1414 | Rocket Bunny | BUNNY | Ethereum | commune | mort | non | état « mort » |
| 1415 | Cthulhu Offerings | OFF | blockchain propre | commune | mort (retiré de CMC en mai 2018) | non | état « mort » |
| 1418 | SHIBORG INU | SHIBORG | BNB Chain | commune | mort | non | état « mort » |
| 1420 | Wall Street Baby | WSB | Ethereum | commune | mort | non | état « mort » |
| 1421 | ShibeCoin | SHIBE | blockchain propre | commune | mort | non | état « mort » |
| 1422 | Grumpycoin | GRUMP | blockchain propre | commune | mort | non | état « mort » |
| 1424 | Orlycoin | ORLY | blockchain propre | commune | mort | non | état « mort » |
| 1425 | Pandacoin (PANDA) | PANDA | blockchain propre | commune | mort | non | état « mort » |
| 1426 | BadgerCoin | BDG | blockchain propre | commune | mort | non | état « mort » |
| 1427 | Conspiracycoin | CYC | blockchain propre | commune | mort | non | état « mort » |
| 1429 | YoloCash | YLC | Ethereum | commune | mort | non | état « mort » |
| 1430 | Ponzicoin | PONZI | blockchain propre | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1431 | FAILCoin | FAIL | blockchain propre | commune | mort | non | état « mort » |
| 1432 | Penguincoin (old) | PENG | blockchain propre | commune | mort | non | état « mort » |
| 1433 | Heisenberg | HEX | blockchain propre | commune | mort | non | état « mort » |
| 1434 | 23 Skidoo | CHAO | blockchain propre | commune | mort | non | état « mort » |
| 1435 | RabbitCoin | RBBT | blockchain propre | commune | mort | non | état « mort » |
| 1436 | BatCoin | BAT | blockchain propre | commune | mort | non | état « mort » |
| 1437 | DuckDuckCoin | DUCK | blockchain propre | commune | mort | non | état « mort » |
| 1438 | Cheesecoin | CHEESE | blockchain propre | commune | mort | non | état « mort » |
| 1440 | X-Children | CHILD | blockchain propre | commune | mort | non | état « mort » |
| 1441 | Dobbscoin | BOB | blockchain propre | commune | mort | non | état « mort » |
| 1442 | DarkShibe | DSB | blockchain propre | commune | mort | non | état « mort » |
| 1443 | EmotiCoin | EMO | blockchain propre | commune | mort | non | état « mort » |
| 1444 | Animecoin (2014) | ANI | blockchain propre | commune | mort | non | état « mort » |
| 1445 | Gossipcoin | GOSS | blockchain propre | commune | à vérifier | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 1446 | DolphinCoin | DOLP | blockchain propre | commune | mort | non | état « mort » |
| 1447 | GorillaBucks | BUCKS | blockchain propre | commune | mort | non | état « mort » |
| 1448 | MugatuCoin | MUGA | blockchain propre | commune | mort | non | état « mort » |
| 1449 | Pyramids | PYRA | blockchain propre | commune | mort | non | état « mort » |
| 1450 | Huskycoin | HC | blockchain propre | commune | mort | non | état « mort » |
| 1451 | Lycancoin | LYC | blockchain propre | commune | mort | non | état « mort » |
| 1452 | LemurCoin | LMR | blockchain propre | commune | mort | non | état « mort » |
| 1453 | Aliencoin | ALN | blockchain propre | commune | mort | non | état « mort » |
| 1454 | Selfiecoin | SLFI | blockchain propre | commune | mort | non | état « mort » |
| 1455 | CrackCoin | CRACK | blockchain propre | commune | mort | non | état « mort » |
| 1456 | Doomcoin | DOOM | blockchain propre | commune | mort | non | état « mort » |
| 1457 | BananaBits | NANAS | blockchain propre | commune | mort | non | état « mort » |
| 1458 | Dougcoin | DOUG | blockchain propre | commune | mort | non | état « mort » |
| 1459 | MtGoxCoin | GOX | blockchain propre | commune | mort | non | état « mort » |
| 1460 | NoodlyAppendageCoin | NDL | blockchain propre | commune | mort | non | état « mort » |
| 1461 | Fonziecoin | FONZ | blockchain propre | commune | mort | non | état « mort » |
| 1462 | Tomatocoin | TMT | blockchain propre | commune | mort | non | état « mort » |
| 1463 | Hobbitcoin | HBC | blockchain propre | commune | mort | non | état « mort » |
| 1465 | RipoffCoin | RIPO | blockchain propre | commune | mort | non | état « mort » |
| 1466 | NewWorldOrderCoin | NWO | blockchain propre | commune | mort | non | état « mort » |
| 1467 | TacoCoin | TCO | blockchain propre | commune | mort | non | état « mort » |
| 1468 | Chococoin | CCC | blockchain propre | commune | mort | non | état « mort » |
| 1471 | CandyCoin | YUM | blockchain propre | commune | mort | non | état « mort » |
| 1472 | Unattainium | UNAT | blockchain propre | commune | mort | non | état « mort » |
| 1473 | CryptoMETH | METH | blockchain propre | commune | mort | non | état « mort » |
| 1474 | Tamagucci | TAM | blockchain propre | commune | mort | non | état « mort » |
| 1476 | DogeBlackCoin | DOGEBC | blockchain propre | commune | mort | non | état « mort » |
| 1477 | NopeCoin | NOPE | blockchain propre | commune | mort | non | état « mort » |
| 1478 | SiameseCoin | SIS | blockchain propre | commune | mort | non | état « mort » |
| 1481 | Frycoin | FRY | blockchain propre | commune | mort | non | état « mort » |
| 1483 | LeproCoin | LPC | blockchain propre | commune | mort | non | état « mort » |
| 1484 | Magic Internet Money | MIM | blockchain propre | commune | mort | non | état « mort » |
| 1486 | PotatoCoin | SPUDS | blockchain propre | commune | mort | non | état « mort » |
| 1487 | ConfessionCoin | CFN | blockchain propre | commune | mort | non | état « mort » |
| 1488 | FistBump | FIST | blockchain propre | commune | mort | non | état « mort » |
| 1489 | REKTcoin | REKT | blockchain propre | commune | mort | non | état « mort » |
| 1490 | 100xCoin | 100X | BNB Chain | commune | mort | non | état « mort » |
| 1491 | ABG | ABG | NEAR | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1492 | Andwu Tet | à vérifier | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1493 | Arbi Pepe | PEPE (Arbitrum) | Arbitrum | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1494 | Arbinu | ARBINU | Arbitrum | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1495 | Baby Arbitrum | BARB | Arbitrum | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1496 | Bananacoin | BCO | à vérifier | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1497 | Base Baboon | BOON | Base | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1499 | Big Dog Coin | BDOG | BNB Chain | commune | mort | non | état « mort » |
| 1500 | BitCone | CONE | Polygon | commune | mort | non | état « mort » |
| 1501 | blobs | BLOBS | Ethereum | commune | mort | non | état « mort » |
| 1502 | Bombardiro | à vérifier | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1503 | Bomeow | BOMEOW | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1504 | Boom Shiba | BOOMSHIBA | BNB Chain | commune | mort | non | état « mort » |
| 1505 | Bugg Inu | BUGG | Ethereum | commune | mort | non | état « mort » |
| 1506 | Captain Shibarrow | SHIBARROW | BNB Chain | commune | mort | non | état « mort » |
| 1507 | CATS•IN•THE•SATS | CATS | Bitcoin | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1508 | Cheems Inu | CINU | Ethereum | commune | mort | non | état « mort » |
| 1509 | ChillDeer | CHILLDEER | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1510 | Christmas Floki X | CFloki X | BNB Chain | commune | mort | non | état « mort » |
| 1511 | CoShi Inu | COSHI | Ethereum | commune | mort | non | état « mort » |
| 1512 | CYPHER•GENESIS | CYPHER | Bitcoin | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1514 | DED † | DED | Polkadot | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1515 | Dink Doink | DINK | à vérifier | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1516 | Doge Dash | DOGEDASH | à vérifier | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1518 | DogeWarrior | DWR | BNB Chain | commune | mort | non | état « mort » |
| 1519 | DogeZilla | DOGEZILLA | BNB Chain | commune | mort | non | état « mort » |
| 1520 | DogWifCat | à vérifier | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1522 | Dragon Sun | DRGN | Tron | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1523 | DropArb | DROP | Arbitrum | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1526 | ETHEREUM IS GOOD | EBULL | Ethereum | commune | mort | non | état « mort » |
| 1528 | Fairmoon | FAIR | BNB Chain | commune | mort | non | état « mort » |
| 1529 | Fantasy Pepe | FEPE | Polygon | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1530 | Fantom Doge | RIP | Fantom | commune | mort | non | état « mort » |
| 1532 | Floki Shiba | FSHIB | BNB Chain | commune | mort | non | état « mort » |
| 1533 | Flokinomics | FLOKIN | BNB Chain | commune | mort | non | état « mort » |
| 1536 | GloryDoge | GLORYD | BNB Chain | commune | mort | non | état « mort » |
| 1537 | GMEKitty | GMEKITTY | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1538 | GNEAR | GNEAR | NEAR | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1540 | GotFomo | GTFO | blockchain propre | commune | mort | non | état « mort » |
| 1542 | Green Shiba Inu | GINU | BNB Chain | commune | mort | non | état « mort » |
| 1543 | Grumpy Cat Coin | GRUMPY | Ethereum | commune | mort | non | état « mort » |
| 1544 | Hasbulla | HASBI | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1545 | HeMa | à vérifier | BNB Chain | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1546 | HODL 2.0 | HODL | BNB Chain | commune | mort | non | état « mort » |
| 1549 | Intel (Intear) | INTEL | NEAR | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1550 | International Squid Games | SQUIDGAMES | BNB Chain | commune | mort | non | état « mort » |
| 1552 | Jindoge | JINDOGE | Ethereum | commune | mort | non | état « mort » |
| 1553 | Kekec the Balkan Dwarf | KEKEC | Ethereum | commune | mort | non | état « mort » |
| 1554 | Kermit | KERMIT | Ethereum | commune | mort | non | état « mort » |
| 1556 | Kilo Shiba Inu | KSHIB | à vérifier | commune | mort | non | état « mort » |
| 1557 | King Floki | KING | BNB Chain | commune | mort | non | état « mort » |
| 1558 | Kurama Inu | KUNU | Ethereum | commune | mort | non | état « mort » |
| 1559 | La Doge de Papel | LDDP | BNB Chain | commune | mort | non | état « mort » |
| 1560 | Ligo | LIGO | Bitcoin | commune | mort | non | état « mort » |
| 1561 | Lucky Meow Coin | LMAO | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1562 | MaskDoge | MASKDOGE | BNB Chain | commune | mort | non | état « mort » |
| 1563 | Maxi Doge | MAXI | BNB Chain | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1564 | MEME•ECONOMICS | MEMERUNE | Bitcoin | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1565 | Mice | MICE | Bitcoin | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1567 | Mini Baby Doge | MINIBABYDOGE | BNB Chain | commune | mort | non | état « mort » |
| 1568 | Mini Kishu | MINIKISHU | BNB Chain | commune | mort | non | état « mort » |
| 1569 | Mini Shiba | MINISHIBA | BNB Chain | commune | mort | non | état « mort » |
| 1570 | Molandak | MOLANDAK | Monad | commune | mort | non | état « mort » |
| 1571 | MONCAT | MONCAT | Monad | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1572 | Moon Token | MOONTOKEN | BNB Chain | commune | mort | non | état « mort » |
| 1574 | MoonMoon | MOONMOON | BNB Chain | commune | mort | non | état « mort » |
| 1575 | Mouch | à vérifier | Monad | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1576 | Moyaki | à vérifier | Monad | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1577 | Muncat | MUNCAT | Tron | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1578 | Nano Doge Token | NANODOGE | BNB Chain | commune | mort | non | état « mort » |
| 1579 | Nano Dogecoin | NDC | BNB Chain | commune | mort | non | état « mort » |
| 1580 | NOEAR | NOEAR | NEAR | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1581 | Nostalgia | NOS | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1582 | Olen Mosk | à vérifier | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1583 | Oxbt | OXBT | Bitcoin | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1584 | Pepe 3.0 | PEPE3.0 | Ethereum | commune | mort | non | état « mort » |
| 1585 | Pepe Inu | PEPEINU | Ethereum | commune | mort | non | état « mort » |
| 1586 | Pepe on Monad | à vérifier | Monad | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1587 | Pepe Ordinals | PEPE | Bitcoin | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1588 | Pepoclown | HONK | Ethereum | commune | mort | non | état « mort » |
| 1589 | Poodlana | à vérifier | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1592 | Punch | PUNCH | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1593 | PUP | PUP | BNB Chain | commune | en déclin (≈ 0,19 M$) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 1594 | Raptor Jesus | RAPTOR | Ethereum | commune | mort | non | état « mort » |
| 1595 | Rats † | RATS | Bitcoin | commune | à vérifier (homonyme sur CoinGecko, non rapproché) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 1596 | RED | RED | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1598 | Roar | ROAR | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1599 | Safe Star | SAFESTAR | BNB Chain | commune | mort | non | état « mort » |
| 1600 | SafeGalaxy | SAFEGALAXY | BNB Chain | commune | mort | non | état « mort » |
| 1601 | SAFEPLUTO69 | SAFEPLUTO | BNB Chain | commune | mort | non | état « mort » |
| 1602 | Saitama Inu † | SAITAMA | Ethereum | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1603 | Sanshu Inu | SANSHU | Ethereum | commune | mort | non | état « mort » |
| 1604 | Santa Floki | HOHOHO | BNB Chain | commune | mort | non | état « mort » |
| 1606 | SEPPUKU•IN•MAY•AND•GO•AWAY | SEPPUKU | Bitcoin | commune | actif | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 1608 | Shib2.0 | SHIB2.0 | Ethereum | commune | mort | non | état « mort » |
| 1609 | Shiba 2.0 | SHIBA 2.0 | Ethereum | commune | mort | non | état « mort » |
| 1610 | Shiba Lite | SHIBLITE | BNB Chain | commune | mort | non | état « mort » |
| 1611 | Shiba Monk | SHIBAMONK | BNB Chain | commune | mort | non | état « mort » |
| 1612 | SHIBA2K22 | SHIBA22 | BNB Chain | commune | mort | non | état « mort » |
| 1613 | ShibaCash | SHIBACASH | BNB Chain | commune | mort | non | état « mort » |
| 1614 | ShibaCorgi | SHICO | BNB Chain | commune | mort | non | état « mort » |
| 1615 | Shibanomics | SHIBIN | BNB Chain | commune | mort | non | état « mort » |
| 1616 | ShibX | ShibX | BNB Chain | commune | mort | non | état « mort » |
| 1617 | Sincere Doge | SDOGE | BNB Chain | commune | mort | non | état « mort » |
| 1618 | Skibidi | à vérifier | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1619 | SMLE | SMLE | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1620 | Smog | SMOG | Ethereum | commune | mort | non | état « mort » |
| 1621 | SolanaDoge | à vérifier | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1622 | Solciety | à vérifier | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1623 | Son of Shib | SON | BNB Chain | commune | mort | non | état « mort » |
| 1624 | SpaceCorgi | SCORGI | BNB Chain | commune | mort | non | état « mort » |
| 1625 | Spooky Shiba | SpookyShiba | BNB Chain | commune | mort | non | état « mort » |
| 1626 | Squid Pet | SQUIDPET | BNB Chain | commune | mort | non | état « mort » |
| 1627 | Squidanomics | SQUID | BNB Chain | commune | mort | non | état « mort » |
| 1628 | Suijak | SUIJAK | Sui | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1629 | Surge Inu | SURGE | BNB Chain | commune | mort | non | état « mort » |
| 1630 | Tamadoge † | TAMA | Ethereum | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1631 | Tata | TATA | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1632 | TikTok Memes | TIKTOK | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1633 | TJR | TJR | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1635 | Tsuzuki Inu | TZKI | Ethereum | commune | mort | non | état « mort » |
| 1636 | TurtSat | TURT | Bitcoin | commune | à vérifier (homonyme sur CoinGecko, non rapproché) | non | aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée |
| 1637 | Twerk Finance | TWERK | BNB Chain | commune | mort | non | état « mort » |
| 1638 | Uncle Doge | UDOGE | BNB Chain | commune | mort | non | état « mort » |
| 1639 | UNIMOON | UNIMOON | BNB Chain | commune | mort | non | état « mort » |
| 1641 | Watcoin | WAT | blockchain propre | commune | mort | non | état « mort » |
| 1642 | Whale Fall | Whale | BNB Chain | commune | mort | non | état « mort » |
| 1643 | WhitePepe | WHITEPEPE | Solana | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1644 | Wojak Finance | WOJ | à vérifier | commune | mort (absent de CoinGecko) | non | état « mort » |
| 1645 | Yellow Ket | KET | Avalanche | commune | mort (absent de CoinGecko) | non | état « mort » |
