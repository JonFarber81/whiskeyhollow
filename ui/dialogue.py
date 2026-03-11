"""Dialogue overlay — Phase 13.

Shows a blocking NPC dialogue box when the player encounters a named NPC.
No branching — linear dialog only (MVP).
"""

from __future__ import annotations

import json
import os
from typing import Optional, TYPE_CHECKING

import tcod.console
import tcod.context
import tcod.event

from ui import color as Color
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

if TYPE_CHECKING:
    from engine.engine import Engine

_NPC_DATA: Optional[dict] = None


def _load_npc_data() -> dict:
    global _NPC_DATA
    if _NPC_DATA is None:
        path = os.path.join(os.path.dirname(__file__), "..", "data", "npcs.json")
        try:
            with open(path) as f:
                _NPC_DATA = json.load(f)
        except Exception:
            _NPC_DATA = {}
    return _NPC_DATA


def show_dialogue(
    engine: "Engine",
    npc_key: str,
    event_type: str,
    context: tcod.context.Context,
    console: tcod.console.Console,
) -> None:
    """
    Show a blocking dialogue overlay for the given NPC and event type.
    Player presses any key to dismiss.
    """
    npcs = _load_npc_data()
    npc_data = npcs.get(npc_key, {})
    lines = npc_data.get("dialogue", {}).get(event_type, [])
    if not lines:
        return

    line = engine.rng.choice(lines)
    npc_name = npc_data.get("name", npc_key)

    _draw_dialogue(console, engine, npc_name, line, npc_data)
    context.present(console)

    # Wait for keypress
    for event in tcod.event.wait():
        if isinstance(event, (tcod.event.KeyDown, tcod.event.Quit)):
            return


def _draw_dialogue(
    console: tcod.console.Console,
    engine: "Engine",
    npc_name: str,
    line: str,
    npc_data: dict,
) -> None:
    """Render the dialogue box onto the console."""
    engine.render(console)

    # Dialog box — bottom third of screen
    bw = SCREEN_WIDTH - 10
    bh = 8
    bx = 5
    by = SCREEN_HEIGHT - bh - 2

    npc_color = tuple(npc_data.get("color", [220, 200, 140]))

    console.draw_frame(
        x=bx, y=by, width=bw, height=bh,
        title=f" {npc_name} ",
        fg=npc_color,
        bg=Color.PANEL_BG,
    )

    # Word-wrap the line
    from ui.message_log import MessageLog
    wrapped = MessageLog._wrap(f'"{line}"', bw - 4)
    for i, text in enumerate(wrapped[:bh - 3]):
        console.print(x=bx + 2, y=by + 2 + i, string=text, fg=Color.PARCHMENT)

    console.print(
        x=bx + 2, y=by + bh - 2,
        string="[Any key] Continue",
        fg=Color.MID_GREY,
    )


def trigger_meet_dialogue(
    engine: "Engine",
    npc_key: str,
    context: Optional[tcod.context.Context],
    console: Optional[tcod.console.Console],
) -> None:
    """Called when the player first encounters a named NPC."""
    if context and console:
        show_dialogue(engine, npc_key, "on_meet", context, console)
    # Also log it
    npcs = _load_npc_data()
    npc_name = npcs.get(npc_key, {}).get("name", npc_key)
    engine.message_log.add_message(
        f"You encounter {npc_name}!", fg=Color.GOLD
    )
