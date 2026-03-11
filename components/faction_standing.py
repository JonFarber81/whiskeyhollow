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
        from entities.perks import has_perk
        current = self.rep.get(faction_key, 0)

        # Phase 16: Street Rep perk — halve rep loss
        entity = getattr(self, "entity", None)
        if entity and has_perk(entity, "street_rep"):
            amount = max(1, amount // 2)

        # Phase 16: Made Man perk — can't drop below 25 in any faction
        new_val = max(0, current - amount)
        if entity and has_perk(entity, "made_man"):
            new_val = max(25, new_val) if current >= 25 else new_val

        self.rep[faction_key] = new_val

    def get_rep(self, faction_key: str) -> int:
        return self.rep.get(faction_key, 0)

    def rank_title(self, faction_key: str) -> str:
        from factions.faction_data import get_faction
        return get_faction(faction_key).rank_title(self.get_rep(faction_key))

    def set_starting_affinity(self, faction_key: str, amount: int = 10) -> None:
        """Give player a head start in their class-preferred faction."""
        self.rep[faction_key] = max(self.rep.get(faction_key, 0), amount)

    # -----------------------------------------------------------------------
    # Serialization (Phase 14)
    # -----------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {"rep": dict(self.rep)}

    @classmethod
    def from_dict(cls, data: dict) -> "FactionStanding":
        obj = cls.__new__(cls)
        obj.rep = data.get("rep", {})
        obj.entity = None
        # Ensure all faction keys exist
        from factions.faction_data import FACTIONS
        for key in FACTIONS:
            if key not in obj.rep:
                obj.rep[key] = 0
        return obj
