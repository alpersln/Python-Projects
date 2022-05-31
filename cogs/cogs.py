import discord
from discord.ext import commands


class SocialMedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def socialmedia(self, ctx):
        await ctx.send("Merhaba")


def setup(bot):
    bot.add_cog(SocialMedia(bot))
