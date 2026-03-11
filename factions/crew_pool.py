"""Procedural crew recruitment pool."""

from __future__ import annotations

import random
from typing import List

from components.crew_member import CrewMember, CrewRole

# Period-appropriate KC names
_FIRST_NAMES = [
    "Sal", "Rita", "Tommy", "Vera", "Eddie", "Dolores", "Benny", "Flo",
    "Dutch", "Mabel", "Vinnie", "Hazel", "Ace", "Pearl", "Shorty", "Ethel",
    "Knuckles", "Loretta", "Paddy", "Agnes", "Clem", "Ruthie", "Dago", "Bess",
]
_LAST_NAMES = [
    "Malone", "Torrio", "Capelli", "Burke", "O'Brien", "Marchetti",
    "Flynn", "Rossi", "Hennessey", "DeLuca", "Callahan", "Vitale",
    "Hannigan", "Conti", "Finneran", "Greco",
]

_ROLE_SKILLS = {
    CrewRole.MUSCLE:  {"combat": 3, "intimidation": 2, "stealth": 1},
    CrewRole.DRIVER:  {"driving": 4, "stealth": 2, "combat": 1},
    CrewRole.LOOKOUT: {"stealth": 4, "perception": 3, "combat": 1},
    CrewRole.FIXER:   {"persuasion": 4, "bribery": 3, "combat": 1},
}

_ROLE_WAGES = {
    CrewRole.MUSCLE:  60,
    CrewRole.DRIVER:  50,
    CrewRole.LOOKOUT: 55,
    CrewRole.FIXER:   70,
}


def generate_hire_candidates(rng: random.Random, count: int = 4) -> List[CrewMember]:
    """Generate a pool of hireable crew for the job board / faction contacts."""
    candidates = []
    roles = list(CrewRole)
    for _ in range(count):
        role = rng.choice(roles)
        first = rng.choice(_FIRST_NAMES)
        last = rng.choice(_LAST_NAMES)
        name = f"{first} {last}"
        skills = dict(_ROLE_SKILLS[role])
        # Small random variation in skills
        for k in skills:
            skills[k] = max(1, skills[k] + rng.randint(-1, 1))

        candidates.append(CrewMember(
            name=name,
            role=role,
            loyalty=rng.randint(50, 75),
            skills=skills,
            wage=_ROLE_WAGES[role] + rng.randint(-10, 10),
            hp=20,
            max_hp=20,
        ))
    return candidates
