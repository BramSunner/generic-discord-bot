import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class GenericBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = "!", intents = intents)

    async def setup_hook(self):
        for cog in config.COGS_DIR.glob("*.py"):
            cog_name = cog.stem
            try:
                await self.load_extension(f"cogs.{cog_name}")
                print(f"Loaded cog: {cog_name}")
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")

        await self.tree.sync()
        print("Slash commands synced globally!")

bot = GenericBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    await bot.change_presence(activity = discord.CustomActivity(name = "/help"))

bot.run(config.DISCORD_TOKEN, log_handler = config.handler, log_level = config.logging.DEBUG)