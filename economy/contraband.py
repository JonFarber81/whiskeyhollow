"""Contraband types — the goods that drive the bootlegging economy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ContrabandType:
    key: str
    name: str
    base_value: int          # Base cash per unit
    heat_modifier: float     # Multiplier on heat gain when caught carrying
    weight: int              # Units of carrying capacity per case
    description: str


CONTRABAND_TYPES: Dict[str, ContrabandType] = {
    "whiskey": ContrabandType(
        key="whiskey",
        name="Whiskey",
        base_value=50,
        heat_modifier=1.5,
        weight=2,
        description="Top-shelf hooch. High value, high heat.",
    ),
    "beer": ContrabandType(
        key="beer",
        name="Beer",
        base_value=15,
        heat_modifier=0.8,
        weight=3,
        description="Giggle water in bulk. Low margin, low heat.",
    ),
    "gin": ContrabandType(
        key="gin",
        name="Gin",
        base_value=35,
        heat_modifier=1.0,
        weight=2,
        description="Quick sale, moderate heat.",
    ),
    "medicinal_alcohol": ContrabandType(
        key="medicinal_alcohol",
        name="Medicinal Alcohol",
        base_value=20,
        heat_modifier=0.4,
        weight=1,
        description="Technically legal. Low heat, low margin.",
    ),
}


def get_contraband(key: str) -> ContrabandType:
    return CONTRABAND_TYPES[key]
