"""Character class for Western RPG game."""

from typing import Dict, Any
from dice import roll_4d6_drop_lowest, roll_starting_money


class Character:
    """Represents a character in the Western RPG game."""
    
    def __init__(self, name: str = "") -> None:
        """Initialize a new character."""
        self.name: str = name
        self.level: int = 1
        self.experience: int = 0
        self.dollars: int = 0
        
        # Core attributes (3-18 range)
        self.vigor: int = 0      # Physical strength, endurance, toughness
        self.finesse: int = 0    # Dexterity, agility, coordination
        self.smarts: int = 0     # Intelligence, wisdom, awareness
        
        # Derived stats
        self.hit_points: int = 0
        self.max_hit_points: int = 0
        
        # Starting gear
        self.inventory = ["Worn Boots", "Tattered Hat", "Old Knife"]
        self.weapon: str = "Old Knife"
        self.armor: str = "Worn Clothes"
        self.location: str = "Whiskey Hollow"

    def roll_attributes(self) -> None:
        """Roll 4d6 drop lowest for each attribute."""
        self.vigor = roll_4d6_drop_lowest()
        self.finesse = roll_4d6_drop_lowest()
        self.smarts = roll_4d6_drop_lowest()
        self.dollars = roll_starting_money()
        self.calculate_derived_stats()
    
    def calculate_derived_stats(self) -> None:
        """Calculate hit points based on attributes."""
        self.max_hit_points = (self.vigor + self.finesse + self.smarts) // 3
        self.hit_points = self.max_hit_points
    
    def get_attribute_modifier(self, attribute: int) -> int:
        """Get D&D-style modifier for an attribute."""
        return (attribute - 10) // 2
    
    def display_character_sheet(self) -> None:
        """Display formatted character information."""
        print("\n" + "="*50)
        print(f"CHARACTER SHEET - {self.name.upper()}")
        print("="*50)
        print(f"Level: {self.level}    Experience: {self.experience}")
        print(f"Dollars: ${self.dollars}    Location: {self.location}")
        print("-"*50)
        print("ATTRIBUTES:")
        print(f"Vigor:   {self.vigor:2d} ({self.get_attribute_modifier(self.vigor):+d})  [Physical strength & toughness]")
        print(f"Finesse: {self.finesse:2d} ({self.get_attribute_modifier(self.finesse):+d})  [Agility & coordination]")
        print(f"Smarts:  {self.smarts:2d} ({self.get_attribute_modifier(self.smarts):+d})  [Intelligence & awareness]")
        print("-"*50)
        print(f"Hit Points: {self.hit_points}/{self.max_hit_points}")
        print(f"Weapon:     {self.weapon}")
        print(f"Armor:      {self.armor}")
        print("="*50)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert character to dictionary for saving."""
        return {
            'name': self.name,
            'level': self.level,
            'experience': self.experience,
            'dollars': self.dollars,
            'vigor': self.vigor,
            'finesse': self.finesse,
            'smarts': self.smarts,
            'hit_points': self.hit_points,
            'max_hit_points': self.max_hit_points,
            'inventory': self.inventory,
            'weapon': self.weapon,
            'armor': self.armor,
            'location': self.location
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load character from dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)