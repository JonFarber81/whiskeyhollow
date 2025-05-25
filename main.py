"""Simple Western RPG Character Creator."""

import os
from character import Character
from file_manager import SaveManager


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_title():
    """Display the game title."""
    print("""

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

    
    """)


def get_character_name() -> str:
    """Get character name from user."""
    while True:
        name = input("Enter character name: ").strip()
        if name and len(name) <= 20:
            return name
        print("Please enter a valid name (1-20 characters)")


def create_new_character() -> Character:
    """Create a new character."""
    clear_screen()
    show_title()
    
    name = get_character_name()
    character = Character(name)
    
    print(f"\nCreating character: {name}")
    print("\nRolling attributes...")
    
    while True:
        character.roll_attributes()
        character.display_character_sheet()
        
        choice = input("\n1. Keep these stats\n2. Roll again\n3. Set manually\nChoice: ").strip()
        
        if choice == "1":
            break
        elif choice == "2":
            continue
        elif choice == "3":
            set_manual_attributes(character)
            break
        else:
            print("Invalid choice, keeping current stats.")
            break
    
    return character


def set_manual_attributes(character: Character):
    """Set attributes manually."""
    print("\nSet attributes manually (3-18):")
    
    while True:
        try:
            vigor = int(input("Vigor: "))
            finesse = int(input("Finesse: "))
            smarts = int(input("Smarts: "))
            
            if all(3 <= attr <= 18 for attr in [vigor, finesse, smarts]):
                character.vigor = vigor
                character.finesse = finesse
                character.smarts = smarts
                character.calculate_derived_stats()
                break
            else:
                print("All attributes must be between 3 and 18.")
        except ValueError:
            print("Please enter valid numbers.")


def load_character(save_manager: SaveManager) -> Character:
    """Load an existing character."""
    saves = save_manager.list_save_files()
    
    if not saves:
        print("No saved characters found.")
        input("Press Enter to continue...")
        return None
    
    print("\nSaved Characters:")
    for i, filename in enumerate(saves, 1):
        info = save_manager.get_save_info(filename)
        if info:
            print(f"{i}. {info['name']} (Level {info['level']}, ${info['dollars']})")
        else:
            print(f"{i}. {filename}")
    
    try:
        choice = int(input(f"\nSelect character (1-{len(saves)}): "))
        if 1 <= choice <= len(saves):
            return save_manager.load_character(saves[choice - 1])
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")
    
    return None


def main():
    """Main program loop."""
    save_manager = SaveManager()
    current_character = None
    
    while True:
        clear_screen()
        show_title()
        
        if current_character:
            print(f"Current Character: {current_character.name}")
        
        print("\n1. Create New Character")
        print("2. Load Character")
        if current_character:
            print("3. View Character Sheet")
            print("4. Save Character")
        print("0. Quit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            current_character = create_new_character()
            if current_character:
                print(f"\nCharacter '{current_character.name}' created!")
                input("Press Enter to continue...")
        
        elif choice == "2":
            loaded_char = load_character(save_manager)
            if loaded_char:
                current_character = loaded_char
                input("Press Enter to continue...")
        
        elif choice == "3" and current_character:
            clear_screen()
            current_character.display_character_sheet()
            input("\nPress Enter to continue...")
        
        elif choice == "4" and current_character:
            save_manager.save_character(current_character)
            input("Press Enter to continue...")
        
        elif choice == "0":
            print("\nThanks for playing!")
            break
        
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()