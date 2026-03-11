"""UI menus — character creation, inventory, crew, faction board."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.console
import tcod.context
import tcod.event

from ui import color as Color
from entities.character_class import CharacterClass, CLASS_DEFS, get_class_def
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

if TYPE_CHECKING:
    from engine.engine import Engine


# ---------------------------------------------------------------------------
# Character Creation
# ---------------------------------------------------------------------------

def run_character_creation(
    context: tcod.context.Context,
    root_console: tcod.console.Console,
) -> tuple[str, CharacterClass]:
    """
    Blocking menu: returns (player_name, chosen_class).
    Arrow keys / Enter to navigate.
    """
    classes = list(CharacterClass)
    selected = 0
    player_name = "Jack"

    while True:
        root_console.clear()
        _draw_character_creation(root_console, classes, selected, player_name)
        context.present(root_console)

        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()

            if isinstance(event, tcod.event.KeyDown):
                key = event.sym

                if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.k:
                    selected = (selected - 1) % len(classes)
                elif key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.j:
                    selected = (selected + 1) % len(classes)
                elif key == tcod.event.KeySym.RETURN:
                    return player_name, classes[selected]
                elif key == tcod.event.KeySym.ESCAPE:
                    raise SystemExit()


def _draw_character_creation(
    console: tcod.console.Console,
    classes: list[CharacterClass],
    selected: int,
    player_name: str,
) -> None:
    cx = SCREEN_WIDTH // 2
    cy = 4

    # Title
    console.print(x=cx - 8, y=cy, string="WHISKEY HOLLOW", fg=Color.AMBER)
    console.print(x=cx - 17, y=cy + 1, string="Kansas City, 1924 — Choose Your Racket", fg=Color.SEPIA)
    console.print(x=cx - 10, y=cy + 2, string="─" * 20, fg=Color.AMBER_DARK)

    # Class picker
    for i, char_class in enumerate(classes):
        cd = CLASS_DEFS[char_class]
        y_pos = cy + 4 + (i * 2)
        if i == selected:
            console.print(x=cx - 20, y=y_pos, string=f"▶ {cd.name}", fg=Color.GOLD)
        else:
            console.print(x=cx - 20, y=y_pos, string=f"  {cd.name}", fg=Color.LIGHT_GREY)

    # Detail panel for selected class
    cd = CLASS_DEFS[classes[selected]]
    detail_x = cx - 5
    detail_y = cy + 4

    console.print(x=detail_x, y=detail_y, string=cd.name, fg=Color.AMBER)
    console.print(x=detail_x, y=detail_y + 1, string=cd.description, fg=Color.PARCHMENT)
    console.print(x=detail_x, y=detail_y + 2, string=f'"{cd.flavor}"', fg=Color.SEPIA)

    console.print(x=detail_x, y=detail_y + 4, string="STATS", fg=Color.AMBER_DARK)
    stats_labels = [
        ("STR", cd.str),
        ("DEX", cd.dex),
        ("INT", cd.int_),
        ("CHA", cd.cha),
        ("LCK", cd.luck),
    ]
    for j, (label, val) in enumerate(stats_labels):
        bar = "█" * (val // 2)
        console.print(x=detail_x, y=detail_y + 5 + j, string=f"{label} {val:2d} {bar}", fg=Color.AMBER)

    console.print(x=detail_x, y=detail_y + 11, string=f"Starting Cash: ${cd.starting_cash}", fg=Color.GOLD)
    console.print(x=detail_x, y=detail_y + 12, string=f"Faction:  {cd.faction_affinity}", fg=Color.SEPIA)

    # Footer
    console.print(
        x=cx - 18, y=SCREEN_HEIGHT - 3,
        string="[↑↓] Browse classes    [Enter] Begin    [Esc] Quit",
        fg=Color.MID_GREY,
    )


# ---------------------------------------------------------------------------
# Crew Menu
# ---------------------------------------------------------------------------

def run_crew_menu(engine: Engine, context: tcod.context.Context, console: tcod.console.Console) -> None:
    """Blocking crew management overlay. Press Esc or c to close."""
    crew = engine.crew
    selected = 0

    while True:
        console.clear()
        engine.render(console)
        _draw_crew_menu(console, engine, selected)
        context.present(console)

        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()
            if isinstance(event, tcod.event.KeyDown):
                key = event.sym
                if key in (tcod.event.KeySym.ESCAPE, tcod.event.KeySym.c):
                    return
                if key in (tcod.event.KeySym.UP, tcod.event.KeySym.k) and crew.members:
                    selected = (selected - 1) % len(crew.members)
                elif key in (tcod.event.KeySym.DOWN, tcod.event.KeySym.j) and crew.members:
                    selected = (selected + 1) % len(crew.members)
                elif key == tcod.event.KeySym.f and crew.members:
                    # Fire selected crew member
                    member = crew.members[selected]
                    crew.remove(member)
                    engine.message_log.add_message(
                        f"You let {member.name} go.", fg=Color.MID_GREY
                    )
                    selected = max(0, selected - 1)
                elif key == tcod.event.KeySym.h:
                    # Hire — show candidate pool
                    run_hire_menu(engine, context, console)


def _draw_crew_menu(console: tcod.console.Console, engine: Engine, selected: int) -> None:
    from components.crew_member import CrewStatus
    crew = engine.crew
    ox, oy, w, h = 5, 3, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 6

    console.draw_frame(x=ox, y=oy, width=w, height=h, title=" CREW MANAGEMENT ", fg=Color.AMBER, bg=Color.PANEL_BG)
    console.print(x=ox + 2, y=oy + 2, string=f"Crew: {len(crew.members)}/4   Cash: ${engine.cash:,}", fg=Color.GOLD)
    console.print(x=ox + 2, y=oy + 3, string="[↑↓] Select  [f] Fire  [h] Hire  [Esc] Close", fg=Color.MID_GREY)
    console.print(x=ox + 2, y=oy + 4, string="─" * (w - 4), fg=Color.AMBER_DARK)

    if not crew.members:
        console.print(x=ox + 4, y=oy + 6, string="No crew. Press [h] to hire.", fg=Color.MID_GREY)
        return

    for i, m in enumerate(crew.members):
        row_y = oy + 6 + i * 6
        fg = Color.GOLD if i == selected else Color.PARCHMENT
        prefix = "▶ " if i == selected else "  "
        status_str = m.status.value.upper()
        console.print(x=ox + 2, y=row_y, string=f"{prefix}{m.name}  [{m.role.value}]  {status_str}", fg=fg)
        console.print(x=ox + 4, y=row_y + 1, string=f"Loyalty: {m.loyalty:3d}   Wage: ${m.wage}/chapter   HP: {m.hp}/{m.max_hp}", fg=Color.SEPIA)
        skill_str = "  ".join(f"{k}:{v}" for k, v in m.skills.items())
        console.print(x=ox + 4, y=row_y + 2, string=f"Skills: {skill_str}", fg=Color.MID_GREY)
        console.print(x=ox + 4, y=row_y + 3, string=m.role_bonus_description, fg=Color.AMBER_DARK)


def run_hire_menu(engine: Engine, context: tcod.context.Context, console: tcod.console.Console) -> None:
    """Show hireable candidates and let player recruit one."""
    from factions.crew_pool import generate_hire_candidates
    candidates = generate_hire_candidates(engine.rng, count=4)
    selected = 0

    while True:
        console.clear()
        engine.render(console)
        _draw_hire_menu(console, engine, candidates, selected)
        context.present(console)

        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()
            if isinstance(event, tcod.event.KeyDown):
                key = event.sym
                if key in (tcod.event.KeySym.ESCAPE,):
                    return
                if key in (tcod.event.KeySym.UP, tcod.event.KeySym.k):
                    selected = (selected - 1) % len(candidates)
                elif key in (tcod.event.KeySym.DOWN, tcod.event.KeySym.j):
                    selected = (selected + 1) % len(candidates)
                elif key == tcod.event.KeySym.RETURN:
                    candidate = candidates[selected]
                    if engine.crew.add(candidate):
                        engine.message_log.add_message(
                            f"{candidate.name} joins your crew as {candidate.role.value}.",
                            fg=Color.GREEN,
                        )
                        return
                    else:
                        engine.message_log.add_message(
                            "Crew is full. Fire someone first.", fg=Color.ORANGE
                        )


def _draw_hire_menu(console: tcod.console.Console, engine: Engine, candidates: list, selected: int) -> None:
    ox, oy, w, h = 5, 3, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 6
    console.draw_frame(x=ox, y=oy, width=w, height=h, title=" HIRE CREW ", fg=Color.AMBER, bg=Color.PANEL_BG)
    console.print(x=ox + 2, y=oy + 2, string="[↑↓] Browse  [Enter] Hire  [Esc] Back", fg=Color.MID_GREY)
    console.print(x=ox + 2, y=oy + 3, string="─" * (w - 4), fg=Color.AMBER_DARK)

    for i, m in enumerate(candidates):
        row_y = oy + 5 + i * 5
        fg = Color.GOLD if i == selected else Color.PARCHMENT
        prefix = "▶ " if i == selected else "  "
        console.print(x=ox + 2, y=row_y, string=f"{prefix}{m.name}  [{m.role.value}]  Wage: ${m.wage}/chapter", fg=fg)
        skill_str = "  ".join(f"{k}:{v}" for k, v in m.skills.items())
        console.print(x=ox + 4, y=row_y + 1, string=f"Skills: {skill_str}", fg=Color.SEPIA)
        console.print(x=ox + 4, y=row_y + 2, string=m.role_bonus_description, fg=Color.AMBER_DARK)


# ---------------------------------------------------------------------------
# Faction / Job Board Menu
# ---------------------------------------------------------------------------

def run_faction_menu(engine: Engine, context: tcod.context.Context, console: tcod.console.Console) -> None:
    """Faction board — view rep + accept jobs."""
    from factions.faction_data import FACTIONS, all_factions
    from factions.job_board import generate_jobs, resolve_job_success, resolve_job_failure

    factions = all_factions()
    faction_idx = 0
    job_idx = 0
    standing = getattr(engine.player, "faction_standing", None)
    mode = "factions"   # "factions" | "jobs"
    current_jobs: list = []

    while True:
        console.clear()
        engine.render(console)
        if mode == "factions":
            _draw_faction_board(console, engine, factions, faction_idx, standing)
        else:
            _draw_job_board(console, engine, current_jobs, job_idx, factions[faction_idx])
        context.present(console)

        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()
            if isinstance(event, tcod.event.KeyDown):
                key = event.sym
                if key in (tcod.event.KeySym.ESCAPE, tcod.event.KeySym.f):
                    if mode == "jobs":
                        mode = "factions"
                    else:
                        return
                elif key in (tcod.event.KeySym.UP, tcod.event.KeySym.k):
                    if mode == "factions":
                        faction_idx = (faction_idx - 1) % len(factions)
                    else:
                        job_idx = (job_idx - 1) % len(current_jobs) if current_jobs else 0
                elif key in (tcod.event.KeySym.DOWN, tcod.event.KeySym.j):
                    if mode == "factions":
                        faction_idx = (faction_idx + 1) % len(factions)
                    else:
                        job_idx = (job_idx + 1) % len(current_jobs) if current_jobs else 0
                elif key == tcod.event.KeySym.RETURN:
                    if mode == "factions":
                        # Open job board for this faction
                        faction = factions[faction_idx]
                        rep = standing.get_rep(faction.key) if standing else 0
                        current_jobs = generate_jobs(faction.key, rep, engine.rng)
                        job_idx = 0
                        mode = "jobs"
                    elif mode == "jobs" and current_jobs:
                        # Accept job — simple instant resolution for now
                        job = current_jobs[job_idx]
                        _resolve_job_interactively(job, engine)
                        current_jobs.pop(job_idx)
                        job_idx = max(0, job_idx - 1)


def _draw_faction_board(console, engine, factions, selected_idx, standing) -> None:
    ox, oy, w, h = 3, 2, SCREEN_WIDTH - 6, SCREEN_HEIGHT - 4
    console.draw_frame(x=ox, y=oy, width=w, height=h, title=" FACTION BOARD [f] ", fg=Color.AMBER, bg=Color.PANEL_BG)
    console.print(x=ox + 2, y=oy + 2, string="[↑↓] Select faction  [Enter] View jobs  [Esc] Close", fg=Color.MID_GREY)

    for i, faction in enumerate(factions):
        row_y = oy + 4 + i * 6
        rep = standing.get_rep(faction.key) if standing else 0
        title = faction.rank_title(rep)
        fg = faction.color if i == selected_idx else Color.LIGHT_GREY
        prefix = "▶ " if i == selected_idx else "  "
        console.print(x=ox + 2, y=row_y, string=f"{prefix}{faction.name}", fg=fg)
        console.print(x=ox + 4, y=row_y + 1, string=f"Rep: {rep:3d}/100  Rank: {title}", fg=Color.SEPIA)
        bar_w = 30
        filled = int(bar_w * rep / 100)
        bar = "█" * filled + "░" * (bar_w - filled)
        console.print(x=ox + 4, y=row_y + 2, string=bar, fg=faction.color)
        if i == selected_idx:
            desc = faction.description[:w - 8]
            console.print(x=ox + 4, y=row_y + 3, string=desc, fg=Color.PARCHMENT)


def _draw_job_board(console, engine, jobs, selected_idx, faction) -> None:
    ox, oy, w, h = 3, 2, SCREEN_WIDTH - 6, SCREEN_HEIGHT - 4
    console.draw_frame(x=ox, y=oy, width=w, height=h, title=f" JOBS — {faction.name} ", fg=faction.color, bg=Color.PANEL_BG)
    console.print(x=ox + 2, y=oy + 2, string="[↑↓] Select  [Enter] Accept  [Esc] Back", fg=Color.MID_GREY)

    if not jobs:
        console.print(x=ox + 4, y=oy + 5, string="No jobs available right now.", fg=Color.MID_GREY)
        return

    for i, job in enumerate(jobs):
        row_y = oy + 4 + i * 7
        fg = Color.GOLD if i == selected_idx else Color.PARCHMENT
        prefix = "▶ " if i == selected_idx else "  "
        stars = "★" * job.difficulty + "☆" * (5 - job.difficulty)
        console.print(x=ox + 2, y=row_y, string=f"{prefix}[{job.job_type.value.upper()}] {job.title}", fg=fg)
        console.print(x=ox + 4, y=row_y + 1, string=f"Difficulty: {stars}", fg=Color.AMBER)
        console.print(x=ox + 4, y=row_y + 2, string=job.description, fg=Color.SEPIA)
        console.print(x=ox + 4, y=row_y + 3, string=f"Reward: ${job.cash_reward}  Rep: +{job.rep_reward}  Heat on fail: +{job.heat_on_failure}", fg=Color.GOLD)


def _resolve_job_interactively(job, engine) -> None:
    """Quick probabilistic job resolution until full job maps are implemented."""
    from factions.job_board import resolve_job_success, resolve_job_failure
    from ui import color as Color

    # Base success chance from difficulty
    base_chance = max(20, 90 - job.difficulty * 15)

    # Class bonuses
    char_class = getattr(engine, "char_class", None)
    bonus = 0
    if char_class:
        from entities.character_class import CLASS_DEFS, CharacterClass
        from factions.job_board import JobType
        cd = CLASS_DEFS.get(char_class)
        if cd:
            if job.job_type == JobType.BRIBERY:
                bonus += int(cd.bonus.bribery_success_bonus * 100)
            elif job.job_type == JobType.DELIVERY:
                bonus += int(cd.bonus.delivery_reward_bonus * 100)
            elif job.job_type == JobType.INTIMIDATION:
                bonus += int(cd.bonus.intimidation_success_bonus * 100)

    # Crew bonuses
    crew = getattr(engine, "crew", None)
    if crew:
        from components.crew_member import CrewRole
        from factions.job_board import JobType
        if job.job_type in (JobType.INTIMIDATION,) and crew.has_role(CrewRole.MUSCLE):
            bonus += 20
        elif job.job_type == JobType.BRIBERY and crew.has_role(CrewRole.FIXER):
            bonus += 20
        elif job.job_type == JobType.DELIVERY and crew.has_role(CrewRole.DRIVER):
            bonus += 15

    success_chance = min(95, base_chance + bonus)
    roll = engine.rng.randint(1, 100)

    if roll <= success_chance:
        resolve_job_success(job, engine)
    else:
        resolve_job_failure(job, engine)


# ---------------------------------------------------------------------------
# Help Screen
# ---------------------------------------------------------------------------

def run_help_screen(context: tcod.context.Context, console: tcod.console.Console) -> None:
    console.clear()
    _draw_help(console)
    context.present(console)
    for event in tcod.event.wait():
        if isinstance(event, (tcod.event.KeyDown, tcod.event.Quit)):
            return


def _draw_help(console: tcod.console.Console) -> None:
    ox, oy, w, h = 5, 2, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 4
    console.draw_frame(x=ox, y=oy, width=w, height=h, title=" HELP — WHISKEY HOLLOW ", fg=Color.AMBER, bg=Color.PANEL_BG)

    lines = [
        ("MOVEMENT", None),
        ("Arrow keys / numpad / vi-keys (hjklyubn)", Color.PARCHMENT),
        (". or numpad5  — Wait one turn", Color.PARCHMENT),
        ("", None),
        ("ACTIONS", None),
        ("c  — Crew management (hire, fire, view)", Color.PARCHMENT),
        ("f  — Faction board (view rep, accept jobs)", Color.PARCHMENT),
        ("s  — Spend skill points on stats", Color.PARCHMENT),
        ("g  — Pick up item", Color.PARCHMENT),
        ("i  — Inventory", Color.PARCHMENT),
        ("?  — This help screen", Color.PARCHMENT),
        ("Esc — Quit", Color.PARCHMENT),
        ("", None),
        ("COMBAT", None),
        ("Walk into an enemy to attack.", Color.PARCHMENT),
        ("Roll: d20 + ATK vs 10 + DEF. 10+ over target = crit.", Color.PARCHMENT),
        ("Guns raise your heat level when fired.", Color.PARCHMENT),
        ("", None),
        ("HEAT", None),
        ("Heat 0-49  — Normal patrol activity.", Color.HEAT_COOL),
        ("Heat 50-79 — Cops actively patrol. Watch your back.", Color.HEAT_WARM),
        ("Heat 80+   — RAID. Get out or fight through.", Color.HEAT_HOT),
        ("", None),
        ("WIN CONDITIONS", None),
        ("Reach Boss rank (85+ rep) in any faction + control 3 districts.", Color.GOLD),
        ("Or accumulate $50,000 and retire.", Color.GOLD),
        ("", None),
        ("Press any key to close.", Color.MID_GREY),
    ]

    headers = {"MOVEMENT", "ACTIONS", "COMBAT", "HEAT", "WIN CONDITIONS"}
    y = oy + 2
    for text, fg in lines:
        if text in headers:
            console.print(x=ox + 2, y=y, string=text, fg=Color.AMBER)
        elif fg and text:
            console.print(x=ox + 4, y=y, string=text, fg=fg)
        y += 1


# ---------------------------------------------------------------------------
# Skill Point Spend Menu
# ---------------------------------------------------------------------------

def run_skill_menu(engine: Engine, context: tcod.context.Context, console: tcod.console.Console) -> None:
    stats = getattr(engine.player, "stats", None)
    if not stats:
        return

    stat_names = ["strength", "dexterity", "intelligence", "charisma", "luck"]
    labels = {"strength": "STR — Melee dmg, HP base",
              "dexterity": "DEX — Dodge, Stealth, Ranged",
              "intelligence": "INT — Market insight, Heat rate",
              "charisma": "CHA — Bribery, Crew loyalty, Rep gain",
              "luck": "LCK — Crit chance, Escape, Job luck"}
    selected = 0

    while True:
        console.clear()
        engine.render(console)
        _draw_skill_menu(console, engine, stats, stat_names, labels, selected)
        context.present(console)

        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()
            if isinstance(event, tcod.event.KeyDown):
                key = event.sym
                if key in (tcod.event.KeySym.ESCAPE, tcod.event.KeySym.s):
                    return
                elif key in (tcod.event.KeySym.UP, tcod.event.KeySym.k):
                    selected = (selected - 1) % len(stat_names)
                elif key in (tcod.event.KeySym.DOWN, tcod.event.KeySym.j):
                    selected = (selected + 1) % len(stat_names)
                elif key == tcod.event.KeySym.RETURN:
                    if stats.skill_points > 0:
                        stat = stat_names[selected]
                        if stats.spend_skill_point(stat):
                            # Update fighter derived stats
                            fighter = engine.player.fighter
                            fighter.max_hp = stats.max_hp
                            fighter.hp = min(fighter.hp, fighter.max_hp)
                            fighter.base_attack = stats.base_attack
                            fighter.base_defense = stats.base_defense
                            engine.message_log.add_message(
                                f"{stat.upper()} raised to {getattr(stats, stat)}.", fg=Color.GOLD
                            )
                        if stats.skill_points == 0:
                            return
                    else:
                        engine.message_log.add_message("No skill points available.", fg=Color.MID_GREY)


def _draw_skill_menu(console, engine, stats, stat_names, labels, selected) -> None:
    ox, oy, w, h = 15, 5, SCREEN_WIDTH - 30, SCREEN_HEIGHT - 10
    console.draw_frame(x=ox, y=oy, width=w, height=h, title=" SPEND SKILL POINTS ", fg=Color.AMBER, bg=Color.PANEL_BG)
    console.print(x=ox + 2, y=oy + 2, string=f"Available SP: {stats.skill_points}", fg=Color.GOLD)
    console.print(x=ox + 2, y=oy + 3, string="[↑↓] Select  [Enter] Spend  [Esc] Close", fg=Color.MID_GREY)

    attr_map = {"strength": "strength", "dexterity": "dexterity", "intelligence": "intelligence",
                "charisma": "charisma", "luck": "luck"}
    short = {"strength": "STR", "dexterity": "DEX", "intelligence": "INT", "charisma": "CHA", "luck": "LCK"}

    for i, stat in enumerate(stat_names):
        val = getattr(stats, stat)
        mod = stats._mod(val)
        fg = Color.GOLD if i == selected else Color.PARCHMENT
        prefix = "▶ " if i == selected else "  "
        bar = "█" * (val // 2)
        console.print(x=ox + 2, y=oy + 5 + i * 3, string=f"{prefix}{short[stat]} {val:2d} ({mod:+d})  {bar}", fg=fg)
        console.print(x=ox + 4, y=oy + 6 + i * 3, string=labels[stat], fg=Color.SEPIA)


# ---------------------------------------------------------------------------
# Main Menu (Phase 14) — New Game / Continue / Quit
# ---------------------------------------------------------------------------

def run_main_menu(
    context: tcod.context.Context,
    root_console: tcod.console.Console,
    saves: list,
) -> str:
    """Show main menu. Returns 'new', 'continue', or 'quit'."""
    has_save = any(s.get("exists") for s in saves)
    options = []
    if has_save:
        options.append(("continue", "Continue"))
    options.append(("new", "New Game"))
    options.append(("quit", "Quit"))

    selected = 0

    while True:
        root_console.clear()
        _draw_main_menu(root_console, options, selected, saves)
        context.present(root_console)

        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                return "quit"
            if isinstance(event, tcod.event.KeyDown):
                key = event.sym
                if key in (tcod.event.KeySym.UP, tcod.event.KeySym.k):
                    selected = (selected - 1) % len(options)
                elif key in (tcod.event.KeySym.DOWN, tcod.event.KeySym.j):
                    selected = (selected + 1) % len(options)
                elif key == tcod.event.KeySym.RETURN:
                    return options[selected][0]
                elif key == tcod.event.KeySym.ESCAPE:
                    return "quit"


def _draw_main_menu(
    console: tcod.console.Console,
    options: list,
    selected: int,
    saves: list,
) -> None:
    cx = SCREEN_WIDTH // 2
    cy = SCREEN_HEIGHT // 2 - 10

    console.print(x=cx - 7, y=cy, string="WHISKEY HOLLOW", fg=Color.AMBER)
    console.print(x=cx - 17, y=cy + 1, string="Kansas City, 1924 — A Prohibition-Era Roguelike", fg=Color.SEPIA)
    console.print(x=cx - 10, y=cy + 2, string="─" * 20, fg=Color.AMBER_DARK)

    for i, (key, label) in enumerate(options):
        y = cy + 5 + i * 2
        if i == selected:
            console.print(x=cx - 6, y=y, string=f"▶  {label}", fg=Color.GOLD)
        else:
            console.print(x=cx - 6, y=y, string=f"   {label}", fg=Color.LIGHT_GREY)

    # Show save info if a save exists
    save = next((s for s in saves if s.get("exists")), None)
    if save:
        console.print(
            x=cx - 20, y=cy + 14,
            string=f"Save: {save['name']} ({save['char_class']}) — "
                   f"Turn {save['turn']} | ${save['cash']:,} | {save['district']}",
            fg=Color.MID_GREY,
        )

    console.print(
        x=cx - 15, y=SCREEN_HEIGHT - 3,
        string="[↑↓] Navigate   [Enter] Select   [Esc] Quit",
        fg=Color.MID_GREY,
    )


# ---------------------------------------------------------------------------
# Perk Selection Menu (Phase 16)
# ---------------------------------------------------------------------------

def run_perk_selection(
    engine,
    context: tcod.context.Context,
    console: tcod.console.Console,
    char_class=None,
    is_creation: bool = False,
) -> Optional[str]:
    """
    Show a perk selection overlay and return the chosen perk key.
    If is_creation=True, used at character creation (engine may be None).
    Otherwise used at level-up with a live engine.
    """
    from entities.perks import get_perk_options, PERKS
    from entities.character_class import CharacterClass

    # Resolve class value string
    if char_class is not None:
        class_val = char_class.value if isinstance(char_class, CharacterClass) else str(char_class)
    elif engine:
        cc = getattr(engine, "char_class", None)
        class_val = cc.value if cc else "Brawler"
    else:
        class_val = "Brawler"

    owned = list(getattr(getattr(engine, "player", None), "perks", [])) if engine else []

    # Draw 3 options
    rng_src = getattr(engine, "rng", None) if engine else None
    options = get_perk_options(class_val, owned, count=3, rng=rng_src)
    if not options:
        return None

    selected = 0

    while True:
        console.clear()
        if engine:
            engine.render(console)
        _draw_perk_selection(console, options, selected, is_creation)
        context.present(console)

        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()
            if isinstance(event, tcod.event.KeyDown):
                key = event.sym
                if key in (tcod.event.KeySym.UP, tcod.event.KeySym.k):
                    selected = (selected - 1) % len(options)
                elif key in (tcod.event.KeySym.DOWN, tcod.event.KeySym.j):
                    selected = (selected + 1) % len(options)
                elif key == tcod.event.KeySym.RETURN:
                    perk = options[selected]
                    if engine and engine.player:
                        engine.player.perks.append(perk.key)
                        from main import _apply_immediate_perk
                        _apply_immediate_perk(engine.player, perk.key)
                        engine.message_log.add_message(
                            f"Perk acquired: {perk.name}!", fg=Color.GOLD
                        )
                        # Phase 16: Word Gets Around — all factions +2 rep on level-up
                        from entities.perks import has_perk
                        if has_perk(engine.player, "word_gets_around"):
                            standing = getattr(engine.player, "faction_standing", None)
                            if standing:
                                for fk in standing.rep:
                                    standing.rep[fk] = min(100, standing.rep[fk] + 2)
                    return perk.key
                elif key == tcod.event.KeySym.ESCAPE and not is_creation:
                    return None  # Level-up: skip perk (rare edge case)


def _draw_perk_selection(
    console: tcod.console.Console,
    options: list,
    selected: int,
    is_creation: bool,
) -> None:
    from entities.perks import PERKS
    title = " CHOOSE A STARTING PERK " if is_creation else " LEVEL UP — CHOOSE A PERK "
    ox, oy, w, h = 8, 5, SCREEN_WIDTH - 16, SCREEN_HEIGHT - 10
    console.draw_frame(x=ox, y=oy, width=w, height=h, title=title, fg=Color.GOLD, bg=Color.PANEL_BG)
    console.print(x=ox + 2, y=oy + 2, string="[↑↓] Browse   [Enter] Pick", fg=Color.MID_GREY)

    cat_colors = {
        "combat": Color.RED,
        "economy": Color.GOLD,
        "shadow": Color.PARCHMENT,
        "influence": Color.AMBER,
    }

    for i, perk in enumerate(options):
        row_y = oy + 4 + i * 6
        fg = Color.GOLD if i == selected else Color.PARCHMENT
        prefix = "▶ " if i == selected else "  "
        cat_fg = cat_colors.get(perk.category, Color.SEPIA)
        console.print(x=ox + 2, y=row_y, string=f"{prefix}{perk.name}", fg=fg)
        console.print(x=ox + 4, y=row_y + 1, string=f"[{perk.category.upper()}]", fg=cat_fg)
        console.print(x=ox + 4, y=row_y + 2, string=perk.description[:w - 8], fg=Color.SEPIA)
        if i < len(options) - 1:
            console.print(x=ox + 2, y=row_y + 4, string="─" * (w - 4), fg=Color.AMBER_DARK)


# ---------------------------------------------------------------------------
# Perk Viewer (Phase 16) — Press 'p' to view owned perks
# ---------------------------------------------------------------------------

def run_perk_viewer(
    engine: "Engine",
    context: tcod.context.Context,
    console: tcod.console.Console,
) -> None:
    from entities.perks import PERKS
    perks_owned = getattr(engine.player, "perks", [])

    console.clear()
    engine.render(console)
    ox, oy, w, h = 8, 3, SCREEN_WIDTH - 16, SCREEN_HEIGHT - 6
    console.draw_frame(x=ox, y=oy, width=w, height=h, title=" YOUR PERKS ", fg=Color.GOLD, bg=Color.PANEL_BG)

    if not perks_owned:
        console.print(x=ox + 2, y=oy + 3, string="No perks yet. Level up to earn them!", fg=Color.MID_GREY)
    else:
        for i, key in enumerate(perks_owned):
            perk = PERKS.get(key)
            if perk:
                row_y = oy + 2 + i * 3
                console.print(x=ox + 2, y=row_y, string=f"★ {perk.name}", fg=Color.GOLD)
                console.print(x=ox + 4, y=row_y + 1, string=perk.description[:w - 8], fg=Color.SEPIA)

    console.print(x=ox + 2, y=oy + h - 2, string="Press any key to close.", fg=Color.MID_GREY)
    context.present(console)

    for event in tcod.event.wait():
        if isinstance(event, (tcod.event.KeyDown, tcod.event.Quit)):
            return
