"""Admin keyboard layouts."""
import json
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import get_round_cost

class AdminKeyboards:
    """Factory for admin inline keyboards."""
    
    @staticmethod
    def new_game_controls(next_round: int = 1) -> InlineKeyboardMarkup:
        """
        Keyboard for new game with first round start.
        
        Args:
            next_round: The next round number to start
            
        Returns:
            InlineKeyboardMarkup
        """
        keyboard = [
            [
                InlineKeyboardButton(
                    text=f"▶️ Start Round {next_round}",
                    callback_data=f'admin:{json.dumps({"a":"ask_cost","n":next_round})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 Post Cost Hint",
                    callback_data=f'admin:{json.dumps({"a":"post_cost","n":next_round})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Show Status",
                    callback_data=f'admin:{json.dumps({"a":"status"})}'
                ),
                InlineKeyboardButton(
                    text="❌ Cancel Game",
                    callback_data=f'admin:{json.dumps({"a":"cancel"})}'
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    @staticmethod
    def active_round_controls(round_index: int) -> InlineKeyboardMarkup:
        """
        Keyboard for managing an active round.
        
        Args:
            round_index: Current round number
            
        Returns:
            InlineKeyboardMarkup
        """
        keyboard = [
            [
                InlineKeyboardButton(
                    text="⏸ Pause Round",
                    callback_data=f'admin:{json.dumps({"a":"pause_round"})}'
                ),
                InlineKeyboardButton(
                    text="🔒 Close Round",
                    callback_data=f'admin:{json.dumps({"a":"close_round"})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔓 Reveal Number",
                    callback_data=f'admin:{json.dumps({"a":"reveal"})}'
                ),
                InlineKeyboardButton(
                    text="📊 Show Status",
                    callback_data=f'admin:{json.dumps({"a":"status"})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Cancel Game",
                    callback_data=f'admin:{json.dumps({"a":"cancel"})}'
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    @staticmethod
    def paused_round_controls(round_index: int) -> InlineKeyboardMarkup:
        """
        Keyboard for a paused round.
        
        Args:
            round_index: Current round number
            
        Returns:
            InlineKeyboardMarkup
        """
        keyboard = [
            [
                InlineKeyboardButton(
                    text="▶️ Resume Round",
                    callback_data=f'admin:{json.dumps({"a":"resume_round"})}'
                ),
                InlineKeyboardButton(
                    text="🔒 Close Round",
                    callback_data=f'admin:{json.dumps({"a":"close_round"})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔓 Reveal Number",
                    callback_data=f'admin:{json.dumps({"a":"reveal"})}'
                ),
                InlineKeyboardButton(
                    text="📊 Show Status",
                    callback_data=f'admin:{json.dumps({"a":"status"})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Cancel Game",
                    callback_data=f'admin:{json.dumps({"a":"cancel"})}'
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    @staticmethod
    def between_rounds_controls(next_round: int) -> InlineKeyboardMarkup:
        """
        Keyboard between rounds (after closing a round).
        
        Args:
            next_round: The next round number
            
        Returns:
            InlineKeyboardMarkup
        """
        keyboard = [
            [
                InlineKeyboardButton(
                    text=f"▶️ Start Round {next_round}",
                    callback_data=f'admin:{json.dumps({"a":"ask_cost","n":next_round})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 Post Cost Hint",
                    callback_data=f'admin:{json.dumps({"a":"post_cost","n":next_round})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔓 Reveal Number",
                    callback_data=f'admin:{json.dumps({"a":"reveal"})}'
                ),
                InlineKeyboardButton(
                    text="📊 Show Status",
                    callback_data=f'admin:{json.dumps({"a":"status"})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Cancel Game",
                    callback_data=f'admin:{json.dumps({"a":"cancel"})}'
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    @staticmethod
    def select_stars_cost(round_index: int) -> InlineKeyboardMarkup:
        """
        Keyboard for selecting Stars cost for a round.
        
        Args:
            round_index: The round number to start
            
        Returns:
            InlineKeyboardMarkup
        """
        keyboard = [
            [
                InlineKeyboardButton(
                    text="⭐ 1 Star",
                    callback_data=f'admin:{json.dumps({"a":"start_round","n":round_index,"c":1})}'
                ),
                InlineKeyboardButton(
                    text="⭐⭐ 2 Stars",
                    callback_data=f'admin:{json.dumps({"a":"start_round","n":round_index,"c":2})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐⭐⭐ 3 Stars",
                    callback_data=f'admin:{json.dumps({"a":"start_round","n":round_index,"c":3})}'
                ),
                InlineKeyboardButton(
                    text="⭐⭐⭐⭐ 4 Stars",
                    callback_data=f'admin:{json.dumps({"a":"start_round","n":round_index,"c":4})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐⭐⭐⭐⭐ 5 Stars",
                    callback_data=f'admin:{json.dumps({"a":"start_round","n":round_index,"c":5})}'
                ),
                InlineKeyboardButton(
                    text="⭐⭐⭐⭐⭐⭐ 6+ Stars",
                    callback_data=f'admin:{json.dumps({"a":"start_round","n":round_index,"c":6})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Cancel",
                    callback_data=f'admin:{json.dumps({"a":"status"})}'
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

