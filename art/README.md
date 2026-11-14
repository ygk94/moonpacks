# Card art generator

Offline generator for the Moonpacks card visuals: one SVG per card plus its NEP-177 metadata. Python 3, standard
library only. The front calls it at build time (`front/scripts/prepare-assets.mjs`); it is not part of the site.

## Commands

From `art/`:

```sh
# full catalogue (JSON, detected by its extension), English card text as used by the front
python3 -m memaster_art --catalogue ../docs/data/catalogue-v2.json --out out/ --langue en [--limit N] [--planche]

# demo catalogue
python3 -m memaster_art --catalogue ../docs/data/catalogue-demo.json --out out/demo/ --planche

# regenerate the committed examples in exemples/v2 (with PNG previews)
python3 -m memaster_art.exemples --catalogue ../docs/data/catalogue-v2.json --dest exemples/v2 --png

# tests
python3 -m unittest discover -s tests

# PNG preview of one SVG
python3 outils/rendre_png.py out/bonk-bonk.svg --dest /tmp/png
```

From the repository root: `PYTHONPATH=art python3 -m memaster_art --catalogue docs/data/catalogue-v2.json --out art/out/`.

Options:

- `--langue en`: visible SVG text in English (rarity labels, state, peak year, disclaimer). The default is `fr`.
  Ticker and coin name never change. The JSON metadata text stays in the generator's original language (French).
- `--planche`: HTML contact sheets, 50 cards per page (`planche-01.html`, ...).
- `--base-url https://.../`: prefix for the `media` and `reference` fields. Empty by default (relative paths).
- `--inclure-a-decider`: also render the catalogue's "to be decided" section (by default only `catalogue` is read).
- `--mythiques 12,40`: force these card numbers (or tickers) to mythic. Not needed when the catalogue already marks them.
- `--limit N`: only the first N cards.

The CLI also reads the older markdown catalogue format (first table of a `## Cartes` section, columns matched by
name); `tests/data/catalogue-v1.md` is such a catalogue and is used by the tests.

`out/` is ignored by git. `exemples/v2/` is committed: two cards per rarity (one alive, one dead when possible),
the sealed mythic back and a contact sheet (`planche-v2.svg`, `planche-v2.png`).

## Output per card

| File | Content |
|---|---|
| `<id>.svg` | The visual, 500 x 700 (5:7), 4 to 15 KB |
| `<id>.json` | NEP-177 metadata: `title`, `description`, `media`, `media_hash`, `extra`, `reference`, `reference_hash` |
| `<id>.ref.json` | Off-chain JSON pointed to by `reference` |
| `dos-mythique.svg` / `.json` | The sealed "?" back shared by every mythic card |
| `mythique-m1.json`, ... | Mythic metadata, byte-identical to `dos-mythique.json` |

`<id>` is the stable slug from the catalogue (`bonk-bonk`); it names the files, seeds the art and is the
metadata identifier. `media_hash` and `reference_hash` are the base64 sha256 of the file. `extra` is a JSON string,
as NEP-177 requires: rarity, state, chain, peak year, identifier, number, non-affiliation notice.

## Mythic cards

Mythics are always anonymous, before and after reveal: no front, title "?", description "?", and the common
sealed back. Their metadata contains no id, number, ticker or reference. The real mythic list lives in a file
that is never committed (`docs/data/secrets/`, ignored by git) and that this generator never reads. When that file
is present locally, a test checks that no real name, ticker or address leaks into the generated output.

## Design rules

- **Pure function.** A card depends only on (identifier, ticker, name, chain, rarity, state, peak year, number).
  Same input, same bytes. Randomness comes from sha256 and a small splitmix64 generator, so it does not depend
  on the Python version.
- **Art.** The seed (identifier, ticker, chain) picks a palette (analogous, complementary, triad, split), one of
  six patterns (tiling, orbits, waves, shards, constellation, sun) and a central geometric emblem. Rarity and state
  only change the frame and effects, so a card keeps its art if its rarity changes.
- **Frames.**

| Rarity | Frame and effects |
|---|---|
| common | Speckled grey stone, tombstone-arch window, grass at the foot, faded colours |
| rare | Blue steel, diamonds in the corners |
| epic | Purple, corner brackets and beads, thick rule |
| legendary | Gold, rainbow holographic veil and diagonal sheen, sparkles on the border |
| mythic | Sealed back: guilloche rosette, red "?" seal |

- **States.** `active`: full colour. `declining`: desaturated with one crack. `dead`: warm stone grey, four
  cracks, "here lies" above the ticker and a dagger with the year engraved in the art.
- **Thumbnail.** Bold 64 px ticker (shrunk or compressed with `textLength` when long), spaced rarity label,
  coloured state badge. Everything reads at 150 px wide.
- **Weight.** No blur filters, grouped paths, one-decimal numbers: 4 to 15 KB per card (tests require < 30 KB).

## Legal safeguards

This is not legal advice.

- **Fully abstract art.** Only generated geometric shapes: no logos, characters, animals, faces, and no redrawing
  "in the style of" a project's visuals.
- **No external resources.** No `<image>`, no embedded fonts, no `@font-face`, no external links. Fonts are the
  generic `sans-serif`, `serif` and `monospace` families.
- **The ticker is plain data.** Ticker, name, chain and identifier are written as plain text, with no
  project-specific styling.
- **Non-affiliation notice** in the footer of every card, in the SVG `<desc>`, in `description` and in `extra`.
- **Replaceable.** Any visual can be regenerated or replaced card by card without touching the tokens.
- **Tests.** `tests/test_rendu.py` rejects `image`, `style`, `script` and `foreignObject` elements, external
  links, non-generic fonts and a list of forbidden words outside data fields, and checks that this guard does
  catch a forbidden word.

## PNG rendering

`outils/rendre_png.py` uses `rsvg-convert` or `cairosvg` when installed, otherwise on macOS `qlmanage` then `sips`
(crop to 500 x 700). PNGs are only for review; the reference media is the SVG.
