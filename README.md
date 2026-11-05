# Esperanto — Vorto de la Tago

A monochrome TRMNL e-paper micro-learning plugin for Esperanto.

## Modes
- **Learn:** progressive vocabulary and short grammar notes.
- **Discover:** idioms, unusual words and cultural notes.
- **Mixed (default):** alternating Learn / Discover by calendar day.

User settings: `content_mode`, `translation_language` (en/de/es/fr), `difficulty` (beginner/intermediate/advanced).

## Sync or install
1. For the existing GitHub-connected private plugin, sync from the TRMNL editor. The plugin files live under `src/`.
2. For a manual import, make a flat ZIP of the contents of `src/` and use the private plugin **Import** feature.
3. Verify the polling URL and custom fields from `src/settings.yml`, then force a refresh.

The plugin polls hourly so it can pick up the daily payload after GitHub Actions publishes it.

All content ships from GitHub as static JSON. GitHub Actions updates `data/daily.json` at 00:15 UTC each day (and allows manual dispatch). TRMNL sees changed polling data and can regenerate its screen. No external paid API or private server is required. Content repeats after its current pool is exhausted; the day-of-year selection also repeats annually.

## Data design
`data/catalogue.json` contains `learn` and `discover` arrays. The generated `data/daily.json` also contains `day_number` and `generated_date`. Every item has a `level`, an Esperanto title, translated labels (en/de/es/fr), Esperanto example, translated example, and short grammar or cultural note. Keep the JSON well below TRMNL's 100 KB polling limit. The initial catalogue is intentionally small, **not** 365 completed lessons.

## Validation
Run `python3 scripts/generate_daily.py` to refresh daily data and `python3 scripts/validate.py` to check schema and languages. From the repository root, run `trmnlp lint` and `trmnlp serve`. Use the preview's device and view controls to inspect Full, Half Horizontal, Half Vertical and Quadrant on TRMNL OG and TRMNL X. To preview a different language, mode or level, set the corresponding value under `custom_fields` in `.trmnlp.yml`.

References: https://help.trmnl.com/en/articles/10542599-importing-and-exporting-private-plugins and https://help.trmnl.com/en/articles/10513740-custom-plugin-form-builder
