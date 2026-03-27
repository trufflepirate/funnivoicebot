"""
bot.py — Discord voice bot entry point.

Sets up the bot client, loads extension cogs, and starts the connection
to Discord. Run this file directly to start the bot:

    python bot.py

Make sure DISCORD_BOT_TOKEN is set in your environment or in a .env file.
"""

from __future__ import annotations

import asyncio
import sys

import discord
from discord.ext import commands

import config

# ---------------------------------------------------------------------------
# Bot factory
# ---------------------------------------------------------------------------

INITIAL_EXTENSIONS: list[str] = [
    "cogs.voice",
]


def create_bot() -> commands.Bot:
    """Create and configure the :class:`commands.Bot` instance.

    Intents are configured to allow the bot to read guild voice states,
    which is required for joining/leaving voice channels.
    """
    intents = discord.Intents.default()
    intents.voice_states = True
    intents.message_content = True

    bot = commands.Bot(
        command_prefix=config.COMMAND_PREFIX,
        intents=intents,
        description="A modular Discord voice bot.",
    )
    return bot


# ---------------------------------------------------------------------------
# Extension loader
# ---------------------------------------------------------------------------


async def load_extensions(bot: commands.Bot) -> None:
    """Load all cog extensions listed in ``INITIAL_EXTENSIONS``."""
    for extension in INITIAL_EXTENSIONS:
        await bot.load_extension(extension)


# ---------------------------------------------------------------------------
# Event handlers
# ---------------------------------------------------------------------------


def register_events(bot: commands.Bot) -> None:
    """Attach top-level event listeners to *bot*."""

    @bot.event
    async def on_ready() -> None:
        """Fired once the bot has connected to Discord and is ready."""
        print(f"Logged in as {bot.user} (ID: {bot.user.id})")
        print(f"Connected to {len(bot.guilds)} guild(s).")
        print("------")

    @bot.event
    async def on_disconnect() -> None:
        """Fired when the bot loses its connection to Discord."""
        print("Bot disconnected from Discord.")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


async def main() -> None:
    """Initialise and run the bot."""
    if not config.BOT_TOKEN:
        print(
            "Error: DISCORD_BOT_TOKEN is not set. "
            "Add it to your environment or .env file.",
            file=sys.stderr,
        )
        sys.exit(1)

    bot = create_bot()
    register_events(bot)

    async with bot:
        await load_extensions(bot)
        await bot.start(config.BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
