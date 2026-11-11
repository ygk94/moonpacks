# Série 4 : valeur aléatoire par pack, gold pack redéfini

## Tables de valeur V

V en multiples du prix du pack. Paliers : normal et rush de 20 à 100 % par pas de 5 %, puis de 110 à 200 % par pas de 10 % (27 paliers) ; gold de 100 à 500 % (18 paliers). Forme lognormale discrétisée (σ = 0,6 pour normal et rush, 0,4 pour le gold), poids entiers sur 1 000 000. (a) : la cible est la moyenne ; (b) : la cible est la médiane.

| Variante | Table | Min | Max | q10 | Médiane | q90 | **Moyenne** | Écart-type | Sous 50 % | Au-dessus de 100 % |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| (a) | normale | 20 % | 200 % | 30 % | 65 % | 140 % | **75,0 %** | 44 % | 31,0 % | 20,5 % |
| (a) | gold | 100 % | 500 % | 110 % | 180 % | 300 % | **200,0 %** | 80 % | 0,0 % | 92,0 % |
| (a) | rush | 20 % | 200 % | 30 % | 70 % | 150 % | **80,0 %** | 45 % | 26,9 % | 24,0 % |
| (a) | **flux réel** (pitié + rush) | 20 % | 500 % | 30 % | 65 % | 150 % | **81,0 %** | 53 % | 29,3 % | 23,9 % |
| (b) | normale | 20 % | 200 % | 35 % | 75 % | 160 % | **86,6 %** | 48 % | 22,3 % | 28,8 % |
| (b) | gold | 100 % | 500 % | 120 % | 200 % | 350 % | **216,4 %** | 87 % | 0,0 % | 94,7 % |
| (b) | rush (= normale) | 20 % | 200 % | 35 % | 75 % | 160 % | **86,6 %** | 48 % | 22,3 % | 28,8 % |
| (b) | **flux réel** (pitié + rush) | 20 % | 500 % | 35 % | 80 % | 180 % | **92,6 %** | 57 % | 21,2 % | 31,9 % |

Médiane d'une table discrète : plus petit palier où la fonction de répartition atteint 50 %.

## Effet de la pitié, du gold pack et du rush sur la moyenne

Pitié N = 20, p0 = 2 %, k = 0,2 % ; population de 100 000 joueurs (médiane 4 packs) : g_pop = 4,64 % des packs en gold, g_∞ = 6,65 % pour un joueur qui ne s'arrête pas (ou un compteur revendable). Rush : 5 % des packs non gold. La pitié l'emporte sur le rush.

| Variante | Normal seul | + gold de pitié (g_pop) | **+ rush (flux réel)** | Flux avec g_∞ | Poids du gold | Poids du rush | Part du budget en gold | Moyenne normale pour 75 % au global |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| (a) | 75,0 % | 80,8 % | **81,0 %** | 83,5 % | +5,8 pts | +0,2 pts | 11 % | 68,3 % |
| (b) | 86,6 % | 92,6 % | **92,6 %** | 95,2 % | +6,0 pts | +0,0 pts | 11 % | 67,2 % |

### Le mythique du gold pack (20 %)

Un gold pack sort un mythique avec la probabilité 20 %, un pack normal avec 0,010 % (1 sur 10 000). En moyenne sur le flux : 0,94 % des packs, soit **1 mythique tous les 107 packs, 94 fois plus qu'avant**.

| Lecture | Coût en jetons d'un gold pack | Coût moyen par pack vendu (g_pop) | Avec g_∞ |
|---|---:|---:|---:|
| **Mythique dans V** (multiplicateur, recommandé) | 0 en plus de V | 0 | 0 |
| Mythique à valeur fixe hors V (55,2 × prix, comme en série 3) | +1104 % du prix | +51,7 % du prix | +73,9 % du prix |

**Coût d'un mythique hors V, en points de couverture du flux réel** (part du mythique dans le 5e emplacement du gold × valeur fixe ; les mythiques des packs normaux et rush comptés aussi) :

| Valeur fixe du mythique | mythique à 20 % dans le gold | mythique à 5 % dans le gold | mythique à 2 % dans le gold |
|---:|---:|---:|---:|
| 5,0 × prix | +4,7 pts | +1,2 pts | +0,5 pts |
| 10,0 × prix | +9,4 pts | +2,4 pts | +1,0 pts |
| 55,2 × prix | +51,7 pts | +13,3 pts | +5,7 pts |

Hors V à 55,2 × prix, le flux paierait 133 % du prix en jetons : la maison perd à chaque pack et la ruine est certaine, quelle que soit la réserve. Seul le stock borne la perte : 30 mythiques × 55,2 = 1 656 × prix (331 $ / 828 $), dépensés presque tous dans les premiers milliers de packs.

Stock : avec 10 exemplaires par mythique (`serie-exemple.json`, 30 au total), les mythiques sont épuisés après **3 202 packs** (contre 300 000 sans le gold pack) ; le 5e emplacement du gold retombe alors sur le légendaire. Légendaires : 4,93 % par pack (contre 0,98 %), stock de 1 050 épuisé après 21 290 packs.

## Répartition de V entre les cartes

Variante (a). Multiplicateurs : commune 1, rare 2, epique 3, legendaire 6, mythique 20. 20 communes brûlables (sur 91 vivantes) : sans elles, le 5e emplacement ne peut pas retomber vers le bas et 65 % des packs auraient une rare brûlable comme seule brûlable (11 rares brûlables seulement). 1 000 000 packs par type.

**Pack normal** : 1,12 brûlables par pack (1 seule : 89 %). Cartes par pack : commune 4,34, rare 0,43, epique 0,22, legendaire 0,01, mythique 0,00.

| Rareté | Brûlables par pack | Part de V | Valeur moyenne (× prix) | q10 / médiane / q90 | Min / max | Moyenne à 0,20 $ | Moyenne à 0,50 $ |
|---|---:|---:|---:|---:|---:|---:|---:|
| commune | 0,710 | 62,7 % | 0,66 | 0,20 / 0,55 / 1,30 | 0,010 / 2,00 | 0,132 $ | 0,331 $ |
| rare | 0,224 | 20,8 % | 0,70 | 0,25 / 0,60 / 1,30 | 0,044 / 2,00 | 0,139 $ | 0,349 $ |
| epique | 0,176 | 15,6 % | 0,66 | 0,25 / 0,55 / 1,20 | 0,060 / 2,00 | 0,133 $ | 0,332 $ |
| legendaire | 0,010 | 0,9 % | 0,71 | 0,27 / 0,60 / 1,30 | 0,120 / 2,00 | 0,141 $ | 0,353 $ |
| mythique | 0,000 | 0,0 % | 0,76 | 0,27 / 0,70 / 1,37 | 0,190 / 2,00 | 0,152 $ | 0,380 $ |

Cartes brûlables sous 0,02 NEAR (0,05 $) à 0,20 $ : 11,2 % ; plus petite carte : 0,010 × prix (0,002 $), 0,005 $ à 0,50 $.

**Pack gold** : 2,38 brûlables par pack (1 seule : 16 %). Cartes par pack : rare 1,41, epique 2,53, legendaire 0,86, mythique 0,20.

| Rareté | Brûlables par pack | Part de V | Valeur moyenne (× prix) | q10 / médiane / q90 | Min / max | Moyenne à 0,20 $ | Moyenne à 0,50 $ |
|---|---:|---:|---:|---:|---:|---:|---:|
| rare | 0,067 | 1,1 % | 0,32 | 0,14 / 0,29 / 0,55 | 0,059 / 1,25 | 0,064 $ | 0,159 $ |
| epique | 1,262 | 29,5 % | 0,47 | 0,20 / 0,42 / 0,80 | 0,079 / 1,67 | 0,093 $ | 0,234 $ |
| legendaire | 0,852 | 52,8 % | 1,24 | 0,60 / 1,10 / 2,00 | 0,158 / 5,00 | 0,248 $ | 0,619 $ |
| mythique | 0,200 | 16,7 % | 1,67 | 0,92 / 1,54 / 2,61 | 0,526 / 5,00 | 0,334 $ | 0,836 $ |

Cartes brûlables sous 0,02 NEAR (0,05 $) à 0,20 $ : 9,8 % ; plus petite carte : 0,059 × prix (0,012 $), 0,029 $ à 0,50 $.

**Pack rush** : 1,14 brûlables par pack (1 seule : 87 %). Cartes par pack : commune 4,19, rare 0,50, epique 0,29, legendaire 0,01, mythique 0,00.

| Rareté | Brûlables par pack | Part de V | Valeur moyenne (× prix) | q10 / médiane / q90 | Min / max | Moyenne à 0,20 $ | Moyenne à 0,50 $ |
|---|---:|---:|---:|---:|---:|---:|---:|
| commune | 0,622 | 53,7 % | 0,69 | 0,20 / 0,60 / 1,40 | 0,020 / 2,00 | 0,138 $ | 0,345 $ |
| rare | 0,264 | 24,4 % | 0,74 | 0,25 / 0,63 / 1,40 | 0,018 / 2,00 | 0,147 $ | 0,368 $ |
| epique | 0,236 | 20,6 % | 0,70 | 0,25 / 0,60 / 1,30 | 0,046 / 2,00 | 0,140 $ | 0,349 $ |
| legendaire | 0,014 | 1,3 % | 0,74 | 0,30 / 0,64 / 1,40 | 0,107 / 2,00 | 0,148 $ | 0,371 $ |
| mythique | 0,000 | 0,0 % | 0,85 | 0,40 / 0,70 / 1,74 | 0,182 / 2,00 | 0,170 $ | 0,425 $ |

Cartes brûlables sous 0,02 NEAR (0,05 $) à 0,20 $ : 10,8 % ; plus petite carte : 0,018 × prix (0,004 $), 0,009 $ à 0,50 $.


## Marge par pack

NEAR à 2,5 $. Gaz 48 Tgas = 0,012 $, payé par l'équipe (cas prudent) ; stockage ~1 Ko payé par l'acheteur en plus du prix (dépôt) ; achat groupé des jetons 0,5 % à 1 % de la valeur (0,75 % au centre). Couverture = flux réel (pitié g_pop et rush).

| Variante | Prix | Couverture | **Marge** | Fourchette (frais 1 % → 0,5 %) | Marge si l'acheteur paie le gaz | Après réserve δ = 5 % | Débours de l'acheteur | Packs pour 10 NEAR de coûts fixes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| (a) | 0,20 $ | 81,0 % | **0,025 $ (12 %)** | 0,024 $ à 0,025 $ | 0,037 $ (18 %) | 0,015 $ | 0,225 $ | 1 012 |
| (a) | 0,50 $ | 81,0 % | **0,080 $ (16 %)** | 0,079 $ à 0,081 $ | 0,092 $ (18 %) | 0,055 $ | 0,525 $ | 314 |
| (b) | 0,20 $ | 92,6 % | **0,001 $ (1 %)** | 0,001 $ à 0,002 $ | 0,013 $ (7 %) | -0,009 $ | 0,225 $ | 18 034 |
| (b) | 0,50 $ | 92,6 % | **0,021 $ (4 %)** | 0,020 $ à 0,023 $ | 0,033 $ (7 %) | -0,004 $ | 0,525 $ | 1 165 |

Rappel série 3 (couverture 65 %) : 0,057 $ (29 %) à 0,20 $, 0,161 $ (32 %) à 0,50 $.

## Borne anti-arbitrage

Gain moyen de « j'achète, je brûle tout, je revends le reste », en part du prix : c × couverture + reventes − gaz des burns, avec c = 0,961 (achat, burn, revente). Borne : 85 % (ε = 15 %). Le cycle de pitié est celui d'un joueur qui ouvre jusqu'au gold pack (g_∞) ; le gold pack seul n'est choisissable qu'au 20e pack, après 19 packs normaux.

| Variante | Pack normal | Pack rush | Cycle de pitié | Gold pack seul | Borne |
|---|---:|---:|---:|---:|---:|
| (a) | 73,3 % | 78,1 % | 81,5 % | 197 % | 85 % |
| (b) | 84,4 % | 84,5 % | **93,0 %** | 213 % | 85 % |

En gras : au-dessus de la borne.

## Réserve et ruine

La réserve reçoit (couverture + δ) × prix par vente (δ = 5 %) et paie V. Packs indépendants, type tiré avec les parts du flux réel. R₀ = plus gros V possible + quantile de la plus forte baisse : la réserve peut toujours payer le pack suivant, sauf avec la probabilité visée. En multiples du prix (tout est proportionnel au prix), puis en dollars.

| Cas | Couverture | Ventes | Trajectoires | V max | R₀ 5 % | **R₀ 1 %** | R₀ 1 % à 0,20 $ | R₀ 1 % à 0,50 $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| (a) | 81,0 % | 10 000 | 5 000 | 5,0 | 14,0 × P | **19,2 × P** | 4 $ | 10 $ |
| (a) | 81,0 % | 100 000 | 2 000 | 5,0 | 13,6 × P | **19,0 × P** | 4 $ | 10 $ |
| (b) | 92,6 % | 10 000 | 5 000 | 5,0 | 15,1 × P | **21,3 × P** | 4 $ | 11 $ |
| (b) | 92,6 % | 100 000 | 2 000 | 5,0 | 15,2 × P | **21,2 × P** | 4 $ | 11 $ |
| (a) + mythique hors V à 5 × prix, 2 % du gold | 81,5 % | 10 000 | 5 000 | 10,0 | 20,4 × P | **27,0 × P** | 5 $ | 14 $ |
| (a) + mythique hors V à 5 × prix, 2 % du gold | 81,5 % | 100 000 | 2 000 | 10,0 | 20,4 × P | **26,5 × P** | 5 $ | 13 $ |

Série 3 (65 %, mythique 55 × prix, V_cap 60 × prix) : 308 × P pour 1 % sur 100 000 ventes. La réserve s'effondre parce que V est borné (5 × P au plus) : il n'y a plus de jackpot à couvrir.
