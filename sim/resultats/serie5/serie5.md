# Série 5 : pitié sans garantie, mythique 1 pour 10⁶, gold 99/1, V moyenne 75 %

Paramètres : `configs/serie5.yaml`. Coûts de la série 4, sauf 971 octets par pack (stockage payé par l'acheteur) ; gaz 48 Tgas (valeur de la série 4, pas de meilleure mesure). Tables publiées : `tables-valeur.json` (gold identique à la série 4 : oui).

## Valeur moyenne V

| Pack normal | Pack rush | Gold pack | **Flux réel** (g_pop exact, rush 5 %) | Flux g_pop simulé | Flux g_∞ |
|---:|---:|---:|---:|---:|---:|
| 75,00 % | 75,00 % | 200,00 % | **75,0026 %** | 75,0026 % | 75,0050 % |

Rush : même paliers et même σ que le normal, calibré sur la même moyenne : les deux tables sont identiques. Le gold pack (200 %) pèse moins de 0,01 point sur le flux.

## Fréquence des gold packs (pitié sans garantie)

p(n) = min(p_max, p0 + k·n), p0 = 1/50 000, p_max = 1/25 000, k = 2.0e-08 : plafond atteint au pack 1001 du cycle (1 000 + 1 par l'arrondi flottant, sans effet), atteint par 97,0 % des cycles. Au-delà, chance constante : queue géométrique exacte, E[T] = Σ_{j<m} S(j) + S(m) / p_max. Aucun gold garanti. Un pack rush compte comme un pack sans gold (n + 1).

| Mesure | Part des packs en gold | **1 gold pour** |
|---|---:|---:|
| g_∞ (joueur qui ne s'arrête pas), exact | 3.961e-05 | **25 248 packs** |
| g_∞, Monte-Carlo : 1 000 000 cycles | 3.964e-05 | 25 227 (± 25) |
| g_∞, Monte-Carlo : flux stationnaire de 300 000 000 packs-joueurs (11 803 golds) | 3.934e-05 | 25 417 (± 0,9 %) |
| g_pop (population de la série 4, 100 000 joueurs, 1 066 305 packs), exact | 2.073e-05 | **48 230 packs** |
| g_pop, une simulation de cette population (17 golds) | 1.594e-05 | 62 724 |

Avec cette population (médiane 4 packs par joueur), 99,98 % des joueurs ne voient aucun gold pack. g_pop exact : espérance des golds par joueur par l'équation de renouvellement (sans tirage) ; la simulation compte une poignée de golds.

## Fréquence des mythiques

Mythique à 2.50e-07 par emplacement (poids 5 sur 2·10⁷ du contrat), emplacements 1 à 4 ; le 5e (tiré parmi les brûlables) ne peut pas être mythique. Gold pack : 5e emplacement mythique 1 %, plus les planchers rare/épique (table standard restreinte).

| Flux | Mythiques par pack | **1 mythique pour** |
|---|---:|---:|
| pack normal | 1.000e-06 | 1 000 000 packs |
| pack gold | 1.003e-02 | 100 packs |
| pack rush | 1.000e-06 | 1 000 000 packs |
| **packs classiques** (normal + rush 5 %) | 1.000e-06 | **1 000 000 packs** |
| flux avec gold (g_pop) | 1.208e-06 | **827 919 packs** |
| flux avec gold (g_∞) | 1.397e-06 | 715 799 packs |

Avec g_∞, 28 % des mythiques sortent d'un gold pack.

## Marge par pack

NEAR à 2,5 $. Gaz 48 Tgas = 0,012 $, payé par l'équipe (cas prudent) ; stockage ~1 Ko payé par l'acheteur en plus du prix (dépôt) ; achat groupé des jetons 0,5 % à 1 % de la valeur (0,75 % au centre). Couverture = flux réel (pitié g_pop et rush).

| Variante | Prix | Couverture | **Marge** | Fourchette (frais 1 % → 0,5 %) | Marge si l'acheteur paie le gaz | Après réserve δ = 5 % | Débours de l'acheteur | Packs pour 10 NEAR de coûts fixes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| (a) | 0,20 $ | 75,0 % | **0,037 $ (18 %)** | 0,036 $ à 0,037 $ | 0,049 $ (24 %) | 0,027 $ | 0,224 $ | 679 |
| (a) | 0,50 $ | 75,0 % | **0,110 $ (22 %)** | 0,109 $ à 0,111 $ | 0,122 $ (24 %) | 0,085 $ | 0,524 $ | 227 |

Rappel série 3 (couverture 65 %) : 0,057 $ (29 %) à 0,20 $, 0,161 $ (32 %) à 0,50 $.

## Borne anti-arbitrage

Gain moyen de « j'achète, je brûle tout, je revends le reste », en part du prix (c = 0,961). Borne 85 %. Sans garantie, le gold pack n'est jamais choisissable ; le cycle de pitié est celui d'un joueur qui ouvre jusqu'au gold (g_∞).

| Pack normal | Pack rush | Cycle de pitié | Gold pack seul (non choisissable) | Borne |
|---:|---:|---:|---:|---:|
| 73,3 % | 73,3 % | 73,3 % | 197 % | 85 % |

## Tables de valeur V

V en multiples du prix du pack. Paliers : normal et rush de 20 à 100 % par pas de 5 %, puis de 110 à 200 % par pas de 10 % (27 paliers) ; gold de 100 à 500 % (18 paliers). Forme lognormale discrétisée (σ = 0,6 pour normal et rush, 0,4 pour le gold), poids entiers sur 1 000 000. (a) : la cible est la moyenne ; (b) : la cible est la médiane.

| Variante | Table | Min | Max | q10 | Médiane | q90 | **Moyenne** | Écart-type | Sous 50 % | Au-dessus de 100 % |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| (a) | normale | 20 % | 200 % | 30 % | 65 % | 140 % | **75,0 %** | 44 % | 31,0 % | 20,5 % |
| (a) | gold | 100 % | 500 % | 110 % | 180 % | 300 % | **200,0 %** | 80 % | 0,0 % | 92,0 % |
| (a) | rush | 20 % | 200 % | 30 % | 65 % | 140 % | **75,0 %** | 44 % | 31,0 % | 20,5 % |
| (a) | **flux réel** (pitié + rush) | 20 % | 500 % | 30 % | 65 % | 140 % | **75,0 %** | 44 % | 31,0 % | 20,5 % |

Médiane d'une table discrète : plus petit palier où la fonction de répartition atteint 50 %.
