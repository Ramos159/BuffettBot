import discord
import logging
import traceback
from peewee import SqliteDatabase
from discord.ext import commands
from settings import DISCORD_TOKEN
from models.models import GuildSetting


"""set up logger. maybe later ill find a way to send the logs as a message to a channel."""
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def determine_prefix(bot, message):
    """Self Explanitory"""
    guild_id = message.guild.id
    guild = GuildSetting.get(GuildSetting.discord_ID == guild_id)

    return guild.prefix


bot = commands.Bot(command_prefix=determine_prefix)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the tendies"))


"""These will be cogs i will impliment eventually"""
cogs = [
    'guild_logger',
    'config',
    #     'events',
    #     'profile',
    #     'quote',
    'stock',
    #     'crypto',
    #     'portfolio',
    #     'option'
    'info'
]

if __name__ == "__main__":

    for cog in cogs:
        try:
            bot.load_extension(f"cogs.{cog}")
            print(f"cog: {cog} added successfully")
        except Exception as error:
            print(f"Error loading Cog: {cog}")
            traceback.print_exception(type(error), error, error.__traceback__)

    bot.run(DISCORD_TOKEN, bot=True, reconnect=True)
