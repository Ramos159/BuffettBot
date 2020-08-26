import discord
import finnhub
import requests
from discord.ext import commands
from random import randint
from settings import FINNHUB_TOKEN


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
        Sends an embed containing quote information for a provided stock
    """

    def __init__(self, bot):
        """
        """
        self.bot = bot
        self.api = finnhub.Client(api_key=FINNHUB_TOKEN)

    @commands.group()
    async def stock(self, ctx):
        """Sell/Buy or get various inforamtion regarding stocks"""
        return

    @stock.command()
    async def quote(self, ctx, symbol=None):
        """Get a quote for a symbol"""
        if symbol is None:
            await ctx.send("Please provide a symbol for the `stock quote` command")
            return

        try:
            quote = self.api.quote(symbol.upper())
        except finnhub.FinnhubAPIException:
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
        """Get company info from a symbol"""
        if symbol is None:
            await ctx.send("Please provide a symbol for the `stock info` command")
            return

        try:
            quote = self.api.company_profile2(symbol=symbol.upper())
        except finnhub.FinnhubAPIException:
            await ctx.send("`Finnhub API Limit reached, try again later`")
            return

        if not quote:
            await ctx.send("Please provide a valid symbol for the `stock info` command")
            return

        embed = discord.Embed()

        embed.title = f"{quote['name']}"
        embed.color = randint(0, 0xffffff)
        embed.set_thumbnail(url=quote["logo"])
        embed.add_field(name="Ticker", value=f"{quote['ticker']}")
        embed.add_field(name="Industry", value=f"{quote['finnhubIndustry']}")
        embed.add_field(name="Exchange", value=f"{quote['exchange']}")
        embed.add_field(name="Market Cap",
                        value=f"{quote['marketCapitalization']}")
        embed.add_field(name="Outstanding",
                        value=f"{quote['shareOutstanding']}")
        embed.add_field(name="IPO", value=f"{quote['ipo']}")
        embed.set_footer(text=quote['weburl'])

        await ctx.send(embed=embed)


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

    bot.add_cog(Stock(bot))
