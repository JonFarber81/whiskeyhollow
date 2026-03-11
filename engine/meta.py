"""Meta-progression — persists run achievements and unlocks across games."""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING

META_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "meta_save.json")

if TYPE_CHECKING:
    from engine.engine import Engine


def load_meta() -> dict:
    try:
        with open(META_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "runs_completed": 0, "best_cash": 0,
            "best_faction_rank": "", "total_kills": 0, "total_jobs": 0,
            "unlocks": {"already_connected": False, "well_armed": False, "nest_egg": False},
        }


def save_meta(meta: dict) -> None:
    os.makedirs(os.path.dirname(META_PATH), exist_ok=True)
    with open(META_PATH, "w") as f:
        json.dump(meta, f, indent=2)


def update_meta_on_run_end(engine: Engine, won: bool) -> dict:
    """Called when a run ends (win or loss). Updates and saves meta."""
    meta = load_meta()
    meta["runs_completed"] += 1

    if engine.cash > meta.get("best_cash", 0):
        meta["best_cash"] = engine.cash

    # Check kills for "Well-Armed" unlock
    kills = getattr(engine, "total_kills", 0)
    meta["total_kills"] = meta.get("total_kills", 0) + kills
    if kills >= 10:
        meta["unlocks"]["well_armed"] = True

    # Check cash for "Nest Egg" unlock
    if engine.cash >= 5000:
        meta["unlocks"]["nest_egg"] = True

    # Check faction rank for "Already Connected" unlock
    standing = getattr(engine.player, "faction_standing", None)
    if standing:
        from constants import REP_SOLDIER
        for key, rep in standing.rep.items():
            if rep >= REP_SOLDIER:
                meta["unlocks"]["already_connected"] = True
                from factions.faction_data import get_faction
                meta["best_faction_rank"] = get_faction(key).rank_title(rep)
                break

    meta["total_jobs"] = meta.get("total_jobs", 0) + getattr(engine, "jobs_completed", 0)

    save_meta(meta)
    return meta
