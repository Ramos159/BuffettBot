import discord
from discord.ext import commands
from datetime import datetime
from settings import GUILD_LOG_CHANNEL, BOT_LOG_CHANNEL, MEMBER_LOG_CHANNEL


class GuildLogger(commands.Cog):
    """Guild Logger Module"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        Function fired when the bot joins a guild\n
        Returns an embed to the guild log
        """

        channel = self.bot.get_channel(GUILD_LOG_CHANNEL)
        await channel.send(self.guild_join_embed(guild))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """
        Function fired when the bot leaves a guild\n
        Returns an embed to the guild log
        """

        channel = self.bot.get_channel(GUILD_LOG_CHANNEL)
        await channel.send(self.guild_remove_embed(guild))

    def get_current_date_time(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        return dt_string

    def guild_join_embed(self, guild):
        """Makess an embed for the guild log on join"""

        embed = discord.Embed()
        embed.title = "Guild Join"
        embed.type = "rich"
        embed.set_thumbnail(url=guild.icon)
        embed.add_field(name="Server Name", value=guild.name)
        embed.add_field(name="Server Description", value=guild.description)
        embed.add_field(name="Region", value=guild.region)
        embed.add_field(name="ID", value=guild.id)
        embed.set_footer(text=self.get_current_date_time())
        return embed

    def guild_remove_embed(self, guild):
        """Makes an embed for the guild log on leave"""

        embed = discord.Embed()
        embed.title = "Guild Leave"
        embed.type = "rich"
        embed.set_thumbnail(url=guild.icon)
        embed.add_field(name="Server Name", value=guild.name)
        embed.add_field(name="Server Description", value=guild.description)
        embed.add_field(name="Region", value=guild.region)
        embed.add_field(name="ID", value=guild.id)
        embed.set_footer(text=self.get_current_date_time())
        return embed


def setup(bot):
    bot.add_cog(GuildLogger(bot))
