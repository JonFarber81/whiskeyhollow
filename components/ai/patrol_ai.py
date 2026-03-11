"""Patrol AI — walks waypoints, alerts to hostile on player sight."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple

from components.ai.base_ai import BaseAI

if TYPE_CHECKING:
    from engine.engine import Engine


class PatrolAI(BaseAI):
    """Walks between waypoints. Switches to HostileEnemy AI when player is spotted."""

    def __init__(self, waypoints: List[Tuple[int, int]]) -> None:
        self.waypoints = waypoints
        self.current_wp = 0
        self.path: List[Tuple[int, int]] = []

    def perform(self, engine: Engine) -> None:
        # If player visible → alert and switch AI
        if engine.game_map.visible[self.entity.x, self.entity.y]:
            from ui import color as Color
            engine.message_log.add_message(
                f"{self.entity.name} spots you! The bull blows his whistle!",
                fg=Color.ORANGE,
            )
            from components.ai.hostile_ai import HostileEnemy
            self.entity.ai = HostileEnemy()
            self.entity.ai.entity = self.entity
            self.entity.ai.perform(engine)
            return

        # Patrol waypoints
        if not self.waypoints:
            return

        target_x, target_y = self.waypoints[self.current_wp]
        if self.entity.x == target_x and self.entity.y == target_y:
            self.current_wp = (self.current_wp + 1) % len(self.waypoints)
            return

        if not self.path:
            self.path = self.get_path_to(target_x, target_y, engine)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            blocking = engine.game_map.get_blocking_entity_at(dest_x, dest_y)
            if not blocking:
                self.entity.move(dest_x - self.entity.x, dest_y - self.entity.y)
