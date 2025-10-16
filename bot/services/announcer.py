"""Announcer service for formatting game messages."""
from typing import Optional
from bot.storage.models import Game, Round, Guess
from bot.services.commit_reveal import verify
from bot.translations import Translations
from bot.config import LANGUAGE

class Announcer:
    """Formats messages for game announcements."""
    
    @staticmethod
    def game_created(target_hash: str, prize_amount: Optional[float] = None, sponsor_name: Optional[str] = None) -> str:
        """Format message for new game creation."""
        t = Translations.get
        lang = LANGUAGE
        
        prize_text = f"\n{t('prize', lang, amount=prize_amount)}\n" if prize_amount else "\n"
        sponsor_text = f"{t('sponsored_by', lang, sponsor=sponsor_name)}\n" if sponsor_name else ""
        
        return (
            f"{t('game_created_title', lang)}\n\n"
            f"{t('provably_fair', lang)}\n"
            f"<code>{target_hash}</code>\n"
            f"{prize_text}"
            f"{sponsor_text}"
            f"{t('rules_title', lang)}\n"
            f"{t('rule_range', lang)}\n"
            f"{t('rule_guesses', lang)}\n"
            f"{t('rule_duration', lang)}\n"
            f"{t('rule_hints', lang)}\n"
            f"{t('rule_winner', lang)}\n"
            f"{t('rule_loyalty', lang)}\n\n"
            f"{t('start_button_prompt', lang)}"
        )
    
    @staticmethod
    def round_started(round_index: int, cost: int, duration_minutes: int = 2, sponsor_message: Optional[str] = None) -> str:
        """Format message for round start."""
        t = Translations.get
        lang = LANGUAGE
        
        # Only round 1 requires minimum guesses
        if round_index == 1:
            duration_text = f"{t('duration_with_min', lang, minutes=duration_minutes)}\n"
        else:
            duration_text = f"{t('duration', lang, minutes=duration_minutes)}\n"
        
        base_message = (
            f"{t('round_started', lang, round=round_index)}\n\n"
            f"{t('suggested_cost', lang, cost=cost)}\n"
            f"{duration_text}"
            f"{t('range', lang)}\n"
            f"{t('guess_limit', lang)}\n\n"
            f"{t('good_luck', lang)}"
        )
        
        # Add sponsor message if provided
        if sponsor_message:
            base_message += f"\n\n{t('sponsor_message', lang, message=sponsor_message)}"
        
        return base_message
    
    @staticmethod
    def round_paused() -> str:
        """Format message for round pause."""
        return Translations.get('round_paused', LANGUAGE)
    
    @staticmethod
    def round_resumed(round_index: int) -> str:
        """Format message for round resume."""
        return Translations.get('round_resumed', LANGUAGE, round=round_index)
    
    @staticmethod
    def round_closed(round_index: int, sponsor_message: Optional[str] = None) -> str:
        """Format message for round close."""
        t = Translations.get
        lang = LANGUAGE
        
        base_message = t('round_closed', lang, round=round_index)
        
        # Add sponsor closing message if provided
        if sponsor_message:
            base_message += f"\n\n{t('sponsor_message', lang, message=sponsor_message)}"
        
        return base_message
    
    @staticmethod
    def hint_message(last_guess: int, target_number: int) -> str:
        """Format hint message based on last guess."""
        t = Translations.get
        lang = LANGUAGE
        
        if last_guess < target_number:
            hint_text = t('hint_higher', lang, guess=last_guess)
        else:
            hint_text = t('hint_lower', lang, guess=last_guess)
        
        return f"{t('hint_title', lang)}\n\n{hint_text}"
    
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
        t = Translations.get
        lang = LANGUAGE
        
        # Format user mention
        user_mention = f"@{username}" if username else f"User {user_id}"
        
        # Verify hash
        verification = verify(number, salt, target_hash)
        verify_emoji = "✅" if verification else "❌"
        verify_status = t('verification_valid', lang) if verification else t('verification_invalid', lang)
        
        # Calculate actual prize won based on loyalty penalty
        prize_text = ""
        if prize_amount:
            actual_prize = (prize_amount * loyalty_percent) / 100
            prize_text = f"{t('prize_won', lang, amount=f'{actual_prize:.0f}')}\n"
            # Show penalty info if loyalty is less than 100%
            if loyalty_percent < 100:
                penalty = 100 - loyalty_percent
                prize_text += f"{t('loyalty_penalty', lang, penalty=penalty)}\n"
        
        return (
            f"{t('winner_title', lang)}\n\n"
            f"{t('winner', lang, user=user_mention)}\n"
            f"{t('secret_number', lang, number=number)}\n"
            f"{t('won_in_round', lang, round=round_index)}\n"
            f"{prize_text}"
            f"{t('proof_title', lang)}\n"
            f"{t('proof_number', lang, number=number)}\n"
            f"{t('proof_salt', lang, salt=salt)}\n"
            f"{t('proof_hash', lang, hash=target_hash)}\n\n"
            f"{t('verification', lang, emoji=verify_emoji, status=verify_status)}\n\n"
            f"{t('thank_you', lang)}"
        )
    
    @staticmethod
    def game_canceled() -> str:
        """Format message for game cancellation."""
        return Translations.get('game_canceled', LANGUAGE)
    
    @staticmethod
    def guess_limit_reached() -> str:
        """Format message when player reaches guess limit."""
        return Translations.get('guess_limit_reached', LANGUAGE)
    
    @staticmethod
    def invalid_guess() -> str:
        """Format message for invalid guess."""
        return Translations.get('invalid_guess', LANGUAGE)
    
    @staticmethod
    def no_active_game() -> str:
        """Format message when no game is active."""
        return Translations.get('no_active_game', LANGUAGE)
    
    @staticmethod
    def not_accepting_guesses() -> str:
        """Format message when round is not accepting guesses."""
        return Translations.get('not_accepting_guesses', LANGUAGE)
    
    @staticmethod
    def status_message(
        game: Game,
        active_round: Optional[Round],
        total_rounds: int,
        last_guess_value: Optional[int]
    ) -> str:
        """Format status message."""
        t = Translations.get
        lang = LANGUAGE
        
        status_text = f"{t('status_title', lang)}\n\n"
        status_text += f"{t('game_state', lang, state=game.status)}\n"
        status_text += f"{t('total_rounds', lang, rounds=total_rounds)}\n\n"
        
        if active_round:
            status_text += f"{t('active_round', lang, round=active_round.round_index)}\n"
            status_text += f"{t('total_guesses', lang, guesses=active_round.total_guesses)}\n"
            status_text += f"{t('suggested_cost', lang, cost=active_round.message_cost_hint)}\n"
            
            if last_guess_value is not None:
                status_text += f"{t('last_guess', lang, guess=last_guess_value)}\n"
            
            # Calculate guesses until next hint
            guesses_to_hint = 10 - (active_round.total_guesses % 10)
            if guesses_to_hint < 10:
                status_text += f"{t('next_hint', lang, guesses=guesses_to_hint)}\n"
        
        return status_text
    
    @staticmethod
    def help_message() -> str:
        """Format help/start message."""
        t = Translations.get
        lang = LANGUAGE
        
        return (
            f"{t('help_title', lang)}\n\n"
            f"{t('how_to_play', lang)}\n"
            f"{t('help_step1', lang)}\n"
            f"{t('help_step2', lang)}\n"
            f"{t('help_step3', lang)}\n"
            f"{t('help_step4', lang)}\n"
            f"{t('help_step5', lang)}\n"
            f"{t('help_step6', lang)}\n\n"
            f"{t('loyalty_title', lang)}\n"
            f"{t('loyalty_rule1', lang)}\n"
            f"{t('loyalty_rule2', lang)}\n"
            f"{t('loyalty_rule3', lang)}\n"
            f"{t('loyalty_rule4', lang)}\n\n"
            f"{t('commands_title', lang)}\n"
            f"{t('cmd_start', lang)}\n"
            f"{t('cmd_status', lang)}\n"
            f"{t('cmd_newgame', lang)}\n"
            f"{t('cmd_start_round', lang)}\n"
            f"{t('cmd_pause_round', lang)}\n"
            f"{t('cmd_resume_round', lang)}\n"
            f"{t('cmd_close_round', lang)}\n"
            f"{t('cmd_reveal', lang)}\n"
            f"{t('cmd_cancel_game', lang)}\n"
            f"{t('cmd_post_cost', lang)}\n\n"
            f"{t('help_footer', lang)}"
        )
    
    @staticmethod
    def manual_reveal(number: int, salt: str, target_hash: str) -> str:
        """Format manual reveal message (no winner)."""
        t = Translations.get
        lang = LANGUAGE
        
        verification = verify(number, salt, target_hash)
        verify_emoji = "✅" if verification else "❌"
        verify_status = t('verification_valid', lang) if verification else t('verification_invalid', lang)
        
        return (
            f"{t('reveal_title', lang)}\n\n"
            f"{t('secret_was', lang, number=number)}\n\n"
            f"{t('proof_title', lang)}\n"
            f"{t('proof_number', lang, number=number)}\n"
            f"{t('proof_salt', lang, salt=salt)}\n"
            f"{t('proof_hash', lang, hash=target_hash)}\n\n"
            f"{t('verification', lang, emoji=verify_emoji, status=verify_status)}\n\n"
            f"{t('no_winner', lang)}"
        )
    
    @staticmethod
    def cost_hint(round_index: int, cost: int) -> str:
        """Format cost hint message."""
        t = Translations.get
        lang = LANGUAGE
        
        return (
            f"{t('cost_hint_title', lang, round=round_index)}\n\n"
            f"{t('cost_suggested', lang, cost=cost)}\n\n"
            f"{t('cost_warning', lang)}"
        )
