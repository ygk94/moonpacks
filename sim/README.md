# Pack economics simulator

Monte-Carlo and exact models of the Moonpacks pack mechanics: card rarities, the NEAR backing paid into each card,
burn value, the reserve, the pity counter for gold packs, gold rushes, burn-driven rarity and dead-coin
resurrection. It was used to choose the parameters that the contract now applies. See
[`docs/mechanics.md`](../docs/mechanics.md) for the mechanics themselves.

Python 3, with `numpy`, `pyyaml` and `pytest` (`requirements.txt`).

## Setup and tests

```bash
cd sim
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q tests
```

CI runs the same thing (`pip install -r requirements.txt`, then `python -m pytest -q tests`).

## Commands

The code was written with French identifiers, so commands and options are in French
(`boosters` = packs, `trajectoires` = ruin trajectories, `sensibilite` = sensitivity, `tout` = all,
`pitie` = pity, `rarete-burn` = burn-driven rarity, `--rapide` = quick run with 10x fewer draws).

```bash
# one config: prints a table, writes resultats/<config>.md and .json
.venv/bin/python -m memaster_sim run configs/serie1-A-10near.yaml
.venv/bin/python -m memaster_sim run configs/serie1-A-10near.yaml --boosters 5000000 --trajectoires 20000 --seed 4

# sensitivity grids (beta, legendary weights, mythic odds)
.venv/bin/python -m memaster_sim sensibilite configs/serie1-A-10near.yaml

# series 1 configs and the worked example (series 2 to 5 have their own commands), about 4 min
.venv/bin/python -m memaster_sim tout --boosters 2000000

# series 2: regenerate configs, run the grid, sensitivity to the factor between tiers
.venv/bin/python -m memaster_sim.serie2 configs
.venv/bin/python -m memaster_sim.serie2 run --boosters 2000000 --trajectoires 20000
.venv/bin/python -m memaster_sim.serie2 sensibilite --total 150 --prix 5 --trajectoires 20000

# series 3: regenerate configs, run everything (about 10 min) or selected sections
.venv/bin/python -m memaster_sim.serie3 configs
.venv/bin/python -m memaster_sim.serie3 run
.venv/bin/python -m memaster_sim.serie3 run --rapide --sections pitie rush

# series 4: pack configs, then everything (about 20 s)
.venv/bin/python -m memaster_sim.serie4 configs
.venv/bin/python -m memaster_sim.serie4 run

# series 5 (the parameters used by the contract), about 5 s
.venv/bin/python -m memaster_sim.serie5 [--rapide]
```

Every command accepts `--sortie <dir>` to write somewhere other than `resultats/`.

## The five series

| Series | Configs | What it studies |
|---|---|---|
| 1 | `serie1-{A,B,C}-*.yaml`, `exemple-4-4.yaml` | First model: 5-slot packs at 5 or 10 NEAR, backing ratio beta, reserve ruin risk, mythic odds. `exemple-4-4` is a small hand-checked example kept as a regression test |
| 2 | `serie2-NNNbrul-PPnear.yaml` (generated) | Full catalogue (`docs/data/catalogue-v2.json`): number of burnable cards x pack price |
| 3 | `serie3-PPPc-CCcouv.yaml` (generated), `serie3-mecaniques.yaml` | Low-price packs (15 cents to 1 dollar) x coverage; measured gas and storage costs, pity, rush, burn-driven rarity, resurrection |
| 4 | `serie4-PPPc.yaml` (generated), `serie4-valeur.yaml` | Value tables V drawn per pack, gold pack, margin, anti-arbitrage bound |
| 5 | `serie5.yaml` | Final parameters: pity without guarantee, mythic about 1 in a million packs, gold pack 99/1, average V of 75 % |

Generated configs should not be edited by hand; rerun the `configs` command of their series instead.

## Layout

| Path | Role |
|---|---|
| `memaster_sim/modele.py` | Config loading, outcome tables, kappa, exact formulas (mean, variance, beta bound, normal reserve) |
| `memaster_sim/simulation.py` | Vectorised draws, statistics, simulated beta bound, ruin simulation |
| `memaster_sim/rapport.py` | Markdown and JSON output, sensitivity grids |
| `memaster_sim/catalogue.py` | Loader for `docs/data/catalogue-v2.json`: counts per rarity, seeded choice of burnable cards |
| `memaster_sim/couts.py` | Real cost of a pack (gas, storage, batched token purchase), margin, break-even price |
| `memaster_sim/valeur.py` | Value tables V (calibration, quantiles, published format), reserve |
| `memaster_sim/gold.py` | Gold table, mixing tables with a shared kappa, reserve with gold packs |
| `memaster_sim/pitie.py` | Pity counter (with or without a guarantee): cycle law, stationary rate, exact population rate, Monte-Carlo checks |
| `memaster_sim/rush.py` | Gold rush: Poisson purchase flow with spikes, sliding window, fixed or relative threshold, pause |
| `memaster_sim/rarete_burn.py` | Burn-driven rarity: weight x circulating / minted, three renormalisations, floor |
| `memaster_sim/resurrection.py` | Dead-coin resurrection: cost of existing copies, budget and fund |
| `memaster_sim/serie2.py` ... `serie5.py` | Config generation and runs for each series |
| `configs/` | YAML configs; every key is commented in `configs/serie1-A-10near.yaml` |
| `resultats/` | Committed JSON outputs, one file or folder per series (regenerable) |
| `tests/` | Pytest suite: draws, the worked example, series constraints, catalogue loader, costs, mechanics, value tables, burn rules shared with the contract |

Running the commands also writes markdown reports next to the JSON files; only the JSON outputs are kept in the
repository.

## Writing a config

The main keys (see the comments in `configs/serie1-A-10near.yaml`):

- `raretes.<name>`: `poids` (weight), `part_brulable` (probability that a card drawn in this rarity is burnable),
  `plafond` (maximum backing of one card, NEAR), `revente` (average resale price of a collectible card, NEAR),
  `effectif` and `brulables` (catalogue counts), optional `multiplicateur` (overrides the global multiplier).
- `emplacements.tables`: one probability table per slot type; `emplacements.ordre`: the type of each of the 5 slots.
- `beta`, `delta` (share of the price paid into the reserve), `epsilon`, `v_cap`, `couts` (`s_achat`, `f_burn`,
  `f_burn_fixe`, `s_vente`, `phi`).
- `calibrer_avec_plafonds: true` recomputes kappa so that the mean backing stays equal to beta x price despite
  per-card caps.

Rarities are free-form: add or remove them as long as the tables name them.

## Key results (series 5, `resultats/serie5/serie5.json`)

With NEAR at 2.50 dollars and packs at 0.20 or 0.50 dollars:

- Normal and rush packs return an average value V of 75 % of the price; a gold pack returns 200 %.
- Burning a whole pack immediately returns about 73 % of the price, under the 85 % anti-arbitrage bound.
- Gold pack chance starts at 1 in 50,000 and rises to 1 in 25,000 after 1,000 packs without one (no guarantee);
  over the long run that is about 1 gold pack per 25,000 packs.
- A mythic appears in about 1 in a million classic packs, and in about 1 % of gold packs.
- In the cautious case where the project pays the gas, the margin is about 0.037 dollar per pack at 0.20 dollar
  (18 %) and about 0.11 dollar at 0.50 dollar (22 %).
