# Front Memaster (web)

Démo **testnet seulement**. Cahier des charges : `docs/front/CONSIGNE.md`.

## Lancer en local

Depuis `front/` (Node 20+ et Python 3 requis) :

```sh
npm install && npm run dev
```

Puis ouvrir http://127.0.0.1:5173. Vite n'écoute que sur la machine (`127.0.0.1`) ; pour ouvrir le front au réseau
local (un téléphone, par exemple) : `DEV_HOST=0.0.0.0 npm run dev`. `npm run dev` prépare d'abord les fichiers publics (`scripts/prepare-assets.mjs`),
puis lance Vite :

- `public/catalog.json` : fiche publique de chaque carte (ticker, nom, chaîne, état), tirée de
  `docs/data/catalogue-v2.json`. Les mythiques sont exclues.
- `public/cards/*.svg` : visuels générés par `art/` en anglais (`--langue en`), « à décider » compris (le contrat
  en a 1 646), plus le dos « ? » commun aux mythiques. Ils ne sont régénérés que si le catalogue ou `art/` change.

Ces fichiers sont ignorés par git. Autres commandes : `npm run build` (vérification des types et build de prod dans
`dist/`, suivi du contrôle anti-fuite des mythiques), `npm run typecheck`, `npm test` (vitest, puis le même
contrôle), `npm run check:mythics` et `npm run smoke` (voir « Testé »).

## Indexeur (facultatif)

Dans un second terminal, depuis `front/` :

```sh
npm run indexer
```

Ce petit service (`indexer/`, Node seul, SQLite intégré `node:sqlite`) lit les transactions du contrat avec l'API
de fastnear (`tx.test.fastnear.com` : `/v0/account`, puis `/v0/transactions`, reçus et journaux compris). Il garde
les événements NEP-297 dans `indexer/data/` (ignoré par git) et expose une API en lecture seule sur
`127.0.0.1:8787` (`INDEXER_HOST=0.0.0.0` pour l'ouvrir au réseau local, `INDEXER_PORT` pour le port) :
`/status`, `/trending?hours=24`, `/sales`, `/resurrected` et `/events?event=…`. Il ne parcourt pas les blocs :
neardata renvoie vite des 429. Il ne lit une transaction qu'une fois passés 20 blocs, quand le tirage est fini.

En dev, le front l'interroge sur `http://127.0.0.1:8787`, ou sur `VITE_INDEXER_URL` si elle est définie. S'il ne
répond pas, « Trending » se rabat sur les annonces du contrat. Les événements du contrat v3 `pack_refunded` et `revenue_withdrawn` sont gardés
comme les autres (lisibles par `/events?event=…`), sans être affichés dans le front.

Pagination : `/v0/account` est lu en ordre croissant, par pages de 100 (`resume_token`). Le curseur n'avance
qu'après une page pleine et entièrement lue, et le dédoublonnage par hash couvre la relecture de la dernière page.
`/history?series_id=0` renvoie les événements utiles au rejeu complet d'une série (achats, tirages, burns,
résurrections), dans l'ordre d'exécution.

## Configuration

Les variables `VITE_*` sont décrites dans `.env.example`, valeurs par défaut comprises. Aucune clé n'est nécessaire.
Par défaut, le front (et l'indexeur) visent le contrat **v3** `app3.memaster-demo-j7xg7z.testnet`, avec deux
séries ouvertes (entrée et standard), et non `app2.…` (v2, `docs/testnet.md`) ni `app.…`, l'ancienne version que
cite la consigne. `VITE_CONTRACT_ID=app2.memaster-demo-j7xg7z.testnet npm run dev` revient à la v2 : les erreurs
sans code, le pack `stuck` sans remboursement et le stockage non rendu y sont gérés. Le RPC est fastnear. Le front
refuse de démarrer hors testnet.

## Pile

Vite, React 19, TypeScript, Framer Motion pour l'ouverture, CSS pour les effets de rareté. Wallet :
`@hot-labs/near-connect`, avec MetaMask (connecteur « Ethereum Wallets », comptes `0x…`, NEP-518) en tête de liste.
Pas de routeur ni de bibliothèque d'état : un routeur par hash suffit (`#/shop`, `#/collection`, `#/market`,
`#/rates`, `#/legal`).

| Dossier | Contenu |
|---|---|
| `src/near/` | RPC (vues, statut de transaction), lectures typées du contrat, événements NEP-297, wallet, traduction des erreurs du contrat |
| `src/lib/` | Formats, cours publics (CoinGecko pour NEAR, DexScreener puis CoinGecko pour les coins ; cache de 5 min en mémoire et dans `localStorage`, ids CoinGecko regroupés par appel, recul après un 429 avec la dernière valeur connue), catalogue, estimation de la quantité de jetons, logique d'un pack (relance, remboursement, stockage rendu), répartition d'un achat sur le marché |
| `src/components/` | Carte (effets par rareté), visuel de pack, en-tête et bandeau, fenêtre modale, détail de carte (burn, mise en vente) |
| `src/pages/` | Boutique, Ouverture, Collection, Marché, Transparence, Mentions légales |

## Écrans et règles de la consigne

- **Ouverture** (`src/pages/Opening.tsx`). L'animation part dès la signature. On lit ensuite `get_pack` toutes les
  500 ms. Les cartes sont révélées une par une dès que le tirage est lu, la brûlable en dernier, avec une
  anticipation, un éclat et un temps de pose de plus en plus longs selon la rareté. Le gold pack a sa propre mise en
  scène : fond or, annonce à la déchirure, suspense sur la dernière carte. Si le pack ne progresse plus pendant
  `retry_delay_blocks`, le bouton « Retry reveal » apparaît, pour l'acheteur seulement (v3 : `retry_reveal` lui est
  réservé ; les autres comptes voient que seul l'acheteur peut relancer). Un pack `stuck` propose « Refund »
  (`refund_stuck_pack`, contrat v3 : prix et stockage non utilisé rendus à l'acheteur, quel que soit le compte qui
  le demande), puis affiche le statut `refunded` et le montant rendu. Sur `app2`, un pack `stuck` affiche un message
  de contact. Le rejeu d'une ouverture passée se fait depuis Collection, onglet Packs, ou par l'URL `#/open?pack=N`.
- **Vérification d'un tirage** (`src/verify/`) : un bouton « Verify this pack » dans le récapitulatif de
  l'ouverture et dans Collection, onglet Packs. Deux niveaux, portés de `verifier/` :
  - **sans état** (`verify.ts`) : hash de la table recalculé, chaîne des graines jusqu'à `acc`, jet de rareté de
    chaque emplacement et retombée, rareté de la carte, palier de valeur ;
  - **rejeu complet** (`replay.ts`, avec l'historique de l'indexeur) : toute la série est rejouée depuis son
    ouverture (compteurs, burns, résurrections, gold rush), puis chaque carte est recalculée exactement, avec la
    décision gold pack et la répartition de la valeur. Les libellés ne montrent jamais le compteur de pitié.
  Testé sur les 31 packs réels de `docs/data/testnet-2026-11-11-v2/` (cartes identiques à l'index près), et en
  direct sur les packs 0, 12 et 30. Une graine, une carte ou un achat manquant falsifié est détecté.
- **Cartes ressuscitées** : badge « Back from the dead », lu dans la vue `get_resurrected` du contrat.
- **Mythiques** : toujours la carte « ? ». Aucun nom ni fichier de mythique n'est servi. `scripts/check-mythics.mjs`
  le contrôle après chaque build et dans `npm test` : pas de fiche ni de fichier mythique publics et, si le fichier
  secret `docs/data/secrets/mythiques.json` est présent, aucun vrai nom, ticker, id ou adresse de mythique dans
  `src/`, `public/`, `dist/` et `indexer/`. Le terme trouvé n'est jamais affiché dans le journal.
- **Performance** : les pages secondaires sont chargées à la demande et l'écran d'ouverture est préchargé ; les
  visuels des 5 cartes sont chargés pendant le tirage, avant la déchirure (attente plafonnée à 1,5 s).
- **Pas de pourcentage de rentabilité ni de « valeur garantie »** : on n'affiche que des quantités de jetons et des
  cours publics.
- **Pas de compteur de pitié.** Le gold pack n'est annoncé nulle part avant la déchirure.
- **Pas de fausse urgence** : le seul compte à rebours est celui du gold rush, calculé depuis `rush_until` et le
  temps de bloc. L'achat d'un pack demande une confirmation et renvoie vers les taux. L'achat d'une carte sur le
  marché aussi : « Buy » ouvre un récapitulatif avec le prix exact en NEAR, les redevances prises sur ce prix
  (`nft_payout`, NEP-199) et la part du vendeur, puis « Confirm and buy » signe.
- **Bandeau permanent** « Demo · NEAR testnet » avec un lien vers les mentions légales, visible aussi pendant
  l'ouverture et dans les fenêtres.
- **Interface en anglais.** Les paniques du contrat sont traduites dans `src/near/errors.ts` par leur code stable
  `E_…` (contrat v3, liste dans `contract/ERRORS.md`, textes anglais repris de ce fichier), avec repli sur l'ancien
  texte français pour `app2`. `errors.test.ts` échoue si un code d'`ERRORS.md` n'est pas traduit, ou l'inverse.

## Points ouverts (à voir avec Hugo)

La liste complète des décisions, des tests et du travail restants est dans `docs/front/RESTE-A-FAIRE.md`.

1. **Quantité de jetons.** Sur testnet, l'adossement (`amount`) est une part de la valeur du pack en yoctoNEAR, pas
   une quantité de jetons (`docs/mecaniques-spec.md`). Le front l'estime avec `amount × cours NEAR / cours du coin`.
   Il faudra lire la vraie quantité quand le redeemer achètera les jetons.
2. **Dépôt de stockage.** Le contrat demande le pire cas, 0,016 NEAR par pack (`required_deposit − price`). La
   consigne parle d'environ 0,006 NEAR, et 0,01 NEAR au premier pack. Le front affiche le montant joint et
   l'estimation de ce qui est réellement consommé. Contrat v3 (reconnu à sa vue `get_treasury`) : la boutique précise
   que l'excédent est rendu à l'ouverture ; le récapitulatif de l'ouverture affiche le montant rendu
   (`pack_revealed.storage.refund`, sinon `get_pack` : prépayé − `storage_used`), et le burn le stockage libéré
   rendu (`card_redeemed.storage_refund`). Sur `app2`, rien de cela n'est promis.
3. **Prix des packs.** Le contrat n'a qu'une série, à 0,1 NEAR. Les packs à 0,20 $ et 0,50 $ demandent de nouvelles
   séries côté contrat. La boutique affiche déjà toutes les séries ouvertes.
4. **Trending.** Il vient de l'indexeur (ventes et annonces sur 24 h, plus les dernières ventes), et à défaut des
   annonces en cours. Pour un déploiement public, il faudra héberger l'indexeur ; il vise un seul contrat.
5. **Pack bloqué.** Le contrat n'accepte `retry_reveal` que sur un pack `pending`, et en v3 que de l'acheteur. Après
   `MAX_ATTEMPTS`, le pack passe `stuck` : en v3, « Refund » appelle `refund_stuck_pack` (le pack passe `refunded`).
   Le rejeu depuis Collection, onglet Packs, y mène aussi.
6. **MetaMask sur iOS** et **WalletConnect** : WalletConnect est branché mais inactif tant que
   `VITE_WALLETCONNECT_PROJECT_ID` est vide (`projectId` gratuit sur cloud.reown.com). Son client n'est chargé
   que s'il est actif. Non testé sur un téléphone.

## Testé

- `npm test` : 110 tests. Formats et montants (BigInt), événements, traduction par code de chaque erreur de
  `contract/ERRORS.md` (et repli français pour `app2`), pack `stuck` remboursable et relance réservée à l'acheteur,
  stockage rendu (ouverture, burn, texte de la boutique), confirmation d'achat sur le marché, dépôt d'annonce lu
  dans `get_config`, cache et recul des cours publics, file du RPC, cache des cartes par série, écoute locale de
  Vite et de l'indexeur, ordre de révélation, rendu « ? » des mythiques, suivi du burn, vérification
  sans état et rejeu complet sur les vrais packs du testnet (falsifications rejetées), vecteurs de
  `verifier/tests/vectors/` (draw.rs et contrat en sandbox : tirages, plafonds, gold pack, burns, résurrections,
  valeur, gold rush), logique de l'indexeur (événements v3 compris), contrôle anti-fuite des mythiques.
- `npm run smoke` (avec `npm run dev`, et `npm run indexer` pour la vérification complète) : parcours en lecture
  seule dans Chromium sans tête (Playwright, `npx playwright install chromium-headless-shell` une fois), captures
  dans `smoke-captures/`. Aucun wallet ni transaction. Les échecs CORS du RPC fastnear quand il limite le débit
  sont comptés à part, comme ceux des cours publics ; le contenu des pages reste vérifié. Passé le 12/11 contre
  `app3` (boutique à deux séries, packs 0, 12 et 30 entièrement vérifiés, stockage rendu affiché).
- Build et vérification des types.
- Contre le contrat v2 sur testnet, dans un navigateur : boutique (prix, dépôt, gold rush), rejeu complet de packs
  réels jusqu'au récapitulatif, page des taux (taux, hash de table, hash du code), vérification des packs 0, 12 et
  30 sur les données en direct, marché branché sur l'indexeur, liste des wallets avec MetaMask en premier, mise en
  page mobile.
- Indexeur : il a rattrapé les 45 transactions du contrat, avec autant d'événements que dans le relevé de référence
  (31 `pack_bought`, 31 `pack_revealed`, 62 `reveal_step`).
- **Pas encore testé, faute de wallet** : connexion, achat signé, burn, mise en vente et achat sur le marché. Il
  n'y a pas encore eu de vente ni de résurrection sur `app2`, donc « Trending » et les dernières ventes sont vides.
