import discord
from discord.ext import commands
import re
import os
admin_list=[637868010157244449]
cogs = [
    'main',
    'global_chat'
]
class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def reload(self, ctx):
        if not ctx.author.id in admin_list:
            return await ctx.send('Admin専用コマンドです')
        await ctx.send("更新中")
        for files in cogs:
            for cog in os.listdir(f".cogs/{files}"):
                if cog == 'reload.py':
                    continue
                if cog.endswith(".py"):
                    try:
                        self.bot.reload_extension(f"cogs.{files}.{cog[:-3]}")
                    except commands.ExtensionNotLoaded:
                        self.bot.load_extension(f"cogs.{files}.{cog[:-3]}")

        await ctx.send("更新しました")
def setup(bot):
    bot.add_cog(Reload(bot))