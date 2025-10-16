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
                    callback_data=f'admin:{json.dumps({"a":"start_round","n":{next_round}})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 Post Cost Hint",
                    callback_data=f'admin:{json.dumps({"a":"post_cost","n":{next_round}})}'
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
                    callback_data=f'admin:{json.dumps({"a":"start_round","n":{next_round}})}'
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 Post Cost Hint",
                    callback_data=f'admin:{json.dumps({"a":"post_cost","n":{next_round}})}'
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
