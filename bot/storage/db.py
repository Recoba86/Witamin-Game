"""Database module for SQLite operations."""
import aiosqlite
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
from bot.storage.models import Game, Round, Guess, Participation, GameStatus, RoundStatus

class Database:
    """Database handler for the game bot."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        
    async def init_db(self):
        """Initialize the database schema."""
        async with aiosqlite.connect(self.db_path) as db:
            # Create games table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    target_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    number INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    finished_at TIMESTAMP,
                    winner_user_id INTEGER,
                    prize_amount REAL,
                    sponsor_name TEXT,
                    sponsor_start_message TEXT,
                    sponsor_end_message TEXT
                )
            """)
            
            # Create rounds table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS rounds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id INTEGER NOT NULL,
                    index INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    message_cost_hint INTEGER,
                    started_at TIMESTAMP,
                    ended_at TIMESTAMP,
                    total_guesses INTEGER DEFAULT 0,
                    FOREIGN KEY (game_id) REFERENCES games(id)
                )
            """)
            
            # Create guesses table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS guesses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id INTEGER NOT NULL,
                    round_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    value INTEGER NOT NULL,
                    is_correct BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (game_id) REFERENCES games(id),
                    FOREIGN KEY (round_id) REFERENCES rounds(id)
                )
            """)
            
            # Create participations table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS participations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id INTEGER NOT NULL,
                    round_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    guesses_count INTEGER DEFAULT 0,
                    FOREIGN KEY (game_id) REFERENCES games(id),
                    FOREIGN KEY (round_id) REFERENCES rounds(id),
                    UNIQUE(game_id, round_id, user_id)
                )
            """)
            
            # Create indices for better performance
            await db.execute("CREATE INDEX IF NOT EXISTS idx_games_chat ON games(chat_id)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_rounds_game ON rounds(game_id)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_guesses_round ON guesses(round_id)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_participations_game ON participations(game_id)")
            
            await db.commit()
    
    # Game operations
    async def create_game(self, game: Game) -> int:
        """Create a new game."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """INSERT INTO games (chat_id, status, target_hash, salt, number, created_at, prize_amount, 
                   sponsor_name, sponsor_start_message, sponsor_end_message)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (game.chat_id, game.status, game.target_hash, game.salt, game.number, game.created_at, 
                 game.prize_amount, game.sponsor_name, game.sponsor_start_message, game.sponsor_end_message)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_active_game(self, chat_id: int) -> Optional[Game]:
        """Get the active game for a chat."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT * FROM games 
                   WHERE chat_id = ? AND status NOT IN (?, ?) 
                   ORDER BY created_at DESC LIMIT 1""",
                (chat_id, GameStatus.GAME_FINISHED, GameStatus.GAME_CANCELED)
            )
            row = await cursor.fetchone()
            if row:
                return self._row_to_game(row)
            return None
    
    async def get_game(self, game_id: int) -> Optional[Game]:
        """Get a game by ID."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM games WHERE id = ?", (game_id,))
            row = await cursor.fetchone()
            if row:
                return self._row_to_game(row)
            return None
    
    async def update_game_status(self, game_id: int, status: str):
        """Update game status."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE games SET status = ? WHERE id = ?",
                (status, game_id)
            )
            await db.commit()
    
    async def finish_game(self, game_id: int, winner_user_id: int):
        """Mark game as finished with winner."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """UPDATE games SET status = ?, finished_at = ?, winner_user_id = ? 
                   WHERE id = ?""",
                (GameStatus.GAME_FINISHED, datetime.now(), winner_user_id, game_id)
            )
            await db.commit()
    
    # Round operations
    async def create_round(self, round_obj: Round) -> int:
        """Create a new round."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """INSERT INTO rounds (game_id, index, status, message_cost_hint, started_at, total_guesses)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (round_obj.game_id, round_obj.index, round_obj.status, 
                 round_obj.message_cost_hint, round_obj.started_at, round_obj.total_guesses)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_active_round(self, game_id: int) -> Optional[Round]:
        """Get the active round for a game."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT * FROM rounds 
                   WHERE game_id = ? AND status IN (?, ?) 
                   ORDER BY index DESC LIMIT 1""",
                (game_id, RoundStatus.ACTIVE, RoundStatus.PAUSED)
            )
            row = await cursor.fetchone()
            if row:
                return self._row_to_round(row)
            return None
    
    async def get_round(self, round_id: int) -> Optional[Round]:
        """Get a round by ID."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM rounds WHERE id = ?", (round_id,))
            row = await cursor.fetchone()
            if row:
                return self._row_to_round(row)
            return None
    
    async def get_rounds_for_game(self, game_id: int) -> List[Round]:
        """Get all rounds for a game."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM rounds WHERE game_id = ? ORDER BY index",
                (game_id,)
            )
            rows = await cursor.fetchall()
            return [self._row_to_round(row) for row in rows]
    
    async def update_round_status(self, round_id: int, status: str):
        """Update round status."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE rounds SET status = ? WHERE id = ?",
                (status, round_id)
            )
            await db.commit()
    
    async def close_round(self, round_id: int):
        """Close a round."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE rounds SET status = ?, ended_at = ? WHERE id = ?",
                (RoundStatus.CLOSED, datetime.now(), round_id)
            )
            await db.commit()
    
    async def increment_round_guesses(self, round_id: int):
        """Increment total guesses for a round."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE rounds SET total_guesses = total_guesses + 1 WHERE id = ?",
                (round_id,)
            )
            await db.commit()
    
    # Guess operations
    async def create_guess(self, guess: Guess) -> int:
        """Create a new guess."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """INSERT INTO guesses (game_id, round_id, user_id, value, is_correct, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (guess.game_id, guess.round_id, guess.user_id, guess.value, 
                 guess.is_correct, guess.created_at)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_user_guesses_in_round(self, round_id: int, user_id: int) -> List[Guess]:
        """Get all guesses by a user in a round."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT * FROM guesses 
                   WHERE round_id = ? AND user_id = ? 
                   ORDER BY created_at""",
                (round_id, user_id)
            )
            rows = await cursor.fetchall()
            return [self._row_to_guess(row) for row in rows]
    
    async def get_last_guess(self, round_id: int) -> Optional[Guess]:
        """Get the last guess in a round."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT * FROM guesses 
                   WHERE round_id = ? 
                   ORDER BY created_at DESC LIMIT 1""",
                (round_id,)
            )
            row = await cursor.fetchone()
            if row:
                return self._row_to_guess(row)
            return None
    
    # Participation operations
    async def increment_participation(self, game_id: int, round_id: int, user_id: int):
        """Increment or create participation record."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO participations (game_id, round_id, user_id, guesses_count)
                   VALUES (?, ?, ?, 1)
                   ON CONFLICT(game_id, round_id, user_id) 
                   DO UPDATE SET guesses_count = guesses_count + 1""",
                (game_id, round_id, user_id)
            )
            await db.commit()
    
    async def get_user_participated_rounds(self, game_id: int, user_id: int) -> List[int]:
        """Get list of round indices where user participated."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """SELECT DISTINCT r.index 
                   FROM participations p
                   JOIN rounds r ON p.round_id = r.id
                   WHERE p.game_id = ? AND p.user_id = ?
                   ORDER BY r.index""",
                (game_id, user_id)
            )
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
    
    # Helper methods to convert rows to objects
    def _row_to_game(self, row) -> Game:
        """Convert database row to Game object."""
        return Game(
            id=row['id'],
            chat_id=row['chat_id'],
            status=row['status'],
            target_hash=row['target_hash'],
            salt=row['salt'],
            number=row['number'],
            created_at=row['created_at'],
            finished_at=row['finished_at'],
            winner_user_id=row['winner_user_id'],
            prize_amount=row['prize_amount'],
            sponsor_name=row['sponsor_name'],
            sponsor_start_message=row['sponsor_start_message'],
            sponsor_end_message=row['sponsor_end_message']
        )
    
    def _row_to_round(self, row) -> Round:
        """Convert database row to Round object."""
        return Round(
            id=row['id'],
            game_id=row['game_id'],
            index=row['index'],
            status=row['status'],
            message_cost_hint=row['message_cost_hint'],
            started_at=row['started_at'],
            ended_at=row['ended_at'],
            total_guesses=row['total_guesses']
        )
    
    def _row_to_guess(self, row) -> Guess:
        """Convert database row to Guess object."""
        return Guess(
            id=row['id'],
            game_id=row['game_id'],
            round_id=row['round_id'],
            user_id=row['user_id'],
            value=row['value'],
            is_correct=row['is_correct'],
            created_at=row['created_at']
        )
