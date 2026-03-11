"""Base AI class for all non-player actors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Optional, Tuple

import tcod

if TYPE_CHECKING:
    from engine.engine import Engine
    from entities.actor import Actor


class BaseAI(ABC):
    entity: Actor

    @abstractmethod
    def perform(self, engine: Engine) -> None:
        raise NotImplementedError

    def get_path_to(self, dest_x: int, dest_y: int, engine: Engine) -> List[Tuple[int, int]]:
        """Compute a walkable path toward a destination, avoiding other actors."""
        cost = np.array(engine.game_map.tiles["walkable"], dtype=np.int8)
        # Mark other actors as blocking (cost 10 to route around them)
        for entity in engine.game_map.actors:
            if entity is not self.entity and entity.blocks_movement:
                cost[entity.x, entity.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)
        pathfinder.add_root((self.entity.x, self.entity.y))
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()
        return [(x, y) for x, y in path]


# Avoid circular import at module level
import numpy as np  # noqa: E402
