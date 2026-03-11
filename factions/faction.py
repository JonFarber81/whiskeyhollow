"""Faction class — a criminal or political organization in KC."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class RepLevel:
    min_rep: int
    title: str
    perk: str = ""    # Description of perk unlocked at this rank


@dataclass
class Faction:
    key: str
    name: str
    description: str
    color: Tuple[int, int, int]
    home_district: str
    enemy_factions: List[str] = field(default_factory=list)
    rep_levels: List[RepLevel] = field(default_factory=list)
    job_pool: List[str] = field(default_factory=list)

    def rank_title(self, rep: int) -> str:
        """Return the rank title for the given rep value."""
        title = "Nobody"
        for level in self.rep_levels:
            if rep >= level.min_rep:
                title = level.title
        return title

    def rank_perk(self, rep: int) -> str:
        perk = ""
        for level in self.rep_levels:
            if rep >= level.min_rep and level.perk:
                perk = level.perk
        return perk
