# Whiskey Hollow: A Kansas City Bootlegger Roguelike

## Project Overview

**Whiskey Hollow** is a roguelike RPG set in Prohibition-era Kansas City (1920–1933), built in Python using the TCOD (libtcod) library. The player runs a bootlegging operation, manages a crew, moves contraband, fights rival gangs and cops, and climbs the ranks of organized crime through faction allegiance and completed jobs.

Primary inspirations: *Peaky Blinders*, *Boardwalk Empire*, *Road to Perdition*, *Miller's Crossing*. *Mafia*, *Grand Theft Auto*, *Dwarf Fortress*, *Rogue*

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Roguelike Engine | `tcod` (python-tcod) |
| Input/Rendering | `tcod` event loop + console |
| Data / State | Python dataclasses + JSON serialization |
| Save System | JSON files (human-readable saves) |
| Procedural Gen | Custom Python (seeded `random` / `numpy`) |
| Testing | `pytest` |
| Linting | `ruff` + `mypy` |
| Package Mgmt | `uv` or `pip` with `requirements.txt` |

---

## Project Structure

```
whiskeyhollow/
├── CLAUDE.md                   # This file
├── README.md
├── requirements.txt
├── main.py                     # Entry point
│
├── engine/
│   ├── __init__.py
│   ├── engine.py               # Core game loop, state machine
│   ├── event_handler.py        # Input handling (tcod events)
│   ├── renderer.py             # All tcod rendering logic
│   └── exceptions.py           # Custom exceptions (QuitGame, etc.)
│
├── world/
│   ├── __init__.py
│   ├── map_gen.py              # Procedural map generation
│   ├── tile_types.py           # Tile definitions (floor, wall, door, etc.)
│   ├── game_map.py             # GameMap class, FOV, pathfinding
│   └── locations.py            # Named KC locations (speakeasy, warehouse, etc.)
│
├── entities/
│   ├── __init__.py
│   ├── entity.py               # Base Entity class
│   ├── actor.py                # Actors (player, NPCs, enemies)
│   ├── item.py                 # Items (booze, weapons, cash, evidence)
│   └── spawner.py              # Procedural entity/enemy spawning
│
├── components/
│   ├── __init__.py
│   ├── fighter.py              # Combat stats (HP, attack, defense)
│   ├── inventory.py            # Item management
│   ├── crew_member.py          # Crew/party member component
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── base_ai.py          # Base AI class
│   │   ├── hostile_ai.py       # Enemy AI (cops, rival gang)
│   │   ├── friendly_ai.py      # Crew follower AI
│   │   └── patrol_ai.py        # Patrol patterns (beat cops)
│   └── faction_standing.py     # Faction rep tracker
│
├── factions/
│   ├── __init__.py
│   ├── faction.py              # Faction class
│   ├── faction_data.py         # Static faction definitions
│   ├── job_board.py            # Procedural job generation
│   └── reputation.py           # Rep thresholds, rank titles, perks
│
├── combat/
│   ├── __init__.py
│   ├── combat_engine.py        # Turn-based combat resolution
│   ├── weapons.py              # Weapon definitions & stats
│   └── encounter_table.py      # Random encounter tables
│
├── economy/
│   ├── __init__.py
│   ├── contraband.py           # Goods: whiskey, gin, beer, etc.
│   ├── market.py               # Price fluctuation, supply/demand
│   ├── heat.py                 # Police heat / wanted level
│   └── transaction.py          # Buy/sell/transport logic
│
├── ui/
│   ├── __init__.py
│   ├── panels.py               # Side panels, status bars
│   ├── menus.py                # Inventory, crew, faction menus
│   ├── message_log.py          # In-game message log
│   └── color.py                # Color palette (sepia/noir theme)
│
├── data/
│   ├── tiles.png               # Tileset (or use tcod default)
│   ├── factions.json           # Faction definitions
│   ├── jobs.json               # Job templates
│   ├── names_kc.json           # Period-appropriate KC name lists
│   └── random_tables.json      # D&D-style random tables
│
├── saves/
│   └── .gitkeep
│
└── tests/
    ├── test_combat.py
    ├── test_economy.py
    ├── test_factions.py
    └── test_map_gen.py
```

---

## Core Game Systems

### 1. Map & World

- **City Map Layer**: Overworld Kansas City grid. Districts include River Market (warehouses), West Bottoms (industrial), 18th & Vine (jazz clubs / speakeasies), Union Station area, Westport.
- **Dungeon-Style Locations**: Each location (warehouse, speakeasy, police precinct, rival gang HQ) is procedurally generated per visit using BSP room/corridor generation via `tcod.bsp`.
- **Tile Types**: Floor, wall, door (locked/unlocked), window, bar counter, crate, vault.
- **FOV**: Standard raycasting FOV via `tcod.map.compute_fov`. Darkness matters — sneak jobs use vision strategically.

### 2. Entity Component System (ECS-lite)

Entities own components as Python dataclass attributes. Keep it simple — no full ECS framework.

```python
# Example pattern
@dataclass
class Actor(Entity):
    fighter: Fighter
    ai: BaseAI | None
    inventory: Inventory
    crew_member: CrewMember | None = None
```

### 3. Factions

Five major factions. Each has:
- `name`, `description`, `color` (for UI)
- `rep_levels`: list of rank titles with thresholds (0–100 rep scale)
- `job_pool`: list of job template keys
- `enemies`: list of hostile faction names
- `home_district`: primary KC district

| Faction | Theme | Archetype |
|---|---|---|
| **Pendergast Machine** | Political / City Hall | The bosses who run KC |
| **Union Station Crew** | Smuggling / Transport | Move product via rail & trucks |
| **River Market Syndicate** | Warehousing / Wholesale | Supply chain & muscle |
| **The Jazz District Co.** | Speakeasies / Front Businesses | Money laundering, influence |
| **Kansas City PD (Corrupt)** | Law / Protection Rackets | Pay them off or fight them |

> Factions have relations with each other. Rising in one may damage standing in another.

### 4. Jobs System

Jobs are the core progression loop. Generated procedurally from templates in `jobs.json`.

**Job Types:**
- `delivery` — Move contraband from A to B without being caught
- `heist` — Rob a rival shipment or cash stash
- `intimidation` — Rough up a target (combat-likely)
- `protection` — Guard a location for N turns against waves
- `bribery` — Navigate a social encounter to pay off a cop/official
- `assassination` — Take out a named rival (high risk/reward)
- `intel` — Scout a rival location and return

**Job Rewards:** Cash, rep with faction, rare items, crew unlocks, territory control.

**Job Failure Consequences:** Heat increase, rep loss, crew injury/death, enemy faction aggression.

### 5. Economy & Heat

- **Contraband types**: Whiskey (high value), Beer (bulk), Gin (quick sale), Medicinal Alcohol (low heat)
- **Market prices** fluctuate by district and by a `market_turn_timer`
- **Heat Level** (0–100): Increases from combat, failed jobs, loud movement. High heat triggers cop patrols and raids. Reduce heat via bribes, laying low, or killing witnesses.
- **Cash** is the universal currency. Track it carefully.

### 6. Combat

Turn-based, tile-based. Inspired by classic roguelikes.

- **Melee**: Fists, knives, brass knuckles, Tommy guns (close range)
- **Ranged**: Pistols, shotguns, Tommy guns — line-of-sight required
- **Crew Combat**: Crew members act on player's turn cycle as friendlies
- **Enemy Types**: Beat Cops (patrol, call backup), Detectives (smart AI, investigate), Rival Goons (aggressive), Made Men (tough, high stats), Mob Bosses (boss fights)
- **Stealth Option**: Moving through shadows (non-FOV tiles of enemies) avoids triggering hostiles on non-combat jobs

### 7. Crew System

The player can recruit and manage up to 4 crew members.

```python
@dataclass
class CrewMember:
    role: str           # "Driver", "Muscle", "Lookout", "Fixer"
    loyalty: int        # 0-100, affects reliability
    skills: dict        # e.g. {"combat": 3, "stealth": 1, "driving": 5}
    wage: int           # Weekly upkeep cost
    status: str         # "available", "injured", "arrested", "dead"
```

**Roles:**
- **Muscle** — Combat bonus, intimidation jobs
- **Driver** — Delivery speed bonus, escape chance
- **Lookout** — Heat reduction, early enemy warning
- **Fixer** — Bribery success, reduces cop heat, jailbreaks arrested crew

### 8. Progression & Roguelike Loop

- **Death is permanent** (true roguelike). New run = new character, new seed.
- **Meta-progression** (optional): Unlock new starting faction allegiances or starting items via prior run achievements stored in a `meta_save.json`.
- **Win Condition**: Reach rank "Boss" in any faction AND control 3+ districts, OR accumulate $50,000 cash and retire.
- **Floor/Run Structure**: Each "chapter" is a set of jobs in a district. Completing a chapter advances the narrative and unlocks harder districts.

---

## Rendering & UI Layout

```
┌─────────────────────────────────┬───────────────────┐
│                                 │  PLAYER STATUS    │
│                                 │  HP: 45/60        │
│         GAME MAP                │  Cash: $1,240     │
│         (tcod console)          │  Heat: 34%        │
│                                 │  District: Bottoms│
│                                 ├───────────────────┤
│                                 │  CREW             │
│                                 │  > Sal (Muscle)   │
│                                 │  > Rita (Fixer)   │
├─────────────────────────────────┼───────────────────┤
│  MESSAGE LOG                    │  FACTION REP      │
│  > You move 3 cases of whiskey  │  Pendergast: 42   │
│  > Sal knocks out the guard     │  Syndicate: 17    │
│  > Heat +5 (gunshot heard)      │  Jazz Co.: 61 ★   │
└─────────────────────────────────┴───────────────────┘
```

- Use `tcod` root console with sub-consoles (blit pattern)
- Color palette: amber/sepia tones, dark backgrounds, red for danger
- All colors defined in `ui/color.py` as named constants

---

## Coding Conventions

### Python Style
- **Python 3.11+** — use `match/case`, `TypeAlias`, `Self` where appropriate
- Type hints on all functions and class attributes
- Dataclasses for data-heavy structures; regular classes for behavioral objects
- `@property` for derived stats (e.g., `total_attack = base_attack + weapon_bonus`)
- No global mutable state — pass `engine` or `game_map` as context

### File Conventions
- One primary class per file (exceptions for small helpers)
- All magic numbers go in `constants.py`
- JSON data files for all static game data (factions, jobs, names, random tables)
- `random_tables.json` follows d100 table format:

```json
{
  "encounter_westbottoms_night": [
    {"range": [1, 20], "result": "beat_cop_patrol"},
    {"range": [21, 50], "result": "rival_goon_2"},
    {"range": [51, 75], "result": "nothing"},
    {"range": [76, 95], "result": "drunk_civilian"},
    {"range": [96, 100], "result": "made_man_ambush"}
  ]
}
```

### TCOD Patterns
- Always use `tcod.context` for window management
- Tile data stored as structured numpy arrays (dtype with `walkable`, `transparent`, `dark`, `light` fields)
- Use `tcod.path.SimpleGraph` or `tcod.path.Pathfinder` for enemy pathfinding
- FOV recomputed each turn only when player moves

### Saving & Loading
- Game state serialized to JSON via `__dict__` + custom encoders for tcod/numpy types
- Save files in `saves/slot_N.json`
- `engine.save_game()` / `engine.load_game()` as primary interface

---

## Random Tables Design Philosophy

All randomness should be:
1. **Seeded** at run start (store seed in save file for reproducibility/debug)
2. **Table-driven** — avoid hardcoded random logic; roll against `random_tables.json`
3. **Weighted** — use `random.choices(population, weights)` pattern, not flat random
4. **Narratively meaningful** — every random result should produce a story beat in the message log

---

## Historical Flavor Notes

- Kansas City in the 1920s was dominated by the **Pendergast political machine** (Tom Pendergast ran the city)
- **18th & Vine** was a real jazz hub — speakeasies were thick here
- **Union Station** (1914) was a major transit hub — ideal for smuggling
- **West Bottoms** = industrial meatpacking district, great for warehouses
- **River Market** = old commercial district near Missouri River
- Period slang to use in message log: *hooch, giggle water, bulls (cops), heat, the feds, torpedo (hitman), gat (gun), speakeasy, blind pig, on the lam*
- Weapons: .38 revolver, 1911 pistol, Winchester shotgun, Thompson submachine gun (Tommy gun), sawed-off, blackjack, straight razor

---

## Development Phases

### Phase 1 — Skeleton (MVP)
- [ ] tcod window + basic map rendering
- [ ] Player movement + FOV
- [ ] Basic combat (player vs. 1 enemy)
- [ ] Message log
- [ ] Simple inventory

### Phase 2 — Core Loop
- [ ] Procedural map generation (BSP)
- [ ] Enemy AI (hostile + patrol)
- [ ] Items: weapons, contraband, cash
- [ ] Heat system
- [ ] Save/load

### Phase 3 — Factions & Jobs
- [ ] Faction data + rep system
- [ ] Job board + job resolution
- [ ] Faction rank progression
- [ ] Named NPCs per faction

### Phase 4 — Crew & Economy
- [ ] Crew recruitment & management
- [ ] Crew AI in combat
- [ ] Market price system
- [ ] Contraband transport loop

### Phase 5 — Polish & Roguelike Feel
- [ ] Procedural KC district names & flavor text
- [ ] Random encounter tables fully populated
- [ ] Meta-progression unlocks
- [ ] Win/loss conditions
- [ ] Multiple floors/chapters
- [ ] Boss encounters

---

## Key Commands (Default Keybinds)

| Key | Action |
|---|---|
| Arrow Keys / numpad | Move / attack |
| `g` | Pick up item |
| `i` | Open inventory |
| `c` | Open crew menu |
| `f` | Open faction/job board |
| `m` | Open city map |
| `>` | Descend / enter location |
| `<` | Exit location |
| `Esc` | Pause / main menu |
| `?` | Help |

---

## Claude Code Guidance

When implementing features, prefer:
- **Composition over inheritance** for entities
- **Data-driven design** — if it can be in JSON, put it in JSON
- **Small, testable functions** — combat resolution should be pure functions where possible
- **Explicit state** — avoid hidden side effects; mutations to `engine.game_map` or `actor.fighter` should be obvious at the call site
- **Fail loudly** — raise descriptive exceptions rather than silent failures

When generating new content (jobs, NPCs, encounters), always:
1. Check `random_tables.json` first — add new tables there
2. Use the seeded RNG from `engine.rng`
3. Log the result to `engine.message_log`