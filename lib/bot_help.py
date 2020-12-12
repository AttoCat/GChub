from discord.ext import commands


class BotHelp(commands.HelpCommand):
    """
    botのヘルプを実装するclass
    command_not_foundとsubcommand_not_found以外では文字列を返しても送信されないことに注意してください
    Contextの取得にはself.contextを用いてください
    """
    def __init__(self):
        super().__init__()

    def command_not_found(self, string: str) -> str:
        """
        コマンドが見つからない際に呼び出されるメソッド
        :param string: 見つからなかったコマンド名
        :return:　チャンネルに送信したい文字列
        """
        pass

    def subcommand_not_found(self, command: commands.command, string: str) -> str:
        """
        サブコマンドが見つからない際に呼び出されるメソッド
        :param command: 要求されたサブコマンドのないコマンド
        :param string: 見つからなかったサブコマンド名
        :return: チャンネルに送信したい文字列
        """
        pass

    async def send_bot_help(self, mapping):
        """
        ヘルプコマンド単体で実行されたときに呼び出されるメソッド
        """
        pass

    async def send_command_help(self, command: commands.command):
        """
        コマンド(全てではなく一つ)のヘルプを要求されたときに呼び出されるメソッド
        コマンドが見つからなかった場合command_not_found()が呼ばれます
        :param command: ヘルプを要求されたコマンド
        """
        pass

    async def send_cog_help(self, cog: commands.Cog):
        """
        cogのヘルプを要求されたときに呼び出されるメソッド
        :param cog: ヘルプを要求されたcog
        """
        pass

    async def send_group_help(self, group: commands.Group):
        """
        グループのヘルプを要求されたときに呼び出されるメソッド
        :param group: ヘルプを要求されたグループ
        """
        pass

