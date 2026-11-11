# Simulateur économique Memaster

Monte-Carlo des boosters (phase 2.1 de `docs/plan.md`). Les résultats et les recommandations sont dans `RAPPORT.md`.

## Installation

```bash
cd sim
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Commandes

```bash
# une config : tableau markdown à l'écran, plus resultats/<config>.md et .json
.venv/bin/python -m memaster_sim run configs/serie1-A-10near.yaml

# plus de tirages, plus de trajectoires de ruine, autre graine
.venv/bin/python -m memaster_sim run configs/serie1-A-10near.yaml --boosters 5000000 --trajectoires 20000 --seed 4

# grilles de sensibilité (β, poids des légendaires, cote du mythique)
.venv/bin/python -m memaster_sim sensibilite configs/serie1-A-10near.yaml

# toutes les configs de configs/, avec les grilles pour celles qui ont un mythique (environ 4 min)
.venv/bin/python -m memaster_sim tout --boosters 2000000

# série 2 (catalogue v2) : régénérer les configs, simuler la grille, sensibilité au facteur entre paliers
.venv/bin/python -m memaster_sim.serie2 configs
.venv/bin/python -m memaster_sim.serie2 run --boosters 2000000 --trajectoires 20000
.venv/bin/python -m memaster_sim.serie2 sensibilite --total 150 --prix 5 --trajectoires 20000

# tests
.venv/bin/python -m pytest -q tests
```

## Fichiers

| Fichier | Rôle |
|---|---|
| `configs/exemple-4-4.yaml` | L'exemple travaillé de `docs/marche-droits-economie.md`, partie 4.4 |
| `configs/serie1-A-10near.yaml` | Série 1, jeu A : 10 NEAR, mythique 1 sur 5 000 |
| `configs/serie1-B-10near.yaml` | Série 1, jeu B : 10 NEAR, mythique 1 sur 2 000, petite réserve |
| `configs/serie1-C-5near.yaml` | Série 1, jeu C : 5 NEAR, mythique 1 sur 10 000 |
| `configs/serie2-NNNbrul-PPnear.yaml` | Série 2 : catalogue v2, NNN brûlables, PP NEAR (générées, ne pas éditer ; `tout` les ignore) |
| `memaster_sim/catalogue.py` | Chargeur de `docs/data/catalogue-v2.json` : effectifs par rareté, choix des brûlables à graine fixe |
| `memaster_sim/serie2.py` | Génération des configs et grille de la série 2, résultats dans `resultats/serie2/` |
| `memaster_sim/modele.py` | Config, tables d'issues, κ, formules exactes (espérance, variance, borne β, R₀ normale) |
| `memaster_sim/simulation.py` | Tirages vectorisés, statistiques, borne β simulée, simulation de ruine |
| `memaster_sim/rapport.py` | Sorties markdown et JSON, grilles de sensibilité |
| `tests/` | Pytest : tirages, exemple 4.4, contraintes de la série 1, chargeur du catalogue v2 et configs de la série 2 |
| `resultats/` | Sorties générées (régénérables) |

## Écrire une config

Chaque clé est commentée dans `configs/serie1-A-10near.yaml`. L'essentiel :

- `raretes.<nom>` : `poids` (w), `part_brulable` (probabilité qu'une carte tirée dans cette rareté soit brûlable),
  `plafond` (adossement maximal d'une carte, NEAR), `revente` (prix moyen d'une carte de collection, NEAR),
  `effectif` et `brulables` (catalogue), `multiplicateur` facultatif (remplace le multiplicateur global).
- `emplacements.tables` : une table de probabilités par type d'emplacement ; `emplacements.ordre` : le type de chaque
  emplacement (5 entrées).
- `beta`, `delta` (part du prix versée à la réserve), `epsilon`, `v_cap`, `couts` (`s_achat`, `f_burn`,
  `f_burn_fixe`, `s_vente`, `phi`).
- `calibrer_avec_plafonds: true` recalcule κ pour que l'adossement moyen reste égal à β·P malgré les plafonds par carte.

Les raretés sont libres : on peut en ajouter ou en retirer, du moment que les tables les nomment.
