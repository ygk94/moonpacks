# Memaster (nom provisoire)

Second projet de l'équipe pour le NEAR HACKATHON, tracks **NFTs** et **memecoins**. Le nom n'est pas encore choisi.

## L'idée

- On paie en NEAR un **booster de 5 cartes NFT** (sur NEAR) représentant des memecoins de toutes les chaînes, avec une rareté.
- Certaines cartes sont **burnables**, quelle que soit leur rareté : on brûle la carte et on reçoit les jetons du memecoin.
  Ces jetons sont achetés et bloqués au moment de l'ouverture du booster.
- Les memecoins morts sont des **cartes de collection**, dans les mêmes boosters.
- Les taux de drop sont publiés **on-chain**.
- Wallet visé : MetaMask. Démo : NEAR Intents.
- Catalogue visé : 500 à 1000 cartes (786 aujourd'hui, dont 13 brûlables via NEAR Intents).

## Mécaniques (détail : `docs/mecaniques.md`)

1. **Compteur de pitié** : chaque pack ouvert sans gold pack augmente la chance du suivant ; au bout de N packs, le gold
   pack est garanti. Compteur on-chain par compte, formule publiée ; variante : le compteur vit dans un NFT revendable.
2. **Rareté pilotée par les burns** : plus la communauté brûle les cartes d'un memecoin, plus les cartes restantes de ce
   coin deviennent rares dans les packs suivants.
3. **Gold rush collectif** : quand la communauté atteint un palier (par exemple 1 000 packs dans la semaine), les taux
   s'améliorent pour tout le monde pendant une durée fixe.
4. **Résurrection des coins morts** : si le cours d'un memecoin « mort » remonte au-dessus d'un seuil, ses cartes de
   collection deviennent burnables (oracle de prix et stock de jetons à cadrer).

## Prix du pack

Avec 65 % du prix reversé en jetons et un contrat optimisé (~0,05 $ de coûts par pack), le **seuil de rentabilité est
vers 0,15 $**. À 0,20 $, c'est possible mais à peine rentable (~2 centimes par pack). Pour une marge saine de 20 à 30 %,
viser **0,35 à 0,50 $**. Piste : pack d'entrée à 0,20 $, pack standard à 0,50–1 $. Hypothèse : NEAR à 2,5 $, chiffres à
recalculer avec le gaz réel mesuré sur testnet.

## État au 11/11/2026

C'est de la recherche, pas encore de code. **Le plan de travail est dans `docs/plan.md`.** Tout est dans `docs/` :

| Fichier | Contenu |
|---|---|
| `mecaniques.md` | Les 4 mécaniques retenues et le calcul du prix du pack |
| `historique-echanges.md` | Nos échanges sur le projet : demandes, décisions, questions ouvertes |
| `intents-et-garde.md` | Garde des jetons via NEAR Intents, relayeur, burn |
| `wallets-et-alea.md` | MetaMask sur NEAR, tirage aléatoire, marketplace |
| `marche-droits-economie.md` | Marché, droit français des jeux, économie du booster |
| `plan.md` | **Le plan de travail**, par phases, avec les décisions à prendre |
| `intents-couverture.md` | Memecoins réellement disponibles sur NEAR Intents (relevé du 11/11), coûts d'achat et de retrait |
| `catalogue-final.md` | **Le catalogue retenu** : 786 cartes, avec rareté, burn (statut Intents réel) et chaîne, plus 77 jetons « à décider » |
| `catalogue*.md` | Catalogues intermédiaires (général, Solana, Base et autres, historiques, CoinGecko brut) |
| `visuels-droits.md` | Droits sur les visuels : 233 cartes avec ayant droit identifiable, 0 sous licence ouverte, 553 sans licence connue |
| `devis-intents.py`, `data/` | Script de devis 1Click `dry` et relevés bruts du 11/11 |
| `recuperer-images.py` | Télécharge les logos et adresses depuis CoinGecko (`python3 docs/recuperer-images.py`) |

## Points de vigilance

- **Juridique** : un paquet aléatoire payant à valeur revendable remplit sans doute les critères des jeux d'argent en France.
  Testnet ou démo fermée seulement, avis juridique avant tout mainnet.
- **Visuels** : aucun logo n'est réutilisable publiquement tel quel. Les images téléchargées (`docs/images/`) restent
  internes et ne sont pas versionnées. Visuels originaux à générer.
- **Secrets** : aucune clé dans le dépôt, seulement des variables d'environnement.
- **Garder le dépôt privé** tant que l'équipe n'a pas décidé de le publier.
