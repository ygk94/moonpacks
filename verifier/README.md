# Vérificateur public Memaster

Script Python qui permet à n'importe qui de vérifier les tirages du contrat Memaster (`../contract/`) à partir de
données publiques : la table de la série, les événements `pack_revealed` et `mythic_revealed`, et le RPC NEAR.

- Python 3.9 ou plus, **bibliothèque standard uniquement** (aucune dépendance à installer).
- `memaster_verifier/core.py` réimplémente `contract/src/draw.rs` (`initial_acc`, `mix`, `roll`, `draw_slot` avec la
  retombée), et `canon.py` reproduit `serde_json::to_vec` pour le hash de table et le `content_hash` des mythiques.
  Le code ne réutilise rien du Rust : il suit la spécification du contrat, et sa concordance octet par octet est
  vérifiée par des vecteurs tirés du contrat lui-même (voir « Tests »).

## Séries à mécaniques

Les mécaniques (`docs/mecaniques-spec.md`) sont dans la table hachée (`mechanics`, absent pour une série sans
mécanique : `canon.py` ne l'écrit alors pas, et les hash d'avant ne bougent pas). Tout l'état qui influence un tirage est
journalisé, et le vérificateur le **rejoue à partir des événements seuls**, sans archive d'état (`verify.SeriesReplay`) :

| Mécanique | Événements lus | Ce qui est recalculé |
|---|---|---|
| Pitié | `pack_revealed.mechanics.pity` | `gold_roll = roll(acc, 0, 2) mod 10⁶`, `p = min(10⁶, p0 + k·n)`, décision (`n + 1 ≥ N` ou `gold_roll < p`), `after`, et le compteur de chaque compte chaîné d'un booster au suivant |
| Table de taux | `pack_revealed.mechanics.mode` | `gold` si la pitié l'accorde, sinon `rush` si le pack est rush, sinon `base` ; `rarity_roll` avec les poids de cette table |
| Gold pack | `pack_revealed.draws` d'un pack `gold` | un emplacement par entrée de `mechanics.gold.slots` ; poids de l'emplacement (les siens, ou la base tronquée sous le plancher), retombée `core.fallback_order` (vers le bas jusqu'au plancher, vers le haut, puis sous le plancher), choix de la carte, restreint aux brûlables pour un emplacement `burnable` |
| Valeur du pack | `pack_revealed.mechanics.value`, `card_resurrected` | dernier emplacement d'un pack normal tiré parmi les brûlables ; `value_roll = roll(acc, 0, 3) mod Σpoids`, palier de la table du pack (normale, gold, rush), `total = ⌊prix × V / 10⁴⌋`, répartition au prorata des multiplicateurs entre les brûlables du tirage (résurrections rejouées), reste au plus fort multiplicateur (`core.split_value`) |
| Gold rush | `pack_bought.rush` (hauteurs, acheteurs) | anneau de seaux rejoué (`core.rush_on_buy`) : `active`, `window_count`, `baseline_count`, `triggered` ; plafond de packs rush par compte et par rush (`core.rush_account`) : `rush`, `capped`, `account_rush_packs` ; égalité avec `pack_revealed.mechanics.rush`. Un `pack_bought` manquant pour un booster est une **erreur** (le drapeau rush n'est pas cru sur parole) |
| Burns | `card_redeemed.burn_seq`, `card_resurrected.resurrect_seq`, `pack_revealed.mechanics.burn_seq` / `resurrect_seq` | compteurs de burn et brûlables au moment du tirage, poids bruts lissés par l'a priori `K` (`burn.prior_k`), ratio moyen pour une carte ressuscitée, poids renormalisés entre brûlables de la rareté, choix de la carte ; un numéro de séquence manquant est signalé |
| Résurrection | `card_resurrected.card_index` | la carte figure dans `mechanics.resurrection.eligible` (table hachée), sinon erreur |

`pack --event FICHIER --table table.json` sur une série à mécaniques rejoue tous les événements utiles du fichier
(`pack_bought`, `pack_revealed`, `card_redeemed`, `card_resurrected`), dans l'ordre du fichier. `stats` compare les
raretés visées au mélange des tables effectivement utilisées, booster par booster ; le test par carte est omis quand la
rareté est pilotée par les burns. Sans les `pack_bought`, le rejeu d'une série à rush échoue : il faut les achats pour
vérifier le drapeau rush.
Sans `card_redeemed`, le choix de la carte d'une série à burns n'est pas recalculé (vérification partielle). Sans
rejeu des `card_resurrected` (par exemple `--no-state` après une résurrection), la brûlable garantie et la répartition
de la valeur ne sont pas recalculées ; V, son palier et le total le sont toujours.

## Ce qui est vérifié

| Commande | Vérification |
|---|---|
| `table` | Avec `--rpc` : la table est **lue par pages**. `get_series_header` donne l'en-tête sans les cartes, le hash enregistré à l'ouverture et `card_count` ; les pages de `get_series_cards` (200 cartes au plus, `--page-size`) sont lues au même bloc que l'en-tête. Le script reconstruit la table, vérifie que chaque page est exactement la forme `serde_json` de `Vec<CardDef>` et que le nombre de cartes est `card_count`, **recalcule le hash localement** et le compare au hash enregistré (`get_series_header.table_hash` et `get_series_table_hash.stored`). Le contrat ne recalcule rien, et aucune vue lue ne relit la table entière : le coût de chaque appel est borné (4 à 25 Tgas à taille maximale, voir le README du contrat). Avec `--file` : `sha256` du fichier (un fichier reformaté est accepté, on hache sa forme canonique). Affiche les poids par rareté. |
| `pack` | Pour un `pack_revealed` : `table_hash` de l'événement égal à `sha256(table)`, `initial_acc = sha256("memaster:pack" ‖ pack_id_le ‖ owner ‖ table_hash)`, chaque `acc = sha256(acc ‖ seed ‖ pack_id_le ‖ owner)` dans l'ordre des graines (relances comprises), `acc` final, puis chaque emplacement : `rarity_roll`, rareté visée, retombée, `card_roll`, type et index de la carte. |
| `mythic` | `sha256(card_id ‖ sel) = commitment` et `sha256(json(content) ‖ sel) = content_hash`, comparés aux engagements **de la table hachée**, pas à ceux que l'événement déclare. Vérifie aussi que le sel fait 32 octets. |
| `stats` | Test du χ² sur les raretés visées (`rolled_rarity`, indépendantes des plafonds) contre les poids publics, puis sur les cartes de chaque rareté sans plafond. Avec `--replay`, rejoue en plus toute la série depuis l'ouverture et vérifie chaque tirage. |
| `code` | `code_hash` du compte déployé égal au `sha256` (base58) d'un wasm local. |

### L'état des plafonds

Le choix de la carte dépend des compteurs `minted` au moment du tirage : une carte plafonnée n'est plus tirable, et la
rareté retombe d'un cran. `pack` obtient cet état de l'une de ces façons :

1. `--snapshot FICHIER` : `minted` et `mythic_minted` juste avant le tirage (la sortie de `get_series` convient) ;
2. `--history FICHIER` : tous les `pack_revealed` de la série dans l'ordre d'exécution. Le script rejoue les
   compteurs depuis l'ouverture (tous à zéro) jusqu'au booster visé. C'est la méthode la plus sûre ;
3. `--rpc` seul : `get_series` lu au bloc qui précède le dernier reçu du tirage. Le bloc du dernier reçu est la
   hauteur de la dernière graine journalisée. Il faut que le nœud ait encore cet état : un nœud d'archive pour un
   tirage ancien ;
4. `--no-state` (ou rien de tout cela) : vérification partielle. Seuls `acc`, `rarity_roll`, la rareté visée, la
   retombée vers le bas et la cohérence entre carte et rareté sont vérifiés. `card_roll` et la carte ne le sont pas.

Si l'on passe plusieurs événements à `--event` (sans `--pack-id`), ils sont tous rejoués dans l'ordre du fichier.

## Ce qui ne peut pas être vérifié

- **L'origine des graines.** Le vérificateur part des graines journalisées. Il prouve que les cartes découlent de ces
  graines, de la table hachée et de l'état des plafonds, rien de plus. Qu'une graine soit bien `env::random_seed()`
  du reçu repose sur le code déployé. Relier depuis l'extérieur une graine journalisée à la valeur aléatoire publique
  d'un bloc (`hash(action_hash ‖ random_value)` d'après nearcore) n'a pas été confirmé et n'est pas implémenté
  (`docs/wallets-et-alea.md`, section 3, et la TODO du contrat).
- **Le producteur du dernier bloc.** Il connaît la graine de son bloc avant d'y inclure le dernier reçu, et il peut
  retenir ce bloc. L'avantage se limite au dernier reçu, et k > 1 n'y change rien. Le contrat n'utilise pas de VRF
  externe. Un tirage correct au sens du vérificateur peut donc avoir été « choisi » par un validateur qui a retenu un
  bloc. Aucun script ne peut le détecter.
- **Le validateur des mesures.** Le sandbox n'a qu'un validateur et produit un bloc par reçu. Le rythme réel des reçus
  sur testnet et sur mainnet n'est pas mesuré.
- **Les tirages échoués.** La graine d'un dernier reçu échoué n'est pas journalisée, puisque son état est annulé. Son
  résultat peut être recalculé à partir de données publiques, mais pas par ce script. L'échec ne dépend pas du
  résultat (README du contrat, « Tirage », point 6).
- **L'exhaustivité des événements.** Le rejeu (`--history`, `stats --replay`) suppose une liste complète et ordonnée
  des `pack_revealed` de la série (et, pour une série à mécaniques, des `pack_bought`, `card_redeemed` et
  `card_resurrected` ; les numéros `burn_seq` et `resurrect_seq` détectent un burn ou une résurrection manquants), venant d'un indexeur ou d'un nœud d'archive. Le RPC ne liste pas les événements.
  Une liste incomplète fausse l'état des plafonds, donc les boosters suivants paraissent non conformes. L'ordre de
  deux tirages finalisés dans le même bloc ne se déduit pas des événements : l'ordre du fichier fait foi.
- **Le code source.** `code` compare le code déployé à un wasm local. Sans build reproductible, ce qui n'est pas
  encore configuré, cela ne prouve pas que le wasm vient du code publié. L'owner garde sa clé : les tables ouvertes
  sont immuables par le code, pas par la gouvernance.
- **Les mythiques non révélées.** Avant la révélation, seuls l'engagement, le poids et le plafond sont publics. L'owner
  peut ne jamais révéler.
- **Les `token_id` et les métadonnées NFT** ne sont pas recoupés avec les tirages (`token_id = pack_id × 10 +
  emplacement` ; les métadonnées sont reconstruites par le contrat depuis la table).
- **La couverture de la table rush** (≤ 80 %) n'est pas vérifiable sans la valeur des cartes : elle est contrôlée hors
  chaîne par `contract/scripts/build_series.py` (`manifest.json["coverage"]`).
- **La décision de l'oracle de prix** (résurrection) n'est pas vérifiée : seul son effet est rejoué.
- Un `pack_revealed` d'un nœud RPC est cru tel que le nœud le sert. Pour s'en passer, il faut interroger plusieurs
  nœuds.

## Commandes

```bash
cd verifier
python3 -m memaster_verifier --help

# Table : lue par pages (en-tête + get_series_cards), hash recalculé ici et comparé au hash enregistré
python3 -m memaster_verifier table --rpc testnet --contract memaster.testnet --series 0
python3 -m memaster_verifier table --rpc testnet --contract memaster.testnet --series 0 --page-size 100
# … ou depuis un fichier
python3 -m memaster_verifier table --file table.json --expected-hash b386…a301

# Booster depuis une transaction (buy_pack, ou retry_reveal pour une relance)
python3 -m memaster_verifier pack --rpc testnet --contract memaster.testnet \
    --tx-hash 59zSx2FN… --sender alice.testnet
# … avec l'historique complet de la série pour l'état des plafonds
python3 -m memaster_verifier pack --rpc testnet --contract memaster.testnet \
    --tx-hash 59zSx2FN… --sender alice.testnet --history serie0.jsonl
# Booster depuis un fichier, table et instantané fournis (hors ligne)
python3 -m memaster_verifier pack --event ev.json --table table.json --snapshot get_series.json
# Toute une série rejouée depuis l'ouverture
python3 -m memaster_verifier pack --event serie0.jsonl --table table.json

# Mythique : préimages publiées par get_mythic_commitments, ou événement mythic_revealed
python3 -m memaster_verifier mythic --rpc testnet --contract memaster.testnet --series 0
python3 -m memaster_verifier mythic --event mythic_revealed.json --table table.json

# Fréquences contre taux annoncés (χ², seuil 0,001 par défaut), avec rejeu complet
python3 -m memaster_verifier stats --events serie0.jsonl --table table.json --replay

# Code déployé contre un wasm local
python3 -m memaster_verifier code --rpc testnet --contract memaster.testnet --wasm memaster.wasm
```

`--rpc` accepte une URL, `mainnet` ou `testnet`. Les fichiers d'événements peuvent être un objet JSON, une liste,
du JSONL, ou les lignes de logs brutes `EVENT_JSON:{…}`. Les données seules et l'enveloppe NEP-297 sont toutes deux
acceptées. Pour `table --file`, le mieux est d'enregistrer les octets bruts de la vue (`result` du RPC).
Les commandes `pack`, `mythic` et `stats` sans `--table` lisent elles aussi la table par pages, et refusent une table
dont le hash recalculé diffère du hash enregistré. Le script n'appelle plus `get_series_table` ni
`get_series_table_hash.recomputed` (supprimé du contrat) : ces vues dépassaient 180 Tgas sur une série de 2 000 cartes.

Codes de sortie : `0` vérifié, `1` non conforme (ou écart statistique significatif), `2` erreur d'entrée ou de RPC.

## Tests

```bash
cd verifier
python3 -m unittest discover -s tests -t . -v      # 60 tests (1 sauté sans scripts/out/), ~2 s, hors ligne
```

`tests/test_pages.py` (6 tests) simule le RPC à partir d'une table : en-tête, pages de 200, 37 et 1 cartes, page
falsifiée, carte manquante, plafond de 200 par page, et `pack` qui charge sa table par pages. Il exécute
`../contract/scripts/build_series.py scripts/serie-exemple.json` dans un dossier temporaire et vérifie que le hash
obtenu par pages est celui de la table complète (`table_hash.txt`, calcul d'avant), puis refait la vérification sur
`contract/scripts/out/serie-v2/` s'il existe. La concordance avec le vrai contrat est testée en sandbox
(`catalogue_v2_batched_load_and_packs`, `max_size_series_fits` dans `contract/tests/sandbox.rs`).

`tests/test_value.py` (13 tests) : ordre de retombée, base tronquée sous le plancher, arrondi des yocto (reste au plus
fort multiplicateur), palier unique, légendaire épuisée (montée à la mythique, puis sous le plancher), rejeu des gold packs
et de la valeur des événements réels, valeur, palier, répartition, emplacement gold et emplacement manquant falsifiés,
vérification partielle d'un gold pack ; `build_series.py` : fichier secret des mythiques (dictionnaire ou liste), repli
sur le champ `secret`, message clair sans l'un ni l'autre, fichier incomplet, `--tables-valeur` (multiplicateurs
décimaux, bornes du contrat, table rush > 80 % refusée), tables provisoires de 20 à 200 % et de moyenne 75 %.

`tests/test_mechanics.py` (20 tests) : concordance avec `mech_vectors.json`, renormalisation des burns (part des
brûlables exacte), rejeu des événements réels de `sandbox_mech_vectors.json` (pitié, rush, burns jusqu'à la dernière
carte, résurrection), et événements falsifiés détectés (compteur de pitié, décision or, drapeau rush, burn manquant,
burns ignorés, `pack_bought` manquant, résurrection hors liste), CLI compris. Correctifs de la revue des mécaniques
(`ReviewFixes`) : lissage par l'a priori K, ratio moyen d'une ressuscitée, rush d'un seul acteur plafonné à 3 packs.

Les vecteurs de `tests/vectors/` sont générés depuis le contrat par le crate Rust `vectorgen/`, qui dépend de
`../contract` sans le modifier :

- `draw_vectors.json` (test `draw_vectors`) : 200 tables pseudo-aléatoires passées au code compilé de
  `memaster::draw`. Elles comportent des plafonds atteints ou dépassés, des poids nuls, des mythiques, des `pack_id`
  proches de `u64::MAX`, et des chaînes avec guillemets, antislash, caractères de contrôle, DEL, U+2028, BOM et
  emojis. Les vecteurs couvrent `serde_json::to_string(table)`, le hash, `initial_acc`, `mix`, `roll` et les tirages
  complets avec les compteurs. S'y ajoutent 60 engagements mythiques ;
- `mech_vectors.json` (test `mech_vectors`) : 120 tables à mécaniques passées au code compilé de `memaster::draw`
  (`pity_is_gold`, `pack_mode`, `draw_pack_mech` : gold pack à planchers aléatoires, brûlable garantie, burns, a priori K,
  listes ressuscitables et résurrections ; `pack_value`), 200 répartitions `split_value` (prix, valeurs et
  multiplicateurs aléatoires), et 30 séquences de 250 achats de trois comptes pour `rush_on_buy` et `rush_account` ;
- `sandbox_mech_vectors.json` : événements réels de `contract/tests/sandbox.rs` `mechanics_end_to_end`
  (`MECH_VECTORS_OUT=… cargo test --test sandbox -- mechanics_end_to_end`) ;
- `sandbox_vectors.json` (test `sandbox_vectors`) : le wasm du contrat est déployé dans near-sandbox. Trois séries y
  sont ouvertes : 90 boosters avec plafonds et mythique, 4 boosters à retombées en cascade, et une table Unicode.
  Pour chaque booster, le fichier garde l'événement réel, `minted` avant l'achat et le hash de transaction, ainsi
  que l'événement `mythic_revealed`. Le test lance ensuite le CLI Python contre le RPC du sandbox (`table`, `pack
  --tx-hash`, `mythic`, `code`) et échoue s'il ne rend pas « vérifié ».
  Ces vecteurs datent d'avant la pagination et n'ont pas été régénérés (les tirages n'ont pas changé) : leur
  `get_series_table_hash` contient encore `recomputed`, que le test ne vérifie que s'il est présent.

```bash
cd verifier/vectorgen
cargo test --test gen_vectors -- draw_vectors mech_vectors  # vecteurs purs, sans réseau
NEAR_SANDBOX_BIN_PATH=/chemin/near-sandbox \
  cargo test --test gen_vectors sandbox_vectors -- --nocapture   # ~90 s
```

`MEMASTER_WASM` désigne le wasm à déployer. Par défaut, c'est `../../contract/target/near/memaster.wasm`, à
construire avec `cargo near build non-reproducible-wasm` dans `contract/`. Sans `NEAR_SANDBOX_BIN_PATH`,
near-workspaces télécharge le binaire near-sandbox. `SKIP_PY_RPC=1` saute l'appel au CLI Python.

Résultat au 11/11/2026 : les 200 cas purs et les 96 boosters réels concordent tous, sans exception. Après le gold
pack à planchers et la table de valeur, `draw_vectors.json` régénéré est encore identique à l'octet ; `mech_vectors.json`
et `sandbox_mech_vectors.json` ont été régénérés (nouveau format des mécaniques) et concordent au bit près. Après
l'introduction des mécaniques et du stockage minimal par carte, puis après les correctifs de la revue des mécaniques,
`draw_vectors.json` régénéré est identique au bit près (aucune différence git) ; `sandbox_vectors.json` (anciens `token_id`) n'a pas été régénéré et passe toujours. Le premier
booster d'une série n'est plus servi par `EXPERIMENTAL_tx_status` du sandbox (`NOT_OBSERVED`) après quelques
centaines de blocs. D'où le conseil d'un nœud d'archive pour les transactions anciennes.

## Structure

| Fichier | Rôle |
|---|---|
| `memaster_verifier/core.py` | Algorithme de `draw.rs` (mécaniques comprises : pitié, table de taux, gold pack à planchers, brûlable garantie, valeur du pack, burns renormalisés, rush), hash de table, engagements mythiques |
| `memaster_verifier/canon.py` | Sérialisation identique à `serde_json` pour `SeriesTable` et `MythicContent` |
| `memaster_verifier/verify.py` | Vérifications de table (entière ou par pages), de booster, de mythique ; rejeu d'une série, `SeriesReplay` (événements mêlés des mécaniques) |
| `memaster_verifier/stats.py` | χ² d'adéquation (fonction gamma incomplète, sans scipy) |
| `memaster_verifier/rpc.py` | Client JSON-RPC NEAR (`query`, `EXPERIMENTAL_tx_status`, `view_account`) |
| `memaster_verifier/cli.py` | Commandes `table`, `pack`, `mythic`, `stats`, `code` ; lecture paginée de la table (`fetch_table_pages`) |
| `tests/` | Tests unittest et vecteurs |
| `vectorgen/` | Générateur Rust des vecteurs (code du contrat et sandbox) |
