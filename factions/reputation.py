"""Reputation rank system and perk evaluation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from constants import REP_BOSS, WIN_DISTRICTS_BOSS

if TYPE_CHECKING:
    from engine.engine import Engine


def check_win_condition(engine: Engine) -> bool:
    """Return True if the player has met a win condition."""
    from constants import WIN_CASH_RETIRE
    # Retirement win
    if engine.cash >= WIN_CASH_RETIRE:
        engine.message_log.add_message(
            f"You've stashed ${engine.cash:,}. Time to retire to Florida.",
            fg=(230, 190, 40),
        )
        return True

    # Boss win — reach top rank in any faction + hold 3 districts
    standing = getattr(engine.player, "faction_standing", None)
    if standing:
        for key, rep in standing.rep.items():
            if rep >= REP_BOSS:
                controlled = getattr(engine, "controlled_districts", [])
                if len(controlled) >= WIN_DISTRICTS_BOSS:
                    from factions.faction_data import get_faction
                    faction = get_faction(key)
                    engine.message_log.add_message(
                        f"You are the Boss of {faction.name}. Kansas City is yours.",
                        fg=(230, 190, 40),
                    )
                    return True
    return False
