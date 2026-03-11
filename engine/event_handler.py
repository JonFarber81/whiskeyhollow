"""Input handling — translates tcod events into game actions."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event
import tcod.console
import tcod.context

from engine.exceptions import Impossible, QuitGame

if TYPE_CHECKING:
    from engine.engine import Engine

# Movement keys: arrow keys, numpad, vi-keys
MOVE_KEYS: dict[int, tuple[int, int]] = {
    # Arrow keys
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    # Numpad
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_9: (1, -1),
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_3: (1, 1),
    # Vi-keys
    tcod.event.KeySym.k: (0, -1),
    tcod.event.KeySym.j: (0, 1),
    tcod.event.KeySym.h: (-1, 0),
    tcod.event.KeySym.l: (1, 0),
    tcod.event.KeySym.y: (-1, -1),
    tcod.event.KeySym.u: (1, -1),
    tcod.event.KeySym.b: (-1, 1),
    tcod.event.KeySym.n: (1, 1),
    # Wait
    tcod.event.KeySym.PERIOD: (0, 0),
    tcod.event.KeySym.KP_5: (0, 0),
}

WAIT_KEYS = {tcod.event.KeySym.PERIOD, tcod.event.KeySym.KP_5}


class EventHandler:
    def __init__(
        self,
        engine: Engine,
        context: Optional[tcod.context.Context] = None,
        console: Optional[tcod.console.Console] = None,
    ) -> None:
        self.engine = engine
        self.context = context
        self.console = console

    def handle_events(self, event: tcod.event.Event) -> None:
        if isinstance(event, tcod.event.Quit):
            raise QuitGame()
        if isinstance(event, tcod.event.KeyDown):
            self.handle_key(event)

    def handle_key(self, event: tcod.event.KeyDown) -> None:
        key = event.sym

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            self.perform_bump(dx, dy)
        elif key == tcod.event.KeySym.ESCAPE:
            raise QuitGame()
        elif key == tcod.event.KeySym.c and self.context and self.console:
            from ui.menus import run_crew_menu
            run_crew_menu(self.engine, self.context, self.console)
        elif key == tcod.event.KeySym.f and self.context and self.console:
            from ui.menus import run_faction_menu
            run_faction_menu(self.engine, self.context, self.console)
        elif key == tcod.event.KeySym.s and self.context and self.console:
            from ui.menus import run_skill_menu
            run_skill_menu(self.engine, self.context, self.console)
        elif key == tcod.event.KeySym.SLASH and event.mod & tcod.event.Modifier.SHIFT and self.context and self.console:
            # ? = Shift+/
            from ui.menus import run_help_screen
            run_help_screen(self.context, self.console)
        elif key == tcod.event.KeySym.s and event.mod & tcod.event.Modifier.CTRL:
            # Ctrl+S — quick save (slot 0)
            self.engine.save_game(slot=0)
        elif key == tcod.event.KeySym.p and self.context and self.console:
            # p — perk list viewer
            from ui.menus import run_perk_viewer
            run_perk_viewer(self.engine, self.context, self.console)
        elif key == tcod.event.KeySym.v:
            # v — Vanish perk (once per run)
            self._use_vanish_perk()

    def _use_vanish_perk(self) -> None:
        """Vanish perk — reduce heat to 0 once per run."""
        from entities.perks import has_perk
        from ui import color as Color
        player = self.engine.player
        if not has_perk(player, "vanish"):
            return
        if getattr(self.engine, "_vanish_used", False):
            self.engine.message_log.add_message(
                "Vanish already used this run.", fg=Color.MID_GREY
            )
            return
        self.engine.heat = 0
        self.engine._vanish_used = True
        self.engine.message_log.add_message(
            "You vanish into the shadows. Heat drops to zero.", fg=Color.PARCHMENT
        )

    def perform_bump(self, dx: int, dy: int) -> None:
        """Move the player or attack an adjacent actor."""
        engine = self.engine
        player = engine.player
        dest_x = player.x + dx
        dest_y = player.y + dy

        if dx == 0 and dy == 0:
            # Wait — pass turn
            engine.message_log.add_message("You lay low.", fg=engine.message_log.messages[-1].fg if engine.message_log.messages else (255,255,255))
            self._end_turn()
            return

        if not engine.game_map.in_bounds(dest_x, dest_y):
            raise Impossible("That way is blocked.")

        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            raise Impossible("The wall don't move for nobody.")

        target = engine.game_map.get_actor_at(dest_x, dest_y)
        if target:
            from combat.combat_engine import resolve_attack
            resolve_attack(player, target, engine)
            self._end_turn()
            return

        player.move(dx, dy)
        self._end_turn()

    def _end_turn(self) -> None:
        self.engine.update_fov()
        self.engine.handle_enemy_turns()
        self.engine.turn_count += 1
        # Phase 15: fire level-up perk screen if needed
        if self.engine.pending_level_up and self.context and self.console:
            from ui.menus import run_perk_selection
            run_perk_selection(self.engine, self.context, self.console)
            self.engine.consume_level_up()
