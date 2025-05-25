"""File management utilities for Western RPG game.

This module handles all file I/O operations including saving and loading
character data, managing save directories, and handling file operations
safely with proper error handling.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from character import Character


class SaveFileManager:
    """Manages save file operations for the game.
    
    Handles creating, loading, listing, and managing character save files
    with proper error handling and validation.
    
    Attributes:
        save_directory: Directory where save files are stored.
        file_extension: Extension used for save files.
    """
    
    def __init__(self, save_directory: str = "saves", file_extension: str = "_save.json") -> None:
        """Initialize the save file manager.
        
        Args:
            save_directory: Directory to store save files.
            file_extension: File extension for save files.
        """
        self.save_directory = save_directory
        self.file_extension = file_extension
        self._ensure_save_directory_exists()
    
    def _ensure_save_directory_exists(self) -> None:
        """Create save directory if it doesn't exist."""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
    
    def _generate_filename(self, character_name: str) -> str:
        """Generate filename for a character save.
        
        Args:
            character_name: Name of the character.
            
        Returns:
            Generated filename for the save file.
        """
        safe_name = character_name.lower().replace(' ', '_').replace('/', '_').replace('\\', '_')
        # Remove any other potentially problematic characters
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c in ('_', '-'))
        return f"{self.save_directory}/{safe_name}{self.file_extension}"
    
    def save_character(self, character: Character) -> Tuple[bool, str]:
        """Save a character to file.
        
        Args:
            character: Character instance to save.
            
        Returns:
            Tuple of (success: bool, message: str).
        """
        try:
            self._ensure_save_directory_exists()
            
            # Get character data and add save metadata
            save_data = character.to_dict()
            save_data['save_date'] = datetime.now().isoformat()
            save_data['game_version'] = "1.0.0"  # For future compatibility
            
            filename = self._generate_filename(character.name)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return True, f"Game saved as: {filename}"
            
        except PermissionError:
            return False, "Permission denied - cannot write to save directory"
        except OSError as e:
            return False, f"File system error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error saving game: {str(e)}"
    
    def load_character(self, filename: str) -> Tuple[bool, Optional[Character], str]:
        """Load a character from file.
        
        Args:
            filename: Path to the save file.
            
        Returns:
            Tuple of (success: bool, character: Character or None, message: str).
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Validate save data
            if not self._validate_save_data(save_data):
                return False, None, "Invalid or corrupted save file"
            
            # Create character and load data
            character_name = save_data.get('name', 'Unknown')
            character = Character(character_name)
            character.from_dict(save_data)
            
            return True, character, f"Successfully loaded {character_name}"
            
        except FileNotFoundError:
            return False, None, "Save file not found"
        except json.JSONDecodeError:
            return False, None, "Save file is corrupted or invalid JSON"
        except PermissionError:
            return False, None, "Permission denied - cannot read save file"
        except Exception as e:
            return False, None, f"Unexpected error loading game: {str(e)}"
    
    def _validate_save_data(self, data: Dict[str, Any]) -> bool:
        """Validate that save data contains required fields.
        
        Args:
            data: Save data dictionary to validate.
            
        Returns:
            True if data is valid, False otherwise.
        """
        required_fields = ['name', 'level', 'vigor', 'finesse', 'smarts']
        return all(field in data for field in required_fields)
    
    def list_save_files(self) -> List[str]:
        """List all available save files.
        
        Returns:
            List of save file names (without directory path).
        """
        if not os.path.exists(self.save_directory):
            return []
        
        try:
            files = os.listdir(self.save_directory)
            return [f for f in files if f.endswith(self.file_extension)]
        except OSError:
            return []
    
    def get_save_file_info(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get information about a save file without fully loading it.
        
        Args:
            filename: Name of the save file.
            
        Returns:
            Dictionary with save file info or None if error.
        """
        try:
            full_path = os.path.join(self.save_directory, filename)
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                'character_name': data.get('name', 'Unknown'),
                'level': data.get('level', 1),
                'location': data.get('location', 'Unknown'),
                'save_date': data.get('save_date', 'Unknown'),
                'dollars': data.get('dollars', data.get('gold', 0))  # Handle old saves
            }
        except Exception:
            return None
    
    def delete_save_file(self, filename: str) -> Tuple[bool, str]:
        """Delete a save file.
        
        Args:
            filename: Name of the save file to delete.
            
        Returns:
            Tuple of (success: bool, message: str).
        """
        try:
            full_path = os.path.join(self.save_directory, filename)
            if os.path.exists(full_path):
                os.remove(full_path)
                return True, f"Deleted save file: {filename}"
            else:
                return False, "Save file not found"
        except PermissionError:
            return False, "Permission denied - cannot delete save file"
        except Exception as e:
            return False, f"Error deleting save file: {str(e)}"
    
    def backup_save_file(self, filename: str) -> Tuple[bool, str]:
        """Create a backup of a save file.
        
        Args:
            filename: Name of the save file to backup.
            
        Returns:
            Tuple of (success: bool, message: str).
        """
        try:
            import shutil
            
            full_path = os.path.join(self.save_directory, filename)
            backup_path = f"{full_path}.backup"
            
            shutil.copy2(full_path, backup_path)
            return True, f"Backup created: {backup_path}"
            
        except Exception as e:
            return False, f"Error creating backup: {str(e)}"


def create_save_manager() -> SaveFileManager:
    """Factory function to create a SaveFileManager instance.
    
    Returns:
        Configured SaveFileManager instance.
    """
    return SaveFileManager()


def quick_save_character(character: Character) -> bool:
    """Quick save function for a character.
    
    Args:
        character: Character to save.
        
    Returns:
        True if save was successful, False otherwise.
    """
    manager = create_save_manager()
    success, message = manager.save_character(character)
    print(message)
    return success


def quick_load_character(save_file: str) -> Optional[Character]:
    """Quick load function for a character.
    
    Args:
        save_file: Name of the save file to load.
        
    Returns:
        Loaded Character instance or None if failed.
    """
    manager = create_save_manager()
    success, character, message = manager.load_character(
        os.path.join(manager.save_directory, save_file)
    )
    print(message)
    return character if success else None


def get_available_saves() -> List[Tuple[str, Dict[str, Any]]]:
    """Get list of available saves with their information.
    
    Returns:
        List of tuples containing (filename, save_info).
    """
    manager = create_save_manager()
    save_files = manager.list_save_files()
    
    saves_with_info = []
    for filename in save_files:
        info = manager.get_save_file_info(filename)
        if info:
            saves_with_info.append((filename, info))
    
    return saves_with_info