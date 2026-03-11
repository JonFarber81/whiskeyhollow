"""Job board — generates and resolves jobs for the player."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import auto, Enum
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.engine import Engine


class JobType(Enum):
    DELIVERY = "delivery"
    HEIST = "heist"
    INTIMIDATION = "intimidation"
    PROTECTION = "protection"
    BRIBERY = "bribery"
    ASSASSINATION = "assassination"
    INTEL = "intel"


@dataclass
class Job:
    job_type: JobType
    title: str
    description: str
    faction_key: str
    cash_reward: int
    rep_reward: int
    heat_on_failure: int
    difficulty: int         # 1-5
    duration_turns: int     # Estimated turns for narrative flavor
    active: bool = False
    completed: bool = False
    failed: bool = False


# Job title templates per type (picked randomly)
_TITLES: Dict[str, List[str]] = {
    "delivery": [
        "Move Three Cases of Hooch",
        "Whiskey Run to 18th Street",
        "Night Delivery, No Questions",
        "Slip Past the Checkpoint",
    ],
    "heist": [
        "Rob the Rival's Shipment",
        "Crack the Precinct Evidence Room",
        "Snatch the Cash Box",
        "The Warehouse Job",
    ],
    "intimidation": [
        "Rough Up the Shop Owner",
        "Collect What's Owed",
        "Send a Message",
        "Discourage the Competition",
    ],
    "protection": [
        "Guard the Speakeasy Tonight",
        "Watch the Warehouse",
        "Keep the Shipment Safe",
        "Defend the Drop Point",
    ],
    "bribery": [
        "Pay Off the Judge",
        "Grease the Sergeant's Palm",
        "Buy Silence at the Precinct",
        "Put the Inspector on the Pad",
    ],
    "assassination": [
        "Take Out the Rival Capo",
        "Silence the Witness",
        "Remove an Obstacle",
        "The Long Goodbye",
    ],
    "intel": [
        "Scout the Rival's Warehouse",
        "Count the Bulls at the Precinct",
        "Map the Underground Route",
        "Find Out Who Talked",
    ],
}

_DESCRIPTIONS: Dict[str, str] = {
    "delivery": "Get the goods from A to B without the bulls noticing.",
    "heist": "Take what ain't yours — yet.",
    "intimidation": "Have a persuasive conversation with someone who needs convincing.",
    "protection": "Keep the location safe for a set number of turns.",
    "bribery": "Grease the right palms. Your CHA will do the talking.",
    "assassination": "Permanent solutions to temporary problems.",
    "intel": "Get in, look around, get out. Don't get made.",
}


def generate_jobs(
    faction_key: str,
    player_rep: int,
    rng: random.Random,
    count: int = 3,
) -> List[Job]:
    """Generate a list of available jobs for a faction based on player rep."""
    from factions.faction_data import get_faction
    faction = get_faction(faction_key)
    available_types = faction.job_pool

    # Scale difficulty with rep
    min_diff = max(1, player_rep // 25)
    max_diff = min(5, min_diff + 2)

    jobs = []
    for _ in range(count):
        job_type_key = rng.choice(available_types)
        jtype = JobType(job_type_key)
        difficulty = rng.randint(min_diff, max_diff)

        # Scale rewards with difficulty
        base_cash = 50 + difficulty * 40 + rng.randint(-20, 40)
        base_rep = 5 + difficulty * 3

        title = rng.choice(_TITLES.get(job_type_key, [f"Unknown {job_type_key}"]))
        desc = _DESCRIPTIONS.get(job_type_key, "A job worth doing.")

        jobs.append(Job(
            job_type=jtype,
            title=title,
            description=desc,
            faction_key=faction_key,
            cash_reward=base_cash,
            rep_reward=base_rep,
            heat_on_failure=difficulty * 8,
            difficulty=difficulty,
            duration_turns=difficulty * 20,
        ))

    return jobs


def resolve_job_success(job: Job, engine: Engine) -> None:
    """Apply success rewards to the engine/player."""
    from ui import color as Color
    engine.cash += job.cash_reward
    engine.message_log.add_message(
        f"Job complete: {job.title}. +${job.cash_reward}, +{job.rep_reward} rep.",
        fg=Color.GREEN,
    )

    standing = getattr(engine.player, "faction_standing", None)
    if standing:
        # Class bonus to rep gain
        from entities.character_class import CLASS_DEFS, CharacterClass
        char_class = getattr(engine, "char_class", None)
        rep_mult = 1.0
        if char_class:
            cd = CLASS_DEFS.get(char_class)
            if cd:
                rep_mult = 1.0 + cd.bonus.faction_rep_gain_bonus
        final_rep = max(1, int(job.rep_reward * rep_mult))
        standing.gain_rep(job.faction_key, final_rep, engine)

    # Grant skill point every 3rd job (tracked on engine)
    engine.jobs_completed = getattr(engine, "jobs_completed", 0) + 1
    if engine.jobs_completed % 3 == 0:
        stats = getattr(engine.player, "stats", None)
        if stats:
            stats.skill_points += 1
            engine.message_log.add_message(
                "You've earned a skill point. (Press 's' to spend it.)",
                fg=Color.AMBER,
            )

    job.completed = True


def resolve_job_failure(job: Job, engine: Engine) -> None:
    """Apply failure penalties."""
    from ui import color as Color
    from economy.heat import HeatSystem
    hs = HeatSystem(engine)
    hs.increase(job.heat_on_failure, reason="failed job")

    standing = getattr(engine.player, "faction_standing", None)
    if standing:
        rep_loss = max(2, job.rep_reward // 2)
        standing.lose_rep(job.faction_key, rep_loss)
        engine.message_log.add_message(
            f"Job failed: {job.title}. -{rep_loss} rep.", fg=Color.RED
        )

    job.failed = True
