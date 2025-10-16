"""Announcer service for formatting game messages."""
from typing import Optional
from bot.storage.models import Game, Round, Guess
from bot.services.commit_reveal import verify

class Announcer:
    """Formats messages for game announcements."""
    
    @staticmethod
    def game_created(target_hash: str, prize_amount: Optional[float] = None, sponsor_name: Optional[str] = None) -> str:
        """Format message for new game creation."""
        prize_text = f"\n💰 <b>Prize:</b> {prize_amount} ⭐\n" if prize_amount else "\n"
        sponsor_text = f"🎗 <b>Sponsored by:</b> {sponsor_name}\n" if sponsor_name else ""
        
        return (
            "🎮 <b>New Game Started!</b>\n\n"
            "🔒 <b>Provably Fair Commitment</b>\n"
            f"<code>{target_hash}</code>\n"
            f"{prize_text}"
            f"{sponsor_text}"
            "📋 <b>Rules:</b>\n"
            "• Secret number is between 1 and 10,000\n"
            "• Each player can guess up to 10 times per round\n"
            "• Each round lasts 2 minutes (or until 10 guesses minimum)\n"
            "• Bot reacts 👍 if number is higher, 👎 if lower\n"
            "• First correct guess wins!\n"
            "• Stay in the game longer for bigger rewards! 🎁\n\n"
            "👆 Admin: Press <b>Start Round 1</b> to begin!"
        )
    
    @staticmethod
    def round_started(round_index: int, cost: int, duration_minutes: int = 2, sponsor_message: Optional[str] = None) -> str:
        """Format message for round start."""
        # Only round 1 requires minimum guesses
        duration_text = f"⏱ Duration: <b>{duration_minutes} minutes</b>"
        if round_index == 1:
            duration_text += " (min 10 guesses)"
        duration_text += "\n"
        
        base_message = (
            f"🔥 <b>Round {round_index} Started!</b>\n\n"
            f"💰 Suggested cost: <b>{cost} ⭐ Star(s)</b>\n"
            f"{duration_text}"
            f"🎯 Range: 1 - 10,000\n"
            f"📊 Limit: 10 guesses per player\n\n"
            "Good luck! 🍀"
        )
        
        # Add sponsor message if provided
        if sponsor_message:
            base_message += f"\n\n📢 <b>Sponsor Message:</b>\n{sponsor_message}"
        
        return base_message
    
    @staticmethod
    def round_paused() -> str:
        """Format message for round pause."""
        return "⏸ <b>Round Paused</b>\n\nWaiting for admin to resume..."
    
    @staticmethod
    def round_resumed(round_index: int) -> str:
        """Format message for round resume."""
        return f"▶️ <b>Round {round_index} Resumed!</b>\n\nContinue guessing!"
    
    @staticmethod
    def round_closed(round_index: int, sponsor_message: Optional[str] = None) -> str:
        """Format message for round close."""
        base_message = (
            f"🔒 <b>Round {round_index} Closed</b>\n\n"
            "No winner yet. Admin can start the next round."
        )
        
        # Add sponsor closing message if provided
        if sponsor_message:
            base_message += f"\n\n📢 <b>Sponsor Message:</b>\n{sponsor_message}"
        
        return base_message
    
    @staticmethod
    def hint_message(last_guess: int, target_number: int) -> str:
        """Format hint message based on last guess."""
        if last_guess < target_number:
            direction = "higher ⬆️"
        else:
            direction = "lower ⬇️"
        
        return (
            f"💡 <b>Hint!</b>\n\n"
            f"The secret number is <b>{direction}</b> than {last_guess}"
        )
    
    @staticmethod
    def winner_announcement(
        user_id: int,
        username: Optional[str],
        number: int,
        salt: str,
        target_hash: str,
        loyalty_percent: int,
        round_index: int,
        prize_amount: Optional[float] = None
    ) -> str:
        """Format winner announcement with reveal."""
        # Format user mention
        user_mention = f"@{username}" if username else f"User {user_id}"
        
        # Verify hash
        verification = verify(number, salt, target_hash)
        verify_emoji = "✅" if verification else "❌"
        
        # Calculate actual prize won based on loyalty penalty
        prize_text = ""
        if prize_amount:
            actual_prize = (prize_amount * loyalty_percent) / 100
            prize_text = f"💰 Prize Won: <b>{actual_prize:.0f} ⭐</b>\n"
            # Show penalty info if loyalty is less than 100%
            if loyalty_percent < 100:
                penalty = 100 - loyalty_percent
                prize_text += f"⚠️ Loyalty Penalty: <b>{penalty}% (missed rounds)</b>\n"
        
        return (
            f"🎉 <b>WE HAVE A WINNER!</b> 🎉\n\n"
            f"🏆 Winner: {user_mention}\n"
            f"🎯 Secret Number: <b>{number}</b>\n"
            f"📍 Won in Round: <b>{round_index}</b>\n"
            f"{prize_text}"
            f"🔓 <b>Proof (Commit-Reveal):</b>\n"
            f"Number: <code>{number}</code>\n"
            f"Salt: <code>{salt}</code>\n"
            f"Hash: <code>{target_hash}</code>\n\n"
            f"Verification: {verify_emoji} <b>{'VALID' if verification else 'INVALID'}</b>\n\n"
            f"Thank you for playing! 🎮"
        )
    
    @staticmethod
    def game_canceled() -> str:
        """Format message for game cancellation."""
        return "❌ <b>Game Canceled</b>\n\nA new game can be started with /newgame"
    
    @staticmethod
    def guess_limit_reached() -> str:
        """Format message when player reaches guess limit."""
        return "⚠️ You've reached the maximum of 10 guesses for this round."
    
    @staticmethod
    def invalid_guess() -> str:
        """Format message for invalid guess."""
        return "❌ Invalid guess. Please send a number between 1 and 10,000."
    
    @staticmethod
    def no_active_game() -> str:
        """Format message when no game is active."""
        return "⚠️ No active game. Admin can start one with /newgame"
    
    @staticmethod
    def not_accepting_guesses() -> str:
        """Format message when round is not accepting guesses."""
        return "⏸ Round is not currently accepting guesses. Please wait for admin."
    
    @staticmethod
    def status_message(
        game: Game,
        active_round: Optional[Round],
        total_rounds: int,
        last_guess_value: Optional[int]
    ) -> str:
        """Format status message."""
        status_text = f"📊 <b>Game Status</b>\n\n"
        status_text += f"🎮 Game State: <b>{game.status}</b>\n"
        status_text += f"📈 Total Rounds: <b>{total_rounds}</b>\n\n"
        
        if active_round:
            status_text += f"🔥 <b>Active Round {active_round.round_index}</b>\n"
            status_text += f"📊 Total Guesses: <b>{active_round.total_guesses}</b>\n"
            status_text += f"💰 Suggested Cost: <b>{active_round.message_cost_hint} ⭐</b>\n"
            
            if last_guess_value is not None:
                status_text += f"🎯 Last Guess: <b>{last_guess_value}</b>\n"
            
            # Calculate guesses until next hint
            guesses_to_hint = 10 - (active_round.total_guesses % 10)
            if guesses_to_hint < 10:
                status_text += f"💡 Next Hint: <b>{guesses_to_hint} guesses away</b>\n"
        
        return status_text
    
    @staticmethod
    def help_message() -> str:
        """Format help/start message."""
        return (
            "🎯 <b>Incremental Guess Game</b>\n\n"
            "<b>How to Play:</b>\n"
            "1. A secret number between 1-10,000 is chosen\n"
            "2. Send your guess as a number in the chat\n"
            "3. You can guess up to 10 times per round\n"
            "4. Bot reacts 👍 (higher) or 👎 (lower) to each guess\n"
            "5. Rounds last 2 minutes (minimum 10 guesses total)\n"
            "6. First to guess correctly wins the prize!\n\n"
            "<b>Loyalty Rewards:</b>\n"
            "• Join from Round 1: 100% reward\n"
            "• Miss Round 1: 75% reward\n"
            "• Miss other rounds: -15% per round\n"
            "• Minimum: 50% reward\n\n"
            "<b>Commands:</b>\n"
            "/start - Show this help\n"
            "/status - View current game status\n"
            "/newgame [prize] - (Admin) Start new game\n\n"
            "🎮 <i>Guess the hidden number! One winner, fair hash, "
            "and bigger rewards the longer you stay in the game!</i>"
        )
    
    @staticmethod
    def manual_reveal(number: int, salt: str, target_hash: str) -> str:
        """Format manual reveal message (no winner)."""
        verification = verify(number, salt, target_hash)
        verify_emoji = "✅" if verification else "❌"
        
        return (
            "🔓 <b>Game Revealed</b>\n\n"
            f"🎯 Secret Number was: <b>{number}</b>\n\n"
            f"<b>Proof (Commit-Reveal):</b>\n"
            f"Number: <code>{number}</code>\n"
            f"Salt: <code>{salt}</code>\n"
            f"Hash: <code>{target_hash}</code>\n\n"
            f"Verification: {verify_emoji} <b>{'VALID' if verification else 'INVALID'}</b>\n\n"
            "No winner this time. Better luck next game! 🎮"
        )
    
    @staticmethod
    def cost_hint(round_index: int, cost: int) -> str:
        """Format cost hint message."""
        return (
            f"💰 <b>Round {round_index} Cost</b>\n\n"
            f"Suggested: <b>{cost} ⭐ Star(s)</b>\n\n"
            "⚠️ Admin should manually set this in Telegram's "
            "\"Starred Group Settings\" before starting the round."
        )
