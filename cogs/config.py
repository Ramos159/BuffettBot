from discord.ext import commands
from models.models import GuildSetting


class Config(commands.Cog):
    """
    Config Module.

    Attributes
    ----------
    bot : Bot
        bot insance from main.py

    Methods
    -------

    is_admin() -> boolean
        Returns true if user is an admin

    config() -> None
        Creates config group command

    trade_channel -> None
        Sets live trade channel

    prefix() -> None
        Sets command prefix
    """

    def __init__(self, bot):
        self.bot = bot

    async def is_admin(self, ctx=None):
        async def predicate(ctx):
            return ctx.message.author.server_permissions.administrator is True
        return commands.check(predicate)

    @commands.group()
    async def config(self, ctx):
        """Config bot settings."""
        return

    @config.command(aliases=["tc"])
    @commands.check(is_admin)
    async def trade_channel(self, ctx, channel_id=None):
        """Set a channel for the live trade stream. set to a channel id or type unset to remove it."""
        if channel_id is None:
            await ctx.send('`Please give me a channel ID to set`')
            return

        guild = GuildSetting.get(GuildSetting.discord_ID == ctx.guild.id)

        if channel_id == "unset":
            guild.trade_channel = None
            await ctx.send("`Live Trade Channel removed`")

        guild.trade_channel = channel_id
        guild.save()

        await ctx.send('`Live Trade Channel updated`')

    @config.command(aliases=["pf"])
    @commands.check(is_admin)
    async def prefix(self, ctx, prefix=None):
        """Set command prefix for the bot"""
        if prefix is None:
            await ctx.send('`Please enter a new prefix to use`')
            return

        guild = GuildSetting.get(GuildSetting.discord_ID == ctx.guild.id)
        guild.prefix = prefix
        guild.save()

        await ctx.send('`Prefix updated`')


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
    bot.add_cog(Config(bot))
