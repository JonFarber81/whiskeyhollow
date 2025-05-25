"""Character creation system for Western RPG game.

This module handles the complete character creation workflow including
name input, attribute rolling, manual attribute setting, and character
finalization with proper validation and user feedback.
"""

from typing import Dict, Optional, Tuple
from character import Character
from dice import roll_dice
from display import pause_with_message
from menus import (
    show_character_creation_intro, show_attribute_rolling_screen,
    show_attribute_rolling_menu, get_manual_attributes, show_character_finalization
)
from file_manager import quick_save_character


class CharacterCreator:
    """Handles the character creation process.
    
    Manages the workflow from name input through attribute assignment
    to final character creation and saving.
    
    Attributes:
        character: The character being created.
        creation_complete: Whether character creation is finished.
    """
    
    def __init__(self) -> None:
        """Initialize the character creator."""
        self.character: Optional[Character] = None
        self.creation_complete: bool = False
    
    def create_character(self) -> Optional[Character]:
        """Run the complete character creation process.
        
        Returns:
            Created Character instance or None if creation was cancelled.
        """
        # Step 1: Get character name
        if not self._get_character_name():
            return None
        
        # Step 2: Welcome message
        self._show_welcome_message()
        
        # Step 3: Handle attribute assignment
        if not self._handle_attribute_assignment():
            return None
        
        # Step 4: Finalize character
        self._finalize_character()
        
        # Step 5: Save character
        self._save_character()
        
        self.creation_complete = True
        return self.character
    
    def _get_character_name(self) -> bool:
        """Get character name from player.
        
        Returns:
            True if name was successfully obtained, False if cancelled.
        """
        try:
            name = show_character_creation_intro()
            if not name:
                return False
            
            self.character = Character(name)
            return True
            
        except KeyboardInterrupt:
            print("\nCharacter creation cancelled.")
            return False
    
    def _show_welcome_message(self) -> None:
        """Show welcome message with character name."""
        if self.character:
            print(f"\nWell howdy, {self.character.name}! Time to see what you're made of...")
            pause_with_message("Press Enter to roll your attributes...")
    
    def _handle_attribute_assignment(self) -> bool:
        """Handle the attribute rolling/setting process.
        
        Returns:
            True if attributes were successfully assigned, False if cancelled.
        """
        while True:
            # Show rolling screen and roll attributes
            show_attribute_rolling_screen()
            
            if not self.character:
                return False
            
            self.character.roll_attributes()
            self.character.display_character_sheet()
            
            # Get player choice for what to do with these attributes
            choice = show_attribute_rolling_menu()
            
            if choice == "1":  # Keep attributes
                return True
            elif choice == "2":  # Roll again
                continue
            elif choice == "3":  # Manual setting
                return self._handle_manual_attributes()
            else:
                print("Invalid choice. Keeping current attributes.")
                pause_with_message()
                return True
    
    def _handle_manual_attributes(self) -> bool:
        """Handle manual attribute setting.
        
        Returns:
            True if attributes were successfully set, False if cancelled.
        """
        try:
            if not self.character:
                return False
            
            attributes = get_manual_attributes()
            
            # Apply the manually entered attributes
            for attr_name, value in attributes.items():
                setattr(self.character, attr_name, value)
            
            # Recalculate derived stats
            self.character.calculate_derived_stats()
            
            return True
            
        except KeyboardInterrupt:
            print("\nManual attribute setting cancelled. Using rolled attributes.")
            pause_with_message()
            return True
    
    def _finalize_character(self) -> None:
        """Show character finalization screen."""
        if self.character:
            show_character_finalization(self.character)
    
    def _save_character(self) -> bool:
        """Save the created character.
        
        Returns:
            True if save was successful, False otherwise.
        """
        if not self.character:
            return False
        
        return quick_save_character(self.character)
    
    def get_character(self) -> Optional[Character]:
        """Get the created character.
        
        Returns:
            The created Character instance or None if not created.
        """
        return self.character if self.creation_complete else None


class AttributeRoller:
    """Handles attribute rolling with various methods.
    
    Provides different ways to generate character attributes including
    standard 4d6 drop lowest, point buy systems, and testing methods.
    """
    
    @staticmethod
    def roll_4d6_drop_lowest() -> int:
        return roll_dice(num_dice=4, sides=6, drop_lowest=1)['result']
    
    
    @staticmethod
    def roll_attribute_set_standard() -> Dict[str, int]:
        """Roll a standard set of attributes using 4d6 drop lowest.
        
        Returns:
            Dictionary of attribute names to values.
        """
        return {
            'vigor': AttributeRoller.roll_4d6_drop_lowest(),
            'finesse': AttributeRoller.roll_4d6_drop_lowest(),
            'smarts': AttributeRoller.roll_4d6_drop_lowest()
        }
    

def create_new_character() -> Optional[Character]:
    """Factory function to create a new character.
    
    Returns:
        Created Character instance or None if creation failed.
    """
    creator = CharacterCreator()
    return creator.create_character()


def validate_character_name(name: str) -> Tuple[bool, str]:
    """Validate a character name.
    
    Args:
        name: Character name to validate.
        
    Returns:
        Tuple of (is_valid: bool, error_message: str).
    """
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    name = name.strip()
    
    if len(name) > 20:
        return False, "Name must be 20 characters or less"
    
    if len(name) < 1:
        return False, "Name must be at least 1 character"
    
    # Check for invalid characters (basic validation)
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        if char in name:
            return False, f"Name cannot contain '{char}'"
    
    return True, ""


def validate_attribute_value(value: int) -> Tuple[bool, str]:
    """Validate an attribute value.
    
    Args:
        value: Attribute value to validate.
        
    Returns:
        Tuple of (is_valid: bool, error_message: str).
    """
    if value < 3:
        return False, "Attribute values must be at least 3"
    
    if value > 18:
        return False, "Attribute values cannot exceed 18"
    
    return True, ""


def get_attribute_description(attribute_name: str) -> str:
    """Get description for an attribute.
    
    Args:
        attribute_name: Name of the attribute.
        
    Returns:
        Description string for the attribute.
    """
    descriptions = {
        'vigor': 'Physical strength, endurance, and toughness',
        'finesse': 'Dexterity, agility, and coordination', 
        'smarts': 'Intelligence, wisdom, and awareness'
    }
    
    return descriptions.get(attribute_name.lower(), 'Unknown attribute')