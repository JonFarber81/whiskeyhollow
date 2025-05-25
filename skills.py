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
            'natural_environment': Skill('Natural Environment', 'smarts', 'Wilderness survival and nature knowledge'),
            'navigate': Skill('Navigate', 'smarts', 'Navigation and pathfinding'),
            'pistols': Skill('Pistols', 'finesse', 'Handgun combat and accuracy'),
            'persuasion_and_rhetoric': Skill('Persuasion and Rhetoric', 'smarts', 'Convincing others through speech'),
            'prospecting': Skill('Prospecting', 'smarts', 'Finding valuable minerals and resources'),
            'repair': Skill('Repair', 'smarts', 'Fixing tools, weapons, and equipment'),
            'riding': Skill('Riding', 'finesse', 'Horseback riding and animal handling'),
            'rifles_shotguns': Skill('Rifles and Shotguns', 'finesse', 'Long gun combat and marksmanship'),
            'slink': Skill('Slink', 'finesse', 'Moving stealthily and avoiding detection'),
            'strong_arm': Skill('Strong Arm', 'vigor', 'Using threats of force and violence to coerce others'),
            'survival': Skill('Survival', 'smarts', 'Finding water, making traps, scavenging, building shelter'),
            'throw': Skill('Throw', 'finesse', 'Throwing rocks, spears, knives, and other projectiles'),
            'track': Skill('Track', 'smarts', 'Tracking human or animal prey'),
            'trade': Skill('Trade', 'smarts', 'Negotiating good deals when buying or selling'),
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


# Global skill manager instance
skill_manager = SkillManager()