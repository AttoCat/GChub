from discord.ext import commands


class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Join(bot))
