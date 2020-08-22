import discord
from discord.ext import commands
import logging
from handlers.client_event_handlers import handle_on_message, handle_on_ready
from settings import DISCORD_API_TOKEN

"""set up logger. maybe later ill find a way to send the logs as a message to a channel."""
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@bot.event
async def on_ready():
    handle_on_ready(bot)


def determine_prefix():
    """This will eventually use a database to get the guild prefix, for now we just use ?"""

    return '?'


"""These will be cogs i will impliment eventually"""
# cogs = [
# 'guild_logger'
#     'events',
#     'profile',
#     'quote',
#     'stock',
#     'crypto',
#     'portfolio',
#     'option'
# 'invite'
# ]

bot = commands.Bot(command_prefix=determine_prefix)
bot.run(DISCORD_API_TOKEN)
