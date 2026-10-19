---
title: How to Play
---

[← Home](index.md)

# How to Play

## Installing and running

You need Python 3.11 or newer.

```bash
git clone https://github.com/JonFarber81/whiskeyhollow.git
cd whiskeyhollow
pip install -r requirements.txt
python main.py
```

The game uses a system monospace font by default. To use a CP437 bitmap tileset instead, put the PNG at `data/tiles/Alloy_curses_12x12.png` and set `USE_TILESHEET = True` in `constants.py`.

## Controls

| Key | Action |
|---|---|
| Arrow keys / numpad / `hjkl yubn` | Move. Walking into an enemy attacks it |
| `.` or numpad `5` | Wait a turn ("lay low") |
| `c` | Crew menu |
| `f` | Faction and job board |
| `s` | Skill menu (spend skill points) |
| `p` | View your perks |
| `v` | Use **Vanish**, if you have the perk |
| `Ctrl+S` | Quick save |
| `?` | Help screen |
| `Esc` | Quit |

Numpad and vi-keys (`y u b n`) move diagonally.

## The screen

```
┌─────────────────────────────────┬───────────────────┐
│                                 │  PLAYER STATUS    │
│         GAME MAP                │  HP, Cash, Heat,  │
│                                 │  District         │
│                                 ├───────────────────┤
│                                 │  CREW             │
├─────────────────────────────────┼───────────────────┤
│  MESSAGE LOG                    │  FACTION REP      │
└─────────────────────────────────┴───────────────────┘
```

Watch the message log. Combat results, heat changes, and random events all show up there, written in period slang.

## Choosing a class

Each class has its own stats, starting cash, starting gear, a free perk, and a faction it gets along with.

| Class | Stats (STR / DEX / INT / CHA / LUCK) | Cash | Starts with | Perk | Bonus | Affinity |
|---|---|---|---|---|---|---|
| **Brawler** | 16 / 12 / 8 / 10 / 9 | $150 | Brass knuckles | Iron Fists | +20% combat damage, +15% intimidation | River Market Syndicate |
| **Con Man** | 8 / 12 / 13 / 16 / 11 | $300 | Forged documents | Silk Tongue | +25% bribery, +10% rep gain | The Jazz District Co. |
| **Smuggler** | 10 / 14 / 12 / 10 / 9 | $200 | 3 cases of whiskey | Numbers Runner | +20% delivery rewards | Union Station Crew |
| **Fixer** | 8 / 10 / 14 / 14 / 9 | $400 | A police contact | Friends in Low Places | +25% heat reduction, +15% rep gain | Pendergast Machine |

**Brawler** is the easiest class to start with: you get the most HP and you hit hard. **Fixer** starts with the most money and has the easiest time with the cops, but goes down quickly in a fight.

## Winning and losing

There are two ways to win:

1. **Retire.** Save up **$50,000** in cash.
2. **Take over.** Reach **Boss** rank (85+ rep) in any faction and control **3 or more districts**.

You lose when you die. Death is permanent. Each new run gets a new random seed and a new map.

## Tips for new players

- Keep heat below 50. Above that, cop patrols start showing up. At 80 you get raided.
- Fights make noise, and noise raises heat. On delivery and intel jobs, stay out of enemies' line of sight.
- Gaining rep with one faction can cost you rep with its rivals, so choose who you work for carefully.
- You can hire up to 4 crew members, but they each draw a wage, so check that you can afford them.
- Quick save with `Ctrl+S` before a risky job.
