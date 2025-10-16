# 🎯 Incremental Guess Game - Telegram Bot

A Telegram bot that runs a provably fair guessing game in group chats. Players compete to guess a secret number between 1 and 10,000, with loyalty rewards for consistent participation.

## 🌟 Features

- **Provably Fair**: Uses commit-reveal scheme with SHA256 hashing
- **Multi-Language Support**: Accepts English, Persian (۰-۹), and Arabic (٠-٩) numerals
- **Loyalty Rewards**: Players who join early and stay longer get bigger rewards
- **Round-Based Gameplay**: Multiple rounds with increasing difficulty/cost
- **Timed Rounds**: Each round lasts 2 minutes (configurable), but stays open until at least 10 guesses
- **Reaction Hints**: Bot reacts with 👍 (higher) or 👎 (lower) to each guess
- **Prize System**: Set a prize amount when creating the game
- **Sponsor System**: Optional sponsor with custom messages at round start/end
- **Unlimited Guesses**: No limit on total guesses (10 per player per round)
- **Admin Controls**: Full game management via inline keyboard buttons

## 📋 Game Rules

1. **Secret Number**: A random number between 1-10,000 is chosen and committed with a cryptographic hash
2. **Rounds**: Admin manually starts each round with increasing suggested costs (1⭐, 5⭐, 20⭐, etc.)
3. **Round Duration**: Each round lasts 2 minutes (configurable), but stays open until at least 10 total guesses are made
4. **Guessing**: Each player can make up to 10 guesses per round
5. **Instant Feedback**: Bot reacts to each guess with 👍 (number is higher) or 👎 (number is lower)
6. **Winner**: First player to guess correctly wins the prize
7. **Verification**: When revealed, the bot shows the number, salt, and hash verification ✅

## 🏆 Loyalty Reward Formula

Winners receive a percentage based on their participation:

```
P = max(50, 100 - (25 * missed_round1) - (15 * other_missed_rounds))
```

**Examples:**
- Joined from Round 1 and stayed: **100%**
- Missed Round 1: **75%**
- Missed Round 1 & Round 3: **60%**
- Joined only in Round 4: **50%** (minimum)

## 🚀 Setup Instructions

### Prerequisites

- Python 3.11 or higher
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Admin user IDs (your Telegram user ID)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   ```
   BOT_TOKEN=your_bot_token_here
   ADMIN_IDS=123456789,987654321
   ```

4. **Run the bot**
   ```bash
   python -m bot.main
   ```

### Finding Your Telegram User ID

1. Start a chat with [@userinfobot](https://t.me/userinfobot)
2. Send any message
3. Copy your user ID and add it to `ADMIN_IDS` in `.env`

## 🎮 How to Play

### For Admins

1. Add the bot to your Telegram group
2. Use `/newgame` to create a new game with optional parameters:
   - **Simple**: `/newgame 1000` (just prize)
   - **With Sponsor**: `/newgame 1000 | TechCorp | Welcome message | Closing message`
   - **Format**: `/newgame [prize] | [sponsor] | [start_msg] | [end_msg]`
3. The bot posts a commitment hash (provably fair!)
4. Click "▶️ Start Round 1" to begin
5. If sponsor is set, bot shows sponsor message at round start
6. Rounds automatically close after 2 minutes (if at least 10 guesses were made)
7. If sponsor is set, bot shows closing message at round end
8. Manage the game using inline keyboard buttons:
   - **Pause/Resume Round**: Temporarily stop accepting guesses
   - **Close Round**: End current round, start next one
   - **Reveal Number**: Manually end game and show answer
   - **Cancel Game**: Cancel and reset
   - **Post Cost Hint**: Show suggested star cost
   - **Show Status**: Display game statistics

### For Players

1. Use `/start` to see the rules
2. Send a number (1-10,000) to make a guess
3. You can use English (256), Persian (۲۵۶), or Arabic (٢٥٦) numerals
4. Watch for the bot's reaction:
   - 👍 = The secret number is higher
   - 👎 = The secret number is lower
5. First to guess correctly wins the prize! 🎉

### Commands

- `/start` - Show help and game rules
- `/status` - View current game status
- `/newgame [params]` - (Admin only) Start a new game
  - Format: `/newgame [prize] | [sponsor] | [start_msg] | [end_msg]`
  - Example: `/newgame 1000 | TechCorp | Welcome! | Thanks for playing!`

## 📁 Project Structure

```
bot/
├── main.py                 # Bot entry point
├── config.py              # Configuration and settings
├── handlers/
│   ├── admin.py          # Admin command handlers
│   ├── player.py         # Player guess handlers
│   └── common.py         # Common commands (/start, /status)
├── keyboards/
│   └── admin.py          # Admin inline keyboards
├── services/
│   ├── game_engine.py    # Core game logic
│   ├── commit_reveal.py  # Provably fair cryptography
│   ├── parsing.py        # Multi-language number parsing
│   ├── validators.py     # Input validation
│   └── announcer.py      # Message formatting
├── storage/
│   ├── db.py            # Database operations
│   └── models.py        # Data models
└── utils/
    └── logging.py       # Logging configuration
```

## 🧪 Testing Scenarios

### 1. Full Game Flow with Sponsor
1. `/newgame 500 | TechCorp | Try our new app! | Thanks for participating!`
2. Bot posts hash commitment, prize (500 ⭐), and sponsor (TechCorp)
3. Start Round 1 → Timer starts + "Try our new app!" shown
4. Players send 10+ guesses → Bot reacts with 👍 or 👎
5. Round auto-closes → "Thanks for participating!" shown
6. Someone guesses correctly → Winner announced with prize

### 2. Loyalty Calculation
- Player joins Round 1, 2, 4 (misses Round 3)
- Wins in Round 4
- Loyalty = `max(50, 100 - 0 - 15) = 85%`

### 3. Guess Limit
- Player sends 10 guesses in a round
- 11th guess → Rejected with message

### 4. Multi-Language
- Player sends: "256" ✅
- Player sends: "۲۵۶" ✅
- Player sends: "٢٥٦" ✅
- All parsed as 256, bot reacts with 👍 or 👎

### 5. Timer with Minimum Guesses
- Round starts at 3:00 PM (2-minute timer)
- Only 5 guesses made by 3:02 PM
- Round stays open until 10th guess
- 10th guess at 3:05 PM → Round closes

### 6. Reaction Hints
- Player guesses 5000, secret is 7500
- Bot reacts with 👍 (higher)
- Player guesses 9000
- Bot reacts with 👎 (lower)

### 7. Manual Reveal
- No winner after several rounds
- Admin clicks "Reveal Number"
- Game ends, number verified with hash

## 🔧 Configuration

Edit `.env` to customize:

```bash
# Bot Configuration
BOT_TOKEN=your_token_here
ADMIN_IDS=123456789,987654321

# Database
DATABASE_PATH=game_bot.db

# Game Settings
MIN_NUMBER=1
MAX_NUMBER=10000
ROUND_DURATION_MINUTES=2

# Logging
LOG_LEVEL=INFO
```

Round costs are configured in `bot/config.py`:
```python
ROUND_COSTS = {
    1: 1,
    2: 5,
    3: 20,
    4: 50,
    # ... add more
}
```

## 📊 Database Schema

The bot uses SQLite with four main tables:

- **games**: Game instances with commitment hash
- **rounds**: Individual rounds within games
- **guesses**: All player guesses
- **participations**: Tracks player participation per round

## 🎯 Pinned Group Message

Consider pinning this message in your group:

```
🎯 Guess the hidden number (1–10,000)! 
Bot reacts 👍 (higher) or 👎 (lower) to each guess.
Rounds last 2 minutes. One winner, fair hash, big prizes!

Use /start for rules | /status for current game info
```

## 🔒 Security & Fairness

- **Commit-Reveal Scheme**: The secret number is hashed with a random salt before the game starts
- **Hash Posted First**: Players can verify the game wasn't rigged
- **SHA256**: Cryptographically secure hashing
- **Verification**: On reveal, the bot proves the number matches the original hash

## 📝 License

This project is open source. Feel free to modify and use as needed.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 💡 Tips

- **Prize & Sponsor**: Set when creating the game:
  - Simple: `/newgame 1000` (just prize)
  - With sponsor: `/newgame 1000 | TechCorp | Welcome! | Goodbye!`
  - No sponsor: Messages won't be displayed if sponsor fields are empty
- **Round Timer**: Configurable in `.env` (default 2 minutes)
- **Minimum Guesses**: Rounds need at least 10 total guesses before timer can close them
- **Unlimited Guesses**: No limit on total guesses from all players combined
- **Reaction Hints**: Bot automatically reacts to every guess with 👍 or 👎
- **Star Costs**: The bot displays suggested costs but doesn't handle payments. Admins must manually configure star costs in Telegram's group settings.
- **Group Type**: Works best in supergroups
- **Admin Rights**: Bot needs permission to send messages and use inline keyboards
- **Performance**: Uses `uvloop` for better async performance (optional)

## 📞 Support

If you encounter issues:
1. Check the console logs for errors
2. Verify your `.env` configuration
3. Ensure the bot has proper permissions in the group
4. Check that your Python version is 3.11+

---

**Built with ❤️ using aiogram v3**

Enjoy your game! 🎮✨
