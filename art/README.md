# Visuels des cartes Memaster

Générateur hors ligne des visuels de cartes, en SVG, avec leurs métadonnées NEP-177. Ce n'est pas le front.
Python 3, bibliothèque standard uniquement.

## Commandes

Depuis `art/` :

```sh
python3 -m memaster_art --catalogue ../docs/catalogue-final.md --out out/ [--limit N] [--planche]
python3 -m unittest discover -s tests                     # tests
python3 -m memaster_art.exemples --catalogue ../docs/catalogue-final.md --dest exemples --png
python3 outils/rendre_png.py out/0001-doge.svg --dest /tmp/png   # relecture en PNG
```

Catalogue v2 (JSON, détecté par l'extension) :

```sh
python3 -m memaster_art --catalogue ../docs/data/catalogue-v2.json --out out/v2/ [--inclure-a-decider]
python3 -m memaster_art.exemples --catalogue ../docs/data/catalogue-v2.json --dest exemples/v2 --png
```

Depuis la racine du dépôt : `PYTHONPATH=art python3 -m memaster_art --catalogue docs/catalogue-final.md --out art/out/`.

Options :

- `--planche` : planches HTML de contact, 50 cartes par page (`planche-01.html`, …), à ouvrir dans un navigateur.
- `--base-url https://…/` : préfixe des champs `media` et `reference`. Vide par défaut : chemins relatifs.
- `--mythiques 1,2,3` : passe ces N° en mythique (règle v2). On peut aussi donner un ticker, mais il vise toutes
  les cartes qui le portent (8 cartes pour `DOGE,SHIB,PEPE` dans le catalogue actuel). Un catalogue v2 dont la
  colonne Rareté vaut déjà « mythique » n'a pas besoin de cette option.

`out/` est ignoré par git (`art/.gitignore`). `exemples/` est versionné : 11 cartes et le dos scellé, en SVG,
PNG et JSON, plus une planche.

## Catalogue v2 (`docs/data/catalogue-v2.json`)

- Seule la section `catalogue` est lue (1 649 cartes) ; `--inclure-a-decider` ajoute les 101 « à décider ».
- L'identifiant de carte est l'`id` stable (slug) : nom des fichiers (`bonk-bonk.svg`), graine de l'art,
  `identifiant` des métadonnées. Le N° (« 12 », « M1 », « AD3 ») n'est qu'affiché.
- Champs lus : liste blanche `CHAMPS_LUS` de `catalogue_v2.py`. Le champ `secret` est jeté au décodage JSON et
  n'est jamais lu ni écrit ; `drapeau` n'est pas lu (rien sur la carte).
- Mythiques : toujours scellées. Pas de recto : `mythique-m1.json` pointe vers `dos-mythique.svg`, sans
  `reference`, avec seulement l'`id` et le N° dans `extra`. Un test vérifie l'absence de DOGE/SHIB/PEPE.
- État : « mort… » donne le style cimetière, « en déclin… », « actif », sinon « à vérifier ».
- Chaîne : `chaine_normalisee`. Année du pic : première année du `pic`, sinon du `lancement`.
- Burn : « à définir » n'est pas affiché ; `burn: null` dans le `.ref.json`, avec l'`adresse` si connue.
- `exemples/v2/` : 2 cartes par rareté (une vivante, une morte si possible) et le dos, plus `planche-v2.png`.

## Sorties par carte

| Fichier | Contenu |
|---|---|
| `0001-doge.svg` | Visuel, 500 × 700 (5:7), 4 à 15 Ko |
| `0001-doge.json` | Métadonnées NEP-177 : `title`, `description`, `media`, `media_hash`, `extra`, `reference`, `reference_hash` |
| `0001-doge.ref.json` | JSON hors chaîne pointé par `reference` |
| `dos-mythique.svg` / `.json` | Dos scellé « ? », commun à toutes les mythiques (s'il y en a) |

`media_hash` et `reference_hash` sont le sha256 du fichier, en base64. `extra` est une chaîne JSON, comme le veut
NEP-177 : rareté, état, chaîne, année du pic, identifiant, N°, mention de non-affiliation.

## Lecture du catalogue

Le CLI lit le premier tableau de la section `## Cartes`, par nom de colonne : N°, Nom, Ticker, Chaîne,
Période de gloire (ou Lancement), Pic de capitalisation, État (ou État actuel), Rareté (ou Rareté proposée), Adresse.

- Rareté : `*` retiré, accents tolérés, `mythique` accepté. Valeur inconnue : commune.
- État : `actif (dérivé)` devient `actif`, `en déclin (dérivé)` devient `en déclin`. Tout ce qui n'est ni actif,
  ni en déclin, ni mort devient `à vérifier` (pastille « état ? »). Rien n'est inventé.
- Chaîne : première chaîne citée, sans parenthèses. « à vérifier » s'affiche « chaîne ? ».
- Année du pic : première année trouvée dans la période de gloire, sinon dans le pic. Sinon « pic inconnu ».
- Identifiant : l'adresse si la cellule en contient une entre backticks, sinon `memaster:<N°>`.

## Règles de design

- **Fonction pure.** Une carte dépend de (identifiant, ticker, nom, chaîne, rareté, état, année du pic, N°).
  Même entrée, même octets. Le hasard vient d'un sha256 et d'un générateur splitmix64 maison, pour ne pas
  dépendre de la version de Python.
- **Art.** La graine (identifiant, ticker, chaîne) choisit une palette (analogue, complémentaire, triade,
  fendue), un motif parmi six (pavage, orbites, ondes, éclats, constellation, soleil) et un emblème géométrique
  central (étoile, polygones emboîtés, anneau cranté). Rareté et état ne changent que le cadre et les effets :
  une carte garde son art si sa rareté change.
- **Cadres.**

| Rareté | Cadre et effets |
|---|---|
| commune | Pierre grise mouchetée, fenêtre en arche de pierre tombale, herbe au pied, épitaphe « CIMETIÈRE DES MÈMES », couleurs passées |
| rare | Acier bleu, losanges aux coins |
| épique | Violet, équerres et perles aux coins, filet épais |
| légendaire | Or, voile holographique arc-en-ciel et reflet diagonal sur l'art, étincelles sur la bordure |
| mythique | Recto : obsidienne, or et cramoisi, aura dorée et rayons derrière l'emblème, holo, « MYTHIQUE · SECRÈTE ». Dos : rosace guillochée, sceau rouge « ? », « SCELLÉE » |

- **États.** `actif` : couleurs pleines. `en déclin` : couleurs désaturées et une fissure. `mort` : gris de pierre
  légèrement chaud, quatre fissures, « ICI REPOSE » au-dessus du ticker et « † année » gravé dans l'art
  (« † » seul si l'année est inconnue).
- **Dos des mythiques.** Il ne dépend d'aucune carte : les trois mythiques ont le même dos, octet pour octet, et
  ses métadonnées ne contiennent ni ticker ni nom.
- **Miniature.** Ticker en gras de 64 px (réduit, puis compressé avec `textLength` s'il est long), rareté en
  capitales espacées, pastille d'état colorée. Tout se lit dans une vignette de 150 px de large.
- **Poids.** Pas de filtre de flou, chemins regroupés, nombres à une décimale : 4 à 15 Ko par carte sur les
  786 cartes du catalogue (le test exige moins de 30 Ko).

## Garde-fous juridiques

D'après `docs/marche-droits-economie.md` (section 2.3) et `docs/visuels-droits.md`. Ce n'est pas un avis juridique.

- **Art 100 % abstrait.** Que des formes géométriques générées. Aucun logo, personnage, animal, grenouille,
  chien, visage, ni redessin « à la manière de ». Aucun motif ne s'inspire du visuel d'un projet.
- **Aucune ressource externe.** Pas d'`<image>`, pas de police embarquée, pas de `@font-face`, pas de lien
  externe. Les polices sont les familles génériques `sans-serif`, `serif` et `monospace` : aucune police d'un
  projet n'est imitée.
- **Le ticker n'est qu'une donnée.** Ticker, nom, chaîne et identifiant sont écrits en texte simple, sans
  stylisation propre à un projet. Le risque de marque n'est pas nul pour autant (section 2.3, point 3).
- **Mention de non-affiliation.** « Sans lien ni partenariat avec les projets cités » en pied de chaque carte,
  et la phrase complète dans le `<desc>` du SVG, dans la `description` et dans `extra` des métadonnées.
- **Retrait possible.** Un visuel se régénère ou se remplace carte par carte, sans toucher aux jetons.
- **Tests.** `tests/test_rendu.py` refuse les balises `image`, `style`, `script`, `foreignObject`, les liens
  externes, les polices non génériques et une liste de mots interdits (logo, grenouille, chien, shiba, pepe,
  kabosu, visage, officiel, …) hors des champs de données. Un test vérifie que ce garde-fou détecte bien un mot
  interdit.
- **À faire avant toute mise en ligne.** Faire valider l'approche par un juriste. Les 233 cartes de la liste A de
  `visuels-droits.md` (dont DOGE, SHIB, PEPE) gardent leur risque de nom et de ticker, même avec un art abstrait.

## Rendu PNG

`outils/rendre_png.py` utilise `rsvg-convert` ou `cairosvg` s'ils sont installés. Sinon, sur macOS, il passe par
`qlmanage` (vignette carrée) puis `sips` (recadrage en 500 × 700). Les PNG ne servent qu'à la relecture : le
média de référence est le SVG.
