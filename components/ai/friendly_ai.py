"""Friendly crew AI — follows player, attacks hostiles in range."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple

from components.ai.base_ai import BaseAI

if TYPE_CHECKING:
    from engine.engine import Engine
    from entities.actor import Actor


class CrewAI(BaseAI):
    """Follows player, attacks the nearest hostile visible to them."""

    def __init__(self) -> None:
        self.path: List[Tuple[int, int]] = []

    def perform(self, engine: Engine) -> None:
        player = engine.player

        # Find nearest hostile in FOV
        target = self._nearest_hostile(engine)
        if target:
            dx = target.x - self.entity.x
            dy = target.y - self.entity.y
            distance = max(abs(dx), abs(dy))
            if distance <= 1:
                from combat.combat_engine import resolve_attack
                resolve_attack(self.entity, target, engine)
                return
            self.path = self.get_path_to(target.x, target.y, engine)
        else:
            # Follow player — stay within 2 tiles
            dist_to_player = max(abs(player.x - self.entity.x), abs(player.y - self.entity.y))
            if dist_to_player > 2:
                self.path = self.get_path_to(player.x, player.y, engine)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            blocking = engine.game_map.get_blocking_entity_at(dest_x, dest_y)
            if not blocking or blocking is player:
                self.entity.move(dest_x - self.entity.x, dest_y - self.entity.y)

    def _nearest_hostile(self, engine: Engine) -> Optional[Actor]:
        """Return the closest actor that is not the player or crew."""
        from entities.actor import Actor
        best = None
        best_dist = 999
        for actor in engine.game_map.actors:
            if actor is engine.player or actor is self.entity:
                continue
            # Check if it's a crew member
            if getattr(actor, "_is_crew", False):
                continue
            if engine.game_map.visible[actor.x, actor.y]:
                dist = max(abs(actor.x - self.entity.x), abs(actor.y - self.entity.y))
                if dist < best_dist:
                    best_dist = dist
                    best = actor
        return best
