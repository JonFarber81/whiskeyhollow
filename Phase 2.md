Whiskey Hollow: Development Roadmap (Phases 11–16)
Phases 1–10 are complete. The game is fully playable end-to-end with 4 classes, BSP maps, 5 factions, and a crew system. The next 6 phases focus on graphical polish, world structure, narrative depth, and a robust RPG progression layer.

Architectural Context
Renderer: Uses console.rgb with numpy structs.

Tile Logic: For TTF, ch is a Unicode codepoint. For Tilesheets, ch is a tile index.

Current Gaps: Faction perks are text-only; Meta-progression unlocks are tracked but not yet applied to new runs.

Phase 11: Graphical Tileset
Scope: Medium

Goal: Replace standard TTF with a crisp, hand-crafted CP437 bitmap to maintain the noir aesthetic.

Implementation: Approach A (Hand-crafted CP437)

Why: Zero changes to tile_types.py or entity char fields. Maintains the "text-mode" feel while improving visual clarity.

Assets: Use Alloy_curses_12x12.png or Taffer_10x10.png.

Files to Modify

constants.py:

TILESET_PATH = "data/tiles/Alloy_curses_12x12.png"

TILESET_COLUMNS, TILESET_ROWS = 16, 16

USE_TILESHEET = True

main.py: Update _load_tileset() to handle tcod.tileset.load_tilesheet using tcod.tileset.CHARMAP_CP437.

Phase 12: Static Named Maps
Scope: Medium

Goal: Create authored, non-procedural locations for boss encounters and story beats.

Authoring 4 Initial Maps

Key	Name	Purpose
union_station_interior	Union Station	Crew boss encounter; smuggling delivery.
the_blue_room	The Blue Room	Jazz District speakeasy; social jobs.
river_market_warehouse	River Market	Syndicate HQ; heist objectives.
kcpd_precinct	KC Police Precinct	Assassination jobs; evidence room.
Map Data Structure (data/maps/*.json)

Maps are stored as JSON with a char_map (e.g., "#": "wall") and spawn_points for the player, NPCs, and objectives.

Phase 13: Named NPCs and Boss Encounters
Scope: Large

Goal: Introduce unique characters with specific dialogue and multi-phase AI.

Boss AI Logic

Phase 1: Tactical movement and smart chasing.

Transition: Triggered at 50% HP (e.g., "Big Jim Torrio" calls reinforcements).

Phase 2: Increased aggression and special ability usage.

Dialogue System

Located in ui/dialogue.py.

A blocking overlay that pulls lines from data/npcs.json based on events (on_meet, on_attack, on_low_hp).

Phase 14: Save / Load System
Scope: Medium

Goal: Implement a human-readable JSON serialization system.

Serialization Rules

Numpy Arrays: Convert to .tolist() for JSON; restore via np.array(..., dtype=tile_dt).

RNG: Save state via rng.getstate().

Exclusions: Never serialize tcod objects (consoles, contexts); recreate them on load.

Save File Structure

Stored in saves/slot_N.json. Contains global state (heat, cash), player stats, inventory, crew status, and the current map state.

Phase 15: Leveling and Progression
Scope: Medium

Goal: Move from "flat" stats to a dynamic Level 1–10 system.

The Level Formula

Level is a computed property based on total reputation and jobs completed:

Level=1+ 
50
TotalRep
​	
 + 
5
JobsCompleted
​	
 
Faction Rank Perk Hooks

Mechanical implementation of previously "text-only" perks:

Pendergast (Soldier): Heat decays 10% faster.

Jazz District (Barfly): +15% sell price.

KCPD (Protected): Cops ignore player at Heat < 50.

Phase 16: Perk System
Scope: Large

Goal: A pool of 24 unique perks categorized by Combat, Economy, Shadow, and Influence.

Perk Categories

Combat: e.g., Sucker Punch (+3 damage on the first attack of a fight).

Economy: e.g., Black Market (Sell contraband 15% above market price).

Shadow: e.g., Vanish (Once per run, instantly reset Heat to 0).

Influence: e.g., Made Man (Immune to rep loss below 25 in any faction).

Selection Flow

Creation: Pick 1 perk from 3 class-appropriate options.

Level-Up: Draw 3 random perks; player chooses 1.

Implementation Strategy
Recommended Build Order

Phase 14 (Save/Load): Crucial for testing long-term progression.

Phase 11 (Tiles): Quick visual win.

Phase 16 (Perks): Defines the RPG experience.

Phase 15 (Leveling): Ties perks to gameplay loop.

Phase 12 (Static Maps): Sets the stage for the finale.

Phase 13 (NPCs/Bosses): Adds the final layer of narrative depth.