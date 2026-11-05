#!/usr/bin/env python3
"""Validate Esperanto TRMNL catalogue content and local plugin files."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data/catalogue.json").read_text(encoding="utf-8"))
languages = {"en", "de", "es", "fr"}
levels = {"beginner", "intermediate", "advanced"}
assert set(data) == {"learn", "discover"}
for mode, entries in data.items():
    assert entries, mode
    for entry in entries:
        assert entry["level"] in levels, entry
        for key in ("word", "example_eo"):
            assert isinstance(entry[key], str) and entry[key].strip()
        for key in ("translations", "examples", "notes"):
            assert set(entry[key]) == languages, (mode, entry["word"], key)
            assert all(isinstance(x, str) and x.strip() for x in entry[key].values())
    assert all(any(e["level"] == level for e in entries) for level in levels)
for name in ("settings.yml", "shared.liquid", "full.liquid",
             "half_horizontal.liquid", "half_vertical.liquid", "quadrant.liquid"):
    assert (ROOT / "src" / name).is_file(), name
daily = json.loads((ROOT / "data/daily.json").read_text(encoding="utf-8"))
assert daily["learn"] == data["learn"] and daily["discover"] == data["discover"]
assert 1 <= daily["day_number"] <= 366
assert len(daily["generated_date"]) == 10
assert len((ROOT / "data/daily.json").read_bytes()) < 100_000
print(f"OK: {sum(map(len, data.values()))} entries; 2 modes, 3 levels, 4 languages")
