"""Character class for Western RPG game with Rich terminal enhancements."""

import random
import time
from typing import Dict, Any

# Rich imports
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.prompt import IntPrompt, Prompt
from rich.text import Text
from rich.columns import Columns
from rich import box

from dice import roll_4d6_drop_lowest, roll_starting_money
from skills import skill_manager

# Global console for Rich output
console = Console()


class Character:
    """Represents a character in the Western RPG game."""
    
    def __init__(self, name: str = "") -> None:
        """Initialize a new character."""
        self.name: str = name
        self.age: int = 0
        self.level: int = 1
        self.experience: int = 0
        self.dollars: int = 0
        self.skill_points: int = 0
        
        # Core attributes (3-18 range)
        self.vigor: int = 0      # Physical strength, endurance, toughness
        self.finesse: int = 0    # Dexterity, agility, coordination
        self.smarts: int = 0     # Intelligence, wisdom, awareness
        
        # Skills - only store skills with points > 0
        self.skills: Dict[str, int] = {}
        
        # Derived stats
        self.hit_points: int = 0
        self.max_hit_points: int = 0
        self.movement: int = 0    # Movement in yards per turn
        
        # Inventory system - slot-based
        self.inventory: Dict[str, int] = {}  # item_name: quantity
        self.base_inventory_slots: int = 0   # Based on vigor
        self.bonus_inventory_slots: int = 0  # From backpacks, etc.
        
        # Equipment slots
        self.weapon: str = "Unarmed"
        self.armor: str = "Clothes"
        self.location: str = "Whiskey Hollow"

    def roll_attributes(self) -> None:
        """Roll 4d6 drop lowest for each attribute."""
        self.vigor = roll_4d6_drop_lowest()
        self.finesse = roll_4d6_drop_lowest()
        self.smarts = roll_4d6_drop_lowest()
        self.dollars = roll_starting_money()
        self.calculate_derived_stats()
    
    def apply_age_effects(self) -> None:
        """Apply age-based bonuses and penalties with Rich formatting."""
        if not (14 <= self.age <= 57):
            console.print(f"[red]⚠️  Warning: Age {self.age} is outside normal range (14-57)[/red]")
            return
        
        # Age effects header
        console.print(Panel(
            f"[bold gold1]Applying Life Experience Effects[/bold gold1]\n"
            f"[sandy_brown]{self.name}, Age {self.age}[/sandy_brown]",
            title="[bold cyan]⏳ AGE & WISDOM[/bold cyan]",
            border_style="cyan"
        ))
        
        # Determine skill points and tests based on age
        if 14 <= self.age <= 22:
            skill_points = 5
            attribute_boosts = 2
            vigor_tests = 0
            category = "Young"
            category_color = "bright_green"
        elif 23 <= self.age <= 26:
            skill_points = 5
            attribute_boosts = 3
            vigor_tests = 0
            category = "Prime (Early)"
            category_color = "green"
        elif 27 <= self.age <= 30:
            skill_points = 6
            attribute_boosts = 2
            vigor_tests = 0
            category = "Prime"
            category_color = "yellow"
        elif 31 <= self.age <= 34:
            skill_points = 7
            attribute_boosts = 1
            vigor_tests = 1
            category = "Prime (Late)"
            category_color = "orange1"
        elif 35 <= self.age <= 48:
            skill_points = 9
            attribute_boosts = 0
            vigor_tests = 3
            category = "Experienced"
            category_color = "red"
        elif 49 <= self.age <= 52:
            skill_points = 11
            attribute_boosts = 0
            vigor_tests = 5
            category = "Experienced (Elder)"
            category_color = "red3"
        elif 53 <= self.age <= 56:
            skill_points = 13
            attribute_boosts = 0
            vigor_tests = 7
            category = "Elder"
            category_color = "purple"
        elif self.age == 57:
            skill_points = 15
            attribute_boosts = 0
            vigor_tests = 9
            category = "Ancient"
            category_color = "bright_magenta"
        
        # Display age category with styling
        console.print(f"\n[bold {category_color}]Age Category: {category}[/bold {category_color}]")
        
        # Create effects summary table
        effects_table = Table(box=box.SIMPLE, border_style="gold1", show_header=False)
        effects_table.add_column("Effect", style="bold cyan")
        effects_table.add_column("Amount", style="bold yellow", justify="right")
        
        effects_table.add_row("🎓 Skill Points Gained", str(skill_points))
        effects_table.add_row("⬆️ Attribute Boosts", str(attribute_boosts))
        if vigor_tests > 0:
            effects_table.add_row("⚡ Vigor Tests Required", str(vigor_tests))
        
        console.print(effects_table)
        console.print()
        
        # Apply skill points
        self.skill_points += skill_points
        console.print(f"[bold green]✅ Gained {skill_points} skill points![/bold green]")
        
        # Apply attribute boosts with animation
        if attribute_boosts > 0:
            console.print(f"\n[bold gold1]🎲 Rolling for {attribute_boosts} attribute boosts...[/bold gold1]")
            
            for i in range(attribute_boosts):
                with console.status(f"[bold]Rolling boost #{i + 1}...[/bold]", spinner="dots"):
                    time.sleep(0.8)  # Dramatic pause
                self._apply_random_attribute_boost(i + 1)
        
        # Apply vigor tests with suspense
        if vigor_tests > 0:
            console.print(f"\n[bold red]💀 Time takes its toll... Making {vigor_tests} vigor tests[/bold red]")
            
            for i in range(vigor_tests):
                with console.status(f"[bold]Preparing test #{i + 1}...[/bold]", spinner="dots"):
                    time.sleep(0.5)
                self._make_vigor_test(i + 1)
        
        # Recalculate derived stats (including movement) after all attribute changes
        self.calculate_derived_stats()
        
        console.print(Panel(
            "[bold green]✨ Age effects applied successfully![/bold green]\n"
            f"[sandy_brown]{self.name} is ready for adventure![/sandy_brown]",
            title="[bold gold1]TRANSFORMATION COMPLETE[/bold gold1]",
            border_style="green"
        ))
    
    def _apply_random_attribute_boost(self, boost_num: int) -> None:
        """Apply a random +1 attribute boost (max 18) with Rich visualization."""
        attributes = ['vigor', 'finesse', 'smarts']
        
        # Only consider attributes that aren't already at max
        available_attributes = [attr for attr in attributes if getattr(self, attr) < 18]
        
        if not available_attributes:
            console.print(f"[dim]Boost #{boost_num}: All attributes at maximum (18), boost wasted[/dim]")
            return
        
        chosen_attr = random.choice(available_attributes)
        old_value = getattr(self, chosen_attr)
        setattr(self, chosen_attr, old_value + 1)
        new_value = getattr(self, chosen_attr)
        
        console.print(
            f"[bold green]Boost #{boost_num}:[/bold green] "
            f"[bold cyan]{chosen_attr.title()}[/bold cyan] "
            f"[yellow]{old_value}[/yellow] → [bold yellow]{new_value}[/bold yellow]"
        )
    
    def _make_vigor_test(self, test_num: int) -> None:
        """Make a vigor test with Rich dice animation."""
        vigor_modifier = self.get_attribute_modifier(self.vigor)
        dice_to_roll = max(1, vigor_modifier + 1)  # At least 1 die, +1 for base
        
        console.print(f"\n[bold red]⚡ Vigor Test #{test_num}[/bold red]")
        console.print(f"[dim]Rolling {dice_to_roll}d6 (need at least one 5 or 6 to pass)[/dim]")
        
        # Dice rolling animation
        with Progress(
            TextColumn("[progress.description]"),
            BarColumn(),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("🎲 Rolling dice...", total=100)
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.02)
        
        rolls = [random.randint(1, 6) for _ in range(dice_to_roll)]
        successes = [r for r in rolls if r >= 5]
        
        # Display dice results with colors
        dice_display = []
        for roll in rolls:
            if roll >= 5:
                dice_display.append(f"[bold green]{roll}[/bold green]")
            else:
                dice_display.append(f"[dim]{roll}[/dim]")
        
        console.print(f"  🎲 Rolled: {' '.join(dice_display)}")
        console.print(f"  ✨ Successes: {len(successes)}")
        
        if successes:
            console.print(f"  [bold green]✅ PASSED![/bold green] No attribute loss")
        else:
            console.print(f"  [bold red]❌ FAILED![/bold red] Must lose 1 attribute point")
            self._lose_random_attribute()
    
    def _lose_random_attribute(self) -> None:
        """Lose 1 point from a random attribute (minimum 3) with Rich formatting."""
        attributes = ['vigor', 'finesse', 'smarts']
        attribute_icons = {'vigor': '🥊', 'finesse': '🎯', 'smarts': '🧠'}
        
        # Only consider attributes above minimum
        available_attributes = [attr for attr in attributes if getattr(self, attr) > 3]
        
        if not available_attributes:
            console.print("    [dim]All attributes at minimum (3), no loss applied[/dim]")
            return
        
        chosen_attr = random.choice(available_attributes)
        old_value = getattr(self, chosen_attr)
        setattr(self, chosen_attr, old_value - 1)
        new_value = getattr(self, chosen_attr)
        
        icon = attribute_icons.get(chosen_attr, '💀')
        console.print(
            f"    [bold red]{icon} Lost:[/bold red] "
            f"[bold cyan]{chosen_attr.title()}[/bold cyan] "
            f"[yellow]{old_value}[/yellow] → [bold red]{new_value}[/bold red]"
        )
    
    def calculate_derived_stats(self) -> None:
        """Calculate hit points, movement, and inventory capacity based on attributes."""
        self.max_hit_points = (self.vigor + self.finesse + self.smarts) // 3
        self.hit_points = self.max_hit_points
        # Base inventory slots equal to vigor score
        self.base_inventory_slots = self.vigor
        # Movement is average of vigor and finesse (yards per turn)
        self.movement = (self.vigor + self.finesse) // 2
    
    def allocate_skill_points(self) -> None:
        """Enhanced skill point allocation with Rich UI and skill descriptions."""
        if self.skill_points <= 0:
            console.print("[yellow]No skill points to allocate.[/yellow]")
            return
        
        while self.skill_points > 0:
            console.clear()
            
            # Header with remaining points
            header = Panel(
                f"[bold gold1]Skill Training for {self.name}[/bold gold1]\n"
                f"[sandy_brown]Remaining Points: {self.skill_points}[/sandy_brown]\n"
                f"[dim]Skills are capped at level 3[/dim]",
                title="[bold cyan]🎓 SKILL ALLOCATION[/bold cyan]",
                border_style="cyan"
            )
            console.print(header)
            
            # Create skills table organized by attribute
            skills_list = skill_manager.get_skill_list()
            
            # Group skills by attribute
            vigor_skills = []
            finesse_skills = []
            smarts_skills = []
            mixed_skills = []
            
            for i, (key, skill) in enumerate(skills_list, 1):
                current_level = self.skills.get(key, 0)
                skill_info = {
                    'number': i,
                    'key': key,
                    'skill': skill,
                    'level': current_level
                }
                
                if 'vigor' in skill.attribute.lower() and 'finesse' not in skill.attribute.lower():
                    vigor_skills.append(skill_info)
                elif 'finesse' in skill.attribute.lower() and 'vigor' not in skill.attribute.lower():
                    finesse_skills.append(skill_info)
                elif 'smarts' in skill.attribute.lower():
                    smarts_skills.append(skill_info)
                else:
                    mixed_skills.append(skill_info)
            
            # Display skill tables
            self._display_skill_category("VIGOR SKILLS", vigor_skills, "red")
            self._display_skill_category("FINESSE SKILLS", finesse_skills, "yellow")
            self._display_skill_category("SMARTS SKILLS", smarts_skills, "cyan")
            if mixed_skills:
                self._display_skill_category("MIXED SKILLS", mixed_skills, "magenta")
            
            console.print()
            console.print(Panel(
                "[bold]0.[/bold] Finish allocation (must spend all points)\n"
                "[bold]?[/bold] Show skill descriptions",
                border_style="green",
                padding=(0, 1)
            ))
            
            try:
                user_input = Prompt.ask(
                    f"\nSelect skill to improve, ? for help (0 to finish, {self.skill_points} points left)",
                    console=console
                )
                
                # Handle help command
                if user_input == "?" or user_input.lower() == "help":
                    self._show_skill_descriptions(skills_list)
                    continue
                
                # Convert to integer for skill selection
                choice = int(user_input)
                
                if choice == 0:
                    if self.skill_points > 0:
                        console.print(f"[red]⚠️  You must spend all {self.skill_points} skill points before continuing.[/red]")
                        Prompt.ask("Press Enter to continue", default="", console=console)
                        continue
                    else:
                        break
                
                if 1 <= choice <= len(skills_list):
                    skill_key, skill = skills_list[choice - 1]
                    current_level = self.skills.get(skill_key, 0)
                    
                    if current_level >= 3:
                        console.print(f"[red]❌ {skill.name} is already at maximum level (3).[/red]")
                        Prompt.ask("Press Enter to continue", default="", console=console)
                        continue
                    
                    # Show skill info before adding point
                    console.print(f"\n[bold cyan]📖 {skill.name}[/bold cyan]")
                    console.print(f"[dim]{skill.description}[/dim]")
                    console.print(f"[yellow]Attribute: {skill.attribute.title()}[/yellow]")
                    
                    # Add point to skill with animation
                    self.skills[skill_key] = current_level + 1
                    self.skill_points -= 1
                    
                    # Show skill improvement animation
                    console.print(f"\n[bold green]✨ {skill.name} improved![/bold green]")
                    
                    # Progress bar animation
                    with Progress(
                        TextColumn("[progress.description]"),
                        BarColumn(),
                        console=console,
                        transient=True
                    ) as progress:
                        task = progress.add_task(
                            f"Level {current_level} → {self.skills[skill_key]}", 
                            total=100
                        )
                        for i in range(100):
                            progress.update(task, advance=1)
                            time.sleep(0.01)
                    
                    console.print(f"[bold cyan]{skill.name}[/bold cyan] is now level [bold yellow]{self.skills[skill_key]}[/bold yellow]!")
                    time.sleep(1.5)  # Give more time to read the description
                
                else:
                    console.print("[red]Invalid selection.[/red]")
                    Prompt.ask("Press Enter to continue", default="", console=console)
                    
            except ValueError:
                console.print("[red]Invalid input. Enter a number, or ? for help.[/red]")
                Prompt.ask("Press Enter to continue", default="", console=console)
            except KeyboardInterrupt:
                console.print("[yellow]Skill allocation cancelled.[/yellow]")
                break
        
        console.print(f"\n[bold green]🎉 Skill allocation complete for {self.name}![/bold green]")
    
    def _show_skill_descriptions(self, skills_list: list):
        """Display all skill descriptions in a comprehensive help screen."""
        console.clear()
        
        # Header
        header = Panel(
            f"[bold gold1]Skill Reference Guide[/bold gold1]\n"
            f"[sandy_brown]Choose your path wisely, {self.name}[/sandy_brown]",
            title="[bold cyan]📚 SKILL DESCRIPTIONS[/bold cyan]",
            border_style="cyan"
        )
        console.print(header)
        
        # Group skills by attribute for organized display
        skill_groups = {
            'Vigor': [],
            'Finesse': [],
            'Smarts': [],
            'Mixed': []
        }
        
        for i, (key, skill) in enumerate(skills_list, 1):
            skill_entry = {
                'number': i,
                'name': skill.name,
                'description': skill.description,
                'current_level': self.skills.get(key, 0)
            }
            
            if 'vigor' in skill.attribute.lower() and 'finesse' not in skill.attribute.lower():
                skill_groups['Vigor'].append(skill_entry)
            elif 'finesse' in skill.attribute.lower() and 'vigor' not in skill.attribute.lower():
                skill_groups['Finesse'].append(skill_entry)
            elif 'smarts' in skill.attribute.lower():
                skill_groups['Smarts'].append(skill_entry)
            else:
                skill_groups['Mixed'].append(skill_entry)
        
        # Display each group
        group_colors = {
            'Vigor': 'red',
            'Finesse': 'yellow', 
            'Smarts': 'cyan',
            'Mixed': 'magenta'
        }
        
        for group_name, skills in skill_groups.items():
            if not skills:
                continue
                
            color = group_colors[group_name]
            
            # Create table for this attribute group
            table = Table(
                title=f"{group_name} Skills",
                box=box.ROUNDED,
                border_style=color,
                show_header=True,
                header_style=f"bold {color}"
            )
            table.add_column("#", style="dim", width=3, justify="center")
            table.add_column("Skill", style=f"bold {color}", width=20)
            table.add_column("Level", justify="center", width=6)
            table.add_column("Description", style="dim white", min_width=40)
            
            for skill in skills:
                # Show current level with visual indicator (all 5 levels)
                level = skill['current_level']
                if level > 0:
                    level_display = f"[bold yellow]{level}[/bold yellow]/5"
                else:
                    level_display = "[dim]0[/dim]/5"
                
                table.add_row(
                    str(skill['number']),
                    skill['name'],
                    level_display,
                    skill['description']
                )
            
            console.print(table)
            console.print()  # Add spacing between tables
        
        # Footer with instructions
        footer = Panel(
            "[bold white]💡 Skill Progression:[/bold white]\n"
            "• [dim]Level 0:[/dim] Untrained - Basic attempts possible\n"
            "• [dim yellow]Level 1:[/dim] Novice - Some training and practice\n"
            "• [yellow]Level 2:[/yellow] Trained - Regular practice and experience\n" 
            "• [bold yellow]Level 3:[/bold yellow] Skilled - Maximum at character creation\n"
            "• [bold green]Level 4:[/bold green] Expert - Advanced training (post-creation)\n"
            "• [bold bright_green]Level 5:[/bold bright_green] Master - Legendary expertise (post-creation)\n\n"
            "[bold white]💡 Training Tips:[/bold white]\n"
            "• Choose skills that match your character's background and goals\n"
            "• Higher levels give significantly better chances of success\n"
            "• Skills can be improved beyond level 3 through gameplay",
            title="[bold gold1]Training Wisdom[/bold gold1]",
            border_style="gold1"
        )
        console.print(footer)
        
        Prompt.ask("\n[bold sandy_brown]Press Enter to return to skill selection[/bold sandy_brown]", 
                  default="", console=console)
    
    def _display_skill_category(self, title: str, skills_list: list, color: str):
        """Display a category of skills in a Rich table."""
        if not skills_list:
            return
        
        table = Table(title=title, box=box.ROUNDED, border_style=color, show_header=True)
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("Skill", style=f"bold {color}", min_width=20)
        table.add_column("Level", justify="center", width=8)
        table.add_column("Progress", justify="center", width=12)
        
        for skill_info in skills_list:
            number = skill_info['number']
            skill = skill_info['skill']
            level = skill_info['level']
            
            # Create progress visualization showing all 5 levels
            progress_bar = "●" * level + "○" * (5 - level)
            
            # Color the progress based on level with expanded scale
            if level == 5:
                level_style = "bold bright_green"
                progress_style = "bold bright_green"
            elif level == 4:
                level_style = "bold green"
                progress_style = "bold green"
            elif level == 3:
                level_style = "bold yellow"
                progress_style = "bold yellow"
            elif level >= 2:
                level_style = "yellow"
                progress_style = "yellow"
            elif level == 1:
                level_style = "dim yellow"
                progress_style = "dim yellow"
            else:
                level_style = "dim"
                progress_style = "dim"
            
            table.add_row(
                str(number),
                skill.name,
                Text(str(level), style=level_style),
                Text(progress_bar, style=progress_style)
            )
        
        console.print(table)
    
    def get_skill_level(self, skill_key: str) -> int:
        """Get the level of a specific skill."""
        return self.skills.get(skill_key, 0)
    
    def display_character_sheet(self) -> None:
        """Display character sheet with Rich formatting and layout."""
        console.clear()
        
        # Character header with western flair
        header_content = (
            f"[bold gold1]{self.name.upper()}[/bold gold1]\n"
            f"[sandy_brown]Age {self.age} • Level {self.level} • Experience {self.experience}[/sandy_brown]\n"
            f"[yellow]💰 ${self.dollars}[/yellow]"
        )
        
        if self.skill_points > 0:
            header_content += f" • [cyan]📚 {self.skill_points} Skill Points[/cyan]"
        
        header_content += f"\n[dim]📍 {self.location}[/dim]"
        
        header = Panel(
            header_content,
            title="[bold red3] CHARACTER SHEET [/bold red3]",
            border_style="gold1",
            padding=(1, 2)
        )
        console.print(header)
        
        # Attributes panel
        attr_table = Table(box=box.ROUNDED, border_style="cyan", title="Core Attributes")
        attr_table.add_column("Attribute", style="bold cyan", width=12)
        attr_table.add_column("Score", justify="center", style="bold yellow", width=6)
        attr_table.add_column("Mod", justify="center", style="bold green", width=5)
        attr_table.add_column("Description", style="dim white")
        
        attr_table.add_row(
            "Vigor", 
            str(self.vigor), 
            f"{self.get_attribute_modifier(self.vigor):+d}",
            "Strength & Toughness"
        )
        attr_table.add_row(
            "Finesse", 
            str(self.finesse), 
            f"{self.get_attribute_modifier(self.finesse):+d}",
            "Agility & Coordination"
        )
        attr_table.add_row(
            "Smarts", 
            str(self.smarts), 
            f"{self.get_attribute_modifier(self.smarts):+d}",
            "Intelligence & Awareness"
        )
        
        attr_panel = Panel(attr_table, border_style="cyan")
        
        # Skills panel
        if self.skills:
            skills_table = Table(box=box.ROUNDED, border_style="green", title="Learned Skills")
            skills_table.add_column("Skill", style="bold green", min_width=18)
            skills_table.add_column("Level", justify="center", style="bold yellow", width=6)
            skills_table.add_column("Progress", justify="center", width=10)
            skills_table.add_column("Attribute", style="dim cyan", width=10)
            
            sorted_skills = sorted(self.skills.items(), key=lambda x: skill_manager.get_skill(x[0]).name if skill_manager.get_skill(x[0]) else x[0])
            
            for skill_key, level in sorted_skills:
                skill = skill_manager.get_skill(skill_key)
                if skill:
                    # Show all 5 possible levels (current max is 3 at creation, but can grow to 5)
                    progress_bar = "●" * level + "○" * (5 - level)
                    # Color progress based on level
                    if level == 5:
                        progress_style = "bold bright_green"  # Master level
                    elif level == 4:
                        progress_style = "bold green"         # Expert level  
                    elif level == 3:
                        progress_style = "bold yellow"        # Skilled level
                    elif level >= 2:
                        progress_style = "yellow"             # Trained level
                    elif level == 1:
                        progress_style = "dim yellow"         # Novice level
                    else:
                        progress_style = "dim white"          # Untrained
                    
                    skills_table.add_row(
                        skill.name,
                        str(level),
                        Text(progress_bar, style=progress_style),
                        skill.attribute
                    )
            
            skills_panel = Panel(skills_table, border_style="green")
        else:
            skills_panel = Panel(
                "[dim]No skills learned yet.\nSpend some time training![/dim]",
                title="[bold green]Skills[/bold green]",
                border_style="green"
            )
        
        # Status panel
        status_content = (
            f"[bold red]❤️  Health:[/bold red] {self.hit_points}/{self.max_hit_points}\n"
            f"[bold cyan]🏃 Movement:[/bold cyan] {self.movement} yards/turn\n"
            f"[bold yellow]🔫 Weapon:[/bold yellow] {self.weapon}\n"
            f"[bold blue]🛡️  Armor:[/bold blue] {self.armor}\n"
            f"[bold gold1]💰 Money:[/bold gold1] ${self.dollars}\n"
            f"{self.display_inventory_status()}"
        )
        
        # Show inventory contents if any
        if self.inventory:
            status_content += f"\n[bold cyan]📦 Carrying:[/bold cyan]"
            for item_name, quantity in sorted(self.inventory.items()):
                slots_used = self._get_item_slot_usage(item_name)
                if quantity > 1:
                    status_content += f"\n  • {item_name} x{quantity} ({slots_used * quantity} slots)"
                else:
                    status_content += f"\n  • {item_name} ({slots_used} slot{'s' if slots_used != 1 else ''})"
        
        status_panel = Panel(
            status_content,
            title="[bold sandy_brown]Status & Equipment[/bold sandy_brown]",
            border_style="sandy_brown"
        )
        
        # Display in columns
        console.print(Columns([attr_panel, skills_panel], equal=True))
        console.print(status_panel)
        
        # Footer with flavor text
        footer_text = f"[dim italic]The legend of {self.name} continues to grow in the dusty streets of {self.location}...[/dim italic]"
        console.print(f"\n{footer_text}")
    
    def get_attribute_modifier(self, attribute: int) -> int:
        """Get D&D-style modifier for an attribute."""
        return (attribute - 10) // 2
    
    # Inventory Management Methods
    def get_total_inventory_slots(self) -> int:
        """Get total available inventory slots."""
        return self.base_inventory_slots + self.bonus_inventory_slots
    
    def get_used_inventory_slots(self) -> int:
        """Calculate how many inventory slots are currently used."""
        # For now, each item takes 1 slot unless specified otherwise
        # This will be expanded when we add item definitions
        used_slots = 0
        for item_name, quantity in self.inventory.items():
            # Placeholder: all items take 1 slot each for now
            # Later we'll look up item definitions for actual slot usage
            item_slots = self._get_item_slot_usage(item_name)
            used_slots += item_slots * quantity
        return used_slots
    
    def get_available_inventory_slots(self) -> int:
        """Get number of unused inventory slots."""
        return self.get_total_inventory_slots() - self.get_used_inventory_slots()
    
    def _get_item_slot_usage(self, item_name: str) -> int:
        """Get how many slots an item uses (placeholder for future item system)."""
        # Placeholder logic - will be replaced with proper item definitions
        item_name_lower = item_name.lower()
        
        # Heavy weapons
        if 'rifle' in item_name_lower or 'shotgun' in item_name_lower:
            return 3
        elif 'pistol' in item_name_lower or 'revolver' in item_name_lower:
            return 2
        # Armor
        elif 'armor' in item_name_lower or 'vest' in item_name_lower:
            return 2
        # Backpacks (special case - they add slots rather than use them)
        elif 'backpack' in item_name_lower or 'saddlebags' in item_name_lower:
            return 0  # Backpacks don't use slots, they add them
        # Default: most items use 1 slot
        else:
            return 1
    
    def can_add_item(self, item_name: str, quantity: int = 1) -> bool:
        """Check if character has enough inventory space for an item."""
        item_slots = self._get_item_slot_usage(item_name)
        slots_needed = item_slots * quantity
        return self.get_available_inventory_slots() >= slots_needed
    
    def add_item(self, item_name: str, quantity: int = 1) -> bool:
        """Add item to inventory if there's space."""
        if not self.can_add_item(item_name, quantity):
            return False
        
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity
        
        # Handle special items that modify inventory capacity
        if 'backpack' in item_name.lower():
            self.bonus_inventory_slots += 5  # Backpack adds 5 slots
        elif 'saddlebags' in item_name.lower():
            self.bonus_inventory_slots += 8  # Saddlebags add more slots
        
        return True
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """Remove item from inventory."""
        if item_name not in self.inventory:
            return False
        
        if self.inventory[item_name] < quantity:
            return False
        
        # Handle special items that modify inventory capacity
        if 'backpack' in item_name.lower():
            self.bonus_inventory_slots -= 5 * quantity
        elif 'saddlebags' in item_name.lower():
            self.bonus_inventory_slots -= 8 * quantity
        
        self.inventory[item_name] -= quantity
        if self.inventory[item_name] <= 0:
            del self.inventory[item_name]
        
        return True
    
    def display_inventory_status(self) -> str:
        """Get a formatted string showing inventory status."""
        used = self.get_used_inventory_slots()
        total = self.get_total_inventory_slots()
        available = self.get_available_inventory_slots()
        
        if available <= 2:
            color = "red"
            status = "Nearly Full!"
        elif available <= 5:
            color = "yellow"
            status = "Getting Heavy"
        else:
            color = "green"
            status = "Plenty of Room"
        
        return f"[{color}]🎒 Inventory: {used}/{total} slots ({status})[/{color}]"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert character to dictionary for saving."""
        return {
            'name': self.name,
            'age': self.age,
            'level': self.level,
            'experience': self.experience,
            'dollars': self.dollars,
            'skill_points': self.skill_points,
            'vigor': self.vigor,
            'finesse': self.finesse,
            'smarts': self.smarts,
            'hit_points': self.hit_points,
            'max_hit_points': self.max_hit_points,
            'movement': self.movement,  # Add movement to save data
            'skills': self.skills,  # Only saves skills with points > 0
            'inventory': self.inventory,  # Now a dict of item_name: quantity
            'base_inventory_slots': self.base_inventory_slots,
            'bonus_inventory_slots': self.bonus_inventory_slots,
            'weapon': self.weapon,
            'armor': self.armor,
            'location': self.location
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load character from dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Handle legacy save files that might not have movement
        if not hasattr(self, 'movement') or self.movement == 0:
            self.calculate_derived_stats()  # This will recalculate movement
        
        # Handle legacy save files that might have old inventory format
        if isinstance(self.inventory, list):
            # Convert old list format to new dict format
            old_inventory = self.inventory
            self.inventory = {}
            for item in old_inventory:
                if item in self.inventory:
                    self.inventory[item] += 1
                else:
                    self.inventory[item] = 1