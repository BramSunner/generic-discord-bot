import discord
from discord.ext import commands
from discord import app_commands

from typing import List
import config
import asyncio

from scripts import text_util



class SoundCog(commands.Cog, name="Sound Commands"):
    def __init__(self, bot):
        self.bot = bot



    async def play_autocomplete(
            interaction: discord.Interaction,
            current: str
    ) -> List[app_commands.Choice[str]]:
        """Autocomplete function for the play command."""
        # Filter options based on user input (current).
        sound_choices = [sound.stem for sound in config.SOUNDS_DIR.glob("*.mp3")]
        filtered_choices = [c for c in sound_choices if current.lower() in c.lower()]
        return [app_commands.Choice(name = c, value = c) for c in filtered_choices[:15]] # Limit to 15 choices to avoid hitting Discord's limit.

    

    @app_commands.command(
            name = 'play',
    )
    @app_commands.autocomplete(sound_name = play_autocomplete)
    async def play(self, ctx, sound_name: str = None):
        if sound_name is None:
            await text_util.reply_in_channel(ctx, "text", "Use !slist to see the list of available sounds.")
            return

        sound_name = discord.utils.escape_mentions(sound_name)
        sound_name = sound_name.replace("`", "").replace("*", "").replace("/", "")
    
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is None:
            await text_util.reply_in_channel(ctx, "text", "You must be in a voice channel to use this command.")
            return
       
        if ctx.voice_client is None:
            await voice_channel.connect()

        elif ctx.voice_client.channel != voice_channel:
            await ctx.voice_client.move_to(voice_channel)

        # Define a callback function to handle the end of the audio playback.
        def disconnect_callback(error):
            if error:
                print(f"Player error: {error}")
            
            # Use asyncio to run the async disconnect coroutine from a sync function
            coro = ctx.voice_client.disconnect()
            fut = asyncio.run_coroutine_threadsafe(coro, ctx.bot.loop)
            try:
                fut.result()
            except Exception as e:
                print(f"Disconnect error: {e}")

        # Play the sound.
        sound_path = f'{config.SOUNDS_DIR}/{sound_name}.mp3'
        try:
            ctx.voice_client.play(discord.FFmpegPCMAudio(executable=config.FFMPEG_PATH, source=sound_path), after=disconnect_callback)
            await text_util.reply_in_channel(ctx, "text", f"Now playing: {sound_name}")
        except Exception as e:
            await text_util.reply_in_channel(ctx, "text", f"Error playing sound: {e}")



    @commands.command(
            name = 'slist',
            description = 'Lists all available sounds.'
    )
    async def slist(self, ctx):
        """Lists all available sounds in the sounds directory."""
        try: 
            sound_list = [sound.stem for sound in config.SOUNDS_DIR.glob("*.mp3")]
            await text_util.reply_in_channel(ctx, "text", f"Available sounds: {', '.join(sound_list)}") 

        except Exception as e:
            await text_util.reply_in_channel(ctx, "text", f"Error listing sounds: {e}") 

# Setup function to add the cog to the bot.
async def setup(bot):
        await bot.add_cog(SoundCog(bot))