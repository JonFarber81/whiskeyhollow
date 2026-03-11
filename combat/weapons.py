"""Weapon definitions and stats."""

from __future__ import annotations

from dataclasses import dataclass
from enum import auto, Enum
from typing import Dict, Tuple


class WeaponType(Enum):
    MELEE = auto()
    RANGED = auto()


@dataclass(frozen=True)
class Weapon:
    key: str
    name: str
    weapon_type: WeaponType
    damage_dice: Tuple[int, int]   # (num_dice, die_size) e.g. (1, 6) = 1d6
    attack_bonus: int              # Added to actor's base_attack
    range_tiles: int               # 1 = melee only; >1 = ranged
    heat_on_use: int               # Heat increase when used (guns are loud)
    value: int                     # Cash value if sold
    description: str = ""

    def roll_damage(self, rng) -> int:
        return sum(rng.randint(1, self.damage_dice[1]) for _ in range(self.damage_dice[0]))


# All weapons keyed by their JSON key
WEAPONS: Dict[str, Weapon] = {
    "fists": Weapon(
        key="fists",
        name="Fists",
        weapon_type=WeaponType.MELEE,
        damage_dice=(1, 3),
        attack_bonus=0,
        range_tiles=1,
        heat_on_use=0,
        value=0,
        description="Your knuckles. They've never let you down.",
    ),
    "brass_knuckles": Weapon(
        key="brass_knuckles",
        name="Brass Knuckles",
        weapon_type=WeaponType.MELEE,
        damage_dice=(1, 4),
        attack_bonus=1,
        range_tiles=1,
        heat_on_use=0,
        value=15,
        description="Knuckle dusters. Silent and persuasive.",
    ),
    "knife": Weapon(
        key="knife",
        name="Knife",
        weapon_type=WeaponType.MELEE,
        damage_dice=(1, 6),
        attack_bonus=1,
        range_tiles=1,
        heat_on_use=0,
        value=20,
        description="A straight razor or folding knife. Quiet work.",
    ),
    "blackjack": Weapon(
        key="blackjack",
        name="Blackjack",
        weapon_type=WeaponType.MELEE,
        damage_dice=(1, 4),
        attack_bonus=2,
        range_tiles=1,
        heat_on_use=0,
        value=10,
        description="A leather sap. Good for putting someone to sleep.",
    ),
    "revolver_38": Weapon(
        key="revolver_38",
        name=".38 Revolver",
        weapon_type=WeaponType.RANGED,
        damage_dice=(2, 4),
        attack_bonus=2,
        range_tiles=6,
        heat_on_use=15,
        value=80,
        description="A .38 Special. Six shots. Make 'em count.",
    ),
    "pistol_1911": Weapon(
        key="pistol_1911",
        name="1911 Pistol",
        weapon_type=WeaponType.RANGED,
        damage_dice=(2, 5),
        attack_bonus=3,
        range_tiles=7,
        heat_on_use=15,
        value=120,
        description="The Army's favorite. Seven rounds of persuasion.",
    ),
    "shotgun_winchester": Weapon(
        key="shotgun_winchester",
        name="Winchester Shotgun",
        weapon_type=WeaponType.RANGED,
        damage_dice=(3, 5),
        attack_bonus=4,
        range_tiles=3,
        heat_on_use=25,
        value=150,
        description="A pump shotgun. Room-clearance special.",
    ),
    "sawed_off": Weapon(
        key="sawed_off",
        name="Sawed-Off Shotgun",
        weapon_type=WeaponType.RANGED,
        damage_dice=(3, 6),
        attack_bonus=3,
        range_tiles=2,
        heat_on_use=30,
        value=100,
        description="Concealable. Devastating at close range.",
    ),
    "tommy_gun": Weapon(
        key="tommy_gun",
        name="Tommy Gun",
        weapon_type=WeaponType.RANGED,
        damage_dice=(2, 6),
        attack_bonus=5,
        range_tiles=5,
        heat_on_use=40,
        value=300,
        description="Thompson submachine gun. Chicago's calling card.",
    ),
}


def get_weapon(key: str) -> Weapon:
    return WEAPONS.get(key, WEAPONS["fists"])
