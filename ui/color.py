"""Sepia/noir color palette for Whiskey Hollow."""

from typing import Tuple

Color = Tuple[int, int, int]

# Backgrounds
BLACK: Color = (0, 0, 0)
DARK_GREY: Color = (20, 20, 20)
PANEL_BG: Color = (10, 8, 5)

# Text / UI neutrals
WHITE: Color = (255, 255, 255)
LIGHT_GREY: Color = (180, 180, 180)
MID_GREY: Color = (120, 120, 120)

# Sepia / amber — primary atmosphere
AMBER: Color = (210, 150, 50)
AMBER_DARK: Color = (160, 100, 20)
SEPIA: Color = (180, 130, 70)
PARCHMENT: Color = (220, 195, 140)

# Danger / combat
RED: Color = (200, 30, 30)
RED_DARK: Color = (140, 10, 10)
ORANGE: Color = (220, 100, 20)

# Money / success
GOLD: Color = (230, 190, 40)
GREEN: Color = (60, 180, 60)
GREEN_DARK: Color = (30, 120, 30)

# Heat bar gradient (cool → hot)
HEAT_COOL: Color = (40, 140, 200)
HEAT_WARM: Color = (220, 160, 30)
HEAT_HOT: Color = (220, 40, 20)

# Faction colors
FACTION_PENDERGAST: Color = (100, 60, 180)   # Political purple
FACTION_UNION: Color = (60, 130, 200)         # Rail blue
FACTION_SYNDICATE: Color = (180, 80, 30)      # Rust/brick
FACTION_JAZZ: Color = (200, 170, 40)          # Brass gold
FACTION_KCPD: Color = (60, 80, 160)           # Navy blue

# Map tiles
TILE_DARK_WALL: Color = (30, 22, 12)
TILE_DARK_FLOOR: Color = (50, 38, 20)
TILE_LIGHT_WALL: Color = (100, 80, 40)
TILE_LIGHT_FLOOR: Color = (80, 62, 30)

# Message log categories
MSG_DEFAULT: Color = PARCHMENT
MSG_ATTACK: Color = RED
MSG_PLAYER_GOOD: Color = GREEN
MSG_LOOT: Color = GOLD
MSG_HEAT: Color = ORANGE
MSG_REP: Color = AMBER
MSG_INFO: Color = LIGHT_GREY
MSG_DEATH: Color = RED_DARK

# Player / NPC chars
PLAYER_COLOR: Color = AMBER
ENEMY_GOON: Color = (200, 60, 60)
ENEMY_COP: Color = (80, 100, 200)
ITEM_COLOR: Color = (180, 200, 80)
