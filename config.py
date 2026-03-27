"""
config.py — Bot configuration loader.

Reads settings from environment variables (or a .env file).
Add new configuration values here as the bot grows.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Core Discord settings
# ---------------------------------------------------------------------------

# Bot token obtained from the Discord Developer Portal.
# Set the DISCORD_BOT_TOKEN environment variable (or add it to a .env file).
BOT_TOKEN: str = os.environ.get("DISCORD_BOT_TOKEN", "")

# Command prefix used to trigger text commands (e.g. "!join").
COMMAND_PREFIX: str = os.environ.get("COMMAND_PREFIX", "!")
