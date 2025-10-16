"""Data models for the game bot."""
from enum import Enum
from datetime import datetime
from typing import Optional

class GameStatus(str, Enum):
    """Game status enumeration."""
    IDLE = "IDLE"
    GAME_COMMITTED = "GAME_COMMITTED"
    ROUND_ACTIVE = "ROUND_ACTIVE"
    ROUND_PAUSED = "ROUND_PAUSED"
    GAME_FINISHED = "GAME_FINISHED"
    GAME_CANCELED = "GAME_CANCELED"

class RoundStatus(str, Enum):
    """Round status enumeration."""
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    CLOSED = "CLOSED"

class Game:
    """Represents a game instance."""
    def __init__(
        self,
        id: Optional[int] = None,
        chat_id: int = 0,
        status: str = GameStatus.IDLE,
        target_hash: str = "",
        salt: str = "",
        number: Optional[int] = None,
        created_at: Optional[datetime] = None,
        finished_at: Optional[datetime] = None,
        winner_user_id: Optional[int] = None,
        prize_amount: Optional[float] = None,
    ):
        self.id = id
        self.chat_id = chat_id
        self.status = status
        self.target_hash = target_hash
        self.salt = salt
        self.number = number
        self.created_at = created_at or datetime.now()
        self.finished_at = finished_at
        self.winner_user_id = winner_user_id
        self.prize_amount = prize_amount

class Round:
    """Represents a game round."""
    def __init__(
        self,
        id: Optional[int] = None,
        game_id: int = 0,
        index: int = 1,
        status: str = RoundStatus.PENDING,
        message_cost_hint: Optional[int] = None,
        started_at: Optional[datetime] = None,
        ended_at: Optional[datetime] = None,
        total_guesses: int = 0,
    ):
        self.id = id
        self.game_id = game_id
        self.index = index
        self.status = status
        self.message_cost_hint = message_cost_hint
        self.started_at = started_at
        self.ended_at = ended_at
        self.total_guesses = total_guesses

class Guess:
    """Represents a player's guess."""
    def __init__(
        self,
        id: Optional[int] = None,
        game_id: int = 0,
        round_id: int = 0,
        user_id: int = 0,
        value: int = 0,
        is_correct: bool = False,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.game_id = game_id
        self.round_id = round_id
        self.user_id = user_id
        self.value = value
        self.is_correct = is_correct
        self.created_at = created_at or datetime.now()

class Participation:
    """Represents a player's participation in a round."""
    def __init__(
        self,
        id: Optional[int] = None,
        game_id: int = 0,
        round_id: int = 0,
        user_id: int = 0,
        guesses_count: int = 0,
    ):
        self.id = id
        self.game_id = game_id
        self.round_id = round_id
        self.user_id = user_id
        self.guesses_count = guesses_count
