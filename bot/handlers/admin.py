"""Admin command handlers."""
import json
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from bot.config import ADMIN_IDS, get_round_cost, ROUND_DURATION_MINUTES
from bot.services.game_engine import GameEngine
from bot.services.announcer import Announcer
from bot.keyboards.admin import AdminKeyboards
from bot.storage.models import GameStatus, RoundStatus

logger = logging.getLogger(__name__)

router = Router()

def is_admin(user_id: int) -> bool:
    """Check if user is admin."""
    return user_id in ADMIN_IDS

async def get_engine(message_or_query) -> GameEngine:
    """Get game engine from bot data."""
    if isinstance(message_or_query, Message):
        return message_or_query.bot.get("game_engine")
    else:
        return message_or_query.bot.get("game_engine")

@router.message(Command("newgame"))
async def cmd_newgame(message: Message):
    """Handle /newgame command - create a new game.
    
    Usage: /newgame [prize] [sponsor_name] [start_msg] [end_msg]
    All parameters are optional and separated by pipe |
    Example: /newgame 1000 | TechCorp | Welcome to our sponsored round! | Thanks for playing!
    """
    if not is_admin(message.from_user.id):
        await message.reply("⚠️ Only admins can start a new game.")
        return
    
    if not message.chat.type in ["group", "supergroup"]:
        await message.reply("⚠️ This command only works in groups.")
        return
    
    engine: GameEngine = message.bot.get("game_engine")
    
    # Check if there's already an active game
    existing_game = await engine.db.get_active_game(message.chat.id)
    if existing_game:
        await message.reply(
            "⚠️ There's already an active game. Cancel it first with the Cancel button."
        )
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
            await message.reply(
                "⚠️ Invalid format!\n\n"
                "<b>Usage:</b>\n"
                "<code>/newgame [prize] | [sponsor] | [start_msg] | [end_msg]</code>\n\n"
                "<b>Examples:</b>\n"
                "• <code>/newgame 1000</code> (just prize)\n"
                "• <code>/newgame 1000 | TechCorp | Welcome! | Thanks!</code>\n"
                "• <code>/newgame | | Welcome | Goodbye</code> (no prize/sponsor name)",
                parse_mode="HTML"
            )
            return
    
    # Create new game
    game, target_hash = await engine.create_game(
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

@router.callback_query(F.data.startswith("admin:"))
async def handle_admin_callback(callback: CallbackQuery):
    """Handle all admin callback buttons."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⚠️ Only admins can use these controls.", show_alert=True)
        return
    
    # Parse callback data
    try:
        json_data = callback.data.replace("admin:", "")
        data = json.loads(json_data)
        action = data.get("a")
    except json.JSONDecodeError:
        await callback.answer("❌ Invalid callback data", show_alert=True)
        return
    
    engine: GameEngine = callback.bot.get("game_engine")
    
    # Get active game
    game = await engine.db.get_active_game(callback.message.chat.id)
    if not game and action not in ["status"]:
        await callback.answer("⚠️ No active game", show_alert=True)
        return
    
    # Route to appropriate handler
    if action == "start_round":
        await handle_start_round(callback, engine, game, data.get("n", 1))
    elif action == "pause_round":
        await handle_pause_round(callback, engine, game)
    elif action == "resume_round":
        await handle_resume_round(callback, engine, game)
    elif action == "close_round":
        await handle_close_round(callback, engine, game)
    elif action == "reveal":
        await handle_reveal(callback, engine, game)
    elif action == "cancel":
        await handle_cancel(callback, engine, game)
    elif action == "post_cost":
        await handle_post_cost(callback, engine, game, data.get("n", 1))
    elif action == "status":
        await handle_status(callback, engine, callback.message.chat.id)
    else:
        await callback.answer("❌ Unknown action", show_alert=True)

async def handle_start_round(callback: CallbackQuery, engine: GameEngine, game, round_index: int):
    """Handle starting a new round."""
    # Verify no round is currently active
    active_round = await engine.db.get_active_round(game.id)
    if active_round and active_round.status == RoundStatus.ACTIVE:
        await callback.answer("⚠️ A round is already active", show_alert=True)
        return
    
    # Start the round
    round_obj = await engine.start_round(game.id, round_index)
    
    # Send announcement with sponsor message if available
    announcement = Announcer.round_started(
        round_index, 
        round_obj.message_cost_hint, 
        ROUND_DURATION_MINUTES,
        game.sponsor_start_message
    )
    keyboard = AdminKeyboards.active_round_controls(round_index)
    
    await callback.message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer(f"✅ Round {round_index} started")
    logger.info(f"Round {round_index} started for game {game.id}")

async def handle_pause_round(callback: CallbackQuery, engine: GameEngine, game):
    """Handle pausing the current round."""
    active_round = await engine.db.get_active_round(game.id)
    if not active_round:
        await callback.answer("⚠️ No active round", show_alert=True)
        return
    
    await engine.pause_round(active_round.id)
    
    announcement = Announcer.round_paused()
    keyboard = AdminKeyboards.paused_round_controls(active_round.index)
    
    await callback.message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer("⏸ Round paused")
    logger.info(f"Round {active_round.id} paused")

async def handle_resume_round(callback: CallbackQuery, engine: GameEngine, game):
    """Handle resuming a paused round."""
    active_round = await engine.db.get_active_round(game.id)
    if not active_round:
        await callback.answer("⚠️ No active round", show_alert=True)
        return
    
    await engine.resume_round(active_round.id)
    
    announcement = Announcer.round_resumed(active_round.index)
    keyboard = AdminKeyboards.active_round_controls(active_round.index)
    
    await callback.message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer("▶️ Round resumed")
    logger.info(f"Round {active_round.id} resumed")

async def handle_close_round(callback: CallbackQuery, engine: GameEngine, game):
    """Handle closing the current round."""
    active_round = await engine.db.get_active_round(game.id)
    if not active_round:
        await callback.answer("⚠️ No active round", show_alert=True)
        return
    
    await engine.close_round(active_round.id)
    
    # Calculate next round number
    all_rounds = await engine.db.get_rounds_for_game(game.id)
    next_round = len(all_rounds) + 1
    
    # Send announcement with sponsor end message if available
    announcement = Announcer.round_closed(active_round.index, game.sponsor_end_message)
    keyboard = AdminKeyboards.between_rounds_controls(next_round)
    
    await callback.message.reply(announcement, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer("🔒 Round closed")
    logger.info(f"Round {active_round.id} closed")

async def handle_reveal(callback: CallbackQuery, engine: GameEngine, game):
    """Handle manual reveal of the number."""
    # Verify the game
    is_valid = await engine.verify_game(game.id)
    
    announcement = Announcer.manual_reveal(game.number, game.salt, game.target_hash)
    
    await callback.message.reply(announcement, parse_mode="HTML")
    
    # Mark game as finished (no winner)
    await engine.db.update_game_status(game.id, GameStatus.GAME_FINISHED)
    
    await callback.answer("🔓 Number revealed")
    logger.info(f"Game {game.id} manually revealed")

async def handle_cancel(callback: CallbackQuery, engine: GameEngine, game):
    """Handle game cancellation."""
    await engine.cancel_game(game.id)
    
    announcement = Announcer.game_canceled()
    await callback.message.reply(announcement, parse_mode="HTML")
    await callback.answer("❌ Game canceled")
    logger.info(f"Game {game.id} canceled")

async def handle_post_cost(callback: CallbackQuery, engine: GameEngine, game, round_index: int):
    """Handle posting cost hint for a round."""
    cost = get_round_cost(round_index)
    announcement = Announcer.cost_hint(round_index, cost)
    
    await callback.message.reply(announcement, parse_mode="HTML")
    await callback.answer("💰 Cost hint posted")

async def handle_status(callback: CallbackQuery, engine: GameEngine, chat_id: int):
    """Handle status request."""
    status = await engine.get_status(chat_id)
    
    if not status:
        await callback.answer("⚠️ No active game", show_alert=True)
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
