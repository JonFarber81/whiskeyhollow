"""Actor entity — player, NPCs, enemies."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple

from entities.entity import Entity, RenderOrder

if TYPE_CHECKING:
    from components.fighter import Fighter
    from components.ai.base_ai import BaseAI
    from components.inventory import Inventory
    from world.game_map import GameMap


class Actor(Entity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "@",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<unnamed>",
        fighter: Optional[Fighter] = None,
        ai: Optional[BaseAI] = None,
        inventory: Optional[Inventory] = None,
        game_map: Optional[GameMap] = None,
        # Phase 13: named NPC support
        npc_key: Optional[str] = None,
        is_boss: bool = False,
    ) -> None:
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
            game_map=game_map,
        )
        self.fighter = fighter
        if self.fighter:
            self.fighter.entity = self

        self.ai = ai
        if self.ai:
            self.ai.entity = self

        self.inventory = inventory
        if self.inventory:
            self.inventory.entity = self

        # Phase 13: Named NPC / boss tracking
        self.npc_key: Optional[str] = npc_key
        self.is_boss: bool = is_boss

        # Phase 16: Perk list (player-only in practice)
        self.perks: List[str] = []

    @property
    def is_alive(self) -> bool:
        return bool(self.fighter and self.fighter.hp > 0)

    # -----------------------------------------------------------------------
    # Serialization (Phase 14)  — player-only, excludes AI/inventory
    # -----------------------------------------------------------------------

    def to_dict(self) -> dict:
        from entities.character_class import CharacterClass
        return {
            "x": self.x,
            "y": self.y,
            "name": self.name,
            "char": self.char,
            "color": list(self.color),
            "char_class": getattr(self, "char_class", CharacterClass.BRAWLER).value,
            "stats": getattr(self, "stats", None).to_dict() if getattr(self, "stats", None) else None,
            "fighter": self.fighter.to_dict() if self.fighter else None,
            "faction_standing": getattr(self, "faction_standing", None).to_dict() if getattr(self, "faction_standing", None) else None,
            "perks": list(self.perks),
            "npc_key": self.npc_key,
            "is_boss": self.is_boss,
        }

    @classmethod
    def player_from_dict(cls, data: dict) -> "Actor":
        """Reconstruct the player actor from a save dict."""
        from components.fighter import Fighter
        from components.inventory import Inventory
        from components.faction_standing import FactionStanding
        from entities.stats import Stats
        from entities.character_class import CharacterClass
        from ui import color as Color

        stats = Stats.from_dict(data["stats"]) if data.get("stats") else None
        fighter_data = data.get("fighter")
        if stats:
            fighter = Fighter.from_stats(stats)
            if fighter_data:
                fighter.hp = fighter_data["hp"]  # Restore actual current HP
        elif fighter_data:
            fighter = Fighter.from_dict(fighter_data)
        else:
            fighter = None

        char_class = CharacterClass(data["char_class"])
        actor = cls(
            x=data["x"],
            y=data["y"],
            char=data.get("char", "@"),
            color=tuple(data.get("color", Color.PLAYER_COLOR)),
            name=data["name"],
            fighter=fighter,
            inventory=Inventory(capacity=26),
        )
        actor.stats = stats
        actor.char_class = char_class

        if data.get("faction_standing"):
            fs = FactionStanding.from_dict(data["faction_standing"])
            fs.entity = actor
            actor.faction_standing = fs

        actor.perks = data.get("perks", [])
        actor.npc_key = data.get("npc_key")
        actor.is_boss = data.get("is_boss", False)
        return actor
