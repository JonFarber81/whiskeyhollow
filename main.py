"""Main game module for Western RPG.

This module contains the main game class and entry point for Whiskey Hollow,
a Western-themed RPG game featuring character creation, save/load functionality,
and story-driven gameplay.
"""

import random
import time
import os
import json
from datetime import datetime
from typing import Optional, List

# Import the Character class from our new module
from character import Character


class WesternRPG:
    """Main game class for the Western RPG.
    
    Handles the game loop, menus, character creation, and save/load functionality.
    Provides the main interface between the player and the game world.
    
    Attributes:
        player: The current player character (None if no character loaded).
        game_running: Boolean flag controlling the main game loop.
    """
    
    def __init__(self) -> None:
        """Initialize the game."""
        self.player: Optional[Character] = None
        self.game_running: bool = True
        
    def clear_screen(self) -> None:
        """Clear the terminal screen.
        
        Uses appropriate command for Windows (cls) or Unix-like systems (clear).
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def type_text(self, text: str, delay: float = 0.03) -> None:
        """Print text with typewriter effect.
        
        Args:
            text: The text to display.
            delay: Delay between characters in seconds.
        """
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def display_title_screen(self) -> None:
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
    
    def main_menu(self) -> None:
        """Display main menu and handle selection.
        
        Main game loop that displays the menu and processes user choices
        until the player quits the game.
        """
        while self.game_running:
            self.clear_screen()
            self.display_title_screen()
            
            print("\n\n" + "="*50)
            print("MAIN MENU".center(50))
            print("="*50)
            print("1. New Game")
            print("2. Load Game")
            print("3. Credits")
            print("4. Quit")
            print("="*50)
            
            choice = input("\nWhat's your choice, partner? ").strip()
            
            if choice == "1":
                self.new_game()
            elif choice == "2":
                self.load_game()
            elif choice == "3":
                self.show_credits()
            elif choice == "4":
                self.quit_game()
            else:
                print("\nInvalid choice. Try again, stranger.")
                time.sleep(1)
    
    def new_game(self) -> None:
        """Start character creation process.
        
        Handles the initial game introduction and character name input,
        then proceeds to attribute rolling.
        """
        self.clear_screen()
        
        print("\n" + "="*60)
        print("WELCOME TO THE OLD WEST".center(60))
        print("="*60)
        
        self.type_text("\nYou step off the dusty stagecoach in the frontier town of Whiskey Hollow.")
        self.type_text("The sun beats down mercilessly as you adjust your hat and look around.")
        self.type_text("This is not where your story begins, but it is where your vengeance does...")
        
        # Character name input
        print("\n" + "-"*50)
        while True:
            name = input("What do folks call you? ").strip()
            if name and len(name) <= 20:
                break
            print("Enter a valid name (1-20 characters).")
        
        self.player = Character(name)
        
        print(f"\nWell howdy, {name}! Time to see what you're made of...")
        input("\nPress Enter to roll your attributes...")
        
        self.attribute_rolling_process()
    
    def attribute_rolling_process(self) -> None:
        """Handle the attribute rolling with player choice.
        
        Allows the player to roll attributes multiple times, manually set them
        for testing, or accept the current roll. Continues until player accepts.
        """
        while True:
            self.clear_screen()
            print("\n" + "="*60)
            print("ROLLING YOUR ATTRIBUTES".center(60))
            print("="*60)
            print("Rolling 4d6 and taking the highest 3 for each attribute...")
            print("\nPress Enter to roll...")
            input()
            
            # Animate the rolling process
            print("\nRolling dice...")
            for i in range(3):
                print("." * (i + 1), end="", flush=True)
                time.sleep(0.5)
            print("\n")
            
            if self.player:
                self.player.roll_attributes()
                self.player.display_character_sheet()
            
            print("\nDo you want to:")
            print("1. Keep these attributes")
            print("2. Roll again")
            print("3. Manually set attributes (for testing)")
            
            choice = input("\nYour choice: ").strip()
            
            if choice == "1":
                break
            elif choice == "2":
                continue
            elif choice == "3":
                self.manual_attribute_setting()
                break
            else:
                print("Invalid choice. Keeping current attributes.")
                time.sleep(1)
                break
        
        self.finalize_character()
    
    def manual_attribute_setting(self) -> None:
        """Allow manual attribute setting for testing.
        
        Prompts the player to enter specific values for each attribute,
        useful for testing specific character builds.
        """
        print("\nManual Attribute Setting (Enter values 3-18)")
        attributes = ['vigor', 'finesse', 'smarts']
        
        if not self.player:
            return
            
        for attr in attributes:
            while True:
                try:
                    value = int(input(f"{attr.capitalize()}: "))
                    if 3 <= value <= 18:
                        setattr(self.player, attr, value)
                        break
                    else:
                        print("Value must be between 3 and 18.")
                except ValueError:
                    print("Please enter a valid number.")
        
        self.player.calculate_derived_stats()
    
    def finalize_character(self) -> None:
        """Complete character creation.
        
        Displays the final character sheet, shows starting equipment,
        saves the character, and provides transition to main game.
        """
        if not self.player:
            return
            
        self.clear_screen()
        print("\n" + "="*60)
        print("CHARACTER CREATION COMPLETE".center(60))
        print("="*60)
        
        self.player.display_character_sheet()
        
        print(f"\nWelcome to Whiskey Hollow, {self.player.name}!")
        self.type_text("You've got a few dollars in your pocket, some basic gear, and a world of possibilities ahead.")
        
        # Starting equipment flavor text
        print(f"\nYou're carrying:")
        for item in self.player.inventory:
            print(f"  - {item}")
        
        print(f"\nStarting dollars: ${self.player.dollars}")
        
        input("\nPress Enter to begin your adventure...")
        
        # Save the character
        self.save_character()
        
        # Here you would transition to the main game
        print("\n[Game would continue here...]")
        input("Press Enter to return to main menu...")
    
    def save_character(self) -> None:
        """Save character data to file.
        
        Creates a saves directory if needed and saves character data
        as JSON with timestamp.
        """
        if not self.player:
            return
            
        if not os.path.exists('saves'):
            os.makedirs('saves')
        
        # Use the new to_dict method from Character class
        save_data = self.player.to_dict()
        save_data['save_date'] = datetime.now().isoformat()
        
        filename = f"saves/{self.player.name.lower().replace(' ', '_')}_save.json"
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"\nGame saved as: {filename}")
    
    def load_game(self) -> None:
        """Load a saved game.
        
        Lists available save files and allows player to select one to load.
        Handles cases where no save files exist.
        """
        if not os.path.exists('saves'):
            print("\nNo saved games found.")
            time.sleep(2)
            return
        
        save_files = [f for f in os.listdir('saves') if f.endswith('_save.json')]
        
        if not save_files:
            print("\nNo saved games found.")
            time.sleep(2)
            return
        
        print("\nSaved Games:")
        for i, save_file in enumerate(save_files, 1):
            # Extract character name from filename
            char_name = save_file.replace('_save.json', '').replace('_', ' ').title()
            print(f"{i}. {char_name}")
        
        try:
            choice = int(input("\nSelect save file (number): "))
            if 1 <= choice <= len(save_files):
                self.load_character_from_file(f"saves/{save_files[choice-1]}")
            else:
                print("Invalid selection.")
                time.sleep(1)
        except ValueError:
            print("Invalid input.")
            time.sleep(1)
    
    def load_character_from_file(self, filename: str) -> None:
        """Load character from save file.
        
        Args:
            filename: Path to the save file to load.
        """
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            # Create character and load from dictionary
            name = save_data.get('name', 'Unknown')
            self.player = Character(name)
            self.player.from_dict(save_data)
            
            print(f"\nGame loaded successfully!")
            print(f"Welcome back, {self.player.name}!")
            time.sleep(2)
            
            # Here you would continue to the main game
            print("\n[Game would continue here...]")
            input("Press Enter to return to main menu...")
            
        except Exception as e:
            print(f"\nError loading save file: {e}")
            time.sleep(2)
    
    def show_credits(self) -> None:
        """Display game credits.
        
        Shows information about the game and its developer.
        """
        self.clear_screen()
        print("\n" + "="*50)
        print("CREDITS".center(50))
        print("="*50)
        print("\nWhiskey Hollow - A Western RPG")
        print("Developed by: Jon Farber")
        print("Python Version: 3.x")
        print("\n" + "="*50)
        input("\nPress Enter to return to main menu...")
    
    def quit_game(self) -> None:
        """Exit the game.
        
        Sets the game_running flag to False to exit the main loop.
        """
        print("\nThanks for playing, partner!")
        print("See you on the frontier...")
        self.game_running = False


def main() -> None:
    """Main game entry point.
    
    Creates and starts the main game instance.
    """
    game = WesternRPG()
    game.main_menu()


if __name__ == "__main__":
    main()