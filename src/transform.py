def run(data):
    trmnl = data.get("trmnl") or {}
    state = trmnl.get("state") or {}
    fields = (trmnl.get("plugin_settings") or {}).get("custom_fields_values") or {}
    pools = data.get("refresh_pools")
    if fields.get("lesson_frequency") != "every_refresh" or not pools:
        return {
            **{key: value for key, value in data.items() if key not in ("trmnl", "refresh_pools")},
            "trmnl_state": state,
        }

    mode = fields.get("content_mode") or "mixed"
    level = fields.get("difficulty") or "beginner"
    history = state.get("lesson_history") or {}
    selection = f"{mode}/{level}"
    previous = history.get(selection) or {}
    chosen_mode = mode
    if mode == "mixed":
        chosen_mode = "learn" if previous.get("mode") == "discover" else "discover"

    pool = pools[chosen_mode][level]
    previous_word = previous.get(chosen_mode)
    previous_index = next(
        (index for index, entry in enumerate(pool) if entry["word"] == previous_word),
        -1,
    )
    entry = pool[(previous_index + 1) % len(pool)]
    return {
        "refresh_lesson": {"mode": chosen_mode, "entry": entry},
        "trmnl_state": {
            **state,
            "lesson_history": {
                **history,
                selection: {**previous, "mode": chosen_mode, chosen_mode: entry["word"]},
            }
        },
    }
