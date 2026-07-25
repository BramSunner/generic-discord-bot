import discord
from discord import app_commands
from discord.ext import commands







class AdminCog(commands.Cog, name="Admin Commands"):
    def __init__(self, bot):
        self.bot = bot

    async def is_owner():
        def predicate(ctx):
            return ctx.bot.is_owner(ctx.author)
        return commands.check(predicate)


    # Reload command.
    @commands.command(
            name='reload',
            description='Reloads a specified cog.'
    )
    @commands.is_owner()
    async def reload(self, interaction: discord.Interaction, cog: str = None):
        """Reloads a specified cog if the user is the bot owner."""

        if cog is None:
            await interaction.response.send_message("Please specify a cog to reload. Example: !reload admin")
            return

        try:
            await self.bot.reload_extension(f'cogs.{cog}')
            await interaction.response.send_message(f"Successfully reloaded the '{cog}' cog.")
        except commands.ExtensionNotLoaded:
            await interaction.response.send_message(f"The '{cog}' cog is not loaded. Please load it first.")



    @commands.command(
            name='load',
            description='Loads a specified cog.'
    )
    async def load(self, interaction: discord.Interaction, cog: str = None):
        """Loads a specified cog if the user is the bot owner."""

        if cog is None:
            await interaction.response.send_message("Please specify a cog to load. Example: !load admin")
            return

        try:
            self.bot.load_extension(f'cogs.{cog}')
            await interaction.response.send_message(f"Successfully loaded the '{cog}' cog.")
        except commands.ExtensionAlreadyLoaded:
            await interaction.response.send_message(f"The '{cog}' cog is already loaded.")
        except commands.ExtensionNotFound:
            await interaction.response.send_message(f"The '{cog}' cog was not found. Please check the name and try again.")

    @app_commands.command(
            name='disconnect', 
            description='Disconnect the bot from the server.'
    )
    async def disconnect(self, interaction: discord.Interaction):
        """Disconnects the bot from the server if the user has administrator permissions."""

        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Disconnecting the bot...")
            await self.bot.close()

            print(f'{self.bot.user.name} has been disconnected from the server by {interaction.user.name}.')
        else:
            await interaction.response.send_message("You do not have permission to disconnect the bot.", ephemeral=True)


    @app_commands.command(
            name = 'ping',
            description = 'Check the bot\'s latency.'
    )
    async def ping(self, interaction: discord.Interaction):
        """Responds with the bot's latency in milliseconds."""

        latency = round(self.bot.latency * 1000)  # Converted to milliseconds
        await interaction.response.send_message(f"Pong! Latency: {latency}ms")



# Setup function to add the cog to the bot.
async def setup(bot):
    await bot.add_cog(AdminCog(bot))