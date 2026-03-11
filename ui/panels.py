"""UI panel rendering — status bar, crew panel, message log, faction rep."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tcod.console

from ui import color as Color
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    MAP_WIDTH, MAP_HEIGHT,
    PANEL_WIDTH,
    MSG_LOG_HEIGHT,
)

if TYPE_CHECKING:
    from engine.engine import Engine


def render_all(console: tcod.console.Console, engine: Engine) -> None:
    """Render all UI panels onto the console."""
    _render_status_panel(console, engine)
    _render_crew_panel(console, engine)
    _render_message_log(console, engine)
    _render_faction_panel(console, engine)
    _render_borders(console)


def _render_status_panel(console: tcod.console.Console, engine: Engine) -> None:
    """Top-right panel: player stats."""
    x = MAP_WIDTH
    y = 0
    w = PANEL_WIDTH
    h = 22

    console.draw_rect(x=x, y=y, width=w, height=h, ch=ord(" "), bg=Color.PANEL_BG)
    console.print(x=x + 1, y=y + 1, string="PLAYER STATUS", fg=Color.AMBER)

    player = engine.player
    fighter = player.fighter
    if fighter:
        hp_color = Color.GREEN if fighter.hp > fighter.max_hp // 2 else (
            Color.ORANGE if fighter.hp > fighter.max_hp // 4 else Color.RED
        )
        class_name = engine.char_class.value if engine.char_class else ""
        console.print(x=x + 1, y=y + 2, string=f"{player.name} ({class_name})", fg=Color.PARCHMENT)
        console.print(x=x + 1, y=y + 3, string=f"HP:   {fighter.hp}/{fighter.max_hp}", fg=hp_color)
        # Show stats if player has them
        stats = getattr(player, "stats", None)
        if stats:
            console.print(x=x + 1, y=y + 4, string=f"STR {stats.strength:2d} DEX {stats.dexterity:2d}", fg=Color.SEPIA)
            console.print(x=x + 1, y=y + 5, string=f"INT {stats.intelligence:2d} CHA {stats.charisma:2d}", fg=Color.SEPIA)
            console.print(x=x + 1, y=y + 6, string=f"LCK {stats.luck:2d}  SP:{stats.skill_points}", fg=Color.SEPIA)

    # Heat bar
    heat_pct = engine.heat / 100
    heat_color = (
        Color.HEAT_COOL if heat_pct < 0.33 else
        Color.HEAT_WARM if heat_pct < 0.66 else
        Color.HEAT_HOT
    )
    bar_width = w - 4
    filled = int(bar_width * heat_pct)
    heat_bar = "█" * filled + "░" * (bar_width - filled)
    console.print(x=x + 1, y=y + 10, string=f"Heat: {engine.heat}%", fg=heat_color)
    console.print(x=x + 1, y=y + 11, string=heat_bar, fg=heat_color)

    # Phase 15: Display level
    level = engine._get_player_level()
    console.print(x=x + 1, y=y + 8, string=f"Lvl:  {level}   Cash: ${engine.cash:,}", fg=Color.GOLD)

    # Phase 16: Display perk count
    perks = getattr(engine.player, "perks", [])
    if perks:
        console.print(x=x + 1, y=y + 9, string=f"Perks: {len(perks)}  [p] view", fg=Color.AMBER_DARK)

    console.print(x=x + 1, y=y + 13, string=f"Turn: {engine.turn_count}", fg=Color.MID_GREY)
    console.print(x=x + 1, y=y + 14, string=f"Dist: {engine.district}", fg=Color.SEPIA)


def _render_crew_panel(console: tcod.console.Console, engine: Engine) -> None:
    """Middle-right panel: crew roster."""
    x = MAP_WIDTH
    y = 22
    w = PANEL_WIDTH
    h = MAP_HEIGHT - 22

    console.draw_rect(x=x, y=y, width=w, height=h, ch=ord(" "), bg=Color.PANEL_BG)
    console.print(x=x + 1, y=y + 1, string="CREW  [c]", fg=Color.AMBER)

    crew = getattr(engine, "crew", None)
    if not crew or not crew.members:
        console.print(x=x + 1, y=y + 3, string="(No crew yet)", fg=Color.MID_GREY)
        return

    from components.crew_member import CrewStatus
    status_icons = {
        CrewStatus.AVAILABLE: "●",
        CrewStatus.INJURED:   "✚",
        CrewStatus.ARRESTED:  "⛓",
        CrewStatus.DEAD:      "✖",
    }
    status_colors = {
        CrewStatus.AVAILABLE: Color.GREEN,
        CrewStatus.INJURED:   Color.ORANGE,
        CrewStatus.ARRESTED:  Color.RED,
        CrewStatus.DEAD:      Color.MID_GREY,
    }
    for i, member in enumerate(crew.members):
        if y + 3 + i >= y + h - 1:
            break
        icon = status_icons.get(member.status, "?")
        sc = status_colors.get(member.status, Color.MID_GREY)
        console.print(x=x + 1, y=y + 3 + i, string=icon, fg=sc)
        role_short = member.role.value[:3].upper()
        label = f" {member.name[:12]} ({role_short})"
        console.print(x=x + 2, y=y + 3 + i, string=label, fg=Color.PARCHMENT if member.is_active else Color.MID_GREY)


def _render_message_log(console: tcod.console.Console, engine: Engine) -> None:
    """Bottom-left panel: message log."""
    x = 0
    y = MAP_HEIGHT
    w = MAP_WIDTH
    h = MSG_LOG_HEIGHT

    console.draw_rect(x=x, y=y, width=w, height=h, ch=ord(" "), bg=Color.PANEL_BG)
    console.print(x=x + 1, y=y + 1, string="MESSAGE LOG", fg=Color.AMBER_DARK)
    engine.message_log.render(console, x=x, y=y + 2, width=w, height=h - 2)


def _render_faction_panel(console: tcod.console.Console, engine: Engine) -> None:
    """Bottom-right panel: faction reputation."""
    x = MAP_WIDTH
    y = MAP_HEIGHT
    w = PANEL_WIDTH
    h = MSG_LOG_HEIGHT

    console.draw_rect(x=x, y=y, width=w, height=h, ch=ord(" "), bg=Color.PANEL_BG)
    console.print(x=x + 1, y=y + 1, string="FACTION REP", fg=Color.AMBER)

    standing = getattr(engine.player, "faction_standing", None)
    if not standing:
        console.print(x=x + 1, y=y + 3, string="(No allegiances)", fg=Color.MID_GREY)
        return

    from factions.faction_data import FACTIONS
    short_names = {
        "pendergast": "Pendergast",
        "union_station": "Union Stn",
        "river_market": "Syndicate",
        "jazz_district": "Jazz Co.",
        "kcpd": "KCPD",
    }

    for i, (key, faction) in enumerate(FACTIONS.items()):
        rep = standing.get_rep(key)
        title = faction.rank_title(rep)
        star = " ★" if rep >= 85 else ""
        label = f"{short_names.get(key, key[:8])}: {rep:3d}{star}"
        fg = faction.color if rep > 0 else Color.MID_GREY
        console.print(x=x + 1, y=y + 2 + i * 2, string=label, fg=fg)
        # Mini rep bar
        bar_w = w - 4
        filled = int(bar_w * rep / 100)
        bar = "▪" * filled + "·" * (bar_w - filled)
        console.print(x=x + 1, y=y + 3 + i * 2, string=bar, fg=fg)


def _render_borders(console: tcod.console.Console) -> None:
    """Draw dividing lines between panels."""
    # Vertical divider
    for y in range(SCREEN_HEIGHT):
        console.print(x=MAP_WIDTH, y=y, string="│", fg=Color.AMBER_DARK)
    # Horizontal divider (map / message log)
    for x in range(SCREEN_WIDTH):
        console.print(x=x, y=MAP_HEIGHT, string="─", fg=Color.AMBER_DARK)
    # Corner cross
    console.print(x=MAP_WIDTH, y=MAP_HEIGHT, string="┼", fg=Color.AMBER_DARK)
    # Sub-divider in right panel (status / crew)
    for x in range(MAP_WIDTH, SCREEN_WIDTH):
        console.print(x=x, y=22, string="─", fg=Color.AMBER_DARK)
    console.print(x=MAP_WIDTH, y=22, string="├", fg=Color.AMBER_DARK)
