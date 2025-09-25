import math
from typing import Tuple
from utils import pixel_distance

def get_scores(guess_point: Tuple[float, float], correct_point: Tuple[float, float], 
               max_distance: float = 1000.0, decay_factor: float = 0.01) -> int:
    """
    Calculate score based on pixel distance
    
    Args:
        guess_point: Player's guessed coordinates (x, y)
        correct_point: Correct coordinates (x, y)
        max_distance: Maximum distance (returns 0 points if exceeded)
        decay_factor: Exponential decay coefficient (higher = more rapid point loss)
    
    Returns:
        Calculated score (0-5000 integer)
    """
    from utils import pixel_distance
    
    # Calculate pixel distance
    distance = pixel_distance(guess_point, correct_point)
    
    # Return 0 points if exceeding maximum distance
    if distance >= max_distance:
        return 0
    
    # Exponential point reduction calculation
    # Maximum points (5000) when distance is 0
    # Exponentially decreases as distance increases
    score = 5000 * math.exp(-decay_factor * distance)
    
    # Round to integer and return
    return int(score)


