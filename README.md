# Whiskey Hollow

*A Prohibition-era roguelike set in 1920s Kansas City.*

Run a bootlegging operation, build a crew, climb the faction ladder, and survive the heat — all from a terminal window. Built with Python 3.11 and [tcod](https://python-tcod.readthedocs.io/).

---

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

No build step. No HTTP server. Just a native tcod window. The game automatically saves to `saves/slot_0.json` with **Ctrl+S**. A "Continue" option appears on the main menu when a save exists.

### Optional: CP437 Bitmap Tileset

By default the game uses a system monospace font (SF Mono on macOS, Andale Mono as fallback). To enable a classic roguelike tilesheet:

1. Download a free CP437 bitmap font — [Potash 10×10](https://dwarffortresswiki.org/Tileset_repository) works well
2. Place it at `data/tiles/Potash_10x10.png` (or change `TILESET_PATH` in `constants.py`)
3. Set `USE_TILESHEET = True` in `constants.py`

The game uses the same character codes either way — flipping the tileset requires no code changes.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Roguelike Engine | `tcod` 18.x (python-tcod) |
| Rendering | `tcod` console + context |
| Map Generation | Custom BSP via `world/map_gen.py` |
| Data / State | Python dataclasses + JSON |
| Save System | JSON files in `saves/` |
| Randomness | Seeded `random.Random` on `engine.rng` |
| Package Mgmt | `pip` + `requirements.txt` |

---

## Project Structure

```
whiskeyhollow/
├── CLAUDE.md                    # Developer quick-reference for Claude Code
├── README.md
├── requirements.txt
├── constants.py                 # All magic numbers + tileset config
├── main.py                      # Entry point → main menu → game loop
│
├── engine/
│   ├── engine.py                # All game state; render, FOV, enemy turns
│   ├── event_handler.py         # Key events → game actions
│   ├── save_load.py             # save_game / load_game / delete_save
│   ├── meta.py                  # Run-end meta-progression (meta_save.json)
│   └── exceptions.py            # QuitGame, Impossible, PlayerDead, PlayerWon
│
├── world/
│   ├── map_gen.py               # BSP procedural room/corridor generation
│   ├── game_map.py              # GameMap: tiles (numpy), entities, FOV
│   ├── tile_types.py            # FLOOR, WALL, DOOR, BAR_COUNTER, CRATE
│   └── locations.py             # STATIC_MAPS registry + load_static_map()
│
├── entities/
│   ├── actor.py                 # Actor: Fighter + AI + Inventory + perks
│   ├── entity.py                # Base Entity (x, y, char, color, name)
│   ├── stats.py                 # Stats dataclass (STR/DEX/INT/CHA/LUCK)
│   ├── character_class.py       # 4 playable classes + starting perk
│   ├── perks.py                 # PERKS registry, has_perk(), get_perk_options()
│   ├── item.py                  # Item entity
│   └── spawner.py               # spawn_entity(), spawn_named_npc()
│
├── components/
│   ├── fighter.py               # HP, base_attack, base_defense
│   ├── inventory.py             # Item list
│   ├── crew_member.py           # CrewMember + CrewRoster
│   ├── faction_standing.py      # Rep per faction, rank perks
│   └── ai/
│       ├── base_ai.py           # BaseAI + get_path_to()
│       ├── hostile_ai.py        # Standard enemy chase
│       ├── patrol_ai.py         # Beat cop patrol (KCPD rank perk aware)
│       ├── friendly_ai.py       # Crew follower
│       └── boss_ai.py           # Two-phase boss (taunts + reinforcements)
│
├── factions/
│   ├── faction.py               # Faction dataclass
│   ├── faction_data.py          # Five faction definitions
│   ├── job_board.py             # Job generation + resolution + perk hooks
│   ├── reputation.py            # Rank titles, thresholds, rank perk strings
│   └── crew_pool.py             # Hireable crew roster per faction
│
├── combat/
│   ├── combat_engine.py         # resolve_attack(): D20 + perk hooks
│   └── weapons.py               # Weapon definitions
│
├── economy/
│   ├── heat.py                  # Heat 0–100, patrol/raid thresholds, decay
│   ├── market.py                # sell_price() with district + perk mods
│   └── contraband.py            # Contraband good definitions
│
├── ui/
│   ├── panels.py                # 4-panel layout render
│   ├── menus.py                 # All blocking menus (crew, faction, perks…)
│   ├── dialogue.py              # NPC dialogue overlay
│   ├── message_log.py           # Scrolling log with word-wrap
│   ├── game_over.py             # Death + victory screens
│   └── color.py                 # Named color constants (noir/sepia palette)
│
├── data/
│   ├── perks.json               # 24 perks across 4 categories
│   ├── npcs.json                # 10 named NPCs (bosses + contacts)
│   ├── random_tables.json       # d100 encounter tables
│   ├── names_kc.json            # Period KC name lists
│   ├── economy.json             # Contraband base prices
│   ├── maps/                    # 4 authored KC location maps
│   │   ├── union_station_interior.json
│   │   ├── the_blue_room.json
│   │   ├── river_market_warehouse.json
│   │   └── kcpd_precinct.json
│   └── tiles/                   # Drop a CP437 PNG here to enable tilesheet
│
├── saves/                       # slot_0.json, slot_1.json, slot_2.json
└── tests/
```

---

## Core Systems

### Character Classes

Four playable classes, each with a locked **starting perk** and a **chosen perk** selected at creation:

| Class | Starting Perk | Flavor |
|---|---|---|
| **Brawler** | Iron Fists | +2 unarmed attack; takes hits, dishes them back |
| **Con Man** | Silk Tongue | +3 bribery; talks his way in and out |
| **Smuggler** | Numbers Runner | +20% delivery pay; moves product, fast |
| **Fixer** | Friends in Low Places | +5 heat decay/turn; knows everybody |

Stats use D&D modifiers (score 3–18, modifier −4 to +4). Spend skill points with **`s`** each level.

---

### Perk System

24 perks across four categories, all mechanically active:

| Category | Examples |
|---|---|
| **Combat** | Iron Fists, Deadeye, Streetfighter, Hard Boiled, Sucker Punch, Blood Money |
| **Economy** | Black Market, Silk Tongue, Numbers Runner, Nest Egg |
| **Shadow** | Ghost, Crooked Badge, Vanish, Friends in Low Places |
| **Influence** | Natural Politician, Street Rep, Made Man, Good Boss |

You get **1 auto perk** (class-locked) + **1 chosen perk** at character creation. Further perks unlock at level-up. Level-up automatically opens the perk selection screen. View your perks anytime with **`p`**.

---

### Factions

Five factions with independent reputation tracks (0–100). Rising in one can damage standing in another.

| Faction | Theme | Home District |
|---|---|---|
| **Pendergast Machine** | Political power, city hall | Downtown |
| **Union Station Crew** | Smuggling via rail and truck | Union Station |
| **River Market Syndicate** | Warehousing, wholesale muscle | River Market |
| **Jazz District Co.** | Speakeasies, front businesses | 18th & Vine |
| **Kansas City PD** | Corrupt cops, protection rackets | West Bottoms |

Rank thresholds: 10 (Street Runner) → 25 (Associate) → 45 (Soldier) → 65 (Capo) → 85 (Boss). Each rank unlocks a mechanical bonus, not just a title.

---

### Jobs

Seven job types resolved probabilistically, modified by stats, perks, and crew:

`delivery` · `heist` · `intimidation` · `protection` · `bribery` · `assassination` · `intel`

Rewards: cash, rep, crew loyalty. Failure consequences: heat increase, rep loss, crew injury.

---

### Heat & Economy

- **Heat** (0–100): rises from combat and failed jobs. At 50+ cops begin patrolling more aggressively; at 80+ raids trigger. Reduce heat by laying low, bribing officials, or using the **Vanish** perk (`v`) once per run.
- **Market prices** fluctuate by district. The Jazz District Co.'s Capo rank perk and the Black Market perk each add +15% to sell prices.
- **Cash** is tracked on `engine.cash`. Win condition: retire with **$50,000**.

---

### Crew

Up to 4 crew members. Each has a role, loyalty (0–100), wage, and status.

| Role | Bonus |
|---|---|
| Muscle | Combat power |
| Driver | Delivery speed, escape chance |
| Lookout | Heat reduction, early warning |
| Fixer | Bribery success, cop heat management |

Hire from faction crew pools via the crew menu (**`c`**). Crew wages auto-deduct each job.

---

### Named NPCs & Boss Encounters

Ten named characters in `data/npcs.json`. Bosses use a two-phase AI:

- **Phase 1** (HP > threshold): Aggressive chase + combat taunts in the message log
- **Phase 2** (HP ≤ threshold): Either **calls reinforcements** (spawns 2 goons) or goes **berserk** (+2 attack)

| Boss | Faction | Phase 2 |
|---|---|---|
| Big Jim Torrio | Union Station Crew | Reinforcements |
| The Ox | River Market Syndicate | Berserk |
| Dutch Malone | Jazz District Co. | Reinforcements |
| Captain Morrison | KCPD | Reinforcements |
| Tom Pendergast | Pendergast Machine | Reinforcements |

Contacts (Ward Captain Higgins, Sal the Driver, Dago DeLuca, Mama Dolores, Detective Flynn) give dialogue on meet and job completion.

---

### Static Maps

Four authored Kansas City locations with ASCII room layouts, NPC spawn points, and objectives:

| Map | Location |
|---|---|
| `union_station_interior` | Union Station — rail concourse + crew offices |
| `the_blue_room` | Jazz speakeasy — bar, stage, back room |
| `river_market_warehouse` | Syndicate warehouse — crate rows + office |
| `kcpd_precinct` | Police precinct — lobby, bullpen, cells, evidence room |

---

### Save / Load

- **Ctrl+S** — quick save to slot 0 during play
- **Continue** — on the main menu, loads the most recent save
- 3 save slots (`saves/slot_0.json` through `saves/slot_2.json`), human-readable JSON
- Saves are automatically deleted when you die or win (true roguelike)

---

### Leveling

Level is computed live from jobs completed and total faction rep — it is never stored. When you level up, the perk selection screen opens automatically. Stats can be manually allocated at any time via **`s`**.

---

## UI Layout

```
┌────────────────────────────────────────────────────────────────────────┬────────────────────────────┐
│                                                                        │  PLAYER STATUS             │
│                                                                        │  Jack Malone  Lv 4         │
│                        GAME MAP                                        │  Brawler  [Iron Fists]     │
│                        (72 × 38 tiles)                                 │  HP: 45/60                 │
│                                                                        │  Cash: $1,240              │
│                                                                        │  Heat: 34%                 │
│                                                                        │  Perks: 3                  │
│                                                                        ├────────────────────────────┤
│                                                                        │  CREW                      │
│                                                                        │  > Sal (Muscle)            │
│                                                                        │  > Rita (Fixer)            │
├────────────────────────────────────────────────────────────────────────┼────────────────────────────┤
│  MESSAGE LOG                                                           │  FACTION REP               │
│  > You move 3 cases of whiskey north                                   │  Pendergast:    42         │
│  > Sal floors a rival goon                                             │  Union Station: 17         │
│  > Heat +5 (gunshot heard nearby)                                      │  River Market:   8         │
│  > Big Jim Torrio: "Nobody crosses the Crew and walks out alive!"      │  Jazz District: 61 ★       │
└────────────────────────────────────────────────────────────────────────┴────────────────────────────┘
```

Screen: 100 × 55 cells. Map viewport: 72 × 38. Right panel: 28 wide.

---

## Keybinds

| Key | Action |
|---|---|
| Arrow keys / Numpad / vi-keys (hjklyubn) | Move / attack adjacent enemy |
| `.` or Numpad 5 | Wait (pass turn) |
| `c` | Crew menu |
| `f` | Faction board / take job |
| `s` | Allocate skill points |
| `p` | View perks |
| `v` | Vanish — reset heat to 0 (once per run, requires perk) |
| `Ctrl+S` | Quick save (slot 0) |
| `?` (Shift+/) | Help screen |
| `Esc` | Quit |

---

## Win Conditions

| Condition | Requirement |
|---|---|
| **Retire rich** | Accumulate $50,000 cash |
| **Crime boss** | Reach Boss rank (85+ rep) in any faction AND control 3+ districts |

Death is permanent. Each run starts fresh with a new character. Meta-progression unlocks (stored in `data/meta_save.json`) carry forward between runs.

---

## Development Phases

### ✅ Phases 1–10 — Core Game

- tcod window, console rendering, message log
- Player movement, FOV via `libtcodpy.FOV_SYMMETRIC_SHADOWCAST`
- BSP procedural map generation
- D20 combat engine with crits and period flavor text
- ECS-lite actor/component system
- Five factions with rep ladder, job board, 7 job types
- Crew system (4 max, 4 roles, loyalty, wages)
- Heat system (0–100, patrol/raid thresholds)
- Market price fluctuation per district
- Win/loss conditions, death screen, victory screen, meta-progression

### ✅ Phases 11–16 — Polish

- **Phase 11** — CP437 bitmap tilesheet support (`USE_TILESHEET` toggle in `constants.py`)
- **Phase 12** — Four authored static KC maps with objectives and NPC spawn points
- **Phase 13** — Ten named NPCs, two-phase boss AI, blocking dialogue overlay
- **Phase 14** — Full JSON save/load (`saves/slot_N.json`), main menu with Continue
- **Phase 15** — Live level computation, automatic level-up perk screen, faction rank perks now mechanically active
- **Phase 16** — 24-perk system (4 categories), class starting perks, perk hooks throughout all systems

### Future: Phase 17+

TBD — candidates include an overworld city map, additional authored locations, crew combat AI on the tile map, faction war events, and sound.

---

## Historical Flavor

Kansas City in the 1920s was one of the most wide-open cities in America:

- **Tom Pendergast** ran the city through his political machine — every judge, cop, and ward captain answered to him
- **18th & Vine** was the heart of the jazz scene; speakeasies were dense and brazen
- **Union Station** (1914) was a major rail hub — ideal for moving product
- **West Bottoms** — industrial meatpacking district, home to warehouses and rough work
- **River Market** — old commercial waterfront near the Missouri River

**Period weapons**: .38 revolver, M1911 pistol, Winchester shotgun, Thompson submachine gun (Tommy gun), sawed-off, blackjack, straight razor.

**Period slang** used in the message log: *hooch, giggle water, bulls (cops), the feds, torpedo (hitman), gat (gun), on the lam, blind pig.*

---

*Inspirations: Peaky Blinders · Boardwalk Empire · Miller's Crossing · Road to Perdition · Mafia · Dwarf Fortress*
