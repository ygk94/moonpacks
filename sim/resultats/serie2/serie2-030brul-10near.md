> **Non réalisable à β = 60 %** : avec les plafonds par carte, l'adossement moyen ne dépasse pas 3,33 NEAR. Simulé à β = 33,3 %.

### Série 2 : 30 brûlables, 10 NEAR

| Grandeur | Formule exacte | Monte-Carlo |
|---|---:|---:|
| κ (NEAR par unité de poids) | 47,195 | |
| Adossement moyen par booster (NEAR) | 3,33 | 3,35 ± 0,020 |
| Écart-type par booster (NEAR) | 28,5 | 28,5 |
| Cartes brûlables par booster | 0,02 | 0,02 |
| Booster sans carte brûlable | 98,3 % | 98,3 % |
| P(adossement ≥ prix) | | 1,7 % |
| P(adossement + revente ≥ prix) | | 1,7 % |
| P(au moins un legendaire) | 0,98 % (1 sur 102) | 0,99 % |
| P(au moins un legendaire brûlable) | 0,89 % | 0,89 % |
| P(au moins un mythique) | 0,02 % (1 sur 5 000) | 0,02 % |
| P(au moins un mythique brûlable) | 0,02 % | 0,02 % |
| Gain moyen « brûle tout » (NEAR) | 3,56 | 3,58 |
| Borne β (ε = 15 %) | 84,8 % | inf % |
| Booster touché par V_cap = 600 | | 0,0000 % |
| Cartes brûlables sous 1,4 NEAR | | 0,0 % |

**Percentiles de l'adossement d'un booster (NEAR)**

| p1 | p5 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p99.9 | p99.99 | max |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 100,0 | 280,0 | 477,0 | 577,0 |

**Valeur d'une carte brûlable (NEAR)**

| Rareté | Min | Base (m = 1) | Max | Max en $ |
|---|---:|---:|---:|---:|
| epique | 99,11 | 100,00 | 100,00 | 360 |
| legendaire | 280,00 | 280,00 | 280,00 | 1 008 |
| mythique | 477,00 | 477,00 | 477,00 | 1 717 |

**Fréquence des cartes sur 10 000 boosters**

| Rareté | Cartes par booster | Exemplaires par brûlable | Par carte de collection | Faveur |
|---|---:|---:|---:|---:|
| commune | 4,3399 | n/a | 37,4 | n/a |
| rare | 0,4303 | n/a | 18,7 | n/a |
| epique | 0,2198 | 9,4 | 9,4 | 1,0 |
| legendaire | 0,0098 | 4,7 | 4,7 | 1,0 |
| mythique | 0,0002 | 0,7 | n/a | n/a |

**Réserve** (20000 trajectoires de 10000 ventes, apport (β + δ)·P = 4,33 NEAR par booster)

| R₀ (NEAR) | P(réserve < V_cap avant 10 000 ventes) |
|---:|---:|
| 600 | 76,73 % |
| 850 | 50,29 % |
| 1 640 | 9,98 % |
| 2 420 | 1,99 % |
| 2 720 | 1,02 % |
| 3 770 | 0,10 % |

- Approximation normale (z = 3) : R₀ ≈ 2 422 NEAR. Risque simulé à ce niveau : 1,99 % (un mouvement brownien donnerait 1,11 %).
- R₀ simulé pour un risque de 5,0 % : 1 981 NEAR (7 131 $).
- R₀ simulé pour un risque de 1,0 % : 2 724 NEAR (9 808 $).
- R₀ simulé pour un risque de 0,1 % : 3 766 NEAR (13 556 $).
- Reste après jetons et réserve : 57 % du prix, soit 5,67 NEAR par booster.
- Marge simulée (prix − adossement − δ·P) : 5,65 NEAR par booster.
