# Historique des échanges sur le projet

Échanges entre l'humain porteur du projet et l'agent de préparation du hackathon, du 10 au 11 novembre 2026.
Résumé fidèle des demandes, décisions et résultats, dans l'ordre.

## 10/11 : naissance du projet

**Contexte.** Le benchmark des projets déjà soumis (environ 400) montrait que les tracks memecoins (23 à 26 projets),
NFTs (31 à 32) et games (30) étaient les moins chargées, loin derrière security (194) et agents (189).
Le premier projet de l'équipe, ONA (agent IA privé), est mené à part.

**Demande.** Nouveau projet, tracks NFT et memecoins, pour surfer sur le buzz multi-chaînes :
- on paie en NEAR un booster de 5 cartes NFT NEAR représentant des memecoins de toutes les chaînes, avec rareté ;
- certaines cartes sont burnables, peu importe leur rareté, contre les jetons du memecoin ;
- les memecoins morts sont des cartes de collection dans les mêmes boosters.

**Décisions de l'humain :**
- les jetons sont **achetés et bloqués à l'ouverture** du booster ;
- taux de drop **on-chain** ;
- wallet visé : **MetaMask** ;
- **NEAR Intents** pour la démo ;
- pas de contrainte de date ;
- catalogue visé : **500 à 1000 cartes**.

## 10/11 : recherches

Trois études, puis le catalogue.

**Garde des jetons (`intents-et-garde.md`).**
- Le contrat détient les jetons sous forme de soldes NEP-245 sur `intents.near`.
- Un relayeur hors chaîne, sans pouvoir sur les fonds, fournit des devis 1Click signés.
- La carte n'est mintée qu'après livraison des jetons. Le burn retire directement les jetons vers le joueur.
- Chain Signatures écartées pour le hackathon.
- À vérifier : quels memecoins Intents couvre vraiment (`https://1click.chaindefuser.com/v0/tokens`) et avec quelle liquidité.
- La presse rapporte un piratage d'Intents de 3,8 M$ en octobre 2026.

**Wallets et aléa (`wallets-et-alea.md`).**
- MetaMask n'est pas natif sur NEAR. Il passe par l'adaptateur Ethereum de near-connect (NEP-518, comptes 0x),
  dont le statut mainnet est contradictoire : à tester en premier.
- Tirage : une seule signature, graines cumulées par callbacks, pas d'annulation ni de remboursement une fois le tirage connu.
  Probabilités fixes et publiées.
- Pas de marketplace NEAR active confirmée : prévoir une marketplace intégrée au contrat.

**Marché, droit et économie (`marche-droits-economie.md`).**
- Visuels : tout doit être original. Aucune licence trouvée pour BONK, WIF, SHIB, FLOKI ou PENGU.
- France (article L320-1) : les critères des jeux d'argent semblent remplis, le régime JONUM ne convient pas.
  Testnet ou démo fermée seulement, avis juridique avant mainnet.
- Économie (illustratif) : 60 à 70 % du prix du booster en jetons bloqués. Limite anti-arbitrage vers 82,9 %.
- Si l'achat des jetons échoue : recommandation de créditer la carte en NEAR (à confirmer par l'humain).

**Catalogue (`catalogue-final.md`).**
- Fusion de quatre catalogues de recherche (général 141, Solana 104, Base et autres 139, historiques 112)
  et des rangs CoinGecko de la catégorie memecoins.
- Résultat : **802 cartes** (389 étudiées, 413 issues de CoinGecko seulement), plus **63 jetons « à décider »**
  (jetons politiques comme Official Trump et Melania, cas litigieux).
- Rareté : 4 légendaires, 24 épiques, 123 rares, 651 communes.
- Burn : 26 oui, 44 oui à vérifier, 729 à vérifier, 3 non.
- Chaîne inconnue pour 437 cartes : le script d'images doit la compléter.

## 10–11/11 : images et droits

**Demande.** « Commence à récupérer les images des coins aussi. Pour ceux qui sont sous licence, fais une liste à part,
on verra plus tard pour la génération. »

**Droits (`visuels-droits.md`).**

| Liste | Cartes |
|---|---|
| Ayant droit ou propriété tierce identifiable, à générer plus tard | 248 (dont 145 « à confirmer ») |
| Licence ouverte documentée | 0 |
| Aucune licence connue | 554 |

- Dans la liste à part : Pepe, Brett, Dogecoin, Kabosu, Neiro, dogwifhat, Shiba Inu, Chill Guy, Moo Deng,
  Pudgy Penguins, Moonbirds, Milady, Simon's Cat, Wojak, GME, et les jetons sur Trump ou Elon Musk.
- Les 554 autres n'ont pas d'ayant droit identifié, mais sans licence leur logo appartient à ses créateurs :
  usage interne seulement, à régénérer avant toute mise en ligne publique. Bonk est jugé risqué.
- mfercoin : licence à vérifier.

**Images.** Le script `recuperer-images.py` lit le catalogue, interroge CoinGecko (catégorie meme-token, puis la liste des
plateformes), associe chaque carte par nom et ticker, télécharge les logos dans `docs/images/` et écrit
`images-manifest.csv` (statut, image, chaînes et adresses). Il reprend là où il s'est arrêté.
Il n'a pas encore tourné : le bac à sable de l'agent bloque le réseau. À lancer par un humain :
`python3 docs/recuperer-images.py`.

## 11/11 : dépôt dédié

**Demande.** Créer un dépôt pour le projet (nom provisoire **Memaster**), y mettre tous les échanges,
puis un sujet mesh pour le projet, afin de reprendre le travail sur une autre machine et de le partager à un collègue.

## 11/11 : couverture NEAR Intents et plan

**Demande.** Pas de sujet mesh pour l'instant. Lancer `/v0/tokens`, ajouter ou retirer des cartes en gardant une bonne
quantité, puis établir le plan de tout ce qu'il reste à faire.

**Résultats (`intents-couverture.md`).**
- 229 actifs sur 39 réseaux, une vingtaine de memecoins. Devis `dry` réussis pour 13 cartes (DOGE, SHIB, PEPE, WIF,
  PENGU, SPX, BOME, CASHCAT, TURBO, NearKat, BLACKDRAGON, SHITZU, JAMBO), plus TRUMP (« À décider »).
- Achat : 0,2 à 1,7 % de perte jusqu'à 100 $. Retrait vers la chaîne d'origine : coût fixe de 0,10 à 0,25 $, donc une
  carte brûlable d'au moins 5 $.
- Catalogue : 786 cartes (7 retirées, 14 jetons politiques passés dans « À décider », 5 ajoutées), 77 « À décider ».

**Plan (`plan.md`).** Phases 0 (décisions) à 7 (démo), chemin critique : MetaMask, `mt_transfer` par contrat, retrait.

## 11/11 : catalogue v2 et socle technique

**Demande.** La liste v1 ne va pas. Catalogue **full mèmes**, surtout des anciens qui ont explosé, ont rendu des gens
riches et ne valent plus rien. Ceux qui ont connu un pic fou sont légendaires. Trois coins choisis sont mythiques mais on ne
communique pas dessus : « ? » dans le catalogue. Une grosse liste de mèmes morts en communes. Toutes les chaînes,
recherches en parallèle. Burn : on verra plus tard comment financer ; le retrait vers les exchanges n'est pas notre
problème. Lancer le technique en sous-agents (simulation, contrat Rust NFT…), pas de front.

**Résultats.**
- Recherche par époque et par chaîne dans `docs/recherche-v2/` (r1 à r4), audit de v1 et relevé CoinGecko (r5).
- `docs/catalogue-v2.md` et `docs/data/catalogue-v2.json` : 1 649 cartes (3 / 21 / 235 / 230 / 1 160), 101 « À décider ».
- `contract/` (NEP-171/177/178/181/199, tirage sur reçus chaînés, mythiques scellés, marché, burn abstrait),
  `verifier/`, `sim/`, `art/`, `docs/faisabilite.md` (faisable hors burn, MetaMask viable via near-connect).

## Questions ouvertes

1. Nom du projet.
2. Trancher les 101 « À décider » et les drapeaux du catalogue v2.
3. Créditer la carte en NEAR si l'achat des jetons échoue ? Recommandation : oui.
4. ~~Vérifier la couverture des memecoins sur NEAR Intents~~ : fait le 11/11 (`intents-couverture.md`). À revérifier avant chaque série.
5. Tester MetaMask (adaptateur near-connect) sur testnet en premier.
6. Après le script d'images : compléter chaînes et adresses dans le catalogue.
7. Générer les visuels originaux (d'abord les 248 cartes à ayant droit).
8. Avis juridique avant tout mainnet.
