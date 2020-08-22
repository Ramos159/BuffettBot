import discord
from discord.ext import commands
from discord.utils import oauth_url


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx, *, member: discord.Member = None):
        """Sends an invite to the channel command was invoked"""
        await self.bot.send_typing(ctx.channel)
        invite = 'https://discord.com/oauth2/authorize?client_id=746604823759290399&permissions=392256&scope=bot'
        await ctx.send('''> Use this link to invite me to your server.
                                all permisions are needed for the bot to work, please don't remove any!
                                {}
            '''.format(invite))

    def setup(self, bot):
        self.bot.add_cog(Invite(bot))
