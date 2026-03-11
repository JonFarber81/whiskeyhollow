"""Player stats — STR/DEX/INT/CHA/LUCK with derived values."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Stats:
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 10
    charisma: int = 10
    luck: int = 10

    # Skill points available to spend
    skill_points: int = 0

    @staticmethod
    def _mod(value: int) -> int:
        """D&D-style modifier: (stat - 10) // 2."""
        return (value - 10) // 2

    @property
    def str_mod(self) -> int:
        return self._mod(self.strength)

    @property
    def dex_mod(self) -> int:
        return self._mod(self.dexterity)

    @property
    def int_mod(self) -> int:
        return self._mod(self.intelligence)

    @property
    def cha_mod(self) -> int:
        return self._mod(self.charisma)

    @property
    def luck_mod(self) -> int:
        return self._mod(self.luck)

    @property
    def max_hp(self) -> int:
        return 20 + (self.strength * 2)

    @property
    def base_attack(self) -> int:
        return 2 + self.str_mod

    @property
    def base_defense(self) -> int:
        return self.dex_mod

    @property
    def dodge(self) -> int:
        return 10 + self.dex_mod

    @property
    def stealth_score(self) -> int:
        return self.dex_mod + self.int_mod

    @property
    def bribery_score(self) -> int:
        return self.cha_mod + self.int_mod

    @property
    def crit_threshold_bonus(self) -> int:
        """Crits occur at roll >= (target + 10 - luck_mod)."""
        return self.luck_mod

    def spend_skill_point(self, stat_name: str) -> bool:
        """Spend 1 SP to increase a stat by 1. Returns True on success."""
        if self.skill_points <= 0:
            return False
        if not hasattr(self, stat_name):
            return False
        current = getattr(self, stat_name)
        if current >= 20:  # Hard cap
            return False
        setattr(self, stat_name, current + 1)
        self.skill_points -= 1
        return True

    def summary(self) -> str:
        return (
            f"STR {self.strength:2d} ({self.str_mod:+d}) | "
            f"DEX {self.dexterity:2d} ({self.dex_mod:+d}) | "
            f"INT {self.intelligence:2d} ({self.int_mod:+d}) | "
            f"CHA {self.charisma:2d} ({self.cha_mod:+d}) | "
            f"LCK {self.luck:2d} ({self.luck_mod:+d})"
        )

    # -----------------------------------------------------------------------
    # Serialization (Phase 14)
    # -----------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "strength": self.strength,
            "dexterity": self.dexterity,
            "intelligence": self.intelligence,
            "charisma": self.charisma,
            "luck": self.luck,
            "skill_points": self.skill_points,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Stats":
        return cls(
            strength=data["strength"],
            dexterity=data["dexterity"],
            intelligence=data["intelligence"],
            charisma=data["charisma"],
            luck=data["luck"],
            skill_points=data.get("skill_points", 0),
        )
