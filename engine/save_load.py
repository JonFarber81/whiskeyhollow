"""Save/load system — JSON-based persistence (Phase 14)."""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from engine.engine import Engine

SAVE_DIR = "saves"
SAVE_SLOTS = 3


def _slot_path(slot: int) -> str:
    os.makedirs(SAVE_DIR, exist_ok=True)
    return os.path.join(SAVE_DIR, f"slot_{slot}.json")


def save_game(engine: Engine, slot: int = 0) -> None:
    """Serialize engine state to a JSON save file."""
    path = _slot_path(slot)
    data = engine.to_dict()
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    engine.message_log.add_message(
        f"Game saved to slot {slot + 1}.", fg=(100, 200, 100)
    )


def load_game(slot: int = 0) -> Optional["Engine"]:
    """Load engine state from a JSON save file. Returns None if not found."""
    from engine.engine import Engine
    path = _slot_path(slot)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        data = json.load(f)
    return Engine.from_dict(data)


def list_saves() -> list[dict]:
    """Return metadata for each save slot (or empty dict if no save)."""
    slots = []
    for i in range(SAVE_SLOTS):
        path = _slot_path(i)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                slots.append({
                    "slot": i,
                    "exists": True,
                    "name": data.get("player", {}).get("name", "Unknown"),
                    "char_class": data.get("player", {}).get("char_class", "?"),
                    "turn": data.get("turn_count", 0),
                    "cash": data.get("cash", 0),
                    "district": data.get("district", "?"),
                    "jobs": data.get("jobs_completed", 0),
                })
            except Exception:
                slots.append({"slot": i, "exists": False})
        else:
            slots.append({"slot": i, "exists": False})
    return slots


def delete_save(slot: int = 0) -> None:
    """Remove a save file (called on death/win to prevent reload)."""
    path = _slot_path(slot)
    if os.path.exists(path):
        os.remove(path)
