import discord
from discord.ext import commands
import settings
...

class SoundCog(commands.Cog, name="Sound Commands"):
    def __init__(self, bot):
        self.bot = bot

    # Play command.
    @commands.command(
            name='play',
            description='Plays a specified sound in the voice channel.',
    )
    async def play(self, interaction: discord.Interaction, sound_name: str = None):
        if sound_name is None:
            await interaction.response.send_message("Please specify a sound to play. Example: !play sound_name") # NO. Change this to list sounds, or provide a command to list sounds.

        else:
            voice_channel = interaction.user.voice.channel if interaction.user.voice else None
            if voice_channel is None:
                await interaction.response.send_message("You must be in a voice channel to use this command.")
                return
            else:
                if interaction.client.voice_clients is None:
                    await interaction.response.send_message("Connecting to your voice channel...")
                    await voice_channel.connect()
                elif interaction.client.voice_clients.channel != voice_channel:
                    await interaction.client.voice_clients.move_to(voice_channel)

                # Play the sound.
                sound_path = f'{settings.SOUNDS_DIR}/{sound_name}.mp3'
                try:
                    interaction.client.voice_clients.play(discord.FFmpegPCMAudio(executable='', source=sound_path), after=lambda e: print(f'Finished playing: {e}'))
                    await interaction.response.send_message(f"Now playing: {sound_name}")
                except Exception as e:
                    await interaction.response.send_message(f"Error playing sound: {e}")






# Setup function to add the cog to the bot.
async def setup(bot):
        await bot.add_cog(SoundCog(bot))