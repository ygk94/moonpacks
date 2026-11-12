# Contrat Memaster (NEAR, Rust)

Contrat unique pour les cartes NFT, les boosters, le tirage, les mythiques secrètes, le marché intégré, le burn et les
mécaniques de série (pitié et gold pack à planchers, rareté pilotée par les burns, gold rush, résurrection, valeur
aléatoire par pack : `docs/mecaniques-spec.md`).
Phase 3 de `docs/plan.md`. **Déployé sur testnet, jamais sur mainnet.** La version 3 est sur
`app3.memaster-demo-j7xg7z.testnet` (12/11), avec les deux séries de démo. La version 2 (gold pack ultra rare sans
garantie, mythique 1 sur 10⁶, valeur aléatoire par pack, mythiques anonymes) reste sur
`app2.memaster-demo-j7xg7z.testnet`, et la première version, sans valeur aléatoire, sur
`app.memaster-demo-j7xg7z.testnet`. Mesures dans `docs/testnet.md`.

**Version 3 (12/11, déployée sur `app3` le 12/11)** : stockage prépayé non utilisé rendu au tirage,
stockage libéré rendu au burn, remboursement d'un pack `stuck`, retrait des recettes avec garde-fous
(`withdraw_revenue`, `get_treasury`), codes d'erreur stables (`ERRORS.md`). Détail dans `docs/mecaniques-spec.md`,
section 12. **La disposition borsh change** (`Pack::storage_used`, compteurs de l'état racine, statut `refunded`) :
déployer sur un nouveau compte, comme `app2`.

- near-sdk **5.30.1** et near-contract-standards **5.30.1** (dernières versions sur crates.io le 11/11/2026)
- tests sandbox : near-workspaces **0.24.0** (avec near-sandbox 0.4.0), build par cargo-near-build 0.11.5
- build : cargo-near **0.23.0**

## Architecture

| Fichier | Rôle |
|---|---|
| `src/lib.rs` | État, `new`, constantes de gaz, de limites et de stockage, `set_redeemer`, `propose_price_oracle` / `accept_price_oracle` / `revoke_price_oracle`, métadonnées reconstruites des cartes, `token_id_of` / `parse_token_id` |
| `src/types.rs` | Table de série et mécaniques (dont `GoldParams`, `ValueParams`), cartes, engagements mythiques, packs compacts (`PackDraw`, `CardSlot`, `PackValue`), tirages, annonces |
| `src/mechanics.rs` | Validation des mécaniques (gold pack, tables de valeur, brûlable garantie), compteurs de burn, `set_resurrected` (oracle), vues `get_pity`, `get_rush_state`, `get_burns`, `get_resurrected` |
| `src/series.rs` | `create_series` (brouillon), `create_series_batched` + `append_series_cards` (grosse table par lots, payables), `replace_series_table(_batched)` (brouillon seulement), `delete_draft`, `open_series` (gel, hash, stockage du pire cas), `pause_series`, `resume_series`, `close_series` |
| `src/hash_stream.rs` | SHA-256 incrémental du JSON de la table, tenu à jour pendant le chargement ; coupe de l'en-tête autour de `"cards":[` (motif unique exigé) |
| `src/pack.rs` | `buy_pack`, `reveal_step` (privé), `retry_reveal`, `refund_stuck_pack`, tirage final et mint, stockage mesuré reçu par reçu et prépayé non utilisé rendu |
| `src/treasury.rs` | `get_treasury`, `withdraw_revenue` (retrait borné par les engagements) |
| `src/draw.rs` | Tirage pur et déterministe (sert aussi de référence au vérificateur), pitié, poids renormalisés des burns, fenêtre du rush, gold pack à planchers et retombée (`draw_slot_rule`, `fallback_order`), pack complet (`draw_pack_mech`), valeur (`value_tier`, `split_value`, `pack_value`) |
| `src/mythic.rs` | `reveal_mythic`, `compute_mythic_commitment` |
| `src/market.rs` | `list`, `delist`, `buy` |
| `src/redeem.rs` | `redeem`, `on_redeem_complete` (privé, rend le stockage libéré), interface `Redeemer` (montant = part de la valeur du pack dans une série à table de valeur) |
| `src/nft.rs` | NEP-171 (cœur), 177, 178, 181 (énumération), 199 (`nft_payout`, `nft_transfer_payout`), réécrits sur le stockage minimal par carte |
| `src/views.rs` | Lectures : `get_series`, `get_series_header` (en-tête léger), `get_series_cards` (paginée), `get_series_table_hash` (hash stocké), `get_rates` (paginée), `get_series_table` (petites séries), `get_mythic_commitments`, `get_pack` (avec `storage_used`), `get_packs_for_owner`, `get_card`, `get_backing`, `get_listing(s)`, `get_config` |
| `src/events.rs` | Événements NEP-297 (`standard: "memaster"`, `version: "1.0.0"`) |
| `mock-redeemer/` | Redeemer factice des tests : enregistre `redeem(owner, asset_id, amount)` ou panique sur demande |
| `mock-oracle/` | Oracle de prix factice : `push_resurrection` appelle `set_resurrected` (aucun prix lu) |
| `tests/sandbox.rs` | Tests d'intégration et mesures |
| `src/tests_batch.rs` | Tests unitaires du chargement par lots |
| `src/tests_mech.rs` | Tests unitaires des mécaniques et du stockage par carte |
| `src/tests_v3.rs` | Tests unitaires de la v3 (stockage rendu, pack `stuck` remboursé, retrait, codes d'erreur) |
| `ERRORS.md` | Codes d'erreur stables : code, texte français, proposition anglaise, qui peut la provoquer |
| `scripts/build_series.py` | Arguments des appels de série à partir du catalogue v2, vrais noms des mythiques lus dans `docs/data/secrets/mythiques.json`, tables de valeur (`--tables-valeur`) (voir « Série v2 ») |
| `scripts/validate_series.py` | Validateur à lancer avant `open_series` : règles du contrat réécrites hors ligne (en accord avec `validate_table` sur des tables mutées au hasard, `tests_fuzz.rs`), lots du dossier de sortie, valeur moyenne (rush ≤ 80 %, normale ≤ 100 %), préimages des mythiques révélables, aucun secret dans les fichiers publics (`--git` : fichiers suivis). Appelé aussi par `build_series.py` |

### Séries et table figée

- L'owner crée une série en brouillon, puis l'ouvre. À l'ouverture, la table est figée et
  `table_hash = sha256(serde_json::to_vec(table))` est enregistré. Ce sont exactement les octets de la vue
  `get_series_table`, et aussi ceux de la table reconstruite à partir de `get_series_header` (`header`, dont `cards`
  est vide) et des pages de `get_series_cards` (200 cartes au plus) : c'est ce que fait le vérificateur (testé en
  sandbox sur la série v2 et sur la série de taille maximale).
- **Vues et taille de la table.** `get_series_header` (en-tête sans les cartes, `table_hash` stocké, `card_count`,
  `max_page`), `get_series_table_hash` (hash **stocké**, jamais recalculé), `get_series_cards` et `get_rates`
  (paginées, 200 cartes au plus par page) ont un coût borné quelle que soit la taille de la série (voir « Gaz des
  vues »). `get_rates(series_id, from_index, limit)` donne les sommes par rareté sur toute la table (données de
  tirage compactes) mais ne liste que les cartes visibles de la page, avec leur `index`, puis `next_index` (`null`
  à la fin) ; les engagements mythiques sont toujours tous listés. `get_series_table` reste pour les petites séries :
  elle relit toute la table (183 Tgas pour 2 000 cartes aux chaînes maximales).
- Une table ouverte n'est jamais modifiable : aucune méthode ne l'écrit. L'owner peut seulement mettre en pause,
  reprendre ou fermer les ventes. Le tirage, le marché et le burn continuent pendant une pause.
- La table contient le prix, les cartes par booster (1 à 10), les poids des 5 raretés, les cartes visibles (poids,
  plafond optionnel, médias, adossement optionnel), les engagements mythiques, les redevances (NEP-199, 50 % au
  plus) et, en dernier, les **mécaniques** optionnelles (`mechanics`, absent du JSON quand il vaut `None` : les tables
  sans mécanique gardent leurs octets et leur hash). Les compteurs `minted`, les burns et l'état du rush sont à part,
  dans la série.
- Validation à la création : identifiants uniques, longueurs bornées, au plus 200 cartes par appel, 2 000 par série
  et 20 mythiques. Chaque rareté de poids non nul doit avoir une carte. **Il faut au moins une commune sans
  plafond** : c'est ce qui garantit qu'un tirage n'échoue jamais.
- **Chargement par lots** (table de plus de 200 cartes) : `create_series_batched(table)` avec l'en-tête, les
  mythiques et le premier lot, puis `append_series_cards(series_id, cards)` (200 cartes au plus par appel), puis
  `open_series`. Par lots, les `card_id` doivent être **strictement croissants** (octets UTF-8) : c'est ce qui
  garantit leur unicité sans relire la table. Les règles de couverture sont vérifiées à l'ouverture. Aucun ajout
  n'est possible après l'ouverture.
- **Stockage d'un brouillon par lots, payé par l'owner.** `create_series_batched` et `append_series_cards` sont
  `#[payable]` : le contrat écrit l'état en attente (`flush`), mesure `env::storage_usage()` avant et après, exige
  un dépôt au moins égal à l'augmentation (10¹⁹ yoctoNEAR par octet) et rend l'excédent. Le montant retenu est
  cumulé dans `storage_deposit` (vue `get_series_header`). `scripts/build_series.py` écrit le dépôt de chaque appel
  dans `manifest.json` (`deposits`).
- **`delete_draft(series_id)`** (owner, brouillon seulement) efface les blocs de cartes, les données de tirage, les
  compteurs, les mythiques, les redevances et le flux de hachage, puis rend à l'owner le stockage libéré (mesuré),
  **au plus ce qu'il a payé** (`storage_deposit`). Un brouillon de `create_series`, dont le stockage est resté à la
  charge du contrat, est supprimé sans remboursement. **Emplacement restant** : les identifiants de série sont des
  index de `Vector` et ne sont jamais réutilisés ; la série passe au statut `deleted` avec un en-tête réduit au nom,
  au prix et aux poids (184 o mesurés en sandbox, payés par l'owner et non rendus). Une série supprimée refuse tout
  (`open_series`, `append_series_cards`, `replace_series_table*`).
- **Stockage des cartes.** Les cartes visibles sont rangées par blocs de 50 (`series_cards`). La série ne garde que
  les données de tirage (rareté, poids, plafond, `minted`) : l'achat et le tirage ne relisent jamais la table
  entière, et le dernier reçu lit seulement le bloc de chaque carte tirée.
- **Hash au fil du chargement.** `table_hash` reste `sha256(serde_json::to_vec(table))`, mais il est calculé par
  morceaux (`hash_stream.rs`) : l'en-tête jusqu'à `"cards":[` à la création, chaque carte à son ajout, la fin à
  l'ouverture. Hacher 1,7 Mo d'un coup à l'ouverture coûtait 292 Tgas (mesuré). La coupe de l'en-tête exige que le
  motif `"cards":[` apparaisse **exactement une fois** dans l'en-tête sérialisé (sinon panique), suivi de `]`. L'ordre
  des champs de `SeriesTable` (`name`, `price`, `cards_per_pack`, `rarity_weights`, `cards`, `mythics`, `royalties`, puis
  `mechanics` s'il existe)
  est verrouillé par un test : ajouter ou déplacer un champ casse le test, pas le hash. Le contrat ne recalcule
  jamais le hash d'une table ouverte (l'ancienne vue de contrôle coûtait 229 Tgas à taille maximale).

### Tirage

1. `buy_pack(series_id)`, une seule signature. Le dépôt doit être au moins `prix + stockage du pire cas`
   (`get_series(id).required_deposit`), et le gaz au moins `get_series(id).min_gas` (160 Tgas avec k = 3).
   L'excédent de dépôt est rendu tout de suite, avant le tirage. Le prix est ensuite acquis (sauf pack `stuck`,
   point 7). **Le stockage prépayé non utilisé est rendu au dernier reçu** : chaque reçu du pack mesure ce qu'il
   écrit (`Pack::storage_used`), et le tirage final rend `storage_per_pack − storage_used` (× 10¹⁹) à l'acheteur
   (`pack_revealed.storage`). Sur testnet, cela fait environ 0,0057 NEAR rendus au premier achat d'un compte
   (1 034 o utilisés sur 1 605) et 0,010 NEAR ensuite (602 o).
2. `acc0 = sha256("memaster:pack" || pack_id_le || owner || table_hash)`, puis k reçus `reveal_step` privés et
   chaînés (k = 3 par défaut, de 2 à 6, fixé à l'init). Chacun calcule
   `acc = sha256(acc || env::random_seed() || pack_id_le || owner)`. Le gaz de chaque reçu est **fixé par le contrat** :
   statique, sans répartition du gaz restant (`INTERMEDIATE_STEP_GAS = 10 Tgas`, `FINAL_STEP_GAS = 120 Tgas`,
   `ENTRY_OWN_GAS = 20 Tgas`).
   **k > 1 n'apporte rien contre le producteur du dernier bloc** : il connaît la graine de son bloc avant d'y inclure
   le dernier reçu et peut le retenir. Plusieurs reçus empêchent seulement qu'un acteur fixe le résultat dès
   l'achat (le producteur du bloc d'achat, ou l'acheteur qui choisirait son moment).
3. Le dernier reçu choisit d'abord la **table de taux du pack** si la série a des mécaniques : gold pack si la pitié
   l'accorde (`gold_roll = u128_be(sha256(acc || 0 || 2)[0..16]) mod 10⁹` < `min(p_max, p0 + k·n)` en ppb, sans
   garantie : 1 sur 50 000 au départ, 1 sur 25 000 au plus ; le compteur ne repart à 0 qu'après un gold pack), sinon table rush si le pack a été acheté
   pendant un rush (figé par `buy_pack`), sinon la base. Un gold pack tire un emplacement par entrée de
   `mechanics.gold.slots`, chacun avec son plancher de rareté (retombée : vers le bas jusqu'au plancher, puis vers le
   haut, puis sous le plancher). Il tire ensuite chaque emplacement :
   `rarity_roll = u128_be(sha256(acc || slot || 0)[0..16]) mod Σpoids` choisit la rareté par cumul (mythique → commune).
   Si cette rareté n'a plus de carte disponible (plafond atteint), le tirage **retombe sur la rareté inférieure**.
   Ensuite `card_roll = u128_be(sha256(acc || slot || 1)[0..16]) mod Σpoids_disponibles` choisit la carte (avec la
   rareté pilotée par les burns : poids renormalisés entre brûlables de la rareté).
   Avec une table de valeur, le dernier emplacement d'un pack normal est tiré parmi les brûlables (retombée vers le
   bas, puis vers le haut), puis `value_roll = roll(acc, 0, 3)` choisit la valeur V du pack (en points de base du
   prix) dans la table normale, gold ou rush ; `⌊prix × V / 10⁴⌋` est réparti entre les brûlables du pack au prorata
   des multiplicateurs par rareté, le reste à la carte au plus fort multiplicateur (`docs/mecaniques-spec.md`, section 9).
   Le reçu crée les cartes par mint direct (jamais de `*_transfer_call`) et journalise `pack_revealed` : graines,
   hauteurs, acc intermédiaires et final, tirages complets, le bloc `storage` (`prepaid_bytes`, `used_bytes`,
   `refund`) et, pour une série à mécaniques, le bloc `mechanics`
   (`mode`, `rush`, `pity`, `burn_seq`, `resurrect_seq`, `value`). Ce reçu ne contient aucun `require` qui dépende du
   résultat ; le remboursement du stockage est un simple virement, que le solde couvre toujours (point 7).
4. Une étape périmée (mauvaise tentative, mauvais ordre, pack déjà révélé) est ignorée sans panique.
5. `retry_reveal(pack_id)` est **réservé à l'acheteur du pack** (v3 : un tiers ne peut ni épuiser ses tentatives ni le
   pousser vers `Stuck`), seulement si le pack est `Pending` sans aucune carte écrite et après
   `retry_delay_blocks` blocs sans progrès (100 par défaut, 20 au moins). La tentative est incrémentée, ce qui rend les anciennes
   étapes caduques. `acc` continue d'accumuler. Sont journalisées les graines de tous les reçus **réussis** : celle
   d'un dernier reçu échoué ne l'est pas, puisque son état est annulé.
6. **Un tirage échoué peut être connu.** La graine d'un dernier reçu échoué vaut `hash(action_hash || random_value)`,
   deux valeurs publiques, et `acc` avant ce reçu est journalisé : n'importe qui peut recalculer le résultat qu'il
   aurait donné. Ce n'est pas exploitable, car l'échec ne dépend pas du résultat : le dernier reçu n'a aucun chemin
   d'échec conditionné au tirage (gaz fixe, stockage prépayé, aucun `require` sur les cartes). Personne ne peut donc
   faire échouer les seuls mauvais tirages pour relancer. Un échec relève du protocole ou d'un bug, et la relance
   repart de nouvelles graines.
7. **État `Stuck`, puis remboursement.** Après 10 tentatives (`MAX_ATTEMPTS`), un nouvel appel à `retry_reveal` fait
   passer le pack en `Stuck` et émet `pack_stuck` : plus aucun tirage possible. `refund_stuck_pack(pack_id)`, ouvert à
   tous, rend alors à l'acheteur le prix et le stockage prépayé non utilisé, passe le pack en `refunded` (final) et
   émet `pack_refunded`. **Pas de tirage gratuit, par construction** : un pack tiré ne devient jamais `Stuck`, et le
   dernier reçu n'a aucun chemin d'échec qui dépende du tirage (point 6), donc personne ne peut faire échouer les seuls
   mauvais tirages pour se faire rembourser. Le remboursement du stockage ne peut pas manquer de solde : `withdraw_revenue`
   garde toujours les engagements des packs non tirés et une réserve (voir « Trésorerie »).

Il n'existe aucune méthode d'annulation. Le seul remboursement est celui d'un pack `Stuck` (vérifié dans l'ABI par un
test : `refund_stuck_pack` est la seule méthode dont le nom contient « refund », et elle refuse un pack tiré).

### Mythiques secrètes

- La table publique ne donne pour chaque mythique que `commitment = sha256(card_id || sel)`,
  `content_hash = sha256(json(MythicContent) || sel)`, le poids et le plafond (obligatoire, 100 au plus). La
  probabilité de la rareté et de chaque engagement est donc publique (`get_rates`), sans dévoiler le mème.
- **Décision de conception : un second hash.** `sha256(card_id || sel)` seul ne lie pas le titre, les médias ni
  surtout l'adossement (`asset_id`, `amount`). Sans `content_hash`, l'owner pourrait choisir l'adossement après coup.
  Les deux hashs utilisent le même `sel`, **exactement 32 octets** (refusé sinon), un par mythique : un sel court
  ou réutilisé permettrait, après une première révélation, de retrouver les autres mythiques par force brute sur les
  ~800 mèmes du catalogue. Les engagements et les `content_hash` en double sont refusés.
- **Génération hors ligne :** `python3 scripts/gen_mythics.py ENTREE.json PUBLIC.json scripts/secrets/serie1.json`.
  Le script tire un sel aléatoire de 32 octets par mythique, écrit les engagements à mettre dans la table, et les
  préimages dans un fichier en mode 600, ignoré par git (`scripts/secrets/`, `*.secrets.json`). Exemple d'entrée :
  `scripts/example-mythics.json`. Un test unitaire vérifie que ses hashs sont identiques à ceux du contrat.
- Chaque rareté de poids non nul, mythique comprise, doit avoir au moins une carte ou un engagement de poids non nul
  (sinon `get_rates` afficherait une probabilité impossible).
- **Métadonnées anonymes, avant comme après la révélation** : titre « ? », description « ? », image « ? »
  (`MYTHIC_MEDIA`, la même pour toutes), `extra` réduit à `series_id`, `rarity`, `pack_id` ; `get_card` ne donne ni
  `card_id` ni adossement. Les mythiques sont indiscernables entre elles dans leurs métadonnées
  (`docs/mecaniques-spec.md`, section 11).
- À la première sortie, la carte est créée **scellée** (sans adossement, événement `mythic_drawn`). Le contrat ne peut
  pas révéler seul, car le secret n'est pas sur la chaîne. Quiconque détient la préimage (en pratique l'owner, qui
  surveille `mythic_drawn`) appelle `reveal_mythic`. Le contrat vérifie les deux hashs, refuse une mythique jamais
  sortie, rend l'adossement disponible au burn (`get_backing`) et **publie `card_id`, `sel` et le contenu** dans
  `mythic_revealed` et `get_mythic_commitments` (c'est l'engagement : le coin devient public à ce moment-là, mais
  aucune métadonnée affichée ne change, et plus aucun `nft_metadata_update` n'est émis). Le révélateur paie le
  stockage ajouté.
- Une carte scellée se transfère et se vend, mais ne se brûle pas tant qu'elle n'est pas révélée.

### Stockage minimal par carte

Une carte ne stocke que sa référence : `token_id = pack_id × 10 + emplacement`, un `CardSlot` de 10 o dans le pack
(propriétaire `None` tant que l'acheteur la détient, état, positions) et son tirage compact (`PackDraw`, 31 o). Les listes
NEP-181 sont rangées par blocs (8 o par carte), avec retrait par échange. Les métadonnées NEP-177, l'adossement et
l'état scellé des mythiques sont **reconstruits à la lecture** depuis la table : `nft_token`, `nft_tokens`,
`nft_tokens_for_owner`, `get_card` et `get_backing` gardent leur forme. `reveal_mythic` ne réécrit plus les cartes.
Série v2 : **3 965 o → 848 o par pack** au plus sans mécanique, 964 o avec toutes (premier achat d'un compte compris),
971 o avec le gold pack à planchers et la table de valeur (7 o par pack pour la valeur : `bps` et masque des brûlables).
Sur testnet, le stockage dépend de la longueur du compte acheteur : 1 034 o au premier achat d'un compte de 35
caractères, 602 o ensuite (1 605 o prépayés, calculés pour 64 caractères, voir `docs/testnet.md`). Détail et mesures dans `docs/mecaniques-spec.md`.

### Mécaniques

Pitié et gold pack à plancher de rareté par emplacement, rareté pilotée par les burns, gold rush, résurrection des coins
morts et valeur aléatoire en jetons par pack (brûlable garantie au dernier emplacement) : formules, paramètres par défaut, ce qui
est haché, ce qui est journalisé, coût en gaz et en stockage dans **`docs/mecaniques-spec.md`**. Rôle `price_oracle`
(owner : `propose_price_oracle`, puis `accept_price_oracle` après `oracle_delay_blocks` blocs, 24 h par défaut,
paramètre de `new` ; `revoke_price_oracle` immédiat), méthode `set_resurrected` (oracle, cartes de la liste hachée
`mechanics.resurrection.eligible` seulement : épiques et légendaires non adossées ; sans liste, aucune résurrection). Le contrôle de
couverture de la table rush (≤ 80 %) est fait hors chaîne par `scripts/build_series.py` (moyenne de la table de valeur
rush).

### Marché intégré

`list(token_id, price)` demande un dépôt de 0,005 NEAR, rendu au retrait ou à la vente, et un prix d'au plus 10⁹ NEAR
(`MAX_LISTING_PRICE`, sinon le calcul des redevances déborde). `delist(token_id)`.
`buy(token_id, expected_price)` exige le prix attendu (contre un vendeur qui retirerait puis remettrait sa carte plus
cher juste avant l'achat) et un dépôt au moins égal au prix. Le vendeur reçoit le prix moins les redevances de la série,
l'excédent est rendu. Tout est refusé sur une carte en `Redeeming`. Tout transfert (NEP-171, `nft_transfer_payout`)
retire l'annonce. Une carte en vente ne peut pas être brûlée : il faut d'abord retirer l'annonce.

### Burn en deux temps (interface abstraite)

`redeem(token_id)` (1 yoctoNEAR, gaz ≥ 70 Tgas, propriétaire, carte adossée et pas en vente) fait passer la carte en
`Redeeming` : transfert, vente et nouveau burn sont alors refusés. Le contrat appelle ensuite
`redeemer.redeem(owner, asset_id, amount)` (30 Tgas fixes) puis `on_redeem_complete` (20 Tgas fixes, privé). Si le reçu
du redeemer réussit, quelle que soit sa valeur de retour, la carte est brûlée (`nft_burn`) ; si la série a la rareté
pilotée par les burns, le compteur de la carte et `burn_seq` sont incrémentés (journalisés dans `card_redeemed`).
**Le stockage libéré est rendu au propriétaire** : `on_redeem_complete` mesure les octets libérés (listes NEP-181,
blocs et compteurs vidés, approbations, propriétaire de l'emplacement) et les rend, jamais plus
(`card_redeemed.freed_bytes`, `storage_refund`). L'emplacement du pack (`CardSlot`, `PackDraw`) reste : il porte le
`token_id` des autres cartes, la part de valeur des autres brûlables et `get_pack`. S'il
échoue, la carte revient à `Normal`. L'adossement est celui de la table, ou celui donné par l'oracle (résurrection).
**Série à table de valeur** : `asset_id` reste celui de la carte, mais `amount` est la part de la valeur tirée pour le
pack (yoctoNEAR de valeur, recalculée depuis `Pack::value`), pas le montant de la table. Cas spéciaux à adossement fixe :
une mythique (son contenu révélé) et un exemplaire devenu brûlable après son tirage (montant de l'oracle). Il
est lu par `redeem`, envoyé au redeemer et passé en argument à `on_redeem_complete`, qui journalise celui-là dans
`card_redeemed` (`replaced_by` si l'oracle l'a remplacé entre-temps). **Contrat d'interface : le redeemer doit paniquer s'il ne livre pas.**
L'approvisionnement des jetons et le retrait réel restent à concevoir. Aucune intégration NEAR Intents.

### Transferts et approbations

- `new` est `#[private]` : seul le compte du contrat peut l'initialiser.
- `nft_transfer_call` est réécrit (au lieu de déléguer au standard) pour donner **15 Tgas fixes** à
  `nft_resolve_transfer`, contre 5 dans near-contract-standards. Il exige 45 Tgas au moins. Mesuré : 2,0 Tgas si le
  receveur garde la carte, 3,3 Tgas s'il la rend ou s'il panique.
- `nft_resolve_transfer` est réécrit lui aussi. Il ne retire une annonce (posée entre-temps par le destinataire) que si
  la carte revient **réellement** au propriétaire précédent. Si le destinataire garde la carte, l'a déjà transférée,
  l'a brûlée ou l'a mise en burn, rien n'est repris et son annonce reste.
- Le stockage des approbations effacées est rendu au propriétaire, comme le standard : `nft_transfer`,
  `nft_transfer_payout`, `nft_transfer_call` (à la résolution, selon le cas), `buy` du marché, et le burn.

### Liste des boosters par compte

`(compte, bloc de 32) → pack_ids` et un compteur par compte. Vues paginées : `get_pack_count_for_owner(account_id)` et
`get_packs_for_owner(account_id, from_index, limit)` (100 au plus par appel).

## Commandes

```bash
cd contract
rustup target add wasm32-unknown-unknown        # requis par cargo-near (wasm32v1-none ne suffit pas)
cargo install cargo-near --locked               # 0.23.0

cargo near build non-reproducible-wasm          # → target/near/memaster.wasm (595 245 octets au commit `ec76983` ; v2 : 580 961)
(cd mock-redeemer && cargo near build non-reproducible-wasm)
(cd mock-oracle && cargo near build non-reproducible-wasm)

cargo test --lib                                # 145 tests unitaires environ (python3 requis pour les tests des scripts et le fuzz)
MEMASTER_FUZZ_CASES=5000 cargo test --lib tests_fuzz -- --nocapture   # fuzz différentiel plus long (MEMASTER_FUZZ_SEED pour rejouer)
cargo test --test sandbox -- --nocapture        # 22 tests sandbox, mesures imprimées (~60 à 90 s, en parallèle)
MECH_VECTORS_OUT=../verifier/tests/vectors/sandbox_mech_vectors.json \
  cargo test --test sandbox -- mechanics_end_to_end   # régénère les événements réels du vérificateur

# Série v2 : arguments des appels (aucun secret dans scripts/out/, préimages dans scripts/secrets/)
python3 scripts/build_series.py scripts/serie-exemple.json     # --new-secrets pour tirer de nouveaux sels
python3 scripts/build_series.py scripts/serie-exemple.json --tables-valeur tables.json  # tables de valeur de sim/
cargo test                                      # tout
```

Les tests sandbox compilent eux-mêmes les wasm (production, variante `--features test-hooks`, redeemer factice) dans
`target/near-test/`. Le premier lancement télécharge le binaire near-sandbox, donc il faut le réseau.
La feature `test-hooks` ajoute `test_set_reveal_failure` (owner), qui fait échouer le dernier reçu du tirage. Elle
sert uniquement aux tests de `retry_reveal`, du pack `Stuck` et du retrait, et **ne doit jamais être déployée**.

## Tests

**Unitaires (113, dont 67 d'avant les mécaniques et 15 pour la valeur et le gold pack).** Validation des tables, hash égal au sha256 du JSON de la vue, table ouverte non remplaçable,
pause, dépôt ou gaz insuffisant, tirage complet et adossement (reconstruit depuis la table), étapes périmées ignorées, règles de
`retry_reveal`, déterminisme, retombée en cas de plafond (par rareté et par carte), fréquences sur 20 000 tirages,
engagements (bon sel, mauvais sel, adossement modifié, mythique jamais sortie), marché avec redevances, retrait de
l'annonce au transfert, burn réussi et échoué, interdictions en `Redeeming`. Ajouts de la revue de sécurité : achat
à un prix périmé refusé, poids mythique sans engagement pondéré refusé, `content_hash` en double refusé, sel court
refusé, passage en `Stuck` après 10 tentatives, pagination des boosters par compte, `nft_resolve_transfer` qui garde
l'annonce si le destinataire garde la carte et la retire seulement en cas de retour réel, remboursement exact du
stockage des approbations (transfert, vente, burn), hashs du script `gen_mythics.py` égaux à ceux du contrat.
Chargement par lots (14) : même hash, même vue et mêmes tirages qu'une table chargée d'un coup (lots qui ne
tombent pas sur les blocs), tirage compact identique au tirage de référence (3 000 cas avec plafonds), SHA-256
incrémental égal au SHA-256 de l'hôte (découpages aux bords de bloc), remplacement d'un brouillon par lots, refus :
ajout après ouverture, ajout par un tiers, plus de 200 cartes par appel, plus de 2 000 par série, `card_id` en double
ou hors ordre, ajout à une série complète, couverture vérifiée à l'ouverture ; enfin `build_series.py` sur le catalogue
v2 complet : hash du vérificateur Python = hash du contrat, octets de la vue = `table.json`, engagements = préimages,
aucun vrai nom de mythique dans la table. Revue du chargement par lots (13) : table reconstruite depuis
`get_series_header` et des pages de 200, 64, 50 et 1 cartes = hash stocké ; `get_rates` paginée (chaque carte sur une
seule page, sommes par rareté égales au calcul sur la table complète) ; dépôt manquant ou inférieur d'un yoctoNEAR
refusé (création et ajout), dépôt retenu = augmentation mesurée, excédent rendu exactement ; `delete_draft` (stockage
libéré rendu, borné par le payé, rien pour un brouillon de `create_series`, emplacement restant, identifiants non
réutilisés, série supprimée non ouvrable ni complétable, série ouverte non supprimable, owner seulement) ; ordre des
champs de `SeriesTable` verrouillé ; motif `"cards":[` en double ou absent refusé.

**Mécaniques et stockage par carte (29, `src/tests_mech.rs`).** Pitié : garantie optionnelle N = 1 (tous les packs or), garantie à
`n = N − 1` puis remise à zéro, décision égale à `gold_roll(acc) < p` (mod 10⁹), croissance et plafond de `p` en ppb
(1 / 50 000 → 1 / 25 000 en 1 000 packs, sans dépassement à `n = u32::MAX`), aucune garantie sans `n_max` (le compteur
monte), pack rush qui fait monter le compteur (il ne le remet plus à zéro). Burns : arrondi et
plancher de 25 %, dernière carte brûlée (plancher, jamais 0), carte épuisée par son plafond (0), renormalisation (part
des brûlables exacte sur 2 000 cas), tirages égaux au tirage de référence, `rarity_roll` inchangé, compteurs absents
sans la mécanique. Rush : palier relatif (trafic régulier ×1, ×4 et ×16 sans rush, pic qui déclenche), fenêtre longue
à remplir, pause, rush déclenché au dernier bloc d'un seau qui chevauche la fenêtre suivante, état figé à l'achat
(révélé après la fin : reste rush), pack rush qui remet la pitié à zéro. Résurrection : exemplaires existants et futurs
brûlables, oracle seulement, refus pour une carte déjà adossée, une commune, une rare, remplacement sans nouveau
`resurrect_seq`. Validation des paramètres (13 refus). Stockage : énumération cohérente après transferts et burns
(pages, propriétaires, aucun doublon), propriétaire compact au retour chez l'acheteur, métadonnées reconstruites,
`token_id` canoniques. Revue des mécaniques (6, et `reveal_clears_sealed_tokens_and_keeps_updated_at` dans
`src/tests.rs`) : burns lissés par l'a priori K (scénario de la revue : 10,5 % au lieu de 30,8 %), ressuscitée au ratio
moyen (20 % au lieu de 50 %), résurrection limitée à la liste hachée, oracle en deux temps (refus avant le délai,
oracle proposé sans pouvoir, événements, retrait immédiat), plafond de 3 packs rush par compte, adossement livré
journalisé pendant un remplacement.

**Valeur et gold pack (15, `src/tests_mech.rs`).** Un seul palier (V fixe, prix non multiple de 10⁴ : total exact,
aucun yocto perdu, parts seulement pour les brûlables, dernier emplacement toujours brûlable, vue `get_pack` = journal),
arrondi des yocto (reste au premier plus fort multiplicateur, 1 yocto à partager, aucune brûlable, prix extrême sans
dépassement), pack sans brûlable tirée naturellement (le dernier emplacement remonte à la rare brûlable), retombée vers le
bas avant le haut, ordre de retombée, gold pack (5 cartes, aucune commune, planchers, 99 / 1 au dernier (fréquence du 1 % sur 20 000 tirages), emplacement 2
brûlable, table de valeur gold), légendaires épuisées (montée à la mythique, puis sous le plancher), mythique au plafond
(retombe sur la légendaire), table de valeur selon le mode (normale, gold, rush), `redeem` qui transmet la part tirée,
exemplaire ressuscité après son tirage (montant de l'oracle) et après (part de la valeur), 14 refus de validation
(bornes de la table normale, paliers, poids nuls, multiplicateurs, dépassement, planchers, nombre d'emplacements),
brûlable garantie exigée, stockage prépayé (gold pack plus long et valeur), série sans valeur inchangée.

**Revue du 12/11 (13, `src/tests_fuzz.rs`, `src/tests_limits.rs`).** Fuzz différentiel du tirage : tables valides au
hasard (toutes les mécaniques, poids jusqu'à u32::MAX, prix extrêmes), état au hasard (plafonds atteints, raretés
épuisées, burns jusqu'au plancher, résurrections), contrat et vérificateur Python (`verifier/tests/crosscheck.py`)
comparés au bit près (tirages, valeur, pitié, gold rush), graine fixe et graine d'horloge à chaque `cargo test` ;
validateur hors ligne (`scripts/validate_series.py`) d'accord avec `validate_table` sur des tables mutées au hasard ;
pitié au plafond du compteur, burns au plancher, raretés et mythique épuisées, 40 refus de validation, table aux
bornes, `retry_delay_blocks` minimal.


**Version 3 (19, `src/tests_v3.rs`).** Stockage rendu au tirage (mesure reçu par reçu, rendu = prépayé − utilisé,
un seul virement, à l'acheteur ; second achat d'un compte moins cher), stockage rendu au burn (entrées de liste,
liste vidée, approbations comprises, jamais plus que les octets libérés), pack `stuck` (remboursé une fois à
l'acheteur même demandé par un tiers, prix sorti des recettes, ni étape ni relance ensuite, refus pour un pack en
attente ou tiré, un pack tiré ne devient jamais `stuck`, un tiers ne peut pas relancer le pack d'un autre), prix
d'annonce borné et redevances sans débordement, retrait (solde fixé à engagements + 2 yocto : un yocto de plus refusé,
solde après retrait ≥ engagements ; engagements suivis au tirage, au burn et au retrait d'annonce ; owner et 1 yocto
exigés), codes d'erreur (chaque message en a un, `ERRORS.md` complet dans les deux sens, détection d'un message sans
code).

**Sandbox (22)** :

| Test | Ce qu'il montre |
|---|---|
| `buy_pack_and_measurements` | Achat, recalcul public d'`acc` et des tirages, hauteurs et graines des reçus, gaz et stockage (cas normal et pire cas) ; v3 : `used_bytes` = variation exacte du `storage_usage` du compte, rendu = prépayé − utilisé |
| `distribution_over_300_packs` | 300 boosters (10 acheteurs en parallèle) : raretés tirées dans ±5σ, plafonds respectés, retombées, ratio des communes, recalcul de chaque tirage |
| `caps_fall_back_to_lower_rarity` | Légendaire plafonnée à 3 : exactement 3 créées, le reste retombe |
| `mythic_reveal_and_commitment_check` | Table sans le nom du mème, sortie scellée, métadonnées « ? » identiques avant et après la révélation (ni nom, ni `card_id`, ni adossement dans `nft_token` et `get_card`, aucun `nft_metadata_update`), mauvais sel refusé, révélation, engagements revérifiés depuis l'événement, sortie suivante directe et anonyme |
| `integrated_market` | Mise en vente, achat (95 % plus le dépôt au vendeur, 5 % de redevance), retrait, remise en vente plus chère refusée à l'ancien prix, transfert qui retire l'annonce, `nft_payout` |
| `burn_success_and_failure` | Burn réussi (carte brûlée, redeemer appelé avec les bons arguments), échec (carte restaurée puis brûlable), garde-fous, callback privé ; v3 : `freed_bytes` = baisse exacte du `storage_usage`, rendus |
| `no_cancellation_possible` | Prix acquis, livraison par mint uniquement, aucune méthode d'annulation (ni dans l'ABI), `refund_stuck_pack` seule méthode « refund » et refusée sur un pack tiré, `reveal_step` privé, pas de relance après écriture |
| `insufficient_deposit_or_gas` | Refus à `required - 1` yocto et à 100 Tgas, rien n'est enregistré, excédent rendu |
| `retry_reveal_after_failed_draw` | Dernier reçu en échec : pack `Pending` à l'étape 2, pas de remboursement, relance trop tôt refusée, relance d'un tiers refusée (`E_NOT_PACK_OWNER`), relance par l'acheteur après le délai, seconde relance refusée |
| `worst_case_fits_in_270_tgas` | **Plafond MetaMask** : boosters à 270 Tgas attachés au total, jusqu'à `pack_revealed`, avec table de 200 cartes aux chaînes maximales, 20 engagements, 10 redevances, légendaires épuisées (retombée) et mythique révélée au contenu maximal |
| `buyer_cost_vs_attached_gas` | Coût réel pour l'acheteur selon le gaz attaché |
| `init_is_private` | Un tiers ne peut pas appeler `new` |
| `nft_transfer_call_receivers` | Receveur qui garde, qui rend (`true`) ou qui panique : propriétaire final, approbations restaurées seulement en cas de retour, gaz de la résolution |
| `reveal_with_100_sealed_cards` | Révélation d'une mythique avec 100 cartes scellées et un contenu maximal |
| `catalogue_v2_batched_load_and_packs` | Catalogue v2 complet, avec les mécaniques par défaut de `serie-exemple.json` : refus en une transaction, chargement en 10 transactions avec les dépôts du script, hash = vérificateur Python, octets de la vue = `table.json`, vérificateur Python en mode pagination (pages de 200 et de 77) = même hash, 22 boosters à 160 Tgas (dont au moins un gold pack, assuré par la garantie de test `n_max = 20` ajoutée aux paramètres : la série v2 n'en a pas) revérifiés par le vérificateur Python (rejeu des plafonds, de la valeur et des planchers) |
| `max_size_series_fits` | 2 000 cartes aux chaînes maximales, 20 engagements, 10 redevances, 10 cartes par booster, toutes les mécaniques (gold pack de 10 emplacements, table de valeur ; pire cas) : chargement payé par l'owner, ouverture, gaz des vues légères (en-tête + 10 pages = hash), vérificateur Python par pages, achats au gaz minimal |
| `mechanics_end_to_end` | Toutes les mécaniques : pitié N = 3, rush déclenché par un pic après remplissage de la fenêtre longue, burns de toutes les com_a (jusqu'à la dernière), oracle installé en deux temps (acceptation refusée avant le délai), résurrection d'une épique par `mock-oracle` (rare et commune, hors liste, refusées), 45 à 48 événements rejoués par le vérificateur Python sans archive d'état |
| `worst_case_cascade_with_burns_fits` | Pire cas du dernier reçu : 2 000 cartes, 10 par booster, toutes les mécaniques (gold pack de 10 emplacements à plancher légendaire, table de valeur), légendaires, épiques et rares épuisées (chaque emplacement retombe trois fois, brûlable garantie comprise), burns entre les achats, 200 cartes ressuscitables : 48,4 Tgas au plus sur 120 |
| `value_and_gold_pack_end_to_end` | Gold pack de 5 cartes à planchers un pack sur deux (pitié N = 2), brûlable garantie, valeur tirée et répartie (prix non multiple de 10⁴), burn d'une brûlable d'un pack normal et d'un gold pack : le redeemer factice reçoit exactement la part journalisée ; rejeu par le vérificateur Python (valeur, répartition, planchers) |
| `stuck_pack_is_refunded_once` | v3 : 10 vrais derniers reçus en échec (build `test-hooks`), relance d'un tiers refusée, `Stuck`, remboursement demandé par un tiers et versé exactement à l'acheteur (prix + stockage non utilisé), ni second remboursement, ni relance, ni carte |
| `withdraw_revenue_respects_commitments` | v3 : annonce et pack en attente, refus (tiers, sans 1 yocto, au-delà du retirable), retrait maximal, solde ≥ engagements ; ensuite le pack en attente se tire avec son remboursement, un achat passe, l'annonce se retire avec son dépôt |
| `draft_storage_is_paid_by_owner_and_refunded_on_delete` | Création par lots refusée sans dépôt, stockage payé = augmentation mesurée, excédent rendu, `delete_draft` réservé à l'owner, stockage libéré rendu, emplacement de 184 o, série supprimée inutilisable, série ouverte non supprimable |

## Série v2 (`scripts/build_series.py`)

Le script (bibliothèque standard) lit `docs/data/catalogue-v2.json` et un fichier de paramètres
(`scripts/serie-exemple.json` : prix, cartes par booster, poids, plafonds, brûlables factices, mécaniques, gold pack à
planchers, **tables de valeur provisoires** : normale de 20 à 200 %, moyenne 75 %). `--tables-valeur fichier.json`
remplace les tables de valeur, au format `{"normale": [[bps, poids], …], "gold": […], "rush": […],
"multiplicateurs": {"commune": x, …}}` (clés anglaises acceptées ; multiplicateurs décimaux multipliés par 1 000) ; le
script applique les bornes du contrat et refuse une table rush de moyenne supérieure à 80 %. **Vrais noms des
mythiques** : lus dans `docs/data/secrets/mythiques.json` (ignoré par git, `--mythiques` pour un autre chemin), au format
`{"<id catalogue>": {"id": …, "nom": …}}` ou liste d'objets avec `catalogue_id`. Si le fichier manque, le script se
replie sur le champ `secret` du catalogue s'il existe encore (avertissement), et s'arrête sinon avec un message clair. Il écrit dans
`scripts/out/<slug>/` : `create_series_batched.json`, `append_series_cards.01…08.json`, `open_series.json`, la
table complète `table.json` (octets exacts de `get_series_table`), `table_hash.txt` (calculé par `verifier/`) et
`manifest.json`. **`manifest.json["deposits"]`** donne le dépôt à joindre à chaque appel (yoctoNEAR) : une borne
haute du stockage ajouté (taille JSON des arguments, qui majore la taille borsh, plus des marges par bloc et par
série), arrondie au millième de NEAR. L'excédent est rendu par le contrat. Série v2 : 2,87 NEAR joints en tout,
1,50 NEAR retenus (1,59 NEAR avec les mécaniques par défaut : compteurs de burn et anneau du rush). Exemple d'appel (near-cli-rs) :

```bash
near contract call-function as-transaction <contrat> append_series_cards \
  file-args scripts/out/serie-v2/append_series_cards.01.json prepaid-gas '300 Tgas' \
  attached-deposit '<deposits["append_series_cards.01.json"]> yoctonear' sign-as <owner> network-config testnet sign-with-keychain send
```
 Les 3 mythiques ne sont que des engagements, produits par `gen_mythics.py` ; leurs préimages et
leurs vrais noms ne vont que dans `scripts/secrets/` (ignoré par git, mode 600). Les sels existants sont réutilisés,
donc le hash est stable d'une exécution à l'autre ; `--sels FICHIER` reprend les sels d'un autre fichier de secrets
(par card_id) sans en tirer de neufs. Médias : `media_template` (`ipfs://TODO/<id>.svg` dans l'exemple), ou
`--media-base ipfs://<CID>`, qui donne `ipfs://<CID>/<card_id>.svg` et, pour toutes les mythiques, le visuel « ? »
commun `ipfs://<CID>/mythique.svg` (`mythic_media`, jamais nommé d'après le vrai id). Les cartes sont triées par
`card_id`. Un identifiant de plus de 64 octets est raccourci (voir `manifest.json`). Le script refuse d'écrire si
un vrai nom de mythique apparaît dans une sortie publique.

Mesures (sandbox, 1 646 cartes visibles + 3 engagements, table de 275 Ko) :

| Cas | Résultat |
|---|---|
| Ancien code, limite levée, tout en une transaction | `create_series` 56,5 Tgas (275 Ko d'arguments), `open_series` 118,6 Tgas, mais `buy_pack` à 160 Tgas **échoue** : 27 Tgas pour relire et réécrire 138 Ko de série, au-delà des 20 Tgas propres |
| Nouveau code, en une transaction | Refusé (200 cartes au plus par appel) |
| Nouveau code, par lots | 10 transactions, 253 Tgas en tout, 31,8 Tgas au plus par transaction (mesure du stockage comprise), `open_series` 6,6 Tgas ; stockage 149 803 o (1,50 NEAR), payé par l'owner |
| Booster (5 cartes, 160 Tgas attachés), avant | 48 Tgas au plus en tout, `buy_pack` 6,8 Tgas, dernier reçu 35,3 Tgas ; stockage 4 040 o au plus, 15 715 o prépayés |
| Booster v2, stockage minimal, toutes les mécaniques | 29,5 Tgas au plus en tout, `buy_pack` 8,0 Tgas, dernier reçu 15,5 Tgas ; stockage 964 o au plus, 1 597 o prépayés (848 o sans mécanique) |
| Booster v2, gold pack à planchers et table de valeur (22 boosters dont un gold) | 29,6 Tgas au plus en tout, `buy_pack` 8,1 Tgas, dernier reçu **15,4 Tgas** ; **stockage 971 o au plus, 1 605 o prépayés** |
| Booster v2, gold pack ultra rare (pitié en ppb, garantie de test `n_max = 20` pour mesurer un gold), mythique 5 / 2·10⁷, valeur 75 % (22 boosters dont un gold, 11/11) | 29,9 Tgas au plus en tout, `buy_pack` 8,1 Tgas, dernier reçu **15,7 Tgas** ; **stockage 971 o au plus, 1 605 o prépayés** |
| **Testnet v3** (`app3`, 41 boosters des séries de démo, 1 527 cartes, aucun gold, 12/11) | 29,4 – 31,1 Tgas en tout (moyenne 30,0), `buy_pack` 8,0 – 8,1 Tgas, dernier reçu 14,3 – 15,8 Tgas ; stockage 1 038 o au premier achat d'un compte (1 095 o pour le tout premier), 606 o ensuite, 1 605 o prépayés, **le reste est rendu** (0,00567 à 0,00999 NEAR) |
| **Testnet** (`app2`, 31 boosters de la série v2, aucun gold, 11/11) | 29,3 – 30,6 Tgas en tout (moyenne 29,9), `buy_pack` 8,2 – 8,3 Tgas, dernier reçu 14,7 – 15,9 Tgas ; stockage 1 034 o au premier achat d'un compte (1 091 o pour le tout premier booster), 602 o ensuite, 1 605 o prépayés |
| Taille maximale (2 000 cartes aux chaînes maximales) | lot de 188 Ko, `append_series_cards` 88 Tgas au plus, `open_series` 10,7 Tgas, 1,66 Mo de stockage (16,6 NEAR payés par l'owner) ; booster de 10 cartes : `buy_pack` 9 Tgas, dernier reçu 61 Tgas (avant) ; avec le stockage minimal et toutes les mécaniques : `buy_pack` 10,3 Tgas, dernier reçu 24,3 Tgas au plus, stockage 1 254 o au premier achat ; raretés épuisées en cascade (`worst_case_cascade_with_burns_fits`) : dernier reçu 49,1 Tgas au plus ; avec gold pack de 10 emplacements et table de valeur : dernier reçu 23,3 Tgas au plus (normal et gold), stockage 1 266 o au premier achat, 2 025 o prépayés, cascade 48,4 Tgas |

### Séries de démo « entrée » et « standard » (`docs/series-demo.md`)

Deux séries sur le catalogue de démo complet (1 527 cartes visibles + 3 engagements), mêmes mécaniques que
`serie-exemple.json`, tables de valeur de `sim/resultats/serie5/tables-valeur.json`, 9 brûlables reliées à de vrais
actifs NEAR Intents par adresse de contrat. Déployées sur `app3.memaster-demo-j7xg7z.testnet` (séries 0 et 1, 12/11).

| Fichier | Rôle |
|---|---|
| `scripts/intents_brulables.py` | Rapprochement brûlables -> 1Click `/v0/tokens` par adresse, devis `dry`, correspondance `docs/data/intents-brulables-demo.json` |
| `scripts/series_demo.py` | Écrit `scripts/serie-demo-entree.json` (0,20 $ = 0,0552 NEAR) et `scripts/serie-demo-standard.json` (0,50 $ = 0,1381 NEAR), au cours donné |
| `scripts/ipfs_media.py` | Dossier IPFS des SVG anglais (`prepare`), CID local (`cid`, `npx ipfs-car@3.1.0`), envoi du CAR (`upload`, `PINATA_JWT` ou `W3S_TOKEN`, `--dry-run`) |
| `scripts/tests/` | Tests de ces trois scripts et des options de `build_series.py` : `python3 -m unittest discover -s contract/scripts/tests` |

```bash
cd contract
python3 -I scripts/build_series.py scripts/serie-demo-entree.json --catalogue ../docs/data/catalogue-demo.json \
    --sels scripts/secrets/serie-v2.json [--series-id N]
```

`table_hash` : entrée `2064056b…5a313a40`, standard `382c5a38…eaf4310f` (tables dans `docs/data/series-demo/`).
Visuels : `ipfs://bafybeifejdd5hvm44qa6qv5s3m2avywhdrydhn2rwypccttz52eu5viuia/…`, CID calculé en local, pas encore
envoyé.

### Gaz des vues (série de taille maximale)

Mesuré en sandbox (`max_size_series_fits`) en appelant les vues en transaction : gaz brûlé par le reçu, sur 2 000
cartes aux chaînes maximales, 20 engagements et 10 redevances. Limite d'une vue : 300 Tgas.

| Vue | Avant | Après |
|---|---|---|
| `get_series_header` | (n'existait pas) | 4,7 Tgas |
| `get_series_table_hash` | 229 Tgas (recalcul) | 4,3 Tgas (hash stocké) |
| `get_series_cards`, page de 200 | | 22,2 Tgas au plus |
| `get_rates`, page de 200 | 184 Tgas (table entière) | 25,4 Tgas au plus ; 34,2 Tgas avec la rareté pilotée par les burns |
| `get_series_table` | 183 Tgas | inchangée, réservée aux petites séries ; le vérificateur ne l'appelle plus |

## Mesures (sandbox near-sandbox 0.4.0, 11/11/2026)

### Hauteur de bloc de chaque reçu du tirage (k = 3)

| Reçu | Bloc | Gaz brûlé |
|---|---|---|
| `buy_pack` | 143 | 2,75 Tgas |
| `reveal_step 1` | 144 | 2,40 Tgas |
| `reveal_step 2` | 145 | 2,41 Tgas |
| `reveal_step 3` (tirage et 5 mints) | 146 | 12,84 Tgas |

Résultat identique à chaque exécution (par exemple 228, 229, 230 et 231 lors d'une autre). **Chaque reçu créé par le
contrat s'exécute au bloc suivant, et les 3 graines sont distinctes** (le test l'exige). Cela confirme
`docs/faisabilite.md` : un reçu créé par un contrat s'exécute au plus tôt au bloc suivant, et la graine nearcore vaut
`hash(action_hash || random_value)`, donc elle change à chaque reçu. Comme les reçus tombent dans 3 blocs différents,
le `random_value` de 3 producteurs de bloc (pas forcément distincts) entre dans `acc`. Limite : le sandbox n'a qu'un
validateur et produit un bloc par reçu ; le rythme réel sur testnet et mainnet reste à mesurer (test 1.7).

### Gaz

| Cas | Gaz total brûlé | Plus gros reçu |
|---|---|---|
| Table de 4 cartes, 5 cartes par booster | 21,4 Tgas | 12,8 Tgas (tirage) |
| Pire cas : 200 cartes aux chaînes maximales, 5 cartes par booster | 61,9 Tgas | 36,7 Tgas |
| Pire cas, 10 cartes par booster | 83,9 Tgas | 58,7 Tgas (le `FINAL_STEP_GAS` de 120 Tgas suffit) |
| Pire cas « MetaMask » (voir le test 270 Tgas) | 63 à 68 Tgas | 38 à 42 Tgas |
| `redeem` réussi | 10,4 Tgas (8,1 avec le stockage minimal) | `on_redeem_complete` 3,8 Tgas avec compteurs de burn |
| `nft_transfer_call` (garde / rend / panique) | 8,6 / 9,5 / 9,4 Tgas | résolution 2,0 / 3,3 / 3,3 Tgas sur 15 fixes |
| `reveal_mythic`, 100 cartes scellées, contenu maximal | 85,6 Tgas avant, **5,0 Tgas** avec le stockage minimal | les cartes ne sont plus réécrites |

**Gaz exigé :** `min_gas = 20 + 2 × 10 + 120 = 160 Tgas` avec k = 3 (180 Tgas avec k = 5). C'est sous le plafond de
**270 Tgas par transaction** de l'adaptateur MetaMask (near-connect, comptes `0x…`), qui doit couvrir `buy_pack` et
tous les reçus chaînés. Le protocole mainnet 88 autorise 1 PGas par reçu, mais on vise 270 Tgas au total. Le test
`worst_case_fits_in_270_tgas` le vérifie.

**Coût pour l'acheteur** (`buyer_cost_vs_attached_gas`) : dépôt + gaz réellement brûlé (environ 0,002 à 0,003 NEAR), le
reste du gaz étant rendu. Comme le gaz est prépayé à 0,001 NEAR/Tgas (`docs/faisabilite.md`), le compte doit
toutefois détenir temporairement environ 0,16 NEAR (à 160 Tgas) à 0,27 NEAR (à 270 Tgas) en plus du dépôt.

### Stockage d'un `buy_pack`

| Cas | Utilisé avant | Utilisé après | Prépayé après (`storage_per_pack`) | Dépôt requis après (prix 0,1 NEAR) |
|---|---|---|---|---|
| Table de 4 cartes, 5 cartes par booster | 4 235 o | 888 o | 1 227 o (0,012 NEAR) | 0,112 NEAR |
| Pire cas, 5 cartes par booster | 7 888 o | 829 o | 1 227 o | 0,112 NEAR |
| Pire cas, 10 cartes par booster | 14 975 o | 858 o | 1 527 o | 0,115 NEAR |
| Série v2, toutes les mécaniques | 3 965 o | 964 o | 1 597 o | 0,116 NEAR |

Avant, le dépôt requis était de 0,216 à 0,396 NEAR. Le stockage prépayé est une borne du pire cas calculée à
l'ouverture (`worst_case_pack_storage` : comptes de 64 caractères, premier achat du compte, nouveaux blocs de liste,
entrée de pitié, entrée du plafond de packs rush). Il ne dépend plus de la longueur des métadonnées.

**v3 : le stockage non utilisé est rendu** au dernier reçu (`pack_revealed.storage.refund`). L'ancienne objection
(« un remboursement calculé après le tirage serait un chemin conditionné au résultat ») ne tient pas : le montant dépend
du tirage, mais c'est un virement sortant sans `require`, couvert par le solde (le retrait garde les engagements des
packs non tirés et une réserve) ; il ne peut pas faire échouer le reçu. Mesures (sandbox, 12/11) : table de 4 cartes,
893 o utilisés sur 1 227 au premier achat (0,00334 NEAR rendus), 580 o ensuite (0,00647 NEAR) ; coût réel de
l'acheteur 0,1103 puis 0,1072 NEAR pour 0,11227 NEAR joints. Sur testnet, avec les mesures de la v2 (+4 o en v3), ce serait
environ 567 o rendus au premier achat d'un compte et 999 o ensuite.

### Trésorerie (v3)

`get_treasury()` donne le solde, le stockage occupé, les engagements et le retirable ; `withdraw_revenue(amount?)`
(owner, 1 yocto) retire au plus `solde − (stockage occupé + dépôts d'annonces + packs non tirés + valeur des
brûlables vivantes + 1 NEAR de réserve)`, événement `revenue_withdrawn` (`docs/mecaniques-spec.md`, section 12.4).
L'adossement fixe d'une table sans valeur et celui des mythiques, qui ne sont pas en NEAR, ne sont pas réservés.

### Comparaison v2 → v3 (même sandbox, même jour)

| Cas | v2 (`307321a`) | v3 |
|---|---|---|
| Série v2, 22 boosters à 160 Tgas : gaz total au plus | 29,71 Tgas | 30,99 Tgas (+1,3 : mesure du stockage, virement de remboursement) |
| idem, `buy_pack` / dernier reçu au plus | 8,10 / 15,56 Tgas | 8,21 / 16,04 Tgas |
| idem, stockage au plus / prépayé | 971 o / 1 605 o | 975 o / 1 605 o (+4 o : `Pack::storage_used`) |
| 2 000 cartes, 10 par booster : total | 38,8 – 39,7 Tgas | 39,7 – 42,1 Tgas |
| idem, dernier reçu | 22,4 – 23,3 Tgas | 22,5 – 24,8 Tgas |
| Cascade au pire (dernier reçu, budget 120) | 48,4 Tgas (doc) | 49,4 – 50,4 Tgas |
| `redeem` réussi, total / `on_redeem_complete` au plus | 8,19 / 3,96 Tgas | 8,96 / 4,27 Tgas (budget 20) |
| Pack `Stuck` remboursé | impossible | 3,4 Tgas |
| `withdraw_revenue` | (n'existait pas) | 3,0 Tgas |
| wasm | 580 961 o | 595 094 o (+14 133) ; 595 245 o pour le build déployé sur `app3` |

**Mesuré sur testnet** (`app3`, 41 boosters des séries de démo, 12/11, `docs/testnet.md`) : 29,4 – 31,1 Tgas par
booster (moyenne 30,0, contre 29,9 pour la v2), `buy_pack` 8,0 – 8,1 Tgas, dernier reçu 14,3 – 15,8 Tgas. Stockage :
1 095 o pour le tout premier booster, 1 038 o au premier achat d'un compte, puis 606 o (694 – 702 o au premier achat
d'un compte dans une 2e série). `used_bytes` est égal à la variation de `storage_usage` du contrat. **Montant rendu :
0,00999 NEAR dans le cas courant (999 o), 0,00567 NEAR au premier achat d'un compte**, 0,0051 au plus bas. Coût net
d'un booster à 0,0552 NEAR : 0,0649 NEAR en moyenne, pour 0,07125 NEAR joints. Burn : `card_redeemed.freed_bytes =
16`, 0,00016 NEAR rendus, mais `on_redeem_complete` brûle **8,42 Tgas** sur testnet contre 4,27 en sandbox, sous son
budget de 20 Tgas ; l'écart est à expliquer. `withdraw_revenue` : 3,3 Tgas, refusé au-delà du retirable
(`E_WITHDRAW_LIMIT`). Le prévisionnel « 30,6 – 31,9 Tgas » était donc pessimiste.

## Revue de sécurité du 11/11/2026 : corrections

| # | Point | Correction | Test |
|---|---|---|---|
| 1 | `new` sans `#[private]` | `#[private]` | `init_is_private` |
| 2 | `nft_resolve_transfer` à 5 Tgas | `nft_transfer_call` réécrit, résolution à 15 Tgas fixes, 45 Tgas exigés, résolution allégée (2 à 3,3 Tgas mesurés) | `nft_transfer_call_receivers` |
| 3 | Annonce retirée même si le destinataire garde la carte | Retirée seulement en cas de retour réel | `resolve_keeps_listing_when_receiver_keeps_card`, `resolve_removes_listing_only_on_real_return` |
| 4 | Remise en vente plus chère avant l'achat | `buy(token_id, expected_price)` | `buy_with_stale_price_fails`, `integrated_market` |
| 5 | Poids mythique avec engagements tous à 0 | Un engagement (ou une carte) de poids non nul exigé par rareté pondérée | `mythic_weight_needs_a_weighted_commitment` |
| 6 | Sel court ou réutilisé | Sel de 32 octets exigé, `content_hash` en double refusé, script `scripts/gen_mythics.py` | `short_sel_is_rejected`, `duplicate_content_hash_is_rejected`, `gen_mythics_script_matches_contract_hashes` |
| 7 | Stockage des approbations non rendu | Rendu au transfert, à la vente, au burn et à la résolution | `approvals_storage_is_refunded_on_transfer_sale_and_burn` |
| 8 | Révélation de 100 scellées | Mesurée à 85 Tgas, pas de pagination nécessaire | `reveal_with_100_sealed_cards` |
| 9 | `Vec` par compte non paginé | `(compte, rang) → pack_id` + compteur, vues paginées | `packs_by_owner_is_paginated` |
| 10 | Pack sans issue après 10 tentatives | État et événement `Stuck`, sans remboursement (documenté) | `pack_becomes_stuck_after_max_attempts` |
| 11 | Écarts de doc | Tirage échoué recalculable (et pourquoi c'est sans effet), graines d'un reçu échoué non journalisées, `get_min_buy_gas` corrigé, k > 1 inutile contre le dernier producteur | — |

## Revue du chargement par lots (11/11/2026) : corrections

| # | Point | Correction | Tests |
|---|---|---|---|
| 1 | Vues à 183, 184 et 229 Tgas sur une série maximale, dont dépendait le vérificateur | `get_series_header` (4,7 Tgas), `get_series_table_hash` renvoie le hash stocké (4,3 Tgas), `get_series_cards` lue par blocs et `get_rates` paginées (22 et 25 Tgas par page de 200) ; le vérificateur lit en-tête + pages au même bloc et recalcule le hash lui-même | `header_and_pages_rebuild_the_stored_hash`, `rates_are_paginated_and_match_full_table`, `max_size_series_fits`, `catalogue_v2_batched_load_and_packs`, `verifier/tests/test_pages.py` |
| 2 | Brouillons abandonnés payés par le contrat | `create_series_batched` et `append_series_cards` payables (dépôt ≥ stockage mesuré, excédent rendu), `delete_draft` (stockage libéré rendu à l'owner, borné par le payé), dépôts dans le manifeste du script | `batched_create_requires_storage_deposit`, `append_requires_storage_deposit`, `storage_charge_is_measured_and_excess_refunded`, `delete_draft_*`, `draft_storage_is_paid_by_owner_and_refunded_on_delete` |
| 3 | Coupe de l'en-tête à la première occurrence de `"cards":[` | Motif unique exigé (panique sinon), `]` exigé après ; ordre des champs de `SeriesTable` verrouillé par un test | `series_table_field_order_is_locked`, `cards_key_twice_panics`, `cards_key_missing_panics` |

## Limites connues

- **Graine.** Un producteur de bloc connaît la graine de son bloc et peut retenir un bloc. L'avantage est limité au
  dernier reçu, et k > 1 n'y change rien. Pas de VRF externe.
- **Packs `Stuck`.** Après 10 tentatives échouées (relancées par l'acheteur seul), le pack est remboursable une fois
  (`refund_stuck_pack`) : prix et stockage non utilisé.
- **Révélation des mythiques hors chaîne.** Tant que l'owner n'a pas révélé, la carte reste scellée. Il peut aussi ne
  jamais révéler ; la carte reste alors une mythique sans adossement. Une vue RPC `compute_mythic_commitment`
  transmet le secret au nœud interrogé : il vaut mieux calculer les engagements hors ligne.
- **Retombée.** Elle ne fait que descendre. Si mythique et légendaire sont épuisées, la valeur attendue baisse : c'est
  voulu, puisque attendre ne rapporte rien.
- **Gaz du dernier reçu.** Il est fixe (120 Tgas) et a été mesuré à 48,4 Tgas au pire (2 000 cartes, 10 cartes par
  booster, toutes les mécaniques dont le gold pack à planchers et la table de valeur, raretés épuisées en cascade ; 49,1
  avant) et à 23,3 Tgas sans cascade (chaînes maximales ; 61 Tgas avant le stockage minimal). Une table plus grosse que les limites validées n'est pas possible (2 000 cartes,
  20 mythiques).
- **Grosse série.** Par lots, le stockage de la table (1,5 NEAR pour la série v2) est payé par l'owner. Restent à la
  charge du contrat : `create_series` et `replace_series_table(_batched)` (un seul appel, 200 cartes au plus) et ce que
  l'ouverture ajoute (quelques dizaines d'octets). Un brouillon abandonné se supprime par `delete_draft` ; il laisse
  un emplacement de 184 o. `get_series_table` d'une table de taille maximale renvoie 1,7 Mo pour 183 Tgas : préférer
  `get_series_header` et `get_series_cards`.
- **Stockage.** Le prépayé ne couvre pas les graines des relances au-delà du premier essai (81 o par relance mesurés,
  à la charge du contrat ; le remboursement au tirage vaut alors 0),
  ni pour les entrées de liste d'un acheteur du marché ou d'un destinataire de transfert (environ 120 o au premier,
  8 o ensuite, à la charge du contrat).
- **Mécaniques.** L'oracle de prix est de confiance, comme le redeemer : le contrat ne vérifie ni le cours ni le stock
  de jetons. Il ne peut ressusciter que les cartes de la liste hachée, et l'owner ne le change qu'avec 24 h de délai
  (le retrait est immédiat). Le plafond de packs rush est par compte : un acteur à nombreux comptes le contourne (gain
  de 0,64 prix par compte et par rush, `docs/mecaniques-spec.md`, section 4). La couverture de la table rush (≤ 80 %) n'est contrôlée que hors chaîne, par `build_series.py`. Le
  compteur de pitié est lié au compte (variante NFT revendable non faite). Voir `docs/mecaniques-spec.md`, sections 7 et 10.
- **Valeur.** Le contrat tire et répartit une valeur en yoctoNEAR et la transmet au redeemer ; il ne finance rien et
  ne vérifie pas que le redeemer puisse livrer. Les tables de `serie-exemple.json` sont provisoires (calibrage dans
  `sim/`).
- **Revenus.** Retirables par `withdraw_revenue`, au-delà des engagements (section « Trésorerie »). Avant la v3, il n'existait volontairement aucune
  méthode de retrait, faute de mécanique d'approvisionnement (toujours à concevoir).
- **Redeemer.** Il est de confiance et peut être changé par l'owner. Un redeemer qui réussit sans livrer, ou qui panique
  après avoir livré, casse la garantie. Si le callback manque de gaz (20 Tgas fixes ; le `redeem` complet brûle 10,4 Tgas), la carte
  reste bloquée en `Redeeming`.
- **Owner.** L'owner garde la clé : pas de gel du code, pas de build reproductible configuré. Les tables ouvertes sont
  immuables par le code, pas par la gouvernance.
- **Hors sandbox.** Mesuré sur testnet (deux déploiements, `docs/testnet.md`), pas sur mainnet. Aucun gold pack ni
  aucune mythique n'est sorti sur testnet (probabilités trop faibles pour 31 boosters) : ces chemins ne sont couverts
  que par les tests unitaires et sandbox. MetaMask n'a pas été testé de bout en bout.

## TODO

- Approvisionnement des jetons, contrôle de couverture, retrait réel : un vrai redeemer à la place du mock.
- Sortie de secours sur NEAR, et récupération d'une carte bloquée en `Redeeming` (délai puis restauration).
- Retrait des revenus : fait en v3 (réserve ≥ engagements) ; reste un plafond par coin et la réserve des adossements
  qui ne sont pas en NEAR.
- Build reproductible (`[package.metadata.near.reproducible_build]`), suppression des clés d'accès complet après
  déploiement, publication du hash du code.
- Recalcul externe de `random_seed` à partir de `random_value` et `action_hash` (rythme des reçus et gaz mesurés sur
  testnet, `docs/testnet.md`).
- Script de vérification public (JS ou Python) reprenant `verify_pack_event` de `tests/sandbox.rs`.
- Indexation des cartes scellées en attente de révélation.
- Revue de sécurité et audit avant tout public.
