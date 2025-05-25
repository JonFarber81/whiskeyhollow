# Whiskey Hollow ~ Reckoning

*A tale of vengeance in the West*

## Overview

Whiskey Hollow is a Python-based character creator and management system for Western tabletop RPGs. This project serves as both a practical application for enhancing my Python programming skills and a way to blend my love of westerns with tabletop gaming.

## About This Project

This character creator is designed as a learning exercise to explore various Python concepts including:
- Object-oriented programming with classes and inheritance
- File I/O operations and JSON serialization
- Terminal-based user interfaces
- Dice rolling mechanics and probability
- Data validation and error handling

The combination of western themes and RPG mechanics provides an engaging context for practicing Python development while building something genuinely useful for tabletop gaming.

## Game System

This project implements the character creation rules from **[Cowpunchers Reloaded](https://www.drivethrurpg.com/en/product/422586/cowpunchers-reloaded)**, an excellent Western tabletop RPG. The game features:

- **Three Core Attributes**: Vigor (physical strength), Finesse (agility), and Smarts (intelligence)
- **Age-Based Character Development**: Your character's age affects both starting skills and physical capabilities
- **Comprehensive Skill System**: 28+ skills covering everything from gunfighting to agriculture

*Support the original creators by purchasing Cowpunchers Reloaded from DriveThruRPG!*

## Features

### Character Creation
- **Attribute Rolling**: 4d6 drop lowest for balanced character generation
- **Age Effects System**: Detailed age-based bonuses and penalties
  - Young characters (14-22): Fewer skills but good physical attributes
  - Prime characters (23-34): Balanced development
  - Experienced characters (35-52): Many skills but declining physical abilities
  - Elder characters (53-57): Maximum skills but frail bodies
- **Interactive Skill Allocation**: Point-buy system with visual skill progression

### Character Management
- **Save/Load System**: JSON-based character persistence
- **Character Sheets**: Formatted display of all character information
- **Equipment Tracking**: Basic inventory and gear management


## Installation & Usage

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/whiskeyhollow.git
   cd whiskeyhollow
   ```

2. **Run the Application**
   ```bash
   python main.py
   ```

3. **Character Creation Flow**
   - Enter character name and age
   - Roll or manually set base attributes
   - Age effects are automatically applied
   - Allocate skill points interactively
   - Save your character for future use



## Contributing

This is primarily a personal learning project, but suggestions and feedback are welcome! If you notice any bugs or have ideas for improvements, feel free to open an issue.


## Acknowledgments

- **Cowpunchers Reloaded** by The Basic Expert - The excellent RPG system this implements


## License

This project is for educational and personal use. The game mechanics are based on Cowpunchers Reloaded - please support the original creators by purchasing the official rulebook.