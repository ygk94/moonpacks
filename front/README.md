# Front Memaster (web)

Démo **testnet seulement**. Cahier des charges : `docs/front/CONSIGNE.md`.

## Lancer en local

Depuis `front/` (Node 20+ et Python 3 requis) :

```sh
npm install && npm run dev
```

Puis ouvrir http://localhost:5173. `npm run dev` prépare d'abord les fichiers publics (`scripts/prepare-assets.mjs`),
puis lance Vite :

- `public/catalog.json` : fiche publique de chaque carte (ticker, nom, chaîne, état), tirée de
  `docs/data/catalogue-v2.json`. Les mythiques sont exclues.
- `public/cards/*.svg` : visuels générés par `art/` en anglais (`--langue en`), « à décider » compris (le contrat
  en a 1 646), plus le dos « ? » commun aux mythiques. Ils ne sont régénérés que si le catalogue ou `art/` change.

Ces fichiers sont ignorés par git. Autres commandes : `npm run build` (vérification des types et build de prod dans
`dist/`), `npm run typecheck` et `npm test` (vitest).

## Indexeur (facultatif)

Dans un second terminal, depuis `front/` :

```sh
npm run indexer
```

Ce petit service (`indexer/`, Node seul, SQLite intégré `node:sqlite`) lit les transactions du contrat avec l'API
de fastnear (`tx.test.fastnear.com` : `/v0/account`, puis `/v0/transactions`, reçus et journaux compris). Il garde
les événements NEP-297 dans `indexer/data/` (ignoré par git) et expose une API en lecture seule sur le port 8787 :
`/status`, `/trending?hours=24`, `/sales`, `/resurrected` et `/events?event=…`. Il ne parcourt pas les blocs :
neardata renvoie vite des 429. Il ne lit une transaction qu'une fois passés 20 blocs, quand le tirage est fini.

En dev, le front l'interroge sur `http://localhost:8787`, ou sur `VITE_INDEXER_URL` si elle est définie. S'il ne
répond pas, « Trending » se rabat sur les annonces du contrat.

Limite : `/v0/account` renvoie la liste en une fois. La pagination n'est pas gérée, et l'indexeur écrit un
avertissement si la liste est tronquée. C'est sans effet à l'échelle de la démo (45 transactions au 11/11).

## Configuration

Les variables `VITE_*` sont décrites dans `.env.example`, valeurs par défaut comprises. Aucune clé n'est nécessaire.
Par défaut, le front vise le contrat **v2** `app2.memaster-demo-j7xg7z.testnet` (voir `docs/testnet.md`), et non
`app.…`, l'ancienne version que cite la consigne. Le RPC est fastnear. Le front refuse de démarrer hors testnet.

## Pile

Vite, React 19, TypeScript, Framer Motion pour l'ouverture, CSS pour les effets de rareté. Wallet :
`@hot-labs/near-connect`, avec MetaMask (connecteur « Ethereum Wallets », comptes `0x…`, NEP-518) en tête de liste.
Pas de routeur ni de bibliothèque d'état : un routeur par hash suffit (`#/shop`, `#/collection`, `#/market`,
`#/rates`, `#/legal`).

| Dossier | Contenu |
|---|---|
| `src/near/` | RPC (vues, statut de transaction), lectures typées du contrat, événements NEP-297, wallet, traduction des erreurs du contrat |
| `src/lib/` | Formats, cours publics (CoinGecko pour NEAR, DexScreener puis CoinGecko pour les coins), catalogue, estimation de la quantité de jetons |
| `src/components/` | Carte (effets par rareté), visuel de pack, en-tête et bandeau, fenêtre modale, détail de carte (burn, mise en vente) |
| `src/pages/` | Boutique, Ouverture, Collection, Marché, Transparence, Mentions légales |

## Écrans et règles de la consigne

- **Ouverture** (`src/pages/Opening.tsx`). L'animation part dès la signature. On lit ensuite `get_pack` toutes les
  500 ms. Les cartes sont révélées une par une dès que le tirage est lu, la brûlable en dernier, avec une
  anticipation, un éclat et un temps de pose de plus en plus longs selon la rareté. Le gold pack a sa propre mise en
  scène : fond or, annonce à la déchirure, suspense sur la dernière carte. Si le pack ne progresse plus pendant
  `retry_delay_blocks`, le bouton « Retry reveal » apparaît. Un pack `stuck` affiche un message. Le rejeu d'une
  ouverture passée se fait depuis Collection, onglet Packs, ou par l'URL `#/open?pack=N`.
- **Vérification d'un tirage** (`src/verify/`) : un bouton « Verify this pack » dans le récapitulatif de
  l'ouverture et dans Collection, onglet Packs. Il reprend la logique de `verifier/` au niveau « sans état » :
  hash de la table recalculé, chaîne des graines jusqu'à `acc`, jet de rareté de chaque emplacement et retombée,
  rareté de la carte, palier de valeur du pack. Le choix exact de la carte dans sa rareté et la décision gold
  demandent tout l'historique, donc le vérificateur en ligne de commande. Testé sur les 31 packs réels de
  `docs/data/testnet-2026-11-11-v2/`.
- **Cartes ressuscitées** : badge « Back from the dead », lu dans la vue `get_resurrected` du contrat.
- **Mythiques** : toujours la carte « ? ». Aucun nom ni fichier de mythique n'est servi (`prepare-assets` refuse un
  fichier `mythique-*`).
- **Pas de pourcentage de rentabilité ni de « valeur garantie »** : on n'affiche que des quantités de jetons et des
  cours publics.
- **Pas de compteur de pitié.** Le gold pack n'est annoncé nulle part avant la déchirure.
- **Pas de fausse urgence** : le seul compte à rebours est celui du gold rush, calculé depuis `rush_until` et le
  temps de bloc. L'achat demande une confirmation et renvoie vers les taux.
- **Bandeau permanent** « Demo · NEAR testnet » avec un lien vers les mentions légales, visible aussi pendant
  l'ouverture et dans les fenêtres.
- **Interface en anglais.** Les messages de panique du contrat, en français, sont traduits dans `src/near/errors.ts`.

## Points ouverts (à voir avec Hugo)

La liste complète des décisions, des tests et du travail restants est dans `docs/front/RESTE-A-FAIRE.md`.

1. **Quantité de jetons.** Sur testnet, l'adossement (`amount`) est une part de la valeur du pack en yoctoNEAR, pas
   une quantité de jetons (`docs/mecaniques-spec.md`). Le front l'estime avec `amount × cours NEAR / cours du coin`.
   Il faudra lire la vraie quantité quand le redeemer achètera les jetons.
2. **Dépôt de stockage.** Le contrat demande le pire cas, 0,016 NEAR par pack (`required_deposit − price`). La
   consigne parle d'environ 0,006 NEAR, et 0,01 NEAR au premier pack. Le front affiche les deux : le montant joint et
   l'estimation de ce qui est réellement consommé.
3. **Prix des packs.** Le contrat n'a qu'une série, à 0,1 NEAR. Les packs à 0,20 $ et 0,50 $ demandent de nouvelles
   séries côté contrat. La boutique affiche déjà toutes les séries ouvertes.
4. **Trending.** Il vient de l'indexeur (ventes et annonces sur 24 h, plus les dernières ventes), et à défaut des
   annonces en cours. Pour un déploiement public, il faudra héberger l'indexeur ; il vise un seul contrat.
5. **Pack bloqué.** Le contrat n'accepte `retry_reveal` que sur un pack `pending`. Après `MAX_ATTEMPTS`, le pack
   passe `stuck` et ne peut plus être relancé. Le front propose donc la relance avant ce stade.
6. **MetaMask sur iOS** et **WalletConnect** : il faut un `projectId` WalletConnect (variable d'environnement) pour
   activer les wallets mobiles. Ce n'est pas encore branché.

## Testé

- `npm test` : 26 tests. Formats, événements, traduction des erreurs, ordre de révélation, vérification d'un
  tirage sur les vrais packs du testnet (et rejet d'une graine ou d'une rareté falsifiée), logique de l'indexeur.
- Build et vérification des types.
- Contre le contrat v2 sur testnet, dans un navigateur : boutique (prix, dépôt, gold rush), rejeu complet de packs
  réels jusqu'au récapitulatif, page des taux (taux, hash de table, hash du code), vérification des packs 0, 12 et
  30 sur les données en direct, marché branché sur l'indexeur, liste des wallets avec MetaMask en premier, mise en
  page mobile.
- Indexeur : il a rattrapé les 45 transactions du contrat, avec autant d'événements que dans le relevé de référence
  (31 `pack_bought`, 31 `pack_revealed`, 62 `reveal_step`).
- **Pas encore testé, faute de wallet** : connexion, achat signé, burn, mise en vente et achat sur le marché. Il
  n'y a pas encore eu de vente ni de résurrection sur `app2`, donc « Trending » et les dernières ventes sont vides.
