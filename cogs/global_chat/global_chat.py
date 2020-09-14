from discord.ext import commands


class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        latency = ctx.bot.latency
        await ctx.send(f'{latency*100:.2f}ms')


def setup(bot):
    bot.add_cog(GlobalChat(bot))
