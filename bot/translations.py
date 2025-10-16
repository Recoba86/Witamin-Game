"""Translation module for bilingual support (English and Persian)."""

class Translations:
    """Provides translations for all bot messages."""
    
    # English translations
    EN = {
        # Game announcements
        "game_created_title": "🎮 <b>New Game Started!</b>",
        "provably_fair": "🔒 <b>Provably Fair Commitment</b>",
        "prize": "💰 <b>Prize:</b> {amount} ⭐",
        "sponsored_by": "🎗 <b>Sponsored by:</b> {sponsor}",
        "rules_title": "📋 <b>Rules:</b>",
        "rule_range": "• Secret number is between 1 and 10,000",
        "rule_guesses": "• Each player can guess up to 10 times per round",
        "rule_duration": "• Each round lasts 2 minutes (or until 10 guesses minimum)",
        "rule_hints": "• Bot replies with hints: ⬆️ if number is higher, ⬇️ if lower",
        "rule_winner": "• First correct guess wins!",
        "rule_loyalty": "• Stay in the game longer for bigger rewards! 🎁",
        "start_button_prompt": "👆 Admin: Press <b>Start Round 1</b> to begin!",
        
        # Round announcements
        "round_started": "🔥 <b>Round {round} Started!</b>",
        "suggested_cost": "💰 Suggested cost: <b>{cost} ⭐ Star(s)</b>",
        "duration": "⏱ Duration: <b>{minutes} minutes</b>",
        "duration_with_min": "⏱ Duration: <b>{minutes} minutes</b> (min 10 guesses)",
        "range": "🎯 Range: 1 - 10,000",
        "guess_limit": "📊 Limit: 10 guesses per player",
        "good_luck": "Good luck! 🍀",
        "sponsor_message": "📢 <b>Sponsor Message:</b>\n{message}",
        
        # Round status
        "round_paused": "⏸ <b>Round Paused</b>\n\nWaiting for admin to resume...",
        "round_resumed": "▶️ <b>Round {round} Resumed!</b>\n\nContinue guessing!",
        "round_closed": "🔒 <b>Round {round} Closed</b>\n\nNo winner yet. Admin can start the next round.",
        
        # Hints
        "hint_title": "💡 <b>Hint!</b>",
        "hint_higher": "The secret number is <b>higher ⬆️</b> than {guess}",
        "hint_lower": "The secret number is <b>lower ⬇️</b> than {guess}",
        
        # Winner announcement
        "winner_title": "🎉 <b>WE HAVE A WINNER!</b> 🎉",
        "winner": "🏆 Winner: {user}",
        "secret_number": "🎯 Secret Number: <b>{number}</b>",
        "won_in_round": "📍 Won in Round: <b>{round}</b>",
        "prize_won": "💰 Prize Won: <b>{amount} ⭐</b>",
        "loyalty_penalty": "⚠️ Loyalty Penalty: <b>{penalty}% (missed rounds)</b>",
        "proof_title": "🔓 <b>Proof (Commit-Reveal):</b>",
        "proof_number": "Number: <code>{number}</code>",
        "proof_salt": "Salt: <code>{salt}</code>",
        "proof_hash": "Hash: <code>{hash}</code>",
        "verification": "Verification: {emoji} <b>{status}</b>",
        "verification_valid": "VALID",
        "verification_invalid": "INVALID",
        "thank_you": "Thank you for playing! 🎮",
        
        # Game management
        "game_canceled": "❌ <b>Game Canceled</b>\n\nA new game can be started with /newgame",
        
        # Error messages
        "guess_limit_reached": "⚠️ You've reached the maximum of 10 guesses for this round.",
        "invalid_guess": "❌ Invalid guess. Please send a number between 1 and 10,000.",
        "no_active_game": "⚠️ No active game. Admin can start one with /newgame",
        "not_accepting_guesses": "⏸ Round is not currently accepting guesses. Please wait for admin.",
        "no_active_round": "⚠️ No active round",
        "round_already_active": "⚠️ A round is already active",
        "only_admins": "⚠️ Only admins can use these controls.",
        "only_admins_newgame": "⚠️ Only admins can start a new game.",
        "active_game_exists": "⚠️ There's already an active game. Cancel it first with the Cancel button.",
        "invalid_format": "⚠️ Invalid format!",
        "invalid_callback": "❌ Invalid callback data",
        "unknown_action": "❌ Unknown action",
        
        # Status message
        "status_title": "📊 <b>Game Status</b>",
        "game_state": "🎮 Game State: <b>{state}</b>",
        "total_rounds": "📈 Total Rounds: <b>{rounds}</b>",
        "active_round": "🔥 <b>Active Round {round}</b>",
        "total_guesses": "📊 Total Guesses: <b>{guesses}</b>",
        "last_guess": "🎯 Last Guess: <b>{guess}</b>",
        "next_hint": "💡 Next Hint: <b>{guesses} guesses away</b>",
        
        # Help message
        "help_title": "🎯 <b>Incremental Guess Game</b>",
        "how_to_play": "<b>How to Play:</b>",
        "help_step1": "1. A secret number between 1-10,000 is chosen",
        "help_step2": "2. Send your guess as a number in the chat",
        "help_step3": "3. You can guess up to 10 times per round",
        "help_step4": "4. Bot replies with hints ⬆️ (higher) or ⬇️ (lower) to each guess",
        "help_step5": "5. Rounds last 2 minutes (minimum 10 guesses total)",
        "help_step6": "6. First to guess correctly wins the prize!",
        "loyalty_title": "<b>Loyalty Rewards:</b>",
        "loyalty_rule1": "• Join from Round 1: 100% reward",
        "loyalty_rule2": "• Miss Round 1: 75% reward",
        "loyalty_rule3": "• Miss other rounds: -15% per round",
        "loyalty_rule4": "• Minimum: 50% reward",
        "commands_title": "<b>Commands:</b>",
        "cmd_start": "/start - Show this help",
        "cmd_status": "/status - View current game status",
        "cmd_newgame": "/newgame [prize] - (Admin) Start new game",
        "cmd_start_round": "/start_round - (Admin) Start a new round",
        "cmd_pause_round": "/pause_round - (Admin) Pause current round",
        "cmd_resume_round": "/resume_round - (Admin) Resume paused round",
        "cmd_close_round": "/close_round - (Admin) Close current round",
        "cmd_reveal": "/reveal - (Admin) Reveal the secret number",
        "cmd_cancel_game": "/cancel_game - (Admin) Cancel the game",
        "cmd_post_cost": "/post_cost - (Admin) Post cost hint",
        "help_footer": "🎮 <i>Guess the hidden number! One winner, fair hash, and bigger rewards the longer you stay in the game!</i>",
        
        # Manual reveal
        "reveal_title": "🔓 <b>Game Revealed</b>",
        "secret_was": "🎯 Secret Number was: <b>{number}</b>",
        "no_winner": "No winner this time. Better luck next game! 🎮",
        
        # Cost hint
        "cost_hint_title": "💰 <b>Round {round} Cost</b>",
        "cost_suggested": "Suggested: <b>{cost} ⭐ Star(s)</b>",
        "cost_warning": "⚠️ Admin should manually set this in Telegram's \"Starred Group Settings\" before starting the round.",
        
        # Admin messages
        "newgame_usage": "⚠️ <b>Prize amount required!</b>\n\n<b>Usage:</b>\n<code>/newgame [prize]</code>\nor\n<code>/newgame [prize] | [sponsor] | [start_msg] | [end_msg]</code>\n\n<b>Examples:</b>\n• <code>/newgame 1000</code>\n• <code>/newgame 500 | TechCorp</code>\n• <code>/newgame 1000 | TechCorp | Welcome! | Thanks!</code>",
        "ask_stars_cost": "⭐ <b>Enter Stars Cost for Round {round}</b>\n\nPlease type the number of Stars required to post in this group.\nExamples: <code>1</code>, <code>4</code>, <code>10</code>, etc.\n\nOr send <code>/cancel</code> to cancel.",
        "input_cancelled": "❌ Input cancelled.",
        "no_pending_input": "⚠️ No pending input to cancel.",
        "invalid_stars_number": "⚠️ Invalid number. Please type a valid number of Stars (e.g., 1, 4, 10).",
        "stars_must_be_positive": "⚠️ Stars cost must be a positive number. Please try again.",
        "no_active_game_found": "⚠️ No active game found.",
        "round_started_success": "✅ Round {round} started with {cost} ⭐ cost",
        "round_started_log": "✅ Round {round} started",
        "round_paused_btn": "⏸ Round paused",
        "round_resumed_btn": "▶️ Round resumed",
        "round_closed_btn": "🔒 Round closed",
        "game_revealed_btn": "🔓 Game revealed",
        "game_canceled_btn": "❌ Game canceled",
    }
    
    # Persian translations (با پشتیبانی RTL)
    FA = {
        # Game announcements
        "game_created_title": "🎮 <b>بازی جدید شروع شد!</b>",
        "provably_fair": "🔒 <b>تعهد قابل اثبات</b>",
        "prize": "💰 <b>جایزه:</b> {amount} ⭐",
        "sponsored_by": "🎗 <b>حامی مالی:</b> {sponsor}",
        "rules_title": "📋 <b>قوانین:</b>",
        "rule_range": "• عدد مخفی بین ۱ تا ۱۰,۰۰۰ است",
        "rule_guesses": "• هر بازیکن می‌تواند حداکثر ۱۰ بار در هر دور حدس بزند",
        "rule_duration": "• هر دور ۲ دقیقه طول می‌کشد (یا حداقل ۱۰ حدس)",
        "rule_hints": "• ربات با پیام پاسخ می‌دهد: ⬆️ اگر عدد بالاتر باشد، ⬇️ اگر پایین‌تر باشد",
        "rule_winner": "• اولین حدس درست برنده می‌شود!",
        "rule_loyalty": "• هر چه بیشتر در بازی بمانید، جایزه بیشتری دریافت می‌کنید! 🎁",
        "start_button_prompt": "👆 ادمین: دکمه <b>شروع دور ۱</b> را بزنید!",
        
        # Round announcements
        "round_started": "🔥 <b>دور {round} شروع شد!</b>",
        "suggested_cost": "💰 هزینه پیشنهادی: <b>{cost} ⭐ ستاره</b>",
        "duration": "⏱ مدت زمان: <b>{minutes} دقیقه</b>",
        "duration_with_min": "⏱ مدت زمان: <b>{minutes} دقیقه</b> (حداقل ۱۰ حدس)",
        "range": "🎯 محدوده: ۱ تا ۱۰,۰۰۰",
        "guess_limit": "📊 محدودیت: ۱۰ حدس برای هر بازیکن",
        "good_luck": "موفق باشید! 🍀",
        "sponsor_message": "📢 <b>پیام حامی:</b>\n{message}",
        
        # Round status
        "round_paused": "⏸ <b>دور متوقف شد</b>\n\nمنتظر ادمین برای ادامه...",
        "round_resumed": "▶️ <b>دور {round} از سر گرفته شد!</b>\n\nبه حدس زدن ادامه دهید!",
        "round_closed": "🔒 <b>دور {round} بسته شد</b>\n\nهنوز برنده‌ای نداریم. ادمین می‌تواند دور بعدی را شروع کند.",
        
        # Hints
        "hint_title": "💡 <b>راهنما!</b>",
        "hint_higher": "عدد مخفی <b>بالاتر ⬆️</b> از {guess} است",
        "hint_lower": "عدد مخفی <b>پایین‌تر ⬇️</b> از {guess} است",
        
        # Winner announcement
        "winner_title": "🎉 <b>برنده را داریم!</b> 🎉",
        "winner": "🏆 برنده: {user}",
        "secret_number": "🎯 عدد مخفی: <b>{number}</b>",
        "won_in_round": "📍 برنده در دور: <b>{round}</b>",
        "prize_won": "💰 جایزه برنده: <b>{amount} ⭐</b>",
        "loyalty_penalty": "⚠️ جریمه وفاداری: <b>{penalty}% (دورهای از دست رفته)</b>",
        "proof_title": "🔓 <b>اثبات (Commit-Reveal):</b>",
        "proof_number": "عدد: <code>{number}</code>",
        "proof_salt": "Salt: <code>{salt}</code>",
        "proof_hash": "Hash: <code>{hash}</code>",
        "verification": "تأیید: {emoji} <b>{status}</b>",
        "verification_valid": "معتبر",
        "verification_invalid": "نامعتبر",
        "thank_you": "از شرکت شما متشکریم! 🎮",
        
        # Game management
        "game_canceled": "❌ <b>بازی لغو شد</b>\n\nبازی جدید می‌تواند با /newgame شروع شود",
        
        # Error messages
        "guess_limit_reached": "⚠️ شما به حداکثر ۱۰ حدس برای این دور رسیده‌اید.",
        "invalid_guess": "❌ حدس نامعتبر. لطفا عددی بین ۱ تا ۱۰,۰۰۰ ارسال کنید.",
        "no_active_game": "⚠️ بازی فعالی وجود ندارد. ادمین می‌تواند با /newgame یکی شروع کند",
        "not_accepting_guesses": "⏸ دور در حال حاضر حدس نمی‌پذیرد. لطفا منتظر ادمین بمانید.",
        "no_active_round": "⚠️ دور فعالی وجود ندارد",
        "round_already_active": "⚠️ یک دور در حال حاضر فعال است",
        "only_admins": "⚠️ فقط ادمین‌ها می‌توانند از این کنترل‌ها استفاده کنند.",
        "only_admins_newgame": "⚠️ فقط ادمین‌ها می‌توانند بازی جدید شروع کنند.",
        "active_game_exists": "⚠️ بازی فعالی وجود دارد. ابتدا آن را با دکمه لغو کنید.",
        "invalid_format": "⚠️ فرمت نامعتبر!",
        "invalid_callback": "❌ داده callback نامعتبر است",
        "unknown_action": "❌ عملیات ناشناخته",
        
        # Status message
        "status_title": "📊 <b>وضعیت بازی</b>",
        "game_state": "🎮 وضعیت بازی: <b>{state}</b>",
        "total_rounds": "📈 کل دورها: <b>{rounds}</b>",
        "active_round": "🔥 <b>دور فعال {round}</b>",
        "total_guesses": "📊 کل حدس‌ها: <b>{guesses}</b>",
        "last_guess": "🎯 آخرین حدس: <b>{guess}</b>",
        "next_hint": "💡 راهنمای بعدی: <b>{guesses} حدس دیگر</b>",
        
        # Help message
        "help_title": "🎯 <b>بازی حدس تدریجی</b>",
        "how_to_play": "<b>نحوه بازی:</b>",
        "help_step1": "۱. یک عدد مخفی بین ۱ تا ۱۰,۰۰۰ انتخاب می‌شود",
        "help_step2": "۲. حدس خود را به صورت عدد در چت ارسال کنید",
        "help_step3": "۳. می‌توانید تا ۱۰ بار در هر دور حدس بزنید",
        "help_step4": "۴. ربات با پیام راهنما ⬆️ (بالاتر) یا ⬇️ (پایین‌تر) به هر حدس پاسخ می‌دهد",
        "help_step5": "۵. دورها ۲ دقیقه طول می‌کشند (حداقل ۱۰ حدس کل)",
        "help_step6": "۶. اولین نفری که درست حدس بزند، جایزه را می‌برد!",
        "loyalty_title": "<b>پاداش وفاداری:</b>",
        "loyalty_rule1": "• از دور ۱ شرکت کنید: ۱۰۰٪ پاداش",
        "loyalty_rule2": "• دور ۱ را از دست بدهید: ۷۵٪ پاداش",
        "loyalty_rule3": "• دورهای دیگر را از دست بدهید: ۱۵-٪ برای هر دور",
        "loyalty_rule4": "• حداقل: ۵۰٪ پاداش",
        "commands_title": "<b>دستورات:</b>",
        "cmd_start": "/start - نمایش این راهنما",
        "cmd_status": "/status - مشاهده وضعیت بازی فعلی",
        "cmd_newgame": "/newgame [جایزه] - (ادمین) شروع بازی جدید",
        "cmd_start_round": "/start_round - (ادمین) شروع دور جدید",
        "cmd_pause_round": "/pause_round - (ادمین) توقف دور فعلی",
        "cmd_resume_round": "/resume_round - (ادمین) ادامه دور متوقف شده",
        "cmd_close_round": "/close_round - (ادمین) بستن دور فعلی",
        "cmd_reveal": "/reveal - (ادمین) فاش کردن عدد مخفی",
        "cmd_cancel_game": "/cancel_game - (ادمین) لغو بازی",
        "cmd_post_cost": "/post_cost - (ادمین) ارسال راهنمای هزینه",
        "help_footer": "🎮 <i>عدد مخفی را حدس بزنید! یک برنده، hash منصفانه، و پاداش بیشتر هر چه بیشتر در بازی بمانید!</i>",
        
        # Manual reveal
        "reveal_title": "🔓 <b>بازی فاش شد</b>",
        "secret_was": "🎯 عدد مخفی: <b>{number}</b>",
        "no_winner": "این بار برنده‌ای نداشتیم. بازی بعدی شانس بیشتری داشته باشید! 🎮",
        
        # Cost hint
        "cost_hint_title": "💰 <b>هزینه دور {round}</b>",
        "cost_suggested": "پیشنهادی: <b>{cost} ⭐ ستاره</b>",
        "cost_warning": "⚠️ ادمین باید این را به صورت دستی در \"تنظیمات گروه ستاره‌دار\" تلگرام قبل از شروع دور تنظیم کند.",
        "newgame_usage": "⚠️ <b>مبلغ جایزه الزامی است!</b>\n\n<b>نحوه استفاده:</b>\n<code>/newgame [جایزه]</code>\nیا\n<code>/newgame [جایزه] | [اسپانسر] | [پیام_شروع] | [پیام_پایان]</code>\n\n<b>مثال‌ها:</b>\n• <code>/newgame 1000</code>\n• <code>/newgame 500 | TechCorp</code>\n• <code>/newgame 1000 | TechCorp | خوش آمدید! | متشکریم!</code>",
        
        # Admin messages
        "ask_stars_cost": "⭐ <b>هزینه ستاره برای دور {round} را وارد کنید</b>\n\nلطفا تعداد ستاره‌های مورد نیاز برای پست در این گروه را تایپ کنید.\nمثال‌ها: <code>۱</code>، <code>۴</code>، <code>۱۰</code> و غیره\n\nیا <code>/cancel</code> برای لغو ارسال کنید.",
        "input_cancelled": "❌ ورودی لغو شد.",
        "no_pending_input": "⚠️ ورودی در انتظاری وجود ندارد.",
        "invalid_stars_number": "⚠️ عدد نامعتبر. لطفا یک عدد معتبر برای ستاره‌ها تایپ کنید (مثلا ۱، ۴، ۱۰).",
        "stars_must_be_positive": "⚠️ هزینه ستاره باید یک عدد مثبت باشد. لطفا دوباره تلاش کنید.",
        "no_active_game_found": "⚠️ بازی فعالی پیدا نشد.",
        "round_started_success": "✅ دور {round} با هزینه {cost} ⭐ شروع شد",
        "round_started_log": "✅ دور {round} شروع شد",
        "round_paused_btn": "⏸ دور متوقف شد",
        "round_resumed_btn": "▶️ دور از سر گرفته شد",
        "round_closed_btn": "🔒 دور بسته شد",
        "game_revealed_btn": "🔓 بازی فاش شد",
        "game_canceled_btn": "❌ بازی لغو شد",
    }
    
    @staticmethod
    def get(key: str, lang: str = "en", **kwargs) -> str:
        """
        Get translated text for a given key.
        
        Args:
            key: Translation key
            lang: Language code ('en' or 'fa')
            **kwargs: Format parameters for the text
            
        Returns:
            Formatted translated text
        """
        translations = Translations.FA if lang == "fa" else Translations.EN
        text = translations.get(key, Translations.EN.get(key, f"[{key}]"))
        
        # Format with provided kwargs
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
