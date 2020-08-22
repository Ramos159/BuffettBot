import discord
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


@client.event
async def on_ready():
    handle_on_ready(client)


@client.event
async def on_message(client, message):
    handle_on_message(client, message)


"""These will be cogs i will impliment eventually"""
# cogs = [
#     'events',
#     'profile',
#     'quote',
#     'stock',
#     'crypto',
#     'portfolio',
#     'option'
# ]


client = discord.Client()
client.run(DISCORD_API_TOKEN)
