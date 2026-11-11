# Memaster (nom provisoire)

Second projet de l'équipe pour le NEAR HACKATHON, tracks **NFTs** et **memecoins**. Le nom n'est pas encore choisi.

## L'idée

- On paie en NEAR un **booster de 5 cartes NFT** (sur NEAR) représentant des memecoins de toutes les chaînes, avec une rareté.
- Certaines cartes sont **burnables**, quelle que soit leur rareté : on brûle la carte et on reçoit les jetons du memecoin.
  Ces jetons sont achetés et bloqués au moment de l'ouverture du booster.
- Les memecoins morts sont des **cartes de collection**, dans les mêmes boosters.
- Les taux de drop sont publiés **on-chain**.
- Wallet visé : MetaMask. Démo : NEAR Intents.
- Catalogue visé : 500 à 1000 cartes (802 aujourd'hui).

## État au 11/11/2026

C'est de la recherche, pas encore de code. Tout est dans `docs/` :

| Fichier | Contenu |
|---|---|
| `historique-echanges.md` | Nos échanges sur le projet : demandes, décisions, questions ouvertes |
| `intents-et-garde.md` | Garde des jetons via NEAR Intents, relayeur, burn |
| `wallets-et-alea.md` | MetaMask sur NEAR, tirage aléatoire, marketplace |
| `marche-droits-economie.md` | Marché, droit français des jeux, économie du booster |
| `catalogue-final.md` | **Le catalogue retenu** : 802 cartes, avec rareté, burn et chaîne, plus 63 jetons « à décider » |
| `catalogue*.md` | Catalogues intermédiaires (général, Solana, Base et autres, historiques, CoinGecko brut) |
| `visuels-droits.md` | Droits sur les visuels : 248 cartes avec ayant droit identifiable, 0 sous licence ouverte, 554 sans licence connue |
| `recuperer-images.py` | Télécharge les logos et adresses depuis CoinGecko (`python3 docs/recuperer-images.py`) |

## Points de vigilance

- **Juridique** : un paquet aléatoire payant à valeur revendable remplit sans doute les critères des jeux d'argent en France.
  Testnet ou démo fermée seulement, avis juridique avant tout mainnet.
- **Visuels** : aucun logo n'est réutilisable publiquement tel quel. Les images téléchargées (`docs/images/`) restent
  internes et ne sont pas versionnées. Visuels originaux à générer.
- **Secrets** : aucune clé dans le dépôt, seulement des variables d'environnement.
- **Garder le dépôt privé** tant que l'équipe n'a pas décidé de le publier.
