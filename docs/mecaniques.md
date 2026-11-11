# Mécaniques retenues et prix du pack (11/11/2026)

## Mécaniques

Ajoutées après un classement à l'aveugle des idées : les juges plaçaient le projet 2e en nfts mais 4e en memecoins, avec
le même reproche, « ce n'est pas un memecoin dont la mécanique réagit à sa communauté ». Les mécanismes 1 à 3 y
répondent ; le compteur de pitié sert le confort du joueur et la track nfts.

### 0. Compteur de pitié (idée de l'humain)

- Chaque pack ouvert sans gold pack augmente la chance du suivant ; au bout de N packs, le gold pack est garanti, puis
  le compteur repart à zéro.
- Compteur on-chain par compte, formule publiée : la transparence porte sur une formule, plus sur des taux fixes.
- Variante nfts : le compteur vit dans un NFT revendable. La progression vers le gold pack devient un actif.
- Le coût du gold pack garanti est inclus dans la valeur moyenne d'un pack (taux de couverture moyen, voir plus bas).
- Point de vigilance : la mécanique pousse à racheter, ce qui renforce l'aspect jeu d'argent (voir
  `marche-droits-economie.md`).

### 1. Rareté pilotée par les burns

Quand les joueurs brûlent les cartes d'un memecoin, les cartes restantes de ce coin deviennent plus rares dans les packs
suivants. La communauté fabrique la rareté. Formule publiée, par exemple : poids de tirage du coin =
poids de base × (cartes en circulation / cartes émises).

### 2. Gold rush collectif

Quand la communauté atteint un palier (par exemple 1 000 packs ouverts dans la semaine), les packs suivants ont de
meilleurs taux pour tout le monde pendant une durée fixe (par exemple une heure). Jeu de coordination autour de
l'ouverture. Palier, bonus et durée publiés on-chain.

### 3. Résurrection des coins morts

Si le cours réel d'un memecoin « mort » remonte au-dessus d'un seuil, ses cartes de collection deviennent burnables.
Il faut une source de prix fiable (oracle) et un stock de jetons à acheter à ce moment-là : à cadrer.

## Prix du pack : à partir de combien c'est rentable

Hypothèses à vérifier : cours du NEAR à 2,5 $ (à remplacer par le cours du jour), couverture en jetons de 65 % du prix
(fourchette 60–70 % de `marche-droits-economie.md`, gold packs de pitié compris).

### Coût par pack de 5 cartes

| Poste | Naïf | Optimisé |
|---|---|---|
| Stockage on-chain des 5 NFT (0,01 NEAR par Ko, rendu au burn) | ~3,5 Ko → 0,035 NEAR ≈ 0,09 $ | métadonnées dans le catalogue, chaque carte ne stocke qu'un numéro : ~1 Ko → 0,01 NEAR ≈ 0,025 $ |
| Gaz (achat, tirage aléatoire en callbacks, mint) | ~0,01 NEAR ≈ 0,025 $ | idem |
| Achat des jetons via Intents | un swap par carte : petits montants refusés ou mal cotés | achats groupés : le contrat garde un stock et bloque les jetons de chaque carte à l'ouverture ; ~0,2 % de frais 1Click + écart, ≈ 0,5–1 % de la couverture |
| **Total hors couverture** | **≈ 0,12 $ et plus** | **≈ 0,05 $** |

Le burn ne coûte presque rien si les jetons sont crédités sur le compte Intents du joueur : il les retire ensuite vers
leur chaîne quand il veut, en une fois, à ses frais. Sinon, retirer 5 centimes de jetons vers Ethereum coûterait plus
que leur valeur.

### Seuil de rentabilité

Marge par pack = prix × (1 − 65 %) − coûts.

| Prix du pack | Marge (version optimisée, coûts 0,05 $) | Marge (version naïve, coûts 0,12 $) |
|---|---|---|
| 0,10 $ | −0,015 $ | −0,085 $ |
| **0,15 $** | **≈ 0 (seuil)** | −0,07 $ |
| 0,20 $ | +0,02 $ (10 %) | −0,05 $ |
| 0,35 $ | +0,07 $ (20 %) | ≈ 0 (seuil) |
| 0,50 $ | +0,125 $ (25 %) | +0,055 $ |
| 1,00 $ | +0,30 $ (30 %) | +0,23 $ |

- **20 centimes, c'est possible** mais à peine rentable (~2 centimes par pack), et seulement avec la version optimisée.
- Pour une marge saine (20–30 %), viser **0,35 à 0,50 $**, ou garder 0,20 $ en baissant la couverture vers 50 % pour les
  packs de lancement.
- Piste : pack d'entrée à 0,20 $ (couverture plus basse, peu de cartes burnables), pack standard à 0,50–1 $.
- Le prix bas ne change rien à la question du jeu d'argent : l'avis juridique reste nécessaire avant mainnet.

Chiffres à recalculer quand le contrat sera écrit (taille réelle d'un NFT, gaz réel mesuré sur testnet) et avec le cours
du NEAR du moment.
