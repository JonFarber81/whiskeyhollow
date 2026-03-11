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

    # -----------------------------------------------------------------------
    # Serialization (Phase 14)
    # -----------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Serialize map to JSON-compatible dict."""
        tiles_list = []
        for x in range(self.width):
            col = []
            for y in range(self.height):
                t = self.tiles[x, y]
                col.append({
                    "walkable": bool(t["walkable"]),
                    "transparent": bool(t["transparent"]),
                    "dark": [int(t["dark"]["ch"]),
                             [int(v) for v in t["dark"]["fg"]],
                             [int(v) for v in t["dark"]["bg"]]],
                    "light": [int(t["light"]["ch"]),
                              [int(v) for v in t["light"]["fg"]],
                              [int(v) for v in t["light"]["bg"]]],
                })
            tiles_list.append(col)

        # Serialize living non-player actors
        entities_data = []
        from entities.actor import Actor
        for e in self.entities:
            if isinstance(e, Actor) and e.is_alive:
                entities_data.append({
                    "type": "actor",
                    "x": e.x, "y": e.y,
                    "name": e.name,
                    "char": e.char,
                    "color": list(e.color),
                    "fighter": e.fighter.to_dict() if e.fighter else None,
                    "npc_key": getattr(e, "npc_key", None),
                    "is_boss": getattr(e, "is_boss", False),
                })

        return {
            "width": self.width,
            "height": self.height,
            "tiles": tiles_list,
            "explored": self.explored.tolist(),
            "entities": entities_data,
        }

    @classmethod
    def from_dict(cls, data: dict, player_entity=None) -> "GameMap":
        gmap = cls(data["width"], data["height"])

        # Restore tiles
        for x, col in enumerate(data["tiles"]):
            for y, td in enumerate(col):
                dark = (td["dark"][0], tuple(td["dark"][1]), tuple(td["dark"][2]))
                light = (td["light"][0], tuple(td["light"][1]), tuple(td["light"][2]))
                gmap.tiles[x, y] = np.array(
                    (td["walkable"], td["transparent"], dark, light),
                    dtype=tile_types.tile_dt,
                )

        # Restore explored
        gmap.explored = np.array(data["explored"], dtype=bool)

        # Re-attach player
        if player_entity:
            player_entity.game_map = gmap
            gmap.entities.add(player_entity)

        # Restore non-player actors
        from entities.actor import Actor
        from components.fighter import Fighter
        from components.ai.hostile_ai import HostileEnemy

        for ed in data.get("entities", []):
            if ed["type"] == "actor":
                fighter = None
                if ed.get("fighter"):
                    fighter = Fighter.from_dict(ed["fighter"])
                actor = Actor(
                    x=ed["x"], y=ed["y"],
                    char=ed["char"],
                    color=tuple(ed["color"]),
                    name=ed["name"],
                    fighter=fighter,
                    ai=HostileEnemy(),
                    game_map=gmap,
                )
                actor.npc_key = ed.get("npc_key")
                actor.is_boss = ed.get("is_boss", False)

        return gmap

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
