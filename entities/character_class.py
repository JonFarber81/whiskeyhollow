"""Character class definitions — Brawler, Con Man, Smuggler, Fixer."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Tuple

from entities.stats import Stats


@dataclass(frozen=True)
class ClassBonus:
    """Flat percentage bonuses granted by character class."""
    combat_damage_bonus: float = 0.0       # % bonus to combat damage
    bribery_success_bonus: float = 0.0     # % bonus to bribery rolls
    delivery_reward_bonus: float = 0.0     # % bonus to delivery job cash
    intimidation_success_bonus: float = 0.0
    heat_reduction_bonus: float = 0.0      # % heat reduction per event
    faction_rep_gain_bonus: float = 0.0    # % extra rep from jobs


@dataclass
class CharacterClassDef:
    name: str
    description: str
    flavor: str
    str: int
    dex: int
    int_: int
    cha: int
    luck: int
    starting_cash: int
    bonus: ClassBonus
    faction_affinity: str  # Name of the faction they have a natural connection to
    starting_item_keys: list[str] = field(default_factory=list)

    def make_stats(self) -> Stats:
        return Stats(
            strength=self.str,
            dexterity=self.dex,
            intelligence=self.int_,
            charisma=self.cha,
            luck=self.luck,
        )


class CharacterClass(Enum):
    BRAWLER = "Brawler"
    CON_MAN = "Con Man"
    SMUGGLER = "Smuggler"
    FIXER = "Fixer"


# Class definitions keyed by enum
CLASS_DEFS: Dict[CharacterClass, CharacterClassDef] = {
    CharacterClass.BRAWLER: CharacterClassDef(
        name="Brawler",
        description="A street-hardened fighter who solves problems with his fists.",
        flavor="You grew up scrapping in the West Bottoms. The bulls know your face.",
        str=16, dex=12, int_=8, cha=10, luck=9,
        starting_cash=150,
        bonus=ClassBonus(
            combat_damage_bonus=0.20,
            intimidation_success_bonus=0.15,
        ),
        faction_affinity="River Market Syndicate",
        starting_item_keys=["brass_knuckles"],
    ),
    CharacterClass.CON_MAN: CharacterClassDef(
        name="Con Man",
        description="A silver-tongued grifter who never met a cop he couldn't buy.",
        flavor="You've run every hustle in the city. Your face fits anywhere.",
        str=8, dex=12, int_=13, cha=16, luck=11,
        starting_cash=300,
        bonus=ClassBonus(
            bribery_success_bonus=0.25,
            faction_rep_gain_bonus=0.10,
        ),
        faction_affinity="The Jazz District Co.",
        starting_item_keys=["forged_documents"],
    ),
    CharacterClass.SMUGGLER: CharacterClassDef(
        name="Smuggler",
        description="A delivery man who knows every back road and rail spur in KC.",
        flavor="Three cases of hooch won't move themselves. You know a guy.",
        str=10, dex=14, int_=12, cha=10, luck=9,
        starting_cash=200,
        bonus=ClassBonus(
            delivery_reward_bonus=0.20,
        ),
        faction_affinity="Union Station Crew",
        starting_item_keys=["whiskey_case", "whiskey_case", "whiskey_case"],
    ),
    CharacterClass.FIXER: CharacterClassDef(
        name="Fixer",
        description="A political operator who keeps the heat off everyone's back.",
        flavor="Half the precinct owes you a favor. The other half owes you money.",
        str=8, dex=10, int_=14, cha=14, luck=9,
        starting_cash=400,
        bonus=ClassBonus(
            heat_reduction_bonus=0.25,
            faction_rep_gain_bonus=0.15,
        ),
        faction_affinity="Pendergast Machine",
        starting_item_keys=["police_contact"],
    ),
}


def get_class_def(char_class: CharacterClass) -> CharacterClassDef:
    return CLASS_DEFS[char_class]
