"""Game engine - core business logic for the guessing game."""
import random
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict
from bot.storage.db import Database
from bot.storage.models import Game, Round, Guess, GameStatus, RoundStatus
from bot.services.commit_reveal import make_commit, verify
from bot.config import MIN_NUMBER, MAX_NUMBER, get_round_cost, ROUND_DURATION_MINUTES, MIN_GUESSES_BEFORE_CLOSE

logger = logging.getLogger(__name__)

class GameEngine:
    """Main game engine handling all game logic."""
    
    def __init__(self, db: Database, bot=None):
        self.db = db
        self.bot = bot  # Store bot instance for sending messages
        self.round_timers = {}  # Store active round timers {round_id: task}
    
    async def create_game(
        self, 
        chat_id: int, 
        prize_amount: Optional[float] = None,
        sponsor_name: Optional[str] = None,
        sponsor_start_message: Optional[str] = None,
        sponsor_end_message: Optional[str] = None
    ) -> Tuple[Game, str]:
        """
        Create a new game with commit-reveal.
        
        Args:
            chat_id: The Telegram chat ID
            prize_amount: Optional prize amount for the winner
            sponsor_name: Optional sponsor name
            sponsor_start_message: Optional message to show at round start
            sponsor_end_message: Optional message to show at round end
            
        Returns:
            Tuple of (Game object, hash message for posting)
        """
        # Generate random number and commitment
        secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
        number, salt, target_hash = make_commit(secret_number)
        
        # Create game in database
        game = Game(
            chat_id=chat_id,
            status=GameStatus.GAME_COMMITTED,
            target_hash=target_hash,
            salt=salt,
            number=number,
            created_at=datetime.now(),
            prize_amount=prize_amount,
            sponsor_name=sponsor_name,
            sponsor_start_message=sponsor_start_message,
            sponsor_end_message=sponsor_end_message
        )
        
        game.id = await self.db.create_game(game)
        
        return game, target_hash
    
    async def start_round(self, game_id: int, round_index: int) -> Round:
        """
        Start a new round for the game.
        
        Args:
            game_id: The game ID
            round_index: The round number (1-based)
            
        Returns:
            The created Round object
        """
        # Get suggested cost for this round
        cost = get_round_cost(round_index)
        
        # Create round
        round_obj = Round(
            game_id=game_id,
            round_index=round_index,
            status=RoundStatus.ACTIVE,
            message_cost_hint=cost,
            started_at=datetime.now(),
            total_guesses=0
        )
        
        round_obj.id = await self.db.create_round(round_obj)
        
        # Update game status
        await self.db.update_game_status(game_id, GameStatus.ROUND_ACTIVE)
        
        # Start the round timer
        await self._start_round_timer(round_obj.id, game_id)
        
        return round_obj
    
    async def _start_round_timer(self, round_id: int, game_id: int):
        """
        Start a timer for a round that will auto-close after duration.
        Only closes if minimum guesses (10) have been reached.
        """
        async def timer_task():
            try:
                logger.info(f"Round timer started for round {round_id}, will check after {ROUND_DURATION_MINUTES} minutes")
                # Wait for the configured duration
                await asyncio.sleep(ROUND_DURATION_MINUTES * 60)
                
                logger.info(f"Round timer expired for round {round_id}, checking status...")
                # Check if round is still active
                round_obj = await self.db.get_round(round_id)
                if not round_obj or round_obj.status != RoundStatus.ACTIVE:
                    logger.info(f"Round {round_id} is no longer active, skipping auto-close")
                    return
                
                logger.info(f"Round {round_id} has {round_obj.total_guesses} guesses (min: {MIN_GUESSES_BEFORE_CLOSE})")
                # Only close if we have at least MIN_GUESSES_BEFORE_CLOSE guesses
                if round_obj.total_guesses >= MIN_GUESSES_BEFORE_CLOSE:
                    logger.info(f"Auto-closing round {round_id}...")
                    await self._auto_close_round(round_id, game_id)
                else:
                    logger.info(f"Waiting for minimum guesses for round {round_id}...")
                    # Wait until we reach minimum guesses - check every 30 seconds
                    while True:
                        await asyncio.sleep(30)
                        round_obj = await self.db.get_round(round_id)
                        if not round_obj or round_obj.status != RoundStatus.ACTIVE:
                            logger.info(f"Round {round_id} is no longer active during wait")
                            break
                        logger.info(f"Round {round_id} now has {round_obj.total_guesses} guesses")
                        if round_obj.total_guesses >= MIN_GUESSES_BEFORE_CLOSE:
                            logger.info(f"Minimum guesses reached, auto-closing round {round_id}...")
                            await self._auto_close_round(round_id, game_id)
                            break
            except asyncio.CancelledError:
                # Timer was cancelled (round manually closed/paused)
                logger.info(f"Round timer for round {round_id} was cancelled")
                pass
            except Exception as e:
                logger.error(f"Error in round timer for round {round_id}: {e}", exc_info=True)
            finally:
                # Clean up timer reference
                if round_id in self.round_timers:
                    del self.round_timers[round_id]
        
        # Create and store the timer task
        task = asyncio.create_task(timer_task())
        self.round_timers[round_id] = task
    
    async def _auto_close_round(self, round_id: int, game_id: int):
        """Auto-close a round and send announcement to chat."""
        from bot.services.announcer import Announcer
        from bot.keyboards.admin import AdminKeyboards
        
        logger.info(f"_auto_close_round called for round {round_id}, game {game_id}")
        
        # Get round and game info
        round_obj = await self.db.get_round(round_id)
        game = await self.db.get_game(game_id)
        
        if not round_obj or not game:
            logger.warning(f"Could not find round {round_id} or game {game_id}")
            return
        
        logger.info(f"Closing round {round_id} for game {game_id} in chat {game.chat_id}")
        
        # Close the round (but don't cancel timer - we're IN the timer)
        await self.db.close_round(round_id)
        await self.db.update_game_status(game_id, GameStatus.GAME_COMMITTED)
        
        # Send announcement if bot is available
        if self.bot:
            try:
                # Calculate next round number
                all_rounds = await self.db.get_rounds_for_game(game_id)
                next_round = len(all_rounds) + 1
                
                logger.info(f"Sending auto-close announcement to chat {game.chat_id}, next round: {next_round}")
                
                # Send announcement with sponsor end message if available
                announcement = Announcer.round_closed(round_obj.round_index, game.sponsor_end_message)
                keyboard = AdminKeyboards.between_rounds_controls(next_round)
                
                await self.bot.send_message(
                    chat_id=game.chat_id,
                    text=announcement,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
                logger.info(f"Auto-close announcement sent successfully to chat {game.chat_id}")
            except Exception as e:
                logger.error(f"Failed to send auto-close announcement: {e}", exc_info=True)
        else:
            logger.warning("Bot instance not available, cannot send auto-close announcement")
    
    async def pause_round(self, round_id: int):
        """Pause the current round."""
        round_obj = await self.db.get_round(round_id)
        if round_obj:
            await self.db.update_round_status(round_id, RoundStatus.PAUSED)
            await self.db.update_game_status(round_obj.game_id, GameStatus.ROUND_PAUSED)
            # Cancel the timer
            if round_id in self.round_timers:
                self.round_timers[round_id].cancel()
                del self.round_timers[round_id]
    
    async def resume_round(self, round_id: int):
        """Resume a paused round."""
        round_obj = await self.db.get_round(round_id)
        if round_obj:
            await self.db.update_round_status(round_id, RoundStatus.ACTIVE)
            await self.db.update_game_status(round_obj.game_id, GameStatus.ROUND_ACTIVE)
            # Restart the timer with remaining time
            await self._start_round_timer(round_id, round_obj.game_id)
    
    async def close_round(self, round_id: int):
        """Close the current round."""
        round_obj = await self.db.get_round(round_id)
        if round_obj:
            await self.db.close_round(round_id)
            await self.db.update_game_status(round_obj.game_id, GameStatus.GAME_COMMITTED)
            # Cancel the timer if it exists
            if round_id in self.round_timers:
                self.round_timers[round_id].cancel()
                del self.round_timers[round_id]
    
    async def register_guess(
        self, 
        game_id: int, 
        round_id: int, 
        user_id: int, 
        guess_value: int
    ) -> Tuple[bool, Optional[Guess]]:
        """
        Register a player's guess.
        
        Args:
            game_id: The game ID
            round_id: The round ID
            user_id: The user's Telegram ID
            guess_value: The guessed number
            
        Returns:
            Tuple of (is_correct, Guess object)
        """
        # Get the game to check the secret number
        game = await self.db.get_game(game_id)
        if not game:
            return False, None
        
        # Check if guess is correct
        is_correct = (guess_value == game.number)
        
        # Create guess record
        guess = Guess(
            game_id=game_id,
            round_id=round_id,
            user_id=user_id,
            value=guess_value,
            is_correct=is_correct,
            created_at=datetime.now()
        )
        
        guess.id = await self.db.create_guess(guess)
        
        # Update participation
        await self.db.increment_participation(game_id, round_id, user_id)
        
        # Increment round guess count
        await self.db.increment_round_guesses(round_id)
        
        return is_correct, guess
    
    async def finish_game(self, game_id: int, winner_user_id: int):
        """
        Finish the game with a winner.
        
        Args:
            game_id: The game ID
            winner_user_id: The winning user's Telegram ID
        """
        await self.db.finish_game(game_id, winner_user_id)
        
        # Cancel any active round timers
        active_round = await self.db.get_active_round(game_id)
        if active_round and active_round.id in self.round_timers:
            self.round_timers[active_round.id].cancel()
            del self.round_timers[active_round.id]
    
    async def cancel_game(self, game_id: int):
        """Cancel the current game."""
        await self.db.update_game_status(game_id, GameStatus.GAME_CANCELED)
        
        # Cancel any active round timers
        active_round = await self.db.get_active_round(game_id)
        if active_round and active_round.id in self.round_timers:
            self.round_timers[active_round.id].cancel()
            del self.round_timers[active_round.id]
    
    async def compute_loyalty_for_winner(self, game_id: int, winner_user_id: int) -> int:
        """
        Compute loyalty percentage for the winner.
        
        Formula: P = max(50, 100 - (25 * missed_round1) - (15 * other_missed_rounds))
        
        Args:
            game_id: The game ID
            winner_user_id: The winner's Telegram ID
            
        Returns:
            Loyalty percentage (50-100)
        """
        # Get all rounds for the game
        all_rounds = await self.db.get_rounds_for_game(game_id)
        
        # Get rounds where winner participated
        participated_rounds = await self.db.get_user_participated_rounds(game_id, winner_user_id)
        
        if not all_rounds:
            return 100
        
        # Calculate missed rounds
        all_round_indices = {r.round_index for r in all_rounds}
        participated_set = set(participated_rounds)
        missed_rounds = all_round_indices - participated_set
        
        # Check if missed round 1
        missed_round1 = 1 if 1 in missed_rounds else 0
        
        # Count other missed rounds
        other_missed = len([r for r in missed_rounds if r != 1])
        
        # Calculate loyalty percentage
        loyalty = 100 - (25 * missed_round1) - (15 * other_missed)
        
        # Ensure minimum is 50%
        return max(50, loyalty)
    
    async def get_status(self, chat_id: int) -> Optional[Dict]:
        """
        Get current game status for a chat.
        
        Args:
            chat_id: The Telegram chat ID
            
        Returns:
            Dictionary with game status information or None
        """
        game = await self.db.get_active_game(chat_id)
        if not game:
            return None
        
        active_round = await self.db.get_active_round(game.id)
        
        status = {
            'game': game,
            'active_round': active_round,
            'all_rounds': await self.db.get_rounds_for_game(game.id)
        }
        
        if active_round:
            status['last_guess'] = await self.db.get_last_guess(active_round.id)
        
        return status
    
    async def verify_game(self, game_id: int) -> bool:
        """
        Verify the game's commitment (for revealing).
        
        Args:
            game_id: The game ID
            
        Returns:
            True if verification passes, False otherwise
        """
        game = await self.db.get_game(game_id)
        if not game or game.number is None:
            return False
        
        return verify(game.number, game.salt, game.target_hash)
