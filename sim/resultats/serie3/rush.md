## Gold rush

Flux de base : 200 packs/h (cycle de ±50 % sur la journée), 0,5 pic par jour en moyenne (× 6 pendant 30 min), demande × 2 pendant un rush. Fenêtre glissante 60 min, rush de 3 000 blocs (30 min à 0,6 s par bloc). 20 trajectoires de 30 jours par case.

| Règle | Trafic | Packs / jour | Rushs / jour | Temps en rush | g_rush (part des packs en or) | g_rush p95 |
|---|---:|---:|---:|---:|---:|---:|
| fixe | × 0,5 | 2 534 | 0,02 | 0,0 % | 0,2 % | 1,2 % |
| fixe | × 1,0 | 5 267 | 0,92 | 1,9 % | 8,0 % | 11,8 % |
| fixe | × 2,0 | 15 393 | 20,43 | 42,6 % | 68,6 % | 69,8 % |
| fixe | × 4,0 | 40 146 | 47,19 | 98,3 % | 99,1 % | 99,1 % |
| fixe_cooldown_6h | × 0,5 | 2 539 | 0,01 | 0,0 % | 0,4 % | 2,4 % |
| fixe_cooldown_6h | × 1,0 | 5 198 | 0,29 | 0,6 % | 4,5 % | 6,9 % |
| fixe_cooldown_6h | × 2,0 | 10 655 | 1,27 | 2,6 % | 10,6 % | 12,5 % |
| fixe_cooldown_6h | × 4,0 | 21 847 | 3,04 | 6,3 % | 13,9 % | 14,6 % |
| relatif_2x5_cooldown_6h | × 0,5 | 2 604 | 0,31 | 0,6 % | 4,9 % | 6,5 % |
| relatif_2x5_cooldown_6h | × 1,0 | 5 119 | 0,25 | 0,5 % | 3,9 % | 5,4 % |
| relatif_2x5_cooldown_6h | × 2,0 | 10 413 | 0,31 | 0,6 % | 5,2 % | 7,9 % |
| relatif_2x5_cooldown_6h | × 4,0 | 20 873 | 0,28 | 0,6 % | 5,2 % | 8,5 % |

**Effet sur la marge** (0,20 $, κ calibré pour le trafic prévu × 1 et la pitié proposée). « Table or » : le rush reprend la table de pitié ; « table rush » : facteurs × rare 1,17, epique 1,34, legendaire 1,51, mythique 1,51, couverture 80 %.

| Règle | Table pendant le rush | Trafic | g_rush | Couverture réalisée | Marge / pack | Marge sur 30 jours |
|---|---|---:|---:|---:|---:|---:|
| fixe | or | × 0,5 | 0,2 % | 56,9 % | 0,073 $ | 5 575 $ |
| fixe | or | × 1,0 | 8,0 % | 65,0 % | 0,057 $ | 9 010 $ |
| fixe | or | × 2,0 | 68,6 % | 128,6 % | -0,070 $ | -32 381 $ |
| fixe | or | × 4,0 | 99,1 % | 160,6 % | -0,134 $ | -161 684 $ |
| fixe | rush | × 0,5 | 0,2 % | 63,8 % | 0,059 $ | 4 518 $ |
| fixe | rush | × 1,0 | 8,0 % | 65,0 % | 0,057 $ | 9 010 $ |
| fixe | rush | × 2,0 | 68,6 % | 74,4 % | 0,038 $ | 17 682 $ |
| fixe | rush | × 4,0 | 99,1 % | 79,1 % | 0,029 $ | 34 733 $ |
| fixe_cooldown_6h | or | × 0,5 | 0,4 % | 60,4 % | 0,066 $ | 5 051 $ |
| fixe_cooldown_6h | or | × 1,0 | 4,5 % | 65,0 % | 0,057 $ | 8 893 $ |
| fixe_cooldown_6h | or | × 2,0 | 10,6 % | 71,7 % | 0,044 $ | 13 931 $ |
| fixe_cooldown_6h | or | × 4,0 | 13,9 % | 75,4 % | 0,036 $ | 23 745 $ |
| fixe_cooldown_6h | rush | × 0,5 | 0,4 % | 64,3 % | 0,058 $ | 4 443 $ |
| fixe_cooldown_6h | rush | × 1,0 | 4,5 % | 65,0 % | 0,057 $ | 8 893 $ |
| fixe_cooldown_6h | rush | × 2,0 | 10,6 % | 65,9 % | 0,055 $ | 17 626 $ |
| fixe_cooldown_6h | rush | × 4,0 | 13,9 % | 66,5 % | 0,054 $ | 35 463 $ |
| relatif_2x5_cooldown_6h | or | × 0,5 | 4,9 % | 66,1 % | 0,055 $ | 4 281 $ |
| relatif_2x5_cooldown_6h | or | × 1,0 | 3,9 % | 65,0 % | 0,057 $ | 8 758 $ |
| relatif_2x5_cooldown_6h | or | × 2,0 | 5,2 % | 66,4 % | 0,054 $ | 16 930 $ |
| relatif_2x5_cooldown_6h | or | × 4,0 | 5,2 % | 66,5 % | 0,054 $ | 33 888 $ |
| relatif_2x5_cooldown_6h | rush | × 0,5 | 4,9 % | 65,2 % | 0,057 $ | 4 431 $ |
| relatif_2x5_cooldown_6h | rush | × 1,0 | 3,9 % | 65,0 % | 0,057 $ | 8 758 $ |
| relatif_2x5_cooldown_6h | rush | × 2,0 | 5,2 % | 65,2 % | 0,057 $ | 17 690 $ |
| relatif_2x5_cooldown_6h | rush | × 4,0 | 5,2 % | 65,2 % | 0,057 $ | 35 455 $ |

**Réserve** (R₀ 1 % sur 10 000 ventes, table rush, κ recalibré sur la part observée, 10 000 trajectoires). Les gold packs d'un rush arrivent groupés : on compare au même nombre de gold packs répartis au hasard.

| Cas | g_rush | R₀ 1 %, rush groupés | R₀ 1 %, mêmes gold packs indépendants |
|---|---:|---:|---:|
| relatif_2x5_cooldown_6h_x1 | 4,0 % | 65 $ | 53 $ |
| fixe_x2 | 68,6 % | 82 $ | 49 $ |

**Arbitrage pendant un rush.** Gain moyen « j'achète, je brûle tout » d'un pack : 181 % du prix avec la table or, 80 % avec la table rush (borne : 85 %). Au-dessus de 100 %, chaque pack acheté pendant un rush rapporte en moyenne ; un gros joueur a alors intérêt à déclencher le rush lui-même.
