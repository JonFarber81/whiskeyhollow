"""GameMap: holds tile data, FOV, and entity collections."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Iterator, Optional, Tuple

import numpy as np
import tcod
from tcod import libtcodpy

from world import tile_types

if TYPE_CHECKING:
    from entities.entity import Entity
    from entities.actor import Actor


class GameMap:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.tiles = np.full((width, height), fill_value=tile_types.WALL, dtype=tile_types.tile_dt)
        self.visible = np.full((width, height), fill_value=False)
        self.explored = np.full((width, height), fill_value=False)

        self.entities: set[Entity] = set()

    @property
    def actors(self) -> Iterator[Actor]:
        from entities.actor import Actor
        yield from (e for e in self.entities if isinstance(e, Actor) and e.is_alive)

    @property
    def items(self) -> Iterator[Entity]:
        from entities.item import Item
        yield from (e for e in self.entities if isinstance(e, Item))

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_blocking_entity_at(self, x: int, y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == x and entity.y == y:
                return entity
        return None

    def get_actor_at(self, x: int, y: int) -> Optional[Actor]:
        from entities.actor import Actor
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    def compute_fov(self, x: int, y: int, radius: int = 8) -> None:
        self.visible[:] = tcod.map.compute_fov(
            self.tiles["transparent"],
            (x, y),
            radius=radius,
            algorithm=libtcodpy.FOV_SYMMETRIC_SHADOWCAST,
        )
        self.explored |= self.visible

    def render(self, console: tcod.console.Console) -> None:
        """Render map tiles respecting FOV and exploration."""
        # Visible tiles use "light" graphic; explored-but-not-visible use "dark"
        console.rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        # Draw entities sorted by render order (items under actors)
        for entity in sorted(self.entities, key=lambda e: e.render_order.value):
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
