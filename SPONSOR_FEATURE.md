# Sponsor Feature Documentation

## Overview

The bot now supports optional sponsorship for games. Sponsors can display custom messages at the start and end of each round.

## Features

- ✅ Optional sponsor system (no sponsor = no messages displayed)
- ✅ Sponsor name displayed in game announcement
- ✅ Custom message at round start
- ✅ Custom message at round end
- ✅ All sponsor fields are optional

## Usage

### Creating a Game with Sponsor

Use the `/newgame` command with pipe-separated parameters:

```
/newgame [prize] | [sponsor_name] | [start_message] | [end_message]
```

### Examples

#### 1. No Sponsor (Simple Game)
```
/newgame 1000
```
Result: Prize only, no sponsor messages

#### 2. Full Sponsor Setup
```
/newgame 1000 | TechCorp | Welcome to our sponsored round! Check out techcorp.com | Thanks for playing! Visit us for more games!
```
Result:
- Game shows "Sponsored by: TechCorp"
- At round start: Shows "Welcome to our sponsored round! Check out techcorp.com"
- At round end: Shows "Thanks for playing! Visit us for more games!"

#### 3. Sponsor Messages Only (No Prize/Name)
```
/newgame | | Try our new app! | Thanks for participating!
```
Result: Messages shown but no prize or sponsor name

#### 4. Sponsor Name Only
```
/newgame 500 | CryptoCorp
```
Result: Shows "Sponsored by: CryptoCorp" but no custom messages

## Database Schema

Added three new fields to the `games` table:

```sql
sponsor_name TEXT
sponsor_start_message TEXT
sponsor_end_message TEXT
```

All fields are nullable (optional).

## Message Flow

### Game Creation
```
🎮 New Game Started!

🔒 Provably Fair Commitment
[hash]

💰 Prize: 1000 ⭐
🎗 Sponsored by: TechCorp

📋 Rules:
...
```

### Round Start
```
🔥 Round 1 Started!

💰 Suggested cost: 1 ⭐ Star(s)
⏱ Duration: 2 minutes (min 10 guesses)
🎯 Range: 1 - 10,000
📊 Limit: 10 guesses per player

Good luck! 🍀

📢 Sponsor Message:
Welcome to our sponsored round! Check out techcorp.com
```

### Round End
```
🔒 Round 1 Closed

No winner yet. Admin can start the next round.

📢 Sponsor Message:
Thanks for playing! Visit us for more games!
```

## Integration Points

### Files Modified

1. **bot/storage/models.py**
   - Added sponsor fields to Game model

2. **bot/storage/db.py**
   - Updated schema with sponsor columns
   - Modified create_game and _row_to_game methods

3. **bot/services/game_engine.py**
   - Updated create_game to accept sponsor parameters

4. **bot/services/announcer.py**
   - Updated game_created() to show sponsor name
   - Updated round_started() to show sponsor start message
   - Updated round_closed() to show sponsor end message

5. **bot/handlers/admin.py**
   - Updated /newgame command to parse sponsor parameters
   - Updated handlers to pass sponsor messages to announcer

## API

### Creating a Game with Sponsor

```python
game, target_hash = await engine.create_game(
    chat_id=12345,
    prize_amount=1000.0,
    sponsor_name="TechCorp",
    sponsor_start_message="Welcome to our sponsored round!",
    sponsor_end_message="Thanks for playing!"
)
```

### Announcer Methods

```python
# Game creation with sponsor
announcement = Announcer.game_created(
    target_hash="abc123...",
    prize_amount=1000.0,
    sponsor_name="TechCorp"
)

# Round start with sponsor message
announcement = Announcer.round_started(
    round_index=1,
    cost=1,
    duration_minutes=2,
    sponsor_message="Welcome message"
)

# Round close with sponsor message
announcement = Announcer.round_closed(
    round_index=1,
    sponsor_message="Closing message"
)
```

## Validation

- All sponsor fields are optional
- If sponsor_name is provided but messages are empty, only name is shown
- If messages are provided but no name, only messages are shown
- If all fields are None/empty, no sponsor-related content is displayed

## Testing

### Test Case 1: Full Sponsor
```
/newgame 1000 | TechCorp | Welcome! | Thanks!

Expected:
- Game shows sponsor name
- Round start shows welcome message
- Round end shows thanks message
```

### Test Case 2: No Sponsor
```
/newgame 1000

Expected:
- No sponsor name shown
- No messages at round start/end
```

### Test Case 3: Partial Sponsor
```
/newgame 1000 | TechCorp

Expected:
- Sponsor name shown
- No custom messages (only default round messages)
```

## Benefits

1. **Monetization**: Games can be sponsored by brands
2. **Engagement**: Custom messages can promote products/services
3. **Flexibility**: Completely optional - works without sponsors
4. **Professional**: Clean integration without cluttering non-sponsored games

## Future Enhancements

Potential additions:
- Sponsor logo/image support
- Click tracking for sponsor messages
- Multiple sponsors per game
- Sponsor message at winner announcement
- Different messages for different rounds
