# Consigne : front Memaster (web, puis app iOS)

Établie le 11/11/2026, à partir des décisions de Hugo (`docs/consignes-front.md`). Ce fichier est la commande à donner
à la personne ou à l'agent qui construit le front. Il se lit seul.

## 1. Le produit en deux phrases

On achète en NEAR un booster de 5 cartes NFT de memecoins de toutes les chaînes. Certaines cartes sont **brûlables** :
on les brûle et on reçoit les jetons du memecoin, achetés et bloqués à l'ouverture du booster.

Démo **testnet seulement**. Contrat : `app.memaster-demo-j7xg7z.testnet` (redéploiement prévu avec la valeur aléatoire).

## 2. Règles à respecter

1. **Site en anglais seulement.** Les textes de l'interface sont en anglais. Le code et ses commentaires peuvent rester
   en français.
2. **Mythiques invisibles.** Les 3 cartes mythiques s'affichent avec « ? » en nom, en image et en description, toutes
   identiques. Aucun nom de mythique dans le code, les fichiers publics, les visuels de packs ou les exemples.
3. **Aucun logo ni personnage repris d'un coin.** On utilise uniquement les visuels générés par `art/`.
4. **Pas de pourcentage de rentabilité.** À l'ouverture, on affiche la **quantité de jetons**. On n'écrit jamais
   « 140 % », « profitable » ou « guaranteed value ». Le joueur fait ses calculs.
5. **Pas de compteur de pitié.** Rien n'annonce le gold pack. Le contrat garde un compteur, mais le front ne l'affiche
   pas.
6. **Pas de fausse urgence.** Pas de minuteur inventé ni d'achat en un clic sans accès aux taux. Le seul compte à
   rebours est celui du gold rush, qui est réel.
7. **Aucun secret dans le dépôt.** Les clés vont dans des variables d'environnement (`.env*` est ignoré par git).
8. **Bandeau permanent** « Demo · NEAR testnet », avec un lien vers les mentions légales.

## 3. Plateformes et pile technique

- **Web d'abord**, puis une **app iOS**.
- Pile proposée, à confirmer avec Hugo :
  - web : TypeScript, React (Next.js ou Vite) ;
  - animations : Framer Motion et CSS 3D, ou WebGL pour les effets métalliques ;
  - iOS : React Native (Expo), qui partage la logique (lecture du contrat, formats) avec le web.
- **Wallet** : near-connect, avec MetaMask (comptes `0x…`, NEP-518) en premier et les wallets NEAR natifs en secours.
  Point à tester sur iOS : MetaMask mobile (lien profond ou WalletConnect).
- Le code va dans `front/` (web) et `mobile/` (iOS), sur une branche `feat/front` créée depuis `feat/demo`.
  Jamais directement sur `main`.

## 4. Direction visuelle

- **Cartes** : fond sombre, cadre coloré selon la rareté, effet métallique. Les animations sont de plus en plus riches
  avec la rareté.
- **Packs** : visuels travaillés, qui montrent beaucoup de mèmes du catalogue, jamais les mythiques.
- **Ouverture** : fluide. C'est le moment fort du produit, à soigner en premier.

| Rareté | Couleur | Cadre (clair → foncé) | Animation |
|---|---|---|---|
| Common | gris | `#a3a39b` `#6b6d68` `#4a4c49` | aucune |
| Rare | bleu | `#a9d3ff` `#3d7cc9` `#1d3f73` | légère lueur |
| Epic | violet | `#e7b6ff` `#9b3fe0` `#4a137f` | reflet métallique |
| Legendary | or | `#fff6c2` `#e3b230` `#8a5a00` | reflet et particules |
| Mythic | rouge sombre et or | `#ffd75e` `#8f0d18` `#1a0204` | la plus forte, carte « ? » |

Visuels des cartes : `art/` génère un SVG et le JSON NEP-177 de chaque carte, depuis
`docs/data/catalogue-demo.json` :

```sh
cd art && python3 -m memaster_art --catalogue ../docs/data/catalogue-demo.json --out out/demo/
```

Le dos de carte scellé et des exemples sont dans `art/exemples/v2/`.

## 5. Écrans

### 5.1 Connexion

- Bouton « Connect wallet » (near-connect), avec MetaMask en tête de liste.
- Un nouveau compte MetaMask doit signer une transaction de « setup ». Le front l'explique en une phrase.

**Fini quand** on se connecte avec MetaMask et avec un wallet NEAR natif sur testnet, et que le compte s'affiche.

### 5.2 Boutique

- Les packs en vente, avec leur prix **en NEAR et en dollars** (cours NEAR lu par une API publique).
- Prix recommandés, à confirmer par Hugo : pack d'entrée à 0,20 $, pack standard à 0,50 $.
- Avant l'achat, on montre le dépôt de stockage qui s'ajoute au prix : environ 0,006 NEAR, 0,01 NEAR au premier pack
  d'un compte. Il est rendu quand la carte est brûlée.
- Un lien « Drop rates » mène à la page transparence.
- L'avancement collectif vers le gold rush est affiché. Pendant un rush : la fin du rush et le nombre de packs rush
  restants pour ce compte (3 au plus).

**Fini quand** un achat réussit sur testnet avec le bon dépôt, et qu'un dépôt insuffisant affiche une erreur claire.

### 5.3 Ouverture

- `buy_pack` émet `pack_bought`. Le tirage arrive **3 blocs plus tard** (environ 1,8 s) dans l'événement
  `pack_revealed`, ou par `get_pack(pack_id)`.
- L'animation démarre à la signature. Elle ne doit jamais attendre sans rien montrer, et elle révèle les cartes dès que le
  tirage est lu.
- Les 5 cartes se révèlent une par une, avec la couleur et l'animation de leur rareté. La carte brûlable est la
  dernière.
- On affiche la quantité de jetons de la carte brûlable.
- **Gold pack** (environ 1 sur 50 000) : une mise en scène à part, sans commune, avec du suspense sur la dernière carte.
- Si le pack reste bloqué (événement `pack_stuck`), le front propose `retry_reveal`.

**Fini quand** l'ouverture est fluide sur un ordinateur portable et un iPhone récent, et qu'un pack bloqué se débloque
depuis l'interface.

### 5.4 Collection

- Mes cartes (`nft_tokens_for_owner`), filtrables par rareté et par « burnable ».
- Détail d'une carte : visuel, rareté, chaîne, **valeur du coin** (cours lu hors chaîne : GeckoTerminal ou DexScreener,
  voir `docs/oracle-prix.md`) et quantité de jetons bloqués (`get_backing`). Jamais de « valeur garantie ».
- Pas de « cimetière » séparé : les coins morts sont des cartes comme les autres.
- Une carte d'un coin mort qui devient brûlable (événement `card_resurrected`) est signalée.

### 5.5 Burn

- Bouton « Burn » dans le détail d'une carte brûlable seulement.
- On confirme avant d'agir : le burn détruit la carte.
- Pas de choix de chaîne. Le joueur reçoit directement les jetons.
- Le burn se fait en deux temps : `redeem_started`, puis `card_redeemed` ou `redeem_failed`, et dans ce cas la carte est
  restaurée. Le front suit l'état et le dit.

### 5.6 Marché

- Notre marché, déjà dans le contrat : `list(token_id, price)`, `delist(token_id)`, `buy(token_id, expected_price)`,
  `get_listings`. Événements `card_listed`, `card_delisted`, `card_sold`.
- Une section **« Trending »** : les cartes les plus vendues ou les plus listées récemment. Il faut un petit indexeur des
  événements, à proposer.

### 5.7 Transparence

- Les taux de drop de la série (`get_rates`, paginé) et le hash de la table (`get_series_table_hash`).
- Le hash du code du contrat, avec des liens vers nearblocks (testnet) pour le vérifier soi-même.
- Optionnel : la vérification d'un tirage, en reprenant la logique de `verifier/` (Python) ou en lui renvoyant.

## 6. Lecture du contrat

Tous les appels de lecture sont des `view` gratuites. Les signatures exactes sont dans `contract/src/views.rs`,
`pack.rs`, `market.rs` et `redeem.rs`, et l'ABI dans `contract/target/near/memaster_abi.json` après un build.

| Besoin | Méthode ou événement |
|---|---|
| Séries et prix | `get_series_count`, `get_series_header(series_id)` |
| Taux | `get_rates(series_id, from_index, limit)` |
| Achat | `buy_pack(series_id)`, payable : prix + stockage |
| Résultat d'un pack | événement `pack_revealed`, `get_pack(pack_id)`, `get_packs_for_owner` |
| Cartes | `nft_tokens_for_owner`, `get_card(token_id)`, `get_backing(token_id)` |
| Gold rush | `get_rush_state(series_id, at_height, account_id)` |
| Burn | `redeem(token_id)` et les événements `redeem_*` / `card_redeemed` |
| Marché | `list`, `delist`, `buy`, `get_listing(s)` |
| Transparence | `get_series_table_hash`, `get_config` |

Les événements suivent NEP-297, avec `standard: "memaster"` et `version: "1.0.0"`.

RPC testnet : utiliser **fastnear** (`https://rpc.testnet.fastnear.com`). L'ancien `rpc.testnet.near.org` renvoie
des erreurs 429. Plusieurs événements d'un même bloc se trient par (hauteur, `pack_id`).

## 7. Hors périmètre pour l'instant

- Mention « simulation » sur les parties simulées : à voir plus tard avec Hugo.
- Mainnet : jamais sans avis juridique.
- Paiement par carte bancaire, comptes sans wallet.

## 8. À trancher avec Hugo avant ou pendant le travail

1. Le nom du projet, qui conditionne le logo, les visuels de packs et le domaine.
2. La pile technique (section 3).
3. Les prix des packs.
4. La source du cours des coins et l'indexeur pour « Trending ».
5. MetaMask sur iOS.

## 9. Livraison

- Le web se lance en local avec une seule commande, documentée dans `front/README.md`.
- Une démo de bout en bout sur testnet : connexion, achat, ouverture, collection, burn, mise en vente et achat sur le
  marché, page transparence.
- Pas de push ni de déploiement public sans l'accord de Hugo.
