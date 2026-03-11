#!/usr/bin/env python3
"""Whiskey Hollow — entry point."""

from __future__ import annotations

import random

import tcod
import tcod.console
import tcod.context
import tcod.event

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, TITLE, FONT_PATH, FONT_FALLBACK, TILE_WIDTH, TILE_HEIGHT
from engine.engine import Engine
from engine.event_handler import EventHandler
from engine.exceptions import Impossible, QuitGame, PlayerDead, PlayerWon
from entities.actor import Actor
from entities.character_class import CharacterClass, CLASS_DEFS
from components.fighter import Fighter
from components.inventory import Inventory
from components.faction_standing import FactionStanding
from world.map_gen import generate_dungeon
from entities.spawner import populate_map
from economy.market import Market
from economy.heat import HeatSystem
from ui import color as Color


def new_game(player_name: str = "Jack", char_class: CharacterClass = CharacterClass.BRAWLER) -> Engine:
    """Bootstrap a new game with the chosen class."""
    seed = random.randint(0, 2**32)
    rng = random.Random(seed)

    game_map, rooms = generate_dungeon(
        map_width=MAP_WIDTH,
        map_height=MAP_HEIGHT,
        rng=rng,
    )

    # Build player from class definition
    class_def = CLASS_DEFS[char_class]
    stats = class_def.make_stats()

    # Create player in the center of the first room
    start_x, start_y = rooms[0].center

    player = Actor(
        x=start_x,
        y=start_y,
        char="@",
        color=Color.PLAYER_COLOR,
        name=player_name,
        fighter=Fighter.from_stats(stats),
        inventory=Inventory(capacity=26),
        game_map=game_map,
    )
    # Attach stats and class info to player for later reference
    player.stats = stats
    player.char_class = char_class

    # Faction standing — start with affinity for class faction
    faction_standing = FactionStanding()
    faction_standing.entity = player
    faction_standing.set_starting_affinity(
        _faction_key_for_affinity(class_def.faction_affinity), amount=10
    )
    player.faction_standing = faction_standing

    # Populate map with enemies
    populate_map(game_map, rooms, rng)

    engine = Engine(
        player=player,
        game_map=game_map,
        seed=seed,
        char_class=char_class,
    )
    engine.cash = class_def.starting_cash
    engine.market = Market(rng)
    engine.heat_system = HeatSystem(engine)
    engine.controlled_districts: list[str] = []
    engine.jobs_completed: int = 0
    engine.update_fov()
    engine.message_log.add_message(
        f"Welcome to Kansas City, 1924. You're a {class_def.name}. "
        f"Keep your hat low and your gat close.",
        fg=Color.SEPIA,
    )
    return engine


def _load_tileset() -> tcod.tileset.Tileset:
    import os
    for path in (FONT_PATH, FONT_FALLBACK):
        if os.path.exists(path):
            return tcod.tileset.load_truetype_font(path, TILE_WIDTH, TILE_HEIGHT)
    # Last resort: procedural block elements (always available)
    return tcod.tileset.procedural_block_elements(TILE_WIDTH, TILE_HEIGHT)


def main() -> None:
    tileset = _load_tileset()
    with tcod.context.new(
        columns=SCREEN_WIDTH,
        rows=SCREEN_HEIGHT,
        title=TITLE,
        tileset=tileset,
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")

        from ui.menus import run_character_creation
        from ui.game_over import show_game_over, show_victory
        from factions.reputation import check_win_condition

        while True:
            # Character creation at start of each run
            player_name, char_class = run_character_creation(context, root_console)
            engine = new_game(player_name=player_name, char_class=char_class)
            event_handler = EventHandler(engine, context=context, console=root_console)

            run_ended = False
            while not run_ended:
                root_console.clear()
                engine.render(root_console)
                context.present(root_console)

                for event in tcod.event.wait():
                    context.convert_event(event)
                    try:
                        event_handler.handle_events(event)
                        # Check win condition after every action
                        if check_win_condition(engine):
                            show_victory(engine, context, root_console)
                            run_ended = True
                            break
                    except Impossible as exc:
                        engine.message_log.add_message(str(exc), fg=Color.MID_GREY)
                    except PlayerDead:
                        show_game_over(engine, context, root_console)
                        run_ended = True
                        break
                    except QuitGame:
                        return


def _faction_key_for_affinity(faction_name: str) -> str:
    """Map faction display name to its key."""
    mapping = {
        "Pendergast Machine": "pendergast",
        "Union Station Crew": "union_station",
        "River Market Syndicate": "river_market",
        "The Jazz District Co.": "jazz_district",
        "Kansas City PD (Corrupt)": "kcpd",
    }
    return mapping.get(faction_name, "pendergast")


if __name__ == "__main__":
    main()
