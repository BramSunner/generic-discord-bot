import settings
import discord
from discord import app_commands
from discord.ext import commands

import typing

logger = settings.logging.getLogger("bot")

async def is_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)

def run():
    intents = discord.Intents.all()
    # intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        await bot.tree.sync()
        print("Synced.")

        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                print(cog_file)
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")

        print("...")

    @bot.command(
            name = 'owner',
            aliases = ['own']
    )
    @commands.is_owner()
    async def owner(ctx):
        await ctx.send(f"{ctx.author.mention} is the owner!")

    @owner.error
    async def owner_error(ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f"{ctx.author} is not allowed to use that command.")

    @bot.tree.context_menu(name = "slap")
    async def slap(interaction: discord.Interaction, member: discord.Member):
        if (interaction.user == member or member == None):
            await interaction.response.send_message(f"{interaction.user.mention} slapped themselves!")
        else:
            await interaction.response.send_message(f"{interaction.user.mention} slapped {member.mention}!")

    bot.run(settings.DISCORD_API_SECRET, root_logger = True)

if __name__ == "__main__":
    run()