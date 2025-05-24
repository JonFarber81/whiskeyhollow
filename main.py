import random
import time
import os
import json
from datetime import datetime

class Character:
    def __init__(self, name=""):
        self.name = name
        self.level = 1
        self.experience = 0
        self.gold = random.randint(20, 50)
        
        # Core attributes (3-18 range)
        self.vigor = 0      # Physical strength, endurance, toughness
        self.finesse = 0    # Dexterity, agility, coordination
        self.smarts = 0     # Intelligence, wisdom, awareness
        
        # Derived stats
        self.hit_points = 0
        self.max_hit_points = 0
        
        # Starting inventory
        self.inventory = ["Worn Boots", "Tattered Hat", "Old Knife"]
        self.weapon = "Old Knife"
        self.armor = "Worn Clothes"
        
        # Game progress
        self.location = "Dusty Creek"
        self.quests = []
        self.reputation = 0

    def roll_attributes(self):
        """Roll 4d6, drop lowest for each attribute"""
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
    
    def calculate_derived_stats(self):
        """Calculate hit points based on all three attributes"""
        # Hit points = (Vigor + Finesse + Smarts) / 3
        self.max_hit_points = (self.vigor + self.finesse + self.smarts) // 3
        self.hit_points = self.max_hit_points
    
    def get_attribute_modifier(self, attribute):
        """Get D&D-style modifier for an attribute"""
        return (attribute - 10) // 2
    
    def display_character_sheet(self):
        """Display formatted character information"""
        print("\n" + "="*50)
        print(f"CHARACTER SHEET - {self.name.upper()}")
        print("="*50)
        print(f"Level: {self.level}    Experience: {self.experience}")
        print(f"Gold: ${self.gold}    Location: {self.location}")
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

class WesternRPG:
    def __init__(self):
        self.player = None
        self.game_running = True
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def type_text(self, text, delay=0.03):
        """Print text with typewriter effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def display_title_screen(self):
        """Display ASCII art title screen"""
        title_art = """

██╗    ██╗██╗  ██╗██╗███████╗██╗  ██╗███████╗██╗   ██╗
██║    ██║██║  ██║██║██╔════╝██║ ██╔╝██╔════╝╚██╗ ██╔╝
██║ █╗ ██║███████║██║███████╗█████╔╝ █████╗   ╚████╔╝ 
██║███╗██║██╔══██║██║╚════██║██╔═██╗ ██╔══╝    ╚██╔╝  
╚███╔███╔╝██║  ██║██║███████║██║  ██╗███████╗   ██║   
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   

██╗  ██╗ ██████╗ ██╗     ██╗      ██████╗ ██╗    ██╗
██║  ██║██╔═══██╗██║     ██║     ██╔═══██╗██║    ██║
███████║██║   ██║██║     ██║     ██║   ██║██║ █╗ ██║
██╔══██║██║   ██║██║     ██║     ██║   ██║██║███╗██║
██║  ██║╚██████╔╝███████╗███████╗╚██████╔╝╚███╔███╔╝
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝ ╚═════╝  ╚══╝╚══╝ 

                    ~ RECKONING ~
                    
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░                                      ░
        ░    A tale of vengeance in the West   ░
        ░                                      ░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

        """
        
        print(title_art)
    
    def main_menu(self):
        """Display main menu and handle selection"""
        while self.game_running:
            self.clear_screen()
            self.display_title_screen()
            
            print("\n\n" + "="*50)
            print("MAIN MENU".center(50))
            print("="*50)
            print("1. New Game")
            print("2. Load Game")
            print("3. Credits")
            print("4. Quit")
            print("="*50)
            
            choice = input("\nWhat's your choice, partner? ").strip()
            
            if choice == "1":
                self.new_game()
            elif choice == "2":
                self.load_game()
            elif choice == "3":
                self.show_credits()
            elif choice == "4":
                self.quit_game()
            else:
                print("\nInvalid choice. Try again, stranger.")
                time.sleep(1)
    
    def new_game(self):
        """Start character creation process"""
        self.clear_screen()
        
        print("\n" + "="*60)
        print("WELCOME TO THE OLD WEST".center(60))
        print("="*60)
        
        self.type_text("\nYou step off the dusty stagecoach in the frontier town of Whiskey Hollow.")
        self.type_text("The sun beats down mercilessly as you adjust your hat and look around.")
        self.type_text("This is not where your story begins, but it is where your vengeance does...")
        
        # Character name input
        print("\n" + "-"*50)
        while True:
            name = input("What do folks call you? ").strip()
            if name and len(name) <= 20:
                break
            print("Enter a valid name (1-20 characters).")
        
        self.player = Character(name)
        
        print(f"\nWell howdy, {name}! Time to see what you're made of...")
        input("\nPress Enter to roll your attributes...")
        
        self.attribute_rolling_process()
    
    def attribute_rolling_process(self):
        """Handle the attribute rolling with player choice"""
        while True:
            self.clear_screen()
            print("\n" + "="*60)
            print("ROLLING YOUR ATTRIBUTES".center(60))
            print("="*60)
            print("Rolling 4d6 and taking the highest 3 for each attribute...")
            print("\nPress Enter to roll...")
            input()
            
            # Animate the rolling process
            print("\nRolling dice...")
            for i in range(3):
                print("." * (i + 1), end="", flush=True)
                time.sleep(0.5)
            print("\n")
            
            self.player.roll_attributes()
            self.player.display_character_sheet()
            
            print("\nDo you want to:")
            print("1. Keep these attributes")
            print("2. Roll again")
            print("3. Manually set attributes (for testing)")
            
            choice = input("\nYour choice: ").strip()
            
            if choice == "1":
                break
            elif choice == "2":
                continue
            elif choice == "3":
                self.manual_attribute_setting()
                break
            else:
                print("Invalid choice. Keeping current attributes.")
                time.sleep(1)
                break
        
        self.finalize_character()
    
    def manual_attribute_setting(self):
        """Allow manual attribute setting for testing"""
        print("\nManual Attribute Setting (Enter values 3-18)")
        attributes = ['vigor', 'finesse', 'smarts']
        
        for attr in attributes:
            while True:
                try:
                    value = int(input(f"{attr.capitalize()}: "))
                    if 3 <= value <= 18:
                        setattr(self.player, attr, value)
                        break
                    else:
                        print("Value must be between 3 and 18.")
                except ValueError:
                    print("Please enter a valid number.")
        
        self.player.calculate_derived_stats()
    
    def finalize_character(self):
        """Complete character creation"""
        self.clear_screen()
        print("\n" + "="*60)
        print("CHARACTER CREATION COMPLETE".center(60))
        print("="*60)
        
        self.player.display_character_sheet()
        
        print(f"\nWelcome to Whiskey Hollow, {self.player.name}!")
        self.type_text("You've got a few dollars in your pocket, some basic gear, and a world of possibilities ahead.")
        
        # Starting equipment flavor text
        print(f"\nYou're carrying:")
        for item in self.player.inventory:
            print(f"  - {item}")
        
        print(f"\nStarting gold: ${self.player.gold}")
        
        input("\nPress Enter to begin your adventure...")
        
        # Save the character
        self.save_character()
        
        # Here you would transition to the main game
        print("\n[Game would continue here...]")
        input("Press Enter to return to main menu...")
    
    def save_character(self):
        """Save character data to file"""
        if not os.path.exists('saves'):
            os.makedirs('saves')
        
        save_data = {
            'name': self.player.name,
            'level': self.player.level,
            'experience': self.player.experience,
            'gold': self.player.gold,
            'vigor': self.player.vigor,
            'finesse': self.player.finesse,
            'smarts': self.player.smarts,
            'hit_points': self.player.hit_points,
            'max_hit_points': self.player.max_hit_points,
            'inventory': self.player.inventory,
            'weapon': self.player.weapon,
            'armor': self.player.armor,
            'location': self.player.location,
            'quests': self.player.quests,
            'reputation': self.player.reputation,
            'save_date': datetime.now().isoformat()
        }
        
        filename = f"saves/{self.player.name.lower().replace(' ', '_')}_save.json"
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"\nGame saved as: {filename}")
    
    def load_game(self):
        """Load a saved game"""
        if not os.path.exists('saves'):
            print("\nNo saved games found.")
            time.sleep(2)
            return
        
        save_files = [f for f in os.listdir('saves') if f.endswith('_save.json')]
        
        if not save_files:
            print("\nNo saved games found.")
            time.sleep(2)
            return
        
        print("\nSaved Games:")
        for i, save_file in enumerate(save_files, 1):
            # Extract character name from filename
            char_name = save_file.replace('_save.json', '').replace('_', ' ').title()
            print(f"{i}. {char_name}")
        
        try:
            choice = int(input("\nSelect save file (number): "))
            if 1 <= choice <= len(save_files):
                self.load_character_from_file(f"saves/{save_files[choice-1]}")
            else:
                print("Invalid selection.")
                time.sleep(1)
        except ValueError:
            print("Invalid input.")
            time.sleep(1)
    
    def load_character_from_file(self, filename):
        """Load character from save file"""
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            self.player = Character(save_data['name'])
            
            # Load all attributes
            for key, value in save_data.items():
                if hasattr(self.player, key):
                    setattr(self.player, key, value)
            
            print(f"\nGame loaded successfully!")
            print(f"Welcome back, {self.player.name}!")
            time.sleep(2)
            
            # Here you would continue to the main game
            print("\n[Game would continue here...]")
            input("Press Enter to return to main menu...")
            
        except Exception as e:
            print(f"\nError loading save file: {e}")
            time.sleep(2)
    
    def show_credits(self):
        """Display game credits"""
        self.clear_screen()
        print("\n" + "="*50)
        print("CREDITS".center(50))
        print("="*50)
        print("\nWhiskey Hollow - A Western RPG")
        print("Developed by: Jon Farber")
        print("Python Version: 3.x")
        print("\n" + "="*50)
        input("\nPress Enter to return to main menu...")
    
    def quit_game(self):
        """Exit the game"""
        print("\nThanks for playing, partner!")
        print("See you on the frontier...")
        self.game_running = False

def main():
    """Main game entry point"""
    game = WesternRPG()
    game.main_menu()

if __name__ == "__main__":
    main()