"""Entity spawning — creates actors from template definitions."""

from __future__ import annotations

import random
from typing import Optional, Tuple

from entities.actor import Actor
from components.fighter import Fighter
from components.inventory import Inventory
from components.ai.hostile_ai import HostileEnemy
from components.ai.patrol_ai import PatrolAI
from world.game_map import GameMap
from ui import color as Color


# Enemy templates
_ENEMY_TEMPLATES = {
    "rival_goon": {
        "char": "g", "color": Color.ENEMY_GOON, "name": "Rival Goon",
        "max_hp": 14, "base_attack": 2, "base_defense": 0,
        "ai": "hostile",
    },
    "made_man": {
        "char": "m", "color": (200, 80, 60), "name": "Made Man",
        "max_hp": 25, "base_attack": 4, "base_defense": 2,
        "ai": "hostile",
    },
    "beat_cop": {
        "char": "c", "color": Color.ENEMY_COP, "name": "Beat Cop",
        "max_hp": 20, "base_attack": 2, "base_defense": 1,
        "ai": "patrol",
    },
    "detective": {
        "char": "d", "color": (100, 120, 220), "name": "Detective",
        "max_hp": 28, "base_attack": 3, "base_defense": 2,
        "ai": "hostile",
    },
    "mob_enforcer": {
        "char": "E", "color": (220, 40, 40), "name": "Mob Enforcer",
        "max_hp": 40, "base_attack": 5, "base_defense": 3,
        "ai": "hostile",
    },
}


def spawn_enemy(
    key: str,
    x: int,
    y: int,
    game_map: GameMap,
    patrol_points: Optional[list] = None,
) -> Actor:
    tmpl = _ENEMY_TEMPLATES[key]

    if tmpl["ai"] == "patrol":
        waypoints = patrol_points or [(x, y)]
        ai = PatrolAI(waypoints=waypoints)
    else:
        ai = HostileEnemy()

    actor = Actor(
        x=x, y=y,
        char=tmpl["char"],
        color=tmpl["color"],
        name=tmpl["name"],
        fighter=Fighter(
            max_hp=tmpl["max_hp"],
            hp=tmpl["max_hp"],
            base_attack=tmpl["base_attack"],
            base_defense=tmpl["base_defense"],
        ),
        inventory=Inventory(capacity=4),
        ai=ai,
        game_map=game_map,
    )
    return actor


def spawn_named_npc(
    npc_key: str,
    x: int,
    y: int,
    game_map: GameMap,
) -> Optional[Actor]:
    """
    Phase 13: Spawn a named NPC from data/npcs.json at the given position.
    Uses BossAI for bosses, HostileEnemy for rivals/contacts.
    """
    import json, os
    path = os.path.join(os.path.dirname(__file__), "..", "data", "npcs.json")
    try:
        with open(path) as f:
            npcs = json.load(f)
    except Exception:
        return None

    data = npcs.get(npc_key)
    if not data:
        return None

    from components.ai.boss_ai import BossAI

    tier = data.get("tier", "contact")
    if tier == "boss":
        ai = BossAI(
            npc_key=npc_key,
            phase_threshold=data.get("phase_threshold", 0.5),
            phase_two_behavior=data.get("phase_two_behavior", "calls_reinforcements"),
        )
        is_boss = True
    else:
        ai = HostileEnemy()
        is_boss = False

    actor = Actor(
        x=x, y=y,
        char=data["char"],
        color=tuple(data["color"]),
        name=data["name"],
        fighter=Fighter(
            max_hp=data["hp"],
            hp=data["hp"],
            base_attack=data["attack"],
            base_defense=data["defense"],
        ),
        inventory=Inventory(capacity=4),
        ai=ai,
        game_map=game_map,
        npc_key=npc_key,
        is_boss=is_boss,
    )
    return actor


def populate_map(
    game_map: GameMap,
    rooms: list,
    rng: random.Random,
    max_enemies_per_room: int = 2,
) -> None:
    """Scatter enemies across rooms (skip room 0 — player start)."""
    from world.map_gen import Room
    for room in rooms[1:]:
        num_enemies = rng.randint(0, max_enemies_per_room)
        for _ in range(num_enemies):
            cx, cy = room.center
            ex = rng.randint(room.x + 1, room.x + room.width - 2)
            ey = rng.randint(room.y + 1, room.y + room.height - 2)
            if game_map.get_blocking_entity_at(ex, ey):
                continue
            weights = [50, 10, 30, 10]
            keys = ["rival_goon", "made_man", "beat_cop", "detective"]
            chosen = rng.choices(keys, weights=weights, k=1)[0]
            patrol_pts = [room.center, (cx + 2, cy)] if chosen == "beat_cop" else None
            spawn_enemy(chosen, ex, ey, game_map, patrol_points=patrol_pts)
