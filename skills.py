"""Skills system for Western RPG game."""

import json
import os
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
    
    def __init__(self, skills_file: str = "skills_data.json"):
        """Initialize by loading skills from external JSON file."""
        self.skills_file = skills_file
        self.skills = {}
        self.load_skills()
    
    def load_skills(self):
        """Load skills from JSON file."""
        try:
            # Check if file exists
            if not os.path.exists(self.skills_file):
                print(f"Warning: Skills file '{self.skills_file}' not found. Creating default skills...")
                self._create_default_skills_file()
            
            # Load skills from file
            with open(self.skills_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert JSON data to Skill objects
            self.skills = {}
            for skill_key, skill_data in data.get('skills', {}).items():
                self.skills[skill_key] = Skill(
                    name=skill_data['name'],
                    attribute=skill_data['attribute'],
                    description=skill_data.get('description', '')
                )
            
            print(f"Loaded {len(self.skills)} skills from {self.skills_file}")
            
        except json.JSONDecodeError as e:
            print(f"Error parsing skills file: {e}")
            print("Using default skills...")
            self._load_default_skills()
        except Exception as e:
            print(f"Error loading skills file: {e}")
    
    def _create_default_skills_file(self):
        """Create the default skills JSON file."""
        default_skills = {
            "skills": {
                "acting": {
                    "name": "Acting",
                    "attribute": "smarts",
                    "description": "Performance and deception through acting"
                },
                "agriculture": {
                    "name": "Agriculture",
                    "attribute": "smarts",
                    "description": "Farming, crops, and livestock knowledge"
                },
                "animals": {
                    "name": "Animals",
                    "attribute": "smarts",
                    "description": "Animal handling and knowledge"
                },
                "athletics": {
                    "name": "Athletics",
                    "attribute": "vigor/finesse",
                    "description": "Physical prowess and coordination"
                },
                "bows": {
                    "name": "Bows",
                    "attribute": "finesse",
                    "description": "Archery and bow weapons"
                },
                "carouse": {
                    "name": "Carouse",
                    "attribute": "vigor",
                    "description": "Drinking, partying, and carousing"
                },
                "cooking": {
                    "name": "Cooking",
                    "attribute": "smarts",
                    "description": "Cooking and food preparation"
                },
                "deceive": {
                    "name": "Deceive",
                    "attribute": "smarts",
                    "description": "Lying and manipulation"
                },
                "escamotage": {
                    "name": "Escamotage",
                    "attribute": "finesse",
                    "description": "Sleight of hand and pickpocketing"
                },
                "first_aid": {
                    "name": "First Aid",
                    "attribute": "smarts",
                    "description": "Basic medical treatment"
                },
                "fisticuffs": {
                    "name": "Fisticuffs",
                    "attribute": "vigor",
                    "description": "Unarmed combat"
                },
                "melee_weapons": {
                    "name": "Melee Weapons",
                    "attribute": "vigor",
                    "description": "Combat with melee weapons"
                },
                "language": {
                    "name": "Language",
                    "attribute": "smarts",
                    "description": "Foreign languages"
                },
                "locksmith": {
                    "name": "Locksmith",
                    "attribute": "finesse",
                    "description": "Lock picking and mechanisms"
                },
                "natural_environment": {
                    "name": "Natural Environment",
                    "attribute": "smarts",
                    "description": "Wilderness survival and nature knowledge"
                },
                "navigate": {
                    "name": "Navigate",
                    "attribute": "smarts",
                    "description": "Navigation and pathfinding"
                },
                "pistols": {
                    "name": "Pistols",
                    "attribute": "finesse",
                    "description": "Handgun combat and accuracy"
                },
                "persuasion_and_rhetoric": {
                    "name": "Persuasion and Rhetoric",
                    "attribute": "smarts",
                    "description": "Convincing others through speech"
                },
                "prospecting": {
                    "name": "Prospecting",
                    "attribute": "smarts",
                    "description": "Finding valuable minerals and resources"
                },
                "repair": {
                    "name": "Repair",
                    "attribute": "smarts",
                    "description": "Fixing tools, weapons, and equipment"
                },
                "riding": {
                    "name": "Riding",
                    "attribute": "finesse",
                    "description": "Horseback riding and animal handling"
                },
                "rifles_shotguns": {
                    "name": "Rifles and Shotguns",
                    "attribute": "finesse",
                    "description": "Long gun combat and marksmanship"
                },
                "slink": {
                    "name": "Slink",
                    "attribute": "finesse",
                    "description": "Moving stealthily and avoiding detection"
                },
                "strong_arm": {
                    "name": "Strong Arm",
                    "attribute": "vigor",
                    "description": "Using threats of force and violence to coerce others"
                },
                "survival": {
                    "name": "Survival",
                    "attribute": "smarts",
                    "description": "Finding water, making traps, scavenging, building shelter"
                },
                "throw": {
                    "name": "Throw",
                    "attribute": "finesse",
                    "description": "Throwing rocks, spears, knives, and other projectiles"
                },
                "track": {
                    "name": "Track",
                    "attribute": "smarts",
                    "description": "Tracking human or animal prey"
                },
                "trade": {
                    "name": "Trade",
                    "attribute": "smarts",
                    "description": "Negotiating good deals when buying or selling"
                }
            }
        }
        
        try:
            with open(self.skills_file, 'w', encoding='utf-8') as f:
                json.dump(default_skills, f, indent=2)
            print(f"Created default skills file: {self.skills_file}")
        except Exception as e:
            print(f"Error creating skills file: {e}")
    
    
    def reload_skills(self):
        """Reload skills from file (useful for development/testing)."""
        self.load_skills()
    
    def get_skill_list(self) -> List[Tuple[str, Skill]]:
        """Get sorted list of (key, skill) tuples."""
        return sorted(self.skills.items(), key=lambda x: x[1].name)
    
    def get_skills_by_attribute(self, attribute: str) -> List[Tuple[str, Skill]]:
        """Get skills associated with a specific attribute."""
        return [(key, skill) for key, skill in self.skills.items() 
                if attribute.lower() in skill.attribute.lower()]
    
    def add_skill(self, key: str, name: str, attribute: str, description: str = ""):
        """Add a new skill to the system (runtime only - not saved to file)."""
        self.skills[key] = Skill(name, attribute, description)
    
    def get_skill(self, key: str) -> Skill:
        """Get a skill by its key."""
        return self.skills.get(key)
    
    def save_skills_to_file(self):
        """Save current skills back to the JSON file."""
        try:
            skills_data = {
                "skills": {}
            }
            
            for key, skill in self.skills.items():
                skills_data["skills"][key] = {
                    "name": skill.name,
                    "attribute": skill.attribute,
                    "description": skill.description
                }
            
            with open(self.skills_file, 'w', encoding='utf-8') as f:
                json.dump(skills_data, f, indent=2)
            
            print(f"Skills saved to {self.skills_file}")
            return True
            
        except Exception as e:
            print(f"Error saving skills: {e}")
            return False


# Global skill manager instance
skill_manager = SkillManager()