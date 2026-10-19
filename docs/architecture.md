---
title: Architecture
---

[← Home](index.md)

# Architecture

This page explains how the code is organized, for anyone who wants to read it, fix it, or mod it.

## Stack

| Layer | Choice |
|---|---|
| Language | Python 3.11+ |
| Engine | [python-tcod](https://github.com/libtcod/python-tcod): window, input, console rendering, FOV, pathfinding, BSP |
| Map data | numpy structured arrays |
| Game data | JSON files in `data/` |
| Saves | JSON |
| Tooling | `pytest`, `ruff`, `mypy` |

## Layout

```
whiskeyhollow/
├── main.py            Entry point: tileset loading, new_game(), main loop
├── constants.py       All tunable numbers: screen size, heat thresholds, rep ranks, win conditions
├── engine/            Game loop, input handling, save/load, meta-progression
├── world/             Map generation (BSP), tile types, FOV, named locations
├── entities/          Entity/Actor/Item, character classes, stats, perks, spawning
├── components/        Fighter, inventory, crew member, faction standing, AI behaviors
├── factions/          Faction definitions, reputation and ranks, job board, crew hiring pool
├── combat/            Attack resolution and weapon definitions
├── economy/           Contraband, market prices, heat
├── ui/                Panels, menus, message log, dialogue overlay, color palette
└── data/              JSON: perks, NPCs, economy, names, random tables, static maps
```

## Main ideas

### A lightweight entity–component setup
Entities are Python dataclasses that hold components as plain attributes (`fighter`, `ai`, `inventory`, `crew_member`, `faction_standing`). There's no separate ECS framework. Behavior is built by composition rather than deep inheritance.

### Data lives in JSON
Anything that can live in JSON does: perks (`data/perks.json`), named NPCs and their dialogue (`data/npcs.json`), economy tuning (`data/economy.json`), period names (`data/names_kc.json`), and hand-built maps (`data/maps/*.json`). Usually you can add content without changing any Python.

### Randomness is seeded and comes from tables
Each run starts from one seed, and all randomness uses `engine.rng`. Random outcomes are rolled on d100 tables in `data/random_tables.json`:

```json
{
  "encounter_westbottoms_night": [
    {"range": [1, 20],   "result": "beat_cop_patrol"},
    {"range": [21, 50],  "result": "rival_goon_2"},
    {"range": [51, 75],  "result": "nothing"},
    {"range": [76, 95],  "result": "drunk_civilian"},
    {"range": [96, 100], "result": "made_man_ambush"}
  ]
}
```

Every roll should produce something that shows up in the message log.

### Tiles
Tiles are stored in a numpy structured array with `walkable`, `transparent`, `dark`, and `light` fields. FOV comes from `tcod.map.compute_fov` and is only recomputed when the player moves. Rendering writes straight into `console.rgb`.

### Hand-built maps
Files in `data/maps/` contain a `char_map` that maps each character to a tile type (for example `"#": "wall"`), plus `spawn_points` for the player, NPCs, and objectives.

### Boss AI
`components/ai/boss_ai.py` gives bosses two phases. The switch happens at 50% HP, and the boss becomes more aggressive and uses special abilities. `ui/dialogue.py` shows NPC lines from `npcs.json` when the `on_meet`, `on_attack`, and `on_low_hp` events fire.

### Saving and loading
`engine/save_load.py` writes `saves/slot_N.json`:
- numpy arrays are saved with `.tolist()` and restored with `np.array(..., dtype=tile_dt)`
- RNG state is saved with `rng.getstate()`
- tcod objects such as consoles and contexts are never saved. They get recreated when a game loads

## Adding content

| You want to add… | Edit |
|---|---|
| A perk | `data/perks.json`. Add the logic in `entities/perks.py` if it needs a new `effect_target` |
| A named NPC | `data/npcs.json` |
| A random encounter | `data/random_tables.json` |
| A hand-built location | A new file in `data/maps/` |
| A balance change | `constants.py` |

## Coding conventions

- Type hints everywhere. Use dataclasses for data and regular classes for behavior.
- Put magic numbers in `constants.py`.
- Avoid global mutable state. Pass `engine` around instead.
- Write combat resolution as pure functions where you can.
- Fail loudly: raise a descriptive exception instead of failing silently.
