"""Validation utilities for game logic."""
from typing import Optional
from bot.config import MIN_NUMBER, MAX_NUMBER, MAX_GUESSES_PER_PLAYER
from bot.storage.models import GameStatus, RoundStatus

def validate_guess_range(guess: int) -> bool:
    """
    Validate that a guess is within the acceptable range.
    
    Args:
        guess: The numeric guess
        
    Returns:
        True if valid, False otherwise
    """
    return MIN_NUMBER <= guess <= MAX_NUMBER

def validate_game_status_for_guess(game_status: str) -> bool:
    """
    Validate that the game is in a state that accepts guesses.
    
    Args:
        game_status: Current game status
        
    Returns:
        True if guesses can be accepted, False otherwise
    """
    return game_status in [GameStatus.ROUND_ACTIVE]

def validate_round_status_for_guess(round_status: str) -> bool:
    """
    Validate that the round is in a state that accepts guesses.
    
    Args:
        round_status: Current round status
        
    Returns:
        True if guesses can be accepted, False otherwise
    """
    return round_status == RoundStatus.ACTIVE

def validate_guess_limit(current_guesses: int) -> bool:
    """
    Validate that player hasn't exceeded guess limit for the round.
    
    Args:
        current_guesses: Number of guesses player has already made
        
    Returns:
        True if player can make another guess, False otherwise
    """
    return current_guesses < MAX_GUESSES_PER_PLAYER

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass
