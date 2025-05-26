"""Name generator for Western RPG characters."""

import json
import os
import random
from typing import List, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


class NameGenerator:
    """Generates random Western-themed character names."""
    
    def __init__(self, names_file: str = "names_data.json"):
        """Initialize the name generator with external name data."""
        self.names_file = names_file
        self.names_data = {}
        # Initialize with defaults first, then try to load from file
        self._load_default_names()
        self.load_names()
    
    def load_names(self):
        """Load names from JSON file."""
        try:
            # Check if file exists
            if not os.path.exists(self.names_file):
                console.print(f"[yellow]Names file '{self.names_file}' not found. Creating default names file...[/yellow]")
                self._create_default_names_file()
                return  # Default names already loaded in __init__
            
            # Load names from file
            with open(self.names_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            # Validate that we have all required name categories
            required_keys = ['male_first_names', 'female_first_names', 'surnames']
            for key in required_keys:
                if key not in loaded_data or not loaded_data[key]:
                    console.print(f"[red]Warning: Missing or empty '{key}' in names file. Using defaults.[/red]")
                    return  # Keep default names already loaded
            
            # If validation passes, use the loaded data
            self.names_data = loaded_data
            console.print(f"[green]Loaded {len(self.names_data['male_first_names'])} male names, "
                         f"{len(self.names_data['female_first_names'])} female names, "
                         f"and {len(self.names_data['surnames'])} surnames[/green]")
            
        except json.JSONDecodeError as e:
            console.print(f"[red]Error parsing names file: {e}[/red]")
            console.print("[yellow]Using default names...[/yellow]")
            # Keep default names already loaded
        except Exception as e:
            console.print(f"[red]Error loading names file: {e}[/red]")
            console.print("[yellow]Using default names...[/yellow]")
            # Keep default names already loaded
    
    def _create_default_names_file(self):
        """Create the default names JSON file."""
        default_names = {
            "male_first_names": [
                "Augustus", "Benjamin", "Caleb", "Dalton", "Ezra",
                "Franklin", "Gideon", "Hank", "Isaiah", "Jasper",
                "Knox", "Luther", "Montgomery", "Nathaniel", "Obadiah",
                "Porter", "Quincy", "Reuben", "Silas", "Thaddeus"
            ],
            "female_first_names": [
                "Adelaide", "Beatrice", "Charlotte", "Delilah", "Evangeline",
                "Florence", "Grace", "Helena", "Iris", "Josephine",
                "Katherine", "Lavinia", "Magnolia", "Naomi", "Ophelia",
                "Penelope", "Quinn", "Ruby", "Savannah", "Temperance"
            ],
            "surnames": [
                "Blackwood", "Calhoun", "Dawson", "Evans", "Fletcher",
                "Garrett", "Hawthorne", "Irving", "Jackson", "Knox",
                "Lancaster", "Montgomery", "Nash", "O'Brien", "Parker",
                "Quinn", "Remington", "Sterling", "Thompson", "Whitmore"
            ]
        }
        
        try:
            with open(self.names_file, 'w', encoding='utf-8') as f:
                json.dump(default_names, f, indent=2)
            console.print(f"[green]Created default names file: {self.names_file}[/green]")
            # Don't overwrite names_data here - it's already set in __init__
        except Exception as e:
            console.print(f"[red]Error creating names file: {e}[/red]")
            # names_data is already set to defaults in __init__
    
    def _load_default_names(self):
        """Load default names directly into memory (fallback)."""
        self.names_data = {
            "male_first_names": [
                "Augustus", "Benjamin", "Caleb", "Dalton", "Ezra",
                "Franklin", "Gideon", "Hank", "Isaiah", "Jasper",
                "Knox", "Luther", "Montgomery", "Nathaniel", "Obadiah",
                "Porter", "Quincy", "Reuben", "Silas", "Thaddeus"
            ],
            "female_first_names": [
                "Adelaide", "Beatrice", "Charlotte", "Delilah", "Evangeline",
                "Florence", "Grace", "Helena", "Iris", "Josephine",
                "Katherine", "Lavinia", "Magnolia", "Naomi", "Ophelia",
                "Penelope", "Quinn", "Ruby", "Savannah", "Temperance"
            ],
            "surnames": [
                "Blackwood", "Calhoun", "Dawson", "Evans", "Fletcher",
                "Garrett", "Hawthorne", "Irving", "Jackson", "Knox",
                "Lancaster", "Montgomery", "Nash", "O'Brien", "Parker",
                "Quinn", "Remington", "Sterling", "Thompson", "Whitmore"
            ]
        }
    
    def generate_random_name(self, gender: Optional[str] = None) -> str:
        """Generate a random name. If gender not specified, will prompt user."""
        # Ensure we have valid names data
        if not self.names_data or 'male_first_names' not in self.names_data:
            console.print("[red]Names data not properly loaded. Using fallback names.[/red]")
            self._load_default_names()
        
        if not gender:
            gender = self._ask_for_gender()
        
        # Get appropriate first name list
        if gender.lower() in ['male', 'm']:
            first_names = self.names_data['male_first_names']
        elif gender.lower() in ['female', 'f']:
            first_names = self.names_data['female_first_names']
        else:
            console.print("[red]Invalid gender specified. Using male names as default.[/red]")
            first_names = self.names_data['male_first_names']
        
        # Pick random names
        first_name = random.choice(first_names)
        surname = random.choice(self.names_data['surnames'])
        
        full_name = f"{first_name} {surname}"
        return full_name
    
    def _ask_for_gender(self) -> str:
        """Ask user for character gender with Rich styling."""
        gender_panel = Panel(
            "[bold sandy_brown]Choose your character's gender:[/bold sandy_brown]\n"
            "[bold]M[/bold]ale\n"
            "[bold]F[/bold]emale",
            title="[bold gold1]Character Gender[/bold gold1]",
            border_style="gold1"
        )
        console.print(gender_panel)
        
        gender = Prompt.ask(
            "Gender",
            choices=["M", "F", "Male", "Female", "m", "f", "male", "female"],
            default="M",
            console=console,
            show_choices=False
        )
        
        return gender
    
    def get_random_first_name(self, gender: str) -> str:
        """Get just a random first name."""
        if gender.lower() in ['male', 'm']:
            return random.choice(self.names_data['male_first_names'])
        elif gender.lower() in ['female', 'f']:
            return random.choice(self.names_data['female_first_names'])
        else:
            return random.choice(self.names_data['male_first_names'])
    
    def get_random_surname(self) -> str:
        """Get just a random surname."""
        return random.choice(self.names_data['surnames'])

    
    def add_name(self, category: str, name: str) -> bool:
        """Add a name to a specific category (runtime only)."""
        valid_categories = ['male_first_names', 'female_first_names', 'surnames']
        
        if category not in valid_categories:
            console.print(f"[red]Invalid category. Must be one of: {', '.join(valid_categories)}[/red]")
            return False
        
        if name not in self.names_data[category]:
            self.names_data[category].append(name)
            console.print(f"[green]Added '{name}' to {category}[/green]")
            return True
        else:
            console.print(f"[yellow]'{name}' already exists in {category}[/yellow]")
            return False
    
    def save_names_to_file(self) -> bool:
        """Save current names back to the JSON file."""
        try:
            with open(self.names_file, 'w', encoding='utf-8') as f:
                json.dump(self.names_data, f, indent=2)
            
            console.print(f"[green]Names saved to {self.names_file}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Error saving names: {e}[/red]")
            return False
    
    def reload_names(self):
        """Reload names from file (useful for development)."""
        self.load_names()


# Global name generator instance
name_generator = NameGenerator()