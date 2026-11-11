# Mécaniques : spécification du contrat (11/11/2026)

Mise en œuvre de `docs/mecaniques.md` dans `contract/` (branche `feat/mecaniques-contrat`), avec les corrections tirées
de la simulation de la série 3 (`sim/RAPPORT.md`, branche `feat/mecaniques-sim`). Rien n'est déployé. Les hauteurs sont
en blocs, avec 0,6 s par bloc supposé (non vérifié dans le repo).

## 0. Principes communs

- **Tout est dans la table hachée.** Les paramètres vivent dans `SeriesTable.mechanics`, le dernier champ de la table.
  Ils sont donc couverts par `table_hash = sha256(serde_json::to_vec(table))`. **Sans mécanique, le champ est absent du
  JSON** (`skip_serializing_if`) : une table d'avant garde exactement ses octets, son hash et ses tirages.
  `draw_vectors.json`, régénéré par le nouveau code, ne change pas d'un octet.
- **Ordre JSON** (verrouillé par `hash_stream::tests::mechanics_field_order_is_locked`) :
  `"mechanics":{"gold_weights":…|null,"pity":{"p0_ppm","k_ppm","n_max"}|null,"burn":{"floor_bps"}|null,"rush":{"ratio_bps","min_packs","window_blocks","baseline_blocks","bucket_blocks","duration_blocks","cooldown_blocks","weights"}|null}`.
- **Tout état qui influence un tirage est figé puis journalisé.** Le vérificateur recalcule chaque tirage à partir des
  seuls événements (`pack_bought`, `pack_revealed`, `card_redeemed`, `card_resurrected`), sans archive d'état :
  `verifier/` `SeriesReplay`.
- **Aléa.** Un seul aléa, `acc`, comme avant. Le tirage « gold ou pas » utilise un nouveau tag : `roll(acc, 0, 2)`. Les
  tags 0 (rareté) et 1 (carte) par emplacement ne changent pas.
- **Dernier reçu du tirage sans échec lié au résultat.** La pitié, les burns et la table de taux sont lus et écrits dans
  `finalize_pack`, sans aucun `require`. Le stockage ajouté est borné et prépayé (entrée de pitié comprise), et le gaz
  reste fixe (120 Tgas, 19,5 Tgas au pire mesurés).

Paramètres par défaut, ceux de `contract/scripts/serie-exemple.json` (série v2, poids de base 2 / 20 / 180 / 800 / 8 998) :

| Mécanique | Paramètres par défaut |
|---|---|
| Table or | multiplicateurs mythique × 4, légendaire × 4, épique × 3, rare × 2, la commune compense : 8 / 80 / 540 / 1 600 / 7 772 |
| Pitié | N = 20, p0 = 2 % (20 000 ppm), k = 0,2 % (2 000 ppm) |
| Burns | plancher 25 % (`floor_bps` = 2 500), renormalisation entre brûlables de la rareté |
| Rush | palier relatif × 2,5 (`ratio_bps` = 25 000), 50 packs au moins, fenêtre courte 6 000 blocs (1 h), fenêtre longue 144 000 (24 h), seaux de 1 500 (15 min, 96 seaux), rush de 3 000 blocs (30 min), pause de 36 000 (6 h) |
| Table rush | mythique × 1,51, légendaire × 1,51, épique × 1,34, rare × 1,17 : 3 / 30 / 241 / 936 / 8 790 |
| Couverture (hors chaîne) | base 58,7 %, or 184 %, rush 79,9 % ≤ 80 % (valeurs de rareté de la série 3) |

Le rapport de la simulation propose × 2,5 pour le palier. Le message de coordination citait × 1,5 comme exemple. C'est un
paramètre, et le défaut suit le rapport.

## 1. Stockage par carte minimal

Une carte ne stocke que sa référence :

- `token_id = pack_id × 10 + emplacement`, en décimal canonique (10 cartes par booster au plus) ;
- le pack porte la série, le tirage compact de chaque emplacement (`PackDraw`, 31 o : rolls, raretés, type, index) et
  un `CardSlot` de 10 o (propriétaire `None` tant que l'acheteur la détient, état, positions dans les listes) ;
- les listes NEP-181 (cartes d'un compte, toutes les cartes, packs d'un compte) sont rangées par blocs de 32 ou 64, soit
  8 o par carte. Un retrait échange l'entrée avec la dernière ;
- les métadonnées NEP-177 (`title`, `media`, `reference`, `copies`, `issued_at`, `extra`), l'adossement et le statut
  scellé ou révélé des mythiques sont **reconstruits à la lecture** à partir de la table (`nft_token`, `nft_tokens`,
  `nft_tokens_for_owner`, `get_card`, `get_backing`). `issued_at` vient de l'heure du tirage, stockée dans le pack ; une
  mythique créée scellée prend `updated_at` = date de sa révélation ;
- `price_paid` et `storage_prepaid` de `get_pack` se déduisent de la série ; l'`acc` de chaque graine se recalcule en
  chaînant depuis `initial_acc`.

NEP-171, 178 et 181 sont réécrits (sans `NonFungibleToken`), avec les mêmes méthodes, les mêmes messages et la même
politique de stockage des approbations. `reveal_mythic` ne réécrit plus les cartes scellées : 5 Tgas au lieu de 85,6.

| Stockage d'un pack (mesuré en sandbox) | Avant | Après |
|---|---|---|
| Série v2 (5 cartes), 12 packs, au plus | 3 965 o | 848 o sans mécanique, **964 o avec toutes les mécaniques** (premier achat d'un compte compris) |
| Série v2, prépayé (`storage_per_pack`) | 15 715 o | 1 467 o (0,0147 NEAR) |
| Table de 4 cartes | 4 235 o / 11 655 prépayés | 888 o / 1 227 |
| 200 cartes aux chaînes maximales, 5 / 10 cartes par pack | 7 888 / 14 975 o | 829 / 858 o |
| 2 000 cartes, 10 cartes par pack, toutes les mécaniques | (non mesuré) | 1 259 o au premier achat, 866 à 958 o ensuite, 1 887 prépayés |

Un pack déjà connu du compte coûte environ 560 o ; le premier achat ajoute les compteurs du compte et l'entrée de pitié.
Le prépayé est une borne calculée à l'ouverture (`worst_case_pack_storage`) : comptes de 64 caractères, nouveaux blocs de
liste, premier achat. Comme avant, le surplus n'est pas rendu (un remboursement dépendrait du résultat).

## 2. Compteur de pitié

- **État** : `pity: (compte, série) → n`, packs consécutifs sans gold pack, lu et écrit par le dernier reçu.
  Vue : `get_pity(account_id, series_id)` → `n`, `p_ppm`, `guaranteed_in`.
- **Formule** : `p(n) = min(10⁶, p0_ppm + k_ppm × n)` ppm ; `gold_roll = u128_be(sha256(acc ‖ 0x00 ‖ 0x02)[0..16]) mod 10⁶` ;
  gold pack (pitié) si `n + 1 ≥ N` ou `gold_roll < p(n)`. Avec N = 1, tous les packs sont or.
- **Table du pack** (`draw::pack_mode`) : gold pack de pitié → table or ; sinon, pack rush → table rush ; sinon base.
  La pitié l'emporte sur le rush.
- **Mise à jour** : `n ← 0` après un gold pack **ou un pack rush** (le rapport : « un gold pack de rush remet le compteur
  à zéro »), sinon `n ← n + 1`. Le compteur n'atteint jamais N.
- **Haché** : `gold_weights`, `pity`. **Journalisé** : `pack_revealed.mechanics.pity` = `before`, `gold_roll`, `p_ppm`,
  `gold`, `after`, et `mode`. Le vérificateur recalcule `gold_roll`, `p`, la décision et `after`, puis chaîne le
  compteur de chaque compte d'un booster à l'autre.
- **Coût** : environ 120 o au premier tirage du compte dans la série (prépayé), une lecture et une écriture dans le dernier
  reçu (négligeable).
- **Variante « compteur dans un NFT revendable » (non faite).** Pour l'ajouter : à la première ouverture d'un compte,
  créer une carte spéciale « compteur » (`CardKind::Counter`, index = série) qui porte `n` dans son emplacement. Il faut
  alors lire le compteur depuis cette carte au tirage, au lieu de `(compte, série)`. Il faut aussi la journaliser par
  `token_id` dans `pack_revealed.mechanics.pity.counter_token` et suivre les transferts dans le rejeu : le compteur suit
  la carte, pas le compte. Un compte qui reçoit un compteur alors qu'il en détient déjà un en garde deux, et il faut
  choisir lequel s'applique (le plus haut, ou un compteur actif désigné). La simulation note que, avec un compteur
  revendable, la couverture tend vers g_∞ (67,5 %) : il faudrait alors calibrer sur g_∞.

## 3. Rareté pilotée par les burns

- **Par carte** : une carte = un coin dans notre catalogue. Seules les cartes visibles sont concernées, pas les
  mythiques.
- **Le tirage de rareté ne change pas.** `rarity_roll` utilise seulement les poids de rareté de la table du pack. Les
  burns n'interviennent que dans le choix de la carte **à l'intérieur de la rareté**, et dans la retombée si une rareté
  est épuisée. C'est déjà la structure de `available_weight`, qui est par rareté : le test `burns_shift_weight…`
  compare `rarity_roll` avec et sans burns.
- **Renormalisation entre brûlables** (variante retenue par la simulation). Pour une brûlable `i` (adossée par la table,
  ou ressuscitée) de poids `w`, avec `e` cartes émises et `b` brûlées, son poids brut vaut 0 si elle est épuisée par son
  plafond, `w` si `e = 0`, et sinon `brut = max(⌊w × (e − b) / e⌋, ⌊w × floor_bps / 10⁴⌋, 1)`.
  On pose ensuite, par rareté, `E = Σ brut` et `B = Σ poids disponibles` des brûlables. Le poids dans la rareté vaut
  `brut × B` pour une brûlable, `w × E` pour une carte de collection (`w` si `E = 0`). La part des brûlables dans la rareté
  reste donc exactement `B / (B + Σ w des cartes de collection)` : le poids qu'une brûlable perd revient aux autres
  brûlables de la même rareté. La probabilité de tirer une brûlable et la couverture ne bougent pas. Tout est en entiers
  (u128, au plus 2⁸⁶), sans arrondi sur les parts. `card_roll` est donc stocké sur 128 bits.
- **Plancher** : 25 % du poids de base, tant que la carte n'est pas épuisée par son plafond. Un coin brûlé jusqu'à la
  dernière carte garde ce plancher : il ne s'éteint jamais (test `raw_burn_weight_rounding_and_floor`, sandbox).
  Une rareté qui n'a qu'une brûlable ne change pas : la renormalisation lui rend tout son poids.
- **État** : `BurnState { burned[i], seq }` par série, mis à jour dans `on_redeem_complete` (burn réussi d'une carte
  visible). Les burns de mythiques ne comptent pas. `Series.draw_cards[i].backed` passe à vrai à la résurrection.
- **Haché** : `burn.floor_bps`. **Journalisé** : `card_redeemed` = `series_id`, `kind`, `index`, `burn_seq` (numéro
  d'ordre du burn dans la série) ; `card_resurrected` = `card_index`, `resurrect_seq` ; `pack_revealed.mechanics` =
  `burn_seq`, `resurrect_seq` (état lu au tirage). Le vérificateur applique les burns et les résurrections de numéro
  ≤ ceux du tirage, et signale un numéro manquant.
- **Vues** : `get_series.burned`, `get_series.burn_seq`, `get_burns` (paginée), `get_rates` : `effective_weight` par carte
  et `effective_card_weight` par rareté (le modulo de `card_roll`). `available_card_weight` garde son sens d'avant.
- **Coût** : 4 o par carte de la table pour les compteurs, payés par l'owner au chargement (6,6 Ko pour la série v2) ;
  `on_redeem_complete` 3,7 Tgas au plus (20 fixes) ; le dernier reçu fait deux passes de plus sur les cartes de la rareté
  (voir « Gaz »).

## 4. Gold rush collectif

Corrections de la simulation : un palier fixe s'emballe (69 % des packs en or à trafic × 2). Le palier est donc
**relatif au trafic des 24 dernières heures**, avec une **pause** entre deux rushs et une **table rush propre**.

- **Fenêtre glissante à coût borné** : `m_l = baseline_blocks / bucket_blocks` seaux (≤ 96, anneau dans la série),
  `m_w = window_blocks / bucket_blocks`. Le seau de la hauteur `h` est `b = ⌊h / B⌋`. Un achat incrémente son seau ;
  `C_w` et `C_l` comptent les achats des `m_w` et des `m_l` derniers seaux, celui-ci compris.
- **Pack rush** : un déclenchement a eu lieu à `t` et `t < h ≤ t + duration_blocks`. **L'état est figé à l'achat**
  (`buy_pack`, bit `FLAG_RUSH` du pack). Retarder la révélation ne change rien.
- **Déclenchement** à l'achat `h` si toutes ces conditions tiennent :
  - aucun rush ni pause en cours : `h > t + duration + cooldown`, ou aucun déclenchement encore ;
  - la fenêtre longue est remplie : `h ≥ premier achat de la série + baseline_blocks` ;
  - `C_w ≥ min_packs` et `C_w × m_l × 10⁴ ≥ ratio_bps × C_l × m_w`, c'est-à-dire un rythme court au moins `ratio` fois
    le rythme moyen sur 24 h.

  L'achat qui déclenche n'est pas lui-même rush. Les achats faits pendant le rush comptent dans les fenêtres.
- **Validation à la création** : `ratio_bps ≥ 10⁴`, `ratio_bps × m_w < 10⁴ × m_l` (sinon le palier serait
  inatteignable), fenêtres multiples des seaux, `m_w < m_l ≤ 96`, durée ≥ 1, `min_packs ≥ 1`, table rush valide et
  **distincte de la table or**.
- **Couverture ≤ 80 %, contrôlée hors chaîne.** Le contrat ne connaît pas la valeur des cartes (un adossement est une
  quantité de jetons, pas un prix). `scripts/build_series.py` calcule la couverture de chaque table à partir de
  `coverage_check.rarity_value` (valeur moyenne d'un emplacement par rareté, en multiples du prix). Il **refuse** une table
  rush au-delà de `max_rush` (0,80) et écrit les couvertures dans `manifest.json`. Les valeurs de l'exemple (0 / 0,18 / 4 /
  10 / 55) redonnent les 58,6 / 184 / 80 % de la série 3. Elles sont à recaler sur la simulation à chaque série.
- **Haché** : tout `rush` (table comprise). **Journalisé** : `pack_bought.rush` = `active`, `window_count`,
  `baseline_count`, `triggered`, `last_trigger`, `rush_until` ; `pack_revealed.mechanics.rush`. Le vérificateur rejoue
  l'anneau à partir des `pack_bought` (hauteurs) et compare chaque valeur. Vue : `get_rush_state(series_id, at_height)`.
- **Coût** : anneau de 96 × 12 o dans la série, payé par l'owner à la création ; `buy_pack` lit 96 seaux et en écrit un
  (+1 Tgas mesuré sur la série v2 : 6,9 → 7,9 Tgas).

## 5. Résurrection des coins morts

- **Rôle `price_oracle`** abstrait, comme le redeemer : `set_price_oracle(Option<AccountId>)` (owner),
  `set_resurrected(series_id, card_index, backing)` (oracle seulement, payable : stockage mesuré, excédent rendu).
- **Portée** : cartes visibles **épiques et légendaires** seulement (rare et commune refusées, recommandation de la
  simulation : 94 % du coût viendrait des communes). La carte ne doit pas être déjà adossée par la table. Un nouvel appel
  remplace l'adossement.
- **Effet** : la carte devient brûlable pour les nouvelles cartes **et** pour les exemplaires existants, puisque
  l'adossement est lu à la demande (`get_backing`, `redeem`, `extra.burnable` des métadonnées). Elle rejoint aussi les
  brûlables de sa rareté pour la renormalisation des burns (`resurrect_seq`).
- **Événement** `card_resurrected` : `series_id`, `card_index`, `card_id`, `backing`, `previous`, `oracle_id`,
  `resurrect_seq`, `block_height`. Aucun `nft_metadata_update` : il faudrait lister tous les exemplaires de la carte.
- **Mock** : `contract/mock-oracle/` (`push_resurrection`, réservé à son opérateur) appelle `set_resurrected`. Aucun prix
  n'est lu.
- **À brancher pour un vrai oracle** : une source de prix fiable et résistante à la manipulation (plusieurs sources,
  médiane, TWAP sur plusieurs heures, car les micro-caps se manipulent facilement) ; une règle de seuil publiée, par
  coin, avec une durée minimale au-dessus du seuil ; l'achat effectif du stock de jetons (via Intents) **avant** l'appel,
  puisque l'adossement vaut promesse de livraison au redeemer ; un fonds dédié (la simulation propose 1,5 % du prix,
  réévalué chaque année) ; une gouvernance du compte oracle (multisig, délai). Le contrat ne vérifie ni le prix ni le
  stock : il fait confiance à l'oracle, comme au redeemer.
- **Coût** : environ 150 o par carte ressuscitée (payés par l'oracle), une réécriture de la série.

## 6. Gaz (sandbox, near-sandbox 0.4.0)

| Cas | Avant | Après |
|---|---|---|
| Série v2 complète, toutes les mécaniques, 12 packs à 160 Tgas | dernier reçu 35,3 Tgas, total 48 | dernier reçu **14,1 Tgas**, `buy_pack` 7,9, total 27,9 |
| 2 000 cartes aux chaînes maximales, 10 cartes par pack, toutes les mécaniques | dernier reçu 58,8 Tgas (sans mécanique) | dernier reçu **19,5 Tgas** au pire (table or), `buy_pack` 10,2, total 35,7 |
| `on_redeem_complete` avec burns | (pas de compteur) | 3,7 Tgas sur 20 fixes |
| `redeem` complet | 10,4 Tgas | 8,1 Tgas |
| `reveal_mythic`, 100 scellées | 85,6 Tgas | 5,0 Tgas |
| `get_rates`, page de 200, 2 000 cartes avec burns | 25,4 Tgas | 32,3 Tgas |

Le budget du dernier reçu reste de 120 Tgas fixes et `min_gas` de 160 Tgas. La marge passe d'un facteur 2 à un facteur 6.

## 7. Ce qui reste ouvert

- Variante du compteur dans un NFT revendable (section 2).
- Un vrai oracle (section 5) et l'approvisionnement des jetons.
- Valeurs de rareté de `coverage_check` : à reprendre de la simulation à chaque série. Le contrat ne contrôle pas la
  couverture.
- Temps de bloc réel (0,6 s supposé) pour convertir 1 h, 24 h et 6 h en blocs.
- `nft_metadata_update` pour les exemplaires d'une carte ressuscitée (non émis).
- Mesures sur testnet.
