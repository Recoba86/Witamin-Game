"""Player message handlers for guesses."""
import logging
from aiogram import Router, F
from aiogram.types import Message, ReactionTypeEmoji
from bot.services.game_engine import GameEngine
from bot.services.parsing import extract_guess
from bot.services.validators import (
    validate_guess_range,
    validate_guess_limit,
    validate_round_status_for_guess
)
from bot.services.announcer import Announcer
from bot.storage.models import GameStatus, RoundStatus

logger = logging.getLogger(__name__)

router = Router()

@router.message(F.text, F.chat.type.in_({"group", "supergroup"}))
async def handle_guess(message: Message, game_engine: GameEngine):
    """Handle player guesses in group chats."""
    # Extract guess from message
    guess_value = extract_guess(message.text)
    
    if guess_value is None:
        # Not a guess, ignore
        return
    
    # Validate guess range
    if not validate_guess_range(guess_value):
        await message.reply(Announcer.invalid_guess())
        return
    
    # Get active game
    game = await game_engine.db.get_active_game(message.chat.id)
    if not game:
        # No active game, silently ignore
        return
    
    # Check game status
    if game.status != GameStatus.ROUND_ACTIVE:
        await message.reply(Announcer.not_accepting_guesses())
        return
    
    # Get active round
    active_round = await game_engine.db.get_active_round(game.id)
    if not active_round:
        # No active round, silently ignore
        return
    
    # Check round status
    if not validate_round_status_for_guess(active_round.status):
        await message.reply(Announcer.not_accepting_guesses())
        return
    
    # Check guess limit for this player
    user_guesses = await game_engine.db.get_user_guesses_in_round(
        active_round.id,
        message.from_user.id
    )
    
    if not validate_guess_limit(len(user_guesses)):
        await message.reply(Announcer.guess_limit_reached())
        return
    
    # Register the guess
    is_correct, guess = await game_engine.register_guess(
        game.id,
        active_round.id,
        message.from_user.id,
        guess_value
    )
    
    logger.info(
        f"Guess registered: user={message.from_user.id}, "
        f"value={guess_value}, correct={is_correct}"
    )
    
    # Check if guess is correct (WINNER!)
    if is_correct:
        await handle_winner(message, game_engine, game, active_round)
        return
    
    # Add reaction hint: 👍 if number is higher, 👎 if lower
    try:
        if guess_value < game.number:
            # Number is higher, react with thumbs up
            await message.set_reaction([ReactionTypeEmoji(emoji="👍")])
        else:
            # Number is lower, react with thumbs down
            await message.set_reaction([ReactionTypeEmoji(emoji="👎")])
    except Exception as e:
        logger.warning(f"Could not set reaction: {e}")
        # Fallback: send text hint if reactions fail
        await send_text_hint(message, guess_value, game.number)

async def handle_winner(message: Message, engine: GameEngine, game, active_round):
    """Handle a winning guess."""
    winner_id = message.from_user.id
    winner_username = message.from_user.username
    
    # Calculate loyalty percentage
    loyalty = await engine.compute_loyalty_for_winner(game.id, winner_id)
    
    # Mark game as finished
    await engine.finish_game(game.id, winner_id)
    
    # Send winner announcement
    announcement = Announcer.winner_announcement(
        user_id=winner_id,
        username=winner_username,
        number=game.number,
        salt=game.salt,
        target_hash=game.target_hash,
        loyalty_percent=loyalty,
        round_index=active_round.round_index,
        prize_amount=game.prize_amount
    )
    
    await message.reply(announcement, parse_mode="HTML")
    
    logger.info(
        f"Game {game.id} won by user {winner_id} "
        f"in round {active_round.round_index}, loyalty={loyalty}%, prize={game.prize_amount}"
    )

async def send_text_hint(message: Message, guess_value: int, target_number: int):
    """Send a text hint as fallback if reactions don't work."""
    if guess_value < target_number:
        hint = "👍 The number is <b>higher</b>"
    else:
        hint = "👎 The number is <b>lower</b>"
    
    await message.reply(hint, parse_mode="HTML")
