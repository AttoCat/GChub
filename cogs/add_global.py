from discord.ext import commands


class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
#DBから取得
        all_channel_name=[]#すべてのチャンネル名
        all_channel_pass=[]#すべてのパスワード
        all_channel_owner=[]#すべてのチャンネルオーナー
    #その他変数
        number_list=['1','2','１','２']
        check_list=['Y','y','ｙ','N','n','ｎ']
        dm = await ctx.author.create_dm()
#既に作成済みの場合
        if ctx.author.id in all_channel_owner:
            await ctx.send('あなたははすでにチャンネルを作成しています。')
            return
        else:
            await dm.send("※テキストチャンネルで設定すると情報漏洩の原因となりますのでDMで設定します\nご了承ください")

#チャンネル名
    #取得
        await dm.send("グローバルチャットチャンネルを設定します\nまず追加したいグローバルチャンネル名を記入してください\nなるべく被らないものにしてください")
        def check1(m):
            return m.content and m.author == ctx.author and m.channel == dm
        try:
            cname = await self.bot.wait_for("message",timeout=60.0, check=check1)
        except asyncio.TimeoutError:
            await dm.send('タイムアウトしました\nもう一度最初からお試しください')
            return

    #例外
        if cname.content in all_channel_name:
            await dm.send('既に作られているチャンネル名です\nもう一度お試しください')
            def checkA(m):
                return m.content and m.author == ctx.author and m.channel == dm
            try:
                cname = await self.bot.wait_for("message",timeout=60.0, check=checkA)
            except asyncio.TimeoutError:
                await dm.send('タイムアウトしました\nもう一度最初からお試しください')
                return
            if cname.content in all_channel_name:
                await dm.send('既に作られているチャンネル名です\nもう一度最初からお試しください')
                return

    #出力
        await dm.send('channel_name:`'+cname.content+'`に設定します')

#レイアウト選択
    #取得   
        await dm.send('次はデザイン選択です\n次の2つから一つ選んでください\n埋め込みの色は既定色の白です。')
        await dm.send('1.ノーマル\n2.埋め込み')
        def check2(m):
            return m.content and m.author == ctx.author and m.channel == dm and m.content in number_list
        try:
            layout_type = await self.bot.wait_for("message",timeout=60.0, check=check2)
        except asyncio.TimeoutError:
            await dm.send('タイムアウトしました\nもう一度お試しください')
            return

    #色選択
        if layout_type.content == ('2' or '２'):
        #取得
            await dm.send('次はカラー選択です\nカラーコードを入力してください')
            def checkB(m):
                return m.content and m.author == ctx.author and m.channel == dm
            try:
                color = await self.bot.wait_for("message",timeout=60.0, check=checkB)
            except asyncio.TimeoutError:
                await dm.send('タイムアウトしました\nもう一度お試しください')
                return

    #出力
        else:
            layout = layout_type.content
        if color.content:
            layout = layout_type.content + color.content
        await dm.send('layout:`'+layout+'`\nに設定します')

#公開
    #取得
        await dm.send('次に公開の設定をします\nパスワードを設定すると追加するときにパスワードが必要になります')
        await dm.send('まず、パスワードの有無を指定してください')
        await dm.send('設定する場合 　: 1')
        await dm.send('設定しない場合 : 2')
        def check3(m):
            return m.content and m.author == ctx.author and m.channel == dm and m.content in number_list
        try:
            checker = await self.bot.wait_for("message",timeout=30.0, check=check3)
        except asyncio.TimeoutError:
            await dm.send('タイムアウトしました\nもう一度お試しください')
            return

    #パスワード設定
        if checker.content==('1' or '１'):
        #取得
            await dm.send('パスワードを設定します\n被りにくいものにしてください')
            def check4(m):
                return m.content and m.author == ctx.author and m.channel == dm
            try:
                password = await self.bot.wait_for("message",timeout=60.0, check=check4)
            except asyncio.TimeoutError:
                await dm.send('タイムアウトしました\nもう一度お試しください')
                return

        #例外
            if password.content in all_channel_pass:
            #取得
                await dm.send('文字数が範囲外か、既に使われているパスワードです\nもう一度お試しください')
                def checkC(m):
                    return  m.content and m.author == ctx.author and m.channel == dm
                try:
                    password = await self.bot.wait_for("message",timeout=60.0, check=checkC)
                except asyncio.TimeoutError:
                    await dm.send('タイムアウトしました\nもう一度最初からお試しください')
                    return

            #例外
                if password.content in all_channel_pass:
                    await dm.send('文字数が範囲外か、既に使われているパスワードです\nもう一度最初からお試しください')
                    return
                else:
                    password = password.content

    #パスワードなし
        if checker.content== ('2' or '２'):
            password = "なし"

    #出力
        await dm.send('パスワードは`'+password+'`に設定します')

#確認
    #取得
        await dm.send('最終確認です')
        embed = discord.Embed(title='username:'+ctx.author.name,description=f"```channelname: {cname.content}``````password: {password}```",color=discord.Colour.from_rgb(255,255,255))
        await dm.send(embed=embed)
        await dm.send('上記でよろしいでしょうか？\nYを選択した場合、利用規約に同意したものとみなします\n Y or N')
        def check5(m):
            return m.content and m.author == ctx.author and m.channel == dm and m.content in check_list
        try:
            agree = await self.bot.wait_for("message", check=check5)
        except asyncio.TimeoutError:
            await dm.send('タイムアウトしました\nもう一度最初からお試しください')
            return

    #同意
        if agree.content ==('Y' or 'y' or 'ｙ'):
            await dm.send('設定完了しました')
            return
        else:
            await dm.send('お手数ですがもう一度最初からお試しください')
            return
def setup(bot):
    bot.add_cog(Create(bot))
