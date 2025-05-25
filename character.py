"""Character module for Western RPG game.

This module contains the Character class which represents a player character
or NPC in the Western-themed RPG game.
"""

import random
from typing import Dict, List, Any, Optional


class Character:
    """Represents a character in the Western RPG game.
    
    A character has core attributes (vigor, finesse, smarts), derived stats,
    inventory, and game progress tracking. Characters can be created with
    random attributes or loaded from saved data.
    
    Attributes:
        name: Character's name
        level: Current character level
        experience: Total experience points earned
        dollars: Current money in dollars
        vigor: Physical strength, endurance, toughness (3-18)
        finesse: Dexterity, agility, coordination (3-18)
        smarts: Intelligence, wisdom, awareness (3-18)
        hit_points: Current hit points
        max_hit_points: Maximum hit points
        inventory: List of items carried
        weapon: Currently equipped weapon
        armor: Currently equipped armor
        location: Current game location
        quests: List of active/completed quests
        reputation: Character's reputation score
    """
    
    def __init__(self, name: str = "") -> None:
        """Initialize a new character.
        
        Args:
            name: The character's name. Defaults to empty string.
        """
        self.name: str = name
        self.level: int = 1
        self.experience: int = 0
        self.dollars: int = self._roll_starting_money()
        
        # Core attributes (3-18 range)
        self.vigor: int = 0      # Physical strength, endurance, toughness
        self.finesse: int = 0    # Dexterity, agility, coordination
        self.smarts: int = 0     # Intelligence, wisdom, awareness
        
        # Derived stats
        self.hit_points: int = 0
        self.max_hit_points: int = 0
        
        # Starting inventory
        self.inventory: List[str] = ["Worn Boots", "Tattered Hat", "Old Knife"]
        self.weapon: str = "Old Knife"
        self.armor: str = "Worn Clothes"
        
        # Game progress
        self.location: str = "Dusty Creek"
        self.quests: List[str] = []
        self.reputation: int = 0

    def _roll_starting_money(self) -> int:
        """Roll 3d6 * 10 for starting dollars.
        
        Returns:
            Starting money amount (30-180 dollars).
        """
        dice_total = sum(random.randint(1, 6) for _ in range(3))
        return dice_total * 10

    def roll_attributes(self) -> None:
        """Roll 4d6, drop lowest for each attribute.
        
        Generates random values for vigor, finesse, and smarts using 4d6
        drop lowest method, then calculates derived stats.
        """
        attributes = []
        for _ in range(3):  # Only 3 attributes now
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.sort(reverse=True)
            attribute_value = sum(rolls[:3])  # Take highest 3
            attributes.append(attribute_value)
        
        self.vigor = attributes[0]
        self.finesse = attributes[1]
        self.smarts = attributes[2]
        
        # Calculate derived stats
        self.calculate_derived_stats()
    
    def calculate_derived_stats(self) -> None:
        """Calculate hit points based on all three attributes.
        
        Hit points are calculated as the average of all three core attributes.
        """
        # Hit points = (Vigor + Finesse + Smarts) / 3
        self.max_hit_points = (self.vigor + self.finesse + self.smarts) // 3
        self.hit_points = self.max_hit_points
    
    def get_attribute_modifier(self, attribute: int) -> int:
        """Get D&D-style modifier for an attribute.
        
        Args:
            attribute: The attribute value (typically 3-18).
            
        Returns:
            The modifier value (typically -4 to +4).
        """
        return (attribute - 10) // 2
    
    def display_character_sheet(self) -> None:
        """Display formatted character information to console.
        
        Prints a nicely formatted character sheet showing all character
        stats, attributes, and equipment.
        """
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
        """Convert character to dictionary for saving.
        
        Returns:
            Dictionary containing all character data suitable for JSON serialization.
        """
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
            'location': self.location,
            'quests': self.quests,
            'reputation': self.reputation
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load character from dictionary.
        
        Args:
            data: Dictionary containing character data from save file.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Handle backward compatibility for old save files that used 'gold'
        if 'gold' in data and 'dollars' not in data:
            self.dollars = data['gold']
        
        # Ensure dollars is set if somehow missing
        if not hasattr(self, 'dollars') or self.dollars is None:
            self.dollars = self._roll_starting_money()
    
    def add_experience(self, amount: int) -> bool:
        """Add experience and handle level ups.
        
        Args:
            amount: Experience points to add.
            
        Returns:
            True if character leveled up, False otherwise.
        """
        self.experience += amount
        # Simple level up system - every 100 XP = new level
        new_level = (self.experience // 100) + 1
        if new_level > self.level:
            old_level = self.level
            self.level = new_level
            print(f"\nLevel up! {self.name} is now level {self.level}!")
            # Could add attribute increases, HP boosts, etc. here
            return True
        return False
    
    def add_dollars(self, amount: int) -> None:
        """Add dollars to character.
        
        Args:
            amount: Amount to add (can be negative for spending).
        """
        self.dollars += amount
        if amount > 0:
            print(f"Gained ${amount}! Total dollars: ${self.dollars}")
        elif amount < 0:
            print(f"Lost ${abs(amount)}! Remaining dollars: ${self.dollars}")
    
    def heal(self, amount: int) -> bool:
        """Heal character by specified amount.
        
        Args:
            amount: Hit points to restore.
            
        Returns:
            True if healing occurred, False if already at full health.
        """
        if self.hit_points >= self.max_hit_points:
            print(f"{self.name} is already at full health!")
            return False
        
        old_hp = self.hit_points
        self.hit_points = min(self.hit_points + amount, self.max_hit_points)
        healed = self.hit_points - old_hp
        print(f"{self.name} healed {healed} hit points! ({self.hit_points}/{self.max_hit_points})")
        return True
    
    def take_damage(self, amount: int) -> bool:
        """Apply damage to character.
        
        Args:
            amount: Damage to apply.
            
        Returns:
            True if character is knocked unconscious, False otherwise.
        """
        self.hit_points = max(0, self.hit_points - amount)
        print(f"{self.name} takes {amount} damage! ({self.hit_points}/{self.max_hit_points})")
        
        if self.hit_points <= 0:
            print(f"{self.name} has been knocked unconscious!")
            return True  # Character is down
        return False
    
    def is_alive(self) -> bool:
        """Check if character is alive.
        
        Returns:
            True if character has hit points remaining, False otherwise.
        """
        return self.hit_points > 0
    
    def add_item(self, item: str) -> None:
        """Add item to inventory.
        
        Args:
            item: Name of the item to add.
        """
        self.inventory.append(item)
        print(f"Added {item} to inventory.")
    
    def remove_item(self, item: str) -> bool:
        """Remove item from inventory.
        
        Args:
            item: Name of the item to remove.
            
        Returns:
            True if item was removed, False if not found.
        """
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"Removed {item} from inventory.")
            return True
        else:
            print(f"{item} not found in inventory.")
            return False
    
    def equip_weapon(self, weapon: str) -> bool:
        """Equip a weapon.
        
        Args:
            weapon: Name of the weapon to equip.
            
        Returns:
            True if weapon was equipped, False if not in inventory.
        """
        if weapon in self.inventory:
            old_weapon = self.weapon
            self.weapon = weapon
            print(f"Equipped {weapon}. Previous weapon: {old_weapon}")
            return True
        else:
            print(f"{weapon} not found in inventory.")
            return False
    
    def equip_armor(self, armor: str) -> bool:
        """Equip armor.
        
        Args:
            armor: Name of the armor to equip.
            
        Returns:
            True if armor was equipped, False if not in inventory.
        """
        if armor in self.inventory:
            old_armor = self.armor
            self.armor = armor
            print(f"Equipped {armor}. Previous armor: {old_armor}")
            return True
        else:
            print(f"{armor} not found in inventory.")
            return False