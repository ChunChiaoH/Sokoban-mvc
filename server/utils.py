# Utility functions for Sokoban game
# Shared functions used by multiple controllers

from constants import MOVE_DIRECTIONS

def delta_to_direction_name(delta):
    """
    Convert movement delta (row, col) to direction name.
    
    Args:
        delta (tuple): Movement delta like (-1, 0) for UP
        
    Returns:
        str: Direction name like 'UP', 'DOWN', 'LEFT', 'RIGHT', or 'UNKNOWN'
        
    Example:
        delta_to_direction_name((-1, 0)) -> 'UP'
        delta_to_direction_name((0, 1)) -> 'RIGHT'
    """
    for direction, info in MOVE_DIRECTIONS.items():
        if info['delta'] == delta:
            return direction
    return 'UNKNOWN'

def direction_name_to_delta(direction_name):
    """
    Convert direction name to movement delta.
    
    Args:
        direction_name (str): Direction like 'UP', 'down', 'Left'
        
    Returns:
        tuple or None: Movement delta like (-1, 0) or None if invalid
        
    Example:
        direction_name_to_delta('UP') -> (-1, 0)
        direction_name_to_delta('invalid') -> None
    """
    direction_upper = direction_name.upper()
    if direction_upper in MOVE_DIRECTIONS:
        return MOVE_DIRECTIONS[direction_upper]['delta']
    return None