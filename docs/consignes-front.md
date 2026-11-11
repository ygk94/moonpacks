# Consignes front et parcours joueur

Établi le 11/11/2026. Ce fichier rassemble ce qui concerne le front et le côté joueur : les demandes de Hugo, les
propositions issues de la recherche et les contraintes du contrat. Il sert de base à la discussion avant de coder le
front. Mis à jour avec les réponses de Hugo du 11/11.

## 1. Décisions de Hugo (11/11)

| Sujet | Consigne |
|---|---|
| Plateformes | Site web **et** app mobile, dont une app iOS |
| Langue | Site en **anglais seulement** |
| Wallet | MetaMask, testé ensemble dès qu'il y aura un front. Démo avec NEAR Intents |
| Mythiques | 3 cartes de rareté mythique **sans aucune information** : « ? » en image, en nom et en description |
| Ouverture | Une bonne animation, une ouverture fluide, des visuels de packs travaillés |
| Packs | Montrer beaucoup de mèmes disponibles, jamais les 3 mythiques |
| Prix | Affichés en NEAR **et** en dollars |
| Valeur d'un pack | On montre seulement la **quantité de jetons**. Ni pourcentage du prix ni « rentable ou pas » : le joueur fait ses calculs |
| Gold pack | Aucun compteur ni barre affichée, aucune garantie. La chance monte doucement en jouant : **1 sur 50 000** au départ, **1 sur 25 000** au mieux |
| Gold rush | L'avancement collectif est affiché |
| Collection | Oui. Pas de « cimetière » : on affiche la **valeur du coin** |
| Burn | Bouton dans le détail d'une carte brûlable. **Pas de choix de chaîne** : le joueur reçoit directement les jetons |
| Marché | Notre propre marché, avec les **cartes tendance** |
| Transparence | Taux de drop et hashs, consultables aussi sur l'explorateur NEAR (nearblocks) |
| Mention « simulation » | À voir plus tard |
| Style des cartes | Fond sombre, cadre coloré, **effet métallique**, belles animations pour les hautes raretés |
| Visuels | Originaux seulement, aucun logo d'un coin |
| Catalogue de démo | Pas de cartes à drapeau ni de politiciens, sauf s'il manque de jetons brûlables |
| Après un burn | Une fois les jetons reçus, « c'est plus notre problème » |

## 2. Code couleur des raretés

Couleurs déjà utilisées par les visuels générés (`art/memaster_art/rendu.py`), à enrichir d'un effet métallique.

| Rareté | Couleur | Cadre (clair → foncé) | Animation |
|---|---|---|---|
| Commune | gris | `#a3a39b` `#6b6d68` `#4a4c49` | aucune |
| Rare | bleu | `#a9d3ff` `#3d7cc9` `#1d3f73` | légère |
| Épique | violet | `#e7b6ff` `#9b3fe0` `#4a137f` | reflet métallique |
| Légendaire | or | `#fff6c2` `#e3b230` `#8a5a00` | reflet et particules |
| Mythique | rouge sombre et or | `#ffd75e` `#8f0d18` `#1a0204` | la plus forte ; carte « ? » |

## 3. Parcours joueur

### 3.1 Connexion

- near-connect : MetaMask (compte `0x…`, NEP-518) et les wallets NEAR natifs en secours, sans changer de code.
- Un nouveau compte MetaMask signe d'abord une transaction de « setup ». Le front l'explique.
- Avec MetaMask, un appel est plafonné à 270 Tgas. Un pack en consomme 28 à 30.
- App iOS : near-connect est une bibliothèque web. Il faut vérifier MetaMask mobile (lien profond ou WalletConnect).

### 3.2 Boutique et achat

- Prix en NEAR et en dollars. Recommandation de la simulation : pack d'entrée à 0,20 $ et pack standard à 0,50 $.
- Les taux sont accessibles avant l'achat (page transparence).
- Un petit dépôt de stockage s'ajoute : environ 0,006 NEAR par pack, 0,01 NEAR au premier pack d'un compte. Il est
  rendu quand la carte est brûlée.
- Les visuels de packs montrent beaucoup de mèmes du catalogue, jamais les mythiques.

### 3.3 Ouverture

- Le tirage arrive **3 blocs après l'achat**, soit environ 1,8 s sur testnet. L'animation démarre à la signature et
  révèle les cartes quand l'événement de tirage est lu.
- Les 5 cartes se révèlent une par une, avec la couleur de rareté. La carte brûlable est toujours la dernière.
- On affiche la quantité de jetons de la carte brûlable, pas le pourcentage du prix.
- Gold pack (très rare) : écran spécial, aucune commune, suspense sur la dernière carte.

### 3.4 Mécaniques visibles

| Mécanique | Ce que voit le joueur | Lecture côté contrat |
|---|---|---|
| Gold pack | Rien avant. La surprise à l'ouverture | (`get_pity` existe, non affiché) |
| Gold rush | Avancement collectif vers le palier, puis durée du rush et taux améliorés. 3 packs en rush par compte au plus | `get_rush_state` |
| Rareté par les burns | Rareté actuelle d'une carte brûlable | `get_rates`, `get_burns` |
| Résurrection | Une carte d'un coin mort devient brûlable si son cours remonte | `get_resurrected` |

### 3.5 Collection

- Mes cartes et le détail d'une carte : valeur du coin et quantité de jetons, jamais de « valeur garantie ».
- Lecture : `nft_tokens_for_owner`, `get_card`, `get_backing`, `get_packs_for_owner`.
- Le cours du coin vient d'une source de prix hors chaîne (GeckoTerminal ou DexScreener, voir `oracle-prix.md`).

### 3.6 Burn

- Dans le détail d'une carte brûlable, un bouton « Burn ». Le joueur reçoit directement les jetons, sans choisir de
  chaîne.
- Le burn se fait en deux temps : la carte est « en cours », puis détruite ou restaurée. Le front suit la livraison.

### 3.7 Marché

- Notre marché, déjà dans le contrat (`get_listings`, `nft_payout`), avec une section « tendance ».
- La tendance se calcule hors chaîne, à partir des ventes et des annonces récentes (indexeur à prévoir).

### 3.8 Transparence

- Page des taux et des hashs (table, code du contrat), avec des liens vers nearblocks pour les vérifier.
- Vérification des tirages : le vérificateur Python (`verifier/`) le fait déjà. On le relie ou on reprend sa logique.

### 3.9 Mentions

- Un bandeau « demo / testnet » avec les mentions légales.
- La mention « simulation » sur les parties simulées : à voir plus tard.

## 4. Points de vigilance

- **Jeu d'argent.** Le gold rush pousse à acheter pendant une fenêtre courte. Le front ne doit pas en rajouter : pas de
  fausse urgence, pas d'achat sans accès aux taux.
- **Mythiques.** Aucun nom de mythique dans le front, son code ou ses fichiers publics. Les vrais noms restent dans
  `docs/data/secrets/`.
- **Visuels.** Aucun logo ni personnage repris d'un coin.

## 5. Encore ouvert

1. **Nom du projet**, à trouver avant les visuels et le front.
2. **Durée de la montée du gold pack** : en combien de packs passe-t-on de 1/50 000 à 1/25 000 ? Proposition : 1 000.
3. **MetaMask sur l'app iOS** : à tester.
4. **Source du « coin value »** et de la tendance du marché.
