"""Flexible dice rolling utilities for Western RPG game."""

import random
from typing import List, Optional


def roll_dice(num_dice: int = 1, 
              sides: int = 6, 
              drop_lowest: int = 0, 
              drop_highest: int = 0,
              reroll_below: Optional[int] = None,
              exploding: bool = False,
              modifier: int = 0) -> dict:
    """
    Flexible dice rolling function that can handle various rolling methods.
    
    Args:
        num_dice: Number of dice to roll (default 1)
        sides: Number of sides per die (default 6)
        drop_lowest: Number of lowest dice to drop (default 0)
        drop_highest: Number of highest dice to drop (default 0)
        reroll_below: Reroll any die that shows this value or lower (default None)
        exploding: Whether dice "explode" (roll again on max value) (default False)
        modifier: Fixed modifier to add to final result (default 0)
    
    Returns:
        Dictionary containing:
        - 'result': Final calculated result
        - 'rolls': List of all individual die rolls
        - 'kept_rolls': List of dice that were kept after dropping
        - 'dropped_rolls': List of dice that were dropped
        - 'total_before_modifier': Total before applying modifier
    """
    if num_dice <= 0:
        raise ValueError("Number of dice must be positive")
    if sides <= 0:
        raise ValueError("Number of sides must be positive")
    if drop_lowest + drop_highest >= num_dice:
        raise ValueError("Cannot drop more dice than rolled")
    
    all_rolls = []
    
    # Roll initial dice
    for _ in range(num_dice):
        roll = _roll_single_die(sides, reroll_below, exploding)
        all_rolls.append(roll)
    
    # Sort rolls for dropping (highest to lowest)
    sorted_rolls = sorted(all_rolls, reverse=True)
    
    # Determine which dice to keep
    kept_rolls = sorted_rolls[drop_highest:len(sorted_rolls)-drop_lowest] if drop_lowest > 0 else sorted_rolls[drop_highest:]
    
    # Determine which dice were dropped
    dropped_rolls = []
    if drop_highest > 0:
        dropped_rolls.extend(sorted_rolls[:drop_highest])
    if drop_lowest > 0:
        dropped_rolls.extend(sorted_rolls[-drop_lowest:])
    
    # Calculate totals
    total_before_modifier = sum(kept_rolls)
    final_result = total_before_modifier + modifier
    
    return {
        'result': final_result,
        'rolls': all_rolls,
        'kept_rolls': kept_rolls,
        'dropped_rolls': dropped_rolls,
        'total_before_modifier': total_before_modifier,
        'modifier': modifier
    }


def _roll_single_die(sides: int, reroll_below: Optional[int] = None, exploding: bool = False) -> int:
    """
    Roll a single die with optional reroll and exploding mechanics.
    
    Args:
        sides: Number of sides on the die
        reroll_below: Reroll if result is this value or lower
        exploding: Whether the die explodes on maximum value
    
    Returns:
        Final result of the die roll
    """
    total = 0
    
    while True:
        roll = random.randint(1, sides)
        
        # Check for reroll condition
        if reroll_below is not None and roll <= reroll_below:
            continue  # Reroll this die
        
        total += roll
        
        # Check for exploding die
        if exploding and roll == sides:
            continue  # Roll again and add to total
        
        break  # Normal roll, we're done
    
    return total


# Convenience functions for common RPG rolls
def roll_4d6_drop_lowest() -> int:
    """Standard D&D attribute roll: 4d6 drop lowest."""
    return roll_dice(num_dice=4, sides=6, drop_lowest=1)['result']


def roll_3d6() -> int:
    """Simple 3d6 roll."""
    return roll_dice(num_dice=3, sides=6)['result']


def roll_starting_money() -> int:
    """Roll 3d6 * 10 for starting money."""
    return roll_dice(num_dice=3, sides=6)['result'] * 10


def roll_with_advantage() -> int:
    """Roll 2d20, keep highest (D&D advantage)."""
    return roll_dice(num_dice=2, sides=20, drop_lowest=1)['result']


def roll_with_disadvantage() -> int:
    """Roll 2d20, keep lowest (D&D disadvantage)."""
    return roll_dice(num_dice=2, sides=20, drop_highest=1)['result']


# Example usage and testing
if __name__ == "__main__":
    print("=== Dice Rolling Examples ===")
    
    # Standard attribute roll
    result = roll_dice(num_dice=4, sides=6, drop_lowest=1)
    print(f"4d6 drop lowest: {result['result']} (rolled: {result['rolls']}, kept: {result['kept_rolls']})")
    
    # Heroic attribute roll
    result = roll_dice(num_dice=4, sides=6, drop_lowest=1, reroll_below=2)
    print(f"Heroic 4d6: {result['result']} (rolled: {result['rolls']}, kept: {result['kept_rolls']})")
    
    # Exploding d10
    result = roll_dice(num_dice=1, sides=10, exploding=True)
    print(f"Exploding d10: {result['result']} (all rolls: {result['rolls']})")
    
    # Roll with modifier
    result = roll_dice(num_dice=1, sides=20, modifier=5)
    print(f"d20+5: {result['result']} (rolled: {result['rolls'][0]} + 5)")