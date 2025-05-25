"""Display utilities for Western RPG game.

This module contains functions for screen management, text effects, and
visual elements like ASCII art and formatting utilities.
"""

import os
import time


def clear_screen() -> None:
    """Clear the terminal screen.
    
    Uses appropriate command for Windows (cls) or Unix-like systems (clear).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def type_text(text: str, delay: float = 0.03) -> None:
    """Print text with typewriter effect.
    
    Args:
        text: The text to display.
        delay: Delay between characters in seconds.
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def display_title_screen() -> None:
    """Display ASCII art title screen.
    
    Shows the game's title and subtitle in ASCII art format.
    """
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

                    ~ RECKONING ~
                    
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░                                      ░
        ░    A tale of vengeance in the West   ░
        ░                                      ░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

    """
    
    print(title_art)


def display_section_header(title: str, width: int = 60) -> None:
    """Display a formatted section header.
    
    Args:
        title: The title to display.
        width: Width of the header box. Defaults to 60.
    """
    print("\n" + "="*width)
    print(title.center(width))
    print("="*width)


def display_menu_header(title: str, width: int = 50) -> None:
    """Display a formatted menu header.
    
    Args:
        title: The menu title to display.
        width: Width of the header box. Defaults to 50.
    """
    print("\n\n" + "="*width)
    print(title.center(width))
    print("="*width)


def display_credits() -> None:
    """Display game credits screen.
    
    Shows information about the game and its developer.
    """
    clear_screen()
    print("\n" + "="*50)
    print("CREDITS".center(50))
    print("="*50)
    print("\nWhiskey Hollow - A Western RPG")
    print("Developed by: Jon Farber")
    print("Python Version: 3.x")
    print("\n" + "="*50)


def pause_with_message(message: str = "Press Enter to continue...") -> None:
    """Pause execution with a message.
    
    Args:
        message: Message to display before pausing.
    """
    input(f"\n{message}")


def display_loading_animation(message: str = "Loading", dots: int = 3, delay: float = 0.5) -> None:
    """Display a simple loading animation.
    
    Args:
        message: Base message to display.
        dots: Number of dots to animate.
        delay: Delay between dot animations.
    """
    print(f"\n{message}", end="")
    for i in range(dots):
        print("." * (i + 1), end="", flush=True)
        time.sleep(delay)
    print("\n")


def format_money(amount: int) -> str:
    """Format money amount with dollar sign.
    
    Args:
        amount: Dollar amount to format.
        
    Returns:
        Formatted money string.
    """
    return f"${amount}"


def display_inventory(items: list, title: str = "Inventory") -> None:
    """Display a formatted inventory list.
    
    Args:
        items: List of items to display.
        title: Title for the inventory display.
    """
    print(f"\n{title}:")
    if not items:
        print("  (Empty)")
    else:
        for item in items:
            print(f"  - {item}")


def get_yes_no_input(prompt: str) -> bool:
    """Get yes/no input from user.
    
    Args:
        prompt: Question to ask the user.
        
    Returns:
        True for yes, False for no.
    """
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def get_numeric_choice(prompt: str, min_val: int, max_val: int) -> int:
    """Get a numeric choice within a specified range.
    
    Args:
        prompt: Prompt to display to user.
        min_val: Minimum valid value.
        max_val: Maximum valid value.
        
    Returns:
        Valid numeric choice.
    """
    while True:
        try:
            choice = int(input(prompt))
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Please enter a valid number.")