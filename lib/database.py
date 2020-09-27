import asyncpg
from typing import Union, Any # Tupleがあったけど使われてないので削除。
import os


class Database:
    def __init__(self, bot: Any) -> None:
        self.bot = bot
        self.conn: Union[asyncpg.Connection, None] = None

    async def check_database(self) -> None:
        conn = self.conn or await self.setup()
        try:
            await conn.execute('SELECT "gchat"::regclass')
        except asyncpg.exceptions.UndefinedColumnError:
            await conn.execute('''
                CREATE TABLE gchat (
                    gchat_id varchar(20)
                    owner_id bigint
                    password varchar(100)

                    PRIMARY KEY(gchat_id)
                )
            ''')
        try:
            await conn.execute('SELECT "gchat_channels"::regclass')
        except asyncpg.exceptions.UndefinedColumnError:
            await conn.execute('''
                CREATE TABLE gchat_channels (
                    channel_id bigint
                    gchat_id varchar(20)

                    PRIMARY KEY(channel_id)
                    FOREIGN KEY(gchat_id) REFERENCES global_chat(gchat_id)
                )
            ''')

    async def create_connection(self) -> asyncpg.Connection:
        self.conn = await asyncpg.connect(
            host='',
            port=1234,
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            database=os.environ["POSTGRES_DB"],
            loop=self.bot.loop
        )
        return self.conn
