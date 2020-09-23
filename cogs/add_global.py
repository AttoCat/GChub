from discord.ext import commands


class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
#DBから取得
        all_channel_name=[]
        all_channel_pass=[]
        all_channel_owner=[]
    #その他変数
        number_list=['1','2','１','２']
        check_list=['Y','y','ｙ','N','n','ｎ']
        dm = await ctx.author.create_dm()


def setup(bot):
    bot.add_cog(Create(bot))
