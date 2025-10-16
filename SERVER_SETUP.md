# Server Setup Guide

## Quick Start (First Time Setup)

### 1. Clone the repository
```bash
cd ~
git clone https://github.com/Recoba86/Witamin-Game.git
cd Witamin-Game
```

### 2. Create virtual environment
```bash
python3 -m venv .venv
```

### 3. Activate virtual environment
```bash
source .venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure environment
```bash
cp .env.example .env
nano .env
```

Edit these values:
- `BOT_TOKEN` - Get from @BotFather on Telegram
- `ADMIN_IDS` - Your Telegram user ID (get from @userinfobot)

Example:
```bash
BOT_TOKEN=7123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw
ADMIN_IDS=123456789
```

### 6. Run the bot
```bash
python -m bot.main
```

## Using the Startup Script

Make the script executable (one time):
```bash
chmod +x start.sh
```

Run the bot:
```bash
./start.sh
```

## Running in Background (systemd)

Create a service file:
```bash
sudo nano /etc/systemd/system/witamin-bot.service
```

Add this content:
```ini
[Unit]
Description=Witamin Game Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Witamin-Game
ExecStart=/root/Witamin-Game/.venv/bin/python -m bot.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable witamin-bot
sudo systemctl start witamin-bot
```

Check status:
```bash
sudo systemctl status witamin-bot
```

View logs:
```bash
sudo journalctl -u witamin-bot -f
```

## Using Screen (Alternative to systemd)

Start in background:
```bash
screen -S witamin-bot
cd ~/Witamin-Game
source .venv/bin/activate
python -m bot.main
```

Detach: Press `Ctrl+A` then `D`

Reattach:
```bash
screen -r witamin-bot
```

List screens:
```bash
screen -ls
```

## Using tmux (Alternative)

Start session:
```bash
tmux new -s witamin-bot
cd ~/Witamin-Game
source .venv/bin/activate
python -m bot.main
```

Detach: Press `Ctrl+B` then `D`

Reattach:
```bash
tmux attach -t witamin-bot
```

## Updating the Bot

```bash
cd ~/Witamin-Game
git pull
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

Then restart the bot.

## Troubleshooting

### Module not found errors
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Permission errors
```bash
chmod +x start.sh
```

### Bot not starting
Check logs:
```bash
# If using systemd:
sudo journalctl -u witamin-bot -n 50

# If running manually:
python -m bot.main
```

### Database issues
Delete and recreate:
```bash
rm game_bot.db
python -m bot.main
```

## Environment Variables

All configuration is in `.env`:

```bash
# Required
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321

# Optional (defaults shown)
DATABASE_PATH=game_bot.db
MIN_NUMBER=1
MAX_NUMBER=10000
ROUND_DURATION_MINUTES=2
LOG_LEVEL=INFO
```

## Getting Your Telegram User ID

1. Open Telegram
2. Search for `@userinfobot`
3. Start the bot and send any message
4. It will reply with your user ID
5. Add this ID to `ADMIN_IDS` in `.env`

## Getting Bot Token

1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow instructions to create your bot
5. Copy the token
6. Add to `BOT_TOKEN` in `.env`

## File Permissions

Ensure these files are executable:
```bash
chmod +x start.sh
```

Ensure .env is readable:
```bash
chmod 600 .env
```

## Server Requirements

- Python 3.11 or higher
- 512MB RAM minimum (1GB recommended)
- 100MB disk space
- Internet connection

## First Run Checklist

- [ ] Python 3.11+ installed (`python3 --version`)
- [ ] Git installed (`git --version`)
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured with BOT_TOKEN
- [ ] `.env` file configured with ADMIN_IDS
- [ ] Bot token is valid
- [ ] Admin ID is correct
- [ ] Bot started successfully

## Support

If you encounter issues:
1. Check the logs
2. Verify `.env` configuration
3. Ensure all dependencies are installed
4. Check Python version (3.11+)
5. Verify bot token is valid
6. Confirm you have admin rights in the Telegram group
