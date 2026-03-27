"""
cogs/voice.py — Voice channel management cog.

Handles connecting to and disconnecting from Discord voice channels.
Stub functions are provided for future streaming and Voice Activity
Detection (VAD) modules so that callers already have a stable interface
to build against.
"""

from __future__ import annotations

import discord
from discord.ext import commands


class VoiceCog(commands.Cog, name="Voice"):
    """Commands and helpers for voice-channel management."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ------------------------------------------------------------------
    # Public commands
    # ------------------------------------------------------------------

    @commands.command(name="join", help="Join the voice channel you are in.")
    async def join(self, ctx: commands.Context) -> None:
        """Connect the bot to the caller's current voice channel."""
        voice_client = await connect_to_voice_channel(ctx)
        if voice_client is not None:
            await ctx.send(f"Joined **{voice_client.channel.name}**.")

    @commands.command(name="leave", help="Leave the current voice channel.")
    async def leave(self, ctx: commands.Context) -> None:
        """Disconnect the bot from its current voice channel."""
        await disconnect_from_voice_channel(ctx)

    # ------------------------------------------------------------------
    # Lifecycle events
    # ------------------------------------------------------------------

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        """React to voice-state changes (e.g. auto-leave when channel empties).

        Full logic will be added in a future update.
        """
        pass


# ---------------------------------------------------------------------------
# Modular helper functions
# ---------------------------------------------------------------------------


async def connect_to_voice_channel(
    ctx: commands.Context,
) -> discord.VoiceClient | None:
    """Connect the bot to the voice channel the command author is in.

    Returns the :class:`discord.VoiceClient` on success, or ``None`` if
    the author is not in a voice channel.
    """
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("You must be in a voice channel first.")
        return None

    channel: discord.VoiceChannel = ctx.author.voice.channel

    # If already connected to a different channel, move; otherwise join.
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
        return ctx.voice_client

    return await channel.connect()


async def disconnect_from_voice_channel(ctx: commands.Context) -> None:
    """Disconnect the bot from whichever voice channel it is currently in."""
    if ctx.voice_client is None:
        await ctx.send("I am not in a voice channel.")
        return

    channel_name: str = ctx.voice_client.channel.name
    await ctx.voice_client.disconnect()
    await ctx.send(f"Left **{channel_name}**.")


# ---------------------------------------------------------------------------
# Stub functions — placeholders for future modules
# ---------------------------------------------------------------------------


def start_audio_stream(voice_client: discord.VoiceClient) -> None:
    """Begin streaming audio through *voice_client*.

    .. note::
        Not yet implemented. This stub defines the interface for the
        audio-streaming module that will be added in a future iteration.
    """
    raise NotImplementedError("Audio streaming is not yet implemented.")


def stop_audio_stream(voice_client: discord.VoiceClient) -> None:
    """Stop any active audio stream on *voice_client*.

    .. note::
        Not yet implemented. Counterpart to :func:`start_audio_stream`.
    """
    raise NotImplementedError("Audio streaming is not yet implemented.")


def handle_voice_activity(voice_client: discord.VoiceClient) -> None:
    """Process incoming voice activity from *voice_client*.

    .. note::
        Not yet implemented. This stub defines the interface for the
        Voice Activity Detection (VAD) module that will be added later.
    """
    raise NotImplementedError("Voice Activity Detection is not yet implemented.")


# ---------------------------------------------------------------------------
# Cog setup (required by discord.py extension loader)
# ---------------------------------------------------------------------------


async def setup(bot: commands.Bot) -> None:
    """Register :class:`VoiceCog` with *bot*."""
    await bot.add_cog(VoiceCog(bot))
