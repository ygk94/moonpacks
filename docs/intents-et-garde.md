# Boosters de memecoins : NEAR Intents et garde des tokens

Recherche du 10 novembre 2026. Question : comment acheter, garder et rendre sur sa chaîne d'origine le memecoin qui
adosse chaque carte NFT (NEP-171).

## Limites de cette recherche

Tout vient de recherches web. Aucune page n'a été lue en entier, aucun appel à l'API 1Click n'a été fait, aucune
transaction n'a été envoyée. Les statuts ci-dessous veulent donc dire :

| Statut | Sens |
|---|---|
| **DOC** | Dit par la documentation officielle (extrait remonté par la recherche, page non relue en entier) |
| **TIERS** | Dit par un dépôt, un rapport de bug ou un article tiers, une seule source le plus souvent |
| **INFÉRENCE** | Déduit par moi de faits établis, ou connaissance générale sans source trouvée |
| **NON VÉRIFIÉ** | Cherché sans réponse fiable, ou sources contradictoires |

Plusieurs pages de la doc Intents datent de 259 à 539 jours, et le contrat a changé après l'attaque d'octobre 2026.

**Première action de l'équipe :** `curl https://1click.chaindefuser.com/v0/tokens`, filtré par adresse de contrat. Cette
commande tranche la question 1 en une minute, ce que la recherche web n'a pas pu faire.

## 1. Ce qu'Intents et 1Click supportent

### Chaînes

| Fait | Statut | Source |
|---|---|---|
| Solana, Base, BNB Chain, Monad et Dogecoin figurent dans les chaînes supportées ; Ethereum existe aussi (`blockchain: eth`) | DOC | [Supported Chains](https://docs.near-intents.org/resources/chain-support), [Making a Request](https://docs.near-intents.org/integration/distribution-channels/1click-api/quickstart/making-a-request) |
| Environ 32 à 35 réseaux, selon la source et la date | TIERS, ordre de grandeur | [intents.near.org](https://intents.near.org/), [Leodex](https://leodex.io/learn/near-intents/what-is-near-intents) |
| Dogecoin est marqué entièrement supporté, adresses commençant par D | DOC | [Supported Chains](https://docs.near-intents.org/resources/chain-support) |
| Le pont utilisé dépend de la destination : Omni pour Base, BNB, Solana ; HOT pour BNB, Monad et d'autres ; PoA pour une partie du reste | DOC | [Token Bridges](https://docs.near-intents.org/integration/bridging/overview) |

### Comment la liste est exposée

- **DOC.** `GET https://1click.chaindefuser.com/v0/tokens`, public. Chaque entrée donne `assetId`, `decimals`,
  `blockchain`, `symbol`, `price`, `priceUpdatedAt`, `contractAddress`
  ([doc](https://docs.near-intents.org/integration/distribution-channels/1click-api/quickstart/making-a-request)). La
  doc conseille de relire la liste avant chaque mise en production.
- **TIERS.** Format des identifiants : `nep141:eth-0x….omft.near` ([FastNear](https://js.fastnear.com/intents)),
  `nep141:doge.omft.near` ([Aurora](https://docs.intents.aurora.dev/intents-swap/supported-assets)),
  `nep141:sol-<mint>.omft.near` (un projet GitHub orienté Solana, source exacte non isolée par la recherche).
- **TIERS.** Taille du catalogue : 216 actifs ([PR lintel](https://github.com/DaviRain-Su/lintel/pull/15), non datée) ou
  170 actifs sur 34 réseaux via le pont ([PR Liberdus](https://github.com/Liberdus/web-client-v2/pull/1713)).

**INFÉRENCE, importante pour le produit.** Avec environ 200 actifs toutes chaînes confondues, les memecoins disponibles
sont forcément peu nombreux. Le catalogue de cartes doit être choisi à partir de cette liste. On ne peut pas proposer
n'importe quel memecoin récent, ni s'appuyer sur un flux de type pump.fun.

Le symbole ne suffit pas : il faut comparer l'adresse de contrat (mise en garde d'un projet tiers, même réserve sur la
source). Un identifiant NEP-245 est une
chaîne opaque ([PR Anchorage](https://github.com/anchorageoss/visualsign-parser/pull/479)).

### Memecoins précis

| Token | Statut | Ce qui a été trouvé |
|---|---|---|
| DOGE (natif) | **Probable**, TIERS + DOC pour la chaîne | `nep141:doge.omft.near` dans le [tableau d'Aurora](https://docs.intents.aurora.dev/intents-swap/supported-assets) |
| PEPE (Ethereum) | NON VÉRIFIÉ, plutôt oui | Présent dans le tableau Aurora, identifiant non confirmé ; cité par [NEAR Treasury](https://docs.neartreasury.com/payments/intents) et [NEAR Mobile](https://swap.nearmobile.app/) |
| SHIB (Ethereum) | NON VÉRIFIÉ, plutôt oui | Deux lectures contradictoires du tableau Aurora ; cité par NEAR Mobile |
| WIF, BOME (Solana) | NON VÉRIFIÉ | Une lecture du tableau Aurora les montre, une autre non |
| TRUMP | NON VÉRIFIÉ | Seulement [un site non officiel](https://trump-swap.org/) |
| BONK, FARTCOIN | NON VÉRIFIÉ | Rien trouvé. Ne vaut pas absence |
| Memecoins sur Base, BNB, Monad | NON VÉRIFIÉ | Rien trouvé |

### Montants minimums

- **NON VÉRIFIÉ pour les valeurs.** Je n'ai pas de table par token.
- **TIERS.** Les minimums par token viennent de `supported_tokens` du pont
  ([PR Liberdus](https://github.com/Liberdus/web-client-v2/pull/1713)).
- **TIERS.** 1Click refuse un montant trop petit sous plusieurs formes : un plancher en unités de base, ou une limite
  temporaire en dollars (100 $ dans [ce cas](https://github.com/MFrancis-dev/settle/issues/135)). Exemple de minimum
  observé : 1,31 USDC de Base vers Hyperliquid ([Trezu #1876](https://github.com/NEAR-DevHub/trezu/issues/1876)).
- **TIERS.** Un guide tiers annonce 1 000 DOGE de minimum (source exacte non isolée). À contrôler.
- **DOC probable.** Les très petits dépôts (exemple : 5 000 sats) sont traités à part, comme de la poussière, avec des
  délais possibles (remonté avec les pages de FAQ et de doc Intents, page exacte non isolée).

**INFÉRENCE.** C'est le principal risque de conception. Une carte adossée à 1 $ peut être impossible à retirer si le
minimum du pont ou ses frais sont du même ordre. Le montant minimum d'une carte doit venir du minimum de retrait du
token, avec une marge, et non du prix du booster.

### Slippage, délais, types de swap (DOC)

- `slippageTolerance` en points de base, 100 = 1 %
  ([doc](https://docs.near-intents.org/integration/distribution-channels/1click-api/quickstart/making-a-request)).
- `dry: true` est un aperçu sans `depositAddress`. `dry: false` engage le devis et renvoie l'adresse de dépôt.
- `deadline` : passé ce moment, le remboursement peut commencer. `timeWhenInactive` n'est renvoyé qu'avec `dry: false`
  ([SDK](https://docs.near-intents.org/integration/distribution-channels/1click-api/sdk)).
- `depositType` : `ORIGIN_CHAIN`, `INTENTS`, `CONFIDENTIAL_INTENTS`. `recipientType` : `DESTINATION_CHAIN`, `INTENTS`,
  `CONFIDENTIAL_INTENTS`. `refundType` : `ORIGIN_CHAIN` ou `INTENTS`.
- `EXACT_INPUT` : dépôt insuffisant remboursé à l'échéance, excédent remboursé à `refundTo`
  ([Swap Types](https://docs.near-intents.org/integration/distribution-channels/1click-api/swap-types)). `ANY_INPUT` est
  à éviter ici : pas de remboursement, nouvel essai toutes les 5 minutes, réservé aux partenaires.

### Frais

| Frais | Valeur | Statut |
|---|---|---|
| Protocole, sur chaque transfert | 0,0001 % | DOC, [Fees](https://docs.near-intents.org/resources/fees) |
| Sans clé API | +0,25 % | DOC, [API Keys](https://docs.near-intents.org/integration/distribution-channels/1click-api/authentication) |
| Avec clé API | en général 0,20 % ; 0,01 % sur stablecoins et routes même actif | DOC, même page |
| `appFees` avec clé | partage 50/50, 1Click garde au moins 0,20 % | DOC, [Fee Configuration](https://docs.near-intents.org/integration/distribution-channels/1click-api/fee-config) |
| Retrait NEAR, ZEC, STRK vers Solana | 0,1 % | DOC, [Fees](https://docs.near-intents.org/resources/fees) |
| Frais de pont au retrait | variable ; 0,0024 USDC vers Base observé sur 0,01 USDC | TIERS, [Trezu #1924](https://github.com/NEAR-DevHub/trezu/issues/1924) |

D'anciennes sources donnent 0,1 % ou 0,2 % sans clé. La doc actuelle prime.

### Modes de panne

| Panne | Statut | Source |
|---|---|---|
| Statuts : `PENDING_DEPOSIT`, `KNOWN_DEPOSIT_TX`, `PROCESSING`, `INCOMPLETE_DEPOSIT`, puis `SUCCESS`, `REFUNDED`, `FAILED` | DOC | [Status](https://docs.near-intents.org/api-reference/oneclick/check-swap-execution-status) |
| Aucun solveur ne cote un token : pas de devis, donc pas de swap. Les solveurs sont la seule source de prix | TIERS, article explicatif, source exacte non isolée ; aucun message d'erreur officiel trouvé | Recherche sur la liquidité des solveurs |
| Swap bloqué en `PROCESSING` depuis plus de 20 jours, sans remboursement | TIERS, rapport isolé | [near/intents #399](https://github.com/near/intents/issues/399) |
| Dépôt mal routé, API à `SUCCESS`, sans remboursement (swaps confidentiels) | TIERS, rapport isolé | [near/intents #384](https://github.com/near/intents/issues/384) |
| Plusieurs `ft_withdraw` dans une même transaction NEAR : seul le premier arrive, les autres quittent le solde | TIERS, 2 essais sur 2, vers Base, signalé le 9 nov. 2026 | [Trezu #1924](https://github.com/NEAR-DevHub/trezu/issues/1924) |
| Shield suspend dépôts, retraits, ou les deux sur un réseau ou un pont, ainsi que les swaps qui y passent | DOC | [Shield Status](https://partners.near-intents.org/shield/status) |
| Attaque du 1er oct. 2026 : environ 3,8 M$ de solde sans contrepartie, service suspendu, 11 réseaux coupés selon une source, fonds rendus en 36 h selon le projet | TIERS, presse concordante | [The Block](https://www.theblock.co/news/ecosystems/2026-10-01-near-intents-halts-services-after-3-8-million-exploit-promises-full-compensation-417404), [The Defiant](https://thedefiant.io/news/security/near-intents-postmortem-links-3-8-million-exploit-to-deposit-bug) |

**NON VÉRIFIÉ.** Je n'ai trouvé aucune description officielle de ce qui se passe si le prix passe sous `minAmountOut`
après le dépôt. Le statut `REFUNDED` existe, mais aucune source ne garantit en toutes lettres ce remboursement.

## 2. Comment garder les tokens

Trois options, qui ne s'excluent pas : le registre des cartes reste de toute façon dans notre contrat.

- **A. Solde NEP-245 sur `intents.near`.** Notre contrat est le titulaire du solde.
- **B. Coffre NEP-141.** Les tokens pontés sortent d'Intents et restent sur le compte du contrat.
- **C. Chain Signatures.** Le contrat dérive une adresse sur chaque chaîne et y détient les vrais tokens.

| Critère | A. Solde `intents.near` | B. Coffre NEP-141 | C. Chain Signatures |
|---|---|---|---|
| **Achat à l'ouverture** | Devis `INTENTS` vers `INTENTS`, le contrat paie par `mt_transfer`. Pas de transaction sur l'autre chaîne | Comme A, plus un `ft_withdraw` vers le contrat | 1Click livre sur l'adresse dérivée, ou le contrat signe un swap local (Jupiter, Uniswap) : du code par chaîne |
| **Comptabilité par carte** | Dans notre contrat : `carte -> (token, montant)`. Le grand livre d'Intents ne connaît que le total | Idem | Idem, mais le contrat ne voit pas les soldes distants |
| **Retrait vers la chaîne d'origine** | Appel direct `ft_withdraw` ou `mt_withdraw`. Pas de relais si le format de mémo tient | Il faut repasser par Intents ou par le pont : parcours non documenté | Transaction signée par le MPC, diffusée par n'importe qui. Il faut du gaz sur chaque chaîne |
| **Exécution partielle** | Devis indépendants : un booster de 5 cartes peut réussir à 4 sur 5 | Idem | Idem, plus les échecs propres à chaque chaîne |
| **Prix entre paiement et exécution** | Plancher `minAmountOut`, créditer ce plancher | Idem | Pas de plancher 1Click si swap local : à coder dans la transaction |
| **Audit des réserves** | `mt_batch_balance_of` lisible par tous **et par le contrat** | `ft_balance_of`, idem | Public sur chaque chaîne, **illisible depuis NEAR** sans oracle |
| **Confiance ajoutée** | Contrat Verifier, pont (PoA, HOT ou Omni) | Pont seulement, moins le grand livre | Réseau MPC seulement |
| **Effort hackathon** | Faible | Moyen | Élevé |

Faits d'appui :

- **DOC.** Les dépôts se font par `ft_transfer_call` vers `intents.near`, le `msg` désignant le titulaire. Un compte nommé
  peut recevoir sans clé enregistrée
  ([Deposits](https://docs.near-intents.org/integration/verifier-contract/deposits-and-withdrawals/deposits),
  [Account Abstraction](https://docs.near-intents.org/integration/verifier-contract/account-abstraction)).
- **DOC.** Lecture des soldes par `mt_batch_balance_of`, retrait direct par `ft_withdraw`, `nft_withdraw`, `mt_withdraw`,
  avec 1 yoctoNEAR. Ne pas mettre de `msg`, sinon la protection de remboursement saute
  ([Withdrawals](https://docs.near-intents.org/integration/verifier-contract/deposits-and-withdrawals/withdrawals)).
- **TIERS.** La destination hors NEAR passe par un mémo `WITHDRAW_TO:<adresse>` ou par un message de pont
  ([wheres-my-swap](https://github.com/cryppit/wheres-my-swap)). **Format exact non vérifié.**
- **TIERS.** Le PoA paie depuis un portefeuille géré par un opérateur (même source). C'est donc une garde centralisée.
- **DOC.** Chain Signatures : `v1.signer`, ECDSA pour Ethereum, EdDSA pour Solana, l'adresse dépend du compte appelant et
  du chemin. Le compte distant a besoin de ses propres jetons pour le gaz
  ([doc](https://docs.near.org/chain-abstraction/chain-signatures/implementation)). Le coût exact d'une signature reste
  **non vérifié**. Latence de 7 à 25 s mesurée sur testnet par un seul projet.

**INFÉRENCE.** Le créditage ne doit pas reposer sur une différence de solde avant/après, ambiguë dès que deux achats du
même token se chevauchent. Plus simple :

1. La carte est créditée de `minAmountOut`, le montant signé.
2. Avant de créer la carte, le contrat lit `mt_batch_balance_of` et exige
   `solde >= engagements du token + minAmountOut`.
3. Le surplus éventuel reste une marge du protocole, visible de tous.

D'après la presse sur le post-mortem d'octobre (TIERS, article exact non isolé), la surveillance d'Intents comparait
seulement les totaux entre chaîne d'origine et NEAR, sans confronter les soldes internes aux tokens détenus. C'est
précisément le contrôle à ne pas omettre chez nous.

## 3. Qui déclenche l'achat

### Un contrat ne peut pas appeler 1Click seul

**INFÉRENCE (connaissance générale, pas de phrase officielle trouvée).** Un contrat NEAR s'exécute de façon déterministe
et ne fait pas de requête HTTP. Un acteur hors chaîne doit demander le devis.

**DOC.** Un contrat n'a pas de clé privée, or les intents signés exigent une clé enregistrée
([Account Abstraction](https://docs.near-intents.org/integration/verifier-contract/account-abstraction)). La proposition
[NEP-641](https://github.com/near/NEPs/blob/master/neps/nep-0641.md) vise ce manque, mais reste une proposition.

**Piège.** Un contrat pourrait appeler `add_public_key` pour lui-même. Quiconque détient cette clé contrôlerait alors
tout le solde. Le contrat ne doit jamais le faire, et on doit pouvoir le constater publiquement (`has_public_key`).

### Le schéma qui fonctionne : relais sans pouvoir sur les fonds

Le projet [autonomous-trading-account, PR #186](https://github.com/beneviolabs/autonomous-trading-account/pull/186) décrit
exactement ce qu'il nous faut (**TIERS**, fusion et déploiement non vérifiés) :

1. Le relais obtient un devis 1Click signé (`dry: false`) et le passe au contrat.
2. Le contrat vérifie la signature de 1Click, la validité du devis, le destinataire et le remboursement (lui-même), les
   types `INTENTS`, un plafond de slippage de 2 %, l'échéance.
3. Le contrat appelle `intents.near::mt_transfer` vers `depositAddress`, pour `amountIn`.

Réserves :

- **NON VÉRIFIÉ.** Le format de signature des devis et la clé publique à utiliser : vus dans cette PR seulement.
- **TIERS.** Un audit communautaire signale que la `deadline` de la requête n'est **pas** couverte par la signature, alors
  que `minAmountOut` l'est (source exacte non isolée par la recherche). Le contrat doit donc vérifier l'échéance autrement.
- **TIERS.** La revue de cette PR signale une clé de test dérivée d'une graine publique, acceptée dans certains builds.

### Ce que le relais peut encore faire

| Pouvoir du relais | Conséquence | Parade |
|---|---|---|
| Ne rien faire ou tarder | Booster bloqué | Délai au bout duquel l'acheteur est remboursé. Plusieurs relais possibles |
| Choisir un mauvais moment ou un mauvais devis | Moins de tokens, dans la limite du slippage | Plafond de slippage. Montant minimum par carte fixé à l'avance |
| Détourner les fonds | Impossible si le contrat vérifie destinataire et remboursement | Tests sur ces vérifications |
| Détenir la clé API 1Click | Fuite : perte de la remise, pas des fonds | Secret côté relais |

**INFÉRENCE.** Sans oracle de prix, le contrat ne sait pas si un devis est juste. Le montant minimum attendu par carte,
fixé à la création de la série, sert de garde-fou grossier.

Confiance qui reste quel que soit le relais : le service 1Click, opérateur centralisé, les solveurs, le Verifier, les ponts.

**Pour plus tard.** OutLayer permet à un contrat de demander un calcul hors chaîne par yield/resume, dans une enclave
TDX ([doc NEAR](https://docs.near.org/primitives/off-chain-compute/outlayer)). Cela réduirait la confiance dans le relais.
Un projet tiers rappelle que son dépôt ne vérifiait que la clé du worker, pas l'attestation
([sealed](https://github.com/edycutjong/sealed)). Non testé ici.

### Machine d'états d'un achat (INFÉRENCE)

Une carte n'est créée qu'après livraison confirmée :

`PAYÉ` puis, pour chaque ligne, `COTÉ`, `ENVOYÉ`, et enfin `LIVRÉ`, `REMBOURSÉ` ou `BLOQUÉ`.

- **Livré :** contrôle de couverture réussi, carte créée.
- **Remboursé :** le jeton de paiement est revenu sur le solde Intents du contrat, l'acheteur le récupère.
- **Bloqué :** l'échéance est passée et rien n'est revenu. On ne rembourse pas tant que l'argent n'est pas revenu, sinon
  un swap tardif ferait perdre le protocole (voir le cas de 20 jours en `PROCESSING`).

### Destruction de la carte, token retiré ou sans liquidité

**INFÉRENCE, point clé.** Rendre la carte ne vend rien : on retire le token sous-jacent. **L'absence d'acheteurs ne bloque
donc pas le retrait.** La liquidité compte à l'achat et pour une éventuelle option « vendre contre USDC ». Ce qui compte au
retrait, c'est le pont.

| Situation | Effet attendu | Statut |
|---|---|---|
| Token retiré de `/v0/tokens` | Plus de devis 1Click. Le solde reste dans le grand livre. Retrait direct peut-être possible | NON VÉRIFIÉ, aucune politique de retrait de liste trouvée |
| Pont ou réseau suspendu par Shield | Retrait impossible pendant la suspension | DOC pour la suspension |
| Aucune liquidité | Pas de nouveaux boosters avec ce token ; retrait non concerné | INFÉRENCE |
| Frais de pont supérieurs à la valeur de la carte | Carte de fait impossible à retirer sur l'origine | INFÉRENCE |
| Émetteur qui gèle ou bloque le token (autorité de gel Solana, liste noire ERC-20) | Retrait impossible ou token sans valeur | INFÉRENCE |

Parades proposées (INFÉRENCE) :

- Passer la carte à `RETRAIT_EN_COURS` et ne la détruire que dans le rappel de réussite. Sinon, la restaurer.
- Offrir une sortie de secours **sur NEAR** : `mt_transfer` vers le compte Intents de l'utilisateur, ou `ft_withdraw` vers
  son compte NEAR. Elle ne dépend d'aucun pont.
- Une carte par transaction NEAR, à cause du bug de retraits groupés.
- Un retrait réussi sur NEAR ne prouve pas la livraison sur l'autre chaîne : Trezu a vu le solde débité sans arrivée. Le
  site doit suivre la livraison et le dire.
- L'adresse de destination est vérifiée au mieux côté site. Le contrat ne valide pas pleinement une adresse étrangère, et
  une erreur peut être définitive.
- NEP-171 ne définit pas de destruction standard (INFÉRENCE) : méthode propre, à documenter, avec événement.

## 4. Démonstration sans testnet

**DOC.** Intents n'a pas de testnet et n'en prévoit pas. La doc conseille le mainnet, des comptes dédiés et de petits
montants ([FAQ](https://docs.near-intents.org/near-intents/faqs),
[premier swap](https://docs.near-intents.org/getting-started/first-swap)).

Il existe des bacs à sable communautaires, sans lien officiel : [Tidepool](https://github.com/Watchmeecryt/tidepool) imite
1Click. D'autres projets écrivent un faux `intents.near` ([setllend](https://github.com/TarasBrilian/setllend/pull/18)).

La démonstration la moins chère et honnête tient en trois niveaux, à annoncer tels quels :

| Niveau | Contenu | Ce que cela prouve | Coût |
|---|---|---|---|
| 1. Catalogue réel | `/v0/tokens` et devis `dry: true` pour chaque carte, minimums et prix affichés en direct | Les routes existent aujourd'hui. **Pas** l'exécution | Nul |
| 2. Contrat sur testnet + faux Verifier | Vrais NFT, machine d'états, plafonds, échecs simulés (remboursement, blocage, surplus). Marqué « simulation » à l'écran | La logique de garde, surtout les cas d'échec | Nul |
| 3. Preuve mainnet unique | 1 booster, 2 ou 3 cartes, 1 destruction vers Solana ou Base, sur un compte dédié. Liens vers les transactions | Le trajet complet, une fois | À chiffrer avec les devis ; prévoir quelques dizaines de dollars tant que les minimums ne sont pas connus |

À ne pas faire : présenter un devis `dry: true` comme un achat, ou le faux Verifier comme Intents.

## Architecture recommandée

**Option A, avec relais sans pouvoir sur les fonds.**

1. **Catalogue.** Liste figée de tokens issue de `/v0/tokens`, contrôlée par adresse de contrat, en retenant ceux dont
   le retrait fonctionne et dont le minimum est compatible avec la carte. Priorité aux tokens d'une même chaîne, Solana ou
   Ethereum selon ce que la liste montre.
2. **Contrat de boosters.** NEP-171 et registre `carte -> (token, montant)`. Le contrat est titulaire du solde sur
   `intents.near`, n'enregistre jamais de clé, et son code est vérifiable (pas de clé d'accès complète après le gel).
3. **Paiement.** USDC ou wNEAR déposé sur `intents.near` au nom du contrat.
4. **Achat.** Relais qui fournit les devis signés, `EXACT_INPUT`, `INTENTS` vers `INTENTS`, `refundType: INTENTS`. Le
   contrat vérifie tout puis paie par `mt_transfer`.
5. **Création.** Carte créée à la livraison confirmée, créditée de `minAmountOut`, après contrôle de couverture.
6. **Retrait.** Destruction, `ft_withdraw` ou `mt_withdraw` direct sans relais, une carte par transaction, restauration si
   échec, sortie de secours sur NEAR.
7. **Transparence.** Page publique comparant, token par token, les soldes `intents.near` et la somme des cartes.

Chain Signatures reste à écarter pour le hackathon : un code par chaîne, du gaz partout, et des réserves que le contrat ne
peut pas lire. À reconsidérer ensuite pour réduire la dépendance aux ponts.

## Risques ouverts

| # | Risque | Gravité | Comment le lever |
|---|---|---|---|
| 1 | Memecoins réellement disponibles inconnus | Bloquant | Lire `/v0/tokens` |
| 2 | Minimum et frais de retrait supérieurs à la valeur d'une carte | Bloquant | `supported_tokens`, devis réels, puis fixer la valeur minimale des cartes |
| 3 | Format de retrait contrat vers chaîne d'origine (`WITHDRAW_TO`, pont par token) seulement connu par des tiers | Élevée | Lire `near/intents` et l'Intents SDK, puis un retrait mainnet minuscule |
| 4 | Signature des devis non documentée à notre connaissance, `deadline` non couverte | Élevée | Lire la référence API et la PR #186, tester sur un vrai devis |
| 5 | Un contrat qui appelle `mt_transfer` : seul un projet tiers le montre | Élevée | Test mainnet minuscule, lecture de `contracts/defuse` |
| 6 | La fonction de notification de dépôt a été retirée après l'attaque ; la doc des dépôts (`execute_intents`, `refund_if_fails`) peut être périmée | Moyenne | Lire le post-mortem d'origine et les versions de `near/intents` |
| 7 | Bug de retraits groupés, testé seulement vers Base | Moyenne | Une carte par transaction, essai sur la chaîne retenue |
| 8 | Dépendance à un opérateur : PoA centralisé, 1Click, Shield peut suspendre un réseau | Inhérente | L'annoncer clairement, proposer la sortie sur NEAR |
| 9 | Swaps bloqués sans remboursement | Moyenne | État `BLOQUÉ`, pas de remboursement anticipé, réserve dédiée |
| 10 | Token gelé, abandonné, ou retiré de la liste | Moyenne | Écarter les tokens à autorité de gel ; politique de retrait de liste à demander à l'équipe Intents |
| 11 | Booster aléatoire adossé à des memecoins : qualification juridique (jeu de hasard, offre d'actifs) | À évaluer | Hors de cette recherche, à faire regarder avant tout lancement public |
