# Changes Applied - New Features

## Summary of Changes

All requested features have been successfully implemented:

### ✅ 1. Configurable Round Timer
- **Configuration**: Added `ROUND_DURATION_MINUTES` to `.env` (default: 2 minutes)
- **Smart Closing**: Rounds close after the timer expires, BUT only if at least 10 total guesses have been made
- **Auto-Extension**: If fewer than 10 guesses when timer expires, round stays open until 10th guess

### ✅ 2. Prize System
- **Database**: Added `prize_amount` field to `games` table
- **Command**: Use `/newgame [prize_amount]` to set prize (e.g., `/newgame 1000`)
- **Announcement**: Winner announcement now displays the prize amount won

### ✅ 3. Unlimited Total Guesses
- **Removed**: Old system that limited total guesses and gave hints every 10 guesses
- **New**: No limit on total guesses from all players combined
- **Per-Player Limit**: Still maintains 10 guesses per player per round

### ✅ 4. Reaction-Based Hints
- **Instant Feedback**: Bot reacts to EVERY guess message with:
  - 👍 if the secret number is **higher** than the guess
  - 👎 if the secret number is **lower** than the guess
- **Fallback**: If reactions fail, sends text hint instead

## Files Modified

### Core Logic
- `bot/config.py` - Added timer configuration
- `bot/storage/models.py` - Added prize_amount to Game model
- `bot/storage/db.py` - Updated database schema and operations
- `bot/services/game_engine.py` - Implemented timer logic with asyncio tasks

### Handlers
- `bot/handlers/admin.py` - Added prize parameter to /newgame command
- `bot/handlers/player.py` - Replaced text hints with reactions

### Services
- `bot/services/announcer.py` - Updated all messages to reflect new features

### Documentation
- `README.md` - Updated with all new features and examples
- `.env.example` - Added ROUND_DURATION_MINUTES

## How It Works

### Round Timer Flow
1. Admin starts round → Timer task starts (2 minutes)
2. Players send guesses → Bot reacts with 👍 or 👎
3. Timer expires after 2 minutes
4. If ≥10 guesses made → Round closes automatically
5. If <10 guesses → Round stays open, checks every 30 seconds
6. When 10th guess arrives → Round closes

### Prize Flow
1. Admin: `/newgame 1000` → Creates game with 1000 ⭐ prize
2. Game announcement shows: "💰 Prize: 1000 ⭐"
3. Players compete across rounds
4. Winner found → Announcement shows: "💰 Prize Won: 1000 ⭐"

### Reaction Flow
1. Player sends: "5000"
2. Secret number is 7500
3. Bot immediately reacts: 👍 (higher)
4. Player sends: "9000"
5. Bot immediately reacts: 👎 (lower)
6. Player sends: "7500"
7. Winner! No reaction, just announcement

## Usage Examples

### Starting a Game with Prize
```
Admin: /newgame 5000
Bot: 🎮 New Game Started!
     💰 Prize: 5000 ⭐
     [Hash displayed]
     [Start Round 1 button]
```

### Playing with Reactions
```
Player: 5000
Bot: [👍 reaction on message]

Player: 8000
Bot: [👎 reaction on message]

Player: 7500
Bot: 🎉 WE HAVE A WINNER! 🎉
     🏆 Winner: @player
     💰 Prize Won: 5000 ⭐
     [Full reveal with hash verification]
```

### Timer Behavior
```
3:00 PM - Round starts (2-minute timer)
3:01 PM - 5 guesses made
3:02 PM - Timer expires, but only 5 guesses → stays open
3:03 PM - 8 guesses now
3:04 PM - 10th guess arrives → Round auto-closes
```

## Configuration

Add to your `.env` file:
```bash
ROUND_DURATION_MINUTES=2  # Change to 3, 5, 10, etc.
```

The minimum guesses requirement (10) can be changed in `bot/config.py`:
```python
MIN_GUESSES_BEFORE_CLOSE = 10  # Change if needed
```

## Testing

To test the new features:

1. **Timer**: Set `ROUND_DURATION_MINUTES=1` in `.env` for faster testing
2. **Prize**: Try `/newgame 100` and verify it shows in announcements
3. **Reactions**: Send guesses and watch for 👍/👎 reactions
4. **Unlimited Guesses**: Have multiple players send many guesses (no total limit)

All features are production-ready! 🚀
