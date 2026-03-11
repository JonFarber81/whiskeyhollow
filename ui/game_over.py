"""Game over and victory screens."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tcod.console
import tcod.context
import tcod.event

from ui import color as Color
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

if TYPE_CHECKING:
    from engine.engine import Engine


def show_game_over(engine: Engine, context: tcod.context.Context, console: tcod.console.Console) -> None:
    """Show death screen with run summary. Press any key to return to title."""
    from engine.meta import update_meta_on_run_end
    meta = update_meta_on_run_end(engine, won=False)

    console.clear()
    _draw_game_over(console, engine, meta)
    context.present(console)

    while True:
        for event in tcod.event.wait():
            if isinstance(event, (tcod.event.KeyDown, tcod.event.Quit)):
                return


def show_victory(engine: Engine, context: tcod.context.Context, console: tcod.console.Console) -> None:
    """Show victory screen. Press any key to return to title."""
    from engine.meta import update_meta_on_run_end
    meta = update_meta_on_run_end(engine, won=True)

    console.clear()
    _draw_victory(console, engine, meta)
    context.present(console)

    while True:
        for event in tcod.event.wait():
            if isinstance(event, (tcod.event.KeyDown, tcod.event.Quit)):
                return


def _draw_game_over(console: tcod.console.Console, engine: Engine, meta: dict) -> None:
    cx = SCREEN_WIDTH // 2
    cy = SCREEN_HEIGHT // 4

    lines = [
        (cx, cy,     "YOU'VE BEEN RUBBED OUT",   Color.RED,       True),
        (cx, cy + 1, "Kansas City don't forgive the slow.",  Color.SEPIA, False),
        (cx, cy + 3, "─" * 40,                   Color.AMBER_DARK, False),
    ]
    _center_lines(console, lines)

    # Run summary
    summary_x = cx - 18
    sy = cy + 5
    player = engine.player
    standing = getattr(player, "faction_standing", None)
    best_faction = ""
    best_rep = 0
    if standing:
        for key, rep in standing.rep.items():
            if rep > best_rep:
                best_rep = rep
                from factions.faction_data import get_faction
                best_faction = f"{get_faction(key).name} — {get_faction(key).rank_title(rep)}"

    summary = [
        f"Name:          {player.name}",
        f"Class:         {getattr(player, 'char_class', '?').value if hasattr(getattr(player, 'char_class', None), 'value') else '?'}",
        f"Turns survived:{engine.turn_count:>6}",
        f"Cash at death: ${engine.cash:,}",
        f"Jobs completed:{getattr(engine, 'jobs_completed', 0):>6}",
        f"Best faction:  {best_faction or 'Nobody'}",
        f"Enemies downed:{getattr(engine, 'total_kills', 0):>6}",
    ]
    for i, line in enumerate(summary):
        console.print(x=summary_x, y=sy + i, string=line, fg=Color.PARCHMENT)

    new_unlocks = [k for k, v in meta.get("unlocks", {}).items() if v]
    if new_unlocks:
        console.print(x=summary_x, y=sy + len(summary) + 2, string="META UNLOCKS EARNED:", fg=Color.GOLD)
        for i, u in enumerate(new_unlocks):
            console.print(x=summary_x + 2, y=sy + len(summary) + 3 + i, string=f"★ {u.replace('_', ' ').title()}", fg=Color.AMBER)

    console.print(x=cx - 12, y=SCREEN_HEIGHT - 3,
                  string="Press any key to return to the title screen.",
                  fg=Color.MID_GREY)


def _draw_victory(console: tcod.console.Console, engine: Engine, meta: dict) -> None:
    cx = SCREEN_WIDTH // 2
    cy = SCREEN_HEIGHT // 5

    lines = [
        (cx, cy,     "KANSAS CITY IS YOURS",     Color.GOLD,  True),
        (cx, cy + 1, "They'll be telling stories about you for years.", Color.SEPIA, False),
        (cx, cy + 3, "─" * 40,                  Color.AMBER_DARK, False),
    ]
    _center_lines(console, lines)

    player = engine.player
    sy = cy + 5
    summary_x = cx - 18
    summary = [
        f"Name:          {player.name}",
        f"Cash:          ${engine.cash:,}",
        f"Turns taken:   {engine.turn_count}",
        f"Jobs completed:{getattr(engine, 'jobs_completed', 0):>6}",
    ]
    for i, line in enumerate(summary):
        console.print(x=summary_x, y=sy + i, string=line, fg=Color.PARCHMENT)

    console.print(x=cx - 12, y=SCREEN_HEIGHT - 3,
                  string="Press any key to return to the title screen.",
                  fg=Color.MID_GREY)


def _center_lines(console, lines) -> None:
    for cx, y, text, fg, bold in lines:
        x = cx - len(text) // 2
        console.print(x=x, y=y, string=text, fg=fg)
