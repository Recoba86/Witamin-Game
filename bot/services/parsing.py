"""Parsing utilities for handling multi-language input."""
import re
from typing import Optional

# Digit translation tables
PERSIAN_TO_ENGLISH = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
ARABIC_TO_ENGLISH = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')

def normalize_digits(text: str) -> str:
    """
    Convert Persian and Arabic numerals to English numerals.
    
    Args:
        text: Input text that may contain Persian/Arabic numerals
        
    Returns:
        Text with all numerals converted to English
    """
    # First convert Persian digits
    text = text.translate(PERSIAN_TO_ENGLISH)
    # Then convert Arabic digits
    text = text.translate(ARABIC_TO_ENGLISH)
    return text

def extract_guess(text: str) -> Optional[int]:
    """
    Extract a numeric guess from user message text.
    
    Args:
        text: User message text
        
    Returns:
        Integer guess if found and valid, None otherwise
    """
    # Normalize digits first
    normalized = normalize_digits(text.strip())
    
    # Try to extract a number
    # Look for standalone numbers (not part of a larger word)
    match = re.search(r'\b(\d+)\b', normalized)
    
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    
    return None
