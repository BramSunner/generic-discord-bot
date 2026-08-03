import discord
from discord.ext import commands




class UtilCog(commands.Cog, name="Utility Commands"):
    def __init__(self, bot):
        self.bot = bot




async def setup(bot):
    await bot.add_cog(UtilCog(bot))
    
