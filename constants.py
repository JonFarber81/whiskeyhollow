"""Global constants for Whiskey Hollow."""

# ---------------------------------------------------------------------------
# Phase 11: CP437 Bitmap Tilesheet
# ---------------------------------------------------------------------------
USE_TILESHEET = True  # Set True once you have a CP437 PNG in TILESET_PATH
TILESET_PATH = "data/tiles/Potash_10x10.png"
TILESET_COLUMNS = 16
TILESET_ROWS = 16

# Font fallback (used when USE_TILESHEET is False or file not found)
FONT_PATH = "/System/Library/Fonts/SFNSMono.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/Andale Mono.ttf"
TILE_WIDTH = 12
TILE_HEIGHT = 20   # Taller cells give better line spacing / readability

# Screen dimensions (in character cells, NOT pixels)
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 55

# Map viewport dimensions (left panel)
MAP_WIDTH = 72
MAP_HEIGHT = 38

# Panel dimensions
PANEL_WIDTH = SCREEN_WIDTH - MAP_WIDTH  # 28
STATUS_PANEL_HEIGHT = 22
CREW_PANEL_HEIGHT = MAP_HEIGHT - STATUS_PANEL_HEIGHT  # 21

# Bottom strip dimensions
MSG_LOG_WIDTH = MAP_WIDTH
MSG_LOG_HEIGHT = SCREEN_HEIGHT - MAP_HEIGHT  # 17
FACTION_PANEL_WIDTH = PANEL_WIDTH
FACTION_PANEL_HEIGHT = MSG_LOG_HEIGHT

# Message log settings
MSG_LOG_X = 0
MSG_LOG_Y = MAP_HEIGHT
MAX_MESSAGES = 100

# Inventory
MAX_INVENTORY = 26

# Heat thresholds
HEAT_COP_PATROL = 50
HEAT_RAID = 80

# Faction rep thresholds (rank gates)
REP_STREET_RUNNER = 10
REP_ASSOCIATE = 25
REP_SOLDIER = 45
REP_CAPO = 65
REP_BOSS = 85

# Win conditions
WIN_CASH_RETIRE = 50_000
WIN_DISTRICTS_BOSS = 3

# Crew max size
MAX_CREW = 4

# Title
TITLE = "WHISKEY HOLLOW"
