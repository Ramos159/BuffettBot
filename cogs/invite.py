import discord
from discord.ext import commands
# from discord.utils import oauth_url


class Invite(commands.Cog):
    """Invite Module"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """Sends an invite message with link to the channel command was used in"""

        await ctx.trigger_typing()
        invite = 'https://discord.com/oauth2/authorize?client_id=746604823759290399&permissions=392256&scope=bot'
        await ctx.send(f'>>> Use this link to invite me to your server.\n'
                       f"all permisions are **REQUIRED** for the bot to work, please don't remove any!\n"
                       f"{invite}".format(invite)
                       )


def setup(bot):
    bot.add_cog(Invite(bot))
