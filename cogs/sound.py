import discord
from discord.ext import commands
from discord import app_commands

from typing import List
import config
import asyncio

from scripts import text_util

class SoundCog(commands.Cog, name = "Sound Commands"):
    def __init__(self, bot):
        self.bot = bot

    async def play_autocomplete(
            self,
            interaction: discord.Interaction,
            current: str
    ) -> List[app_commands.Choice[str]]:
        """Autocomplete function for the play command."""
        sound_choices = [sound.stem for sound in config.SOUNDS_DIR.glob("*.mp3")]
        filtered_choices = [c for c in sound_choices if current.lower() in c.lower()]
        return [app_commands.Choice(name=c, value=c) for c in filtered_choices[:15]]

    @app_commands.command(
        name = 'play',
        description = 'Plays a sound in your voice channel'
    )
    @app_commands.autocomplete(sound_name = play_autocomplete)
    async def play(self, interaction: discord.Interaction, sound_name: str = None):
        # 1. Defer the interaction immediately to prevent 3-second timeout errors
        await interaction.response.defer(thinking = True)

        ctx = await commands.Context.from_interaction(interaction)

        if sound_name is None:
            # Note: You may need to update text_util to accept 'interaction' instead of 'ctx'
            await interaction.followup.send("Use /slist to see the list of available sounds.", ephemeral = True)
            return

        sound_name = discord.utils.escape_mentions(sound_name)
        sound_name = sound_name.replace("`", "").replace("*", "").replace("/", "")
    
        # 2. Fix context fetching: Use interaction.user instead of ctx.user
        voice_channel = interaction.user.voice.channel if interaction.user.voice else None

        if voice_channel is None:
            await interaction.followup.send("You must be in a voice channel to use this command.", ephemeral = True)
            return

        # 3. Fix voice client fetching: Use interaction.guild.voice_client
        voice_client = interaction.guild.voice_client

        # 4. Handle connection logic (Connect if completely disconnected, move if already in another channel)
        if voice_client is None:
            voice_client = await voice_channel.connect()
        elif voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)

        # Define a callback function to handle the end of the audio playback.
        def disconnect_callback(error):
            if error:
                print(f"Player error: {error}")
            
            # Use the guild voice client we fetched earlier
            coro = voice_client.disconnect()
            fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                fut.result()
            except Exception as e:
                print(f"Disconnect error: {e}")

        # 5. Wait a moment for the voice client connection to stabilize.
        await asyncio.sleep(1)

        # 6. Play the sound.
        sound_path = f'{config.SOUNDS_DIR}/{sound_name}.mp3'
        try:
            voice_client.play(
                discord.FFmpegPCMAudio(executable=config.FFMPEG_PATH, source=sound_path), 
                after=disconnect_callback
            )
            await interaction.followup.send(f"Now playing: {sound_name}", ephemeral = True)
            
        except Exception as e:
            await interaction.followup.send(f"Error playing sound: {sound_name} because {e}", ephemeral = True)
            pass

        await interaction.followup.send(f"Now playing: {sound_name}", ephemeral = True)



    @commands.command(
            name = 'slist',
            description = 'Lists all available sounds.'
    )
    async def slist(self, ctx):
        """Lists all available sounds in the sounds directory."""
        try: 
            sound_list = [sound.stem for sound in config.SOUNDS_DIR.glob("*.mp3")]
            await text_util.msg_in_channel(ctx, "text", f"Available sounds: {', '.join(sound_list)}") 

        except Exception as e:
            await text_util.msg_in_channel(ctx, "text", f"Error listing sounds: {e}") 

# Setup function to add the cog to the bot.
async def setup(bot):
    await bot.add_cog(SoundCog(bot))










# OLD 


# import discord
# from discord.ext import commands
# from discord import app_commands

# from typing import List
# import config
# import asyncio

# from scripts import text_util



# class SoundCog(commands.Cog, name="Sound Commands"):
#     def __init__(self, bot):
#         self.bot = bot



#     async def play_autocomplete(
#             self,
#             interaction: discord.Interaction,
#             current: str
#     ) -> List[app_commands.Choice[str]]:
#         """Autocomplete function for the play command."""
#         # Filter options based on user input (current).
#         sound_choices = [sound.stem for sound in config.SOUNDS_DIR.glob("*.mp3")]
#         filtered_choices = [c for c in sound_choices if current.lower() in c.lower()]
#         return [app_commands.Choice(name = c, value = c) for c in filtered_choices[:15]] # Limit to 15 choices to avoid hitting Discord's limit.

    

#     @app_commands.command(
#             name = 'play',
#     )
#     @app_commands.autocomplete(sound_name = play_autocomplete)
#     async def play(self, interaction: discord.Interaction, sound_name: str = None):
#         if sound_name is None:
#             await text_util.msg_in_channel(ctx, "text", "Use !slist to see the list of available sounds.")
#             return

#         sound_name = discord.utils.escape_mentions(sound_name)
#         sound_name = sound_name.replace("`", "").replace("*", "").replace("/", "")
    
#         voice_channel = ctx.user.voice.channel if ctx.user.voice else None

#         if voice_channel is None:
#             await text_util.msg_in_channel(ctx, "text", "You must be in a voice channel to use this command.")
#             return


#         elif ctx.voice_client.channel != voice_channel:
#             await ctx.voice_client.move_to(voice_channel)

#         # Define a callback function to handle the end of the audio playback.
#         def disconnect_callback(error):
#             if error:
#                 print(f"Player error: {error}")
            
#             # Use asyncio to run the async disconnect coroutine from a sync function
#             coro = ctx.voice_client.disconnect()
#             fut = asyncio.run_coroutine_threadsafe(coro, ctx.bot.loop)
#             try:
#                 fut.result()
#             except Exception as e:
#                 print(f"Disconnect error: {e}")

#         # Play the sound.
#         sound_path = f'{config.SOUNDS_DIR}/{sound_name}.mp3'
#         try:
#             ctx.voice_client.play(discord.FFmpegPCMAudio(executable=config.FFMPEG_PATH, source=sound_path), after=disconnect_callback)
#             await text_util.msg_in_channel(ctx, "text", f"Now playing: {sound_name}")
#         except Exception as e:
#             await text_util.msg_in_channel(ctx, "text", f"Error playing sound: {e})



#     @commands.command(
#             name = 'slist',
#             description = 'Lists all available sounds.'
#     )
#     async def slist(self, ctx):
#         """Lists all available sounds in the sounds directory."""
#         try: 
#             sound_list = [sound.stem for sound in config.SOUNDS_DIR.glob("*.mp3")]
#             await text_util.msg_in_channel(ctx, "text", f"Available sounds: {', '.join(sound_list)}") 

#         except Exception as e:
#             await text_util.msg_in_channel(ctx, "text", f"Error listing sounds: {e}") 

# Setup function to add the cog to the bot.
# async def setup(bot):
#         await bot.add_cog(SoundCog(bot))