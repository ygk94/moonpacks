# Front Moonpacks : ce qui reste à faire (pour Hugo)

État au 12/11/2026, branche `fix/front-revue` (depuis `feat/front`, avec `feat/demo` fusionnée). La branche est sur
GitHub jusqu'à `956e125` ; les commits suivants (depuis `6540de8`, liste plus bas) ne sont pas encore poussés. Le front vise **`app3`** (contrat v3, deux
séries).

## À faire maintenant : déployer le contrat v4 (14/11)

Tout est prêt (tables, script, site) ; détail dans `docs/front/packs-thematiques.md`. Depuis `contract/`, avec les clés
de `memaster-demo-j7xg7z.testnet` :

```bash
./scripts/deploy_v4.sh
gh variable set CONTRACT_ID --body app4.memaster-demo-j7xg7z.testnet
gh workflow run ci.yml --ref main -f deploy=true
```

Puis noter les comptes et les hashs dans `docs/testnet.md` (section « Version 4 »).

## Ce qui est fait

Le web demandé par `docs/front/CONSIGNE.md` est écrit dans `front/`. Le détail est dans `front/README.md`.

- Écrans : boutique, ouverture des boosters, collection, détail d'une carte avec burn et mise en vente, marché avec
  « Trending », transparence (taux, hash de la table, hash du code, vérification d'un pack), mentions légales.
- Règles de la consigne : interface en anglais, mythiques en « ? », aucun pourcentage de rentabilité, pas de
  compteur de pitié, pas de fausse urgence, bandeau « Demo · NEAR testnet » permanent.
- Visuels : ceux de `art/`, avec une nouvelle option `--langue en` (les SVG étaient en français).
- Indexeur facultatif (`front/indexer/`), pour « Trending » et les dernières ventes.
- 126 tests (`npm test`), un build propre, un contrôle automatique « aucun nom de mythique » et un parcours de fumée
  en lecture seule (`npm run smoke`).
- Parcours de bout en bout avec de vraies transactions testnet (`npm run e2e`), grâce à un wallet de test à clé
  locale, chargé seulement en dev (section 2).

Lancement :

```sh
cd front && npm install && npm run dev      # http://127.0.0.1:5173
cd front && npm run indexer                 # facultatif, second terminal
```

## Décisions d'Enzo du 13/11

- Nom : **Moonpacks**.
- **Site web seulement**, iOS mis de côté.
- Hébergement sur **Vercel**, donc pas de WalletConnect.
- Les **101 jetons « À décider » sont retirés définitivement** : `prepare-assets` ne prend plus que la
  section `catalogue`. Les séries de `app3` ne les contenaient déjà pas.

## 1. Décisions à prendre

| # | Sujet | Situation | Ce qu'il faut trancher |
|---|---|---|---|
| 1 | **Nom du projet** | **Moonpacks** (Enzo, 13/11). Le site l'affiche ; le contrat garde « Memaster » on-chain, remplacé à l'affichage | Vérifier le domaine et les homonymes crypto |
| 2 | **Pile iOS** | **Mise de côté** (Enzo, 13/11) : site web seulement | Rien pour l'instant |
| 3 | **Prix des packs** | Contrat v3 (`app3`) : deux séries ouvertes, « Memaster Entry » (0,0552 NEAR) et « Memaster Standard » (0,1381 NEAR), environ 0,20 $ et 0,50 $ au cours du déploiement. La boutique, la page des taux (sélecteur de série, `#/rates?series=1`) et le gold rush (un panneau par série) les montrent toutes les deux | Le prix est fixé en NEAR : le prix en dollars bougera |
| 4 | **Quantité de jetons d'une carte brûlable** | L'adossement (`amount`) est une **valeur en yoctoNEAR**, pas une quantité de jetons (`docs/mecaniques-spec.md`). Le front estime `amount × cours NEAR / cours du coin`. Pour un coin presque sans valeur, ça donne des nombres énormes (« 25,800T SHIBDOGE ») | Comment le redeemer achète les jetons, et où le front lit la vraie quantité |
| 5 | **Dépôt de stockage** | Le contrat exige **0,01605 NEAR** par pack en plus du prix (1 605 o prépayés, pire cas) : 0,07125 NEAR joints en série 0, 0,15415 en série 1. **Contrat v3 : l'excédent est rendu à l'ouverture** (0,00567 NEAR au premier pack d'un compte, 0,00999 ensuite : mesuré sur les packs 41 à 45 de la nuit) ; la boutique le dit et le récapitulatif affiche le montant rendu | Rien, sauf si le dépôt joint doit baisser |
| 6 | **Dépôt rendu au burn ?** | **Contrat v3 : oui, en partie.** Le burn rend le stockage libéré (`card_redeemed.storage_refund`, environ 16 o pour un burn ordinaire) ; l'emplacement du pack reste écrit (`docs/mecaniques-spec.md`, 12.2). Le front affiche le montant rendu après le burn, sans promesse avant | Corriger la consigne (« rendu au burn » → « l'excédent est rendu à l'ouverture, le stockage libéré au burn ») |
| 7 | **Source des cours** | NEAR/USD : CoinGecko. Cours d'un coin : DexScreener par adresse, sinon CoinGecko par identifiant. Appels directs depuis le navigateur, sans clé, avec un cache de 5 min (mémoire et `localStorage`), des ids regroupés par appel et un recul après un 429 (dernière valeur connue affichée) | Valider, ou passer par un service maison si la démo publique attire du monde |
| 8 | **WalletConnect** | **Pas nécessaire** (Enzo, 13/11) : démo sur ordinateur, MetaMask en extension ou wallet NEAR natif. Le code reste inactif sans `projectId` | Rien |
| 9 | **Mention « simulation »** | **Faite** (13/11) : bandeau sur toutes les pages, mentions au burn, dans le détail d'une carte, dans le récapitulatif et dans les mentions légales | Rien |
| 10 | **Mentions légales** | **Faites** (13/11) : éditeur (projet étudiant), hébergeur Vercel, simulation, données personnelles | Une adresse de contact, si vous voulez (`VITE_CONTACT_EMAIL`) |
| 11 | **Contrat visé** | **`app3.…` est la cible** du front, de l'indexeur et des parcours e2e (v3, deux séries). `VITE_CONTRACT_ID` (et `INDEXER_CONTRACT_ID`) changent de contrat ; `app2` reste pris en charge | Rien |
| 12 | **Push, PR, déploiement public** | Branches poussées. **En ligne sur Vercel** depuis le 13/11 : https://moonpacks-ochre.vercel.app (build statique, `npm run deploy`) | Fusions vers `main` à faire ensemble |

## 2. Tests qui demandent un wallet

Faits le 12/11 vers 1 h 30 par `npm run e2e` (`front/README.md`, « Wallet de test et parcours e2e »), sur `app3`, à
travers l'interface, avec de vraies transactions signées par `buyer1` et `buyer2`. Le wallet de test signe avec la clé
de `~/.near-credentials`, injectée dans la page au moment du test : il remplace MetaMask, pas l'intégration de
near-connect avec un vrai wallet. Coût d'un passage complet : environ 0,23 NEAR sur `buyer1` (série 0 : 0,07125 NEAR
joints, 0,00999 rendus ; série 1 : 0,15415 joints, 0,00999 rendus ; plus le gaz).

- [x] **Achat d'un pack, série 0 puis série 1** : dépôt joint = prix + 0,01605 NEAR (relu dans la transaction),
  ouverture jusqu'au récapitulatif, « Unused storage deposit returned … 0.00999 NEAR », « Verify this pack » à
  « ✓ Draw fully verified » (rejeu complet avec l'indexeur). Pack 44, série 0 :
  [5tfnncrs…](https://testnet.nearblocks.io/txns/5tfnncrskKmkRqNaJ8XK2UdZ2Rq9chYTRsPZisywXvV4) ; pack 45, série 1 :
  [F4Tgqfj…](https://testnet.nearblocks.io/txns/F4TgqfjJLehd4tPNbu3B8G5jgnBVA8mQKyVqj3hhrEAf).
- [x] **Solde insuffisant** : compte implicite neuf crédité de 0,01 NEAR par `buyer1`
  ([4zNq9yrY…](https://testnet.nearblocks.io/txns/4zNq9yrYSsBkuftRNv3RsGw4x4bJSbpfs1DU82p6tAZe)). L'achat est refusé
  par le RPC (`NotEnoughBalance`) et l'écran affiche « The pack was not bought · Your wallet balance is too low for
  this transaction. ». Le compte est ensuite supprimé au profit de `buyer1`
  ([ByLbi2tj…](https://testnet.nearblocks.io/txns/ByLbi2tjQfCVRgWHbVvMDE7Leyu3ZVHXwjrNRacvNJgb)).
- [x] **Burn d'une carte brûlable** depuis le détail (carte 444, NEARKAT) : `redeem_started` puis `card_redeemed`,
  « The freed storage deposit (0.00016 NEAR) was returned too. »
  ([BWfUeHfF…](https://testnet.nearblocks.io/txns/BWfUeHfFQZWsWypWT76MNS9up66QvcW6UrchZEcCwXXS)). Le cas
  `redeem_failed` (carte restaurée) n'est pas provoqué : le redeemer factice ne l'a pas fait échouer.
- [x] **Marché** (carte 440) : mise en vente à 0,00123 NEAR par `buyer1`
  ([AESdopej…](https://testnet.nearblocks.io/txns/AESdopejmcNihfhP26BaStXNBcu9YaweyH9aqfrN8biL)), retrait
  ([5nPFnXtt…](https://testnet.nearblocks.io/txns/5nPFnXttjWYMqJYZ81Piyqz9JrB2GoXf1kB9PudKPHNZ)), nouvelle mise en
  vente ([tHHXVUz6…](https://testnet.nearblocks.io/txns/tHHXVUz6pznecSAZn32FTVHMZqxjDBLCRxEuP2hNeSj)), achat par
  `buyer2` via l'écran de confirmation, « You pay exactly 0.00123 NEAR »
  ([3QPHHa15…](https://testnet.nearblocks.io/txns/3QPHHa15aWfhLiAxkozWzFhL8ssueLtMUuQouiXfPCvn)). Puis « Trending »
  et « Recent sales » montrent la vente, lue par l'indexeur lancé sur un port à part (8797).
- [ ] **Connexion avec un vrai MetaMask** (compte `0x…`, transaction de setup NEP-518) et avec un wallet NEAR natif
  (Meteor, Intear…). Il faut un compte `0x…` alimenté en NEAR testnet.
- [ ] **Ouverture fluide sur un vrai iPhone récent** (vérifiée seulement à la taille d'un téléphone dans un navigateur).
- [ ] **Pack réellement bloqué** (`stuck`) débloqué depuis l'interface : « Retry reveal », puis « Refund ». La logique
  est testée (`npm test`), mais aucun pack n'a jamais bloqué sur testnet : aucun booster acheté sur `app`, `app2` ou `app3` n'a eu besoin de
  `retry_reveal`, et le provoquer demande de faire échouer un reçu du tirage.

Le parcours a trouvé deux défauts, corrigés cette nuit : la fenêtre « Connect wallet » ouverte depuis l'en-tête y
restait coincée, liste des wallets hors de l'écran (le `backdrop-filter` de l'en-tête servait de repère aux éléments
fixes) ; et le détail d'une carte remise en vente pouvait garder l'ancien état (nœud RPC en retard).

Captures : 16 images et `report.json` (tous les hashs), hors dépôt, sur la machine de Hugo. Les passages de mise au point
ont aussi acheté les packs 41 à 43, brûlé la carte 434 et vendu la carte 430 à `buyer2`.

## 3. Travail restant

Déjà fait depuis la première version de ce document : vérification complète dans le navigateur (carte exacte et
décision gold, via l'historique de l'indexeur), pagination de l'indexeur, WalletConnect par variable
d'environnement, chargement plus rapide de l'ouverture, contrôle anti-fuite des mythiques.

`npm run check:mythics` a été lancé cette nuit avec le fichier secret `docs/data/secrets/mythiques.json` présent : il
passe. Sans ce fichier, le contrôle se limite à la structure.


| Sujet | Détail |
|---|---|
| **Images des NFT dans les wallets** | Sur `app3`, `media` = `ipfs://bafybeif…5viuia/<carte>.svg`, CID **calculé mais jamais envoyé** : images cassées. Envoyer le CAR (`contract/scripts/ipfs_media.py upload`) suffit, sans redéploiement |
| **Hébergement de l'indexeur** | Il tourne en local (SQLite). Pour une démo publique, il faut l'héberger quelque part et définir `VITE_INDEXER_URL` |
| **Pack `stuck`** | Contrat v3 : « Refund » appelle `refund_stuck_pack` (prix et stockage non utilisé rendus à l'acheteur), puis le pack s'affiche `refunded`. `retry_reveal` n'est proposé qu'à l'acheteur. Sur `app2`, message de contact |
| **Messages d'erreur du contrat** | Contrat v3 : traduits par code `E_…` (`front/src/near/errors.ts`, textes anglais de `contract/ERRORS.md`) ; un test échoue si un code n'est pas traduit. Repli sur l'ancien texte français pour `app2` |

## Fait pendant la nuit du 11 au 12/11

Enzo, voici ce qui a changé dans `front/` sur `fix/front-revue` depuis `feat/front`. Tout passe : `npm test`
(126 tests), `npm run build`, `npm run check:mythics` (avec le fichier secret), `npm run smoke` et `npm run e2e`
contre `app3`.

- `a325a9b` Contrôle anti-fuite des mythiques utilisable avec le vrai fichier secret
- `7813257` Le vérificateur TypeScript rejoue les vecteurs de `verifier/`
- `d499e0b` Erreurs du contrat traduites, hash de transaction du wallet lu sans planter
- `5be2c1c` Montants à payer affichés exactement, saisie de prix stricte
- `f9ac305` Tests du rendu « ? » des mythiques
- `dfdd7ec` Suivi du burn jusqu'à son issue
- `d5dc829` Parcours de fumée en lecture seule (`npm run smoke`)
- `e22130b` README à jour (tests, `npm run smoke`)
- `8363885` Erreurs du contrat traduites par code `E_…` (v3), repli français pour `app2`
- `5a66afb` Pack `stuck` remboursable (`refund_stuck_pack`), relance réservée à l'acheteur
- `451f22f` Stockage rendu (v3) à l'ouverture et au burn
- `0e6ccf4` Indexeur et Vite : écoute sur 127.0.0.1 par défaut, événements v3 acceptés
- `068f857` Confirmation avant l'achat d'une carte sur le marché
- `7bf5b7f` Tests marché : contrôle du bouton « Buy » dans un test `.ts`
- `131d4a0` Cours publics en cache (5 min, mémoire et `localStorage`), regroupés, recul sur 429
- `bd33534` Dépôt d'annonce lu dans `get_config` au lieu de « 0.005 NEAR » en dur
- `8720487` Définitions de cartes en cache par série (v3 : deux séries)
- `f5145f6` RPC plus sobre sous limite de débit, smoke qui exerce la confirmation du marché
- `fa8eea6` Front et indexeur : contrat v3 `app3` par défaut
- `956e125` README : tests et smoke à jour (v3)
- `6540de8` Fenêtres modales rendues dans `<body>` (fenêtre de connexion coincée dans l'en-tête)
- `99ed702` Détail de carte relu jusqu'au nouvel état après mise en vente ou retrait
- `aa1c756` Wallet de test à clé locale pour les parcours e2e (dev seulement, absent du build de production)
- `c2ec3b9` Parcours e2e sur testnet (`npm run e2e`)
- `b291df1` Taux et gold rush pour toutes les séries
- le commit de documentation qui met ce fichier et `front/README.md` à jour

La branche contient aussi les fusions de `feat/demo` (contrat v3, séries de démo).

## 4. Où regarder

- `front/README.md` : lancement, configuration, structure, règles appliquées, ce qui est testé.
- `front/src/pages/Opening.tsx` : l'ouverture des boosters.
- `front/src/verify/verify.ts` : la vérification d'un tirage (même logique que `verifier/`).
- `front/indexer/indexer.mjs` : l'indexeur et son API.
- `front/scripts/e2e.mjs` : les parcours de bout en bout ; `front/src/near/testKeyWallet.ts` : le wallet de test.
