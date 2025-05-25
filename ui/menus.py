"""Menu systems for Western RPG game.

This module contains menu classes and functions for handling user navigation,
input validation, and menu display throughout the game.
"""

import time
from typing import Callable, Dict, List, Optional
from ui.display import (
    clear_screen, display_title_screen, display_menu_header, 
    display_credits, pause_with_message, get_numeric_choice
)


class MenuOption:
    """Represents a single menu option.
    
    Attributes:
        text: The display text for the option.
        action: Function to call when option is selected.
        enabled: Whether the option is currently available.
    """
    
    def __init__(self, text: str, action: Callable[[], None], enabled: bool = True) -> None:
        """Initialize a menu option.
        
        Args:
            text: Display text for the option.
            action: Function to execute when selected.
            enabled: Whether option is selectable.
        """
        self.text = text
        self.action = action
        self.enabled = enabled


class Menu:
    """Generic menu class for handling user choices.
    
    Provides a reusable menu system with customizable options and display.
    
    Attributes:
        title: Menu title to display.
        options: List of menu options.
        show_title_screen: Whether to show the game title before menu.
    """
    
    def __init__(self, title: str, show_title_screen: bool = False) -> None:
        """Initialize a menu.
        
        Args:
            title: Title to display for this menu.
            show_title_screen: Whether to show game title screen.
        """
        self.title = title
        self.options: List[MenuOption] = []
        self.show_title_screen = show_title_screen
    
    def add_option(self, text: str, action: Callable[[], None], enabled: bool = True) -> None:
        """Add an option to the menu.
        
        Args:
            text: Display text for the option.
            action: Function to execute when selected.
            enabled: Whether option is selectable.
        """
        self.options.append(MenuOption(text, action, enabled))
    
    def display(self) -> None:
        """Display the menu."""
        clear_screen()
        
        if self.show_title_screen:
            display_title_screen()
        
        display_menu_header(self.title)
        
        for i, option in enumerate(self.options, 1):
            if option.enabled:
                print(f"{i}. {option.text}")
            else:
                print(f"{i}. {option.text} (Disabled)")
        
        print("="*50)
    
    def get_choice(self) -> Optional[int]:
        """Get user's menu choice.
        
        Returns:
            Selected option number (1-based) or None for invalid choice.
        """
        try:
            choice = int(input("\nWhat's your choice, partner? ").strip())
            if 1 <= choice <= len(self.options):
                return choice
            else:
                print("\nInvalid choice. Try again, stranger.")
                time.sleep(1)
                return None
        except ValueError:
            print("\nInvalid choice. Try again, stranger.")
            time.sleep(1)
            return None
    
    def run(self) -> None:
        """Run the menu loop until a valid choice is made."""
        while True:
            self.display()
            choice = self.get_choice()
            
            if choice is not None:
                option = self.options[choice - 1]
                if option.enabled:
                    option.action()
                    break
                else:
                    print("\nThat option is not available right now.")
                    time.sleep(1)


def show_main_menu(game_instance) -> str:
    """Show main menu and return user choice.
    
    Args:
        game_instance: Reference to the main game instance.
        
    Returns:
        User's menu choice as string.
    """
    clear_screen()
    display_title_screen()
    
    display_menu_header("MAIN MENU")
    print("1. New Game")
    print("2. Load Game")
    print("3. Credits")
    print("4. Quit")
    print("="*50)
    
    return input("\nWhat's your choice, partner? ").strip()


def show_attribute_rolling_menu() -> str:
    """Show attribute rolling options menu.
    
    Returns:
        User's choice as string.
    """
    print("\nDo you want to:")
    print("1. Keep these attributes")
    print("2. Roll again")
    print("3. Manually set attributes (for testing)")
    
    return input("\nYour choice: ").strip()


def show_character_creation_intro() -> str:
    """Show character creation introduction and get character name.
    
    Returns:
        Character name entered by user.
    """
    clear_screen()
    
    from ui.display import display_section_header, type_text
    
    display_section_header("WELCOME TO THE OLD WEST")
    
    type_text("\nYou step off the dusty stagecoach in the frontier town of Whiskey Hollow.")
    type_text("The sun beats down mercilessly as you adjust your hat and look around.")
    type_text("This is not where your story begins, but it is where your vengeance does...")
    
    # Character name input
    print("\n" + "-"*50)
    while True:
        name = input("What do folks call you? ").strip()
        if name and len(name) <= 20:
            return name
        print("Enter a valid name (1-20 characters).")


def show_attribute_rolling_screen() -> None:
    """Display the attribute rolling screen setup."""
    clear_screen()
    
    from ui.display import display_section_header, display_loading_animation
    
    display_section_header("ROLLING YOUR ATTRIBUTES")
    print("Rolling 4d6 and taking the highest 3 for each attribute...")
    print("\nPress Enter to roll...")
    input()
    
    display_loading_animation("Rolling dice", 3, 0.5)


def get_manual_attributes() -> Dict[str, int]:
    """Get manually entered attributes for testing.
    
    Returns:
        Dictionary of attribute names to values.
    """
    print("\nManual Attribute Setting (Enter values 3-18)")
    attributes = {}
    attribute_names = ['vigor', 'finesse', 'smarts']
    
    for attr_name in attribute_names:
        while True:
            try:
                value = int(input(f"{attr_name.capitalize()}: "))
                if 3 <= value <= 18:
                    attributes[attr_name] = value
                    break
                else:
                    print("Value must be between 3 and 18.")
            except ValueError:
                print("Please enter a valid number.")
    
    return attributes


def show_character_finalization(character) -> None:
    """Show character creation completion screen.
    
    Args:
        character: The created Character instance.
    """
    clear_screen()
    
    from ui.display import display_section_header, type_text, display_inventory, format_money
    
    display_section_header("CHARACTER CREATION COMPLETE")
    
    character.display_character_sheet()
    
    print(f"\nWelcome to Whiskey Hollow, {character.name}!")
    type_text("You've got a few dollars in your pocket, some basic gear, and a world of possibilities ahead.")
    
    display_inventory(character.inventory, "You're carrying")
    print(f"\nStarting dollars: {format_money(character.dollars)}")
    
    pause_with_message("Press Enter to begin your adventure...")


def show_save_game_list(save_files: List[str]) -> int:
    """Show list of save games and get user selection.
    
    Args:
        save_files: List of save file names.
        
    Returns:
        Selected file index (0-based) or -1 for invalid selection.
    """
    print("\nSaved Games:")
    for i, save_file in enumerate(save_files, 1):
        # Extract character name from filename
        char_name = save_file.replace('_save.json', '').replace('_', ' ').title()
        print(f"{i}. {char_name}")
    
    try:
        choice = int(input("\nSelect save file (number): "))
        if 1 <= choice <= len(save_files):
            return choice - 1  # Convert to 0-based index
        else:
            print("Invalid selection.")
            time.sleep(1)
            return -1
    except ValueError:
        print("Invalid input.")
        time.sleep(1)
        return -1


def show_credits_screen() -> None:
    """Display the credits screen."""
    display_credits()
    pause_with_message("Press Enter to return to main menu...")


def show_quit_message() -> None:
    """Display quit game message."""
    print("\nThanks for playing, partner!")
    print("See you on the frontier...")


def show_no_saves_message() -> None:
    """Display message when no save files are found."""
    print("\nNo saved games found.")
    time.sleep(2)


def show_load_success_message(character_name: str) -> None:
    """Show successful load message.
    
    Args:
        character_name: Name of the loaded character.
    """
    print(f"\nGame loaded successfully!")
    print(f"Welcome back, {character_name}!")
    time.sleep(2)


def show_load_error_message(error: str) -> None:
    """Show load error message.
    
    Args:
        error: Error message to display.
    """
    print(f"\nError loading save file: {error}")
    time.sleep(2)


def show_game_placeholder() -> None:
    """Show placeholder for main game content."""
    print("\n[Game would continue here...]")
    pause_with_message("Press Enter to return to main menu...")