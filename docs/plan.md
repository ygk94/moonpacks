# Plan Memaster

Établi le 11/11/2026, à partir de toute la recherche de `docs/` et du relevé NEAR Intents (`intents-couverture.md`).
Le but est d'arriver à une démo honnête pour le NEAR Hackathon (tracks NFTs et memecoins), sans vente au public.

**Principe d'ordre.** D'abord ce qui peut tuer le projet (les tests de faisabilité de la phase 1), ensuite ce qui fixe
les nombres (la phase 2), puis seulement le code. Un test qui échoue en phase 1 change le plan : chaque test a son plan B.

**Légende.** `[ ]` à faire, `[x]` fait, **Hugo** = décision humaine.

---

## Phase 0 : décisions de l'équipe

| # | Décision | Recommandation | État |
|---|---|---|---|
| 0.1 | Nom du projet | À trouver avant les visuels et le front | [ ] **Hugo** |
| 0.2 | Que faire des 101 jetons « À décider » du catalogue v2 (cannabis coins, Verge, Skibidi, homonymes, pics douteux) et des cartes à drapeau (politique, personne réelle, obscène, arnaque avérée) | Exclure « À décider » de la démo ; trancher les drapeaux un par un | [ ] **Hugo** |
| 0.3 | Si l'achat des jetons échoue après le tirage | La carte reste adossée en NEAR, jamais de remboursement | [ ] **Hugo** |
| 0.4 | Prix du booster et part d'adossement β | 10 NEAR (environ 36 $), β = 60 %, après simulation (phase 2) | [ ] **Hugo** |
| 0.5 | Mécanique de burn : quelles cartes, financement des jetons | Reportée (décision du 11/11). Le retrait des jetons vers les exchanges n'est pas notre sujet | [ ] **Hugo**, plus tard |
| 0.6 | Chaînes de la démo | NEAR et Solana, Ethereum seulement si le budget le permet | [ ] **Hugo** |
| 0.7 | Budget de la preuve mainnet | Environ 50 $ sur un compte dédié | [ ] **Hugo** |

## Phase 1 : lever les risques bloquants

Chaque test est petit, isolé, et se fait avant d'écrire le vrai contrat.

| # | Test | Pourquoi | Plan B si échec | État |
|---|---|---|---|---|
| 1.1 | Lire `/v0/tokens` et faire des devis `dry` | Savoir quels memecoins sont réellement disponibles | | [x] 13 brûlables, voir `intents-couverture.md` |
| 1.2 | MetaMask via near-connect (compte `0x…`, NEP-518) : connexion, appel avec dépôt, `nft_transfer` | Wallet voulu, mais retiré de la doc NEAR en octobre 2026 | Wallets NEAR natifs (Meteor, HOT) en premier choix, MetaMask en bonus | [ ] |
| 1.3 | Alimenter un compte `0x…` en NEAR natif depuis Base ou Ethereum | Sans NEAR sur le compte, pas de gaz ni d'achat | Le relais paie le premier dépôt ; ou paiement en USDC sur Intents | [ ] |
| 1.4 | Un contrat de test sur mainnet appelle `intents.near::mt_transfer` vers le `depositAddress` d'un devis réel de 1 $ | Seul un projet tiers montre ce chemin | Garde en coffre NEP-141 (option B) | [ ] |
| 1.5 | Le contrat vérifie la signature ed25519 du devis et les champs (destinataire, remboursement, `minAmountOut`, slippage), et contrôle l'échéance à part | Le relais ne doit avoir aucun pouvoir sur les fonds | Relais de confiance, annoncé comme tel dans la démo | [ ] |
| 1.6 | Le contrat fait `ft_withdraw` ou `mt_withdraw` vers NEAR, puis vers Solana (format de mémo du pont) | Le burn en dépend | Burn vers NEAR seulement | [ ] |
| 1.7 | Testnet : rythme des callbacks internes et gaz du pire cas (5 cartes, la plus chère en stockage) | Le tirage anti-snipe en dépend | Commit-reveal en deux transactions | [ ] |
| 1.8 | Lancer `python3 docs/recuperer-images.py` | Compléter les chaînes et adresses de 423 cartes | Remplissage par lots via CoinGecko `/coins/{id}` | [ ] |

**Chemin critique : 1.2, 1.4 et 1.6.** S'ils passent tous les trois, l'architecture de la recherche tient.

## Phase 2 : économie et catalogue

- [x] **2.0 Catalogue v2** (11/11) : 100 % mèmes, surtout des anciens pump → mort, toutes chaînes. 1 649 cartes
  (mythique 3 scellés « ? » = DOGE, SHIB, PEPE ; légendaire 21 ; épique 235 ; rare 230 ; commune 1 160) et
  101 « À décider ». Script relançable `docs/recherche-v2/consolider.py`, surclassements manuels dans
  `docs/recherche-v2/surclassements.md`. La disponibilité sur NEAR Intents ne filtre plus le catalogue.

- [x] **2.1 Simulateur Monte-Carlo** (`sim/`, série 1 faite ; série 2 sur le catalogue v2 en cours) (Python, `sim/`) : raretés, poids, multiplicateurs, β, coûts réels mesurés
  (achat de 0,2 à 1 %, retrait fixe de 0,10 à 0,25 $). Il calcule l'espérance, la variance, la réserve `R₀`, le plafond
  par booster `V_cap`, la borne anti-arbitrage sur β, et la part de boosters qui valent plus que leur prix.
- [ ] **2.2 Table de la série 1.** Les 13 brûlables, plus une sélection de cartes de collection (cimetière compris),
  avec des plafonds par carte et une taille maximale par coin, fixées à partir des devis à 1 000 $.
- [ ] **2.3 Valeur minimale d'une carte brûlable** : au moins 20 fois le coût de retrait, soit environ 5 $.
- [x] **2.4 Règle objective de « coin mort »** (appliquée dans `catalogue-v2.md`) (liquidité et volume sur 30 jours), appliquée au catalogue.
- [ ] **2.5 Revoir les raretés** des cartes à pic « estimé » (375 cartes) après l'étape 1.8.
- [ ] **2.6 Script de vérification de couverture** à relancer avant chaque série (reprend `devis-intents.py`).

## Phase 3 : contrat NEAR (Rust, near-sdk)

Un seul contrat pour les cartes et le marché. Architecture de `intents-et-garde.md` (option A) et de `wallets-et-alea.md`.

- [x] **3.1 Squelette.** NEP-171, 177, 178 et 199, événements NEP-297, sans clé d'accès complète après le déploiement.
- [x] **3.2 Séries.** La table est figée et hachée à l'ouverture : prix, poids, plafonds, quantité par carte. Elle est
  lisible par tous.
- [x] **3.3 `buy_pack`.** Prix et stockage dans un seul dépôt. Le booster passe à `Pending`, sans aucune annulation.
- [x] **3.4 Tirage** sur 3 à 5 reçus `#[private]` à gaz fixe :
  `acc = sha256(acc || random_seed || pack_id || owner)`, puis `retry_reveal` ouvert à tous après un délai.
- [ ] **3.5 Machine d'achat par ligne** : `PAYÉ → COTÉ → ENVOYÉ → LIVRÉ | REMBOURSÉ | BLOQUÉ`. La carte est créditée de
  `minAmountOut`, après un contrôle de couverture (`mt_batch_balance_of ≥ engagements + minAmountOut`).
- [x] **3.6 Burn en deux temps.** État `Redeeming`, retrait d'une carte par transaction, restauration en cas d'échec,
  sortie de secours sur NEAR.
- [x] **3.7 Marché intégré** (`list` et `buy` dans le même reçu), interdit sur une carte en `Redeeming`.
- [ ] **3.8 Garde-fous.** Arrêt des ventes si la réserve passe sous `V_cap`, plafond par coin, délai de burn, et aucune
  modification silencieuse des taux.
- [ ] **3.9 Tests.** Unitaires et sandbox (near-workspaces) avec un faux Verifier : succès, remboursement, blocage,
  surplus, exécution à 4 cartes sur 5, et tentative de relance après un mauvais tirage.

État au 11/11 : contrat dans `contract/` (67 tests unitaires + 17 sandbox, deux revues de sécurité, rien de critique ;
séries jusqu'à 2 000 cartes chargées par lots, catalogue v2 complet testé via `scripts/build_series.py`),
burn via un `redeemer` abstrait en attendant la décision 0.5, vérificateur public dans `verifier/`. Retrait des recettes
à écrire. Rien n'est déployé.

## Phase 4 : relais (TypeScript)

- [ ] **4.1** Écoute les boosters payés, demande les devis 1Click (`dry: false`, `EXACT_INPUT`, `INTENTS` → `INTENTS`,
  `refundType: INTENTS`) et les soumet au contrat.
- [ ] **4.2** Suit le statut du swap, puis confirme la livraison, ou passe la ligne en remboursée ou bloquée à l'échéance.
- [ ] **4.3** Clé API 1Click dans une variable d'environnement, et en-tête User-Agent explicite (Cloudflare bloque les
  en-têtes par défaut). Plusieurs relais possibles.
- [ ] **4.4** Mode « simulation » branché sur le faux Verifier pour le testnet.

## Phase 5 : visuels et métadonnées

- [x] **5.1 Générateur d'art original et abstrait** (`art/`, régénération sur le v2 en cours), à partir de l'adresse, du ticker et de la rareté. Aucun logo,
  personnage ni ressemblance. Il couvre les 786 cartes, en commençant par les 13 brûlables et les 233 de la liste A.
- [x] **5.2 Cadres de rareté**, et un style « cimetière » pour les coins morts.
- [ ] **5.3 Métadonnées NEP-177.** `reference` et `reference_hash` (IPFS ou Arweave), avec la mention de non-affiliation.
- [ ] **5.4 Changer l'image d'une carte** sans toucher aux jetons bloqués (`nft_metadata_update`).

## Phase 6 : front (web)

- [ ] **6.1 Connexion** near-connect : MetaMask (`0x…`) et wallets NEAR.
- [ ] **6.2 Achat et ouverture animée** du booster. Les taux, l'espérance et « la plupart des boosters valent moins que
  leur prix » sont affichés avant l'achat.
- [ ] **6.3 Collection**, cimetière, détail d'une carte (quantité de jetons, jamais de « valeur garantie »).
- [ ] **6.4 Marché intégré.**
- [ ] **6.5 Burn.** Choix de la destination (NEAR ou chaîne d'origine), adresse Solana lue par la session multichaîne de
  MetaMask, validation du format, confirmation, et suivi de la livraison.
- [ ] **6.6 Page transparence** (soldes `intents.near` comparés aux engagements, jeton par jeton) et **page de
  vérification des tirages** (hash de la table et du code, tirages recalculés, fréquences observées).
- [ ] **6.7 Bandeau** « démo, testnet ou accès fermé », avec les mentions légales.

## Phase 7 : démo et soumission

- [ ] **7.1 Niveau 1.** Catalogue réel et devis `dry` en direct.
- [ ] **7.2 Niveau 2.** Contrat sur testnet avec le faux Verifier, marqué « simulation » à l'écran.
- [ ] **7.3 Niveau 3.** Une preuve sur mainnet : un booster, 2 ou 3 cartes, un burn NEAR → NEAR (par exemple SHITZU ou
  BLACKDRAGON), et si possible un burn vers Solana. Liens vers les transactions.
- [ ] **7.4** Vidéo de démo (skill `demo-video`), README public, pitch.
- [ ] **7.5** Décider de rendre le dépôt public, après un nettoyage : pas de logos tiers, pas de secrets.

## Avant tout public, hors hackathon

- [ ] Avis d'avocat (L320-1, JONUM, MiCA, droit américain), restriction d'âge et de pays.
- [ ] Audit du contrat et du relais.
- [ ] VRF OutLayer pour les séries chères, et Chain Signatures pour réduire la dépendance aux ponts.

---

## Prochaines actions proposées

1. Hugo tranche la phase 0 : nom, « À décider » et drapeaux du catalogue v2, prix et β (après la série 2 de la sim).
2. Front : pas pour l'instant (consigne du 11/11).
3. Test 1.2 (MetaMask, checklist manuelle dans `faisabilite.md`) et 1.7 (callbacks) sur testnet, quand Hugo le valide.
4. Burn (0.5) et relais (phase 4) : plus tard.
