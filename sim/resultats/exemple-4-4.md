### Exemple 4.4 du document

| Grandeur | Formule exacte | Monte-Carlo |
|---|---:|---:|
| κ (NEAR par unité de poids) | 1,000 | |
| Adossement moyen par booster (NEAR) | 6,00 | 6,01 ± 0,008 |
| Écart-type par booster (NEAR) | 11,8 | 11,8 |
| Cartes brûlables par booster | 2,40 | 2,40 |
| Booster sans carte brûlable | 3,8 % | 3,8 % |
| P(adossement ≥ prix) | | 13,1 % |
| P(adossement + revente ≥ prix) | | 13,7 % |
| P(au moins un legendaire) | 1,00 % (1 sur 100) | 1,00 % |
| P(au moins un legendaire brûlable) | 0,48 % | 0,49 % |
| Gain moyen « brûle tout » (NEAR) | 6,36 | 6,37 |
| Borne β (ε = 15 %) | 82,9 % | 83,3 % |
| Booster touché par V_cap = 250 | | 0,0023 % |

**Percentiles de l'adossement d'un booster (NEAR)**

| p1 | p5 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p99.9 | p99.99 | max |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0,0 | 0,5 | 1,0 | 2,0 | 3,0 | 5,5 | 12,0 | 19,0 | 61,0 | 142,5 | 229,0 | 250,0 |

**Valeur d'une carte brûlable (NEAR)**

| Rareté | Min | Base (m = 1) | Max | Max en $ |
|---|---:|---:|---:|---:|
| commune | 0,50 | 1,00 | 2,00 | 7 |
| peu_commune | 1,00 | 2,00 | 4,00 | 14 |
| rare | 4,00 | 8,00 | 16,00 | 58 |
| epique | 15,00 | 30,00 | 60,00 | 216 |
| legendaire | 55,00 | 110,00 | 220,00 | 792 |

**Fréquence des cartes sur 10 000 boosters**

| Rareté | Cartes par booster | Exemplaires par brûlable | Par carte de collection | Faveur |
|---|---:|---:|---:|---:|
| commune | 3,5000 | n/a | n/a | n/a |
| peu_commune | 1,0000 | n/a | n/a | n/a |
| rare | 0,4000 | n/a | n/a | n/a |
| epique | 0,0900 | n/a | n/a | n/a |
| legendaire | 0,0100 | n/a | n/a | n/a |

**Réserve** (4000 trajectoires de 10000 ventes, apport (β + δ)·P = 7,00 NEAR par booster)

| R₀ (NEAR) | P(réserve < V_cap avant 10 000 ventes) |
|---:|---:|
| 250 | 73,42 % |
| 280 | 47,93 % |
| 450 | 10,15 % |
| 560 | 3,33 % |
| 710 | 1,03 % |
| 940 | 0,10 % |

- Approximation normale (z = 3) : R₀ ≈ 564 NEAR. Risque simulé à ce niveau : 3,15 % (un mouvement brownien donnerait 1,11 %).
- R₀ simulé pour un risque de 5,0 % : 517 NEAR (1 861 $).
- R₀ simulé pour un risque de 1,0 % : 712 NEAR (2 561 $).
- Reste après jetons et réserve : 30 % du prix, soit 3,00 NEAR par booster.
