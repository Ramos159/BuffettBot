import discord
from discord.ext import commands
from datetime import datetime
from models import GuildSetting, Guild
# from random import randint
from settings import GUILD_LOG_CHANNEL


class GuildLogger(commands.Cog):
    """
    Guild Logger Module

    Tracks what servers the bot leaves and joins

    Sends embeds into special channels on leaves and joins

    Inherits from the Cog class, this is required by the library

    ...

    Attributes
    ----------
    bot : commands.Bot
        Bot instance from main.py

    guild_log : int
        number id for guild log channel
    """

    def __init__(self, bot):
        self.bot = bot
        self.guild_log = int(GUILD_LOG_CHANNEL)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        Fired when the bot joins a guild.

        Creates a record of Guild Settings if one doesnt exist for the guild

        Params
        ------
        guild : Guild
            Guild or "Server" that which the bot joined

        Returns
        -------
        None
            The bot will simply send an embed to the guild log channel
        """

        new_guild = Guild.get_or_none(Guild.discord_id == guild.id)

        if new_guild is None:
            new_guild = Guild.create(discord_id=guild.id)
            GuildSetting.create(guild=new_guild)

        channel = self.bot.get_channel(self.guild_log)
        await channel.send(embed=self.guild_join_embed(guild))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """
        Fired when the bot leaves a guild

        ...

        Params
        ------
        guild : Guild
            Guild or "Server" that which the bot joined

        Returns
        -------
        None
            The bot will simply send an embed to the guild log channel
        """

        channel = self.bot.get_channel(self.guild_log)
        await channel.send(embed=self.guild_remove_embed(guild))

    def get_current_date_time(self):
        """
        Makes a string from the current time and date\n
        Uses the datetime module

        ...

        Return
        ------
        str 
            This will be a string in the format of m/d/y h:m using current time
        """
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %H:%M")
        return dt_string

    def guild_join_embed(self, guild):
        """
        Makes an embed for the guild log on join

        ...

        Params
        ------
        guild : Guild
            Guild or "Server" that which the bot joined

        Returns
        -------
        Embed
            Discord rich embed with information regarding the guild joined
        """

        embed = discord.Embed()
        embed.color = discord.Color.green()
        embed.title = "Guild Join"
        embed.type = "rich"
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Server Name", value=guild.name)
        embed.add_field(name="Server Description", value=guild.description)
        embed.add_field(name="Region", value=guild.region)
        embed.add_field(name="ID", value=guild.id)
        embed.set_footer(text=self.get_current_date_time())
        return embed

    def guild_remove_embed(self, guild):
        """
        Makes an embed for the guild log on leave

        ...

        Params
        ------
        guild : Guild
            Guild or "Server" that which the bot left

        Returns
        -------
        Embed
            Discord rich embed with information regarding the guild left
        """

        embed = discord.Embed()
        embed.color = discord.Color.red()
        embed.title = "Guild Leave"
        embed.type = "rich"
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Server Name", value=guild.name)
        embed.add_field(name="Server Description", value=guild.description)
        embed.add_field(name="Region", value=guild.region)
        embed.add_field(name="ID", value=guild.id)
        embed.set_footer(text=self.get_current_date_time())
        return embed

    async def create_bot_log(self, guild, err):
        """Creates an embed with details concerning an err and sends it to the log channel."""
        channel = self.bot.get_channel(self.guild_log)

        embed = discord.Embed()
        embed.title = "Error Log"
        embed.description = str(f"`{err}`")
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Guild", value=f"{guild.name}")
        embed.add_field(name="Guild ID", value=f"{guild.id}")
        embed.set_footer(text=self.get_current_date_time())

        await channel.send(embed=embed)


def setup(bot):
    """
    Setup function for Cog class in file

    Ran when cog is loaded VIA load_extension() in main.py

    The bot param is automatically passed in during loading

    ...

    Parameters
    ----------
    bot: Bot
        Bot instance from main.py
    """

    bot.add_cog(GuildLogger(bot))
