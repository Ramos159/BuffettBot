import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
GUILD_LOG_CHANNEL = os.getenv("GUILD_LOG_CHANNEL")
MEMBER_LOG_CHANNEL = os.getenv("MEMBER_LOG_CHANNEL")
BOT_LOG_CHANNEL = os.getenv("BOT_LOG_CHANNEL")
