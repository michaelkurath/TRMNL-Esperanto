#!/usr/bin/env python3
"""Validate Esperanto TRMNL catalogue content and local plugin files."""
import json
from datetime import date
from pathlib import Path

from generate_daily import LEVELS, build_feeds

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data/catalogue.json").read_text(encoding="utf-8"))
languages = {"en", "de", "es", "fr"}
assert set(data) == {"learn", "discover"}
for mode, entries in data.items():
    words = {entry["word"].strip().casefold() for entry in entries}
    assert len(words) == len(entries), (mode, "duplicate lesson")
    for entry in entries:
        assert entry["level"] in LEVELS, entry
        for key in ("word", "example_eo"):
            assert isinstance(entry[key], str) and entry[key].strip()
        for key in ("translations", "examples", "notes"):
            assert set(entry[key]) == languages, (mode, entry["word"], key)
            assert all(isinstance(x, str) and x.strip() for x in entry[key].values())
    for level in LEVELS:
        assert sum(e["level"] == level for e in entries) >= 15, (mode, level)
for name in ("settings.yml", "transform.py", "shared.liquid", "full.liquid",
             "half_horizontal.liquid", "half_vertical.liquid", "quadrant.liquid"):
    assert (ROOT / "src" / name).is_file(), name
feed_dir = ROOT / "data"
today_payload = json.loads((feed_dir / "today.json").read_text(encoding="utf-8"))
generated_date = date.fromisoformat(today_payload["generated_date"])
for name, expected in build_feeds(data, generated_date).items():
    path = feed_dir / name
    assert json.loads(path.read_text(encoding="utf-8")) == expected, name
    assert path.stat().st_size < 100_000, name
print(f"OK: {sum(map(len, data.values()))} entries; 3 modes, 3 levels, 4 languages")
