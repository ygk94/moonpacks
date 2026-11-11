# Consignes front et parcours joueur

Établi le 11/11/2026. Ce fichier rassemble ce qui concerne le front et le côté joueur : les demandes de Hugo, les
propositions issues de la recherche et les contraintes du contrat. Il sert de base à la discussion avant de coder le
front. Tant qu'une ligne n'est pas validée, elle reste une proposition.

Légende des sources :

- **[Hugo]** : demande ou décision de Hugo, citée ou résumée ;
- **[Plan]** : proposition de `plan.md` ou des recherches (`marche-droits-economie.md`, `intents-et-garde.md`) ;
- **[Contrat]** : contrainte technique mesurée ou codée (`contract/`, `testnet.md`, `faisabilite.md`).

## 1. Décisions déjà prises

| Sujet | Consigne | Source |
|---|---|---|
| Calendrier | « On touche pas au front pour le moment » (11/11). Le front démarre après la discussion de ce fichier | [Hugo] |
| Wallet | MetaMask, avec un test ensemble dès qu'il y aura un front | [Hugo] |
| Démo | NEAR Intents | [Hugo] |
| Mythiques | Les 3 mythiques n'apparaissent pas : « dans le catalogue ils auront un ? », « on communique même pas dessus » | [Hugo] |
| Catalogue de démo | Pas de cartes à drapeau ni de politiciens. On les garde seulement s'il manque de jetons brûlables | [Hugo] |
| Valeur d'un pack | Aléatoire, de 20 % à 200 % du prix en jetons, moyenne vers 75 %. « Des fois des bons drops et des fois à chier » | [Hugo] |
| Gold pack | Aucune commune : 2 rares ou mieux, 2 épiques ou mieux, 1 légendaire, qui a 20 % de chance d'être mythique. « Ça peut être 2 bleu 2 violet et 1 gold » | [Hugo] |
| Visuels | Originaux seulement, aucun logo tiers | [Hugo] (README) |
| Retrait après un burn | Une fois les jetons reçus, « ils vont sur les exchanges adaptés, c'est plus notre problème » | [Hugo] |

## 2. Code couleur des raretés

Les visuels générés (`art/memaster_art/rendu.py`) utilisent déjà ces couleurs. Elles correspondent au « 2 bleu,
2 violet, 1 gold » de Hugo.

| Rareté | Couleur | Cadre (clair → foncé) |
|---|---|---|
| Commune | gris | `#a3a39b` `#6b6d68` `#4a4c49` |
| Rare | bleu | `#a9d3ff` `#3d7cc9` `#1d3f73` |
| Épique | violet | `#e7b6ff` `#9b3fe0` `#4a137f` |
| Légendaire | or | `#fff6c2` `#e3b230` `#8a5a00` |
| Mythique | rouge sombre et or | `#ffd75e` `#8f0d18` `#1a0204` |

Les coins morts ont un style « cimetière ». Le dos de carte scellé existe aussi (`art/exemples/`).

## 3. Parcours joueur

### 3.1 Connexion

- near-connect, avec MetaMask (compte `0x…`, NEP-518) et les wallets NEAR natifs. Si l'adaptateur MetaMask tombe le
  jour de la démo, on choisit un autre wallet sans changer de code. **[Plan]** `faisabilite.md` §1
- Un nouveau compte MetaMask doit d'abord signer une transaction de « setup ». Le front l'explique. **[Contrat]**
- Avec MetaMask, un appel est plafonné à 270 Tgas. Un pack en consomme 28 à 30. **[Contrat]**

### 3.2 Boutique et achat

- Deux packs (recommandation de la simulation, à valider) : pack d'entrée à 0,20 $ et pack standard à 0,50 $. **[Plan]**
- **Avant l'achat**, on affiche les taux, la valeur moyenne en jetons et la phrase « la plupart des boosters valent moins
  que leur prix ». **[Plan]** `plan.md` 6.2. Avec la valeur aléatoire, 31 % des packs valent moins de 50 % de leur prix
  et 20 % plus de 100 % (simulation série 4).
- Un petit dépôt de stockage s'ajoute au prix : environ 0,006 NEAR par pack, 0,01 NEAR pour le premier pack d'un
  compte. Il est rendu quand la carte est brûlée. **[Contrat]** `testnet.md`
- On prévient avant l'achat qu'un coin peut mourir après l'ouverture et que ses jetons peuvent alors ne plus rien
  valoir. **[Plan]**

### 3.3 Ouverture

- Le tirage arrive **3 blocs après l'achat**, soit environ 1,8 s sur testnet. L'animation d'ouverture couvre ce délai :
  elle démarre à la signature et révèle les cartes quand l'événement de tirage est lu. **[Contrat]**
- On révèle les 5 cartes une par une, avec la couleur de rareté. On peut finir sur la carte brûlable, qui est toujours
  le dernier emplacement. **[Contrat]**
- On affiche la valeur du pack (quantité de jetons de la carte brûlable). Comme elle varie de 20 % à 200 %, le bon et
  le mauvais tirage doivent se voir. **[Hugo]**
- Gold pack : écran spécial, sans commune, et suspense sur la dernière carte (légendaire ou mythique). **[Hugo]**
- Une mythique tirée s'affiche « ? » jusqu'à la révélation de son contenu. **[Hugo]** **[Contrat]**

### 3.4 Mécaniques visibles (`mecaniques.md`)

| Mécanique | Ce que voit le joueur | Lecture côté contrat |
|---|---|---|
| Compteur de pitié | Progression vers le gold pack garanti, avec la formule publiée | `get_pity` |
| Gold rush | Avancement collectif vers le palier, puis compte à rebours du rush (30 min) et taux améliorés. Limite : 3 packs en rush par compte | `get_rush_state` |
| Rareté par les burns | Rareté actuelle d'une carte brûlable, qui monte quand la communauté brûle ce coin | `get_rates`, `get_burns` |
| Résurrection | Une carte de collection (coin mort) devient brûlable si son cours remonte. Notification au détenteur | `get_resurrected` |

### 3.5 Collection

- Mes cartes, le cimetière des coins morts et le détail d'une carte : quantité de jetons bloqués, jamais de « valeur
  garantie ». **[Plan]** `plan.md` 6.3
- Lecture : `nft_tokens_for_owner`, `get_card`, `get_backing`, `get_packs_for_owner`. **[Contrat]**
- Les cartes apparaissent aussi dans les wallets et sur TradePort grâce aux événements NEP-297. **[Contrat]**

### 3.6 Burn

- On brûle une carte et on reçoit ses jetons (`redeem`). Le burn se fait en deux temps : la carte est « en cours », puis
  détruite ou restaurée. Le front suit la livraison et dit où elle en est. **[Contrat]**
- Le choix de la destination (NEAR ou chaîne d'origine, adresse Solana lue dans MetaMask) est dans `plan.md` 6.5. Il
  est à revoir avec la consigne « après le burn, c'est plus notre problème ». **[Plan]** / **[Hugo]**

### 3.7 Marché

- Un marché intégré existe déjà dans le contrat (`get_listings`, `nft_payout` pour les redevances). **[Contrat]**

### 3.8 Transparence

- Page des taux : la table publiée et son hash. **[Plan]**
- Page de vérification des tirages : le hash de la table et du code, les tirages recalculés, les fréquences observées.
  Le vérificateur Python (`verifier/`) fait déjà tout cela. Le front peut l'appeler ou reprendre sa logique. **[Plan]**
- Page des réserves : les soldes `intents.near` comparés aux engagements, jeton par jeton. **[Plan]**

### 3.9 Mentions

- Un bandeau permanent « démo, testnet ou accès fermé », avec les mentions légales. **[Plan]** `plan.md` 6.7
- Toute partie simulée (faux Verifier) porte la mention « simulation » à l'écran. **[Plan]**

## 4. Points de vigilance

- **Jeu d'argent.** `mecaniques.md` note que la pitié « pousse à racheter, ce qui renforce l'aspect jeu d'argent ». Le
  compte à rebours du rush pousse dans le même sens. Le front ne doit donc pas en rajouter : pas de fausse urgence, pas
  d'achat en un clic sans voir les taux, pas de valeur garantie affichée.
- **Mythiques.** Aucun nom de mythique dans le front, son code ou ses fichiers publics. Les vrais noms restent dans
  `docs/data/secrets/`.
- **Visuels.** Aucun logo ni personnage repris d'un coin.

## 5. À rediscuter

1. **Nom du projet**, à trouver avant les visuels et le front (`plan.md` 0.1).
2. **Prix des packs** : faut-il valider 0,20 $ et 0,50 $ ? Le prix s'affiche-t-il en NEAR, en dollars ou les deux ?
3. **Valeur affichée à l'ouverture** : montrer le pourcentage du prix (« 140 % ! »), une quantité de jetons, ou les deux ?
4. **Burn** : faut-il garder le choix de la chaîne de destination, ou seulement un retrait vers NEAR ou le compte Intents ?
5. **Marché intégré pour la démo** : on le garde, ou on renvoie vers TradePort ?
6. **Compteur de pitié** : un compteur par compte, ou un NFT revendable (variante de `mecaniques.md`) ?
7. **Plateforme** : site web seulement, ou mobile aussi ? Avec MetaMask mobile ?
8. **Langue du site** : français, anglais (jury du hackathon) ou les deux ?
9. **Style graphique** : dans la lignée des cartes générées (fond sombre, cadres colorés), ou une autre direction ?
10. **Ce que montre la démo** : boutique, ouverture, collection et burn, ou aussi le marché et les pages de transparence ?
