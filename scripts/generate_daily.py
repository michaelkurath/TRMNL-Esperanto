#!/usr/bin/env python3
"""Publish a daily changing TRMNL payload from the canonical catalogue."""
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Preserve the original 2026 day numbers and keep counting across New Year.
ROTATION_EPOCH = dt.date(2026, 1, 1)

if __name__ == "__main__":
    catalogue = json.loads((ROOT / "data/catalogue.json").read_text(encoding="utf-8"))
    today = dt.datetime.now(dt.timezone.utc).date()
    payload = {
        "day_number": today.timetuple().tm_yday,
        "rotation_day": (today - ROTATION_EPOCH).days + 1,
        "generated_date": today.isoformat(),
        **catalogue,
    }
    out = ROOT / "data/daily.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {out} for {today}")
