"""Faction standing component — tracks player rep with all factions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class FactionStanding:
    """Attached to the player actor to track rep with each faction."""
    rep: Dict[str, int] = field(default_factory=dict)
    entity: Optional[object] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        from factions.faction_data import FACTIONS
        for key in FACTIONS:
            if key not in self.rep:
                self.rep[key] = 0

    def gain_rep(self, faction_key: str, amount: int, engine: Optional[object] = None) -> None:
        from factions.faction_data import get_faction
        from ui import color as Color
        old = self.rep.get(faction_key, 0)
        new = min(100, old + amount)
        self.rep[faction_key] = new

        if engine:
            faction = get_faction(faction_key)
            old_title = faction.rank_title(old)
            new_title = faction.rank_title(new)
            engine.message_log.add_message(
                f"Rep +{amount} with {faction.name}.", fg=Color.MSG_REP,
            )
            if old_title != new_title:
                engine.message_log.add_message(
                    f"You are now a {new_title} in the {faction.name}!",
                    fg=Color.GOLD,
                )

    def lose_rep(self, faction_key: str, amount: int) -> None:
        self.rep[faction_key] = max(0, self.rep.get(faction_key, 0) - amount)

    def get_rep(self, faction_key: str) -> int:
        return self.rep.get(faction_key, 0)

    def rank_title(self, faction_key: str) -> str:
        from factions.faction_data import get_faction
        return get_faction(faction_key).rank_title(self.get_rep(faction_key))

    def set_starting_affinity(self, faction_key: str, amount: int = 10) -> None:
        """Give player a head start in their class-preferred faction."""
        self.rep[faction_key] = max(self.rep.get(faction_key, 0), amount)
