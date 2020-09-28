import asyncpg
from typing import Union, Any, List
from dataclasses import dataclass
import os


@dataclass
class Gchat:
    """Class for global chat data."""
    gchat_id: str
    owner_id: int
    password: str


@dataclass
class GchatChannel:
    """Class for global chat channel data."""
    channel_id: int
    gchat_id: str


class Database:
    def __init__(self, bot: Any) -> None:
        self.bot = bot
        self.conn: Union[asyncpg.Connection, None] = None

    async def check_database(self, conn: asyncpg.Connection) -> None:
        try:
            await self.conn.execute('SELECT "gchat"::regclass')
        except asyncpg.exceptions.UndefinedColumnError:
            await self.conn.execute('''
                CREATE TABLE gchat (
                    gchat_id varchar(20) PRIMARY KEY,
                    owner_id bigint,
                    password varchar(100)
                )
            ''')
        try:
            await self.conn.execute('SELECT "gchat_channels"::regclass')
        except asyncpg.exceptions.UndefinedColumnError:
            await self.conn.execute('''
                CREATE TABLE gchat_channels (
                    channel_id bigint PRIMARY KEY,
                    gchat_id varchar(20),

                    FOREIGN KEY(gchat_id) REFERENCES global_chat(gchat_id)
                )
            ''')

    async def setup_connection(self) -> asyncpg.Connection:
        self.conn = await asyncpg.connect(
            host='localhost',
            port=12358,
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            database=os.environ["POSTGRES_DB"],
            loop=self.bot.loop
        )
        await self.check_database()
        return self.conn

    async def close(self) -> None:
        if self.conn is not None:
            await self.conn.close()

    async def get_gchat_channels(self, gchat_id: str) -> List[GchatChannel]:
        conn = self.conn or self.setup_connection()
        channel_records = await conn.fetch(f'SELECT * FROM ghat_chnnels WHERE gchat_id="{gchat_id}"')
        channel_object_list: List[GchatChannel] = []
        for channel_tuple in channel_records:
            gchat_channel = GchatChannel(
                channel_id=channel_tuple[0],
                gchat_id=channel_tuple[1]
            )
            channel_object_list.append(gchat_channel)
        return channel_object_list
