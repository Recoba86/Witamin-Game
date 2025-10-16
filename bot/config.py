"""Configuration module for the Telegram Game Bot."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN must be set in .env file")

# Admin configuration
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip().isdigit()]

# Database configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "game_bot.db")

# Game configuration
MIN_NUMBER = int(os.getenv("MIN_NUMBER", "1"))
MAX_NUMBER = int(os.getenv("MAX_NUMBER", "10000"))
MAX_GUESSES_PER_PLAYER = 10
ROUND_DURATION_MINUTES = int(os.getenv("ROUND_DURATION_MINUTES", "2"))
MIN_GUESSES_BEFORE_CLOSE = 10  # Minimum guesses before timer can close round

# Round costs (suggested, displayed only)
ROUND_COSTS = {
    1: 1,
    2: 5,
    3: 20,
    4: 50,
    5: 100,
    6: 200,
    7: 500,
    8: 1000,
}

# Default cost for rounds beyond defined
def get_round_cost(round_number: int) -> int:
    """Get the suggested star cost for a given round number."""
    return ROUND_COSTS.get(round_number, ROUND_COSTS.get(max(ROUND_COSTS.keys()), 1000))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Language configuration
LANGUAGE = os.getenv("LANGUAGE", "en").lower()  # 'en' for English, 'fa' for Persian
if LANGUAGE not in ["en", "fa"]:
    raise ValueError("LANGUAGE must be either 'en' (English) or 'fa' (Persian/Farsi)")

