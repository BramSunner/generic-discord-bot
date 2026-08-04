import discord
from discord.ext import commands

import config



class AdminCog(commands.Cog, name = "Admin Commands"):
    """A cog for administrative commands."""

    def __init__(self, bot):
        self.bot = bot



    @commands.command(
        name = 'shutdown',
        description = 'Shuts down the bot.',
        help = '!shutdown | Shuts down the bot.',
        aliases = ['sd']
    )
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts down the bot."""
        await ctx.send("Shutting down...")
        await self.bot.close()

    @commands.command(
        name = 'load',
        description = 'Loads a cog.',
        help = '!load (cog name) | Loads a cog.',
        aliases = ['l']
    )
    @commands.is_owner()
    async def load(self, ctx, cog_name: str):
        """Loads a cog."""
        try:
            await self.bot.load_extension(f"{config.COGS_DIR}/{cog_name}")
            await ctx.send(f"Cog loaded: {cog_name}")
        except Exception as e:
            await ctx.send(f"Failed to load cog {cog_name}: {e}")

    @commands.command(
        name = 'unload',
        description = 'Unloads a cog.',
        help = '!unload (cog name) | Unloads a cog.',
        aliases = ['ul']
    )
    @commands.is_owner()
    async def unload(self, ctx, cog_name: str):
        """Unloads a cog."""
        try:
            await self.bot.unload_extension(f"{config.COGS_DIR}/{cog_name}")
            await ctx.send(f"Cog unloaded: {cog_name}")
        except Exception as e:
            await ctx.send(f"Failed to unload cog {cog_name}: {e}")

    @commands.command(
        name = 'reload',
        description = 'Reloads a cog.',
        help = '!reload (cog name) | Reloads a cog.',
        aliases = ['rl']
    )
    @commands.is_owner()
    async def reload(self, ctx, cog_name: str):
        """Reloads a cog."""
        try:
            await self.bot.reload_extension(f"{config.COGS_DIR}/{cog_name}")
            await ctx.send(f"Cog reloaded: {cog_name}")
        except Exception as e:
            await ctx.send(f"Failed to reload cog {cog_name}: {e}")



async def setup(bot):
    """Sets up the AdminCog."""
    await bot.add_cog(AdminCog(bot))

