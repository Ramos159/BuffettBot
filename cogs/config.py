import finnhub
import discord
from datetime import datetime
from discord.ext import commands
from models import Guild, GuildStock, Stock
from settings import FINNHUB_TOKEN, BOT_LOG_CHANNEL

# use this snippet beloew later

# async with ctx.typing():
#   await long_operation
# await ctx.send()


class Config(commands.Cog):
    """
    Config Module.
    """

    def __init__(self, bot):
        self.bot = bot
        self.api = finnhub.Client(api_key=FINNHUB_TOKEN)
        self.log = int(BOT_LOG_CHANNEL)

    async def is_admin(self, ctx=None):
        """Checks if the requesting user is an admin"""
        async def predicate(ctx):
            if ctx.message.author.server_permissions.administrator:
                return True
            await ctx.send("Please have an admin use this command")
            return False
        return commands.check(predicate)

    async def has_active_trade_channel(self, ctx=None):
        """Checks if a server has set trade news channel"""
        async def predicate(ctx):
            active = Guild.get(
                Guild.discord_id == ctx.guild.id).new_channel_id
            if active is None:
                await ctx.send("Please use command `config tc set` to set a trade channel")
                return False
            return True
        return commands.check(predicate)

    @commands.group()
    async def config(self, ctx):
        """Config bot settinGuild."""
        return

    @config.group(aliases=["tc"])
    async def trade_channel(self, ctx):
        """Trade Channel settinGuild. shortcut = tc"""
        return

    @trade_channel.command(aliases=["t"])
    @commands.check(is_admin)
    @commands.check(has_active_trade_channel)
    async def track(self, ctx, symbol=None):
        """Sets a new symbol to track"""
        await ctx.trigger_typing()
        if symbol is None:
            await ctx.send('`Please give me a symbol to add`')
            return

        stock = Stock.get_or_none(symbol=symbol)
        guild = Guild.get(Guild.discord_id == ctx.guild.id)
        breakpoint()
        # stock doesnt exist
        if stock is None:
            # see if its a valid symbol
            try:
                new_stock = self.api.quote(symbol)
            except Exception as err:
                await self.create_bot_log(ctx.guild, err)
                await ctx.send("This symbol can't be added at the moment")
                return

            if new_stock is None:
                await ctx.send("Please enter a valid symbol to add")
                return
            # create the global stock since its not there
            stock = Stock.create(symbol=symbol)

        interest = GuildStock.get_or_none(
            GuildStock.stock == stock,
            GuildStock.guild == guild)

        if interest:
            await ctx.send(f"This server is already tracking `{symbol.upper()}`")
            return

        if interest is None:
            GuildStock.create(
                guild=guild, stock=stock)
            await ctx.send(f"This server is now tracking `{symbol.upper()}`")
            return

    @ trade_channel.command(aliases=["ut"])
    @ commands.check(is_admin)
    @ commands.check(has_active_trade_channel)
    async def untrack(self, ctx, symbol=None):
        """Removes a tracked symbol"""
        # pylint yells at line 123, no clue why
        # pylint: disable=no-value-for-parameter
        await ctx.trigger_typing()

        if symbol is None:
            await ctx.send("Please give me a symbol to untrack")
            return

        stock = Stock.get(Stock.symbol == symbol)
        guild = Guild.get(Guild.discord_id == ctx.guild.id)
        interest = GuildStock.get_or_none(
            GuildStock.stock == stock, GuildStock.guild == guild)

        if interest is None:
            await ctx.send(f"You're not tracking `{symbol.upper()}`")
            return

        if interest:
            interest.delete_instance()

            count = Stock.select().count()

            # if no one is interesting in tracking this stock, get rid of it from table
            if count == 0:
                Stock.delete().where(Stock.symbol == symbol)

            await ctx.send(f"No longer tracking trades for `{symbol.upper()}`")
            return

    @ trade_channel.command()
    @ commands.check(is_admin)
    async def set(self, ctx, channel_id=None):
        """Set a channel for the live trade stream. set to a channel id or type unset to remove it."""
        await ctx.trigger_typing()
        if channel_id is None:
            await ctx.send('Please give me a `channel ID` to set')
            return

        guild = Guild.get(Guild.discord_id == ctx.guild.id)

        guild.trade_channel = channel_id
        guild.save()

        await ctx.send('Live Trade Channel updated')
        return

    @ config.command(aliases=["pf"])
    @ commands.check(is_admin)
    async def prefix(self, ctx, prefix=None):
        """Set command prefix for the bot"""
        await ctx.trigger_typing()
        if prefix is None:
            await ctx.send('Please enter a new prefix to use')
            return

        guild = Guild.get(Guild.discord_id == ctx.guild.id)
        guild.prefix = prefix
        guild.save()

        await ctx.send('`Prefix updated`')
        return

    @ trade_channel.command()
    @ commands.check(is_admin)
    async def unset(self, ctx):
        guild = Guild.get(Guild.discord_id == ctx.guild.id)

        guild.trade_channel = None
        await ctx.send("Live Trade Channel removed")
        return

    def get_current_date_time(self):
        """
        Makes a string from the current time and date\n
        Uses the datetime module.
        """
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %H:%M")
        return dt_string

    async def create_bot_log(self, guild, err):
        """Creates an embed with details concerning an err and sends it to the log channel."""
        channel = self.bot.get_channel(self.log)

        embed = discord.Embed()
        embed.title = "Error Log"
        embed.description = str(f"`{err}`")
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Guild", value=f"{guild.name}")
        embed.add_field(name="Guild ID", value=f"{guild.id}")
        embed.set_footer(text=self.get_current_date_time())

        await channel.send(embed=embed)
        return


def setup(bot):
    """
    Setup function for Cog class in file

    Ran when cog is loaded VIA load_extension() in main.py

    The bot param is automatically passed in during loading
    """
    bot.add_cog(Config(bot))
