# Simulateur économique : rapport

Établi le 11/11/2026. Phase 2.1 de `docs/plan.md`. Chiffres en NEAR, avec 1 NEAR ≈ 3,6 $ pour les conversions.
Les sorties complètes sont dans `resultats/` (une page par config, plus les grilles de sensibilité).

## En bref

- **Le jeu recommandé pour la série 1 est le jeu A** : 10 NEAR, β = 60 %, un mythique sur 5 000 boosters, d'une valeur
  d'environ 480 NEAR. Il faut une réserve de départ d'environ **1 200 NEAR** (4 200 $) pour un risque de 1 % sur 10 000 ventes.
- **L'approximation normale du document sous-estime le risque d'un facteur 3 à 5.** À la réserve qu'elle donne, le risque
  simulé est de 3 à 6 %, et non de 1 %. Il faut environ 30 % de réserve en plus.
- **La réserve dépend surtout de la taille du jackpot, pas de sa cote.** `R₀` est toujours au moins égal à `V_cap`, et
  `V_cap` doit couvrir le mythique.
- **La borne anti-arbitrage n'est pas la contrainte qui bloque.** Elle vaut 83 à 84 % pour les trois jeux. Ce qui limite β,
  c'est la marge de l'équipe et la réserve.
- **Avec seulement 13 jetons brûlables, les brûlables deviennent les cartes les plus courantes du jeu.** Une commune
  brûlable sort 57 fois plus souvent qu'une commune de collection.
- L'exemple de la partie 4.4 est retrouvé exactement : κ = 1, 6 NEAR d'adossement moyen et une borne de 82,9 %.

## Méthode

**Modèle.** Un booster a 5 emplacements. Chacun a sa table de raretés. Le 5e emplacement est plus favorable. Une carte
tirée dans la rareté `r` est brûlable avec la probabilité `b_r`. Sinon, c'est une carte de collection. Une carte brûlable
reçoit un adossement `v = min(κ·w_r·m, plafond_r)`, en NEAR dépensés à l'ouverture. Le multiplicateur `m` est tiré à part.
Les mythiques ont une valeur fixe, sans multiplicateur.

**κ.** On généralise la formule de la partie 4.3 à une part brûlable par rareté et à des emplacements différents :

```
κ = β·P / ( E[m] · Σ_emplacements Σ_r p_{s,r} · b_r · w_r )
```

Avec des plafonds par carte, κ est recalculé par bissection pour que l'adossement moyen reste égal à β·P.

**Coûts.** L'adossement est la somme de NEAR dépensée. Les jetons livrés valent `v·(1 − s_achat)`. On prend
`s_achat = 1 %`, dans la fourchette mesurée (0,2 à 1,7 %). Le burn coûte 0,2 % (appFees) plus 0,03 NEAR fixes par carte.

**Monte-Carlo.** Chaque emplacement tire une « issue » (rareté, brûlable ou non, niveau de multiplicateur) par inversion
de la fonction de répartition, avec numpy. On simule 2 millions de boosters par config. Les grilles de sensibilité en
utilisent 1 million par point.

**Borne β simulée.** On cherche par bissection le β où le gain moyen simulé de l'attaquant « j'achète, je brûle tout, je
revends le reste » vaut `P·(1 − ε)`. Les tirages sont les mêmes pour chaque β. Les plafonds et `V_cap` sont pris en compte.

**Ruine.** On simule 10 000 trajectoires de 10 000 ventes. À chaque vente, la réserve reçoit `(β + δ)·P` et paie
l'adossement du booster, plafonné à `V_cap`. On note la plus forte baisse `D` de chaque trajectoire. La réserve passe sous
`V_cap` si `R₀ − V_cap < D`. Une seule simulation donne ainsi toute la courbe du risque selon `R₀`.

## Vérification sur l'exemple 4.4

| Grandeur | Document | Formule du simulateur | Monte-Carlo (2 M) |
|---|---:|---:|---:|
| κ | 1 | 1,000 | |
| Adossement moyen par booster | 6,0 | 6,00 | 6,01 ± 0,01 |
| Écart-type par booster | 11,8 | 11,81 | 11,8 |
| Gain « brûle tout » | 6,36 | 6,36 | 6,37 |
| Borne β (ε = 15 %) | 82,9 % | 82,9 % | 83,3 % (82,7 % sans `V_cap`) |
| P(au moins un légendaire) | 1,0 % | 1,00 % | 1,00 % |
| Aucune carte brûlable | 3,8 % | 3,8 % | 3,8 % |
| Adossement ≥ 10 NEAR | environ 14 % | | **13,1 %** |
| R₀ (z = 3) | 564 | 564 | risque réel 3,2 % ; il faut **712** pour 1 % |

La borne simulée dépasse un peu la formule à cause de `V_cap` : le plafond rogne les plus gros tirages, au profit de la
maison. Sans `V_cap`, l'écart disparaît (test `test_monte_carlo_retrouve_l_exemple`).

## Les trois jeux proposés pour la série 1

Les trois jeux partagent le catalogue v2 provisoire : 520 communes, 150 rares, 80 épiques, 45 légendaires, 3 mythiques.
Les 13 brûlables sont répartis ainsi : 2 communes, 2 rares, 1 épique, 5 légendaires (WIF, PENGU, SPX, BOME, TURBO), et les
3 mythiques (DOGE, SHIB, PEPE). Ces effectifs sont des paramètres.

| | **A : 10 NEAR, équilibré** | **B : 10 NEAR, jackpot fréquent** | **C : 5 NEAR, entrée** |
|---|---:|---:|---:|
| Prix | 10 NEAR (36 $) | 10 NEAR (36 $) | 5 NEAR (18 $) |
| β / δ / reste | 60 % / 10 % / 30 % | 65 % / 10 % / 25 % | 60 % / 10 % / 30 % |
| Mythique | 1 sur 5 000 | 1 sur 2 000 | 1 sur 10 000 |
| Valeur d'un mythique | 477 NEAR (1 720 $) | 240 NEAR (860 $) | 276 NEAR (995 $) |
| Au moins un légendaire | 1 sur 8 (12,4 %) | 1 sur 13 (8,0 %) | 1 sur 10 (9,7 %) |
| Légendaire brûlable | 16 à 66 NEAR | 25 à 105 NEAR | 15 à 38 NEAR |
| Commune brûlable | 1,6 à 6,6 NEAR | 1,8 à 7,5 NEAR | 1,7 à 4,3 NEAR |
| Adossement moyen | 6,00 | 6,50 | 3,00 |
| Médiane de l'adossement | 2,7 | 3,0 | 1,7 |
| Écart-type | 11,6 | 12,9 | 6,1 |
| P(adossement ≥ prix) | 16,0 % | 18,4 % | 20,0 % |
| Booster sans carte brûlable | 28,9 % | 30,1 % | 49,0 % |
| Cartes brûlables par booster | 1,10 | 1,07 | 0,66 |
| Gain « brûle tout » / prix | 62 % | 66 % | 62 % |
| Borne β, formule / simulée | 83,7 % / 83,8 % | 84,4 % / 84,5 % | 83,5 % / 83,7 % |
| `V_cap` | 600 | 300 | 300 |
| R₀ normale (z = 3), risque réel | 903, 5,5 % | 670, 3,0 % | 470, 4,0 % |
| **R₀ pour 1 % de risque** | **1 170 NEAR (4 200 $)** | **790 NEAR (2 840 $)** | **600 NEAR (2 170 $)** |
| R₀ pour 0,1 % de risque | 1 550 | 1 000 | 790 |

Toutes les cartes brûlables valent au moins 1,4 NEAR (5 $), soit 20 fois le coût fixe du retrait. Les trois jeux
respectent ε ≥ 15 % avec une large marge.

**Jeu A.** C'est le plan 0.4 (10 NEAR, β = 60 %). Un mythique vaut 48 fois le prix. Un légendaire sort assez souvent pour
rythmer les ouvertures. Compromis : la plus grosse réserve des trois.

**Jeu B.** Un mythique tous les 2 000 boosters, mais plus petit : 24 fois le prix. Les légendaires sont plus rares et plus
gros. β monte à 65 % pour compenser. Compromis : la réserve baisse d'un tiers, mais la marge aussi (25 % au lieu de 30 %),
et le mythique n'écrase plus autant un gros légendaire (240 contre 105 NEAR).

**Jeu C.** Le prix d'entrée est divisé par deux. Pour garder chaque carte brûlable au-dessus de 5 $, il faut moins de cartes
brûlables : un booster sur deux n'en contient aucune. Compromis : produit moins généreux en jetons, et 1,5 NEAR seulement
par booster pour l'exploitation et la marge.

## Sensibilité (jeu A, détail dans `resultats/serie1-A-10near-sensibilite.md`)

**β.** La borne est franchie vers 84 %. Monter β augmente aussi la réserve nécessaire, car δ reste fixe et l'écart-type
grandit avec κ. Sous 55 %, les communes brûlables passent sous 5 $.

| β | 40 % | 50 % | 60 % | 70 % | 80 % | 85 % |
|---|---:|---:|---:|---:|---:|---:|
| P(adossement ≥ prix) | 10,0 % | 12,2 % | 16,0 % | 21,9 % | 24,4 % | 25,5 % |
| Gain « brûle tout » / prix | 43 % | 53 % | 62 % | 72 % | 81 % | **86 %** |
| R₀ pour 1 % | 922 | 1 043 | 1 173 | 1 314 | 1 437 | 1 477 |

**Poids des légendaires.** Plus de poids sur les légendaires rend les autres cartes plus petites, car κ est recalculé. À
×1,5, les communes brûlables tombent à 1,39 NEAR, juste sous les 5 $. À ×3, la moitié de l'adossement moyen vient des
légendaires, et P(adossement ≥ prix) tombe de 16 à 10 %.

| Facteur | ×0,5 | ×1 | ×1,5 | ×2 | ×3 |
|---|---:|---:|---:|---:|---:|
| Part de l'adossement venant des légendaires | 17 % | 29 % | 39 % | 45 % | 56 % |
| P(adossement ≥ prix) | 20,6 % | 16,0 % | 13,8 % | 11,7 % | 9,8 % |
| R₀ pour 1 % | 1 208 | 1 173 | 1 184 | 1 220 | 1 329 |

**Cote du mythique** (poids et `V_cap` fixes). Rendre le mythique plus rare baisse peu la réserve : elle reste ancrée sur
`V_cap`. Le rendre plus fréquent coûte cher, car plusieurs mythiques peuvent tomber tôt.

| Cote | 1 sur 1 000 | 1 sur 2 000 | 1 sur 5 000 | 1 sur 10 000 | 1 sur 20 000 |
|---|---:|---:|---:|---:|---:|
| Part de l'adossement moyen | 7,5 % | 3,9 % | 1,6 % | 0,8 % | 0,4 % |
| R₀ normale | 1 227 | 1 035 | 903 | 857 | 833 |
| Risque réel à R₀ normale | 5,2 % | 6,1 % | 5,3 % | 4,1 % | 3,1 % |
| R₀ pour 1 % | 1 606 | 1 396 | 1 173 | 1 090 | 1 007 |

Les jeux B et C donnent les mêmes tendances (`resultats/serie1-B-10near-sensibilite.md`, `serie1-C-5near-sensibilite.md`).

## Ce qui surprend

1. **L'approximation normale ne suffit pas.** Elle suppose des pertes gaussiennes. Ici, un seul mythique coûte 20 à 45
   écarts-types d'un booster. À z = 3, le risque réel est de 3 à 6 %, contre 1,1 % pour un mouvement brownien.
2. **Le risque se joue au début.** Pour le jeu A à R₀ = 1 170, le risque est de 0,66 % sur les 500 premières ventes, et de
   0,99 % sur 10 000. Ensuite, l'apport δ fait grossir la réserve plus vite que les jackpots ne la vident.
3. **Les brûlables sont trop fréquentes.** Avec 2 communes brûlables, chacune sort dans 29 % des boosters (jeu A). La seule
   épique brûlable sort dans 15 % des boosters. Les cartes qui portent la valeur deviennent les plus banales du jeu.
4. **La valeur minimale de 5 $ fixe le nombre de brûlables.** À budget fixe, plus de brûlables veut dire des brûlables
   plus petites. À 5 NEAR, la contrainte est dure : un booster sur deux n'a aucune brûlable.
5. **La plupart des boosters valent moins que leur prix.** 80 à 84 % des boosters ont un adossement sous le prix. La
   médiane vaut 27 à 34 % du prix. Il faut l'afficher, comme prévu en 6.2.

## Recommandations

1. **Prendre le jeu A pour la série 1.** Il suit le plan 0.4 et garde 30 % du prix pour l'exploitation et la marge.
2. **Dimensionner la réserve par simulation, pas par la formule normale.** Pour A : 1 200 NEAR pour 1 %, 1 550 NEAR pour
   0,1 %. Si c'est trop pour l'équipe, prendre B (800 NEAR) ou baisser la valeur du mythique.
3. **Fixer `V_cap` juste au-dessus du mythique**, puis la réserve. Le mythique est le premier levier sur la réserve.
4. **Garder β entre 60 et 65 %.** Monter plus haut coûte en marge et en réserve, et rapproche d'une promesse de gain.
5. **Élargir les brûlables avant la série 1**, ou leur donner plusieurs visuels. Sinon, DOGE, SHIB et PEPE mis à part, les
   cartes brûlables seront les plus courantes. Les 58 « candidats » d'Intents sont la première piste.
6. **Pour la démo du hackathon**, sans vente au public, la réserve est théorique. Une série de démo peut garder les mêmes
   tables avec un `V_cap` et un mythique réduits.

## Limites

- La valeur adossée est en NEAR. Le prix des jetons après l'achat n'est pas modélisé. Une carte peut valoir zéro plus tard.
- Les coûts sont des moyennes fixes. Le surcoût réel croît avec la taille de l'achat : à 1 000 $, les jetons NEAR natifs
  perdent 4 à 11 %. Les plafonds par carte (25 à 280 NEAR) en tiennent compte grossièrement. Au-delà de 1 000 $ (pour les
  mythiques), la profondeur n'a pas été mesurée.
- Le prix de revente des cartes de collection est une hypothèse (0,03 à 2 NEAR). Il ne joue presque pas sur la borne.
- Les tirages sont indépendants. Il n'y a pas de tirage maximal par carte dans une série, ni de garantie de pitié.
- La ruine suppose des ventes régulières et des achats toujours réussis. Elle ignore les frais d'exploitation payés sur la
  réserve et une baisse du NEAR.
- Les effectifs du catalogue v2 et la répartition des brûlables par rareté sont provisoires.
- Le seul attaquant testé brûle tout. Les attaques de front-running et de pompage de pool (partie 4.5) ne sont pas simulées.

## Série 2 (catalogue v2)

Établie le 11/11/2026. Configs `configs/serie2-*.yaml` (générées par `python -m memaster_sim.serie2 configs`),
résultats dans `resultats/serie2/` (une page par point, `grille.md`, et la sensibilité au facteur entre paliers).
2 millions de boosters par point, 20 000 trajectoires de 10 000 ventes pour la réserve.

### Ce qui change par rapport à la série 1

**Catalogue.** Le chargeur `memaster_sim/catalogue.py` lit `docs/data/catalogue-v2.json`, garde les 1 649 cartes de la
section « catalogue » et ignore les 101 « à décider » : 1 160 communes, 230 rares, 235 épiques, 21 légendaires, 3 mythiques.

**Quelles cartes sont brûlables.** Le burn n'est pas décidé. On le simule ainsi :
- seules les cartes dont le jeton s'achète encore sont candidates : on écarte les jetons morts et les arnaques avérées,
  soit 1 069 communes sur 1 160, 84 épiques sur 235 et 2 légendaires sur 21. Les mythiques scellés sont toujours candidats ;
- la pyramide est remplie par le haut : les 3 mythiques, les 19 légendaires vivants, puis les épiques jusqu'à 50 %, les
  rares jusqu'à 25 %, les communes en dernier (10 % au plus) ;
- dans chaque rareté, les cartes sont tirées avec une graine fixe (2026). Le tirage est emboîté : les 60 brûlables
  contiennent les 30, etc. Les identifiants sont recopiés dans chaque config (`catalogue.brulables`).

Pourquoi par le haut : (1) le plafond d'adossement par carte suit la liquidité, et elle est en haut (25 NEAR pour une
commune, 280 pour un légendaire) ; (2) les communes sont surtout des mèmes morts, qu'on ne peut pas acheter ; (3) une carte
du haut garde une grosse valeur unitaire, loin du minimum de 5 $ ; (4) le plafond de 50 % garde des épiques de collection.

**Pas de faveur.** `part_brulable = brûlables / effectif` : une brûlable sort aussi souvent que n'importe quelle carte de
sa rareté. C'est la correction du défaut de la série 1, où une commune brûlable sortait 57 fois plus qu'une autre.

**Probabilités de rareté : celles de la série 1 ne tiennent plus.** Avec 1 160 communes et seulement 21 légendaires, les
tables de la série 1 (jeu A) donnent, sur 10 000 boosters, 27,8 exemplaires de chaque commune, 53,0 de chaque rare,
17,9 de chaque épique et 61,8 de chaque légendaire. Un légendaire précis sortirait plus souvent qu'une commune précise,
et une rare plus souvent qu'une commune. La pyramide est inversée. Nouvelle règle : **un exemplaire sort 2 fois moins
souvent à chaque palier** (commune → rare → épique → légendaire). Le mythique garde sa cote de la série 1 (1 sur 5 000
à 10 NEAR, 1 sur 10 000 à 5 NEAR), dans le 5e emplacement. L'emplacement 5 reçoit 50 % des rares, 60 % des épiques et
80 % des légendaires.

| Table | Commune | Rare | Épique | Légendaire | Mythique |
|---|---:|---:|---:|---:|---:|
| Emplacements 1 à 4 | 92,37 % | 5,38 % | 2,20 % | 0,049 % | 0 |
| Emplacement 5 | 64,49 % | 21,51 % | 13,19 % | 0,786 % | 0,02 % (0,01 % à 5 NEAR) |
| Cartes par booster | 4,34 | 0,430 | 0,220 | 0,0098 (1 sur 102) | 1 sur 5 000 |
| Exemplaires de chaque carte sur 10 000 boosters | 37,4 | 18,7 | 9,4 | 4,7 | 0,67 |

Le facteur 2 est un choix. Il pèse beaucoup sur le résultat (voir plus bas).

**Hypothèses reprises de la série 1.** À 10 NEAR, celles du jeu A ; à 5 NEAR, celles du jeu C :

| | 10 NEAR (jeu A) | 5 NEAR (jeu C) |
|---|---:|---:|
| β / δ / reste | 60 % / 10 % / 30 % | 60 % / 10 % / 30 % |
| ε | 15 % | 15 % |
| Poids commune / rare / épique / légendaire | 1 / 1,4 / 3,5 / 10 | 1 / 1,2 / 3 / 9 |
| Multiplicateur (probas 50 / 35 / 15 %) | 0,6 / 1 / 2,5 | 0,8 / 1 / 2 |
| Plafonds par carte (NEAR) | 25 / 30 / 100 / 280 | 25 / 30 / 100 / 280 |
| Mythique : valeur fixe, cote | 477 NEAR, 1 sur 5 000 | 276 NEAR, 1 sur 10 000 |
| `V_cap` | 600 | 300 |
| Coûts | s_achat 1 %, burn 0,2 % + 0,03 NEAR | idem |

Le mythique est désormais à valeur fixe (poids très grand, valeur = plafond), pour garder sa valeur de la série 1 quand
κ change. κ est recalibré à chaque point pour que l'adossement moyen reste égal à β·P.

### Résultats

Marge = prix − adossement moyen simulé − δ·P (ce qui reste pour l'exploitation et l'équipe). Réserves = R₀ simulé pour
que la réserve reste au-dessus de `V_cap` pendant 10 000 ventes avec 95 % ou 99 % de chances.

| Brûlables (myth / lég / ép / rare) | Prix | Marge / booster | P(≥ 1 brûlable) | Plus petite brûlable | σ booster | **R₀ 5 %** | **R₀ 1 %** | R₀ normale (risque réel) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 30 (3 / 19 / 8 / 0) | 5 | 1,49 | 1,6 % | 79,4 | 25,8 | 2 349 | 3 457 | 3 286 (1,3 %) |
| 60 (3 / 19 / 38 / 0) | 5 | 1,49 | 4,4 % | 36,4 | 17,5 | 1 305 | 1 859 | 1 682 (1,7 %) |
| 90 (3 / 19 / 68 / 0) | 5 | 1,50 | 7,1 % | 25,1 | 13,5 | 907 | 1 241 | 1 122 (1,9 %) |
| 120 (3 / 19 / 98 / 0) | 5 | 1,50 | 9,8 % | 19,1 | 11,3 | 733 | 980 | 877 (1,9 %) |
| **150 (3 / 19 / 117 / 11)** | **5** | **1,50** | **13,4 %** | 6,3 | 9,9 | **638** | **833** | 740 (2,1 %) |
| 30 (3 / 19 / 8 / 0) | 10 | 5,65 (β 33 %, non réalisable) | 1,7 % | 99,1 | 28,5 | 1 981 | 2 724 | 2 422 (2,0 %) |
| 60 (3 / 19 / 38 / 0) | 10 | 2,99 | 4,4 % | 94,6 | 32,3 | 2 283 | 3 221 | 2 935 (1,6 %) |
| 90 (3 / 19 / 68 / 0) | 10 | 2,99 | 7,1 % | 47,5 | 26,1 | 1 719 | 2 335 | 2 131 (1,9 %) |
| 120 (3 / 19 / 98 / 0) | 10 | 2,99 | 9,8 % | 32,8 | 23,1 | 1 485 | 2 007 | 1 795 (1,9 %) |
| 150 (3 / 19 / 117 / 11) | 10 | 2,99 | 13,4 % | 9,8 | 21,6 | 1 391 | 1 864 | 1 646 (2,1 %) |

Tableau complet (β effectif, brûlables par booster, P(adossement ≥ prix)) dans `resultats/serie2/grille.md`.

**Lecture.**
1. **La marge ne dépend pas du nombre de brûlables.** Elle est fixée par β et δ : 3,0 NEAR à 10 NEAR, 1,5 NEAR à 5 NEAR.
   La grille joue sur la réserve et sur ce que reçoit l'acheteur.
2. **30 brûlables à 10 NEAR, c'est impossible.** Avec les plafonds de liquidité, l'adossement moyen ne dépasse pas
   3,33 NEAR par booster, soit β = 33 %. La marge monte, mais la promesse de 60 % n'est pas tenue. À 5 NEAR, ça passe
   de justesse, avec des légendaires presque tous à leur plafond.
3. **Plus de brûlables, moins de réserve.** Le budget β·P est réparti sur plus de cartes, donc chaque jackpot est plus
   petit. De 60 à 150 brûlables, la réserve à 1 % baisse de 42 % à 10 NEAR et de 55 % à 5 NEAR.
4. **Même à 150, 87 % des boosters n'ont aucune brûlable.** P(≥ 1 brûlable) ne dépend pas du prix. Elle suit le nombre
   de brûlables et la cote des épiques. C'est le prix d'une vraie rareté sur un catalogue de mèmes morts : la valeur se
   concentre sur 1 booster sur 7 ou 8, qui reçoit alors en moyenne 4,5 fois son prix.
5. **L'approximation normale sous-estime moins qu'en série 1.** À la réserve qu'elle donne, le risque simulé est de 1,3
   à 2,1 % (et non 1 %). Il faut 5 à 13 % de réserve en plus, contre environ 30 % en série 1. La variance vient ici de
   beaucoup de jackpots moyens (épiques, légendaires), plus proches d'une loi normale qu'un seul mythique.
6. **La borne anti-arbitrage reste loin** : 84,8 à 85,2 % pour les points réalisables à 150 brûlables, pour β = 60 %.

**Sensibilité au facteur entre paliers** (150 brûlables, `resultats/serie2/sensibilite-facteur-*.md`).

| Facteur | Légendaires par booster | P(≥ 1 brûlable) | R₀ 1 % à 5 NEAR | R₀ 1 % à 10 NEAR |
|---:|---:|---:|---:|---:|
| 1,5 | 0,022 (1 sur 46) | 21,3 % | 671 | 1 462 |
| 2 | 0,0098 (1 sur 102) | 13,4 % | 833 | 1 864 |
| 3 | 0,0031 (1 sur 320) | 6,8 % | 1 300 | 2 349 |

**Au-delà de la grille.** La règle permet au plus 205 brûlables. À 200 (3 / 19 / 117 / 57 rares / 4 communes), P(≥ 1
brûlable) monte à 22 % et la réserve à 1 % tombe à environ 710 NEAR à 5 NEAR et 1 550 NEAR à 10 NEAR (sondage à 10 000
trajectoires, non inclus dans `resultats/`). La tendance n'est pas saturée.

### Recommandation

1. **150 brûlables** : les 3 mythiques, 19 légendaires, 117 épiques et 11 rares. C'est le point de la grille qui demande
   le moins de réserve aux deux prix et qui donne le plus de boosters avec des jetons (13,4 %). Toutes les brûlables
   valent au moins 6,3 NEAR (23 $), loin du minimum de 1,4 NEAR.
2. **5 NEAR le booster.** Marge 1,50 NEAR par booster (15 000 NEAR sur 10 000 ventes). Réserve : **640 NEAR (2 300 $) pour
   5 %**, **850 NEAR (3 000 $) pour 1 %**. C'est moins que le jeu A de la série 1 (1 170 NEAR). Comme 87 % des boosters
   ne contiennent que des cartes de collection, un booster vide coûte 18 $ au lieu de 36 $.
3. **Si l'équipe veut la marge du plan 0.4, 10 NEAR** : 2,99 NEAR par booster, mais 1 400 NEAR (5 000 $) pour 5 % et
   **1 860 NEAR (6 700 $) pour 1 %**. Rapportée à la réserve, la marge est la même aux deux prix (0,16 à 0,18 % de la
   réserve par vente). Le choix se fait sur le capital disponible et sur le prix d'un booster vide.
4. **Ne pas descendre sous 90 brûlables.** À 60, la réserve est 1,7 à 2,2 fois plus grosse et 96 % des boosters sont vides. À 30 et 10 NEAR, β = 60 %
   est inatteignable.
5. **Prochaine décision : le facteur entre paliers.** Passer de 2 à 1,5 fait passer P(≥ 1 brûlable) de 13 à 21 % et baisse la
   réserve de 20 %, au prix de légendaires deux fois moins rares. Pour aller au-delà de 150, il faut rendre brûlables des
   rares vivantes.

### Limites propres à la série 2

- Le choix des brûlables est tiré au hasard parmi les jetons vivants. Le vrai choix suivra la liquidité de chaque jeton.
  « Vivant » est lu dans le champ `etat` du catalogue, pas vérifié.
- Les plafonds par carte et les poids sont ceux de la série 1. Ils n'ont pas été mesurés sur les jetons du catalogue v2.
- Les réserves sont estimées sur 20 000 trajectoires. Le quantile à 1 % repose sur 200 trajectoires : compter ± 5 %.
