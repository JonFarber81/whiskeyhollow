"""Crew member component — manages a single crew hire."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import auto, Enum
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.engine import Engine


class CrewRole(Enum):
    MUSCLE = "Muscle"
    DRIVER = "Driver"
    LOOKOUT = "Lookout"
    FIXER = "Fixer"


class CrewStatus(Enum):
    AVAILABLE = "available"
    INJURED = "injured"
    ARRESTED = "arrested"
    DEAD = "dead"


@dataclass
class CrewMember:
    name: str
    role: CrewRole
    loyalty: int                    # 0-100
    skills: Dict[str, int] = field(default_factory=dict)   # e.g. {"combat": 3}
    wage: int = 50                  # Cash per chapter
    status: CrewStatus = CrewStatus.AVAILABLE
    hp: int = 20
    max_hp: int = 20

    @property
    def is_active(self) -> bool:
        return self.status == CrewStatus.AVAILABLE

    @property
    def role_bonus_description(self) -> str:
        return {
            CrewRole.MUSCLE:  "Combat dmg +20%, Intimidation +20%",
            CrewRole.DRIVER:  "Delivery cash +15%, Escape +25%",
            CrewRole.LOOKOUT: "Heat rate -20%, Early patrol warning",
            CrewRole.FIXER:   "Bribery +20%, Can spring arrested crew",
        }[self.role]

    def apply_combat_bonus(self, base_attack: int) -> int:
        """Muscle bonus to attack."""
        if self.role == CrewRole.MUSCLE and self.is_active:
            return base_attack + self.skills.get("combat", 0)
        return base_attack

    def apply_delivery_bonus(self, base_cash: int) -> int:
        if self.role == CrewRole.DRIVER and self.is_active:
            return int(base_cash * 1.15)
        return base_cash

    def apply_heat_modifier(self, heat_amount: int) -> int:
        """Lookout reduces incoming heat."""
        if self.role == CrewRole.LOOKOUT and self.is_active:
            return max(1, int(heat_amount * 0.80))
        return heat_amount

    def apply_bribery_bonus(self, base_score: int) -> int:
        if self.role == CrewRole.FIXER and self.is_active:
            return base_score + self.skills.get("persuasion", 2)
        return base_score

    def gain_loyalty(self, amount: int) -> None:
        self.loyalty = min(100, self.loyalty + amount)

    def lose_loyalty(self, amount: int) -> None:
        self.loyalty = max(0, self.loyalty - amount)

    def injure(self, engine: Engine) -> None:
        from ui import color as Color
        self.status = CrewStatus.INJURED
        engine.message_log.add_message(
            f"{self.name} took a hit and is laid up for a while.", fg=Color.ORANGE
        )

    def arrest(self, engine: Engine) -> None:
        from ui import color as Color
        self.status = CrewStatus.ARRESTED
        engine.message_log.add_message(
            f"{self.name} got pinched by the bulls!", fg=Color.RED
        )

    def die(self, engine: Engine) -> None:
        from ui import color as Color
        self.status = CrewStatus.DEAD
        engine.message_log.add_message(
            f"{self.name} is dead. You'll pour one out for them later.", fg=Color.RED_DARK
        )

    def recover(self) -> None:
        """Called at chapter end — injured crew may recover."""
        if self.status == CrewStatus.INJURED:
            self.status = CrewStatus.AVAILABLE
            self.hp = self.max_hp


# ---------------------------------------------------------------------------
# Crew roster attached to the engine
# ---------------------------------------------------------------------------

class CrewRoster:
    def __init__(self) -> None:
        self.members: list[CrewMember] = []

    def add(self, member: CrewMember) -> bool:
        from constants import MAX_CREW
        if len(self.members) >= MAX_CREW:
            return False
        self.members.append(member)
        return True

    def remove(self, member: CrewMember) -> None:
        self.members.remove(member)

    @property
    def active(self) -> list[CrewMember]:
        return [m for m in self.members if m.is_active]

    def pay_wages(self, engine: Engine) -> None:
        """Deduct wages at end of chapter. Low cash → loyalty loss."""
        from ui import color as Color
        total = sum(m.wage for m in self.active)
        if engine.cash >= total:
            engine.cash -= total
            engine.message_log.add_message(
                f"Crew wages paid: -${total}.", fg=Color.GOLD
            )
        else:
            # Can't pay — loyalty drops for everyone
            engine.message_log.add_message(
                "Can't make payroll! Crew loyalty is taking a hit.", fg=Color.RED
            )
            for m in self.active:
                m.lose_loyalty(15)
            engine.cash = 0

    def end_of_chapter(self, engine: Engine) -> None:
        self.pay_wages(engine)
        for m in self.members:
            m.recover()

    def has_role(self, role: CrewRole) -> bool:
        return any(m.role == role and m.is_active for m in self.members)

    def get_role(self, role: CrewRole) -> Optional[CrewMember]:
        for m in self.members:
            if m.role == role and m.is_active:
                return m
        return None
