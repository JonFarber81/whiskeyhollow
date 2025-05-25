"""Dice rolling utilities for Western RPG game."""

import random
from typing import Dict, Any


def roll_dice(num_dice: int = 1, 
              sides: int = 6, 
              drop_lowest: int = 0, 
              drop_highest: int = 0,
              reroll_below: int = None,
              modifier: int = 0) -> Dict[str, Any]:
    """
    Flexible dice rolling function.
    
    Args:
        num_dice: Number of dice to roll
        sides: Number of sides per die
        drop_lowest: Number of lowest dice to drop
        drop_highest: Number of highest dice to drop
        reroll_below: Reroll any die showing this value or lower
        modifier: Fixed modifier to add to result
    
    Returns:
        Dictionary with 'result', 'rolls', 'kept_rolls', 'dropped_rolls'
    """
    if num_dice <= 0 or sides <= 0:
        raise ValueError("Dice and sides must be positive")
    if drop_lowest + drop_highest >= num_dice:
        raise ValueError("Cannot drop more dice than rolled")
    
    # Roll all dice
    all_rolls = []
    for _ in range(num_dice):
        roll = _roll_single_die(sides, reroll_below)
        all_rolls.append(roll)
    
    # Sort for dropping
    sorted_rolls = sorted(all_rolls, reverse=True)
    
    # Drop dice
    kept_rolls = sorted_rolls[drop_highest:]
    if drop_lowest > 0:
        kept_rolls = kept_rolls[:-drop_lowest]
    
    dropped_rolls = []
    if drop_highest > 0:
        dropped_rolls.extend(sorted_rolls[:drop_highest])
    if drop_lowest > 0:
        dropped_rolls.extend(sorted_rolls[-drop_lowest:])
    
    result = sum(kept_rolls) + modifier
    
    return {
        'result': result,
        'rolls': all_rolls,
        'kept_rolls': kept_rolls,
        'dropped_rolls': dropped_rolls,
        'modifier': modifier
    }


def _roll_single_die(sides: int, reroll_below: int = None) -> int:
    """Roll a single die with optional reroll."""
    while True:
        roll = random.randint(1, sides)
        if reroll_below is None or roll > reroll_below:
            return roll


# Convenience functions
def roll_4d6_drop_lowest() -> int:
    """Standard D&D attribute roll."""
    return roll_dice(4, 6, drop_lowest=1)['result']


def roll_3d6() -> int:
    """Simple 3d6 roll."""
    return roll_dice(3, 6)['result']


def roll_starting_money() -> int:
    """Roll 3d6 * 10 for starting money."""
    return roll_dice(3, 6)['result'] * 10