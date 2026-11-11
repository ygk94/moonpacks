# Séries de démo « entrée » et « standard » (12/11/2026)

Branche `feat/series-demo`. **Testnet seulement, rien n'est déployé** : les deux séries attendent la nouvelle version du
contrat. Les paramètres sont générés, les tables construites et vérifiées hors ligne, et les visuels prêts pour IPFS
(CID calculé, rien n'est envoyé).

## Composition

Les deux séries prennent le catalogue de démo complet (`docs/data/catalogue-demo.json`) : **1 527 cartes visibles et
3 engagements de mythiques**. Elles ont les mêmes cartes, les mêmes mécaniques et les mêmes brûlables. Seuls le nom et
le prix changent.

| Rareté | Cartes | Brûlables possibles (catalogue) | Reliées à Intents | Écartées | Brûlables de la série |
|---|---:|---:|---:|---:|---:|
| mythique | 3 | 0 | – | – | 0 |
| légendaire | 21 | 18 | 5 | 13 | 5 |
| épique | 228 | 84 | 1 | 83 | 1 |
| rare | 224 | 89 | 0 | 89 | 0 |
| commune | 1 054 | 27 | 0 | 27 | **3 (appoint)** |
| **Total** | **1 530** | **218** | **6** | **212** | **9** |

- **Mécaniques** : celles de `contract/scripts/serie-exemple.json` (gold pack à planchers, pitié en ppb, rareté
  pilotée par les burns, gold rush, résurrection des épiques et légendaires mortes, ici 82 cartes). Plafond de 50 par
  légendaire ; mythiques de poids 1 et de plafond 10.
- **Tables de valeur** : `sim/resultats/serie5/tables-valeur.json`, 27 paliers recopiés dans `mechanics.value`.
  Moyenne de 75 % du prix en normal et en rush, de 200 % en gold, avec les multiplicateurs commune 1, rare 2, épique 3
  et légendaire 6.
- **Mythiques** : non adossées (le factice `mythique-m1` de l'exemple n'est pas repris). Le visuel est le « ? » commun
  (`mythique.svg`). Les sels sont **ceux de `contract/scripts/secrets/serie-v2.json`** (`build_series.py --sels`) :
  aucun sel neuf n'est tiré. Les engagements `sha256(card_id ‖ sel)` sont donc ceux de la série d'`app2`. Le
  `content_hash` change, puisque le contenu change (media, adossement). Les deux séries de démo ont les mêmes engagements.

## Brûlables reliées à de vrais actifs

Script : `contract/scripts/intents_brulables.py`. Correspondance : `docs/data/intents-brulables-demo.json`, avec la
raison de chaque écart. Relevés : `docs/data/intents-tokens-2026-11-12.json` (1Click `/v0/tokens`, 230 actifs, 11/11
23:05 UTC) et `docs/data/intents-devis-demo-2026-11-12.json` (devis `dry: true`, wNEAR → actif, INTENTS → INTENTS, à
0,04, 0,40, 1 et 4 $, aucun fonds engagé).

La règle tient en trois points :

- Le rapprochement se fait **uniquement par adresse de contrat** : l'`adresse` du catalogue doit égaler le
  `contractAddress` de 1Click. Les adresses EVM sont comparées en minuscules, les autres à l'identique, car Solana
  distingue la casse.
- La chaîne doit concorder. Une adresse `….near` vaut chaîne NEAR. Avec une chaîne « à vérifier », une adresse EVM doit
  en plus avoir le même id CoinGecko des deux côtés.
- Il faut un prix 1Click non nul, et les quatre devis doivent réussir.

| Carte | Rareté | Chaîne | `asset_id` | Décimales | Perte 0,04 / 0,40 / 1 / 4 $ (%) |
|---|---|---|---|---:|---|
| dogwifhat (WIF) | légendaire | sol | `nep141:sol-b9c68f94ec8fd160137af8cdfe5e61cd68e2afba.omft.near` | 6 | 1,22 / 1,21 / 1,21 / 1,21 |
| Pudgy Penguins (PENGU) | légendaire | sol | `nep141:sol-0xaad74c68eecfc9f8c5bdcea614f6167048c795ef.omdep.near` | 6 | 0,31 / 0,30 / 0,30 / 0,33 |
| SPX6900 (SPX) | légendaire | eth | `nep141:eth-0xe0f63a424a4439cbe457d80e4f4b51ad25b2c56c.omft.near` | 8 | 0,49 / 0,52 / 0,52 / 0,54 |
| Book of Meme (BOME) | légendaire | sol | `nep141:sol-57d087fd8c460f612f8701f5499ad8b2eec5ab68.omft.near` | 6 | 0,65 / 0,62 / 0,62 / 0,62 |
| Turbo (TURBO) | légendaire | eth | `nep141:eth-0xa35923162c49cf95e6bf26623385eb431ad920d3.omft.near` | 18 | 1,21 / 1,21 / 1,20 / 1,17 |
| Cash Cat (CASHCAT) | épique | hood | `nep141:hood-0x020bfc650a365f8bb26819deaabf3e21291018b4.omft.near` | 18 | 0,25 / 0,22 / 0,16 / 0,13 |
| NearKat (appoint) | commune | near | `nep141:kat.token0.near` | 18 | 0,55 / 0,56 / 0,56 / 0,60 |
| Black Dragon (appoint) | commune | near | `nep141:blackdragon.tkn.near` | 24 | 0,49 / 0,49 / 0,49 / 0,51 |
| Jambo (appoint) | commune | near | `nep141:jambo-1679.meme-cooking.near` | 18 | 0,33 / 0,34 / 0,34 / 0,35 |

Aucun devis n'a refusé de petit montant : 0,04 $ passe partout. Les adresses de contrat complètes sont dans le JSON.

**Écartées (212), qui redeviennent des cartes de collection pour la démo :**

| Raison | Légendaire | Épique | Rare | Commune |
|---|---:|---:|---:|---:|
| Pas d'adresse de contrat dans le catalogue, et aucun actif 1Click de même id CoinGecko ni de même ticker | 4 | 76 | 89 | 26 |
| Adresse absente de la liste 1Click : Bonk, Floki, Fartcoin, Peanut, Popcat, Goat, MEW, Dogelon ; Degen, Baby Doge, Toshi, PEOPLE, Moo Deng, LADYS ; Kishu | 8 | 6 | 0 | 1 |
| Listé, mais « No liquidity available » à tous les montants : Brett, Mog | 1 | 1 | 0 | 0 |
| Homonyme par ticker seul, non retenu : World is Flat (WIF ≠ dogwifhat) | 0 | 0 | 0 | 1 |

Compléter les adresses du catalogue ne changerait rien aujourd'hui. Aucun des 195 sans adresse n'a d'homonyme Intents par
id CoinGecko, et un seul en a un par ticker.

**Communes d'appoint (3).** Sans commune ni rare brûlable, la brûlable garantie du dernier emplacement remonte toujours
à l'épique Cash Cat, à cause de la retombée vers le haut de `fallback_order`. Une simulation hors ligne de 5 000 packs
(`verifier/` : `core.draw_pack_mech` puis `pack_value`) donne alors **99,9 % d'épiques au dernier emplacement**, et
99,75 % de la valeur pour Cash Cat : c'est le défaut actuel d'`app2`, transposé. On ajoute donc les trois communes du
catalogue dont l'adresse NEAR est cotée sur Intents : NearKat, Black Dragon et Jambo. Le catalogue les dit « mort »,
donc non brûlables, mais leurs devis passent. Sur 20 000 packs normaux, le dernier emplacement est alors à 98,1 %
commune, 1,7 % épique et 0,2 % légendaire. Chaque commune reçoit environ 33 % de la valeur, Cash Cat 1,7 % et chaque
légendaire 0,07 %. En gold pack, l'emplacement brûlable (plancher rare) reste à 97 % Cash Cat. Pour retirer l'appoint,
il suffit de `series_demo.py --sans-appoint`.

`amount` des brûlables : c'est la quantité indicative du jeton (dans sa plus petite unité) qui vaut le prix du pack au
cours 1Click. Le contrat ne la lit pas pour les exemplaires tirés : la part de valeur du pack, en yoctoNEAR, la remplace
(`docs/mecaniques-spec.md`, section 9).

## Tous les memecoins d'Intents : combien de brûlables au maximum ? (12/11)

`contract/scripts/intents_memes.py` liste les memecoins de 1Click `/v0/tokens`, quel que soit le catalogue. Résultat
dans `docs/data/intents-memes-candidats.json`, devis dans `docs/data/intents-devis-memes-2026-11-12.json`. Chaque
actif a un devis `dry` à 0,04 $ (aucun fonds engagé) et sa présence dans `catalogue-v2.json`, par adresse ou, pour une
autre chaîne de la même pièce, par id CoinGecko. Un memecoin est un id de la catégorie meme de CoinGecko, ou un des
jetons signalés dans `intents-couverture.md` (ABG, GNEAR, NOEAR, LOUD, STJACK). PONS et COCA ne sont pas des
memecoins. Les cartes scellées sont exclues, puisqu'une mythique n'est jamais brûlable. Les séries ne changent pas.

25 actifs, soit 20 pièces. Une pièce présente sur plusieurs chaînes ne fait qu'une carte. Une seule pièce est absente
du catalogue v2 : STJACK, commune proposée (pic inconnu, prix nul).

| Rareté retenue | Pièces | Brûlables (devis à 0,04 $ réussi) | Dont au catalogue (hors « à décider ») | Brûlables |
|---|---:|---:|---:|---|
| légendaire | 8 | 6 | 5 | WIF, PENGU, SPX, BOME, TURBO ; TRUMP (« à décider ») |
| épique | 2 | 1 | 1 | CASHCAT |
| rare | 0 | 0 | 0 | aucune |
| commune | 10 | 4 | 4 | NearKat, Black Dragon, Jambo, SHITZU |
| **Total** | **20** | **11** | **10** | |

Sans devis : Brett, Mog, Melania (« à décider »), PURGE, LOUD, STJACK (« No liquidity available »), ainsi que NEARKAT
et wNEARKAT sur Solana (la version NEAR suffit). ABG, GNEAR et NOEAR ont un prix nul.

**Plafond aujourd'hui : 11 brûlables, ou 10 sans les « à décider », et aucune rare.** Intents n'a aucun memecoin
coté à 10-100 M$ de pic. Par rapport aux séries de démo, une seule commune de plus est possible : SHITZU, présente au
catalogue v2 mais absente du catalogue de démo. Pour des rares, il faudrait des actifs hors Intents (autre route
d'achat) ou un surclassement manuel.

## Prix

Cours : **3,62 $/NEAR** (CoinGecko `/simple/price`, 11/11/2026 23:05 UTC). 1Click donnait 3,60 $ à 23:02 UTC. Le
prix est arrondi au 1/10 000 de NEAR.

| Série | Slug | Prix visé | Prix en NEAR | `price` (yocto) |
|---|---|---:|---:|---|
| Memaster Entry | `serie-demo-entree` | 0,20 $ | **0,0552 NEAR** | `55200000000000000000000` |
| Memaster Standard | `serie-demo-standard` | 0,50 $ | **0,1381 NEAR** | `138100000000000000000000` |

## Tables et hash

| Série | `table_hash` | Taille | Appels | Dépôts de chargement |
|---|---|---:|---:|---:|
| entrée | `2064056b4a45953713038136f50f5c2b88f934256c233e5b9c78d9de5a313a40` | 341 393 o | 9 (1 + 7 lots + open) | 3,521 NEAR |
| standard | `382c5a38a80cd25a7605752e35037adb947fcea8b59dbbf553316e83eaf4310f` | 341 398 o | 9 | 3,521 NEAR |

Les tables publiques, les hash et les manifestes sont dans `docs/data/series-demo/<slug>/`, sans aucun nom de mythique.
Le hash ne dépend pas de `--series-id`, qui ne figure que dans les arguments `append_series_cards` et `open_series`.

Vérification hors ligne (`verifier/`) :

- `table --file … --expected-hash …` : VÉRIFIÉ pour les deux séries (octets `serde_json` exacts, sha256 recalculé).
- `mythic --table … --card-id … --sel … --content … --index i` à partir des secrets locaux : VÉRIFIÉ pour les 3
  mythiques de chaque série.
- Non-régression : `build_series.py serie-exemple.json --tables-valeur …serie5…` redonne le hash d'`app2`,
  `0b55b388…13d2bb`.
- Tests : `python3 -m unittest discover -s contract/scripts/tests` (27), `verifier/` (66), `art/` (30).

## Visuels et IPFS

```sh
(cd art && python3 -m memaster_art --catalogue ../docs/data/catalogue-demo.json --out out/demo-en/ --langue en)
cd contract
python3 -I scripts/ipfs_media.py prepare --art ../art/out/demo-en --dest scripts/out/ipfs-demo-en   # 1 528 SVG, 14,2 Mo
python3 -I scripts/ipfs_media.py cid --dir scripts/out/ipfs-demo-en                                # npx ipfs-car@3.1.0 pack
```

**CID : `bafybeifejdd5hvm44qa6qv5s3m2avywhdrydhn2rwypccttz52eu5viuia`**, retrouvé à l'identique après une
régénération complète des SVG. Le dossier contient `<card_id>.svg` pour chaque carte visible et `mythique.svg`, le dos
« ? » commun aux trois mythiques. Aucun fichier ne porte un vrai id, et `prepare` le vérifie s'il trouve le fichier
secret. Les séries visent `ipfs://<CID>/{id}.svg` et `ipfs://<CID>/mythique.svg`. `art/out/` et `contract/scripts/out/`
restent hors de git.

L'envoi n'est **pas fait**, faute de jeton. Il passe par le CAR, pour que le fournisseur garde le CID calculé ici, et le
CID renvoyé est comparé au CID local :

```sh
PINATA_JWT=… python3 -I scripts/ipfs_media.py upload --car scripts/out/ipfs-demo-en.car --provider pinata
W3S_TOKEN=…  python3 -I scripts/ipfs_media.py upload --car scripts/out/ipfs-demo-en.car --provider w3s   # ancienne API, à vérifier
python3 -I scripts/ipfs_media.py upload --car scripts/out/ipfs-demo-en.car --dry-run                     # n'envoie rien
```

## Déploiement (après la nouvelle version du contrat)

1. Régénérer les SVG, le dossier et le CID (ci-dessus). Si le CID change, relancer `series_demo.py --media-base
   ipfs://<CID>` (avec le même `--near-usd` et la même `--cours-source`, ou un cours du jour) puis reconstruire.
2. Envoyer le CAR (`upload`) et vérifier qu'une passerelle sert `…/<CID>/mythique.svg`.
3. Pour chaque série, prendre `N = get_series_count` sur le contrat, puis :
   ```sh
   cd contract
   python3 -I scripts/build_series.py scripts/serie-demo-entree.json --catalogue ../docs/data/catalogue-demo.json \
       --sels scripts/secrets/serie-v2.json --series-id N
   ```
   Envoyer ensuite les appels de `scripts/out/<slug>/manifest.json["calls"]` dans l'ordre, chacun avec son dépôt
   `deposits[…]` et 300 Tgas, comme à l'étape 5 de `scripts/deploy_testnet.sh` (qui ne gère que la série 0), puis
   `open_series`. Le hash doit rester celui du tableau.
4. Contrôler : `python3 -m memaster_verifier table --rpc testnet --contract <compte> --series N --expected-hash <hash>`.
5. Front : `VITE_CONTRACT_ID`. La boutique affiche toutes les séries ouvertes.

Gaz à surveiller : avec les URL IPFS, chaque lot de 200 cartes pèse environ 10 Ko de plus qu'avec `ipfs://TODO/…`.
Ce poids n'a pas été mesuré en sandbox.

## À trancher

- **L'appoint** : garder les trois communes NEAR « mortes » mais cotées (c'est le choix fait ici), ou accepter une
  brûlable garantie presque toujours épique. Autre option : relever la liquidité d'autres communes et rares.
- **Gold pack** : l'emplacement brûlable (plancher rare) tombe à 97 % sur Cash Cat, faute de rare brûlable.
- **Fournisseur IPFS** : Pinata (`PINATA_JWT`) ou web3.storage. L'ancienne API HTTP de web3.storage a peut-être fermé.
  Il faut aussi vérifier que l'envoi d'un CAR chez Pinata (`car=true`) garde bien le CID.
- **Cours** : 0,0552 et 0,1381 NEAR sont figés dans la table. À un autre cours au déploiement, il faut regénérer, ce qui
  change le hash.
- **Mêmes engagements** dans les deux séries et dans `app2` : une révélation dans une série révèle la même mythique
  partout. C'est acceptable pour une démo. Sinon, il faudrait des sels neufs, ce qui est exclu ici.
- **Retrait** : le redeemer reste factice sur testnet. Le coût fixe du retrait vers la chaîne d'origine (0,10 à 0,25 $,
  `intents-couverture.md`) dépasse la valeur d'une carte à ces prix : il faut retirer sur le solde Intents ou sur NEAR.
