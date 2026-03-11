"""Core Engine — game loop, state management, rendering coordination."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional

import tcod.console

from ui.message_log import MessageLog
from ui import color as Color

if TYPE_CHECKING:
    from entities.actor import Actor
    from world.game_map import GameMap


class Engine:
    def __init__(
        self,
        player: Actor,
        game_map: GameMap,
        seed: Optional[int] = None,
        char_class: Optional[object] = None,
    ) -> None:
        self.player = player
        self.game_map = game_map
        self.char_class = char_class

        self.rng = random.Random(seed)
        self.seed = seed if seed is not None else 0

        self.message_log = MessageLog()
        self.turn_count = 0

        # Economy / meta state (populated by subsystems)
        self.heat: int = 0          # 0-100
        self.cash: int = 100
        self.district: str = "West Bottoms"

        # Crew
        from components.crew_member import CrewRoster
        self.crew: CrewRoster = CrewRoster()

    def handle_enemy_turns(self) -> None:
        for actor in list(self.game_map.actors):
            if actor is self.player:
                continue
            if actor.ai:
                actor.ai.perform(self)

    def update_fov(self) -> None:
        self.game_map.compute_fov(self.player.x, self.player.y)

    def render(self, console: tcod.console.Console) -> None:
        from ui.panels import render_all
        self.game_map.render(console)
        render_all(console, self)
