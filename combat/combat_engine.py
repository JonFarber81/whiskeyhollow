"""Turn-based combat resolution — pure functions."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.actor import Actor
    from engine.engine import Engine

# Period-appropriate hit descriptors
_HIT_MSGS = [
    "clips",
    "belts",
    "slugs",
    "cracks",
    "lays into",
    "wallops",
]

_MISS_MSGS = [
    "swings and misses",
    "whiffs it",
    "telegraphs the punch",
    "misses wide",
]

_CRIT_MSGS = [
    "floors",
    "cold-cocks",
    "drops",
    "decks",
]


def resolve_attack(attacker: Actor, defender: Actor, engine: Engine) -> None:
    """Resolve one attack from attacker → defender."""
    from ui import color as Color

    rng = engine.rng
    attack = attacker.fighter.attack
    defense = defender.fighter.defense

    # Roll to hit (d20 + attack vs 10 + defense)
    roll = rng.randint(1, 20) + attack
    target_num = 10 + defense

    if roll >= target_num + 10:
        # Critical hit
        damage = max(1, attack * 2 - defense)
        verb = rng.choice(_CRIT_MSGS)
        msg = f"{attacker.name} {verb} {defender.name} for {damage} damage!"
        fg = Color.RED if attacker is not engine.player else Color.GOLD
        engine.message_log.add_message(msg, fg=fg)
        defender.fighter.take_damage(damage)
    elif roll >= target_num:
        # Normal hit
        damage = max(1, attack - defense)
        verb = rng.choice(_HIT_MSGS)
        msg = f"{attacker.name} {verb} {defender.name} for {damage} damage."
        fg = Color.MSG_ATTACK if defender is engine.player else Color.MSG_DEFAULT
        engine.message_log.add_message(msg, fg=fg)
        defender.fighter.take_damage(damage)
    else:
        # Miss
        verb = rng.choice(_MISS_MSGS)
        msg = f"{attacker.name} {verb}."
        engine.message_log.add_message(msg, fg=Color.MID_GREY)

    # Check for death
    if defender.fighter.hp <= 0:
        defender.fighter.die(engine)
