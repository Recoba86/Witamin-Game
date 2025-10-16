"""Main bot entry point."""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import BOT_TOKEN, DATABASE_PATH, LOG_LEVEL
from bot.storage.db import Database
from bot.services.game_engine import GameEngine
from bot.utils.logging import setup_logging
from bot.handlers import admin, player, common

logger = logging.getLogger(__name__)

async def main():
    """Main bot function."""
    # Setup logging
    setup_logging(LOG_LEVEL)
    logger.info("Starting Telegram Game Bot...")
    
    # Initialize database
    db = Database(DATABASE_PATH)
    await db.init_db()
    logger.info(f"Database initialized at {DATABASE_PATH}")
    
    # Initialize game engine
    game_engine = GameEngine(db)
    logger.info("Game engine initialized")
    
    # Initialize bot and dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Register routers (order matters - more specific first)
    dp.include_router(admin.router)
    dp.include_router(common.router)
    dp.include_router(player.router)  # Last, as it catches all text messages
    
    logger.info("Routers registered")
    
    # Start polling - pass game_engine as workflow_data
    try:
        logger.info("Bot started successfully! Polling for updates...")
        await dp.start_polling(
            bot, 
            allowed_updates=dp.resolve_used_update_types(),
            game_engine=game_engine  # Pass as keyword argument to workflow_data
        )
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}", exc_info=True)
