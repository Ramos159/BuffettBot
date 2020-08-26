import os
from dotenv import load_dotenv

load_dotenv()

FINNHUB_TOKEN = os.getenv("FINMHUB_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_LOG_CHANNEL = os.getenv("GUILD_LOG_CHANNEL")
MEMBER_LOG_CHANNEL = os.getenv("MEMBER_LOG_CHANNEL")
BOT_LOG_CHANNEL = os.getenv("BOT_LOG_CHANNEL")
