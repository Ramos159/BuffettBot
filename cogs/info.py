from discord.ext import commands


class Info(commands.Cog):
    """
    Info Module

    Will contain commands that pertain to any information regarding the bot

    Inherits from the cog class, as all command cogs do

    ...

    Attributes
    ----------
    bot : Bot
        Bot instance from main.py

    Methods
    -------
    info() -> None
        sets up the command group 

    invite() -> None
        sends an invite message to the requested channel

    github() -> None
        sends the github link for this bot to requested channel

    contact() -> None
        sends a message detailing method of contact to owner

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def info(self, ctx):
        """Get information regarding to the bot"""
        return

    @info.command()
    async def invite(self, ctx):
        """
        Sends an invite message with link to the channel command was used in
        """

        await ctx.trigger_typing()
        invite = 'https://discord.com/oauth2/authorize?client_id=746604823759290399&permissions=392256&scope=bot'
        await ctx.send('>>> Use this link to invite me to your server.\n'
                       "all permisions are **REQUIRED** for the bot to work, please don't remove any!\n"
                       f"{invite}"

                       )

    @info.command()
    async def github(self, ctx):
        """
        Sends a github repository link to the channel it was called in
        """
        await ctx.trigger_typing()
        await ctx.send("https://github.com/Ramos159/BuffettBot")

    @info.command()
    async def ping(self, ctx):
        """
        Get latency number from bot
        """

        await ctx.trigger_typing()
        await ctx.send(f">>> Trading and browsing r/wallstreetbets at {round(self.bot.latency * 1000)} ms")

    @info.command()
    async def contact(self, ctx):
        """
        Sends contact info for owner 
        """

        await ctx.send(
            f">>> If you want to gift someone Tesla stock, **edwin#9454** will gladly accept them"
        )


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

    bot.add_cog(Info(bot))
