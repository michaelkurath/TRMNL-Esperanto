#!/usr/bin/env python3
"""Publish today's TRMNL lessons and refresh the legacy feed."""
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Preserve the original 2026 day numbers and keep counting across New Year.
ROTATION_EPOCH = dt.date(2026, 1, 1)
LEVELS = ("beginner", "intermediate", "advanced")
REFRESH_WINDOW_SIZE = 15
LEGACY_POOL_SIZES = {"beginner": 15, "intermediate": 2, "advanced": 2}


def build_feeds(catalogue, today):
    rotation_day = (today - ROTATION_EPOCH).days + 1
    single_index = rotation_day - 1
    mixed_index = single_index // 2
    mixed_mode = "learn" if rotation_day % 2 == 0 else "discover"
    pools = {
        mode: {
            level: [entry for entry in entries if entry["level"] == level]
            for level in LEVELS
        }
        for mode, entries in catalogue.items()
    }
    lessons = {
        mode: {level: pool[single_index % len(pool)] for level, pool in mode_pools.items()}
        for mode, mode_pools in pools.items()
    }
    lessons["mixed"] = {
        level: pool[mixed_index % len(pool)]
        for level, pool in pools[mixed_mode].items()
    }
    metadata = {"rotation_day": rotation_day, "generated_date": today.isoformat()}
    compact = {**metadata, "mixed_mode": mixed_mode, "lessons": lessons}

    # Expose all small pools and a moving window of larger pools.
    refresh = {
        **compact,
        "refresh_pools": {
            mode: {
                level: [
                    pool[(single_index + offset) % len(pool)]
                    for offset in range(min(len(pool), REFRESH_WINDOW_SIZE))
                ] if len(pool) > REFRESH_WINDOW_SIZE else pool
                for level, pool in mode_pools.items()
            }
            for mode, mode_pools in pools.items()
        },
    }

    # Older plugin installs still read daily.json. Keep its catalogue bounded
    # at the original pool sizes while advancing the same daily clock.
    legacy = {
        "day_number": today.timetuple().tm_yday,
        **metadata,
        **{
            mode: [
                entry
                for level, pool in mode_pools.items()
                for entry in pool[:LEGACY_POOL_SIZES[level]]
            ]
            for mode, mode_pools in pools.items()
        },
    }
    return {"today.json": compact, "refresh.json": refresh, "daily.json": legacy}


if __name__ == "__main__":
    catalogue = json.loads((ROOT / "data/catalogue.json").read_text(encoding="utf-8"))
    today = dt.datetime.now(dt.timezone.utc).date()
    for filename, payload in build_feeds(catalogue, today).items():
        out = ROOT / "data" / filename
        formatting = {"separators": (",", ":")} if filename != "daily.json" else {"indent": 2}
        out.write_text(json.dumps(payload, ensure_ascii=False, **formatting) + "\n", encoding="utf-8")
        print(f"Updated {out} for {today} ({out.stat().st_size} bytes)")
