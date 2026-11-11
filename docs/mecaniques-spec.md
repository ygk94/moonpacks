# Mécaniques : spécification du contrat (11/11/2026)

Mise à jour du 11/11 (branche `feat/valeur-contrat`) : gold pack à plancher de rareté par emplacement (section 8) et
valeur aléatoire en jetons par pack (section 9).

Mise à jour du 11/11, branche `feat/gold-rare` (décisions du porteur) : **gold pack ultra rare sans garantie** (pitié en
ppb, de 1 sur 50 000 à 1 sur 25 000, section 2), **mythique à 1 pour 1 000 000 de packs classiques** (poids de base sur
2·10⁷), **mythique à 1 % au dernier emplacement du gold pack**, **valeur moyenne 75 % pour le normal et le rush**, et
**mythiques anonymes** (« ? », section 11).

Mise en œuvre de `docs/mecaniques.md` dans `contract/` (branche `feat/mecaniques-contrat`), avec les corrections tirées
de la simulation de la série 3 (`sim/RAPPORT.md`, branche `feat/mecaniques-sim`). Rien n'est déployé. Les hauteurs sont
en blocs, avec 0,6 s par bloc supposé (non vérifié dans le repo).

## 0. Principes communs

- **Tout est dans la table hachée.** Les paramètres vivent dans `SeriesTable.mechanics`, le dernier champ de la table.
  Ils sont donc couverts par `table_hash = sha256(serde_json::to_vec(table))`. **Sans mécanique, le champ est absent du
  JSON** (`skip_serializing_if`) : une table d'avant garde exactement ses octets, son hash et ses tirages.
  `draw_vectors.json`, régénéré par le nouveau code, ne change pas d'un octet.
- **Ordre JSON** (verrouillé par `hash_stream::tests::mechanics_field_order_is_locked`) :
  `"mechanics":{"gold":{"slots":[{"floor","weights"|null,"burnable"}…]}|null,"pity":{"p0_ppb","k_ppb","p_max_ppb","n_max"|null}|null,"burn":{"floor_bps","prior_k"}|null,"rush":{"ratio_bps","min_packs","window_blocks","baseline_blocks","bucket_blocks","duration_blocks","cooldown_blocks","max_per_account","weights"}|null,"resurrection":{"eligible":[…]}|null,"value":{"normal":[[bps,poids]…],"gold":[…],"rush":[…],"multipliers":{…}}|null}`.
  L'ancienne table de poids or (`gold_weights`) est retirée : le gold pack se décrit par planchers (section 8).
- **Tout état qui influence un tirage est figé puis journalisé.** Le vérificateur recalcule chaque tirage à partir des
  seuls événements (`pack_bought`, `pack_revealed`, `card_redeemed`, `card_resurrected`), sans archive d'état :
  `verifier/` `SeriesReplay`.
- **Aléa.** Un seul aléa, `acc`, comme avant. Le tirage « gold ou pas » utilise un nouveau tag : `roll(acc, 0, 2)`, la
  valeur du pack un autre : `roll(acc, 0, 3)`. Les tags 0 (rareté) et 1 (carte) par emplacement ne changent pas.
- **Dernier reçu du tirage sans échec lié au résultat.** La pitié, les burns et la table de taux sont lus et écrits dans
  `finalize_pack`, sans aucun `require`. Le stockage ajouté est borné et prépayé (entrée de pitié comprise), et le gaz
  reste fixe (120 Tgas ; 48,4 Tgas au pire mesuré, raretés épuisées en cascade, gold pack et valeur compris). La valeur
  ne peut pas déborder : la validation exige que `prix × V_max × multiplicateur_max` tienne sur u128.

Paramètres par défaut, ceux de `contract/scripts/serie-exemple.json` (série v2, poids de base 5 / 40 000 / 360 000 /
1 600 000 / 17 999 995 sur 2·10⁷ : les proportions d'avant, 20 / 180 / 800 / 8 998 sur 10⁴, pour les raretés visibles ;
mythique 5 / 2·10⁷ par emplacement sur les 4 premiers, le 5ᵉ étant tiré parmi les brûlables, soit **1 mythique pour
1 000 000 de packs** normaux) :

| Mécanique | Paramètres par défaut |
|---|---|
| Gold pack | 5 cartes, aucune commune : emplacements 1 et 2 rare ou mieux (le 2 parmi les brûlables), 3 et 4 épique ou mieux (poids de base tronqués), 5 légendaire 99 % ou mythique 1 % (section 8) |
| Valeur | normale 20 à 200 % du prix, moyenne 75 % ; rush même forme, moyenne 75 % ; gold 100 à 800 %, moyenne 218,5 % (inchangé, négligeable) ; multiplicateurs commune 1, rare 2, épique 5, légendaire 20 (section 9). Tables de la simulation : `sim/resultats/serie5/tables-valeur.json` (`--tables-valeur`) |
| Pitié | sans garantie (`n_max` = `null`) ; p0 = 1 / 50 000 (20 000 ppb), k = 20 ppb par pack, plafond 1 / 25 000 (40 000 ppb) atteint en 1 000 packs |
| Burns | plancher 25 % (`floor_bps` = 2 500), a priori K = 20 (`prior_k`), renormalisation entre brûlables de la rareté |
| Rush | palier relatif × 2,5 (`ratio_bps` = 25 000), **100 packs au moins** (50 avant la revue), fenêtre courte 6 000 blocs (1 h), fenêtre longue 144 000 (24 h), seaux de 1 500 (15 min, 96 seaux), rush de 3 000 blocs (30 min), pause de 36 000 (6 h), **3 packs rush au plus par compte et par rush** (`max_per_account`) |
| Résurrection | liste hachée `resurrection.eligible` : règle `dead_epic_legendary` de `build_series.py` (épiques et légendaires « mort… » du catalogue, non adossées : 86 cartes pour la série v2) ; changement d'oracle après 144 000 blocs (24 h, `oracle_delay_blocks` de `new`) |
| Table rush | mythique × 1, légendaire × 1,51, épique × 1,34, rare × 1,17 : 5 / 60 400 / 482 400 / 1 872 000 / 17 585 195 (mythique : 1 pour 1 000 000 de packs rush, comme en base) |
| Couverture (hors chaîne) | avec table de valeur : valeur moyenne de chaque table (base 75 %, gold 218,5 %, rush 75 % ≤ 80 %) ; sans table de valeur : valeurs de rareté de `coverage_check` |

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
  `nft_tokens_for_owner`, `get_card`, `get_backing`). `issued_at` vient de l'heure du tirage, stockée dans le pack. Les
  métadonnées d'une mythique sont anonymes et ne changent jamais (section 11) ;
- `price_paid` et `storage_prepaid` de `get_pack` se déduisent de la série ; l'`acc` de chaque graine se recalcule en
  chaînant depuis `initial_acc`.

NEP-171, 178 et 181 sont réécrits (sans `NonFungibleToken`), avec les mêmes méthodes, les mêmes messages et la même
politique de stockage des approbations. `reveal_mythic` ne réécrit plus les cartes scellées : 5 Tgas au lieu de 85,6.

| Stockage d'un pack (mesuré en sandbox) | Avant | Après | Avec gold pack et valeur (11/11) |
|---|---|---|---|
| Série v2 (5 cartes), au plus | 3 965 o | 848 o sans mécanique, 964 o avec toutes les mécaniques (premier achat d'un compte compris) | **971 o** (22 packs, dont un gold) |
| Série v2, prépayé (`storage_per_pack`) | 15 715 o | 1 597 o (0,016 NEAR) avec toutes les mécaniques | 1 605 o |
| Table de 4 cartes | 4 235 o / 11 655 prépayés | 888 o / 1 227 | inchangé (sans mécanique) |
| 200 cartes aux chaînes maximales, 5 / 10 cartes par pack | 7 888 / 14 975 o | 829 / 858 o | inchangé (sans mécanique) |
| 2 000 cartes, 10 cartes par pack, toutes les mécaniques | (non mesuré) | 1 254 o au premier achat, 860 à 946 o ensuite, 2 017 prépayés | 1 266 o au premier achat, 879 à 947 o ensuite, 2 025 prépayés (gold pack de 10 emplacements) |

La valeur ajoute 7 o par pack (`Pack::value` : `bps` et le masque des brûlables), pas 16 o par carte : les montants se
recalculent depuis ces 7 o, la table et les raretés des tirages (`draw::split_value`). Le prépayé compte 8 o de plus
(`PACK_VALUE_BYTES`) et, si le gold pack a plus d'emplacements que `cards_per_pack`, les cartes en plus.

Un pack déjà connu du compte coûte environ 560 o ; le premier achat ajoute les compteurs du compte et l'entrée de pitié.
Le prépayé est une borne calculée à l'ouverture (`worst_case_pack_storage`) : comptes de 64 caractères, nouveaux blocs de
liste, premier achat. Comme avant, le surplus n'est pas rendu (un remboursement dépendrait du résultat).

## 2. Compteur de pitié (gold pack ultra rare, sans garantie)

- **État** : `pity: (compte, série) → n`, packs consécutifs sans gold pack, lu et écrit par le dernier reçu.
  Vue : `get_pity(account_id, series_id)` → `n`, `p_ppb`, `packs_to_max` (packs avant le plafond, 0 s'il est atteint),
  `guaranteed_in` (`null` sans `n_max`), `params`.
- **Formule** (ppb, parties par milliard : la pente, 0,02 ppm par pack, ne tient pas en ppm entiers) :
  `p(n) = min(p_max_ppb, p0_ppb + k_ppb × n)`, calculé en u128 ; `gold_roll = u128_be(sha256(acc ‖ 0x00 ‖ 0x02)[0..16]) mod 10⁹` ;
  gold pack (pitié) si `gold_roll < p(n)`. **Aucune garantie** : `n_max` est optionnel (`null` par défaut) ; avec
  `n_max = N`, le N-ième pack sans gold pack en est un (`n + 1 ≥ N`), ce qui sert aux tests.
- **Défaut** : `p0_ppb` = 20 000 (1 / 50 000), `p_max_ppb` = 40 000 (1 / 25 000), `k_ppb` = 20, soit le plafond atteint en
  (40 000 − 20 000) / 20 = **1 000 packs** (paramétrable : `k = (p_max − p0) / packs`).
- **Bornes** (validées à la création) : `p0_ppb`, `k_ppb`, `p_max_ppb` ≤ 10⁹ ; `p0_ppb ≤ p_max_ppb` ; `n_max` absent ou
  1 à 10 000 ; refus si `p_max_ppb = 0` sans `n_max` (gold pack inatteignable). `n` est un u32 saturé : aucun
  dépassement, même sans garantie.
- **Table du pack** (`draw::pack_mode`) : gold pack de pitié → gold pack à planchers (section 8) et table de valeur gold ;
  sinon, pack rush → table rush et table de valeur rush ; sinon base et table de valeur normale. La pitié l'emporte sur le
  rush.
- **Mise à jour** (`draw::pity_after`) : `n ← 0` après un gold pack **seulement** ; sinon `n ← n + 1`, **pack rush
  compris** (avant le 11/11, un pack rush remettait aussi le compteur à 0 : la montée ne servait à rien).
- **Fréquence** (simulation série 5, `sim/resultats/serie5/`) : 1 gold pack pour ~25 250 packs pour un joueur qui ne
  s'arrête pas (g_∞), ~48 000 sur la population de la série 4 (la plupart des joueurs ouvrent peu de packs).
- **Haché** : `gold`, `pity`. **Journalisé** : `pack_revealed.mechanics.pity` = `before`, `gold_roll`, `p_ppb`,
  `gold`, `after`, et `mode`. Le vérificateur recalcule `gold_roll`, `p`, la décision et `after`, puis chaîne le
  compteur de chaque compte d'un booster à l'autre. Il lit encore l'ancien format (`p0_ppm`, `k_ppm`, `n_max`
  obligatoire, `p_ppm`, remise à 0 après un pack rush) pour les séries déjà déployées sur testnet.
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
- **Renormalisation entre brûlables** (variante retenue par la simulation). Pour une brûlable `i` adossée par la table,
  de poids `w`, avec `e` cartes émises et `b` brûlées, son poids brut vaut 0 si elle est épuisée par son plafond, `w`
  si `e = 0`, et sinon **`brut = max(⌊w × (e − b + K) / (e + K)⌋, ⌊w × floor_bps / 10⁴⌋, 1)`**, avec `K = prior_k`
  (lissage par a priori : tout se passe comme si chaque carte avait `K` exemplaires de plus, émis et jamais brûlés).
  **Carte ressuscitée** : on calcule d'abord `E₀ = Σ brut` et `B₀ = Σ poids disponibles` des brûlables **de la table**
  de la rareté ; son poids brut vaut `min(brut propre, max(⌊w × E₀ / B₀⌋, ⌊w × floor_bps / 10⁴⌋))` (son brut propre
  si `B₀ = 0`). Elle entre donc avec le **ratio moyen** des brûlables de sa rareté et garde exactement sa part de base
  parmi elles (`w / (B₀ + w)`), au lieu d'un poids plein ; ses propres burns la font encore baisser.
  On pose ensuite, par rareté, `E = Σ brut` et `B = Σ poids disponibles` de toutes les brûlables. Le poids dans la rareté vaut
  `brut × B` pour une brûlable, `w × E` pour une carte de collection (`w` si `E = 0`). La part des brûlables dans la rareté
  reste donc exactement `B / (B + Σ w des cartes de collection)` : le poids qu'une brûlable perd revient aux autres
  brûlables de la même rareté. La probabilité de tirer une brûlable et la couverture ne bougent pas. Tout est en entiers
  (u128, au plus 2⁸⁶), sans arrondi sur les parts. `card_roll` est donc stocké sur 128 bits.
- **Choix de K.** La simulation de la série 3 n'est pas sur cette branche (`sim/` n'a que les séries 1 et 2) : K est
  posé, pas dérivé. Il est de l'ordre des émissions attendues par carte brûlable de la série v2 : une épique sort
  0,09 / 235 ≈ 0,00038 fois par pack, une légendaire 0,01 / 21 ≈ 0,00048, soit 5 à 7 exemplaires en un mois à
  20 packs/h et 28 à 34 à 100 packs/h. K = 20 est au milieu. Effet : une carte émise une fois et brûlée garde 95 % de son
  poids (20/21) ; le plancher de 25 % n'est atteint qu'à `e = b = 3K` = 60 exemplaires brûlés. Dans le scénario de la
  revue (10 épiques brûlables de même poids, les 9 bon marché émises une fois et brûlées), la 10ᵉ passe de 10 % à
  **10,5 %** des épiques brûlables, au lieu de 30,8 % sans lissage (`early_burns_are_smoothed_by_prior`). À recaler
  avec la simulation quand elle sera fusionnée.
- **Plancher** : 25 % du poids de base, tant que la carte n'est pas épuisée par son plafond. Un coin brûlé jusqu'à la
  dernière carte garde ce plancher : il ne s'éteint jamais (test `raw_burn_weight_rounding_and_floor`, sandbox).
  Une rareté qui n'a qu'une brûlable ne change pas : la renormalisation lui rend tout son poids.
- **État** : `BurnState { burned[i], seq }` par série, mis à jour dans `on_redeem_complete` (burn réussi d'une carte
  visible). Les burns de mythiques ne comptent pas. `Series.draw_cards[i].backed` passe à vrai à la résurrection.
- **Haché** : `burn.floor_bps`, `burn.prior_k`, `resurrection.eligible`. **Journalisé** : `card_redeemed` = `series_id`, `kind`, `index`, `burn_seq` (numéro
  d'ordre du burn dans la série), `asset_id` et `amount` **livrés** (adossement lu par `redeem` et passé en argument à
  `on_redeem_complete`), `replaced_by` (adossement courant s'il a été remplacé pendant le burn, sinon `null`) ; `card_resurrected` = `card_index`, `resurrect_seq` ; `pack_revealed.mechanics` =
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
- **Pack rush** : un déclenchement a eu lieu à `t`, `t < h ≤ t + duration_blocks`, **et** l'acheteur a acheté moins de
  `max_per_account` packs rush pendant ce rush (état `(compte, série) → (t, n)`, remis à zéro à chaque déclenchement,
  `draw::rush_account`). Au-delà du plafond, le pack est normal. **L'état est figé à l'achat** (`buy_pack`, bit
  `FLAG_RUSH` du pack). Retarder la révélation ne change rien.
- **Déclenchement** à l'achat `h` si toutes ces conditions tiennent :
  - aucun rush ni pause en cours : `h > t + duration + cooldown`, ou aucun déclenchement encore ;
  - la fenêtre longue est remplie : `h ≥ premier achat de la série + baseline_blocks` ;
  - `C_w ≥ min_packs` (palier absolu) **et** `C_w × m_l × 10⁴ ≥ ratio_bps × C_l × m_w` (palier relatif), c'est-à-dire
    au moins `min_packs` packs dans l'heure et un rythme court au moins `ratio` fois le rythme moyen sur 24 h.

  L'achat qui déclenche n'est pas lui-même rush. Les achats faits pendant le rush comptent dans les fenêtres.
- **Validation à la création** : `ratio_bps ≥ 10⁴`, `ratio_bps × m_w < 10⁴ × m_l` (sinon le palier serait
  inatteignable), fenêtres multiples des seaux, `m_w < m_l ≤ 96`, durée ≥ 1, `min_packs ≥ 1`, `max_per_account ≥ 1`,
  table rush valide et **distincte de la table or**.
- **Rush déclenché par un seul acteur (revue, point 2).** Mesuré avec `core.rush_on_buy` et `core.rush_account` (mêmes
  règles que le contrat) : 30 h de trafic de fond régulier, puis un acteur achète 50 packs dans un même bloc et 200 de
  plus, un par bloc. Gain = espérance gagnée sur un pack de base, `0,799 − 0,587 = 0,212` prix par pack rush.

  | Trafic de fond | Avant (min 50, sans plafond) | Après (min 100, 3 par compte) |
  |---|---|---|
  | 0 / h | rafale minimale 50 ; 200 packs rush sur 200, gain 42,4 prix | rafale minimale 100 ; 3 packs rush, gain 0,64 prix |
  | 20 / h | rafale minimale 35 ; 200 packs rush, gain 42,4 prix | rafale minimale 81 ; 3 packs rush, gain 0,64 prix |
  | 100 / h | rafale minimale 169 ; 59 packs rush (déclenché par ses achats suivants), gain 12,5 prix | rafale minimale 169 ; 3 packs rush, gain 0,64 prix |

  **Gain maximal d'un acteur** : `max_per_account × 0,212 = 0,64` prix du pack par compte et par rush, au plus un rush
  toutes les `duration + cooldown` = 39 000 blocs (6 h 30). Déclencher coûte au moins `min_packs` packs de base (perte
  attendue 41,3 % du prix chacun, soit 41 prix pour 100 packs) : un seul compte y perd. Avec `A` comptes (Sybil), le
  gain vaut `0,64 × A` : il faut environ 65 comptes pour couvrir la rafale, sans compter le stockage du premier achat de
  chaque compte. Un pack rush reste à espérance négative (79,9 % du prix), avant comme après.
- **Délai aléatoire avant le rush (option c) : non fait.** Un délai de quelques blocs tiré de l'aléa d'un reçu
  n'arrête pas l'acteur, qui achète simplement après le délai (le rush dure 3 000 blocs). L'aléa de reçu
  (`random_seed`) n'est pas recalculable par le vérificateur : il faudrait le croire sur parole, ce qui casse le rejeu à
  partir des seuls événements.
- **Couverture ≤ 80 %, contrôlée hors chaîne.** Le contrat ne connaît pas la valeur des cartes (un adossement est une
  quantité de jetons, pas un prix). `scripts/build_series.py` calcule la couverture de chaque table à partir de
  `coverage_check.rarity_value` (valeur moyenne d'un emplacement par rareté, en multiples du prix). Il **refuse** une table
  rush au-delà de `max_rush` (0,80) et écrit les couvertures dans `manifest.json`. Les valeurs de l'exemple (0 / 0,18 / 4 /
  10 / 55) redonnent les 58,6 / 184 / 80 % de la série 3. Elles sont à recaler sur la simulation à chaque série.
- **Haché** : tout `rush` (table et plafond compris). **Journalisé** : `pack_bought.rush` = `active` (période de rush),
  `window_count`, `baseline_count`, `triggered`, `last_trigger`, `rush_until`, `rush` (pack rush), `capped` (plafond
  atteint), `account_rush_packs` (packs rush du compte dans ce rush) ; `pack_revealed.mechanics.rush`. Le vérificateur
  rejoue l'anneau et les plafonds par compte à partir des `pack_bought` (hauteurs, acheteurs) et compare chaque valeur ;
  un `pack_bought` manquant pour un booster d'une série à rush est une erreur. Vue :
  `get_rush_state(series_id, at_height, account_id)` (`account.rush_packs`, `account.remaining`).
- **Coût** : anneau de 96 × 12 o dans la série, payé par l'owner à la création ; `buy_pack` lit 96 seaux et en écrit un
  (+1 Tgas mesuré sur la série v2 : 6,9 → 7,9 Tgas) ; entrée du plafond par compte (130 o prépayés, `RUSH_ENTRY_BYTES`).

## 5. Résurrection des coins morts

- **Rôle `price_oracle`** abstrait, comme le redeemer. **Changement en deux temps** (revue, point 3) :
  `propose_price_oracle(Option<AccountId>)` (owner, événement `price_oracle_proposed` avec `effective_from`), puis
  `accept_price_oracle()` (owner, au plus tôt `oracle_delay_blocks` blocs après la proposition, événement
  `price_oracle_accepted`). Le délai est un paramètre de `new` (`oracle_delay_blocks`, 144 000 blocs = 24 h par défaut) ;
  une nouvelle proposition remplace la précédente et relance le délai. `revoke_price_oracle()` (owner) retire l'oracle
  tout de suite (événement `price_oracle_revoked`) : retirer ne peut que supprimer des résurrections. Vue `get_config` :
  `price_oracle_id`, `price_oracle_pending`, `oracle_delay_blocks`.
  `set_resurrected(series_id, card_index, backing)` : oracle seulement, payable (stockage mesuré, excédent rendu).
- **Portée** : **les cartes de `mechanics.resurrection.eligible`**, liste engagée dans la table hachée (index
  strictement croissants, 200 au plus). Chaque index doit désigner une carte visible **épique ou légendaire non
  adossée** par la table (vérifié à l'ouverture ; rare et commune refusées, recommandation de la simulation : 94 % du
  coût viendrait des communes). Sans ce champ, aucune résurrection : c'est le cas des séries sans mécanique, qui
  pouvaient être ressuscitées avant la revue. Un nouvel appel remplace l'adossement d'une carte de la liste.
- **Effet** : la carte devient brûlable pour les nouvelles cartes **et** pour les exemplaires existants, puisque
  l'adossement est lu à la demande (`get_backing`, `redeem`, `extra.burnable` des métadonnées). Elle rejoint aussi les
  brûlables de sa rareté pour la renormalisation des burns (`resurrect_seq`), avec le ratio moyen des brûlables de la
  table (section 3), pas avec un poids plein.
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
| Série v2 complète, toutes les mécaniques, 12 packs à 160 Tgas | dernier reçu 35,3 Tgas, total 48 | dernier reçu 15,5 Tgas (14,1 avant la revue), `buy_pack` 8,0, total 29,5 ; **avec gold pack et valeur (22 packs, dont un gold) : dernier reçu 15,4 Tgas, `buy_pack` 8,1, total 29,6** |
| 2 000 cartes aux chaînes maximales, 10 cartes par pack, toutes les mécaniques | dernier reçu 58,8 Tgas (sans mécanique) | dernier reçu 24,3 Tgas au pire (19,5 avant la revue) ; **avec gold pack de 10 emplacements et valeur : 23,3 Tgas au plus** (normal et gold), `buy_pack` 10,4, total 39,8 |
| 2 000 cartes, 10 par pack, toutes les mécaniques, légendaires, épiques et rares épuisées : chaque emplacement retombe trois fois jusqu'à la commune ; 23 à 24 burns, 200 cartes ressuscitables (`worst_case_cascade_with_burns_fits`) | (non mesuré) | dernier reçu 49,1 Tgas au pire ; **avec gold pack (10 emplacements à plancher légendaire, dont 2 parmi les brûlables : visée, mythique, puis épique, rare, commune) et brûlable garantie : 48,4 Tgas au pire** |
| Table de valeur et gold pack, 7 cartes, 10 packs (`value_and_gold_pack_end_to_end`) | | dernier reçu 5,2 Tgas, stockage 963 o au plus / 1 475 prépayés |
| `on_redeem_complete` avec burns | (pas de compteur) | 3,8 Tgas sur 20 fixes |
| `redeem` complet | 10,4 Tgas | 8,1 Tgas |
| `reveal_mythic`, 100 scellées | 85,6 Tgas | 5,0 Tgas |
| `get_rates`, page de 200, 2 000 cartes avec burns | 25,4 Tgas | 34,2 Tgas |

Le budget du dernier reçu reste de 120 Tgas fixes et `min_gas` de 160 Tgas. Au pire mesuré (cascade), la marge est d'un
facteur 2,5.

## 7. Revue de sécurité des mécaniques (11/11/2026) : corrections

| # | Sévérité | Point | Correction | Tests |
|---|---|---|---|---|
| 1 | Élevé | Burns en début de série : une carte émise une fois et brûlée tombait au plancher | A priori `K` (`burn.prior_k`, haché, 20 par défaut), plancher gardé, même calcul en Python | `early_burns_are_smoothed_by_prior`, `raw_burn_weight_rounding_and_floor`, `ReviewFixes` (Python) |
| 2 | Moyen | Rush déclenché puis exploité par un seul acteur | `rush.max_per_account` (haché, 3), `min_packs` 50 → 100 ; délai aléatoire non fait (section 4) | `rush_packs_are_capped_per_account`, `test_single_actor_rush_is_capped`, vecteurs `rush_account` |
| 3 | Moyen | L'owner change l'oracle à tout moment ; cartes ressuscitables non engagées ; poids plein d'une ressuscitée | `propose` / `accept` après 24 h, `revoke` immédiat ; `resurrection.eligible` haché ; ratio moyen | `oracle_change_is_two_step_with_delay`, `resurrection_limited_to_hashed_list`, `resurrected_card_enters_with_mean_ratio`, tests Python |
| 4 | Faible | Adossement remplacé pendant un burn | Adossement passé à `on_redeem_complete`, journalisé (`replaced_by`) | `redeem_logs_the_backing_actually_delivered` |
| 5 | Faible | Vérificateur : drapeau rush accepté sans `pack_bought` | Erreur explicite | `test_missing_pack_bought_is_an_error` |
| 6 | Faible | Gaz du pire cas non mesuré en cascade | Mesuré : 49,1 Tgas sur 120 | `worst_case_cascade_with_burns_fits` |
| 7 | Faible | `sealed_tokens[j]` gardé après la révélation | Vidé (et, depuis le 11/11, plus d'`updated_at` : métadonnées anonymes inchangées) | `reveal_clears_sealed_tokens_metadata_unchanged` |

## 8. Gold pack : plancher de rareté par emplacement (11/11)

Décision du porteur : le compteur de pitié est gardé (sans garantie depuis le 11/11, section 2), mais le gold pack change de forme. Il n'est
plus une table de poids renforcés : c'est une liste d'emplacements, chacun avec un **plancher de rareté**.

- **Table** : `mechanics.gold.slots`, 1 à 10 emplacements (indépendamment de `cards_per_pack` ; le prépayé compte le plus
  grand des deux). Chaque emplacement a `floor` (plancher), `weights` (poids propres, nuls sous le plancher) ou `null`
  (poids de base mis à zéro sous le plancher, `draw::gold_slot_weights`), et `burnable` (tiré parmi les brûlables).
- **Défaut** (`serie-exemple.json`) : 5 cartes, aucune commune. Emplacements 1 et 2 rare ou mieux, 3 et 4 épique ou
  mieux (poids de base tronqués : la proportion entre raretés au-dessus du plancher est celle de la base), 5 légendaire
  99 % ou mythique 1 % (`weights` = 1 / 99 ; 20 / 80 avant le 11/11). L'emplacement 2 est `burnable` : il porte la valeur du pack.
- **Tirage** : `rarity_roll = roll(acc, slot, 0) mod Σ poids de l'emplacement` (tag inchangé), rareté visée par cumul.
- **Rareté épuisée** (`draw::fallback_order`, règle définie) : la visée, puis **vers le bas jusqu'au plancher**, puis
  **vers le haut** (au-dessus de la visée, jusqu'à la mythique), puis **sous le plancher** jusqu'à la commune en dernier
  recours. Exemples : 5ᵉ emplacement visant la légendaire épuisée → mythique ; légendaire et mythique épuisées →
  épique ; mythique au plafond → légendaire. Le plancher n'est franchi que si rien n'est tirable au-dessus.
- **Choix de la carte** : comme avant (`card_roll = roll(acc, slot, 1) mod Σ`, poids des burns compris), restreint aux
  brûlables pour un emplacement `burnable`.
- **Validation** : 1 à 10 emplacements ; poids d'un emplacement non tous nuls, nuls sous le plancher, poids mythique
  seulement avec un engagement pondéré ; une rareté pondérée par un emplacement doit avoir une carte ; `pity` exige
  `gold`. La table rush garde ses poids renforcés (la contrainte « distincte de la table or » disparaît avec celle-ci).
- **Haché** : `gold`. **Journalisé** : `pack_revealed.mechanics.mode = "gold"` et les tirages (autant que
  d'emplacements). Le vérificateur recalcule chaque emplacement (`core.draw_slot_rule`).

## 9. Valeur aléatoire en jetons par pack (11/11)

Décision du porteur : la valeur en jetons d'un pack va de 20 % à 200 % du prix, avec une moyenne vers 75 %.

- **Tables** (`mechanics.value`, hachées) : `normal`, `gold`, `rush`, chacune de 1 à 32 paliers `(valeur en points de base
  du prix, poids)`, poids non nuls ; `multipliers` par rareté (mythique 0, autres 1 à 10⁶). **Table normale validée à la
  création : 2 000 ≤ valeur ≤ 20 000 pb.** Tables gold et rush : 1 à 10⁶ pb. Prix borné pour que
  `⌊prix × V / 10⁴⌋ × multiplicateur` tienne sur u128.
- **Tirage de V** (dernier reçu) : `value_roll = u128_be(sha256(acc ‖ 0x00 ‖ 0x03)[0..16]) mod Σ poids`, palier par
  cumul dans l'ordre de la table (`draw::value_tier`). Table gold pour un gold pack, rush pour un pack rush (figé à
  l'achat), normale sinon.
- **Répartition** (`draw::split_value`) : `total = ⌊prix × V / 10⁴⌋` yoctoNEAR de valeur, réparti entre les
  **brûlables du pack** (cartes visibles adossées par la table ou ressuscitées **au moment du tirage**) au prorata du
  multiplicateur de leur rareté : `⌊total × m_i / Σm⌋`, arrondi vers le bas ; **le reste va à la carte au plus fort
  multiplicateur, la première dans l'ordre des emplacements en cas d'égalité**. Aucun yocto n'est perdu.
- **Brûlable garantie** : le dernier emplacement d'un pack normal (base ou rush) est tiré parmi les brûlables. Sa rareté
  visée suit le tirage normal (`rarity_roll` inchangé), avec retombée vers le bas parmi les brûlables, puis vers le haut
  si aucune rareté inférieure n'en a (`fallback_order(visée, commune)`). Un gold pack a son emplacement `burnable`
  (le 2 par défaut), avec la règle de la section 8. Une mythique n'est jamais une brûlable ici : son adossement est dans
  son contenu, secret jusqu'à la révélation.
- **Validation** : avec une table de valeur, ou un emplacement gold `burnable`, il faut une carte **adossée par la table,
  sans plafond et de poids non nul** (une commune ou une rare brûlable illimitée, par exemple). Comme la retombée parcourt
  toutes les raretés visibles, l'emplacement trouve toujours une brûlable et le pack en a toujours au moins une.
- **Adossement transmis** : `redeem` envoie au redeemer `(asset_id, amount)`, avec `asset_id` de la carte (table ou
  oracle) et **`amount` = part de la valeur du pack** pour cet exemplaire. `get_backing`, `get_card` et
  `card_redeemed` donnent ce montant. Le redeemer reste abstrait : il reçoit des yoctoNEAR de valeur, pas des jetons, et
  la conversion dépend du financement, non décidé. Dans une série à table de valeur, l'`amount` de la table n'est donc
  plus lu pour les exemplaires tirés brûlables.
- **Cas spéciaux (adossement fixe, documentés)** : une **mythique** garde l'adossement de son contenu révélé ; un
  exemplaire **devenu brûlable après son tirage** (résurrection) n'a pas de part de valeur et garde le montant de
  l'oracle. Les exemplaires tirés après la résurrection, eux, ont une part.
- **Stockage** : `Pack::value` = `bps` (4 o) et le masque des brûlables (2 o), 7 o avec l'option ; les montants sont
  recalculés à la lecture. Prépayé : `PACK_VALUE_BYTES` = 8 o.
- **Dernier reçu sans échec lié au résultat** : aucun `require` ; les dépassements sont exclus à la création ; sans
  brûlable (impossible pour une table validée), rien n'est réparti.
- **Haché** : `value`. **Journalisé** : `pack_revealed.mechanics.value` = `roll`, `tier`, `bps`, `total`, `amounts`
  (par emplacement, `null` hors brûlables), et `resurrect_seq` (les brûlables du tirage dépendent des résurrections).
  Le vérificateur recalcule V, le total, la répartition au bit près, et la brûlable garantie (rejeu des
  `card_resurrected`).
- **Tables** (`serie-exemple.json` ; celles de la simulation, 27 paliers, via
  `--tables-valeur ../sim/resultats/serie5/tables-valeur.json`, format de la sim lu directement) : normale
  `[[2000,15],[3000,13],[4000,10],[5000,10],[6000,10],[8000,10],[10000,10],[12000,8],[15000,5],[20000,9]]` (moyenne
  exacte 75 %), rush identique (75 %, 78,5 % avant le 11/11), gold `[[10000,30],[15000,25],[20000,20],[30000,13],[50000,8],[80000,4]]`
  (218,5 %), multiplicateurs commune 1, rare 2, épique 5, légendaire 20. `build_series.py` vérifie les bornes du contrat
  et refuse une table rush de moyenne > 80 % (`coverage_check.max_rush`).

## 10. Ce qui reste ouvert

- Variante du compteur dans un NFT revendable (section 2).
- `prior_k` et `min_packs` à recaler sur la simulation de la série 3 quand elle sera fusionnée. Le plafond par compte
  ne résiste pas à un acteur aux nombreux comptes (section 4).
- Un vrai oracle (section 5) et l'approvisionnement des jetons.
- Valeurs de rareté de `coverage_check` : à reprendre de la simulation à chaque série. Le contrat ne contrôle pas la
  couverture.
- Temps de bloc réel (0,6 s supposé) pour convertir 1 h, 24 h et 6 h en blocs.
- `nft_metadata_update` pour les exemplaires d'une carte ressuscitée (non émis ; plus émis non plus à la révélation d'une
  mythique, dont les métadonnées ne changent pas).
- Mesures sur testnet.
- Tables de valeur et multiplicateurs définitifs (calibrage dans `sim/`) ; financement réel de la valeur transmise au
  redeemer.
- Série v2 d'exemple : deux brûlables factices seulement (une commune, une légendaire) ; la brûlable garantie retombe
  donc presque toujours sur la même commune.

## 11. Mythiques anonymes (11/11)

Décision du porteur : 3 mythiques, sans aucune information publique, avant comme après la révélation.

- **Métadonnées NEP-177** (`nft_token`, `nft_tokens`, `nft_tokens_for_owner`) : titre « ? », description « ? », image
  « ? » (`MYTHIC_MEDIA`, un SVG en URI `data:`, le même pour toutes), ni `reference`, ni `copies`, ni `updated_at` ;
  `extra` = `series_id`, `rarity: "mythic"`, `pack_id`. Plus de `card_id`, d'engagement, d'index de mythique ni de
  `burnable`. Les 3 mythiques sont donc indiscernables entre elles dans leurs métadonnées, et celles-ci ne changent pas à
  la révélation (plus de `nft_metadata_update`).
- **`get_card`** d'une mythique : `card_id` et `backing` toujours `null` ; `sealed` dit seulement si l'engagement a été
  ouvert.
- **`art/`** : `mythique-m1.json`, `-m2`, `-m3` sont identiques octet pour octet au JSON du dos commun (titre et
  description « ? », image `dos-mythique.svg`, sans id ni N°).
- **Ce qui reste public, par construction** (à trancher par le porteur, rien n'est supprimé) :
  - l'index de mythique d'un exemplaire (`pack_revealed.draws[].index`, `get_pack`, `get_card.index`, `mythic_drawn`) et
    l'engagement correspondant (`get_mythic_commitments`, `get_rates`) : nécessaires pour vérifier le tirage ;
  - à la révélation (`reveal_mythic`), `mythic_revealed` et `get_mythic_commitments[j].revealed` publient `card_id`,
    sel et contenu (titre, médias, adossement), avec la liste des exemplaires scellés : c'est ce qui rend l'engagement
    vérifiable. Combiné à l'index, cela relie chaque exemplaire à son coin. **Ne pas révéler** garde le secret, mais une
    mythique non révélée **ne peut pas être brûlée** (son adossement est dans le contenu) ;
  - après la révélation, `get_backing` (vue du burn) et `card_redeemed` (burn) donnent l'actif adossé ;
  - le `media` du contenu engagé est construit par `build_series.py` avec l'id réel de la mythique (`media_template`) :
    il n'apparaît qu'à la révélation, jamais dans les métadonnées affichées.

