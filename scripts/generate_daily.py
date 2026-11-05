#!/usr/bin/env python3
"""Publish a daily changing TRMNL payload from the canonical catalogue."""
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalogue = json.loads((ROOT / "data/catalogue.json").read_text(encoding="utf-8"))
today = dt.datetime.now(dt.timezone.utc).date()
payload = {"day_number": int(today.strftime("%j")), "generated_date": today.isoformat(), **catalogue}
out = ROOT / "data/daily.json"
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Updated {out} for {today}")
