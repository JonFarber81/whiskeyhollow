"""Hostile enemy AI — chases and attacks the player."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple

from components.ai.base_ai import BaseAI

if TYPE_CHECKING:
    from engine.engine import Engine


class HostileEnemy(BaseAI):
    """Chases the player when in FOV; attacks when adjacent."""

    def __init__(self) -> None:
        self.path: List[Tuple[int, int]] = []

    def perform(self, engine: Engine) -> None:
        target = engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance

        if engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                # Attack!
                from combat.combat_engine import resolve_attack
                resolve_attack(self.entity, target, engine)
                return
            # Recalculate path
            self.path = self.get_path_to(target.x, target.y, engine)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            # Only move if destination is clear
            blocking = engine.game_map.get_blocking_entity_at(dest_x, dest_y)
            if not blocking:
                self.entity.move(dest_x - self.entity.x, dest_y - self.entity.y)
