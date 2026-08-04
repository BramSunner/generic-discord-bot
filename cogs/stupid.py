import discord
from discord.ext import commands

from scripts import text_util


class StupidCog(commands.Cog, name = "Stupid Commands"):
    """A cog for stupid commands."""

    def __init__(self, bot):
        self.bot = bot



    @commands.command(
        name = 'cum'
    )
    async def cum(self, ctx):
        """Replies with an idiotic message."""
        await text_util.msg_in_channel(ctx, "text", f"Here's that cum you wanted, {ctx.author.mention}.")



async def setup(bot):
    """Sets up the StupidCog."""
    await bot.add_cog(StupidCog(bot))