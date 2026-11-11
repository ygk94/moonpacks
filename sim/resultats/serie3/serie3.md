# Série 3 : packs à bas prix et mécaniques

## Coûts réels et rentabilité

NEAR à 2,50 $. Gaz : 48 Tgas × 0,0001 NEAR/Tgas = 0,0048 NEAR (0,012 $). Stockage : 4 040 octets = 0,0404 NEAR (0,101 $), ou 1 000 octets = 0,0100 NEAR (0,025 $). Achat groupé : 0,75 % de la couverture (fourchette 0,5 % à 1 %).

**Couverture 65 %.** « Prudent » : l'équipe paie le gaz (relais, ou par prudence), l'acheteur paie le stockage en plus du prix. Ancienne marge : tableau de `docs/mecaniques.md` (coûts de 0,05 $).

| Prix | NEAR | Ancienne marge | Coûts équipe | **Marge (prudent)** | Marge, gaz payé par l'acheteur | Après réserve δ = 5 % | Marge si l'équipe paie le stockage, 4 Ko / 1 Ko | Débours acheteur, 4 Ko / 1 Ko |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0,15 $ | 0,060 | 0,002 $ | 0,013 $ | **0,040 $ (27 %)** | 0,052 $ (35 %) | 0,032 $ | -0,061 $ / 0,015 $ | 0,251 $ (+67 %) / 0,175 $ (+17 %) |
| 0,20 $ | 0,080 | 0,020 $ | 0,013 $ | **0,057 $ (29 %)** | 0,069 $ (35 %) | 0,047 $ | -0,044 $ / 0,032 $ | 0,301 $ (+50 %) / 0,225 $ (+12 %) |
| 0,35 $ | 0,140 | 0,072 $ | 0,014 $ | **0,109 $ (31 %)** | 0,121 $ (35 %) | 0,091 $ | 0,008 $ / 0,084 $ | 0,451 $ (+29 %) / 0,375 $ (+7 %) |
| 0,50 $ | 0,200 | 0,125 $ | 0,014 $ | **0,161 $ (32 %)** | 0,173 $ (35 %) | 0,136 $ | 0,060 $ / 0,136 $ | 0,601 $ (+20 %) / 0,525 $ (+5 %) |
| 1,00 $ | 0,400 | 0,300 $ | 0,017 $ | **0,333 $ (33 %)** | 0,345 $ (35 %) | 0,283 $ | 0,232 $ / 0,308 $ | 1,101 $ (+10 %) / 1,025 $ (+2 %) |

**Marge (prudent) selon la couverture, et frais d'achat de 0,5 à 1 %**

| Prix | couverture 50 % | couverture 65 % | couverture 70 % |
|---:|---:|---:|---:|
| 0,15 $ | 0,062 $ à 0,063 $ (42 %) | 0,040 $ à 0,040 $ (26 %) | 0,032 $ à 0,032 $ (21 %) |
| 0,20 $ | 0,087 $ à 0,088 $ (43 %) | 0,057 $ à 0,057 $ (28 %) | 0,047 $ à 0,047 $ (23 %) |
| 0,35 $ | 0,161 $ à 0,162 $ (46 %) | 0,108 $ à 0,109 $ (31 %) | 0,091 $ à 0,092 $ (26 %) |
| 0,50 $ | 0,236 $ à 0,237 $ (47 %) | 0,160 $ à 0,161 $ (32 %) | 0,135 $ à 0,136 $ (27 %) |
| 1,00 $ | 0,483 $ à 0,486 $ (48 %) | 0,332 $ à 0,335 $ (33 %) | 0,281 $ à 0,285 $ (28 %) |

**Prix de seuil (marge nulle)**

| Variante | couverture 50 % | couverture 65 % | couverture 70 % |
|---|---:|---:|---:|
| Équipe paie le gaz, acheteur le stockage | 0,024 $ | 0,035 $ | 0,041 $ |
| Acheteur paie gaz et stockage | 0,000 $ | 0,000 $ | 0,000 $ |
| Équipe paie gaz et stockage (4 Ko) | 0,228 $ | 0,327 $ | 0,383 $ |
| Équipe paie gaz et stockage (1 Ko) | 0,075 $ | 0,107 $ | 0,126 $ |

**Packs pour couvrir les coûts fixes** (prudent ; marge avant réserve / après δ = 5 %)

| Prix | Couverture | Marge (NEAR) | 5 NEAR | 10 NEAR | 10 NEAR après δ |
|---:|---:|---:|---:|---:|---:|
| 0,15 $ | 50 % | 0,0250 | 201 | 401 | 456 |
| 0,20 $ | 50 % | 0,0349 | 144 | 287 | 324 |
| 0,35 $ | 50 % | 0,0647 | 78 | 155 | 174 |
| 0,50 $ | 50 % | 0,0945 | 53 | 106 | 119 |
| 1,00 $ | 50 % | 0,1937 | 26 | 52 | 58 |
| 0,15 $ | 65 % | 0,0159 | 315 | 629 | 775 |
| 0,20 $ | 65 % | 0,0228 | 220 | 439 | 532 |
| 0,35 $ | 65 % | 0,0435 | 115 | 230 | 274 |
| 0,50 $ | 65 % | 0,0642 | 78 | 156 | 185 |
| 1,00 $ | 65 % | 0,1332 | 38 | 76 | 89 |
| 0,15 $ | 70 % | 0,0129 | 389 | 777 | 1 012 |
| 0,20 $ | 70 % | 0,0188 | 267 | 533 | 677 |
| 0,35 $ | 70 % | 0,0365 | 138 | 275 | 340 |
| 0,50 $ | 70 % | 0,0542 | 93 | 185 | 227 |
| 1,00 $ | 70 % | 0,1131 | 45 | 89 | 108 |

## Le pack à chaque prix (sans mécanique)

Même structure qu'en série 2 (150 brûlables) : tout est proportionnel au prix, sauf les plafonds par carte, jamais atteints ici.

| Prix | Couverture | Adossement moyen | σ / prix | P(≥ 1 brûlable) | Plus petite brûlable | Légendaire brûlable | Mythique | P(adossement ≥ prix) | Gain « brûle tout » / prix | Borne β |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0,15 $ | 50 % | 0,075 $ | 1,67 | 13,3 % | 0,16 $ | 1,17 $ à 2,94 $ | 8 $ | 13,3 % | 51,4 % | 84,9 % |
| 0,20 $ | 50 % | 0,100 $ | 1,67 | 13,3 % | 0,21 $ | 1,57 $ à 3,92 $ | 11 $ | 13,3 % | 51,5 % | 84,9 % |
| 0,35 $ | 50 % | 0,175 $ | 1,67 | 13,3 % | 0,37 $ | 2,74 $ à 6,85 $ | 19 $ | 13,3 % | 51,6 % | 84,8 % |
| 0,50 $ | 50 % | 0,250 $ | 1,67 | 13,3 % | 0,52 $ | 3,92 $ à 9,79 $ | 28 $ | 13,3 % | 51,6 % | 84,8 % |
| 1,00 $ | 50 % | 0,500 $ | 1,67 | 13,3 % | 1,04 $ | 7,83 $ à 19,58 $ | 55 $ | 13,3 % | 51,6 % | 84,7 % |
| 0,15 $ | 65 % | 0,098 $ | 2,13 | 13,3 % | 0,20 $ | 1,53 $ à 3,83 $ | 8 $ | 13,3 % | 65,9 % | 84,9 % |
| 0,20 $ | 65 % | 0,130 $ | 2,13 | 13,3 % | 0,27 $ | 2,04 $ à 5,10 $ | 11 $ | 13,3 % | 65,9 % | 84,9 % |
| 0,35 $ | 65 % | 0,227 $ | 2,13 | 13,3 % | 0,48 $ | 3,57 $ à 8,93 $ | 19 $ | 13,3 % | 66,0 % | 84,8 % |
| 0,50 $ | 65 % | 0,325 $ | 2,13 | 13,3 % | 0,68 $ | 5,10 $ à 12,76 $ | 28 $ | 13,3 % | 66,0 % | 84,8 % |
| 1,00 $ | 65 % | 0,650 $ | 2,13 | 13,3 % | 1,36 $ | 10,21 $ à 25,52 $ | 55 $ | 13,3 % | 66,1 % | 84,7 % |
| 0,15 $ | 70 % | 0,105 $ | 2,29 | 13,3 % | 0,22 $ | 1,65 $ à 4,12 $ | 8 $ | 13,3 % | 70,7 % | 84,9 % |
| 0,20 $ | 70 % | 0,140 $ | 2,29 | 13,3 % | 0,29 $ | 2,20 $ à 5,50 $ | 11 $ | 13,3 % | 70,7 % | 84,9 % |
| 0,35 $ | 70 % | 0,245 $ | 2,29 | 13,3 % | 0,51 $ | 3,85 $ à 9,62 $ | 19 $ | 13,3 % | 70,8 % | 84,8 % |
| 0,50 $ | 70 % | 0,350 $ | 2,29 | 13,3 % | 0,73 $ | 5,50 $ à 13,75 $ | 28 $ | 13,3 % | 70,8 % | 84,8 % |
| 1,00 $ | 70 % | 0,700 $ | 2,29 | 13,3 % | 1,47 $ | 11,00 $ à 27,50 $ | 55 $ | 13,3 % | 70,9 % | 84,7 % |

## Réserve et ruine

Monte-Carlo de la série 2 : la réserve reçoit (β + δ)·P par vente et paie l'adossement ; ruine = passer sous V_cap. Simulé à 0,20 $, puis converti : à structure égale, la réserve est proportionnelle au prix (vérifié à 1 $ plus bas).

**Réserve en multiples du prix du pack** (V_cap = 60 × prix compris)

| Couverture | δ | Ventes | Trajectoires | R₀ 5 % | R₀ 1 % |
|---:|---:|---:|---:|---:|---:|
| 50 % | 5 % | 10 000 | 10 000 | 154 | 208 |
| 50 % | 5 % | 100 000 | 2 000 | 150 | 218 |
| 65 % | 2 % | 10 000 | 10 000 | 336 | 464 |
| 65 % | 5 % | 10 000 | 10 000 | 205 | 287 |
| 65 % | 10 % | 10 000 | 10 000 | 138 | 179 |
| 65 % | 2 % | 100 000 | 2 000 | 412 | 565 |
| 65 % | 5 % | 100 000 | 2 000 | 202 | 308 |
| 65 % | 10 % | 100 000 | 2 000 | 137 | 183 |
| 70 % | 5 % | 10 000 | 10 000 | 223 | 318 |
| 70 % | 5 % | 100 000 | 2 000 | 222 | 341 |

**Réserve en dollars** (δ = 5 %)

| Prix | Couverture | R₀ 5 %, 10 000 ventes | R₀ 1 %, 10 000 | R₀ 5 %, 100 000 | R₀ 1 %, 100 000 |
|---:|---:|---:|---:|---:|---:|
| 0,15 $ | 50 % | 23 $ | 31 $ | 23 $ | 33 $ |
| 0,20 $ | 50 % | 31 $ | 42 $ | 30 $ | 44 $ |
| 0,35 $ | 50 % | 54 $ | 73 $ | 53 $ | 76 $ |
| 0,50 $ | 50 % | 77 $ | 104 $ | 75 $ | 109 $ |
| 1,00 $ | 50 % | 154 $ | 208 $ | 150 $ | 218 $ |
| 0,15 $ | 65 % | 31 $ | 43 $ | 30 $ | 46 $ |
| 0,20 $ | 65 % | 41 $ | 57 $ | 40 $ | 62 $ |
| 0,35 $ | 65 % | 72 $ | 101 $ | 71 $ | 108 $ |
| 0,50 $ | 65 % | 102 $ | 144 $ | 101 $ | 154 $ |
| 1,00 $ | 65 % | 205 $ | 287 $ | 202 $ | 308 $ |
| 0,15 $ | 70 % | 34 $ | 48 $ | 33 $ | 51 $ |
| 0,20 $ | 70 % | 45 $ | 64 $ | 44 $ | 68 $ |
| 0,35 $ | 70 % | 78 $ | 111 $ | 78 $ | 119 $ |
| 0,50 $ | 70 % | 112 $ | 159 $ | 111 $ | 170 $ |
| 1,00 $ | 70 % | 223 $ | 318 $ | 222 $ | 341 $ |

Vérification à 1 $ (65 %, 10 000 ventes) : R₀ 1 % = 274 × prix, contre 287 × prix à 0,20 $.

## Compteur de pitié

Population : 100 000 joueurs, packs par joueur lognormaux (médiane 4, σ = 1,4, au plus 5 000). Point 0,20 $, 65 %. κ est calibré sur g_∞ (colonne « couverture std / or »), puis on lit la couverture réalisée dans la population (g_pop).

| N | p0 | k | g_∞ (1 sur) | g_pop | Joueurs sans gold | Gold garantis | Table | Couverture std / or | Part du budget | P(≥ 1 brûlable) en or | Gain « brûle tout » d'un gold / prix | Couverture réalisée (g_pop) |
|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 10 | 2 % | 1,0 % | 8,2 | 9,45 % | 65 % | 49 % | argent | 60,6 % / 97 % | 18 % | 20 % | 97 % | 64,0 % |
| 10 | 2 % | 1,0 % | 8,2 | 9,45 % | 65 % | 49 % | doux | 57,5 % / 119 % | 22 % | 25 % | 118 % | 63,3 % |
| 10 | 2 % | 1,0 % | 8,2 | 9,45 % | 65 % | 49 % | or | 51,5 % / 162 % | 30 % | 36 % | 160 % | 62,0 % |
| 10 | 2 % | 1,0 % | 8,2 | 9,45 % | 65 % | 49 % | fort | 46,4 % / 199 % | 37 % | 43 % | 196 % | 60,8 % |
| 15 | 2 % | 0,4 % | 11,7 | 6,17 % | 73 % | 40 % | argent | 61,9 % / 99 % | 13 % | 20 % | 99 % | 64,1 % |
| 15 | 2 % | 0,4 % | 11,7 | 6,17 % | 73 % | 40 % | doux | 59,6 % / 123 % | 16 % | 25 % | 122 % | 63,5 % |
| 15 | 2 % | 0,4 % | 11,7 | 6,17 % | 73 % | 40 % | or | 55,0 % / 172 % | 23 % | 36 % | 170 % | 62,2 % |
| 15 | 2 % | 0,4 % | 11,7 | 6,17 % | 73 % | 40 % | fort | 50,8 % / 218 % | 29 % | 43 % | 214 % | 61,1 % |
| 20 | 2 % | 0,2 % | 15,0 | 4,64 % | 77 % | 33 % | argent | 62,5 % / 100 % | 10 % | 20 % | 100 % | 64,3 % |
| 20 | 2 % | 0,2 % | 15,0 | 4,64 % | 77 % | 33 % | doux | 60,7 % / 125 % | 13 % | 25 % | 124 % | 63,7 % |
| 20 | 2 % | 0,2 % | 15,0 | 4,64 % | 77 % | 33 % | or | 56,9 % / 179 % | 18 % | 36 % | 176 % | 62,6 % |
| 20 | 2 % | 0,2 % | 15,0 | 4,64 % | 77 % | 33 % | fort | 53,4 % / 229 % | 23 % | 43 % | 224 % | 61,5 % |
| 30 | 1 % | 0,2 % | 20,8 | 3,08 % | 83 % | 19 % | argent | 63,2 % / 101 % | 7 % | 20 % | 101 % | 64,3 % |
| 30 | 1 % | 0,2 % | 20,8 | 3,08 % | 83 % | 19 % | doux | 61,8 % / 128 % | 9 % | 25 % | 127 % | 63,9 % |
| 30 | 1 % | 0,2 % | 20,8 | 3,08 % | 83 % | 19 % | or | 58,9 % / 185 % | 14 % | 36 % | 182 % | 62,8 % |
| 30 | 1 % | 0,2 % | 20,8 | 3,08 % | 83 % | 19 % | fort | 56,1 % / 240 % | 18 % | 43 % | 235 % | 61,8 % |

**Proposition : N = 20, p0 = 2 %, k = 0,2 %, table « or »** (probabilités × rare 2,0, epique 3,0, legendaire 4,0, mythique 4,0), κ calibré sur la population.

| Grandeur | Valeur |
|---|---:|
| Cycle moyen entre deux gold packs | 15,0 packs |
| Cycles qui vont jusqu'à la garantie | 48 % |
| g_∞ / g_pop | 6,65 % / 4,64 % |
| Joueurs qui ne voient aucun gold pack | 77 % |
| Packs ouverts par les 5 % plus gros joueurs | 40 % |
| Couverture d'un pack standard / d'un gold pack | 59,1 % / 185 % |
| Valeur moyenne d'un pack standard / gold | 0,118 $ / 0,371 $ |
| Part du budget jetons prise par les gold packs | 13 % |
| P(≥ 1 brûlable), standard / gold | 13 % / 36 % |
| Plus petite brûlable (κ baisse de 9 %) | 0,25 $ |
| Couverture si tous les compteurs servent (g_∞ : baleines, compteur revendable) | 67,5 % |
| R₀ 1 % sur 10 000 ventes, sans / avec pitié (10 000 trajectoires) | 57 $ / 54 $ |

**Sensibilité à la population** (κ de la proposition)

| Médiane | σ | Packs moyens par joueur | g_pop | Couverture réalisée |
|---:|---:|---:|---:|---:|
| 2 | 1,0 | 3,4 | 2,73 % | 62,6 % |
| 4 | 1,4 | 10,6 | 4,65 % | 65,0 % |
| 8 | 1,6 | 28,4 | 5,71 % | 66,4 % |
| 20 | 1,8 | 95,2 | 6,31 % | 67,1 % |

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

## Rareté pilotée par les burns

Poids effectif = poids × en circulation / émises, sur 100 000 packs, délai moyen avant burn 5 000 packs. « formule_brute » : la part perdue revient à toute la rareté, κ fixe. « formule_recalibree » : idem, κ recalculé pour tenir β. « entre_brulables » : la part perdue revient aux autres brûlables de la rareté. Le rapport (σ fin / σ début)² donne l'ordre de grandeur de la réserve (formule normale).

| Variante | Taux de burn | Couverture finale | Couverture moyenne | Brûlables / pack, début → fin | κ fin / début | (σ fin / σ début)² | Coins au plancher (sur 150) | Jetons bloqués à la fin |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| formule_brute | 20 % | 56,9 % | 57,0 % | 0,139 → 0,118 | 1,00 | 0,91 | 10 | 9 202 $ |
| formule_brute | 50 % | 43,6 % | 46,5 % | 0,139 → 0,085 | 1,00 | 0,75 | 19 | 4 934 $ |
| formule_brute | 80 % | 23,3 % | 28,1 % | 0,139 → 0,041 | 1,00 | 0,48 | 44 | 1 363 $ |
| formule_recalibree | 20 % | 65,0 % | 64,1 % | 0,139 → 0,118 | 1,14 | 1,17 | 10 | 10 508 $ |
| formule_recalibree | 50 % | 65,0 % | 65,1 % | 0,139 → 0,085 | 1,50 | 1,61 | 19 | 7 350 $ |
| formule_recalibree | 80 % | 65,0 % | 64,6 % | 0,139 → 0,041 | 2,83 | 3,40 | 44 | 3 817 $ |
| entre_brulables | 20 % | 65,0 % | 65,2 % | 0,139 → 0,139 | 1,00 | 1,00 | 8 | 10 595 $ |
| entre_brulables | 50 % | 65,0 % | 64,9 % | 0,139 → 0,139 | 1,00 | 1,00 | 14 | 6 806 $ |
| entre_brulables | 80 % | 65,0 % | 64,6 % | 0,139 → 0,139 | 1,00 | 1,00 | 38 | 3 145 $ |
| entre_brulables_plancher | 20 % | 65,0 % | 66,1 % | 0,139 → 0,139 | 1,00 | 1,00 | 0 | 10 699 $ |
| entre_brulables_plancher | 50 % | 65,0 % | 64,7 % | 0,139 → 0,139 | 1,00 | 1,00 | 2 | 6 711 $ |
| entre_brulables_plancher | 80 % | 65,0 % | 65,2 % | 0,139 → 0,139 | 1,00 | 1,00 | 95 | 3 146 $ |

## Résurrection des coins morts

Coins morts du catalogue v2 (hors arnaques) : 1 059 communes, 84 épiques, 2 légendaires. 50 000 packs par mois. Un exemplaire ressuscité reçoit la valeur moyenne d'une brûlable de sa rareté, achetée avec 10 % de surcoût. Le coût rapporté au chiffre d'affaires ne dépend pas du volume (exemplaires et ventes croissent ensemble), mais il croît avec la durée.

| p par coin et par an | Durée | Résurrections (moy. / p99) | Coût moyen | Coût p99 | En part du prix, moyen / p99 | Dont communes | Sans les communes, p99 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0,5 % | 12 mois | 5,7 / 12 | 2 057 $ | 4 748 $ | 1,7 % / 4,0 % | 94 % | 0,73 % |
| 0,5 % | 24 mois | 11,4 / 20 | 8 209 $ | 15 550 $ | 3,4 % / 6,5 % | 94 % | 1,01 % |
| 1,0 % | 12 mois | 11,4 / 20 | 4 115 $ | 7 792 $ | 3,4 % / 6,5 % | 94 % | 1,01 % |
| 1,0 % | 24 mois | 22,7 / 35 | 16 402 $ | 26 321 $ | 6,8 % / 11,0 % | 94 % | 1,42 % |
| 2,0 % | 12 mois | 22,8 / 35 | 8 244 $ | 13 207 $ | 6,9 % / 11,0 % | 94 % | 1,43 % |
| 2,0 % | 24 mois | 45,3 / 61 | 32 729 $ | 46 050 $ | 13,6 % / 19,2 % | 94 % | 2,18 % |
| 5,0 % | 12 mois | 57,2 / 75 | 20 628 $ | 28 139 $ | 17,2 % / 23,4 % | 94 % | 2,52 % |
| 5,0 % | 24 mois | 111,6 / 135 | 80 489 $ | 100 635 $ | 33,5 % / 41,9 % | 94 % | 3,91 % |

**Règle de plafond : enveloppe fixe par résurrection, fonds à 1 % du prix** (1 200 $ sur 12 mois). Enveloppe = fonds / nombre de résurrections p99, partagée entre les exemplaires en circulation. Valeur reçue par exemplaire au bout de 12 mois :

| p par an | Enveloppe | Par commune (part de la valeur pleine) | Par épique (part de la valeur pleine) |
|---:|---:|---:|---:|
| 0,5 % | 100 $ | 0,0445 $ (15,0 %) | 0,178 $ (20 %) |
| 1,0 % | 60 $ | 0,0267 $ (9,0 %) | 0,107 $ (12 %) |
| 2,0 % | 34 $ | 0,0153 $ (5,1 %) | 0,061 $ (7 %) |
| 5,0 % | 16 $ | 0,0071 $ (2,4 %) | 0,029 $ (3 %) |

Sans les communes, payer la pleine valeur à p = 2 %/an demande un fonds de 1,43 % du prix (p99, 12 mois).

## Synthèse : pitié et rush proposés, ensemble

Pitié N = 20, p0 = 2 %, k = 0,2 % (g_pop = 4,64 %) ; rush à palier relatif avec 6 h de pause (g_rush ≈ 3,9 %), table rush à 80 %. Couverture moyenne visée 65 %, δ = 5 %. R₀ sur 10 000 trajectoires.

| Prix | Couverture std / gold / rush | Marge / pack (prudent) | Débours acheteur 4 Ko / 1 Ko | R₀ 1 %, 10 000 ventes | R₀ 1 %, 100 000 ventes | Packs pour 10 NEAR de coûts fixes |
|---:|---:|---:|---:|---:|---:|---:|
| 0,20 $ | 58,6 % / 184 % / 80 % | 0,057 $ (29 %) | 0,301 $ / 0,225 $ | 55 $ | 56 $ | 439 |
| 0,50 $ | 58,6 % / 184 % / 80 % | 0,161 $ (32 %) | 0,601 $ / 0,525 $ | 137 $ | 141 $ | 156 |
| 1,00 $ | 58,6 % / 184 % / 80 % | 0,333 $ (33 %) | 1,101 $ / 1,025 $ | 273 $ | 282 $ | 76 |
