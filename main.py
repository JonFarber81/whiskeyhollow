"""Main game module for Western RPG.

This module contains the main game class and entry point for Whiskey Hollow,
a Western-themed RPG game featuring character creation, save/load functionality,
and story-driven gameplay.
"""

import os
from typing import Optional

# Import core modules
from models.character import Character
from models.game_state import GameState, GamePhase, create_new_game_state

# Import game systems
from game.character_creation import create_new_character

# Import utilities
from utils.file_manager import SaveFileManager, get_available_saves

# Import UI modules
from ui.display import clear_screen, pause_with_message
from ui.menus import (
    show_main_menu, show_credits_screen, show_quit_message, show_no_saves_message,
    show_load_success_message, show_load_error_message, show_game_placeholder,
    show_save_game_list
)


class WesternRPG:
    """Main game class for the Western RPG.
    
    Handles the game loop, menus, character creation, and save/load functionality.
    Provides the main interface between the player and the game world.
    
    Attributes:
        game_state: Current game state including player, world, and progress.
        save_manager: Handles all save/load operations.
        game_running: Boolean flag controlling the main game loop.
    """
    
    def __init__(self) -> None:
        """Initialize the game."""
        self.game_state: GameState = create_new_game_state()
        self.save_manager: SaveFileManager = SaveFileManager()
        self.game_running: bool = True
    
    def main_menu(self) -> None:
        """Display main menu and handle selection.
        
        Main game loop that displays the menu and processes user choices
        until the player quits the game.
        """
        while self.game_running:
            self.game_state.change_phase(GamePhase.MAIN_MENU)
            
            choice = show_main_menu(self)
            
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
                pause_with_message()
    
    def new_game(self) -> None:
        """Start a new game with character creation.
        
        Creates a new character using the character creation system,
        initializes a fresh game state, and transitions to the main game.
        """
        self.game_state.change_phase(GamePhase.CHARACTER_CREATION)
        
        # Use the character creation system
        character = create_new_character()
        
        if character:
            # Set up new game state with the created character
            self.game_state = create_new_game_state()
            self.game_state.set_player(character)
            
            # Save the initial game state
            self._save_game_state()
            
            # Transition to main game
            self._start_main_game()
        else:
            print("\nCharacter creation cancelled.")
            pause_with_message()
    
    def load_game(self) -> None:
        """Load a saved game.
        
        Lists available save files and allows player to select one to load.
        Handles cases where no save files exist.
        """
        saves_with_info = get_available_saves()
        
        if not saves_with_info:
            show_no_saves_message()
            return
        
        # Extract just the filenames for the menu
        save_files = [filename for filename, _ in saves_with_info]
        
        file_index = show_save_game_list(save_files)
        
        if file_index >= 0:
            filename = save_files[file_index]
            self._load_game_state_from_file(filename)
    
    def _load_game_state_from_file(self, filename: str) -> None:
        """Load complete game state from save file.
        
        Args:
            filename: Name of the save file to load.
        """
        full_path = os.path.join(self.save_manager.save_directory, filename)
        
        try:
            import json
            with open(full_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Load the complete game state
            self.game_state.from_dict(save_data)
            
            if self.game_state.player:
                show_load_success_message(self.game_state.player.name)
                self._start_main_game()
            else:
                show_load_error_message("No character data found in save file")
                
        except Exception as e:
            show_load_error_message(str(e))
    
    def _save_game_state(self) -> bool:
        """Save the complete game state.
        
        Returns:
            True if save was successful, False otherwise.
        """
        if not self.game_state.player:
            return False
        
        try:
            import json
            from datetime import datetime
            
            # Ensure save directory exists
            if not os.path.exists(self.save_manager.save_directory):
                os.makedirs(self.save_manager.save_directory)
            
            # Get complete game state data
            save_data = self.game_state.to_dict()
            
            # Generate filename based on character name
            character_name = self.game_state.player.name
            safe_name = character_name.lower().replace(' ', '_').replace('/', '_').replace('\\', '_')
            safe_name = ''.join(c for c in safe_name if c.isalnum() or c in ('_', '-'))
            filename = f"{self.save_manager.save_directory}/{safe_name}_save.json"
            
            # Save the data
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            print(f"\nGame saved as: {filename}")
            return True
            
        except Exception as e:
            print(f"\nError saving game: {str(e)}")
            return False
    
    def _start_main_game(self) -> None:
        """Start or continue the main game.
        
        This is where the actual gameplay would begin after character
        creation or loading a save file.
        """
        if not self.game_state.player:
            return
        
        # Set game phase to town exploration
        self.game_state.change_phase(GamePhase.TOWN_EXPLORATION)
        
        # Move player to their current location
        current_location = self.game_state.get_current_location_info()
        if current_location:
            print(f"\nYou find yourself in {current_location.name}")
            print(current_location.description)
        
        # For now, show placeholder for main game
        show_game_placeholder()
        
        # Here you would implement the main game loop:
        # - Location exploration
        # - NPC interaction
        # - Quest system
        # - Combat system
        # - Inventory management
        # etc.
    
    def show_credits(self) -> None:
        """Display game credits."""
        show_credits_screen()
    
    def quit_game(self) -> None:
        """Exit the game.
        
        Sets the game_running flag to False to exit the main loop.
        """
        show_quit_message()
        self.game_running = False
    
    def get_current_character(self) -> Optional[Character]:
        """Get the current player character.
        
        Returns:
            Current player Character or None if no character loaded.
        """
        return self.game_state.player
    
    def get_game_state(self) -> GameState:
        """Get the current game state.
        
        Returns:
            Current GameState instance.
        """
        return self.game_state


def main() -> None:
    """Main game entry point.
    
    Creates and starts the main game instance.
    """
    game = WesternRPG()
    game.main_menu()


if __name__ == "__main__":
    main()