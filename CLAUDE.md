# CLAUDE.md — Whiskey Hollow Developer Guide

> Fast-load reference for Claude Code. Read this before touching any file.

---

## Run Command

```bash
python main.py
```

Native tcod window — no HTTP server, no build step. All imports are relative to the project root.

---

## Current State

- **Phases 1–16 complete.** Fully playable from character creation through win/loss.
- **Active branch:** `phase2`
- **Python 3.11 + tcod 18.x**

---

## Key Architecture

```
main.py
  └─ run_main_menu()          → New Game / Continue / Quit
       └─ run_game_loop()     → Engine.render() + EventHandler.handle_events()
            ├─ EventHandler   → translates tcod key events → engine calls
            ├─ Engine         → owns ALL state (player, game_map, cash, heat, crew, etc.)
            ├─ GameMap        → tiles (numpy), entities, FOV
            └─ Actor          → owns Fighter + AI + Inventory as component attributes
```

Exceptions control flow: `PlayerDead` and `PlayerWon` exit the game loop. `QuitGame` exits cleanly.

---

## Critical File Index

| File | Purpose | Added |
|------|---------|-------|
| `main.py` | Entry point, tileset loading, game loop, win/loss | Ph 1 |
| `constants.py` | All magic numbers, screen dims, tileset config | Ph 1 |
| `engine/engine.py` | Game state, FOV, enemy turns, level, save_game() | Ph 1 |
| `engine/event_handler.py` | All keybinds → EventHandler.handle_key() | Ph 1 |
| `engine/save_load.py` | save_game / load_game / list_saves / delete_save | Ph 14 |
| `engine/meta.py` | Meta-progression (run-end unlocks → data/meta_save.json) | Ph 10 |
| `engine/exceptions.py` | QuitGame, Impossible, PlayerDead, PlayerWon | Ph 1 |
| `world/game_map.py` | GameMap: tiles, entities, FOV, pathfinding, serialization | Ph 1 |
| `world/map_gen.py` | BSP procedural room generation | Ph 1 |
| `world/tile_types.py` | Tile defs: FLOOR, WALL, DOOR, BAR_COUNTER, CRATE | Ph 1/12 |
| `world/locations.py` | STATIC_MAPS registry + load_static_map() | Ph 12 |
| `entities/actor.py` | Actor class, player_from_dict(), npc_key, is_boss, perks | Ph 1 |
| `entities/stats.py` | Stats dataclass (STR/DEX/INT/CHA/LUCK + D&D modifiers) | Ph 1 |
| `entities/character_class.py` | 4 class defs with starting_perk | Ph 1 |
| `entities/perks.py` | PERKS registry, has_perk(), get_perk_options() | Ph 16 |
| `entities/spawner.py` | spawn_entity, spawn_named_npc() | Ph 1/13 |
| `components/fighter.py` | HP, attack, defense, serialization | Ph 1 |
| `components/faction_standing.py` | Rep per faction, rank perks, serialization | Ph 3 |
| `components/crew_member.py` | CrewMember + CrewRoster, serialization | Ph 4 |
| `components/ai/boss_ai.py` | Two-phase BossAI with dialog + reinforcements | Ph 13 |
| `components/ai/hostile_ai.py` | Standard enemy chase AI | Ph 2 |
| `components/ai/patrol_ai.py` | Beat cop patrol with KCPD rank perk check | Ph 2 |
| `combat/combat_engine.py` | resolve_attack() with D20 + all perk hooks | Ph 2 |
| `economy/heat.py` | Heat 0–100, thresholds, passive decay, perk hooks | Ph 2 |
| `economy/market.py` | sell_price(player) with district + perk mods | Ph 4 |
| `factions/job_board.py` | Job generation + resolve_job_success() + perk hooks | Ph 3 |
| `factions/reputation.py` | Rank titles, thresholds, rank perk strings | Ph 3 |
| `factions/crew_pool.py` | Hireable crew roster per faction | Ph 4 |
| `ui/panels.py` | 4-panel layout: status, crew, message log, faction rep | Ph 1 |
| `ui/menus.py` | All blocking menus: crew, faction, skill, help, perks, main | Ph 1 |
| `ui/dialogue.py` | Blocking NPC dialogue overlay | Ph 13 |
| `ui/game_over.py` | Death + victory screens | Ph 1 |
| `ui/message_log.py` | Scrolling log with word-wrap | Ph 1 |
| `ui/color.py` | Named color constants (noir/sepia palette) | Ph 1 |
| `data/perks.json` | 24 perks across 4 categories | Ph 16 |
| `data/npcs.json` | 10 named NPCs (bosses + contacts) | Ph 13 |
| `data/maps/*.json` | 4 authored KC location maps | Ph 12 |
| `data/random_tables.json` | d100 encounter tables | Ph 1 |
| `data/names_kc.json` | Period-appropriate KC names | Ph 1 |

---

## tcod 18 API Gotchas

```python
# CORRECT tileset loading
tcod.tileset.load_tilesheet(path, cols, rows, tcod.tileset.CHARMAP_CP437)
tcod.tileset.load_truetype_font(path, tile_w, tile_h)

# WRONG — does NOT exist in tcod 18
tcod.tileset.load_default()   # AttributeError

# FOV constant — must go through libtcodpy
from tcod import libtcodpy
libtcodpy.FOV_SYMMETRIC_SHADOWCAST

# Tiles are numpy structured arrays
tile_dt = np.dtype([("walkable", bool), ("transparent", bool),
                    ("dark", tile_graphic), ("light", tile_graphic)])

# CP437 tilesheet mapping
tcod.tileset.CHARMAP_CP437

# Context presentation
context.present(console)   # NOT context.present_console(console)
```

---

## Coding Conventions

- **Composition over inheritance** — Actor owns Fighter + AI + Inventory as attributes
- **No global mutable state** — everything lives on `engine` or `actor`
- **Serialization contract** — every serializable class has `to_dict()` + `from_dict()`
- **JSON-driven data** — perks, NPCs, maps, names, random tables all in `data/`
- **Perk check pattern** — `has_perk(actor, key) → bool` at every callsite
- **Level is computed, never stored** — `engine._get_player_level()` from jobs + rep
- **RNG** — always use `engine.rng` (seeded `random.Random`), never `random` directly
- **Heat/combat resolution** — check perk hooks at the END of the function, after base logic

---

## System Interactions

```
combat_engine.resolve_attack()
  → Iron Fists perk (+2 unarmed)
  → Deadeye perk (+2 ranged)
  → Streetfighter perk (lower crit threshold)
  → River Market rank perk (+10% damage)
  → Sucker Punch perk (+3 first hit)
  → Blood Money perk (+$10 on kill)

economy/heat.py
  → Ghost perk (-25% combat heat)
  → Pendergast rank perk (heat floor)
  → Friends in Low Places perk (+5 decay/turn)
  → Crooked Badge perk (raid threshold +15)

factions/job_board.resolve_job_success()
  → Union Station rank perk (+10% cash)
  → Numbers Runner perk (+20% delivery)
  → Nest Egg perk (+$25/job)
  → Natural Politician perk (+10% rep)
  → Good Boss perk (+10 crew loyalty)

economy/market.sell_price(player)
  → Jazz District rank perk (+15%)
  → Black Market perk (+15%)
```

---

## What NOT to Do

| Don't | Why |
|-------|-----|
| Call `tcod.tileset.load_default()` | Doesn't exist in tcod 18 |
| Store player level | Always computed via `engine._get_player_level()` |
| Add module-level globals | Everything goes on `engine` or `actor` |
| Skip `to_dict()`/`from_dict()` on new serializable classes | Breaks save/load silently |
| Use bare `random` module | Use `engine.rng` for reproducibility |
| Read `data/npcs.json` directly outside of `dialogue.py` / `boss_ai.py` | Use `spawn_named_npc()` or `_load_npc_data()` |
| Hardcode colors inline | Use named constants from `ui/color.py` |

---

## Keybinds (all implemented)

| Key | Action |
|-----|--------|
| Arrows / Numpad / vi-keys (hjklyubn) | Move / attack |
| `.` or Numpad 5 | Wait (pass turn) |
| `c` | Crew menu |
| `f` | Faction / job board |
| `s` | Skill point allocation |
| `p` | Perk viewer |
| `v` | Vanish (perk ability — reset heat once) |
| `Ctrl+S` | Quick save (slot 0) |
| `?` (Shift+/) | Help screen |
| `Esc` | Quit game |

---

## Save System

- Save files: `saves/slot_0.json`, `saves/slot_1.json`, `saves/slot_2.json`
- API: `engine.save_game(slot=0)` / `save_load.load_game(slot=0)`
- Save auto-deleted on death or win (`save_load.delete_save(slot)`)
- Numpy tile arrays serialized as nested lists; RNG state via `getstate()`/`setstate()`

---

## Static Maps

Four authored KC maps in `data/maps/`:

| Key | File | Boss |
|-----|------|------|
| `union_station_interior` | union_station_interior.json | Big Jim Torrio |
| `the_blue_room` | the_blue_room.json | Dutch Malone |
| `river_market_warehouse` | river_market_warehouse.json | The Ox |
| `kcpd_precinct` | kcpd_precinct.json | Captain Morrison |

Load via `world.locations.load_static_map(key)` → returns `(GameMap, spawn_data_dict)`.
