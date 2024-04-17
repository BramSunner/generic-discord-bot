import random

import discord
from discord.ext import commands



class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(
        name = 'roll',
        aliases = ['r'],
        help = '!r 2d4+2 | !r d8+2 2d12+4 8d6+4',
        description = "Roll a die or dice.\nAccepted dice are: d100 d20 d12 d10 d8 d6 d4 d1\nAdd a number preceeding the 'die' for the amount of times to roll it (up to 100 per command).\nAdd a number after to use a modifier from -1000 to +1000",
        brief = '!r (#)(die)(modifier) ...',
        enabled = True
    )
    async def roll(self, ctx, *args):
        embed = discord.Embed(title = ctx.author.name + ' rolled...', description = '', color = discord.Color(0x0197D4))

        for cmd in args:
            
            cmd = cmd.lower()
            die = ""
            mod = 0
            amt = 1
            total = 0
            rlist = []

        # ...
        # Check to see if the command has a single 'd' in it.
        # If not: the command is skipped.
            if cmd.count('d') != 1:
                embed.add_field(name = 'Error: invalid command.', value = 'We skipped *`' + cmd + '`*.', inline = False)
                continue

            # ... 
            # Continue processing command.
            else:
                # ...
                # Check to see if a positive modifier is in use.
                if '+' in cmd:
                    # ...
                    # Check to see if the modifier is in the correct position within the command.
                    # If not: the command is skipped.
                    if cmd.find('+') < cmd.find('d'):
                        embed.add_field(name = 'Error: that \'+\' is in the wrong place.', value = 'We skipped *`' + cmd + '`*.', inline = False)
                        continue
                    
                    # ...
                    # There is a '+' modifier in the right place: continue.
                    else:
                        # ...
                        # Attempt to extract the modifier as an int and place it in our 'mod' variable.
                        try:
                            mod = int(cmd[cmd.find('+'):])
                        # ... 
                        # Catch an incorrect value given and skip the command.
                        except ValueError:
                            embed.add_field(name = 'Error: invalid modifier.', value = 'We skipped *`' + cmd + '`*.', inline = False)
                            continue

                        # ...
                        # Catch an error resulting from overloading the embed with characters.
                        # Set a limit of 1000 for the modifier on each roll.
                        # Note: this limit might be too high... needs further testing.
                        if mod > 1000:
                            embed.add_field(name = "Error: that modifier is a little too high.", value = "We skipped *`" + cmd + "`*.", inline = False)
                            continue

                # ...
                # Check to see if a negative modifier is in use.
                elif '-' in cmd:
                    # ...
                    # Check to see if the modifier is in the correct position within the command.
                    # If not: the command is skipped.
                    if cmd.find('-') < cmd.find('d'):
                        embed.add_field(name = 'Error: that \'-\' is in the wrong place.', value = 'We skipped *`' + cmd + '`*.', inline = False)
                        continue
                    # ...
                    # There is a negative modifier in the right place: continue.
                    else:
                        # ...
                        # Attempt to extract the modifier as an int and place it in our 'mod' variable.
                        try:
                            mod = int(cmd[cmd.find('-'):])
                        # ...
                        # Catch an incorrect value given and skip the command.
                        except ValueError:
                            embed.add_field(name = 'Error: invalid modifier.', value = 'We skipped *`' + cmd + '`*.', inline = False)
                            continue

                        # ...
                        # Catch an error resulting from overloading the embed with characters.
                        # Set a limit of -1000 for the modifier on each roll.
                        # Note: this limit might to be too high... needs further testing.
                        if mod < -1000:
                            embed.add_field(name = "Error: that modifier is a little too low.", value = "We skipped *`" + cmd + "`*.", inline = False)
                            continue
                
                # ...
                # Find and extract the 'die' variable to be used while rolling.
                # Note: if adding further dice... largest amt of characters should be higher on list to avoid issues.
                # Example: 'd100' and 'd10'... if 'd10' is first in list then 'd100' would never be selected when used.
                #           - This shouldn't be all that relevant for further dice additions since those will be non-numerical or joke dice.
                #           - We have covered most of the regular dice with the current list.
                if 'd100' in cmd:
                    die = 'd100'
                
                elif 'd20' in cmd:
                    die = 'd20'
                
                elif 'd12' in cmd:
                    die = 'd12'

                elif 'd10' in cmd:
                    die = 'd10'

                elif 'd8' in cmd:
                    die = 'd8'

                elif 'd6' in cmd:
                    die = 'd6'

                elif 'd4' in cmd:
                    die = 'd4'

                elif 'd2' in cmd:
                    die = 'd2'

                else:
                    embed.add_field(name = "Error: that\'s not a real die.", value = "We skipped *`" + cmd + "`*.", inline = False)
                    continue

                # ...
                # Get the amount of dice to be rolled.
                # Note: we will have to add some error stopping for this.
                if cmd.index('d') > 0:
                    try:
                        amt = int(cmd[:cmd.index('d')])

                    # ...   
                    # Catch a ValueError resulting from an input containing a character other than a number.
                    # Ex: 1ed10+2 | 1&d4+4
                    except Exception as e:
                        embed.add_field(name = "Error: that\'s not a real amount of dice to roll.", value = "We skipped *`" + cmd + "`*.", inline = False)
                        continue

                    # ...
                    # Catch an error resulting from overloading the embed with characters.
                    # Set a limit of 100 dice rolls on an individual command.
                    # Note: this limit might be too high... needs further testing.
                    if amt > 100:
                        embed.add_field(name = "Error: that\'s a lot of dice!", value = "We skipped *`" + cmd + "`*.", inline = False)
                        continue

                for i in range(amt):
                    max = int(die[die.index('d') + 1:])
                    result = random.randint(1, max)

                    # ...
                    # Make critical success bold and append to the roll list to be added to embed.
                    if result == max:  
                        # ...
                        # Set the correct '+' or '-' for the modifier so it doesn't look weird in the embed.
                        if mod >= 0:
                            rlist.append('**' + str(result) + '+' + str(mod) + '**')
                        elif mod < 0:
                            rlist.append('**' + str(result) + str(mod) + '**')

                        result = result + mod
                        total = total + result

                    # ...
                    # Append the normal rolls to the roll list to be added to embed.
                    else:
                        # ...
                        # Set the correct '+' or '-' for the modifier so it doesn't look weird in the embed.
                        if mod >= 0:
                            rlist.append(str(result) + '+' + str(mod))
                        elif mod < 0:
                            rlist.append(str(result) + str(mod))
                        
                        result = result + mod
                        total = total + result
                
                rlist.append('(**' + str(total) + '**)')
            
                embed.add_field(name = str(die) + ' ' + str(mod) if mod < 0 else str(die) + '+' + str(mod) + ' x' + str(amt), value = '_' + str(rlist).translate(str.maketrans({"'" : None, "]" : None, "[" : None})) + '_', inline = False)

        await ctx.message.delete()

        # ...
        # Create a mechanism to send to a DM channel.
        if ctx.channel is discord.channel.DMChannel:
            await ctx.author.send(embed = embed)
            await ctx.message.delete(delay = 120.0)

        # ...
        # Command was sent in a regular text channel.
        else:
            await ctx.send(embed = embed, delete_after = 120.0)
            await ctx.message.delete(delay = 120.0)


async def setup(bot):
    await bot.add_cog(Dice(bot))