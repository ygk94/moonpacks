# Front Memaster : ce qui reste à faire (pour Hugo)

État au 11/11/2026, branche `feat/front` (créée depuis `feat/demo`). Rien n'est poussé.

## Ce qui est fait

Le web demandé par `docs/front/CONSIGNE.md` est écrit dans `front/`. Le détail est dans `front/README.md`.

- Écrans : boutique, ouverture des boosters, collection, détail d'une carte avec burn et mise en vente, marché avec
  « Trending », transparence (taux, hash de la table, hash du code, vérification d'un pack), mentions légales.
- Règles de la consigne : interface en anglais, mythiques en « ? », aucun pourcentage de rentabilité, pas de
  compteur de pitié, pas de fausse urgence, bandeau « Demo · NEAR testnet » permanent.
- Visuels : ceux de `art/`, avec une nouvelle option `--langue en` (les SVG étaient en français).
- Indexeur facultatif (`front/indexer/`), pour « Trending » et les dernières ventes.
- 35 tests (`npm test`), un build propre et un contrôle automatique « aucun nom de mythique ».

Lancement :

```sh
cd front && npm install && npm run dev      # http://localhost:5173
cd front && npm run indexer                 # facultatif, second terminal
```

## 1. Décisions à prendre

| # | Sujet | Situation | Ce qu'il faut trancher |
|---|---|---|---|
| 1 | **Nom du projet** | « Memaster », provisoire, partout dans le front | Le nom, puis le logo, les visuels de packs et le domaine |
| 2 | **Pile iOS** | Rien n'est commencé dans `mobile/` | React Native (Expo) : code partagé avec le web, near-connect réutilisable. Ou Swift : animations natives, mais near-connect est en JavaScript ; compromis possible, une `WKWebView` pour la connexion et la signature |
| 3 | **Prix des packs** | Le contrat n'a qu'une série, à **0,1 NEAR**. La boutique affiche toutes les séries ouvertes | Créer les séries « entrée » (0,20 $) et « standard » (0,50 $) côté contrat. Le prix est fixé en NEAR, donc le prix en dollars bougera |
| 4 | **Quantité de jetons d'une carte brûlable** | L'adossement (`amount`) est une **valeur en yoctoNEAR**, pas une quantité de jetons (`docs/mecaniques-spec.md`). Le front estime `amount × cours NEAR / cours du coin`. Pour un coin presque sans valeur, ça donne des nombres énormes (« 25,800T SHIBDOGE ») | Comment le redeemer achète les jetons, et où le front lit la vraie quantité |
| 5 | **Dépôt de stockage** | Le contrat exige **0,016 NEAR** par pack (pire cas). **Contrat v3 : l'excédent est rendu à l'ouverture** (environ 0,0057 NEAR au premier pack d'un compte, davantage ensuite) ; la boutique le dit et le récapitulatif affiche le montant rendu | Rien, sauf si le dépôt joint doit baisser |
| 6 | **Dépôt rendu au burn ?** | **Contrat v3 : oui, en partie.** Le burn rend le stockage libéré (`card_redeemed.storage_refund`, environ 16 o pour un burn ordinaire) ; l'emplacement du pack reste écrit (`docs/mecaniques-spec.md`, 12.2). Le front affiche le montant rendu après le burn, sans promesse avant | Corriger la consigne (« rendu au burn » → « l'excédent est rendu à l'ouverture, le stockage libéré au burn ») |
| 7 | **Source des cours** | NEAR/USD : CoinGecko. Cours d'un coin : DexScreener par adresse, sinon CoinGecko par identifiant. Appels directs depuis le navigateur, sans clé | Valider, ou passer par un service maison (limites de débit, CoinGecko sans clé) |
| 8 | **MetaMask sur iOS / WalletConnect** | near-connect affiche MetaMask (« Ethereum Wallets ») en premier. WalletConnect n'est pas branché | Créer un `projectId` WalletConnect (gratuit) ; je le brancherai par variable d'environnement |
| 9 | **Mention « simulation »** | Rien n'est affiché sur les parties simulées (redeemer et jetons factices sur testnet) | Le texte et l'endroit (hors périmètre pour l'instant, consigne § 7) |
| 10 | **Mentions légales** | Page en place ; l'éditeur et le contact sont « à compléter » | Les informations d'éditeur |
| 11 | **Contrat visé** | La consigne cite `app.memaster-demo-j7xg7z.testnet`. Le front vise **`app2.…`**, la dernière version (`docs/testnet.md`) | Confirmer `app2`, ou donner le nouveau compte après le redéploiement prévu (variable `VITE_CONTRACT_ID`) |
| 12 | **Push, PR, déploiement public** | Rien n'est poussé (consigne § 9) | Ton accord |

## 2. Tests qui demandent un wallet

Personne n'a encore pu les faire. Il faut un peu de NEAR testnet sur le compte : environ 0,12 NEAR par pack, plus
le gaz. Avec MetaMask, il faut donc alimenter le compte `0x…` (NEP-518).

- [ ] Connexion avec MetaMask, transaction de setup comprise, et avec un wallet NEAR natif (Meteor, Intear…)
- [ ] Achat d'un pack : bon dépôt, ouverture jusqu'au récapitulatif, bouton « Verify this pack »
- [ ] Message clair si le solde est insuffisant
- [ ] Burn d'une carte brûlable : `redeem_started`, puis `card_redeemed` (ou `redeem_failed` et carte restaurée)
- [ ] Mise en vente, retrait, achat par un second compte ; puis « Trending » et les dernières ventes avec l'indexeur
- [ ] Ouverture fluide sur un vrai iPhone récent (vérifiée seulement à la taille d'un téléphone dans un navigateur)
- [ ] Pack bloqué débloqué depuis l'interface (difficile à provoquer volontairement)

## 3. Travail restant

Déjà fait depuis la première version de ce document : vérification complète dans le navigateur (carte exacte et
décision gold, via l'historique de l'indexeur), pagination de l'indexeur, WalletConnect par variable
d'environnement, chargement plus rapide de l'ouverture, contrôle anti-fuite des mythiques.

**À lancer de ton côté** : `cd front && npm run check:mythics`. Le fichier secret des mythiques n'est que sur ta
machine ; sans lui, le contrôle se limite à la structure.


| Sujet | Détail |
|---|---|
| **App iOS** | Tout est à faire, après la décision 2 |
| **Images des NFT dans les wallets** | Les métadonnées on-chain pointent vers `ipfs://TODO/<carte>.svg` (`media_template` de `build_series.py`). Les wallets et explorateurs montreront une image cassée. Il faut héberger les visuels (version anglaise : `--langue en`) et mettre la bonne URL dans la série |
| **Hébergement de l'indexeur** | Il tourne en local (SQLite). Pour une démo publique, il faut l'héberger quelque part et définir `VITE_INDEXER_URL` |
| **Pack `stuck`** | Contrat v3 : « Refund » appelle `refund_stuck_pack` (prix et stockage non utilisé rendus à l'acheteur), puis le pack s'affiche `refunded`. `retry_reveal` n'est proposé qu'à l'acheteur. Sur `app2`, message de contact |
| **Messages d'erreur du contrat** | Contrat v3 : traduits par code `E_…` (`front/src/near/errors.ts`, textes anglais de `contract/ERRORS.md`) ; un test échoue si un code n'est pas traduit. Repli sur l'ancien texte français pour `app2` |

## 4. Où regarder

- `front/README.md` : lancement, configuration, structure, règles appliquées, ce qui est testé.
- `front/src/pages/Opening.tsx` : l'ouverture des boosters.
- `front/src/verify/verify.ts` : la vérification d'un tirage (même logique que `verifier/`).
- `front/indexer/indexer.mjs` : l'indexeur et son API.
