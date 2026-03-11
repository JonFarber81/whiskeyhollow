Whiskey Hollow — Tilesheet Directory
=====================================

Place a CP437 tilesheet PNG here to enable bitmap tile rendering.

To activate:
  1. Download a free CP437 tilesheet (16x16 grid of tiles recommended)
  2. Name it: Alloy_curses_12x12.png  (or update TILESET_PATH in constants.py)
  3. Set USE_TILESHEET = True in constants.py

Recommended free tilesheets (public domain / CC0):
  - Alloy_curses_12x12.png  — itch.io roguelike assets pack
  - Curses_square_16x16.png — ships with python-tcod samples
  - Potash_10x10.png        — clean, slightly stylized

The CHARMAP_CP437 mapping means all existing game tile characters
(#, ., +, @, %, etc.) map automatically to the correct PNG tiles.
No code changes needed beyond setting USE_TILESHEET = True.
