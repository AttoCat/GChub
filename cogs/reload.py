from discord.ext import commands
import os
admin_list = [637868010157244449]


class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx):
        if ctx.author.id not in admin_list:
            return await ctx.send('Admin専用コマンドです')
        await ctx.send("更新中")
        for cog in os.listdir("./cogs"):
            if cog == 'reload.py':
                continue
            if cog.endswith(".py"):
                try:
                    self.bot.reload_extension(f"cogs.{cog[:-3]}")
                except commands.ExtensionNotLoaded:
                    self.bot.load_extension(f"cogs.{cog[:-3]}")

        await ctx.send("更新しました")


def setup(bot):
    bot.add_cog(System(bot))
