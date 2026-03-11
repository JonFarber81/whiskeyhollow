"""Perk system — Phase 16.

24 perks across 4 categories: combat, economy, shadow, influence.
Perks are loaded from data/perks.json at import time.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.actor import Actor


@dataclass(frozen=True)
class Perk:
    key: str
    name: str
    description: str
    category: str               # "combat" | "economy" | "shadow" | "influence"
    class_affinity: List[str]   # CharacterClass.value strings ("Brawler", etc.)
    effect_type: str            # "stat_bonus" | "multiplier" | "unlock" | "passive"
    effect_target: str          # e.g. "combat_damage", "heat_on_kill", "max_hp"
    effect_value: float         # Numeric magnitude of the effect


def _load_perks() -> Dict[str, Perk]:
    path = os.path.join(os.path.dirname(__file__), "..", "data", "perks.json")
    try:
        with open(path, "r") as f:
            raw = json.load(f)
        return {
            key: Perk(
                key=key,
                name=v["name"],
                description=v["description"],
                category=v["category"],
                class_affinity=v.get("class_affinity", []),
                effect_type=v["effect_type"],
                effect_target=v["effect_target"],
                effect_value=float(v.get("effect_value", 0)),
            )
            for key, v in raw.items()
        }
    except FileNotFoundError:
        return {}


# Module-level perk registry — imported everywhere
PERKS: Dict[str, Perk] = _load_perks()


def has_perk(actor: "Actor", key: str) -> bool:
    """Return True if actor owns a perk with the given key."""
    return key in getattr(actor, "perks", [])


def get_perk_options(
    char_class_value: str,
    owned_perks: List[str],
    count: int = 3,
    category_filter: Optional[str] = None,
    rng=None,
) -> List[Perk]:
    """Draw N perks for a perk selection screen.

    Weighted toward class affinity, excludes already-owned perks.
    """
    import random
    _rng = rng or random.Random()

    available = [
        p for k, p in PERKS.items()
        if k not in owned_perks
        and (category_filter is None or p.category == category_filter)
    ]

    if not available:
        return []

    # Weight class-affinity perks 3x
    weighted: List[Perk] = []
    for p in available:
        weight = 3 if char_class_value in p.class_affinity else 1
        weighted.extend([p] * weight)

    _rng.shuffle(weighted)
    # Deduplicate while preserving order
    seen: set = set()
    result: List[Perk] = []
    for p in weighted:
        if p.key not in seen:
            seen.add(p.key)
            result.append(p)
        if len(result) == count:
            break

    return result
