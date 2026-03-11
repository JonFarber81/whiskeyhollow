"""Base Entity class for all game objects."""

from __future__ import annotations

from enum import auto, Enum
from typing import TYPE_CHECKING, Optional, Tuple, Type, TypeVar

if TYPE_CHECKING:
    from world.game_map import GameMap

T = TypeVar("T", bound="Entity")


class RenderOrder(Enum):
    ITEM = auto()
    CORPSE = auto()
    ACTOR = auto()


class Entity:
    """A generic object that exists on the map."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.ITEM,
        game_map: Optional[GameMap] = None,
    ) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order

        if game_map:
            self.game_map = game_map
            game_map.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def place(self, x: int, y: int, game_map: Optional[GameMap] = None) -> None:
        self.x = x
        self.y = y
        if game_map:
            if hasattr(self, "game_map") and self.game_map is not game_map:
                self.game_map.entities.discard(self)
            self.game_map = game_map
            game_map.entities.add(self)
