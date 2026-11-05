# Esperanto — Vorto de la Tago

A monochrome TRMNL e-paper micro-learning plugin for Esperanto.

## Modes
- **Learn:** progressive vocabulary and short grammar notes.
- **Discover:** idioms, unusual words and cultural notes.
- **Mixed (default):** alternating Learn and Discover each time the lesson changes.

User settings: `content_mode`, `translation_language` (en/de/es/fr), `difficulty` (beginner/intermediate/advanced), and `lesson_frequency`.

**New lesson** defaults to **Daily**. Select **Every refresh** to advance on each successful TRMNL plugin refresh. The default polling interval is 60 minutes. Saved State tracks your place separately for each mode and difficulty, and the lessons cycle once you reach the end of a pool.

Each difficulty has 15 Learn lessons and 15 Discover entries. In Daily, Mixed takes 30 days to repeat. Each single-mode rotation takes 15 days.

## Sync or install
1. For the existing GitHub-connected private plugin, sync from the TRMNL editor. The plugin files live under `src/`.
2. For a manual import, make a flat ZIP of the contents of `src/` and use the private plugin **Import** feature.
3. Verify the polling URL and custom fields from `src/settings.yml`. In the markup editor, check that the Serverless tab contains the Python code from `src/transform.py`. Then force a refresh.

The plugin polls hourly so it can pick up the daily payload after GitHub Actions publishes it.

GitHub Actions publishes `data/today.json` at 00:15 UTC each day and supports manual dispatch. The feed contains today’s lesson for each mode and difficulty, with all four translations. The rotation continues across New Year.

## Icon

The monochrome Esperanto star is included in the shared title bar. [esperanto-icon.png](assets/esperanto-icon.png) is the matching 512 × 512 green icon for a listing that accepts a plugin icon upload.

## Data design
`data/catalogue.json` is the full Learn and Discover catalogue. Each entry includes its level, headword, example, and translations and notes in EN, DE, ES and FR. The generator uses the continuous UTC day counter to pick nine entries for `data/today.json`, one for each mode and difficulty combination. The number of entries in that feed stays fixed as the catalogue grows. With **Every refresh**, TRMNL polls `data/refresh.json` instead. That feed includes up to 15 entries per Learn or Discover pool for each difficulty. The Python Serverless transform selects one entry and saves its place for the next refresh.

Existing TRMNL imports can continue to poll `data/daily.json`. That feed advances each day and keeps the original pool sizes. Import the updated plugin from GitHub to switch to the smaller feed and receive future catalogue additions.

Grammar and historical references are available from [lernu!](https://lernu.net/en/gramatiko), the [Esperanto Museum of the Austrian National Library](https://www.onb.ac.at/en/museums/esperanto-museum/about-the-esperanto-museum/), the [Akademio de Esperanto](https://www.akademio-de-esperanto.org/fundamento/), the [UEA Libroservo](https://katalogo.uea.org/katalogo.php), the [Tekstaro de Esperanto](https://tekstaro.com/t?nomo=proverbaro-esperanta), and the [history of the Akademio de Esperanto](https://www.akademio-de-esperanto.org/akademio/index.php?title=Historio_de_la_Akademio).

## Validation
Run `python3 scripts/generate_daily.py` to refresh daily data and `python3 scripts/validate.py` to check schema and languages. From the repository root, run `trmnlp lint` and `trmnlp serve`. Use the preview's device and view controls to inspect Full, Half Horizontal, Half Vertical and Quadrant on TRMNL OG and TRMNL X. To preview a different language, mode or level, set the corresponding value under `custom_fields` in `.trmnlp.yml`.

References: https://help.trmnl.com/en/articles/10542599-importing-and-exporting-private-plugins and https://help.trmnl.com/en/articles/10513740-custom-plugin-form-builder
