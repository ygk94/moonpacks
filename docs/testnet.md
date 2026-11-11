# Memaster sur NEAR testnet (11/11/2026)

Premier déploiement réel, **testnet uniquement** (aucun mainnet, aucun fonds réel). Les mesures sont confrontées aux
chiffres de la sandbox (`contract/README.md`). Script relançable : `contract/scripts/deploy_testnet.sh` ; mesures :
`contract/scripts/measure_testnet.py` ; données brutes : `docs/data/testnet-2026-11-11/`.

## Comptes (ids publics seulement)

| Rôle | Compte |
|---|---|
| Owner du contrat, compte racine (faucet) | `memaster-demo-j7xg7z.testnet` |
| **Contrat Memaster** | [`app.memaster-demo-j7xg7z.testnet`](https://testnet.nearblocks.io/address/app.memaster-demo-j7xg7z.testnet) |
| Redeemer factice (`mock-redeemer`) | `redeemer.memaster-demo-j7xg7z.testnet` |
| Oracle de prix factice (`mock-oracle`, opérateur = owner) | `oracle.memaster-demo-j7xg7z.testnet` |
| Acheteurs de test | `buyer1…buyer3.memaster-demo-j7xg7z.testnet` |
| Comptes faucet vidés vers la racine | `memaster-fund-kndj3m.testnet`, `memaster-fund-l007rk.testnet` |

Le faucet donne 10 NEAR par compte. Il en fallait une vingtaine (wasm de 551 Ko ≈ 5,5 NEAR immobilisés, 1,6 NEAR de
stockage de la série v2, 3 acheteurs), d'où les deux comptes faucet supplémentaires dont le solde a été transféré à la
racine. Les clés sont dans `~/.near-credentials/testnet/` (trousseau « legacy » de near-cli-rs), hors du repo ;
`git status` ne montre aucune clé.

Initialisation : `new(owner_id = racine, redeemer_id = redeemer, reveal_steps = 3, retry_delay_blocks = 100,
oracle_delay_blocks = 30)`. Le délai d'oracle est un **paramètre de `new`** réduit à 30 blocs pour pouvoir installer
l'oracle dans la session (144 000 par défaut) ; le code du contrat n'est pas modifié.

## Code déployé

| | |
|---|---|
| Commit | `188586e` (branche `feat/testnet`, contrat identique à `feat/demo`) |
| Build | `cargo near build non-reproducible-wasm` (cargo-near 0.23.0, rustc 1.99.1), 550 812 octets |
| sha256 (hex) | `b85f59064739231fc9797c1d8f5061a71d749b4b6015dc1607b75ea2549d5751` |
| `code_hash` on-chain (base58) | `DQiLruuJNAaFLZQ3zkd2fXMpCEBn8Ay2o4273wrEpGNk` (`verifier code` : VÉRIFIÉ) |
| mock-redeemer / mock-oracle | `864285ee…4a5157` / `c2b52066…e61782` |

**Build reproductible non fait, à décider.** `cargo near build reproducible-wasm` fonctionne avec Docker et l'image
`sourcescan/cargo-near:0.22.0-rust-1.99.1` (section `[package.metadata.near.reproducible_build]` du modèle de
`cargo near new`), mais il exige `package.repository` en `https://`. Ce lien est ensuite publié dans les métadonnées
NEP-330 du contrat (lisibles par tous). Le repo est privé : publier son URL sur une chaîne publique est une décision du
porteur. En attendant, le hash ne prouve rien sur le code source (README du vérificateur, « Le code source »).

## Transactions clés

| Étape | Transaction | Gaz brûlé |
|---|---|---|
| Déploiement + `new` | [9dZVjj7L…](https://testnet.nearblocks.io/txns/9dZVjj7Lms3R8DsQ91canXK1WdnMu4xgnjG2THz8vLHg) | 42,0 Tgas |
| `propose_price_oracle` / `accept_price_oracle` (30 blocs plus tard) | [5Lo4yhYg…](https://testnet.nearblocks.io/txns/5Lo4yhYgCqA3Pkucj3nyspNE5t5STcPrdhethYfojhg7) / [GNgMVbZe…](https://testnet.nearblocks.io/txns/GNgMVbZeAdfkm3jCKVwoBmkkCjzbi7FMv6aTE9sAnFrk) | |
| Série v2 : `create_series_batched` | [5U1wZazr…](https://testnet.nearblocks.io/txns/5U1wZazrkPUr4vSvDxXECD4PEKUozeqhi9QjKQqQ7kbr) | 21,3 Tgas |
| Série v2 : 8 × `append_series_cards` | [DRk4dAH9…](https://testnet.nearblocks.io/txns/DRk4dAH9bqMgpf6ArkRBa99WPRkeFCccVzNQDj7aLjBz) … [28yD7W2u…](https://testnet.nearblocks.io/txns/28yD7W2ud26UgAapL4s6DoJ7qhZWCxQhdgRbPpuH65k6) | 21,9 → 28,0 Tgas (croît à chaque lot), 15,9 pour le dernier |
| Série v2 : `open_series` | [DPqbaZCa…](https://testnet.nearblocks.io/txns/DPqbaZCai5jrsN8mrbb4ugWqHezVbTonVkkct4oQHAMP) | 8,1 Tgas |
| Série 1 (contrôle) : `create_series` / `open_series` | [GbxmfMPo…](https://testnet.nearblocks.io/txns/GbxmfMPoaUGHseA462UawPgNrMRGhGygvTptZRs5xosz) / [34kELgDZ…](https://testnet.nearblocks.io/txns/34kELgDZcFFhU4EB3CbX1eV3mExRJDQRPs821d27gjAG) | 3,3 / 2,8 Tgas |
| Premier booster (pack 0) | [E3xhY7Ji…](https://testnet.nearblocks.io/txns/E3xhY7JidQtYwzXSGLrShjoDDK58QvmCqXky6qVxkADA) | 29,5 Tgas |
| 3 boosters dans le même bloc (packs 5, 6, 7) | [GPpD3apN…](https://testnet.nearblocks.io/txns/GPpD3apNgQWNdmhtjBgEwSkDf4wb32KoNtqQgCkSPRJs), [6TGvc16Q…](https://testnet.nearblocks.io/txns/6TGvc16QaD524FbjXMBgRYiaAPjWX4xLBqFQbQJPi4pS), [7N7oAMsu…](https://testnet.nearblocks.io/txns/7N7oAMsu1s5TLVD6eUTNmuS6a2ZiZisx4Zko3hrnByhY) | 30,5 / 29,7 / 29,0 Tgas |
| Burn par le redeemer factice (token 330, `ctrl-com-a`) | [75zpK3x2…](https://testnet.nearblocks.io/txns/75zpK3x2f91Vhka1VU6J2KvqD8r1eJpz9Bd4cmZxqv66) | 9,0 Tgas |
| Marché : `list` (token 331, 0,2 NEAR) | [FZQ5EqY3…](https://testnet.nearblocks.io/txns/FZQ5EqY3pEvNtbxBWdbDjbvRmG3sqAc2T8oKDa7npfXo) | 2,9 Tgas |
| Marché : `buy` (5 % de redevance à l'owner) | [2JxgpQ1h…](https://testnet.nearblocks.io/txns/2JxgpQ1hN7JRgowjvFXnrDo81rdVrDzZ9T4ud4v3rrCo) | 6,0 Tgas |
| Résurrection via l'oracle factice (carte 6 de la série v2) | [BtvBKnmA…](https://testnet.nearblocks.io/txns/BtvBKnmADPuzXiv7Q6suY2qHYSCZAmoZF6GE66bjhBQm) | 10,8 Tgas |

Les 38 boosters (pack, série, acheteur, hauteurs, gaz, transaction) sont dans
`docs/data/testnet-2026-11-11/mesures-packs.json`.

## Séries

| Série | Contenu | `table_hash` | Dépôt requis | Prépayé par pack |
|---|---|---|---|---|
| 0 « Memaster v2 » | 1 646 cartes + 3 engagements, toutes les mécaniques (`serie-exemple.json`), 10 transactions | `4420bd36…4b4062` (= `build_series.py`) | 0,11597 NEAR | 1 597 o |
| 1 « Controle sans mecanique » | 4 cartes (une commune adossée, une épique plafonnée à 5), 3 cartes par booster, redevance 5 % | `604b9ef2…73492d` | 0,06107 NEAR | 1 107 o |

Stockage de la série v2 payé par l'owner : 1,598 NEAR retenus (`storage_deposit`) sur 2,878 joints, excédent rendu.

## Mesures

38 boosters (32 sur la série v2, 6 sur la série de contrôle) achetés par 3 comptes, 160 Tgas attachés (`min_gas`).
5 achats en série (un à la fois, stockage lu avant et après), puis des tours de 3 achats lancés en même temps.

### Temps de bloc

| Fenêtre | Temps moyen |
|---|---|
| 10 000 blocs (1 h 39) | **0,593 s** |
| 100 000 blocs (16 h 13) | **0,584 s** |

L'hypothèse de 0,6 s (`docs/mecaniques-spec.md`, `DEFAULT_ORACLE_DELAY_BLOCKS`, paramètres du rush) est **juste à
3 % près, dans le sens court** : 144 000 blocs durent environ 23 h 21 et non 24 h, la fenêtre du rush de 6 000 blocs
58 min, sa durée de 3 000 blocs 29 min. L'écart n'invalide pas les réglages, mais les durées « 24 h » sont un peu plus
courtes en réalité ; c'est à refaire sur mainnet, dont le rythme peut différer. Le code n'a pas été modifié.

### Blocs entre `buy_pack` et `pack_revealed`

| | Testnet | Sandbox |
|---|---|---|
| Transaction → `buy_pack` | 1 bloc (38/38) | 1 bloc |
| `buy_pack` → `reveal_step` 1, 2, 3 | +1, +2, +3 (38/38) | +1, +2, +3 |
| `buy_pack` → `pack_revealed` | **3 blocs (38/38)**, ≈ 1,8 s | 3 blocs |
| Envoi → retour de near-cli (finalité comprise) | 4,9 à 7,4 s, 5,9 s en moyenne | |

Chaque reçu chaîné s'exécute au bloc suivant, sans exception, même avec 3 boosters dans le même bloc : testnet
confirme exactement la sandbox. Aucun reçu n'a échoué, donc **aucun cas de `retry_reveal` ne s'est présenté** (non
provoqué, comme demandé).

### Gaz et coût

Prix du gaz testnet : 100 000 000 yocto/gaz, soit 0,0001 NEAR par Tgas brûlé.

| Étape | Testnet (min – max) | Sandbox (README) |
|---|---|---|
| Transaction (conversion) | 0,31 Tgas | |
| `buy_pack`, série v2 | 8,09 – 8,19 Tgas | 8,0 Tgas |
| `reveal_step` 1 et 2 | 2,53 – 2,59 Tgas | 2,4 Tgas |
| Dernier reçu, série v2 (5 cartes, mécaniques) | 13,96 – 15,92 Tgas | 15,5 Tgas au plus |
| **Booster v2, total** | **28,4 – 30,5 Tgas** (moyenne 29,6) | 29,5 Tgas au plus |
| Booster v2, NEAR brûlés | 0,00275 – 0,00296 NEAR | 0,002 à 0,003 NEAR |
| `buy_pack`, série de contrôle | 3,11 – 3,21 Tgas | |
| Dernier reçu, contrôle (3 cartes) | 4,16 – 4,33 Tgas | |
| Booster de contrôle, total | 13,6 – 13,9 Tgas, 0,00128 NEAR | |
| Chargement de la série v2 (10 transactions) | 219 Tgas en tout, 28,0 Tgas au plus, `open_series` 8,1 | 253 Tgas, 31,8 au plus, `open_series` 6,6 |
| Burn (`redeem` → redeemer → `on_redeem_complete`) | 9,0 Tgas (3,2 + 1,2 + 3,65) | 8,1 Tgas, callback 3,8 |
| `list` / `buy` | 2,9 / 6,0 Tgas | |
| `push_resurrection` → `set_resurrected` | 10,8 Tgas (`set_resurrected` 8,0) | |

Le maximum v2 (30,5 Tgas) dépasse d'un Tgas le « 29,5 au plus » de la sandbox : la sandbox n'a mesuré que 12 boosters
v2. Le dernier reçu reste à 16 Tgas sur 120 fixes, et le total très loin des 160 Tgas exigés et des 270 Tgas de
MetaMask.

### Stockage par pack (série v2, achats en série, `storage_usage` du contrat avant et après)

| Cas | Testnet | Sandbox |
|---|---|---|
| Tout premier booster du contrat (pack 0) | **1 084 o** | |
| Premier booster d'un compte | **1 027 o** (packs 1 et 2) | 964 o au plus (« premier achat d'un compte compris ») |
| Booster suivant du même compte | **595 o** (packs 3 et 4) | |
| Prépayé (`storage_per_pack`) | 1 597 o | 1 597 o |

**Écart à signaler** : le premier achat dépasse les 964 o annoncés comme maximum par la sandbox (+63 à +120 o). Une
cause probable est la longueur des comptes (`buyer1.memaster-demo-j7xg7z.testnet`, 35 caractères, stockés dans
plusieurs clés : liste par compte, compteur, pitié), et pour le pack 0 la création des premières entrées de la série
(anneau du rush, etc.). Le prépayé de 1 597 o, calculé pour des comptes de 64 caractères, couvre toujours largement.
Le chiffre « 964 o au plus » du README est donc à corriger en « dépend de la longueur du compte, ≤ 1 597 o ».

Bilan : le contrat utilise 735 412 o au total, solde 12,67 NEAR (dont 3,5 NEAR de prix encaissés, sans méthode de
retrait, comme prévu).

### Plusieurs boosters dans le même bloc

11 blocs ont reçu 2 ou 3 `buy_pack` (30 boosters sur les 33 achetés en parallèle). Constats :

- tous se révèlent 3 blocs plus tard, leurs `reveal_step` de même rang tombent ensemble dans le même bloc ;
- **les graines de reçus d'un même bloc sont toutes distinctes** (18 groupes vérifiés) : `random_seed` dépend de
  l'`action_hash` du reçu, pas seulement du bloc ;
- **l'ordre d'exécution n'est pas l'ordre d'envoi** : dans le bloc 277243820, buyer1, buyer2 puis buyer3 ont envoyé,
  et le contrat a attribué les packs 5 (buyer2), 6 (buyer3), 7 (buyer1). Le `pack_id`, séquentiel, donne l'ordre réel.
  C'est important pour le vérificateur (ci-dessous).

## Vérification publique

```bash
cd verifier
RPC=https://rpc.testnet.fastnear.com; C=app.memaster-demo-j7xg7z.testnet
python3 -m memaster_verifier table --rpc $RPC --contract $C --series 0     # 9 pages, hash = 4420bd36… : VÉRIFIÉ
python3 -m memaster_verifier table --rpc $RPC --contract $C --series 1     # VÉRIFIÉ
python3 -m memaster_verifier code  --rpc $RPC --contract $C --wasm ../contract/target/near/memaster.wasm  # VÉRIFIÉ
python3 -m memaster_verifier pack --event ../docs/data/testnet-2026-11-11/events-serie0.jsonl \
    --table ../contract/scripts/out/serie-v2/table.json                    # 64/64 vérifiés (32 achats, 32 tirages)
python3 -m memaster_verifier pack --rpc $RPC --contract $C --event ../docs/data/testnet-2026-11-11/events-serie1.jsonl  # 6/6
python3 -m memaster_verifier stats --events ../docs/data/testnet-2026-11-11/events-serie0.jsonl \
    --table ../contract/scripts/out/serie-v2/table.json --replay           # χ² p = 0,49, conforme
python3 -m memaster_verifier pack --rpc $RPC --contract $C --tx-hash 7A2i1j7j… --sender buyer1.…  # contrôle : VÉRIFIÉ, plafonds lus au bloc d'avant
```

Résultat : **tous les tirages sont VÉRIFIÉS** et le hash de la table recalculé par pages est égal au hash enregistré
pour les deux séries. Les fichiers d'événements sont reconstruits par `measure_testnet.py analyze` à partir de
`EXPERIMENTAL_tx_status` de chaque transaction connue.

Limites rencontrées :

- **`rpc.testnet.near.org` est déprécié** : il répond `-429 « THIS ENDPOINT IS DEPRECATED »` après quelques
  requêtes. L'alias `--rpc testnet` du vérificateur (`verifier/memaster_verifier/rpc.py`) pointe encore dessus : il
  faut passer l'URL de fastnear (`https://rpc.testnet.fastnear.com`) ou en changer l'alias (non fait ici).
- **Limites de débit de fastnear** (gratuit) : 429 après quelques dizaines de requêtes rapprochées, y compris pour
  near-cli-rs (« Failed to fetch access KeyList… rate limit », avant signature : aucune transaction n'est partie).
  `measure_testnet.py` réessaie avec attente ; le vérificateur, lui, n'a pas de reprise et sort en erreur 2. La lecture
  d'une table de 1 646 cartes (en-tête + 9 pages) passe sans problème, l'échec est venu de requêtes enchaînées
  juste avant.
- **Ordre des événements.** Le RPC ne liste pas les événements d'un contrat ; il faut connaître les transactions (ici,
  celles qu'on a envoyées) ou un indexeur. Trié dans l'ordre de lecture des transactions, le rejeu du rush échouait
  (15 `pack_bought` NON CONFORMES : `window_count` journalisé 8 ≠ rejoué 6) parce que l'ordre d'envoi diffère de
  l'ordre d'exécution dans un bloc. Trié par (hauteur, `pack_id`), tout est VÉRIFIÉ. Le vérificateur avait raison de
  refuser ; un indexeur doit fournir l'ordre d'exécution, le `pack_id` le permet pour les achats.
- **`pack --tx-hash` sur une série à mécaniques ne vérifie que partiellement** (acc, `rarity_roll`, rareté, retombée) :
  sans rejeu des burns, le choix de la carte n'est pas recalculé, même avec `--rpc`. La vérification complète passe par
  le fichier d'événements de toute la série. Sur la série de contrôle, `--tx-hash` vérifie tout, avec l'état des
  plafonds lu au bloc précédant le dernier reçu.
- **Archive** : non nécessaire ici (tout est récent). Les nœuds non-archive de fastnear ont servi `tx_status` et l'état
  au bloc passé ; `archival-rpc.testnet.fastnear.com` est indiqué pour les tirages anciens.
- Le `card_resurrected` ajouté au fichier d'événements après tous les boosters n'influence aucun tirage ; il n'est pas
  compté par le rejeu (« résurrections 0 »), point à regarder si on rejoue des boosters postérieurs.

## Problèmes rencontrés

1. **Faucet** : 10 NEAR par compte, insuffisant pour un contrat de 551 Ko plus la série v2 ; résolu par deux comptes
   faucet supplémentaires transférés à la racine (3 créations en tout, aucun refus).
2. **« Transaction has expired »** à la création de `buyer1` (sous-compte) : compte non créé, clé locale générée pour
   rien. Le script supprime désormais la clé orpheline et réessaie (3 essais).
3. **RPC** : voir ci-dessus (déprécié, limites de débit). 12 achats sur la série v2 et 6 sur le contrôle ont été
   refusés **avant signature** par la limite de débit, puis relancés : aucun double achat.
4. **Build reproductible** : bloqué par `package.repository` (voir « Code déployé »).
5. Aucun échec de reçu, aucun pack `Pending` ou `Stuck`, aucun `retry_reveal`.

## Relancer

```bash
cd contract
ROOT_ID=<compte>.testnet ./scripts/deploy_testnet.sh       # étapes déjà faites sautées
python3 scripts/measure_testnet.py blocktime --span 100000
python3 scripts/measure_testnet.py buy --contract app.<compte>.testnet --series 0 \
    --buyers buyer1.<compte>.testnet,buyer2.<compte>.testnet,buyer3.<compte>.testnet --rounds 4 --pause 10 --out txs.jsonl
python3 scripts/measure_testnet.py analyze --in txs.jsonl --out mesures.json --events events.jsonl
```

Le script refuse tout réseau autre que testnet et tout compte qui ne finit pas par `.testnet`.
