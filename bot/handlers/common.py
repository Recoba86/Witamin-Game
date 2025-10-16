"""Common handlers for all users."""
import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.game_engine import GameEngine
from bot.services.announcer import Announcer

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command - show help message."""
    announcement = Announcer.help_message()
    await message.reply(announcement, parse_mode="HTML")
    logger.info(f"User {message.from_user.id} requested help")

@router.message(Command("status"))
async def cmd_status(message: Message, game_engine: GameEngine):
    """Handle /status command - show current game status."""
    
    # Get status for this chat
    status = await game_engine.get_status(message.chat.id)
    
    if not status:
        await message.reply(Announcer.no_active_game())
        return
    
    # Extract status information
    last_guess_value = None
    if status.get('last_guess'):
        last_guess_value = status['last_guess'].value
    
    announcement = Announcer.status_message(
        status['game'],
        status.get('active_round'),
        len(status['all_rounds']),
        last_guess_value
    )
    
    await message.reply(announcement, parse_mode="HTML")
    logger.info(f"Status requested for chat {message.chat.id}")
