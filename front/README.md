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
`dist/`) et `npm run typecheck`.

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

1. **Quantité de jetons.** Sur testnet, l'adossement (`amount`) est une part de la valeur du pack en yoctoNEAR, pas
   une quantité de jetons (`docs/mecaniques-spec.md`). Le front l'estime avec `amount × cours NEAR / cours du coin`.
   Il faudra lire la vraie quantité quand le redeemer achètera les jetons.
2. **Dépôt de stockage.** Le contrat demande le pire cas, 0,016 NEAR par pack (`required_deposit − price`). La
   consigne parle d'environ 0,006 NEAR, et 0,01 NEAR au premier pack. Le front affiche les deux : le montant joint et
   l'estimation de ce qui est réellement consommé.
3. **Prix des packs.** Le contrat n'a qu'une série, à 0,1 NEAR. Les packs à 0,20 $ et 0,50 $ demandent de nouvelles
   séries côté contrat. La boutique affiche déjà toutes les séries ouvertes.
4. **Trending.** En attendant un indexeur, « Trending » classe les coins les plus listés à partir des annonces
   (`get_listings`). Indexeur proposé : un petit service qui suit les reçus du contrat (flux de blocs fastnear, ou
   l'API de nearblocks), garde `card_listed`, `card_sold` et `card_delisted` dans SQLite, et expose
   `/trending?window=24h` (ventes et annonces par `card_id`). Il permettrait aussi d'afficher les dernières ventes.
5. **Pack bloqué.** Le contrat n'accepte `retry_reveal` que sur un pack `pending`. Après `MAX_ATTEMPTS`, le pack
   passe `stuck` et ne peut plus être relancé. Le front propose donc la relance avant ce stade.
6. **MetaMask sur iOS** et **WalletConnect** : il faut un `projectId` WalletConnect (variable d'environnement) pour
   activer les wallets mobiles. Ce n'est pas encore branché.

## Testé

- Build et vérification des types.
- Contre le contrat v2 sur testnet, dans un navigateur : boutique (prix, dépôt, gold rush), rejeu complet de packs
  réels (`#/open?pack=0`, `#/open?pack=7`) jusqu'au récapitulatif, page des taux (taux, hash de table, hash du code),
  marché vide, liste des wallets avec MetaMask en premier, mise en page mobile.
- **Pas encore testé, faute de wallet** : connexion, achat signé, burn, mise en vente et achat sur le marché.
