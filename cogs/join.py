from discord.ext import commands
import asyncio


class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        # 変数
        open_channel_name = ['test']   # すべてのパスのないチャンネル名
        close_channel_name = ['TEST']  # すべてのパスのあるチャンネル名
        # 取得
        dm = await ctx.author.create_dm()
        await dm.send("※テキストチャンネルで設定すると情報漏洩の原因となりますのでDMで設定します。\nご了承ください。\n**注意： 全ての入力は1分経過するとタイムアウトとなり、やり直しになります。\n事前に入力内容を決めておき、メモ帳に書いておく等することをお勧めします。**")
        await dm.send("グローバルチャットチャンネルに参加します。\n参加したいグローバルチャンネル名を記入してください。")

        def check1(m):
            return m.content and m.author == ctx.author and m.channel == dm
        try:
            chname = await(self.bot.wait_for("message", timeout=60.0, check=check1))
        except asyncio.TimeoutError:
            await dm.send('タイムアウトしました\nもう一度最初からお試しください')
            return
        # 例外
        if chname.content not in (*open_channel_name, *close_channel_name):
            await dm.send('存在しないチャンネルです。もう一度ご確認ください')
            return
        # 既存
        else:
            new_channel_name = chname.content
            # open
            if chname.content in open_channel_name:
                # DB書き込み
                await ctx.send('認証しました。\n作成中・・・')
            # close
            elif chname.content in close_channel_name:
                # DBからchname.contentでpass取得
                password = 'pass'
                await dm.send('パスワード付きのチャンネルです\nパスワードを入力してください。')

                def check2(m):
                    return m.content and m.author == ctx.author and m.channel == dm
                try:
                    pass_word = await(self.bot.wait_for("message", timeout=60.0, check=check2))
                except asyncio.TimeoutError:
                    await dm.send('タイムアウトしました\nもう一度最初からお試しください')
                    return
                if pass_word.content != password:
                    await dm.send('パスワードが違います\nもう一度入力してください')

                    def check3(m):
                        return m.content and m.author == ctx.author and m.channel == dm
                    try:
                        pass_word = await(self.bot.wait_for("message", timeout=60.0, check=check3))
                    except asyncio.TimeoutError:
                        await dm.send('タイムアウトしました\nもう一度最初からお試しください')
                        return
                    if pass_word.content == password:
                        # DB書き込み
                        await ctx.send('認証しました。\n作成中・・・')
                    else:
                        await dm.send('パスワードが違います\nもう一度最初から設定してください')
                        return
                else:
                    # DB書き込み
                    await ctx.send('認証しました。\n作成中・・・')

            # DB書き込みはここに
            # 作成
            await ctx.send(new_channel_name)
            new_chan = await ctx.guild.create_text_channel(name=new_channel_name)
            await new_chan.create_webhook(name="GChub")


def setup(bot):
    bot.add_cog(Join(bot))
