"""Game state management for Western RPG game.

This module manages the overall game state including player progress,
world state, game settings, and persistent data that affects gameplay
beyond individual character stats.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from enum import Enum
from dataclasses import dataclass, asdict
from models.character import Character


class GamePhase(Enum):
    """Represents different phases of the game."""
    MAIN_MENU = "main_menu"
    CHARACTER_CREATION = "character_creation"
    TOWN_EXPLORATION = "town_exploration"
    WILDERNESS = "wilderness"
    COMBAT = "combat"
    DIALOGUE = "dialogue"
    INVENTORY = "inventory"
    SHOPPING = "shopping"
    QUEST_COMPLETE = "quest_complete"
    GAME_OVER = "game_over"


@dataclass
class Location:
    """Represents a game location.
    
    Attributes:
        name: Display name of the location.
        description: Detailed description of the location.
        available_actions: List of actions available at this location.
        npcs: List of NPCs present at this location.
        items: List of items that can be found here.
        visited: Whether the player has been here before.
        locked: Whether this location is currently accessible.
    """
    name: str
    description: str
    available_actions: List[str]
    npcs: List[str] = None
    items: List[str] = None
    visited: bool = False
    locked: bool = False
    
    def __post_init__(self):
        """Initialize default values for mutable fields."""
        if self.npcs is None:
            self.npcs = []
        if self.items is None:
            self.items = []


@dataclass
class Quest:
    """Represents a game quest.
    
    Attributes:
        id: Unique identifier for the quest.
        title: Display title of the quest.
        description: Detailed quest description.
        objectives: List of quest objectives.
        rewards: Dictionary of rewards (experience, money, items).
        status: Current quest status.
        giver: Name of the quest giver.
        location: Where the quest was obtained.
        prerequisites: List of quest IDs that must be completed first.
    """
    id: str
    title: str
    description: str
    objectives: List[str]
    rewards: Dict[str, Any]
    status: str = "available"  # available, active, completed, failed
    giver: str = ""
    location: str = ""
    prerequisites: List[str] = None
    
    def __post_init__(self):
        """Initialize default values for mutable fields."""
        if self.prerequisites is None:
            self.prerequisites = []


class WorldState:
    """Manages the state of the game world.
    
    Tracks locations, NPCs, global events, and world changes that
    persist across save/load cycles.
    
    Attributes:
        locations: Dictionary of all game locations.
        global_flags: Set of global boolean flags.
        global_variables: Dictionary of global variables.
        time_of_day: Current time in the game world.
        day_count: Number of days that have passed.
        weather: Current weather conditions.
        reputation_factions: Dictionary of faction reputation scores.
    """
    
    def __init__(self) -> None:
        """Initialize world state with default values."""
        self.locations: Dict[str, Location] = {}
        self.global_flags: Set[str] = set()
        self.global_variables: Dict[str, Any] = {}
        self.time_of_day: int = 12  # 24-hour format
        self.day_count: int = 1
        self.weather: str = "clear"
        self.reputation_factions: Dict[str, int] = {}
        
        self._initialize_default_locations()
        self._initialize_default_factions()
    
    def _initialize_default_locations(self) -> None:
        """Set up the default game locations."""
        self.locations = {
            "whiskey_hollow": Location(
                name="Whiskey Hollow",
                description="A dusty frontier town with wooden buildings and dirt roads.",
                available_actions=["visit_saloon", "visit_general_store", "visit_sheriff", "leave_town"]
            ),
            "dusty_creek": Location(
                name="Dusty Creek",
                description="A small settlement by a dried creek bed.",
                available_actions=["explore", "rest", "return_to_town"]
            ),
            "abandoned_mine": Location(
                name="Abandoned Mine",
                description="An old silver mine, now eerily quiet.",
                available_actions=["explore_mine", "return"],
                locked=True
            ),
            "saloon": Location(
                name="The Broken Wheel Saloon",
                description="A rowdy saloon filled with cowboys, gamblers, and troublemakers.",
                available_actions=["order_drink", "play_poker", "talk_to_patrons", "leave"],
                npcs=["bartender", "poker_players", "mysterious_stranger"]
            )
        }
    
    def _initialize_default_factions(self) -> None:
        """Set up default faction reputation."""
        self.reputation_factions = {
            "townsfolk": 0,
            "outlaws": 0,
            "lawmen": 0,
            "merchants": 0,
            "natives": 0
        }
    
    def set_flag(self, flag_name: str) -> None:
        """Set a global flag.
        
        Args:
            flag_name: Name of the flag to set.
        """
        self.global_flags.add(flag_name)
    
    def clear_flag(self, flag_name: str) -> None:
        """Clear a global flag.
        
        Args:
            flag_name: Name of the flag to clear.
        """
        self.global_flags.discard(flag_name)
    
    def has_flag(self, flag_name: str) -> bool:
        """Check if a global flag is set.
        
        Args:
            flag_name: Name of the flag to check.
            
        Returns:
            True if flag is set, False otherwise.
        """
        return flag_name in self.global_flags
    
    def set_variable(self, var_name: str, value: Any) -> None:
        """Set a global variable.
        
        Args:
            var_name: Name of the variable.
            value: Value to set.
        """
        self.global_variables[var_name] = value
    
    def get_variable(self, var_name: str, default: Any = None) -> Any:
        """Get a global variable value.
        
        Args:
            var_name: Name of the variable.
            default: Default value if variable doesn't exist.
            
        Returns:
            Variable value or default.
        """
        return self.global_variables.get(var_name, default)
    
    def visit_location(self, location_name: str) -> bool:
        """Mark a location as visited.
        
        Args:
            location_name: Name of the location.
            
        Returns:
            True if location exists and was marked, False otherwise.
        """
        if location_name in self.locations:
            self.locations[location_name].visited = True
            return True
        return False
    
    def unlock_location(self, location_name: str) -> bool:
        """Unlock a location.
        
        Args:
            location_name: Name of the location to unlock.
            
        Returns:
            True if location was unlocked, False if not found.
        """
        if location_name in self.locations:
            self.locations[location_name].locked = False
            return True
        return False
    
    def modify_reputation(self, faction: str, change: int) -> None:
        """Modify reputation with a faction.
        
        Args:
            faction: Name of the faction.
            change: Amount to change reputation (can be negative).
        """
        if faction in self.reputation_factions:
            self.reputation_factions[faction] += change
            # Clamp reputation between -100 and 100
            self.reputation_factions[faction] = max(-100, min(100, self.reputation_factions[faction]))
    
    def advance_time(self, hours: int = 1) -> None:
        """Advance game time.
        
        Args:
            hours: Number of hours to advance.
        """
        self.time_of_day += hours
        while self.time_of_day >= 24:
            self.time_of_day -= 24
            self.day_count += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert world state to dictionary.
        
        Returns:
            Dictionary representation of world state.
        """
        return {
            'locations': {name: asdict(loc) for name, loc in self.locations.items()},
            'global_flags': list(self.global_flags),
            'global_variables': self.global_variables,
            'time_of_day': self.time_of_day,
            'day_count': self.day_count,
            'weather': self.weather,
            'reputation_factions': self.reputation_factions
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load world state from dictionary.
        
        Args:
            data: Dictionary containing world state data.
        """
        if 'locations' in data:
            self.locations = {
                name: Location(**loc_data) 
                for name, loc_data in data['locations'].items()
            }
        
        if 'global_flags' in data:
            self.global_flags = set(data['global_flags'])
        
        if 'global_variables' in data:
            self.global_variables = data['global_variables']
        
        if 'time_of_day' in data:
            self.time_of_day = data['time_of_day']
        
        if 'day_count' in data:
            self.day_count = data['day_count']
        
        if 'weather' in data:
            self.weather = data['weather']
        
        if 'reputation_factions' in data:
            self.reputation_factions = data['reputation_factions']


class GameState:
    """Main game state manager.
    
    Coordinates the overall game state including player character,
    world state, quest progress, and game settings.
    
    Attributes:
        player: The player character.
        world: The world state.
        current_phase: Current game phase.
        current_location: Current player location.
        active_quests: List of active quests.
        completed_quests: List of completed quests.
        game_settings: Dictionary of game settings.
        statistics: Dictionary of game statistics.
    """
    
    def __init__(self) -> None:
        """Initialize game state."""
        self.player: Optional[Character] = None
        self.world: WorldState = WorldState()
        self.current_phase: GamePhase = GamePhase.MAIN_MENU
        self.current_location: str = "whiskey_hollow"
        self.active_quests: List[Quest] = []
        self.completed_quests: List[Quest] = []
        self.game_settings: Dict[str, Any] = self._initialize_default_settings()
        self.statistics: Dict[str, Any] = self._initialize_statistics()
        self.save_timestamp: Optional[str] = None
    
    def _initialize_default_settings(self) -> Dict[str, Any]:
        """Initialize default game settings.
        
        Returns:
            Dictionary of default game settings.
        """
        return {
            'difficulty': 'normal',
            'auto_save': True,
            'show_dice_rolls': True,
            'combat_speed': 'normal',
            'text_speed': 'normal',
            'sound_enabled': True,
            'music_enabled': True
        }
    
    def _initialize_statistics(self) -> Dict[str, Any]:
        """Initialize game statistics tracking.
        
        Returns:
            Dictionary of game statistics.
        """
        return {
            'play_time_minutes': 0,
            'locations_visited': 0,
            'quests_completed': 0,
            'enemies_defeated': 0,
            'money_earned': 0,
            'money_spent': 0,
            'items_found': 0,
            'deaths': 0,
            'saves_loaded': 0,
            'dialogue_choices_made': 0
        }
    
    def set_player(self, character: Character) -> None:
        """Set the player character.
        
        Args:
            character: The player character.
        """
        self.player = character
        if character.location in self.world.locations:
            self.current_location = character.location
    
    def change_phase(self, new_phase: GamePhase) -> None:
        """Change the current game phase.
        
        Args:
            new_phase: The new game phase to enter.
        """
        self.current_phase = new_phase
    
    def move_player_to_location(self, location_name: str) -> bool:
        """Move player to a new location.
        
        Args:
            location_name: Name of the destination location.
            
        Returns:
            True if move was successful, False otherwise.
        """
        if location_name not in self.world.locations:
            return False
        
        location = self.world.locations[location_name]
        if location.locked:
            return False
        
        self.current_location = location_name
        if self.player:
            self.player.location = location_name
        
        # Mark location as visited and update statistics
        if not location.visited:
            self.world.visit_location(location_name)
            self.statistics['locations_visited'] += 1
        
        return True
    
    def add_quest(self, quest: Quest) -> bool:
        """Add a quest to the active quest list.
        
        Args:
            quest: Quest to add.
            
        Returns:
            True if quest was added, False if already exists.
        """
        # Check if quest already exists
        if any(q.id == quest.id for q in self.active_quests):
            return False
        
        # Check prerequisites
        for prereq in quest.prerequisites:
            if not any(q.id == prereq and q.status == "completed" for q in self.completed_quests):
                return False
        
        quest.status = "active"
        self.active_quests.append(quest)
        return True
    
    def complete_quest(self, quest_id: str) -> Optional[Quest]:
        """Complete a quest and move it to completed list.
        
        Args:
            quest_id: ID of the quest to complete.
            
        Returns:
            Completed Quest object or None if not found.
        """
        for i, quest in enumerate(self.active_quests):
            if quest.id == quest_id:
                quest.status = "completed"
                completed_quest = self.active_quests.pop(i)
                self.completed_quests.append(completed_quest)
                
                # Apply quest rewards
                self._apply_quest_rewards(completed_quest)
                
                # Update statistics
                self.statistics['quests_completed'] += 1
                
                return completed_quest
        
        return None
    
    def _apply_quest_rewards(self, quest: Quest) -> None:
        """Apply rewards from a completed quest.
        
        Args:
            quest: The completed quest.
        """
        if not self.player:
            return
        
        rewards = quest.rewards
        
        if 'experience' in rewards:
            self.player.add_experience(rewards['experience'])
        
        if 'money' in rewards:
            self.player.add_dollars(rewards['money'])
            self.statistics['money_earned'] += rewards['money']
        
        if 'items' in rewards:
            for item in rewards['items']:
                self.player.add_item(item)
                self.statistics['items_found'] += 1
        
        if 'reputation' in rewards:
            for faction, change in rewards['reputation'].items():
                self.world.modify_reputation(faction, change)
    
    def fail_quest(self, quest_id: str) -> Optional[Quest]:
        """Fail a quest and remove it from active list.
        
        Args:
            quest_id: ID of the quest to fail.
            
        Returns:
            Failed Quest object or None if not found.
        """
        for i, quest in enumerate(self.active_quests):
            if quest.id == quest_id:
                quest.status = "failed"
                return self.active_quests.pop(i)
        
        return None
    
    def get_available_quests(self, location: str = None) -> List[Quest]:
        """Get quests available at a location or globally.
        
        Args:
            location: Location to check for quests (None for all).
            
        Returns:
            List of available quests.
        """
        # This would typically load from game data files
        # For now, return empty list
        return []
    
    def update_statistic(self, stat_name: str, value: Any) -> None:
        """Update a game statistic.
        
        Args:
            stat_name: Name of the statistic.
            value: Value to set or add (depending on statistic type).
        """
        if stat_name in self.statistics:
            if isinstance(self.statistics[stat_name], (int, float)):
                self.statistics[stat_name] += value
            else:
                self.statistics[stat_name] = value
    
    def get_current_location_info(self) -> Optional[Location]:
        """Get information about the current location.
        
        Returns:
            Location object for current location or None if not found.
        """
        return self.world.locations.get(self.current_location)
    
    def can_perform_action(self, action: str) -> bool:
        """Check if an action can be performed at current location.
        
        Args:
            action: Action to check.
            
        Returns:
            True if action is available, False otherwise.
        """
        location = self.get_current_location_info()
        if not location:
            return False
        
        return action in location.available_actions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert game state to dictionary for saving.
        
        Returns:
            Dictionary representation of game state.
        """
        return {
            'player': self.player.to_dict() if self.player else None,
            'world': self.world.to_dict(),
            'current_phase': self.current_phase.value,
            'current_location': self.current_location,
            'active_quests': [asdict(q) for q in self.active_quests],
            'completed_quests': [asdict(q) for q in self.completed_quests],
            'game_settings': self.game_settings,
            'statistics': self.statistics,
            'save_timestamp': datetime.now().isoformat()
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load game state from dictionary.
        
        Args:
            data: Dictionary containing game state data.
        """
        if 'player' in data and data['player']:
            self.player = Character()
            self.player.from_dict(data['player'])
        
        if 'world' in data:
            self.world.from_dict(data['world'])
        
        if 'current_phase' in data:
            self.current_phase = GamePhase(data['current_phase'])
        
        if 'current_location' in data:
            self.current_location = data['current_location']
        
        if 'active_quests' in data:
            self.active_quests = [Quest(**q) for q in data['active_quests']]
        
        if 'completed_quests' in data:
            self.completed_quests = [Quest(**q) for q in data['completed_quests']]
        
        if 'game_settings' in data:
            self.game_settings.update(data['game_settings'])
        
        if 'statistics' in data:
            self.statistics.update(data['statistics'])
        
        if 'save_timestamp' in data:
            self.save_timestamp = data['save_timestamp']
            self.statistics['saves_loaded'] += 1


def create_new_game_state() -> GameState:
    """Factory function to create a new game state.
    
    Returns:
        New GameState instance with default values.
    """
    return GameState()


def load_game_state_from_dict(data: Dict[str, Any]) -> GameState:
    """Load game state from dictionary data.
    
    Args:
        data: Dictionary containing saved game state.
        
    Returns:
        GameState instance loaded from data.
    """
    game_state = GameState()
    game_state.from_dict(data)
    return game_state