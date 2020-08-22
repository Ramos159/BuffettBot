import discord
import logging
import traceback
from discord.ext import commands
# from handlers.client_event_handlers import handle_on_message, handle_on_ready
from settings import DISCORD_API_TOKEN

"""set up logger. maybe later ill find a way to send the logs as a message to a channel."""
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# @bot.event
# async def on_ready():
#     handle_on_ready(bot)


def determine_prefix():
    """This will eventually use a database to get the guild prefix, for now we just use ?"""

    return '?'


"""These will be cogs i will impliment eventually"""
cogs = [
    'cogs.guild_logger',
    #     'events',
    #     'profile',
    #     'quote',
    #     'stock',
    #     'crypto',
    #     'portfolio',
    #     'option'
    'cogs.invite'
]

if __name__ == "__main__":
    bot = commands.Bot(command_prefix=determine_prefix())

    for cog in cogs:
        # print(cog)
        try:
            bot.load_extension(cog)
            print("{} added successfully".format(cog))
        except Exception as error:
            print("Error loading Cog {}".format(cog))
            traceback.print_exception(type(error), error, error.__traceback__)

    bot.run(DISCORD_API_TOKEN, bot=True, reconnect=True)
