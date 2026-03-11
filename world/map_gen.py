"""Procedural dungeon generation using BSP room/corridor splitting."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterator, List, Tuple

import tcod
import numpy as np

from world.game_map import GameMap
from world import tile_types


@dataclass
class Room:
    x: int
    y: int
    width: int
    height: int

    @property
    def center(self) -> Tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)

    @property
    def inner(self) -> Tuple[slice, slice]:
        """The inner area of the room (excluding walls)."""
        return slice(self.x + 1, self.x + self.width - 1), slice(self.y + 1, self.y + self.height - 1)

    def intersects(self, other: Room) -> bool:
        return (
            self.x <= other.x + other.width
            and self.x + self.width >= other.x
            and self.y <= other.y + other.height
            and self.y + self.height >= other.y
        )


def _tunnel_horizontal(y: int, x1: int, x2: int) -> Iterator[Tuple[int, int]]:
    for x in range(min(x1, x2), max(x1, x2) + 1):
        yield x, y


def _tunnel_vertical(x: int, y1: int, y2: int) -> Iterator[Tuple[int, int]]:
    for y in range(min(y1, y2), max(y1, y2) + 1):
        yield x, y


def _carve_tunnel(game_map: GameMap, start: Tuple[int, int], end: Tuple[int, int]) -> None:
    x1, y1 = start
    x2, y2 = end
    # L-shaped corridor with random turn direction
    if random.random() < 0.5:
        corner = (x2, y1)
    else:
        corner = (x1, y2)

    for x, y in _tunnel_horizontal(y1, x1, corner[0]):
        game_map.tiles[x, y] = tile_types.FLOOR
    for x, y in _tunnel_vertical(corner[0], y1, y2):
        game_map.tiles[x, y] = tile_types.FLOOR
    for x, y in _tunnel_horizontal(y2, corner[0], x2):
        game_map.tiles[x, y] = tile_types.FLOOR


def generate_dungeon(
    map_width: int,
    map_height: int,
    max_rooms: int = 20,
    room_min_size: int = 5,
    room_max_size: int = 14,
    rng: random.Random | None = None,
) -> Tuple[GameMap, List[Room]]:
    """Generate a dungeon map with BSP-style room placement."""
    if rng is None:
        rng = random.Random()

    game_map = GameMap(map_width, map_height)
    rooms: List[Room] = []

    for _ in range(max_rooms):
        w = rng.randint(room_min_size, room_max_size)
        h = rng.randint(room_min_size, room_max_size)
        x = rng.randint(1, map_width - w - 2)
        y = rng.randint(1, map_height - h - 2)

        new_room = Room(x, y, w, h)

        if any(new_room.intersects(r) for r in rooms):
            continue

        # Carve out floor
        game_map.tiles[new_room.inner] = tile_types.FLOOR

        # Connect to previous room
        if rooms:
            _carve_tunnel(game_map, rooms[-1].center, new_room.center)

        rooms.append(new_room)

    return game_map, rooms
