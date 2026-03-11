"""Tile type definitions using numpy structured arrays."""

from __future__ import annotations

import numpy as np

# Graphic dtype: character + colors
graphic_dt = np.dtype(
    [
        ("ch", np.int32),       # Unicode codepoint
        ("fg", "3B"),           # RGB foreground
        ("bg", "3B"),           # RGB background
    ]
)

# Tile dtype: walkability, transparency, and two graphics (dark/light)
tile_dt = np.dtype(
    [
        ("walkable", bool),
        ("transparent", bool),
        ("dark", graphic_dt),   # Tile in unexplored / out-of-FOV area
        ("light", graphic_dt),  # Tile in FOV
    ]
)


def new_tile(
    *,
    walkable: int,
    transparent: int,
    dark: tuple,
    light: tuple,
) -> np.ndarray:
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# Solid opaque wall
WALL = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("#"), (100, 80, 40), (30, 22, 12)),
    light=(ord("#"), (160, 130, 70), (50, 38, 20)),
)

# Open floor
FLOOR = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("."), (60, 48, 25), (30, 22, 12)),
    light=(ord("."), (100, 80, 40), (50, 38, 20)),
)

# Locked/closed door — treated as wall until opened
DOOR_CLOSED = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("+"), (120, 90, 40), (30, 22, 12)),
    light=(ord("+"), (180, 130, 60), (50, 38, 20)),
)

# Open door
DOOR_OPEN = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("/"), (100, 75, 35), (30, 22, 12)),
    light=(ord("/"), (160, 115, 50), (50, 38, 20)),
)

# Void / unexplored shroud
SHROUD = np.array((ord(" "), (0, 0, 0), (0, 0, 0)), dtype=graphic_dt)

# Phase 12: Static map special tiles
BAR_COUNTER = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("="), (100, 70, 30), (30, 22, 12)),
    light=(ord("="), (160, 120, 50), (50, 38, 20)),
)

CRATE = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("c"), (80, 60, 30), (30, 22, 12)),
    light=(ord("c"), (130, 95, 45), (50, 38, 20)),
)
