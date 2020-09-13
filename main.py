import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()


class GCBot(commands.Bot):
    def __init__(self, prefix='$', **kwargs):
        super().__init__(command_prefix=prefix, **kwargs)
        self._load_cogs()

    def _load_cogs(self):
        cogs = ['cogs.global_chat']
        for cog in cogs:
            self.load_extension(cog)


if __name__ == "__main__":
    bot = GCBot()
    bot.run(os.environ['TOKEN'])
