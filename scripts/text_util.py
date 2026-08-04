import discord

import config


def sanitize(input: str) -> str:
    sanitized_input = input.replace()
    return sanitized_input



async def msg_in_channel(ctx, message_type: str, message) -> None:
    """
    Replies to a message in the preferred channel for the guild.
    If the preferred channel does not exist, it raises a ValueError.

    Parameters:
        ctx (commands.Context): The context of the command invocation.
        message_type (str): The type of message being sent.
        message: The content of the message(s). 

    Raises:
        ValueError: If the preferred channel is not found or the file does not exist.
    """
    try:
        channel = get_channel(ctx)
    except ValueError as e:
        await ctx.reply(f"Error: {e}. Please ask an admin to set a preferred channel first.", delete_after = 10)
        await ctx.message.delete()
        return

    match(message_type):
        case "text":
            await channel.send(message)

        case "m_text":
            for msg in message:
                await channel.send(msg)

        case "embed":
            await channel.send(embed = message)

        case "m_embed":
            for msg in message:
                await channel.send(embed = msg)

    if ctx.channel != channel:
        await ctx.message.delete()
        await ctx.reply(f"Psst... use the preferred channel for commands next time!")



async def msg_in_thread(ctx, thread_title: str, message_type: str, message) -> None:
    """
    Replies to a message in a thread within the preferred channel for the guild.
    If the preferred channel does not exist, it raises a ValueError.
    If the thread does not exist, it creates a new thread and replies in it.

    Parameters:
        ctx (commands.Context): The context of the command invocation.
        thread_title (str): The title of the thread.
        message_type (str): The type of message being sent.
        message: The content of the message(s). 

    Raises:
        ValueError: If the preferred channel is not found or the file does not exist.
    """
    try:
        channel = get_channel(ctx)
    except ValueError as e:
        await ctx.reply(f"Error: {e}. Please ask an admin to set a preferred channel first.", delete_after = 10)
        await ctx.message.delete()
        return

    thread = await get_thread(channel, thread_title)

    match(message_type):
        case "text":
            await thread.send(message)

        case "m_text":
            for msg in message:
                await thread.send(msg)

        case "embed":
            await thread.send(embed = message)

        case "m_embed":
            for msg in message:
                await thread.send(embed = msg)

    # Light reminder to use the preferred channel for commands if the command was invoked in a different channel.
    if ctx.channel != channel:
        await ctx.message.delete()
        await ctx.reply(f"Psst... use the preferred channel for commands next time!")



async def get_channel(ctx) -> discord.TextChannel:
    """
    Retrieves the preferred channel for the guild from file.

    Parameters:
        ctx (commands.Context): The context of the command invocation.
    
    Returns:
        discord.TextChannel: The preferred text channel for the guild.
    
    Raises:
        ValueError: If the preferred channel is not found or the file does not exist.

    """
    try:
        with open(config.PREF_CHANNEL_PATH, "r") as f:
            for line in f:
                if line.startswith(f"{ctx.guild.id}:"):
                    channel_id = int(line.split(":")[1].strip())
                    channel = ctx.guild.get_channel(channel_id)
                    if channel is None:
                        raise ValueError(f"Channel with ID {channel_id} not found in guild {ctx.guild.name}.")
                    return channel
    except FileNotFoundError:
        raise ValueError("Preferred channel file not found. Please set a preferred channel first.")
    
    return None # Return None if no preferred channel is set for the guild.



async def get_thread(channel: discord.TextChannel, thread_title: str, auto_archive_duration: int = 60) -> discord.Thread:
    """
    Retrieves an existing thread or creates a new one in the specified channel.

    Parameters:
        channel (discord.TextChannel): The text channel in which to search for or create the thread.
        thread_title (str): The title of the thread.
        auto_archive_duration (int): The duration in minutes after which the thread will automatically archive. Default is 60 minutes.
        
    Returns:
        discord.Thread: The newly created thread.
    """
    # Search for an existing thread with the specified title.
    for thread in channel.threads:
        if thread.name == thread_title:
            thread.edit(
                auto_archive_duration = auto_archive_duration,
                locked = True
            ) 
            return thread

    # If no existing thread is found, create a new one.
    thread = await channel.create_thread(
        name = thread_title, 
        auto_archive_duration = auto_archive_duration,
        locked = True
    )
    return thread

