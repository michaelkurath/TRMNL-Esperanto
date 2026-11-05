# Esperanto — Vorto de la Tago

A monochrome TRMNL e-paper micro-learning plugin for Esperanto.

## Modes
- **Learn:** progressive vocabulary and short grammar notes.
- **Discover:** idioms, unusual words and cultural notes.
- **Mixed (default):** alternating Learn / Discover by calendar day.

User settings: `content_mode`, `translation_language` (en/de/es/fr), `difficulty` (beginner/intermediate/advanced).

## Install in the existing private plugin
1. Use the TRMNL private plugin **Import** feature with a flat ZIP containing `settings.yml`, `shared.liquid`, `full.liquid`, `half_horizontal.liquid`, `half_vertical.liquid`, `quadrant.liquid`. (Or paste them into their corresponding editor tabs.)
2. Set strategy **Polling**, URL `https://raw.githubusercontent.com/michaelkurath/TRMNL-Esperanto/main/data/catalogue.json`, interval **1440 minutes** (daily).
3. Add the fields from `settings.yml` if pasting manually. Save and Force Refresh.
4. Test all four mashup views and both TRMNL OG and TRMNL X screens.

All content ships from GitHub as static JSON. Dates are selected in Liquid from the render's date; no background job, API key or private service is required. A yearly cycle will repeat because selection uses day-of-year; adding more entries expands the cycle.

## Data design
`data/catalogue.json` contains `learn` and `discover` arrays. Every item has a `level`, an Esperanto title, translated labels (en/de/es/fr), Esperanto example, translated example, and short grammar or cultural note. Keep the JSON well below TRMNL's 100 KB polling limit. The initial catalogue is intentionally small, **not** 365 completed lessons.

## Validation
Run `python3 scripts/validate.py` to check schema and languages. Use TRMNL preview or trmnlp for final display verification. This repository doesn't directly edit the TRMNL account; import or copy the files there.

References: https://help.trmnl.com/en/articles/10542599-importing-and-exporting-private-plugins and https://help.trmnl.com/en/articles/10513740-custom-plugin-form-builder
