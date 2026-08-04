import discord
from discord.ext import commands

from scripts import text_util



class ErrorHandler(commands.Cog, name = "Error Handler"):
    """A cog for handling errors in the bot."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Handles errors that occur during command execution."""

        # Command was not found.
        if isinstance(error, commands.CommandNotFound):
            # await ctx.send("Command not found. Please check your input.")
            await text_util.msg_in_channel(ctx, "text", "Command not found. Please check your input.")
            pass

        # Command was invoked with missing required arguments.
        elif isinstance(error, commands.MissingRequiredArgument):
            # await ctx.send("Missing required argument. Please check the command usage.")
            await text_util.msg_in_channel(ctx, "text", "Missing required argument. Please check the command usage.")
            pass

        # Command was invoked with an invalid argument type.
        elif isinstance(error, commands.BadArgument):
            # await ctx.send("Bad argument provided. Please check the command usage.")
            await text_util.msg_in_channel(ctx, "text", "Bad argument provided. Please check the command usage.")
            pass

        # Couldn't figure out what went wrong with the command.
        else:
            # await ctx.send("An unexpected error occurred. Please try again later.")
            await text_util.msg_in_channel(ctx, "text", "An unexpected error occurred. Please try again later.")
            raise error  # Re-raise the error for logging purposes



async def setup(bot):
    """Sets up the ErrorHandler cog."""
    await bot.add_cog(ErrorHandler(bot))   