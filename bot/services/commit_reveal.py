"""Commit-Reveal service for provably fair number generation."""
import hashlib
import secrets
from typing import Tuple

def make_commit(number: int) -> Tuple[int, str, str]:
    """
    Generate a provably fair commitment.
    
    Args:
        number: The secret number to commit
        
    Returns:
        Tuple of (number, salt, hash)
    """
    salt = secrets.token_hex(16)
    hash_input = f"{number}:{salt}"
    target_hash = hashlib.sha256(hash_input.encode()).hexdigest()
    
    return (number, salt, target_hash)

def verify(number: int, salt: str, expected_hash: str) -> bool:
    """
    Verify that a number and salt produce the expected hash.
    
    Args:
        number: The revealed number
        salt: The revealed salt
        expected_hash: The hash that was committed earlier
        
    Returns:
        True if verification succeeds, False otherwise
    """
    hash_input = f"{number}:{salt}"
    computed_hash = hashlib.sha256(hash_input.encode()).hexdigest()
    
    return computed_hash == expected_hash
