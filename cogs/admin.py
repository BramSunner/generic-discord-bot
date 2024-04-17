import os
from os import listdir
from os import path

import traceback

from asyncio import sleep

import discord
from discord.ext import commands

import settings


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_owner():
        def predicate(ctx):
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
        return commands.check(predicate)


    # .........
    @commands.command(
            name = 'reload',
            description = 'Description.',
            brief = 'Brief',
            help = 'Help.'
    )
    @commands.is_owner()
    async def reload(self, ctx, cog: str = None):
        # No COG specified. Reload all COGS.
        if cog is None:
            async with ctx.typing():
                embed = discord.Embed(
                    title = "Reloading...",
                    color = discord.Color(0x0197D4),
                    timestamp = ctx.message.created_at
                )

                for ext in listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            await self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            await self.bot.load_extension(f"cogs.{ext[:-3]}")

                            embed.add_field(name = f"Reloaded: `{ext}`", value = "", inline = False)

                        # Something went wrong. Let's handle that.
                        except Exception as e:
                            desired_trace = traceback.format_exc(limit = 100)

                            embed.add_field(name = f"Failed to reload: `{ext}`", value = desired_trace, inline = False)
                    
                    await sleep(0.5)
                
                await ctx.send(embed = embed)

        # Reload the specified COG.
        else:
            async with ctx.typing():
                embed = discord.Embed(
                    title = f"Reloading `{cog.lower()}`...",
                    color = discord.Color(0x0197D4),
                    timestamp = ctx.message.created_at
                )

                ext = f"{cog.lower()}.py"

                # File does not exist.
                if not path.exists(f"./cogs/{ext}"):
                    embed.add_field(name = f"Failed to !reload `{ext}`", value = f"`{ext}` does not exist.", inline = False)

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        await self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        await self.bot.load_extension(f"cogs.{ext[:-3]}")

                        embed.add_field(name = f"Reloaded: `{ext}`", value = "", inline = False)

                    # Something went wrong. Let's handle that.
                    except Exception as e:
                        desired_trace = traceback.format_exc(limit = 1)
                        embed.add_field(name = f"Failed to reload: `{ext}`", value = desired_trace, inline = False)

                await ctx.send(embed = embed)


    # ......... 
    @commands.command(
            name = 'load',
            description = 'Description.',
            brief = 'Brief',
            help = 'Help.'
    )
    @commands.is_owner()
    async def load(self, ctx, cog: str = None):
        # No COG specified. Load all COGS.
        if not cog:
            async with ctx.typing():
                embed = discord.Embed(
                    title = "Loading...",
                    color = discord.Color(0x0197D4),
                    timestamp = ctx.message.created_at
                )
        
                for ext in listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            await self.bot.load_extension(f"cogs.{ext[:-3]}")

                            embed.add_field(name = f"Loaded: `{ext}`", value = "", inline = False)

                        # Something went wrong. Let's handle that.
                        except Exception as e:
                            desired_trace = traceback.format_exc(limit = 1)
                            embed.add_field(name = f"Failed to load: `{ext}`", value = desired_trace, inline = False)
                    
                        await sleep(0.5)

                await ctx.send(embed = embed)

        # Load the specified COG.
        else:
            async with ctx.typing():
                embed = discord.Embed(
                    title = "Loading...",
                    color = discord.Color(0x0197D4),
                    timestamp = ctx.message.created_at
                )

                ext = f"{cog.lower()}.py"

                print(ext)

                # File does not exist.
                if not path.exists(f"./cogs/{ext}"):
                    embed.add_field(name = f"Failed to load `{ext}`", value = f"`{ext}` does not exist.", inline = False)

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        await self.bot.load_extension(f"cogs.{ext[:-3]}")

                        embed.add_field(name = f"Loaded: `{ext}`", value = "", inline = False)

                    # Something went wrong. Let's handle that.
                    except Exception as e:
                        desired_trace = traceback.format_exc(limit = 1)

                        embed.add_field(name = f"Failed to load: `{ext}`", value = desired_trace, inline = False)

                await ctx.send(embed = embed)
            
    @commands.command(
            name = 'unload',
            description = 'Description.',
            brief = 'Brief.',
            help = 'Help.'
    )
    @commands.is_owner()
    # Unload a specified COG or all COGS.
    async def unload(self, ctx, cog: str = None):
        if not cog:
            async with ctx.typing():
                embed = discord.Embed(
                    title = "Unloading...",
                    color = discord.Color(0x0197D4),
                    timestamp = ctx.message.created_at
                )

                for ext in listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            await self.bot.unload_extension(f"cogs.{ext[:-3]}")

                            embed.add_field(name = f"Unloaded: `{ext}`", value = "", inline = False)

                        except Exception as e:
                            desired_trace = traceback.format_exc()
                            embed.add_field(name = f"Failed to unload: `{ext}`", value = desired_trace, inline = False)

                        await sleep(0.5)

        else:
            async with ctx.typing():
                embed = discord.Embed(
                    title = "Unloading...",
                    color = discord.Color(0x0197D4),
                    timestamp = ctx.message.created_at
                )

                ext = f"{cog.lower()}.py"

                # Make sure that the file exists.
                if not path.exists(f".\cogs\{ext}"):
                    embed.add_field(name = f"Failed to unload: `{ext}`", value = f"`{ext}` does not exist.", inline = False)

                # Make sure the file is a python file that does not start with _
                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        await self.bot.unload_extension(f"cogs.{ext[:-3]}")

                        embed.add_field(name = f"Unloaded: `{ext}`", value = "", inline = False)

                    # Something went wrong. Let's handle that.            
                    except Exception as e:
                        desired_trace = traceback.format_exc()
                        embed.add_field(name = f"Failed to unload: `{ext}`", value = desired_trace, inline = False)
        
        await ctx.send(embed = embed)
        

                    

    # .........
    @commands.command(
            name = 'sync',
            description = 'Description',
            brief = 'Brief',
            help = 'Help'
    )
    @commands.is_owner()
    async def sync(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(
                title = "Syncing...",
                color = discord.Color(0x0197D4),
                timestamp = ctx.message.created_at
            )
            
            self.bot.tree.copy_global_to(guild = ctx.guild)
            await self.bot.tree.sync()

            embed.add_field(name = "Synced.", value = "", inline = False)

            await ctx.send(embed = embed)



    # ...
    # Catch an unauthorized user attempting to !sync
    @sync.error
    async def sync_error(self, ctx, e):
        if isinstance(e, commands.CommandError):
            await ctx.send(f"Permission denied because {e}")



# ...
async def setup(bot):
    await bot.add_cog(Admin(bot))
