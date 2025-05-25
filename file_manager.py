"""Simple file management for character saves."""

import os
import json
from datetime import datetime
from typing import List, Tuple, Optional
from character import Character


class SaveManager:
    """Handles saving and loading characters."""
    
    def __init__(self, save_directory: str = "saves"):
        self.save_directory = save_directory
        self._ensure_save_directory_exists()
    
    def _ensure_save_directory_exists(self) -> None:
        """Create save directory if it doesn't exist."""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
    
    def save_character(self, character: Character) -> bool:
        """Save a character to file."""
        try:
            # Create safe filename
            safe_name = self._make_safe_filename(character.name)
            filename = f"{self.save_directory}/{safe_name}.json"
            
            # Add save metadata
            save_data = character.to_dict()
            save_data['save_date'] = datetime.now().isoformat()
            
            # Write to file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2)
            
            print(f"\nCharacter saved as: {filename}")
            return True
            
        except Exception as e:
            print(f"\nError saving character: {str(e)}")
            return False
    
    def load_character(self, filename: str) -> Optional[Character]:
        """Load a character from file."""
        try:
            full_path = os.path.join(self.save_directory, filename)
            
            with open(full_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Create and load character
            character = Character()
            character.from_dict(save_data)
            
            print(f"\nCharacter '{character.name}' loaded successfully!")
            return character
            
        except Exception as e:
            print(f"\nError loading character: {str(e)}")
            return None
    
    def list_save_files(self) -> List[str]:
        """List all save files."""
        if not os.path.exists(self.save_directory):
            return []
        
        try:
            files = os.listdir(self.save_directory)
            return [f for f in files if f.endswith('.json')]
        except OSError:
            return []
    
    def get_save_info(self, filename: str) -> Optional[dict]:
        """Get basic info about a save file."""
        try:
            full_path = os.path.join(self.save_directory, filename)
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                'name': data.get('name', 'Unknown'),
                'level': data.get('level', 1),
                'dollars': data.get('dollars', 0),
                'save_date': data.get('save_date', 'Unknown')
            }
        except:
            return None
    
    def _make_safe_filename(self, name: str) -> str:
        """Convert character name to safe filename."""
        safe_name = name.lower().replace(' ', '_')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
        return safe_name or 'character'