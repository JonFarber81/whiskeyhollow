"""Skills system for Western RPG game."""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class Skill:
    """Represents a single skill."""
    name: str
    attribute: str
    description: str = ""


class SkillManager:
    """Manages all skills in the game."""
    
    def __init__(self):
        """Initialize with base skills."""
        self.skills = {
            'acting': Skill('Acting', 'smarts', 'Performance and deception through acting'),
            'agriculture': Skill('Agriculture', 'smarts', 'Farming, crops, and livestock knowledge'),
            'animals': Skill('Animals', 'smarts', 'Animal handling and knowledge'),
            'athletics': Skill('Athletics', 'vigor/finesse', 'Physical prowess and coordination'),
            'bows': Skill('Bows', 'finesse', 'Archery and bow weapons'),
            'carouse': Skill('Carouse', 'vigor', 'Drinking, partying, and carousing'),
            'cooking': Skill('Cooking', 'smarts', 'Cooking and food preparation'),
            'deceive': Skill('Deceive', 'smarts', 'Lying and manipulation'),
            'escamotage': Skill('Escamotage', 'finesse', 'Sleight of hand and pickpocketing'),
            'first_aid': Skill('First Aid', 'smarts', 'Basic medical treatment'),
            'fisticuffs': Skill('Fisticuffs', 'vigor', 'Unarmed combat'),
            'melee_weapons': Skill('Melee Weapons', 'vigor', 'Combat with melee weapons'),
            'language': Skill('Language', 'smarts', 'Foreign languages'),
            'locksmith': Skill('Locksmith', 'finesse', 'Lock picking and mechanisms'),
            'natural_environment': Skill('Natural Environment', 'smarts', ''),
            'navigate': Skill('Navigate', 'Smarts'),
            'pistols': Skill('Pistols', 'Finesse'),
            'persuasion_and_rhetoric': Skill('Persuasion and Rhetoric', 'Smarts'),
            'prospecting': Skill('Prospecting', 'Smarts'),
            'repair': Skill('Repair', 'Smarts'),
            'riding': Skill('Riding', 'Finesse'),
            'rifles_shotguns': Skill('Rifles and Shotguns', 'Finesse'),
            'slink': Skill('Slink', 'Finesse'),
            'strong_arm': Skill('Strong Arm', 'Vigor', 'Ability to use threats of force and violence to coerce others'),
            'survival': Skill('Survival', 'Smarts', 'Ability to find water, make traps, scavenge, build a shelter'),
            'throw': Skill('Throw', 'Finesse', 'Ability to throw a rock, spear, knife, etc...'),
            'track': Skill('Track', 'Smarts', 'Ability to track human or animal prey'),
            'trade': Skill('Trade', 'Smarts', 'Ability to negotiate good deals when buying or selling'),

        }
    
    def get_skill_list(self) -> List[Tuple[str, Skill]]:
        """Get sorted list of (key, skill) tuples."""
        return sorted(self.skills.items(), key=lambda x: x[1].name)
    
    def get_skills_by_attribute(self, attribute: str) -> List[Tuple[str, Skill]]:
        """Get skills associated with a specific attribute."""
        return [(key, skill) for key, skill in self.skills.items() 
                if attribute.lower() in skill.attribute.lower()]
    
    def add_skill(self, key: str, name: str, attribute: str, description: str = ""):
        """Add a new skill to the system."""
        self.skills[key] = Skill(name, attribute, description)
    
    def get_skill(self, key: str) -> Skill:
        """Get a skill by its key."""
        return self.skills.get(key)
    
    def display_skills_menu(self, character_skills: Dict[str, int], available_points: int):
        """Display skills menu for point allocation."""
        print(f"\n{'='*60}")
        print(f"SKILL ALLOCATION - {available_points} points remaining")
        print(f"{'='*60}")
        print("Skills are limited to 3 points maximum")
        print("-" * 60)
        
        skills_list = self.get_skill_list()
        
        for i, (key, skill) in enumerate(skills_list, 1):
            current_level = character_skills.get(key, 0)
            attr_display = skill.attribute.title()
            
            # Show current level with visual indicators
            level_display = "●" * current_level + "○" * (3 - current_level)
            
            print(f"{i:2d}. {skill.name:<15} [{attr_display:<12}] {level_display} ({current_level}/3)")
        
        print("-" * 60)
        print("0. Finish allocation")
        return skills_list


# Global skill manager instance
skill_manager = SkillManager()