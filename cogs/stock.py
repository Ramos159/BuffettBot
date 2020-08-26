import discord
import finnhub
from discord.ext import commands
from settings import FINNHUB_API_TOKEN


class Stock(commands.Cog):
    """
    Stock Module 

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
        self.api = finnhub.Client(api_key=FINNHUB_API_TOKEN)

    @commands.group()
    async def stock(self, ctx):
        """Sell/Buy or get various inforamtion regarding stocks"""
        return

    @stock.command()
    async def quote(self, ctx, symbol=None):
        """Get a quote with the message arguement"""
        if symbol is None:
            await ctx.send("Please provide a symbol for the `stock quote` command")
            return

        quote = self.api.quote(symbol.upper())

        if not quote:
            await ctx.send("Please provide a valid symbol for the `stock quote` command")
            return

        await ctx.send(":)")


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
