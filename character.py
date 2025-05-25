"""Character class for Western RPG game."""

import random
from typing import Dict, Any
from dice import roll_4d6_drop_lowest, roll_starting_money


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
    
    def apply_age_effects(self) -> None:
        """Apply age-based bonuses and penalties."""
        if not (14 <= self.age <= 57):
            print(f"Warning: Age {self.age} is outside normal range (14-57)")
            return
        
        print(f"\n--- Applying Age Effects for {self.age}-year-old {self.name} ---")
        
        # Determine skill points and tests based on age
        if 14 <= self.age <= 22:
            skill_points = 5
            attribute_boosts = 2
            vigor_tests = 0
        elif 23 <= self.age <= 26:
            skill_points = 5
            attribute_boosts = 3
            vigor_tests = 0
        elif 27 <= self.age <= 30:
            skill_points = 6
            attribute_boosts = 2
            vigor_tests = 0
        elif 31 <= self.age <= 34:
            skill_points = 7
            attribute_boosts = 1
            vigor_tests = 1
        elif 35 <= self.age <= 48:
            skill_points = 9
            attribute_boosts = 0
            vigor_tests = 3
        elif 49 <= self.age <= 52:
            skill_points = 11
            attribute_boosts = 0
            vigor_tests = 5
        elif 53 <= self.age <= 56:
            skill_points = 13
            attribute_boosts = 0
            vigor_tests = 7
        elif self.age == 57:
            skill_points = 15
            attribute_boosts = 0
            vigor_tests = 9
        
        print(f"Gains: {skill_points} skill points, {attribute_boosts} attribute boosts")
        if vigor_tests > 0:
            print(f"Must make {vigor_tests} vigor tests or lose attributes")
        
        # Apply skill points
        self.skill_points += skill_points
        
        # Apply attribute boosts
        for i in range(attribute_boosts):
            self._apply_random_attribute_boost(i + 1)
        
        # Apply vigor tests
        for i in range(vigor_tests):
            self._make_vigor_test(i + 1)
        
        # Recalculate derived stats
        self.calculate_derived_stats()
        print("--- Age Effects Complete ---\n")
    
    def _apply_random_attribute_boost(self, boost_num: int) -> None:
        """Apply a random +1 attribute boost (max 18)."""
        attributes = ['vigor', 'finesse', 'smarts']
        # Only consider attributes that aren't already at max
        available_attributes = [attr for attr in attributes if getattr(self, attr) < 18]
        
        if not available_attributes:
            print(f"Attribute Boost #{boost_num}: All attributes at maximum (18), boost wasted")
            return
        
        chosen_attr = random.choice(available_attributes)
        old_value = getattr(self, chosen_attr)
        setattr(self, chosen_attr, old_value + 1)
        new_value = getattr(self, chosen_attr)
        
        print(f"Attribute Boost #{boost_num}: {chosen_attr.title()} increased from {old_value} to {new_value}")
    
    def _make_vigor_test(self, test_num: int) -> None:
        """Make a vigor test - roll d6s equal to vigor modifier, need 5+ to pass."""
        vigor_modifier = self.get_attribute_modifier(self.vigor)
        dice_to_roll = max(1, vigor_modifier + 1)  # At least 1 die, +1 for base
        
        print(f"Vigor Test #{test_num}: Rolling {dice_to_roll}d6 (need at least one 5 or 6)")
        
        rolls = [random.randint(1, 6) for _ in range(dice_to_roll)]
        successes = [r for r in rolls if r >= 5]
        
        print(f"  Rolled: {rolls}")
        print(f"  Successes (5-6): {successes}")
        
        if successes:
            print(f"  PASSED! No attribute loss.")
        else:
            print(f"  FAILED! Must lose 1 random attribute point.")
            self._lose_random_attribute()
    
    def _lose_random_attribute(self) -> None:
        """Lose 1 point from a random attribute (minimum 3)."""
        attributes = ['vigor', 'finesse', 'smarts']
        # Only consider attributes above minimum
        available_attributes = [attr for attr in attributes if getattr(self, attr) > 3]
        
        if not available_attributes:
            print("    All attributes at minimum (3), no loss applied")
            return
        
        chosen_attr = random.choice(available_attributes)
        old_value = getattr(self, chosen_attr)
        setattr(self, chosen_attr, old_value - 1)
        new_value = getattr(self, chosen_attr)
        
        print(f"    {chosen_attr.title()} decreased from {old_value} to {new_value}")
    
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
        print(f"Age: {self.age}    Level: {self.level}    Experience: {self.experience}")
        print(f"Dollars: ${self.dollars}    Skill Points: {self.skill_points}")
        print(f"Location: {self.location}")
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