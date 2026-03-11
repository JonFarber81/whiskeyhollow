"""Static map loader — Phase 12.

Named locations in Kansas City are authored JSON maps rather than procedurally
generated dungeons.  The format is human-readable and easy to edit.

Usage:
    from world.locations import load_static_map
    game_map, meta = load_static_map("union_station_interior")
"""

from __future__ import annotations

import json
import os
from typing import Dict, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from world.game_map import GameMap

# Registry: map key → JSON filename (relative to data/maps/)
STATIC_MAPS: Dict[str, str] = {
    "union_station_interior": "union_station_interior.json",
    "the_blue_room":          "the_blue_room.json",
    "river_market_warehouse": "river_market_warehouse.json",
    "kcpd_precinct":          "kcpd_precinct.json",
}

_MAPS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "maps")

# Char → tile type mapping
_CHAR_TO_TILE = {
    "#": "wall",
    ".": "floor",
    "+": "door_closed",
    "/": "door_open",
    "B": "bar_counter",
    "C": "crate",
    " ": "wall",    # Blank treated as wall
}


def load_static_map(key: str) -> Tuple["GameMap", dict]:
    """
    Load an authored map by key.

    Returns (GameMap, metadata_dict) where metadata contains:
        name, district, spawn_points, objectives
    """
    from world.game_map import GameMap
    from world import tile_types

    filename = STATIC_MAPS.get(key)
    if not filename:
        raise KeyError(f"Unknown static map key: {key!r}")

    path = os.path.join(_MAPS_DIR, filename)
    with open(path, "r") as f:
        data = json.load(f)

    rows = data["rows"]
    # Determine dimensions from the longest row
    height = len(rows)
    width = max(len(r) for r in rows) if rows else 1

    gmap = GameMap(width, height)
    char_map = data.get("char_map", {})

    # Merge default char→tile with any map-specific overrides
    tile_mapping = {**_CHAR_TO_TILE, **{k: v for k, v in char_map.items() if k not in _CHAR_TO_TILE}}

    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            tile_name = tile_mapping.get(ch, "wall")
            gmap.tiles[x, y] = _get_tile(tile_name, tile_types)

    meta = {
        "key": key,
        "name": data.get("name", key),
        "district": data.get("district", "Unknown"),
        "spawn_points": data.get("spawn_points", {}),
        "objectives": data.get("objectives", []),
    }
    return gmap, meta


def _get_tile(name: str, tile_types) -> object:
    """Convert a tile type name to a numpy tile struct."""
    mapping = {
        "wall": tile_types.WALL,
        "floor": tile_types.FLOOR,
        "door_closed": tile_types.DOOR_CLOSED,
        "door_open": tile_types.DOOR_OPEN,
        "bar_counter": tile_types.BAR_COUNTER,
        "crate": tile_types.CRATE,
    }
    return mapping.get(name, tile_types.WALL)


def is_static_map(key: str) -> bool:
    return key in STATIC_MAPS
