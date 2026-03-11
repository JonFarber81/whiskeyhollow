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
    """Resolve one attack from attacker -> defender."""
    from ui import color as Color
    from entities.perks import has_perk

    rng = engine.rng
    attack = attacker.fighter.attack
    defense = defender.fighter.defense

    # Phase 16: Deadeye — ranged attack bonus
    if attacker is engine.player and has_perk(attacker, "deadeye"):
        weapon = getattr(attacker.inventory, "equipped_weapon", None) if attacker.inventory else None
        if weapon and getattr(weapon, "ranged", False):
            attack += 2

    # Phase 16: Streetfighter — lower crit threshold
    crit_bonus = 0
    if attacker is engine.player and has_perk(attacker, "streetfighter"):
        crit_bonus = 2

    # Phase 15: River Market rank perk — +10% combat damage at Soldier rank
    if attacker is engine.player:
        standing = getattr(engine.player, "faction_standing", None)
        if standing and standing.get_rep("river_market") >= 45:
            attack = int(attack * 1.10)

    # Roll to hit (d20 + attack vs 10 + defense)
    roll = rng.randint(1, 20) + attack
    target_num = 10 + defense
    crit_threshold = target_num + 10 - crit_bonus

    if roll >= crit_threshold:
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
        # Phase 16: Sucker Punch — first attack per enemy deals +3
        if attacker is engine.player and has_perk(attacker, "sucker_punch"):
            combat_key = id(defender)
            first_hit_set = getattr(engine, "_first_hit_enemies", set())
            if combat_key not in first_hit_set:
                damage += 3
                first_hit_set.add(combat_key)
                engine._first_hit_enemies = first_hit_set
        # Phase 16: Iron Fists — unarmed +2 damage
        if attacker is engine.player and has_perk(attacker, "iron_fists"):
            weapon = getattr(attacker.inventory, "equipped_weapon", None) if attacker.inventory else None
            if weapon is None or getattr(weapon, "key", "") in ("fists", ""):
                damage += 2
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
        # Phase 16: Blood Money — earn $10 per kill
        if attacker is engine.player and has_perk(attacker, "blood_money"):
            engine.cash += 10
        defender.fighter.die(engine)
