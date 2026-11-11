# Faisabilité technique de Memaster (hors burn)

Vérification du 11 novembre 2026, en lecture seule : aucune transaction, aucune clé, aucun compte créé. Ce document
complète `wallets-et-alea.md` et sert à cocher les tests 1.2, 1.3 et 1.7 de `plan.md`. Le burn est volontairement
laissé de côté.

**Méthode.** Lecture du code source (nearcore `master` au commit `45c2bbd` du 10/11/2026, `azbang/near-connect`,
`gagdiez/eth-wallet`), des spécifications NEP, et appels RPC publics sur mainnet (`rpc.mainnet.near.org`,
`rpc.mainnet.fastnear.com`, `archival-rpc.mainnet.fastnear.com`, API FastNear). La recherche web n'a servi qu'aux
tarifs d'hébergement : le quota de recherche était épuisé, d'où des tarifs lus directement sur les pages de prix et
les API de prix.

| Statut | Sens |
| --- | --- |
| **[Code]** | Vérifié dans le code source, chemin et commit cités |
| **[RPC]** | Vérifié par appel RPC public sur mainnet le 11/11/2026 |
| **[Doc]** | Documentation ou spécification officielle |
| **[Tiers]** | Source tierce : page de prix, site d'un acteur |
| **[A]** | Analyse de notre part, déduite des points vérifiés |
| **[NV]** | Non vérifié |

## Verdict global

**Faisable.** Rien de ce qui a été vérifié ne bloque le produit (boosters payés en NEAR, cartes NEP-171, tirage sur
plusieurs reçus, MetaMask, marché intégré).

- **MetaMask : viable comme wallet principal.** L'adaptateur est dans le manifeste en ligne de near-connect, le
  relais tourne sur mainnet et des comptes `0x…` font des appels avec dépôt tous les jours. Un seul point n'a pas été
  observé directement : un `nft_transfer`. Le même contrôle d'1 yocto a en revanche été observé sur `ft_transfer_call`.
  Reste à faire tourner la checklist manuelle ci-dessous.
- **Aléa : le tirage sur 3 reçus chaînés tient.** Chaque reçu créé par un contrat s'exécute au plus tôt au bloc
  suivant, avec une valeur aléatoire de bloc nouvelle. La graine change aussi d'un reçu à l'autre et d'une action à
  l'autre.
- **Ce qui change par rapport à la recherche précédente :**
  - la limite de gaz est passée à **1 PGas** (et non plus 300 Tgas), mais la voie MetaMask reste plafonnée à
    **270 Tgas** pour l'ensemble de la chaîne de reçus ;
  - le gaz est maintenant **prépayé à 0,001 NEAR/Tgas**, dix fois le prix brûlé : un compte `0x…` doit avoir environ
    0,3 NEAR de marge en plus du prix du booster ;
  - **Paras vide ses contrats de marché** ; TradePort est le seul marché encore actif, avec peu de volume.

## 1. MetaMask sur NEAR

### 1.1 near-connect a-t-il toujours un adaptateur Ethereum ?

**Oui [Code] [RPC].**

- Le dépôt actif est `github.com/azbang/near-connect` (paquet npm `@hot-labs/near-connect`, version 0.12.0 du
  26/10/2026, dernier commit le 07/11/2026). Le dépôt `near/near-connect` n'existe pas.
- L'adaptateur a été ajouté par la PR #103 (`gagdiez/eth-wallets`, « feat: add EVM wallet support »), fusionnée le
  08/10/2026. L'entrée `ethereum-wallets` (version 0.1.4) figure toujours dans `repository/manifest.json` au dernier
  commit. Ses capacités :
  - `signAndSendTransaction` et `signAndSendTransactions` : oui ;
  - `signMessage`, `signDelegateActions` et `signInWithFunctionCallKey` : non ;
  - mainnet et testnet : oui.
- near-connect charge par défaut ses manifestes depuis deux adresses (`src/NearConnector.ts`, lignes 56 et 57) :
  `raw.githubusercontent.com/hot-dao/near-selector/…/manifest.json` et `cdn.jsdelivr.net/gh/azbang/hot-connector/…`.
  Toutes deux servent le manifeste 1.1.0 avec `ethereum-wallets` 0.1.4 **[RPC, HTTP]**. MetaMask apparaît donc sans
  configuration.
- L'adaptateur chargé dans le bac à sable est `https://evm-on-near.dev/executor.js`, servi le 11/11 (en-tête
  `last-modified` du 08/10/2026). C'est un script court : il ouvre une fenêtre `evm-on-near.dev`, qui parle à
  MetaMask via Reown AppKit. Son code source est `github.com/gagdiez/eth-wallet` (dernier commit le 08/10/2026).
- Limites lues dans `gagdiez/eth-wallet` (`src/encoding.ts`, `README.md`) :
  - **une action par transaction** : `encodeTransactions` lève une erreur si `actions.length !== 1` ;
  - **gaz plafonné à 270 Tgas** par appel (`MAX_GAS`) : le relais impose 300 Tgas et garde 30 Tgas pour le contrat
    portefeuille ;
  - pas de clé d'accès complet, pas de NEP-413, pas d'actions déléguées ;
  - si l'application demande `addFunctionCallKey` à la connexion, l'option est **ignorée** : chaque transaction
    demande donc une approbation dans MetaMask ;
  - il faut autoriser les **fenêtres pop-up**, et le navigateur doit gérer Web Locks.

### 1.2 Le contrat de portefeuille eth-implicit est-il actif sur mainnet ?

**Oui [RPC] [Code].**

- **Protocole mainnet : version 88**, nœuds en 2.14.0 (`status` sur les deux RPC). Dans nearcore `master`, la version
  stable est 89 (`core/primitives-core/src/version.rs`, `STABLE_PROTOCOL_VERSION = 89`). Elle n'est pas encore active
  sur mainnet.
- Depuis nearcore 2.11.0, les comptes `0x…` utilisent un **contrat global** (CHANGELOG 2.11.0 : « ETH implicit
  accounts now use a globally deployed contract »). Les identifiants mainnet sont dans
  `runtime/runtime/src/wallet_contract.rs` :

| Rôle | Hash | État mainnet |
| --- | --- | --- |
| Portefeuille actuel (protocole 88) | `2zodJZK2e4nnv5AqwCRnenNSmkikXhEd7PPY6BmfTmW4` | Déployé, 274 477 octets (`view_global_contract_code`) **[RPC]** |
| Nouvelle version, active au protocole 89 (`UpdatedEthWalletContract`) | `5LM8a65dWxesxZeWq3HjCcjLkNTwHjTUPp8R117wZJDw` | Déployé, 247 641 octets **[RPC]**. Remplacera l'ancien automatiquement au passage en 89 |
| Ancien « magic hash » mainnet | `77CJrGB4MNcG2fJXr87m3HCZngUMxZQYwhqGqcHSd7BB` | Héritage, redirigé vers le contrat global |

- **Relais mainnet** : `https://eth-rpc.mainnet.near.org` répond, avec `eth_chainId = 0x18d` (397, l'identifiant
  NEP-518 de mainnet). Le testnet `eth-rpc.testnet.near.org` répond `0x18e` (398). La méthode `near_getPublicKey`
  renvoie la clé du relais `ed25519:4RC4T7Kk9g7z1zbX6fppbGtFTgtsSfzC96SftbQedq5F` **[RPC]**.
- **Comptes réels** : l'API FastNear (`/v0/public_key/…/all`) liste **1 352 comptes** qui portent cette clé de relais.
  Deux comptes ont été vérifiés par `view_account` et `view_access_key_list` :

| Compte | Contrat | Clé du relais |
| --- | --- | --- |
| `0x8aea61ee7c1996f1a6c41601c8a5f8dda6d46835` | `code_hash = 1111…`, `global_contract_hash = 2zodJZ…` ; `view_code` renvoie bien le code de 274 477 octets | `FunctionCall`, méthode `rlp_execute` uniquement, sur le compte lui-même, `allowance: null` |
| `0xd45c07513dcc121b8af7d3f0c8dd2fe1484eb085` | Même contrat global | Même clé, mais avec une `allowance` de 0,248 NEAR |

- **Activité** : sur 496 de ces comptes analysés, 115 ont signé 1 944 transactions, dont 545 en septembre, 693 en
  octobre et 209 entre le 1er et le 11 novembre. La plus récente date du 11/11/2026 à 01h22 UTC **[RPC, API FastNear]**.
  La voie est donc vivante, avec un usage réel modeste.

### 1.3 Appel avec dépôt attaché et `nft_transfer` (1 yocto)

| Capacité | Réponse | Preuve |
| --- | --- | --- |
| Appel avec dépôt en NEAR | **Oui** | **[RPC]** `0xdcc200ce…` → `wrap.near::near_deposit`, dépôt de 1 322 NEAR, `SuccessValue` (tx `4AtzKHM1YMrV4VW5XUD5sckERtUD4p3bYXWKNHkuh8ph`, 30/10/2026). Un montant non rond passe aussi : 1,867605089672 NEAR (tx `AmGgp6c6…`, 07/11) |
| Appel avec exactement 1 yoctoNEAR | **Oui** | **[RPC]** `0x8aea…` → `ft_transfer_call` avec `deposit=1`, 180 Tgas, succès de bout en bout (tx `8DTphmEocruWKQMnKBkA88nsdJKyu9aV8eoJMY9o7uHF`, 28/10/2026) |
| `storage_deposit` de 0,00125 NEAR | **Oui** | **[RPC]** plusieurs transactions sur `wrap.near` et d'autres jetons |
| `nft_transfer` | **Très probablement** | **[A]** Pas observé dans l'échantillon, mais c'est un `FunctionCall` avec 1 yocto, soit exactement le cas de `ft_transfer_call` (même `assert_one_yocto`). L'encodeur traite tous les appels de la même façon : 1 yocto donne `value = 0` et `yoctoNear = 1` (`src/encoding.ts`). À confirmer avec la checklist |
| Mise en vente sur un marché externe (`nft_approve`) | Oui, en principe | **[A]** Même mécanisme : un appel avec dépôt de stockage |

**Ce qui coûte en pratique.**

- **Gaz prépayé à 0,001 NEAR/Tgas** **[Code] [RPC]** :
  - le gaz attaché est acheté à `max(prix courant, min_gas_purchase_price)` (`core/primitives/src/fees.rs`,
    ligne 548) ;
  - `min_gas_purchase_price = 1e9` yocto par unité de gaz (`EXPERIMENTAL_protocol_config`), alors que le gaz est brûlé
    au prix courant de 1e8 (`gas_price`) ;
  - un appel à 270 Tgas immobilise donc environ **0,3 NEAR** au départ, dont l'essentiel est remboursé.
- Le compte `0x…` doit donc détenir **prix du booster + stockage + environ 0,3 NEAR**.
- Si la clé du relais a une `allowance`, elle doit couvrir ce prépaiement, sinon la transaction est refusée **[A]**.
  C'est le cas d'anciens comptes, comme `0xd45c…` à 0,248 NEAR. Les nouveaux comptes créés par eth-wallet n'ont pas
  de limite (`allowance` non renseignée dans `AddKey`).
- La création du compte et l'ajout de la clé sont **payés par le relais** (transaction d'accueil à 1 wei, README
  d'eth-wallet). Les transactions suivantes sont payées par le solde NEAR du compte.

### 1.4 Conclusion et plan B

**MetaMask peut être le wallet principal [A].** Conditions :

1. **Achat en un seul appel.** `buy_pack` reçoit le prix et le stockage dans le même dépôt. Tout le travail qui suit
   (3 reçus de tirage et 5 mints) doit tenir dans **270 Tgas au total**, car le gaz des reçus enfants est pris sur
   celui de l'appel d'origine **[A]**.
2. **Pas de lot d'actions.** Mise en vente, achat sur le marché et transfert font chacun l'objet d'un appel séparé,
   donc d'une approbation par action.
3. **Alimenter le compte en NEAR.** Il faut un virement de NEAR natif vers l'adresse `0x…` : NEP-518 crée
   automatiquement le compte sur un `Transfer` **[Doc]**. Le parcours depuis Base ou Ethereum (test 1.3 du plan)
   reste **[NV]**.

**Plan B.**

- Garder near-connect tel quel : son sélecteur propose aussi HOT, Meteor, Intear et les autres. Le contrat ne fait
  aucune différence entre un compte `0x…` et un compte `.near` (identification par `predecessor_account_id`). Si
  l'adaptateur faillit le jour de la démo, on clique simplement sur un autre wallet, sans changer de code.
- **Risque calendrier.** Le passage au protocole 89 remplace le contrat portefeuille par la version `5LM8a…`. Il faut
  refaire la checklist après cette mise à jour si elle tombe pendant le hackathon. La date n'est pas connue **[NV]**.

### 1.5 Checklist de test manuel (15 minutes, navigateur avec MetaMask)

Prérequis : MetaMask installé, environ 1 NEAR disponible sur un wallet ou un exchange, Node.js installé. Les montants
sont minuscules, mais c'est mainnet : utiliser un compte MetaMask dédié.

1. **Lancer la page de test officielle** (2 min). C'est une petite application near-connect avec un formulaire
   d'appel libre :
   ```sh
   git clone https://github.com/gagdiez/eth-wallet && cd eth-wallet/example
   cp .env.example .env.local   # puis y mettre VITE_NEAR_NETWORK=mainnet
   npm install && npm run dev
   ```
   Ouvrir l'adresse affichée (`http://localhost:5173`) et **autoriser les pop-ups** pour ce site.
2. **Connexion** (2 min). Cliquer sur *Connect*, puis choisir *Ethereum Wallets* et *MetaMask*.
   - MetaMask doit proposer d'**ajouter le réseau « NEAR Protocol », chain ID 397** : accepter.
   - Noter l'adresse `0x…`.
   - Si le compte est nouveau, MetaMask demande une transaction de « setup » à **1 wei de gas price**, payée par le
     relais : la signer.
   - ✅ La page affiche `0x…` connecté.
3. **Alimenter le compte** (3 min). Envoyer **0,5 NEAR** natif sur l'adresse `0x…` (en minuscules) depuis un autre
   wallet NEAR ou un exchange qui accepte un compte NEAR implicite.
   - ✅ Sur `https://nearblocks.io/address/0x…`, le solde apparaît.
4. **Vérifier la clé du relais** (1 min). Sur nearblocks, onglet *Access keys*, une seule clé doit apparaître :
   `FunctionCall` vers le compte lui-même, méthode `rlp_execute`, *allowance* illimitée.
5. **Appel avec dépôt** (2 min). Dans la section *Call a NEAR contract* :
   - Contrat `wrap.near`, méthode `storage_deposit`, arguments `{}`, dépôt `0.00125`. Signer dans MetaMask.
   - ✅ « SuccessValue » dans le résultat.
   - Puis contrat `wrap.near`, méthode `near_deposit`, arguments `{}`, dépôt `0.01`.
   - ✅ Succès.
6. **Appel avec 1 yocto, le cas de `nft_transfer`** (2 min). Contrat `wrap.near`, méthode `near_withdraw`, arguments
   `{"amount":"5000000000000000000000"}`, dépôt `0.000000000000000000000001` (24 décimales, soit 1 yocto).
   - ✅ Succès. C'est le même contrôle `assert_one_yocto` que `nft_transfer`.
7. **`nft_transfer` réel** (3 min, si possible). Depuis un wallet NEAR habituel, envoyer une NFT quelconque au `0x…`.
   Puis, dans la page de test : contrat de la NFT, méthode `nft_transfer`, arguments
   `{"receiver_id":"<ton compte .near>","token_id":"<id>"}`, dépôt de 1 yocto.
   - ✅ La NFT revient. Sans NFT sous la main, refaire ce point sur notre contrat de test (test 1.7 du plan).
8. **Noter les résultats** dans `plan.md`, ligne 1.2 : les hash des transactions et le solde restant. Le solde doit
   avoir baissé d'environ 0,012 NEAR plus quelques millièmes de gaz ; le prépaiement de 0,03 NEAR par appel à 30 Tgas
   est remboursé.

**En cas d'échec :**

| Symptôme | Cause probable |
| --- | --- |
| « Popup blocked » | Autoriser les pop-ups pour le site |
| « Not enough balance » | Pas assez de NEAR pour le prépaiement du gaz |
| « Wallet window closed » | Vérifier sur nearblocks avant de recommencer : la transaction est peut-être déjà passée |

## 2. Aléa

### 2.1 `env::random_seed()` change-t-il par reçu, par bloc, par action ?

**Par action, donc aussi par reçu et par bloc [Code], protocole 88 sur mainnet et `master`.**

La valeur aléatoire du bloc est calculée dans `core/primitives/src/utils.rs`, lignes 540 à 543 :

```rust
signer.compute_vrf_with_proof(prev_block_header.random_value().as_ref());
let random_value = hash(vrf_value.0.as_ref());
```

C'est le VRF du producteur du bloc sur la valeur aléatoire du bloc précédent. Elle est transmise au runtime telle
quelle (`chain/chain/src/chain_update.rs`, ligne 576 : `random_seed: *block_header.random_value()`).

La graine vue par le contrat est calculée dans `runtime/runtime/src/function_call.rs`, ligne 288 :

```rust
let random_seed = near_primitives::utils::create_random_seed(*action_hash, apply_state.random_seed);
```

avec, dans `core/primitives/src/utils.rs`, ligne 347 :

```rust
pub fn create_random_seed(action_hash: CryptoHash, random_seed: CryptoHash) -> Vec<u8> {
    // Since every action hash is unique, the seed will be unique per receipt and even
    // per action within a receipt.
    ... hash(action_hash || random_seed)
```

Enfin, `action_hash = create_action_hash_from_receipt_id(receipt_id, block_height, action_index)`
(`runtime/runtime/src/lib.rs`, ligne 1043).

Conséquences **[A]** :

- La graine est **identique pendant toute une exécution de méthode**. Deux appels à `env::random_seed()` dans le même
  appel renvoient la même valeur, ce qui confirme la doc near-sdk.
- Elle est **différente pour deux reçus du même bloc**. Le souvenir noté **[NV]** dans `wallets-et-alea.md` est
  donc confirmé.
- **Mais toute l'imprévisibilité vient de `random_value`.** `action_hash` est calculable à l'avance par n'importe qui :
  il découle de l'identifiant du reçu et de la hauteur. Deux reçus du même bloc ont des graines différentes, mais le
  producteur de ce bloc les connaît toutes les deux. Mélanger `pack_id` et le compte reste utile pour la vérification
  publique, pas pour la sécurité.
- **Vérifiable de l'extérieur.** `random_value` est dans l'en-tête de chaque bloc (RPC `block`, champ
  `header.random_value`), et `action_hash` se recalcule. Un vérificateur peut donc recalculer `random_seed`. Cela
  corrige le point **[NV]** de `wallets-et-alea.md` section 3, « Limite » **[A]**, sous réserve d'un test de
  recalcul.

### 2.2 Un callback ou un appel à soi-même s'exécute-t-il forcément dans un bloc ultérieur ?

**Oui pour tout reçu créé par un contrat, y compris vers lui-même [Code] [RPC]. Deux exceptions, sans effet ici.**

- Les reçus créés pendant l'exécution (`new_receipts`) passent par `receipt_sink.forward_or_buffer_receipt`. Ce sont
  des reçus sortants, intégrés au chunk suivant (`runtime/runtime/src/lib.rs`, lignes 1272 et suivantes ;
  `congestion_control.rs`, ligne 158). Rien n'est exécuté dans le même bloc, même vers le même compte. Sous
  congestion, un reçu peut être retardé de plusieurs blocs, jamais avancé.
- **Exception 1 : les reçus locaux.** Seul le reçu issu *directement d'une transaction* dont signataire et
  destinataire sont égaux s'exécute dans le même bloc (`lib.rs`, ligne 2351 : `if receipt.receiver_id() == signer_id`
  donne `local_receipts`). Avec MetaMask, c'est le cas de `rlp_execute`, exécuté sur le `0x…` lui-même. Notre
  `buy_pack` arrive donc au bloc suivant.
- **Exception 2 : `DeleteAccount`.** Une promesse avec une seule action `DeleteAccount` s'exécute juste après le reçu
  qui l'a créée (CHANGELOG 2.11.0). Sans objet pour nous.
- **Mesure réelle [RPC]** sur la tx `8DTphm…` :

| Hauteur | Reçu | Producteur |
| --- | --- | --- |
| 221971089 | `rlp_execute` | `astro-stakers` |
| 221971090 | `ft_transfer_call` | `aca87218…` |
| 221971091 | `ft_on_transfer` | `stake1` |
| 221971092 | callback du contrat vers lui-même | `here` |
| 221971093 | `rlp_execute_callback` | `svrn` |

  Un bloc par saut, environ 0,55 s par bloc, et une valeur `random_value` différente à chaque bloc. Dans cet exemple,
  les producteurs sont tous différents.

### 2.3 Conclusion pour un tirage sur 3 reçus chaînés

**La conception de `wallets-et-alea.md` tient [A].**

- `buy_pack` au bloc N, puis 3 reçus internes `#[private]` aux blocs N+1, N+2 et N+3 au minimum. Chacun voit une
  `random_value` nouvelle, produite par le VRF du producteur de son bloc. Ce producteur n'est pas forcément différent
  d'un bloc à l'autre : l'attribution est tirée au poids du stake (`epoch_info.rs`, `block_producers_sampler`).
- Pour biaiser le résultat, il faut contrôler le **dernier** bloc de la chaîne et accepter de ne pas le produire. Un
  gros validateur peut produire deux blocs consécutifs, mais il ne connaît pas la valeur des blocs suivants avant que
  le précédent soit produit.
- **3 reçus suffisent pour un hackathon.** Au-delà, chaque reçu coûte environ 0,5 s de latence et un peu de gaz.
- **Budget gaz.** Les 3 reçus et les 5 mints doivent tenir dans les 270 Tgas attachés par MetaMask. Il faut fixer le
  gaz de chaque reçu dans le contrat, et refuser `buy_pack` si `env::prepaid_gas()` est insuffisant **[A]**.

## 3. Limites du protocole (mainnet, protocole 88)

Valeurs lues par `EXPERIMENTAL_protocol_config` le 11/11/2026 **[RPC]**, identiques à
`core/parameters/res/runtime_configs/parameters.yaml` **[Code]**.

| Paramètre | Valeur | Commentaire |
| --- | --- | --- |
| `max_total_prepaid_gas` (par transaction) | **1 000 Tgas = 1 PGas** | CHANGELOG nearcore 2.11.0 : « Contract gas limit is increased from 300 TGas to 1 PGas » |
| `max_gas_burnt` (par appel de fonction, donc par reçu) | **1 PGas** | Idem |
| Gaz par chunk (`gas_limit`) | 1 PGas | Un reçu de 1 PGas remplit un chunk entier |
| **Plafond effectif avec MetaMask** | **270 Tgas** pour l'appel, 300 Tgas pour la transaction du relais | `gagdiez/eth-wallet/src/encoding.ts`, `MAX_GAS` **[Code]** |
| Prix du gaz brûlé | 1e8 yocto/gaz = **0,0001 NEAR/Tgas** | RPC `gas_price` |
| Prix d'achat minimal du gaz | 1e9 yocto/gaz = **0,001 NEAR/Tgas** | NEP-642, CHANGELOG 2.13.0, remboursé à l'écart près |
| `storage_amount_per_byte` | 1e19 yocto = **0,00001 NEAR par octet**, soit 1 NEAR pour 100 ko | Plus 40 octets comptés par entrée (`num_extra_bytes_record`) |
| `max_contract_size` | **4 194 304 octets (4 Mio)** | Un contrat global est aussi possible |
| `max_transaction_size` | 1 572 864 octets | |
| `max_arguments_length`, `max_length_storage_value`, `max_receipt_size` | 4 Mio chacun | |
| `max_total_log_length` | 16 384 octets par exécution | Limite pour les événements `nft_mint` et `pack_revealed` : 5 cartes passent largement |
| `max_actions_per_receipt` | 100 | |

### Coût estimé du mint de 5 NFT avec métadonnées [A]

Calcul sur le modèle `near-contract-standards`. Chaque entrée coûte clé + valeur + 40 octets.

| Entrée par carte | Octets environ |
| --- | --- |
| `owner_by_id` (id → `0x…` de 42 caractères) | 100 |
| `token_metadata_by_id` : titre, `media` et `reference` IPFS (environ 70 caractères chacun), `media_hash`, `reference_hash`, `extra` court | 450 à 550 |
| `tokens_per_owner` (ensemble itérable : 2 entrées) | 180 |
| Notre état : carte, rareté, quantité réservée | 100 |
| **Total par carte** | **830 à 930** |

- **Booster de 5 cartes**, avec l'enregistrement du booster d'environ 200 octets : 4,4 à 4,9 ko, soit **0,044 à
  0,049 NEAR (environ 0,17 $)**, bloqués sur le contrat tant que les cartes existent.
- **Recommandation** : exiger **0,06 NEAR** de stockage dans le dépôt, pour couvrir le pire cas.
- Pour réduire ce coût : ne garder sur la chaîne que `title`, `media`, `media_hash`, `reference` et
  `reference_hash`, et mettre le reste dans le JSON `reference`.
- **Gaz** : de l'ordre de 50 à 100 Tgas pour les 3 reçus et les 5 mints, soit 0,005 à 0,01 NEAR brûlés **[A]**.
- **À mesurer** au test 1.7 (sandbox ou testnet), avec `env::storage_usage()` avant et après.

## 4. Hébergement des images et métadonnées

Hypothèse : environ 1 000 images et 1 000 JSON de métadonnées. Tarifs lus le 11/11/2026.

| Option | Coût pour 1 000 cartes | Remarques | Statut |
| --- | --- | --- | --- |
| **Pinata**, offre gratuite | 0 $ | 1 Go, **500 fichiers**, 10 Go de bande passante, 1 passerelle. Avec 2 000 fichiers, il faut un dossier par CID ; la façon dont Pinata compte un dossier est **[NV]**. Offre Picnic à 20 $/mois, 1 To | **[Tiers]** [pinata.cloud/pricing](https://pinata.cloud/pricing) |
| **Filebase**, offre gratuite | 0 $ | 5 Go, **500 fichiers épinglés**, 10 Go de sortie IPFS. Pro à 7,50 $/mois, épinglage illimité | **[Tiers]** [filebase.com/pricing](https://filebase.com/pricing/) |
| **web3.storage / Storacha** | — | `storacha.network/pricing` redirige maintenant vers `fil.one`, un stockage S3 qui ne parle pas d'IPFS. **À éviter** | **[Tiers]** |
| **Arweave** (paiement direct ou Turbo) | Prix réseau : 14,21 AR par Gio, Turbo identique, avec AR à 3,26 $. **Images de 200 ko : environ 9 $. SVG de 5 ko : environ 0,25 $.** JSON : quelques centimes | Paiement unique, stockage permanent. La gratuité de Turbo sous 100 Kio n'a pas été confirmée : l'API de prix facture 100 Kio | **[RPC]** API `arweave.net/price` et `payment.ardrive.io`, cours Binance |
| **NEAR, état du contrat** | 0,00001 NEAR par octet : **images de 200 ko : 2 000 NEAR, environ 7 300 $**. **SVG de 3 ko : 30 NEAR, environ 110 $**, récupérables | Seul intérêt : un SVG génératif entièrement sur la chaîne. Les marchés attendent pourtant une URL dans `media`, d'où un `data:` URL de 3 ko par carte et plus de stockage par mint | **[RPC]** + **[A]** |

**Recommandation pour le hackathon [A].**

1. Générer les images en **SVG** (art abstrait génératif, voir `plan.md` 5.1) : quelques kilo-octets par carte.
2. Les publier sur **IPFS en deux dossiers**, un pour les images et un pour les JSON, chacun sous un seul CID, avec
   **Filebase gratuit** (5 Go) ou Pinata gratuit.
3. Renseigner `base_uri` sur la passerelle, et `media_hash` et `reference_hash` sur chaque carte.
4. Après le hackathon, copier les deux dossiers sur **Arweave** : moins de 5 $ pour du SVG, et un stockage permanent
   sans abonnement. Il suffit alors de changer `base_uri`, ou de passer par `nft_metadata_update`.

## 5. Marchés NFT NEAR fin 2026 et standards attendus

Complément à `wallets-et-alea.md` section 4. Activité mesurée par l'API FastNear (`/v0/account`, dernières 200
transactions) et par la lecture des transactions en archive **[RPC]**.

| Marché | Contrat | Situation au 11/11/2026 | Statut |
| --- | --- | --- | --- |
| **TradePort** | `market.tradeport.near` (613 NEAR, 9,4 Mo d'état) | **Le seul encore actif.** 171 636 transactions au total, 100 sur les 30 derniers jours, la dernière le 20/10/2026. Échantillon : surtout des mises en vente (`nft_on_approve`), 6 signataires sur 3 jours. Volume faible | **[RPC]** |
| **Paras** | `marketplace.paras.near`, `x.paras.near` | **En fermeture.** Le 21/10/2026, des centaines de transferts de solde vers `reserved.paras.near`, puis plus rien. Contrats réduits à environ 74 ko d'état et 1 NEAR | **[RPC]** |
| **Mintbase** | `simple.market.mintbase1.near`, `market.mintbase1.near` | Quasi à l'arrêt : 0 et 8 transactions sur 30 jours, la dernière le 17/10 | **[RPC]** |
| **Few and Far** | `market.fewandfar.near` | Mort : 1 transaction en 30 jours, un échec qui ressemble à du spam | **[RPC]** |
| **Apollo42** | `apollo42.near` | Mort : dernière transaction le 24/10/2025 | **[RPC]** |
| **Bitte** | `market.bitte.near` | Compte inexistant | **[RPC]** |

**Où les cartes seront vues.** Les wallets et explorateurs découvrent les NFT par les **événements NEP-297**
(`EVENT_JSON:` avec `standard: "nep171"`, `event: "nft_mint"`, `nft_transfer` ou `nft_burn`), indexés notamment par
FastNear. Exemple : `api.fastnear.com/v1/account/<compte>/nft` renvoie les contrats NFT détenus par un compte
**[RPC]**. Un mint sans événement `nft_mint` est invisible pour eux **[A]**.

**Standards à implémenter.** Statuts lus dans `near/NEPs`, branche `master` **[Doc]**.

| NEP | Statut | Ce que ça demande |
| --- | --- | --- |
| NEP-171 Core | Final, version 1.2.0 | `nft_transfer` et `nft_transfer_call` avec 1 yocto, `nft_token`, événements |
| NEP-177 Metadata | Final | `nft_metadata()`, `spec: "nft-1.0.0"`, `base_uri`, et par carte `media`, `media_hash`, `reference`, `reference_hash`, `extra`, `copies`. Le JSON `reference` prime en cas de conflit avec la chaîne |
| NEP-178 Approval | Final | Nécessaire pour TradePort : la mise en vente passe par `nft_approve` vers `market.tradeport.near` avec `msg = {"price", "market_type":"sale", "ft_token_id":"near"}` **[RPC]**, tx `FcaTipq1…` |
| NEP-181 Enumeration | Final | `nft_tokens_for_owner`, `nft_supply_for_owner`, `nft_total_supply` : utiles au front et aux indexeurs |
| NEP-199 Royalties | **Final**, ce qui corrige le **[P]** de `wallets-et-alea.md` | `nft_payout`, `nft_transfer_payout` : attendu par les marchés pour verser les redevances |
| NEP-297 Events | Final | Le format des événements ci-dessus |

**Conclusion [A].** Il n'y a pas de liquidité externe sur laquelle compter : il faut garder le **marché intégré au
contrat des cartes**. On expose quand même NEP-171, 177, 178, 181 et 199 avec les événements NEP-297, pour que
TradePort et les wallets affichent les cartes sans travail supplémentaire. Se faire lister sur TradePort relève de
leur procédure de collection **[NV]**.

## Sources principales

- **nearcore**, `master` au commit `45c2bbd` (10/11/2026) :
  - `core/primitives/src/utils.rs` : `create_random_seed`, calcul du VRF ;
  - `runtime/runtime/src/function_call.rs`, `lib.rs` et `congestion_control.rs` ;
  - `runtime/runtime/src/wallet_contract.rs` ;
  - `core/primitives/src/fees.rs` ;
  - `core/primitives-core/src/version.rs` ;
  - `core/parameters/res/runtime_configs/parameters.yaml` et `87.yaml` ;
  - `CHANGELOG.md` (2.11.0 à 2.14.0).
- **near-connect** : [github.com/azbang/near-connect](https://github.com/azbang/near-connect), commit `e71894f` du
  07/11/2026, PR #103 et `repository/manifest.json`.
- **eth-wallet** : [github.com/gagdiez/eth-wallet](https://github.com/gagdiez/eth-wallet), commit `d47756b` du
  08/10/2026, en particulier `src/encoding.ts`, `src/wallet.ts`, `src/networks.ts`, `README.md` et `example/`.
- **NEP** : [NEP-518](https://github.com/near/NEPs/blob/master/neps/nep-0518.md) (statut « New »),
  [NEP-171](https://github.com/near/NEPs/blob/master/neps/nep-0171.md), 177, 178, 181, 199, 297.
- **RPC mainnet** : `status`, `EXPERIMENTAL_protocol_config`, `gas_price`, `view_account`, `view_code`,
  `view_access_key_list`, `view_global_contract_code`, `block`, `EXPERIMENTAL_tx_status` ; relais
  `eth-rpc.mainnet.near.org` (`eth_chainId`, `near_getPublicKey`) ; API FastNear (`/v0/public_key`, `/v0/account`,
  `/v1/account/…/nft`).
- **Tarifs** : [Pinata](https://pinata.cloud/pricing), [Filebase](https://filebase.com/pricing/),
  [fil.one](https://fil.one/pricing), API `arweave.net/price` et `payment.ardrive.io/v1/price`, cours Binance (AR à
  3,26 $, NEAR à 3,65 $ le 11/11/2026).

## Non vérifié, à couvrir par les tests de la phase 1

- `nft_transfer` signé par MetaMask : checklist, point 7.
- Le coût exact en stockage et en gaz d'un booster : test 1.7.
- Alimenter un `0x…` depuis Base ou Ethereum : test 1.3.
- La date d'activation du protocole 89, qui changera le contrat portefeuille.
- Le recalcul externe de `random_seed` à partir de `random_value` et `action_hash` : à faire une fois dans le
  vérificateur public.
- La façon dont Pinata et Filebase comptent un dossier IPFS (un ou plusieurs fichiers).
