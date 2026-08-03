import os
import pathlib
import logging
from dotenv import load_dotenv



# Load environment variables from .env file.
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Check if the DISCORD_TOKEN is set.
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is not set in the environment variables. Please check your .env file.")

# Base paths for the project.
BASE_DIR = pathlib.Path(__file__).parent
COGS_DIR = BASE_DIR / "cogs"
PREF_CHANNEL_PATH = BASE_DIR / "res" / "preferred_channels.txt"
FFMPEG_PATH = BASE_DIR / "res" / "ffmpeg" / "bin" / "ffmpeg.exe"
SOUNDS_DIR = BASE_DIR / "res" / "sounds"

# Set up logging configuration.
handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')