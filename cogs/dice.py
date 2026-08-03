import discord
from discord.ext import commands

from scripts import dice_util, text_util



class DiceCog(commands.Cog, name="Dice Commands"):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(
        name = 'roll',
        description = 'Rolls dice based on the provided request.',
        help = '!roll (dice roll request) | Example: !roll 2d6+3',
        aliases = ['r']
    )
    async def roll(self, ctx, *, request: str) -> None:
        """
        Rolls dice based on the provided request.
        Replies in a thread within the preferred channel for the guild.

        Parameters:
            ctx (commands.Context): The context of the command invocation.
            request (str): The dice roll request string.
        """
        embeds = dice_util.process_command(ctx.author, request)
        await text_util.reply_in_thread(ctx, "Roll Results", "m_embed", embeds) 



async def setup(bot):
    await bot.add_cog(DiceCog(bot))
