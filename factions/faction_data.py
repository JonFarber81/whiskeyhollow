"""Static faction definitions for Whiskey Hollow."""

from __future__ import annotations

from typing import Dict

from factions.faction import Faction, RepLevel
from ui import color as Color

FACTIONS: Dict[str, Faction] = {
    "pendergast": Faction(
        key="pendergast",
        name="Pendergast Machine",
        description="Tom Pendergast runs this city from City Hall. His Machine controls judges, cops, and contracts. Work for the Machine and you work for the most powerful man in Kansas City.",
        color=Color.FACTION_PENDERGAST,
        home_district="Westport",
        enemy_factions=["kcpd"],
        job_pool=["bribery", "intel", "assassination", "protection"],
        rep_levels=[
            RepLevel(0, "Nobody"),
            RepLevel(10, "Ward Heeler", "Cops look the other way once per run"),
            RepLevel(25, "Associate", "Access to Pendergast job board"),
            RepLevel(45, "Soldier", "Heat decays 10% faster"),
            RepLevel(65, "Capo", "Can bribe detectives"),
            RepLevel(85, "Boss", "WIN CONDITION: You run this city"),
        ],
    ),
    "union_station": Faction(
        key="union_station",
        name="Union Station Crew",
        description="They move product by rail, truck, and river barge. If it's coming into Kansas City, the Crew has a cut. Join them and you'll have the best delivery network in the Midwest.",
        color=Color.FACTION_UNION,
        home_district="Union Station",
        enemy_factions=["kcpd"],
        job_pool=["delivery", "heist", "protection"],
        rep_levels=[
            RepLevel(0, "Nobody"),
            RepLevel(10, "Runner", "Delivery cash +10%"),
            RepLevel(25, "Associate", "Access to Union Station job board"),
            RepLevel(45, "Soldier", "Delivery jobs always available"),
            RepLevel(65, "Capo", "Can move 2 extra contraband units per job"),
            RepLevel(85, "Boss", "WIN CONDITION: You control the supply chain"),
        ],
    ),
    "river_market": Faction(
        key="river_market",
        name="River Market Syndicate",
        description="Warehouses, muscle, and wholesale. The Syndicate controls the supply side — they buy in bulk and sell to the speakeasies. Brute force is their preferred negotiating tactic.",
        color=Color.FACTION_SYNDICATE,
        home_district="River Market",
        enemy_factions=["jazz_district"],
        job_pool=["intimidation", "heist", "protection", "delivery"],
        rep_levels=[
            RepLevel(0, "Nobody"),
            RepLevel(10, "Tough", "Intimidation jobs +10%"),
            RepLevel(25, "Associate", "Access to Syndicate job board"),
            RepLevel(45, "Enforcer", "Combat damage +10%"),
            RepLevel(65, "Capo", "Muscle crew available for hire"),
            RepLevel(85, "Boss", "WIN CONDITION: You own the supply"),
        ],
    ),
    "jazz_district": Faction(
        key="jazz_district",
        name="The Jazz District Co.",
        description="Speakeasies, blind pigs, and front businesses along 18th & Vine. They launder money through jazz clubs and are connected to every politician who likes a good time.",
        color=Color.FACTION_JAZZ,
        home_district="18th and Vine",
        enemy_factions=["river_market"],
        job_pool=["bribery", "delivery", "intel", "assassination"],
        rep_levels=[
            RepLevel(0, "Nobody"),
            RepLevel(10, "Barfly", "Access to Jazz Co. fences — sell contraband 15% above market"),
            RepLevel(25, "Associate", "Access to Jazz District job board"),
            RepLevel(45, "Manager", "Bribery success +10%"),
            RepLevel(65, "Capo", "Fixer crew available for hire"),
            RepLevel(85, "Boss", "WIN CONDITION: You run the night life"),
        ],
    ),
    "kcpd": Faction(
        key="kcpd",
        name="Kansas City PD (Corrupt)",
        description="Most of the force is on the take. Pay them off and they'll turn a blind eye. Cross them and they'll bring the whole precinct down on you.",
        color=Color.FACTION_KCPD,
        home_district="West Bottoms",
        enemy_factions=["pendergast", "union_station"],
        job_pool=["bribery", "protection", "intel"],
        rep_levels=[
            RepLevel(0, "Suspect"),
            RepLevel(10, "Known Associate", "Heat reduction bribes cost 20% less"),
            RepLevel(25, "Informant", "Access to KCPD tip-offs (intel jobs)"),
            RepLevel(45, "Protected", "Cops ignore you at heat <50"),
            RepLevel(65, "On the Pad", "Raids never trigger"),
            RepLevel(85, "Captain's Friend", "WIN CONDITION: You own the law"),
        ],
    ),
}


def get_faction(key: str) -> Faction:
    return FACTIONS[key]


def all_factions() -> list[Faction]:
    return list(FACTIONS.values())
