"""Admin command handlers."""
import json
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from bot.config import ADMIN_IDS, get_round_cost, ROUND_DURATION_MINUTES, LANGUAGE
from bot.services.game_engine import GameEngine
from bot.services.announcer import Announcer
from bot.keyboards.admin import AdminKeyboards
from bot.storage.models import GameStatus, RoundStatus
from bot.translations import Translations

logger = logging.getLogger(__name__)

router = Router()

# Temporary storage for pending round starts (chat_id -> round_index)
pending_round_starts = {}

def is_admin(user_id: int) -> bool:
    """Check if user is admin."""
    return user_id in ADMIN_IDS

@router.message(Command("newgame"))
async def cmd_newgame(message: Message, game_engine: GameEngine):
    """Handle /newgame command - create a new game.
    
    Usage: /newgame [prize] [sponsor_name] [start_msg] [end_msg]
    All parameters are optional and separated by pipe |
    Example: /newgame 1000 | TechCorp | Welcome to our sponsored round! | Thanks for playing!
    """
    t = Translations.get
    lang = LANGUAGE
    
    if not is_admin(message.from_user.id):
        await message.reply(t('only_admins_newgame', lang))
        return
    
    if not message.chat.type in ["group", "supergroup"]:
        await message.reply("⚠️ This command only works in groups.")
        return
    
    # Check if there's already an active game
    existing_game = await game_engine.db.get_active_game(message.chat.id)
    if existing_game:
        await message.reply(t('active_game_exists', lang))
        return
    
    # Parse command arguments
    # Format: /newgame [prize] | [sponsor_name] | [start_message] | [end_message]
    prize_amount = None
    sponsor_name = None
    sponsor_start = None
    sponsor_end = None
    
    command_text = message.text.replace("/newgame", "").strip()
    
    if command_text:
        # Split by pipe separator
        parts = [p.strip() for p in command_text.split("|")]
        
        try:
            # First part is prize amount
            if parts[0]:
                prize_amount = float(parts[0])
            
            # Second part is sponsor name
            if len(parts) > 1 and parts[1]:
                sponsor_name = parts[1]
            
            # Third part is sponsor start message
            if len(parts) > 2 and parts[2]:
                sponsor_start = parts[2]
            
            # Fourth part is sponsor end message
            if len(parts) > 3 and parts[3]:
                sponsor_end = parts[3]
                
        except ValueError:
            await message.reply(t('invalid_format', lang), parse_mode="HTML")
            return
    
    # Create new game
    game, target_hash = await game_engine.create_game(
        message.chat.id, 
        prize_amount,
        sponsor_name,
        sponsor_start,
        sponsor_end
    )
    
    # Send announcement
    announcement = Announcer.game_created(target_hash, prize_amount, sponsor_name)
    keyboard = AdminKeyboards.new_game_controls(next_round=1)
    
    await message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    logger.info(
        f"New game created in chat {message.chat.id}, game_id={game.id}, "
        f"prize={prize_amount}, sponsor={sponsor_name}"
    )

@router.message(Command("start_round"))
async def cmd_start_round(message: Message, game_engine: GameEngine):
    """Handle /start_round command - prompt for Stars cost."""
    t = Translations.get
    lang = LANGUAGE
    
    if not is_admin(message.from_user.id):
        await message.reply(t('only_admins', lang))
        return
    
    # Get active game
    game = await game_engine.db.get_active_game(message.chat.id)
    if not game:
        await message.reply(t('no_active_game', lang))
        return
    
    # Determine next round
    all_rounds = await game_engine.db.get_rounds_for_game(game.id)
    next_round = len(all_rounds) + 1
    
    # Check if a round is already active
    active_round = await game_engine.db.get_active_round(game.id)
    if active_round and active_round.status == RoundStatus.ACTIVE:
        await message.reply(t('round_already_active', lang))
        return
    
    # Store pending round and ask for Stars cost
    pending_round_starts[message.chat.id] = next_round
    await message.reply(t('ask_stars_cost', lang, round=next_round), parse_mode="HTML")
    logger.info(f"Admin {message.from_user.id} initiated /start_round for round {next_round}")

@router.message(Command("pause_round"))
async def cmd_pause_round(message: Message, game_engine: GameEngine):
    """Handle /pause_round command."""
    t = Translations.get
    lang = LANGUAGE
    
    if not is_admin(message.from_user.id):
        await message.reply(t('only_admins', lang))
        return
    
    game = await game_engine.db.get_active_game(message.chat.id)
    if not game:
        await message.reply(t('no_active_game', lang))
        return
    
    active_round = await game_engine.db.get_active_round(game.id)
    if not active_round:
        await message.reply(t('no_active_round', lang))
        return
    
    await game_engine.pause_round(active_round.id)
    
    announcement = Announcer.round_paused()
    keyboard = AdminKeyboards.paused_round_controls(active_round.round_index)
    
    await message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    logger.info(f"Round {active_round.id} paused via command")

@router.message(Command("resume_round"))
async def cmd_resume_round(message: Message, game_engine: GameEngine):
    """Handle /resume_round command."""
    t = Translations.get
    lang = LANGUAGE
    
    if not is_admin(message.from_user.id):
        await message.reply(t('only_admins', lang))
        return
    
    game = await game_engine.db.get_active_game(message.chat.id)
    if not game:
        await message.reply(t('no_active_game', lang))
        return
    
    active_round = await game_engine.db.get_active_round(game.id)
    if not active_round:
        await message.reply(t('no_active_round', lang))
        return
    
    await game_engine.resume_round(active_round.id)
    
    announcement = Announcer.round_resumed(active_round.round_index)
    keyboard = AdminKeyboards.active_round_controls(active_round.round_index)
    
    await message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    logger.info(f"Round {active_round.id} resumed via command")

@router.message(Command("close_round"))
async def cmd_close_round(message: Message, game_engine: GameEngine):
    """Handle /close_round command."""
    t = Translations.get
    lang = LANGUAGE
    
    if not is_admin(message.from_user.id):
        await message.reply(t('only_admins', lang))
        return
    
    game = await game_engine.db.get_active_game(message.chat.id)
    if not game:
        await message.reply(t('no_active_game', lang))
        return
    
    active_round = await game_engine.db.get_active_round(game.id)
    if not active_round:
        await message.reply(t('no_active_round', lang))
        return
    
    await game_engine.close_round(active_round.id)
    
    # Calculate next round number
    all_rounds = await game_engine.db.get_rounds_for_game(game.id)
    next_round = len(all_rounds) + 1
    
    # Send announcement with sponsor end message if available
    announcement = Announcer.round_closed(active_round.round_index, game.sponsor_end_message)
    keyboard = AdminKeyboards.between_rounds_controls(next_round)
    
    await message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    logger.info(f"Round {active_round.id} closed via command")

@router.message(Command("reveal"))
async def cmd_reveal(message: Message, game_engine: GameEngine):
    """Handle /reveal command - manually reveal the number."""
    t = Translations.get
    lang = LANGUAGE
    
    if not is_admin(message.from_user.id):
        await message.reply(t('only_admins', lang))
        return
    
    game = await game_engine.db.get_active_game(message.chat.id)
    if not game:
        await message.reply(t('no_active_game', lang))
        return
    
    # Verify the game
    is_valid = await game_engine.verify_game(game.id)
    
    announcement = Announcer.manual_reveal(game.number, game.salt, game.target_hash)
    
    await message.reply(announcement, parse_mode="HTML")
    
    # Mark game as finished (no winner)
    await game_engine.db.update_game_status(game.id, GameStatus.GAME_FINISHED)
    
    logger.info(f"Game {game.id} manually revealed via command")

@router.message(Command("cancel_game"))
async def cmd_cancel_game(message: Message, game_engine: GameEngine):
    """Handle /cancel_game command."""
    t = Translations.get
    lang = LANGUAGE
    
    if not is_admin(message.from_user.id):
        await message.reply(t('only_admins', lang))
        return
    
    game = await game_engine.db.get_active_game(message.chat.id)
    if not game:
        await message.reply(t('no_active_game', lang))
        return
    
    await game_engine.cancel_game(game.id)
    
    announcement = Announcer.game_canceled()
    
    await message.reply(announcement, parse_mode="HTML")
    logger.info(f"Game {game.id} canceled via command")

@router.message(Command("post_cost"))
async def cmd_post_cost(message: Message, game_engine: GameEngine):
    """Handle /post_cost command - post cost hint for next round."""
    t = Translations.get
    lang = LANGUAGE
    
    if not is_admin(message.from_user.id):
        await message.reply(t('only_admins', lang))
        return
    
    game = await game_engine.db.get_active_game(message.chat.id)
    if not game:
        await message.reply(t('no_active_game', lang))
        return
    
    # Determine next round
    all_rounds = await game_engine.db.get_rounds_for_game(game.id)
    next_round = len(all_rounds) + 1
    
    cost = get_round_cost(next_round)
    announcement = Announcer.cost_hint(next_round, cost)
    
    await message.reply(announcement, parse_mode="HTML")
    logger.info(f"Cost hint posted for round {next_round} via command")

@router.message(Command("cancel"))
async def cmd_cancel_input(message: Message):
    """Cancel any pending admin input."""
    t = Translations.get
    lang = LANGUAGE
    
    if not is_admin(message.from_user.id):
        return
    
    if message.chat.id in pending_round_starts:
        del pending_round_starts[message.chat.id]
        await message.reply(t('input_cancelled', lang))
    else:
        await message.reply(t('no_pending_input', lang))

@router.message(F.text)
async def handle_stars_cost_input(message: Message, game_engine: GameEngine):
    """Handle Stars cost input from admin."""
    t = Translations.get
    lang = LANGUAGE
    
    # Check if this chat has a pending round start
    if message.chat.id not in pending_round_starts:
        return  # Not waiting for input from this chat
    
    # Check if user is admin
    if not is_admin(message.from_user.id):
        return
    
    # Get the round index
    round_index = pending_round_starts[message.chat.id]
    
    # Parse the Stars cost
    try:
        stars_cost = int(message.text.strip())
        if stars_cost < 0:
            await message.reply(t('stars_must_be_positive', lang))
            return
    except ValueError:
        await message.reply(t('invalid_stars_number', lang))
        return
    
    # Clear the pending state
    del pending_round_starts[message.chat.id]
    
    # Get the game
    game = await game_engine.db.get_active_game(message.chat.id)
    if not game:
        await message.reply(t('no_active_game_found', lang))
        return
    
    # Verify no round is currently active
    active_round = await game_engine.db.get_active_round(game.id)
    if active_round and active_round.status == RoundStatus.ACTIVE:
        await message.reply(t('round_already_active', lang))
        return
    
    # Start the round with the specified Stars cost
    round_obj = await game_engine.start_round(game.id, round_index, stars_cost)
    
    # Send announcement with sponsor message if available
    announcement = Announcer.round_started(
        round_index, 
        round_obj.message_cost_hint, 
        ROUND_DURATION_MINUTES,
        game.sponsor_start_message
    )
    keyboard = AdminKeyboards.active_round_controls(round_index)
    
    await message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    logger.info(f"Round {round_index} started for game {game.id} with {stars_cost} Stars cost")

@router.callback_query(F.data.startswith("admin:"))
async def handle_admin_callback(callback: CallbackQuery, game_engine: GameEngine):
    """Handle all admin callback buttons."""
    t = Translations.get
    lang = LANGUAGE
    
    if not is_admin(callback.from_user.id):
        await callback.answer(t('only_admins', lang), show_alert=True)
        return
    
    # Parse callback data
    try:
        json_data = callback.data.replace("admin:", "")
        data = json.loads(json_data)
        action = data.get("a")
    except json.JSONDecodeError:
        await callback.answer(t('invalid_callback', lang), show_alert=True)
        return
    
    # Get active game
    game = await game_engine.db.get_active_game(callback.message.chat.id)
    if not game and action not in ["status"]:
        await callback.answer(t('no_active_game', lang), show_alert=True)
        return
    
    # Route to appropriate handler
    if action == "ask_cost":
        await handle_ask_cost(callback, data.get("n", 1))
    elif action == "pause_round":
        await handle_pause_round(callback, game_engine, game)
    elif action == "resume_round":
        await handle_resume_round(callback, game_engine, game)
    elif action == "close_round":
        await handle_close_round(callback, game_engine, game)
    elif action == "reveal":
        await handle_reveal(callback, game_engine, game)
    elif action == "cancel":
        await handle_cancel(callback, game_engine, game)
    elif action == "post_cost":
        await handle_post_cost(callback, game_engine, game, data.get("n", 1))
    elif action == "status":
        await handle_status(callback, game_engine, callback.message.chat.id)
    else:
        await callback.answer(t('unknown_action', lang), show_alert=True)

async def handle_ask_cost(callback: CallbackQuery, round_index: int):
    """Ask admin to type Stars cost for the round."""
    t = Translations.get
    lang = LANGUAGE
    
    # Store the pending round start
    pending_round_starts[callback.message.chat.id] = round_index
    
    await callback.message.reply(
        t('ask_stars_cost', lang, round=round_index),
        parse_mode="HTML"
    )
    await callback.answer()

async def handle_pause_round(callback: CallbackQuery, engine: GameEngine, game):
    """Handle pausing the current round."""
    t = Translations.get
    lang = LANGUAGE
    
    active_round = await engine.db.get_active_round(game.id)
    if not active_round:
        await callback.answer(t('no_active_round', lang), show_alert=True)
        return
    
    await engine.pause_round(active_round.id)
    
    announcement = Announcer.round_paused()
    keyboard = AdminKeyboards.paused_round_controls(active_round.round_index)
    
    await callback.message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer(t('round_paused_btn', lang))
    logger.info(f"Round {active_round.id} paused")

async def handle_resume_round(callback: CallbackQuery, engine: GameEngine, game):
    """Handle resuming a paused round."""
    t = Translations.get
    lang = LANGUAGE
    
    active_round = await engine.db.get_active_round(game.id)
    if not active_round:
        await callback.answer(t('no_active_round', lang), show_alert=True)
        return
    
    await engine.resume_round(active_round.id)
    
    announcement = Announcer.round_resumed(active_round.round_index)
    keyboard = AdminKeyboards.active_round_controls(active_round.round_index)
    
    await callback.message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer(t('round_resumed_btn', lang))
    logger.info(f"Round {active_round.id} resumed")

async def handle_close_round(callback: CallbackQuery, engine: GameEngine, game):
    """Handle closing the current round."""
    t = Translations.get
    lang = LANGUAGE
    
    active_round = await engine.db.get_active_round(game.id)
    if not active_round:
        await callback.answer(t('no_active_round', lang), show_alert=True)
        return
    
    await engine.close_round(active_round.id)
    
    # Calculate next round number
    all_rounds = await engine.db.get_rounds_for_game(game.id)
    next_round = len(all_rounds) + 1
    
    # Send announcement with sponsor end message if available
    announcement = Announcer.round_closed(active_round.round_index, game.sponsor_end_message)
    keyboard = AdminKeyboards.between_rounds_controls(next_round)
    
    await callback.message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer(t('round_closed_btn', lang))
    logger.info(f"Round {active_round.id} closed")

async def handle_reveal(callback: CallbackQuery, engine: GameEngine, game):
    """Handle manual reveal of the number."""
    t = Translations.get
    lang = LANGUAGE
    
    # Verify the game
    is_valid = await engine.verify_game(game.id)
    
    announcement = Announcer.manual_reveal(game.number, game.salt, game.target_hash)
    
    await callback.message.reply(announcement, parse_mode="HTML")
    
    # Mark game as finished (no winner)
    await engine.db.update_game_status(game.id, GameStatus.GAME_FINISHED)
    
    await callback.answer(t('game_revealed_btn', lang))
    logger.info(f"Game {game.id} manually revealed")

async def handle_cancel(callback: CallbackQuery, engine: GameEngine, game):
    """Handle game cancellation."""
    t = Translations.get
    lang = LANGUAGE
    
    await engine.cancel_game(game.id)
    
    announcement = Announcer.game_canceled()
    
    await callback.message.reply(announcement, parse_mode="HTML")
    await callback.answer(t('game_canceled_btn', lang))
    logger.info(f"Game {game.id} canceled")

async def handle_post_cost(callback: CallbackQuery, engine: GameEngine, game, round_index: int):
    """Handle posting cost hint for a round."""
    cost = get_round_cost(round_index)
    announcement = Announcer.cost_hint(round_index, cost)
    
    await callback.message.reply(announcement, parse_mode="HTML")
    await callback.answer("💰 Cost hint posted")

async def handle_status(callback: CallbackQuery, engine: GameEngine, chat_id: int):
    """Handle status request."""
    t = Translations.get
    lang = LANGUAGE
    
    status = await engine.get_status(chat_id)
    
    if not status:
        await callback.answer(t('no_active_game', lang), show_alert=True)
        return
    
    last_guess_value = None
    if status.get('last_guess'):
        last_guess_value = status['last_guess'].value
    
    announcement = Announcer.status_message(
        status['game'],
        status.get('active_round'),
        len(status['all_rounds']),
        last_guess_value
    )
    
    await callback.message.reply(announcement, parse_mode="HTML")
    await callback.answer("📊 Status displayed")
