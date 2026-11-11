# Couverture NEAR Intents : quels memecoins on peut vraiment brûler

Relevé du 11 novembre 2026, vers 01 h UTC. Données brutes dans `data/` : la liste
`intents-tokens-2026-11-11.json` et les devis `intents-devis-2026-11-11.json`. Pour relancer :
`python3 -I docs/devis-intents.py <tokens.json> <sortie.json>`.

**Méthode.** `GET https://1click.chaindefuser.com/v0/tokens`, puis pour chaque memecoin des devis
`POST /v0/quote` en `dry: true`, `EXACT_INPUT`, `INTENTS` → `INTENTS`, depuis wNEAR, à 1, 10, 100 et 1 000 $, avec 1 % de
slippage toléré. Le retrait est mesuré par un devis `recipientType: DESTINATION_CHAIN` à 1 et 10 $. Aucun fonds n'a été
engagé. Un devis `dry` prouve qu'une route existe à l'instant T. Il ne prouve pas que l'exécution réussira.

## Ce qu'on apprend

1. **229 actifs sur 39 réseaux, mais seulement une vingtaine de memecoins.** C'est ce que l'étude prévoyait : le burn ne
   portera que sur une petite partie du catalogue. Les autres cartes restent des cartes de collection.
2. **13 memecoins sont cotés de 1 à 100 $**, avec une perte de 0,2 à 1,7 % à l'achat. TRUMP l'est aussi, mais il est dans
   « À décider ».
3. **Le retrait vers la chaîne d'origine coûte un montant fixe, d'environ 0,10 à 0,25 $.** Cela fait 2 à 25 % de perte sur
   une carte à 1 $, et 1 à 3,5 % sur une carte à 10 $. Un retrait vers le solde Intents ou vers NEAR ne coûte rien.
   Conséquence : **une carte brûlable doit valoir au moins 5 à 10 $** si on veut un retrait vers la chaîne d'origine.
   Sinon, on propose d'abord le retrait sur NEAR.
4. **Les devis sont signés** (`signature: ed25519:…`), et le champ `appFees` montre 20 points de base prélevés sans clé
   API. Le risque 4 de `intents-et-garde.md` est en partie levé : le format de la signature existe, mais il reste à le
   vérifier dans un contrat.
5. **La profondeur limite les hautes raretés.** À 1 000 $, BLACKDRAGON, TRUMP et TURBO (version Solana) n'ont plus de
   liquidité, et la perte sur SHITZU, JAMBO et NearKat passe à 4 à 11 %.
6. **0,00 % de perte sur SPX (Ethereum) et CASHCAT : c'est suspect.** Le prix de référence de l'API est peut-être en
   retard. Il faudra comparer les quantités livrées, pas les montants en dollars.
7. Python se fait bloquer par Cloudflare (erreur 1010) avec son en-tête User-Agent par défaut. Le relais devra envoyer
   un en-tête explicite.

## Memecoins brûlables (devis réussis)

Perte = 1 − valeur reçue / valeur envoyée, d'après `amountOutUsd`.

| Carte | Jeton | Version Intents | Perte 1 $ | 10 $ | 100 $ | 1 000 $ | Retrait 1 $ | Retrait 10 $ |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | DOGE | `nep141:doge.omft.near` (natif) | 0,34 % | 0,32 % | 0,35 % | 0,35 % | non testé | non testé |
| 2 | SHIB | Ethereum | 0,42 % | 0,42 % | 0,42 % | 0,42 % | 12,96 % | 2,12 % |
| 3 | PEPE | Ethereum | 0,23 % | 0,26 % | 0,29 % | 0,29 % | 25,19 % | 3,44 % |
| 7 | WIF | Solana | 0,82 % | 0,82 % | 0,82 % | 0,98 % | 23,13 % | 3,51 % |
| 12 | PENGU | Solana | 0,41 % | 0,41 % | 0,43 % | 0,45 % | 1,98 % | 1,09 % |
| 15 | SPX | Ethereum / Solana | 0,00 / 0,55 % | 0,00 / 0,55 % | 0,00 / 0,52 % | 0,00 / 0,53 % | 15,70 / 23,07 % | 2,64 / 3,41 % |
| 21 | BOME | Solana | 0,57 % | 0,57 % | 0,62 % | 0,63 % | 22,87 % | 3,13 % |
| 67 | CASHCAT | Robinhood Chain | 0,00 % | 0,00 % | 0,00 % | 0,03 % | 9,96 % | 1,16 % |
| 190 | TURBO | Ethereum, Solana, NEAR | 0,60 % | 0,60 % | 0,57 % | 0,66 % (eth) | 11,86 % (eth) | 1,80 % (eth) |
| 371 | NearKat | NEAR (aussi Solana) | 0,62 % | 0,72 % | 1,72 % | 10,67 % | sans objet | sans objet |
| 488 | BLACKDRAGON | NEAR | 0,75 % | 0,80 % | 1,24 % | pas de liquidité | sans objet | sans objet |
| 743 | SHITZU | NEAR | 0,61 % | 0,64 % | 1,00 % | 4,47 % | sans objet | sans objet |
| 803 | JAMBO | NEAR (meme-cooking) | 0,34 % | 0,38 % | 0,75 % | 4,35 % | sans objet | sans objet |
| D1 | TRUMP | Solana | 0,62 % | 0,62 % | 0,62 % | pas de liquidité | 2,02 % | 1,12 % |

DOGE existe aussi sur Aptos, avec 0,79 % de perte. Pour un retrait DOGE natif, il faut une adresse en D… : à tester.

## Listés, mais sans liquidité le 11/11

| Carte | Jeton | Chaîne | Statut |
|---|---|---|---|
| 13 | BRETT | Base | « No liquidity available » à tous les montants |
| 56 | MOG | Ethereum | idem |
| 206 | PURGE (Forgive Me Father) | NEAR, meme-cooking | idem |
| 807 | LOUD | Solana | idem, ajouté au catalogue |
| D6 | MELANIA | Solana | idem, dans « À décider » |
| | STJACK | NEAR | idem, jeton inconnu, non ajouté |
| | wNEARKAT, NEARKAT (Solana) | Solana | pas de devis : la version NEAR suffit |

Ces jetons sont à revérifier avant chaque série : la liquidité des solveurs change.

## Listés, mais morts : cartes de collection

ABG, GNEAR et NOEAR sont des memecoins NEAR lancés sur meme-cooking. Leur prix vaut 0, et un devis à 1 $ rend 0 $. Ils
entrent au catalogue (n° 804 à 806) comme cartes de collection, avec le burn à « non ». Ils vont dans le cimetière.

## Écartés : listés, mais pas des memecoins

PONS (launchpad sur Robinhood Chain) et COCA (wallet). Les autres actifs de la liste sont des stablecoins, des jetons
natifs, des versions enveloppées, ou des jetons DeFi et d'infrastructure (AAVE, UNI, LINK, SWEAT, RHEA, etc.).

## Ce qui a changé dans le catalogue

- **Burn.** Les valeurs « oui » et « à vérifier » sont remplacées par le statut réel : « oui (Intents) » (13),
  « Intents sans liquidité » (4), « absent d'Intents (candidat) » (58, les anciens « oui » ou « oui à vérifier »),
  « absent d'Intents » (705) et « non » (6). Les candidats sont les premiers à surveiller si Intents les ajoute.
- **Chaînes et adresses complétées** pour CASHCAT, NearKat, SHITZU et PURGE.
- **Ajouts (5).** JAMBO, brûlable. ABG, GNEAR et NOEAR, morts. LOUD, listé sans liquidité.
- **Retraits (7).** Cinq jetons qui ne sont pas des memecoins (Dentacoin, Private Aviation Finance, OriginTrail BRC-20,
  ZygoSwap, Zora) et deux noms obscènes (Puss, Bitchemical Token).
- **Déplacés dans « À décider » (14).** Les jetons politiques (Trump, Biden, Harris, Poutine, MAGA, America Party,
  Central African Republic Meme…), selon la même règle qu'Official Trump et Melania. Les célébrités et les patrons
  (Elon, CZ, rappeurs) restent au catalogue : leur visuel est déjà dans la liste A de `visuels-droits.md`, à générer sans
  ressemblance.
- **Total : 786 cartes**, plus 77 jetons « À décider ». Rareté : 4 légendaires, 23 épiques, 121 rares, 638 communes.

## Conséquences pour la conception

- **Les 13 brûlables couvrent toutes les raretés.** Légendaire : DOGE, SHIB, PEPE. Épique : WIF, PENGU, SPX, BOME. Rare :
  CASHCAT. Commune : TURBO, NearKat, BLACKDRAGON, SHITZU, JAMBO. La règle « brûlable quelle que soit la rareté » tient
  donc, à condition que la table de tirage favorise ces 13 pièces au sein de chaque rareté.
- **Valeur minimale d'une carte brûlable.** Elle doit dépasser vingt fois le coût fixe du retrait, soit au moins 5 $.
  Avec un booster à environ 10 $ et β = 60 %, cela fait peu de cartes brûlables par booster, mais plus grosses. C'est à
  simuler (voir le plan, phase 2).
- **Plafond par coin.** Les jetons NEAR natifs perdent plus de 4 % dès 1 000 $ : ils sont réservés aux petites valeurs.
- **Démo.** La route NEAR → NEAR (BLACKDRAGON, SHITZU, JAMBO, NearKat) est la moins risquée pour la preuve mainnet : pas
  de pont, et un retrait gratuit.
