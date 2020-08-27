import discord
import finnhub
import requests
from datetime import datetime
from discord.ext import commands
from random import randint
from settings import FINNHUB_TOKEN
from settings import BOT_LOG_CHANNEL


class Stock(commands.Cog):
    """
    Stock Module.

    Deals with anything/everything related to stocks

    Inherits from Cog class, as is requiered by the library

    ...

    Attributes
    ----------
    bot: commands.Bot
        The bot instance from main.py

    api: finnhub.Client
        the finnhub api we use to receive stock information


    Methods
    -------
    stock() -> None
        Sets up stock command group

    quote() -> None
        Sends an embed containing quote information for a provided symbol

    info() -> None
        Sends an embed containing company information for the provided symbol
    """

    def __init__(self, bot):
        """
        """
        self.bot = bot
        self.api = finnhub.Client(api_key=FINNHUB_TOKEN)
        self.log = int(BOT_LOG_CHANNEL)

    async def create_bot_log(self, ctx, err):
        """Creates an embed with details concerning an err and sends it to the log channel."""
        channel = self.bot.get_channel(self.log)

        embed = discord.Embed()

        embed.title = "Finnhub API Error"
        embed.description = str(f"`{err}`")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="Guild", value=f"{ctx.guild}")
        embed.add_field(name="Guild ID", value=f"{ctx.guild.id}")
        embed.add_field(name="Message", value=f"{ctx.message.content}")
        embed.add_field(name="Message ID", value=f"{ctx.message.id}")
        embed.add_field(name="User", value=f"{ctx.message.author.name}")
        embed.add_field(name="User ID", value=f"{ctx.message.author.id}")
        embed.set_footer(text=self.get_current_date_time())

        await channel.send(embed=embed)

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

    @commands.group()
    async def stock(self, ctx):
        """Sell/Buy or get various inforamtion regarding stocks."""
        return

    @stock.command()
    async def quote(self, ctx, symbol=None):
        """Get a quote for a symbol."""
        if symbol is None:
            await ctx.send("Please provide a symbol for the `stock quote` command")
            return

        try:
            quote = self.api.quote(symbol.upper())
        except finnhub.FinnhubAPIException as err:
            await self.create_bot_log(ctx, err)
            await ctx.send("`Finnhub API Limit reached, try again later`")
            return

        if not quote:
            await ctx.send("Please provide a valid symbol for the `stock quote` command")
            return

        embed = discord.Embed()

        embed.title = f"{symbol.upper()}"
        embed.color = randint(0, 0xffffff)
        embed.add_field(name="Current", value=f"${quote['c']}")
        embed.add_field(name="High", value=f"${quote['h']}")
        embed.add_field(name="Low", value=f"${quote['l']}")
        embed.add_field(name="Opening", value=f"${quote['o']}")
        embed.add_field(name="Previous Closing", value=f"${quote['pc']}")

        await ctx.send(embed=embed)

    @stock.command()
    async def info(self, ctx, symbol=None):
        """Get company info from a symbol."""
        if symbol is None:
            await ctx.send("Please provide a symbol for the `stock info` command")
            return

        try:
            info = self.api.company_profile2(symbol=symbol.upper())
        except finnhub.FinnhubAPIException as err:
            await self.create_bot_log(ctx, err)
            await ctx.send("`Finnhub API Limit reached, try again later`")
            return

        if not info:
            await ctx.send("Please provide a valid symbol for the `stock info` command")
            return

        embed = discord.Embed()

        embed.title = f"{info['name']}"
        embed.color = randint(0, 0xffffff)
        embed.set_thumbnail(url=info["logo"])
        embed.add_field(name="Ticker", value=f"{info['ticker']}")
        embed.add_field(name="Industry", value=f"{info['finnhubIndustry']}")
        embed.add_field(name="Exchange", value=f"{info['exchange']}")
        embed.add_field(name="Market Cap",
                        value=f"{info['marketCapitalization']}")
        embed.add_field(name="Outstanding",
                        value=f"{round(info['shareOutstanding'],2)}")
        embed.add_field(name="IPO", value=f"{info['ipo']}")
        embed.url = info['weburl']

        await ctx.send(embed=embed)

    @stock.command()
    async def sentiment(self, ctx, symbol=None):
        """Get Sentiment stats surrounding a company from a symbol."""
        if symbol is None:
            await ctx.send("Please provide a symbol for the `stock sentiment` command")
            return

        try:
            sent = self.api.news_sentiment(symbol.upper())
        except finnhub.FinnhubAPIException as err:
            await self.create_bot_log(ctx, err)
            await ctx.send("`Finnhub API Limit reached, try again later`")

            return

        if not sent:
            await ctx.send("Please provide a valid symbol for the `stock sentiment` command")
            return

        embed = discord.Embed()

        # Finnhub API gives me decimals no greater than 0, need to multiply and round number
        embed.title = f"{sent['symbol']} Sentiment Report"
        embed.color = randint(0, 0xffffff)
        embed.add_field(
            name='Bullish', value=f"{round(sent['sentiment']['bullishPercent'] * 100 )}%")
        embed.add_field(name="Sector Avg. Bullish",
                        value=f"{round(sent['sectorAverageBullishPercent']) * 100}%")
        embed.add_field(name="Article Buzz",
                        value=f"{round(sent['buzz']['buzz']) * 100}%")
        embed.add_field(name="Week Article Count",
                        value=f"{round(sent['buzz']['articlesInLastWeek'])}")
        embed.add_field(name="News Score",
                        value=f"{round(sent['companyNewsScore'] * 100)}%")
        embed.add_field(name="Sector Avg. News Score",
                        value=f"{round(sent['sectorAverageNewsScore']) * 100}%")

        await ctx.send(embed=embed)


def setup(bot):
    """
    Setup function for Cog class in file.

    Ran when cog is loaded VIA load_extension() in main.py

    The bot param is automatically passed in during loading

    ...

    Parameters
    ----------
    bot: Bot
        Bot instance from main.py
    """

    bot.add_cog(Stock(bot))
