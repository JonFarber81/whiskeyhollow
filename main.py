"""Simple Western RPG Character Creator with Rich Terminal UI."""

import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
from rich import box

from character import Character, console  # Import shared console
from file_manager import SaveManager
from name_generator import name_generator
import random

def show_title():
    """Display the game title with Rich styling."""
    title_art = """
██╗    ██╗██╗  ██╗██╗███████╗██╗  ██╗███████╗██╗   ██╗
██║    ██║██║  ██║██║██╔════╝██║ ██╔╝██╔════╝╚██╗ ██╔╝
██║ █╗ ██║███████║██║███████╗█████╔╝ █████╗   ╚████╔╝ 
██║███╗██║██╔══██║██║╚════██║██╔═██╗ ██╔══╝    ╚██╔╝  
╚███╔███╔╝██║  ██║██║███████║██║  ██╗███████╗   ██║   
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   

██╗  ██╗ ██████╗ ██╗     ██╗      ██████╗ ██╗    ██╗
██║  ██║██╔═══██╗██║     ██║     ██╔═══██╗██║    ██║
███████║██║   ██║██║     ██║     ██║   ██║██║ █╗ ██║
██╔══██║██║   ██║██║     ██║     ██║   ██║██║███╗██║
██║  ██║╚██████╔╝███████╗███████╗╚██████╔╝╚███╔███╔╝
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝ ╚═════╝  ╚══╝╚══╝ 
    """
    
    # Create title with western colors
    title_text = Text(title_art, style="bold gold1")
    subtitle = Text("~ RECKONING ~", style="bold red3")
    tagline = Text("A tale of vengeance in the West", style="italic sandy_brown")
    
    # Create decorative border
    border_content = Align.center(
        Text("🤠 " + "─" * 50 + " 🤠", style="dim yellow")
    )
    
    console.clear()
    console.print()
    console.print(Align.center(title_text))
    console.print()
    console.print(Align.center(subtitle))
    console.print()
    console.print(Align.center(tagline))
    console.print()
    console.print(border_content)
    console.print()


def get_character_name() -> str:
    """Get character name from user with Rich styling and random name option."""
    console.print(Panel(
        "[bold sandy_brown]What's your name, stranger?[/bold sandy_brown]\n"
        "[dim]Enter a name for your character (1-20 characters)\n"
        "Or type 'random' to generate a random Western name[/dim]",
        title="[bold gold1]Character Creation[/bold gold1]",
        border_style="gold1"
    ))
    
    while True:
        name_input = Prompt.ask("Character name (or 'random')", console=console)
        
        if name_input.lower() == 'random':
            # Generate random name
            console.print("\n[bold gold1]🎲 Generating a random name...[/bold gold1]")
            
            random_name = name_generator.generate_random_name()
            
            # Show the generated name with flair
            name_panel = Panel(
                f"[bold sandy_brown]{random_name}[/bold sandy_brown]",
                title="[bold gold1]🎯 Random Name Generated[/bold gold1]",
                border_style="gold1",
                padding=(1, 2)
            )
            console.print(name_panel)
            
            # Ask if they want to keep it
            keep_name = Prompt.ask(
                "Keep this name?",
                choices=["y", "n", "yes", "no"],
                default="y",
                console=console
            )
            
            if keep_name.lower() in ['y', 'yes']:
                return random_name
            else:
                console.print("[yellow]Let's try again...[/yellow]")
                # Generate another or let them type manually
                choice = Prompt.ask(
                    "Generate another random name or enter manually?",
                    choices=["random", "manual", "r", "m"],
                    default="random",
                    console=console
                )
                if choice.lower() in ['random', 'r']:
                    continue  # Will generate another random name
                # If manual, fall through to normal name input
                
        elif name_input and len(name_input) <= 20:
            return name_input
        else:
            console.print("[red]Please enter a valid name (1-20 characters) or 'random'[/red]")


def get_character_age() -> int:
    """Get character age from user with Rich table."""
    age_table = Table(title="Age Categories", box=box.ROUNDED, border_style="gold1")
    age_table.add_column("Age Range", style="bold cyan", justify="center")
    age_table.add_column("Category", style="bold yellow", justify="center")
    age_table.add_column("Effects", style="green")
    
    age_table.add_row("14-22", "Young", "Fewer skills, good attributes")
    age_table.add_row("23-34", "Prime", "Balanced growth")
    age_table.add_row("35-52", "Experienced", "Many skills, declining body")
    age_table.add_row("53-57", "Elder", "Maximum skills, frail body")
    
    console.print()
    console.print(age_table)
    console.print()
    
    while True:
        age = IntPrompt.ask(
            "[bold sandy_brown]How old are you, partner?[/bold sandy_brown]",
            console=console,
            default=25
        )
        if 14 <= age <= 57:
            return age
        console.print("[red]Age must be between 14 and 57.[/red]")


def display_rolled_attributes(character: Character):
    """Display character attributes after rolling."""
    attr_table = Table(title="Character Attributes", box=box.HEAVY_EDGE, border_style="gold1")
    attr_table.add_column("Attribute", style="bold cyan", justify="left")
    attr_table.add_column("Score", style="bold yellow", justify="center")
    attr_table.add_column("Modifier", style="bold green", justify="center")
    attr_table.add_column("Description", style="dim white")
    
    # Vigor
    vigor_mod = character.get_attribute_modifier(character.vigor)
    attr_table.add_row(
        "Vigor", 
        str(character.vigor), 
        f"{vigor_mod:+d}",
        "Physical strength & toughness"
    )
    
    # Finesse
    finesse_mod = character.get_attribute_modifier(character.finesse)
    attr_table.add_row(
        "Finesse", 
        str(character.finesse), 
        f"{finesse_mod:+d}",
        "Agility & coordination"
    )
    
    # Smarts
    smarts_mod = character.get_attribute_modifier(character.smarts)
    attr_table.add_row(
        "Smarts", 
        str(character.smarts), 
        f"{smarts_mod:+d}",
        "Intelligence & awareness"
    )
    
    console.print()
    console.print(attr_table)
    console.print(f"\n💰 [bold yellow]Starting Money:[/bold yellow] ${character.dollars}")


def set_manual_attributes(character: Character):
    """Set attributes manually with Rich prompts."""
    console.print(Panel(
        "[bold sandy_brown]Set your base attributes manually[/bold sandy_brown]\n"
        "[dim]Each attribute should be between 3-18[/dim]",
        title="[bold gold1]Manual Attribute Setting[/bold gold1]",
        border_style="gold1"
    ))
    
    while True:
        try:
            vigor = IntPrompt.ask("Vigor (3-18)", console=console, default=10)
            finesse = IntPrompt.ask("Finesse (3-18)", console=console, default=10)
            smarts = IntPrompt.ask("Smarts (3-18)", console=console, default=10)
            
            if all(3 <= attr <= 18 for attr in [vigor, finesse, smarts]):
                character.vigor = vigor
                character.finesse = finesse
                character.smarts = smarts
                character.calculate_derived_stats()
                break
            else:
                console.print("[red]All attributes must be between 3 and 18.[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Attribute setting cancelled.[/yellow]")
            return


def create_new_character() -> Character:
    """Create a new character with Rich UI."""
    console.clear()
    show_title()
    
    name = get_character_name()
    age = get_character_age()
    
    character = Character(name)
    character.age = age
    
    
    console.print(f"\n✨ [bold green]Character Created![/bold green] [bold sandy_brown]{name}[/bold sandy_brown], age [bold yellow]{age}[/bold yellow]")
    
    # Attribute rolling loop
    while True:
        console.print("\n🎲 [bold gold1]Rolling base attributes...[/bold gold1]")
        
        # Simulate rolling with progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Rolling dice...", total=100)
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.001)
        
        character.roll_attributes()
        display_rolled_attributes(character)
        
        # Choice menu with Rich styling
        choices_panel = Panel(
            "[bold]1.[/bold] Keep these stats and apply age effects\n"
            "[bold]2.[/bold] Roll again\n"
            "[bold]3.[/bold] Set manually",
            title="[bold gold1]What would you like to do?[/bold gold1]",
            border_style="gold1"
        )
        console.print(choices_panel)
        
        choice = Prompt.ask("Choice", choices=["1", "2", "3"], default="1", console=console)
        
        if choice == "1":
            # Apply age effects
            console.print("\n⏳ [bold gold1]Applying age effects...[/bold gold1]")
            character.apply_age_effects()
            
            # Skill allocation
            console.print("\n📚 [bold gold1]Time to learn some skills...[/bold gold1]")
            Prompt.ask("Press Enter to continue to skill allocation", default="", console=console)
            character.allocate_skill_points()
            
            character.display_character_sheet()
            break
        elif choice == "2":
            continue
        elif choice == "3":
            set_manual_attributes(character)
            character.apply_age_effects()
            
            console.print("\n📚 [bold gold1]Time to learn some skills...[/bold gold1]")
            Prompt.ask("Press Enter to continue to skill allocation", default="", console=console)
            character.allocate_skill_points()
            
            character.display_character_sheet()
            break
    
    return character

def create_random_character() -> Character:
    """Create a completely random character with Rich UI."""
    console.clear()
    show_title()
    
    console.print(Panel(
        "[bold gold1]🎲 Creating a Random Character[/bold gold1]\n"
        "[sandy_brown]Let fate decide your destiny in the West...[/sandy_brown]",
        title="[bold cyan]RANDOM GENERATION[/bold cyan]",
        border_style="cyan"
    ))
    
    # Generate random name (no gender prompt needed - pick randomly)
    console.print("\n[bold gold1]🎯 Rolling for identity...[/bold gold1]")
    
    with console.status("[bold]Consulting the fates...[/bold]", spinner="dots"):
        time.sleep(0.5)  # Dramatic pause
    
    # Randomly pick gender and generate name
    gender = random.choice(['male', 'female'])
    name = name_generator.generate_random_name(gender)
    
    console.print(f"[bold sandy_brown]Name:[/bold sandy_brown] {name}")
    
    # Generate random age (weighted toward more interesting ranges)
    age_weights = {
        range(14, 23): 15,  # Young - less common
        range(23, 35): 35,  # Prime - most common  
        range(35, 53): 30,  # Experienced - common
        range(53, 58): 20   # Elder - less common
    }
    
    # Pick weighted random age
    age_ranges = []
    weights = []
    for age_range, weight in age_weights.items():
        age_ranges.append(age_range)
        weights.append(weight)
    
    chosen_range = random.choices(age_ranges, weights=weights)[0]
    age = random.choice(list(chosen_range))
    
    console.print(f"[bold sandy_brown]Age:[/bold sandy_brown] {age}")
    
    # Create character
    character = Character(name)
    character.age = age
    
    # Roll attributes with animation
    console.print(f"\n[bold gold1]🎲 Rolling attributes for {name}...[/bold gold1]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Rolling dice...", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.005)
    
    character.roll_attributes()
    display_rolled_attributes(character)
    
    # Apply age effects
    console.print(f"\n[bold gold1]⏳ Applying life experience...[/bold gold1]")
    character.apply_age_effects()
    
    # Random skill allocation
    console.print(f"\n[bold gold1]📚 Learning skills randomly...[/bold gold1]")
    character.allocate_skill_points_randomly()
    
    # Final character sheet
    console.print(f"\n[bold green]🌟 Behold your random character![/bold green]")
    time.sleep(1)
    character.display_character_sheet()
    
    return character


def create_random_character_quick() -> Character:
    """Create a random character with minimal UI for batch generation."""
    # Randomly pick gender and generate name
    gender = random.choice(['male', 'female'])
    name = name_generator.generate_random_name(gender)
    
    # Generate weighted random age
    age_weights = {
        range(14, 23): 15,
        range(23, 35): 35,
        range(35, 53): 30,
        range(53, 58): 20
    }
    
    age_ranges, weights = zip(*age_weights.items())
    chosen_range = random.choices(age_ranges, weights=weights)[0]
    age = random.choice(list(chosen_range))
    
    # Create and setup character
    character = Character(name)
    character.age = age
    character.roll_attributes()
    character.apply_age_effects()
    character.allocate_skill_points_randomly()
    
    return character

def load_character_rich(save_manager: SaveManager) -> Character:
    """Load character with Rich interface."""
    saves = save_manager.list_save_files()
    
    if not saves:
        console.print(Panel(
            "[bold red]No saved characters found in Whiskey Hollow.[/bold red]\n"
            "[dim]Create a new character to get started![/dim]",
            title="[bold gold1]No Saves Found[/bold gold1]",
            border_style="red"
        ))
        Prompt.ask("Press Enter to continue", default="", console=console)
        return None
    
    # Create saves table
    saves_table = Table(title="Saved Characters", box=box.HEAVY_HEAD, border_style="gold1")
    saves_table.add_column("#", style="bold cyan", justify="center")
    saves_table.add_column("Name", style="bold yellow")
    saves_table.add_column("Age", justify="center", style="cyan")
    saves_table.add_column("Level", justify="center", style="green")
    saves_table.add_column("Money", justify="right", style="gold1")
    saves_table.add_column("Skills", justify="center", style="sandy_brown")
    
    for i, filename in enumerate(saves, 1):
        info = save_manager.get_save_info(filename)
        if info:
            saves_table.add_row(
                str(i),
                info['name'],
                str(info['age']),
                str(info['level']),
                f"${info['dollars']}",
                f"{info['skill_points']} SP"
            )
        else:
            saves_table.add_row(str(i), filename, "?", "?", "?", "?")
    
    console.print()
    console.print(saves_table)
    
    try:
        choice = IntPrompt.ask(
            f"Select character (1-{len(saves)})",
            console=console,
            default=1
        )
        if 1 <= choice <= len(saves):
            character = save_manager.load_character(saves[choice - 1])
            if character:
                console.print(f"[bold green]✅ {character.name} loaded successfully![/bold green]")
            return character
        else:
            console.print("[red]Invalid selection.[/red]")
    except (ValueError, KeyboardInterrupt):
        console.print("[yellow]Loading cancelled.[/yellow]")
    
    return None


def main():
    """Main program loop with Rich interface."""
    save_manager = SaveManager()
    current_character = None
    
    while True:
        console.clear()
        show_title()
        
        # Current character status
        if current_character:
            status_panel = Panel(
                f"[bold gold1]{current_character.name}[/bold gold1] • "
                f"Age {current_character.age} • "
                f"Level {current_character.level} • "
                f"${current_character.dollars}",
                title="[bold sandy_brown]Current Character[/bold sandy_brown]",
                border_style="sandy_brown"
            )
            console.print(status_panel)
        
        # Main menu
        menu_options = [
            "[bold]1.[/bold] 🆕 Create New Character",
            "[bold]2.[/bold] 🎲 Create Random Character", 
            "[bold]3.[/bold] 📂 Load Character",
        ]

        if current_character:
            menu_options.extend([
                "[bold]4.[/bold] 📋 View Character Sheet",
                "[bold]5.[/bold] 💾 Save Character"
            ])

        menu_options.append("[bold]0.[/bold] 🚪 Quit")

        # Update the choice handling:
        valid_choices = ["1", "2", "3", "0"]
        if current_character:
            valid_choices.extend(["4", "5"])

        menu_panel = Panel(
            "\n".join(menu_options),
            title="[bold gold1]Main Menu[/bold gold1]",
            border_style="gold1",
            padding=(1, 2)
        )
        console.print(menu_panel)        
        choice = Prompt.ask("Choice", choices=valid_choices, console=console)

        if choice == "1":
            current_character = create_new_character()
            if current_character:
                console.print(f"\n[bold green]🎉 {current_character.name} is ready for adventure![/bold green]")
                Prompt.ask("Press Enter to continue", default="", console=console)

        elif choice == "2":
            current_character = create_random_character()
            if current_character:
                console.print(f"\n[bold green]🎉 Random character {current_character.name} is ready for adventure![/bold green]")
                Prompt.ask("Press Enter to continue", default="", console=console)

        elif choice == "3":
            loaded_char = load_character_rich(save_manager)
            if loaded_char:
                current_character = loaded_char
                Prompt.ask("Press Enter to continue", default="", console=console)

        elif choice == "4" and current_character:
            current_character.display_character_sheet()
            Prompt.ask("\nPress Enter to continue", default="", console=console)

        elif choice == "5" and current_character:
            with console.status("[bold gold1]Saving character...[/bold gold1]"):
                success = save_manager.save_character(current_character)
            
            if success:
                console.print("[bold green]✅ Character saved successfully![/bold green]")
            else:
                console.print("[bold red]❌ Failed to save character.[/bold red]")
            Prompt.ask("Press Enter to continue", default="", console=console)

        elif choice == "0":
            console.print("\n[bold gold1]Thanks for visiting Whiskey Hollow, partner![/bold gold1]")
            console.print("[dim]May your aim be true and your legend grow...[/dim] 🤠")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Until we meet again, stranger...[/bold red] 🌅")