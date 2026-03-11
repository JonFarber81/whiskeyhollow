"""Fighter component — derives HP and combat values from Stats."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.actor import Actor
    from entities.stats import Stats
    from engine.engine import Engine


@dataclass
class Fighter:
    """
    Combat component. Can be initialized with raw values (for simple enemies)
    or linked to a Stats object (for the player and named NPCs).
    """
    max_hp: int
    hp: int
    base_attack: int
    base_defense: int
    stats: Optional[Stats] = field(default=None, repr=False)
    entity: Optional[Actor] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        # If we have a stats object, derive values from it
        if self.stats:
            self.max_hp = self.stats.max_hp
            self.hp = self.max_hp
            self.base_attack = self.stats.base_attack
            self.base_defense = self.stats.base_defense
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    @classmethod
    def from_stats(cls, stats: Stats) -> Fighter:
        return cls(
            max_hp=stats.max_hp,
            hp=stats.max_hp,
            base_attack=stats.base_attack,
            base_defense=stats.base_defense,
            stats=stats,
        )

    @property
    def attack(self) -> int:
        bonus = 0
        if self.entity and self.entity.inventory:
            weapon = self.entity.inventory.equipped_weapon
            if weapon:
                bonus += getattr(weapon, "attack_bonus", 0)
        return self.base_attack + bonus

    @property
    def defense(self) -> int:
        return self.base_defense

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0
        healed = min(amount, self.max_hp - self.hp)
        self.hp += healed
        return healed

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    def die(self, engine: Engine) -> None:
        from ui import color as Color
        if engine.player is self.entity:
            death_msg = "You have been rubbed out. Game over, flatfoot."
            death_color = Color.RED
        else:
            death_msg = f"{self.entity.name} is down for the count."
            death_color = Color.AMBER
            # Track kills on engine
            engine.total_kills = getattr(engine, "total_kills", 0) + 1
        engine.message_log.add_message(death_msg, fg=death_color)

        self.entity.char = "%"
        self.entity.color = Color.RED_DARK
        self.entity.blocks_movement = False
        self.entity.name = f"remains of {self.entity.name}"
        from entities.entity import RenderOrder
        self.entity.render_order = RenderOrder.CORPSE

        if engine.player is self.entity:
            from engine.exceptions import PlayerDead
            raise PlayerDead()

    # -----------------------------------------------------------------------
    # Serialization (Phase 14)
    # -----------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "hp": self.hp,
            "max_hp": self.max_hp,
            "base_attack": self.base_attack,
            "base_defense": self.base_defense,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Fighter":
        return cls(
            hp=data["hp"],
            max_hp=data["max_hp"],
            base_attack=data["base_attack"],
            base_defense=data["base_defense"],
        )
