import os
import discord
import traceback
import re
import unicodedata
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
Nickname_prefix_re = re.compile(r"[「\[［\(（](.+)[\]］\)）」]")

def get_prefix(bot, message):
    if message.guild is None:
        return commands.when_mentioned_or("gc!")
    match_tmp = re.match(Nickname_prefix_re, message.guild.me.display_name)
    if match_tmp is None:
        return commands.when_mentioned_or("gc!")
    elif unicodedata.category(match_tmp[1][-1])[0] in "LN":
        return commands.when_mentioned_or(match_tmp[1] + " ")
    else:
        return commands.when_mentioned_or(match_tmp[1])


class GCBot(commands.Bot):
    def __init__(self, prefix=get_prefix, **kwargs):
        self.prefix = prefix
        self.logch_id = 725117475225600041  # commandsチャンネルに設定
        super().__init__(command_prefix=prefix, **kwargs)

    async def _load_cogs(self):
        self.load_extension("cogs.reload")
        for cog in os.listdir("./cogs"):
            if cog == 'reload.py':
                continue
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"cogs.{cog[:-3]}")
                except commands.ExtensionAlreadyLoaded:
                    self.reload_extension(f"cogs.{cog[:-3]}")

    async def on_ready(self):
        await self._load_cogs()
        await self.change_presence(
            activity=discord.Game(
                name=f"{self.prefix}about | {len(self.guilds)}guilds"
            )
        )

    async def on_command_error(self, ctx, error1):
        orig_error = getattr(error1, "original", error1)
        error_msg = ''.join(
            traceback.TracebackException.from_exception(orig_error).format())
        error_msg = "```py\n" + error_msg + "\n```"
        await self.get_channel(self.logch_id).send(error_msg)


if __name__ == "__main__":
    bot = GCBot()
    bot.run(os.environ['TOKEN'])
