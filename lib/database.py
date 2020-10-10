import asyncpg
from typing import Any, List, Optional
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
        self.conn: Optional[asyncpg.Connection] = None

    async def _check_database(self, conn: asyncpg.Connection) -> None:
        """create table(s) if required table(s) are not exists."""
        try:
            await self.conn.execute("SELECT 'gchat'::regclass")
        except asyncpg.exceptions.UndefinedColumnError:
            await self.conn.execute('''
                CREATE TABLE gchat (
                    gchat_id varchar(20) PRIMARY KEY,
                    owner_id bigint,
                    password varchar(100)
                )
            ''')
        try:
            await self.conn.execute("SELECT 'gchat_channels'::regclass")
        except asyncpg.exceptions.UndefinedColumnError:
            await self.conn.execute('''
                CREATE TABLE gchat_channels (
                    channel_id bigint PRIMARY KEY,
                    gchat_id varchar(20),

                    FOREIGN KEY(gchat_id) REFERENCES gchat(gchat_id)
                )
            ''')

    async def _setup_connection(self) -> asyncpg.Connection:
        """setup connection and returns `asyncpg.Connection` object."""
        self.conn = await asyncpg.connect(
            host='localhost',
            port=12358,
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            database=os.environ["POSTGRES_DB"],
            loop=self.bot.loop
        )
        await self._check_database(self.conn)
        return self.conn

    async def close(self) -> None:
        """close connection if exists connection."""
        if self.conn is not None:
            await self.conn.close()

    async def get_gchat_channels(self, gchat_id: str) -> List[GchatChannel]:
        """returns List of `GChatChannel` object that match `gchat_id`."""
        conn = self.conn or await self._setup_connection()
        channel_records = await conn.fetch(f"SELECT * FROM gchat_channels WHERE gchat_id='{gchat_id}'")
        channel_object_list: List[GchatChannel] = []
        for record in channel_records:
            gchat_channel = GchatChannel(
                channel_id=record[0],
                gchat_id=record[1]
            )
            channel_object_list.append(gchat_channel)
        return channel_object_list

    async def get_gchat(self, gchat_id) -> Optional[Gchat]:
        """returns `GChat` object from `gchat_id` if exists."""
        conn = self.conn or await self._setup_connection()
        gchat_record = await conn.fetch(f"SELECT * FROM gchat WHERE gchat_id='{gchat_id}'")
        if not gchat_record:
            return None
        gchat_record = gchat_record[0]
        gchat = Gchat(
            gchat_id=gchat_record[0],
            owner_id=gchat_record[1],
            password=gchat_record[2]
        )
        return gchat

    async def get_gchat_channel(self, channel_id) -> Optional[GchatChannel]:
        """returns `GChatChannel` object from `channel_id` if exists."""
        conn = self.conn or await self._setup_connection()
        gchat_channel_record = await conn.fetch(f'SELECT * FROM gchat_channels WHERE channel_id={channel_id}')
        if not gchat_channel_record:
            return None
        gchat_channel_record = gchat_channel_record[0]
        gchat_channel = GchatChannel(
            channel_id=gchat_channel_record[0],
            gchat_id=gchat_channel_record[1]
        )
        return gchat_channel

    async def create_gchat(self, gchat_id, owner_id, password) -> Gchat:
        """insert into database `gchat` an row and returns `Gchat` object."""
        conn = self.conn or await self._setup_connection()
        await conn.execute(f"INSERT INTO gchat VALUES ('{gchat_id}', {owner_id}, '{password}')")
        gchat = Gchat(
            gchat_id=gchat_id,
            owner_id=owner_id,
            password=password
        )
        return gchat

    async def add_gchat_channel(self, channel_id, gchat_id) -> GchatChannel:
        """insert into database `gchat_channels` and row and returns `GchatChannel` object."""
        conn = self.conn or await self._setup_connection()
        gchat = await conn.fetch(f"SELECT * FROM gchat WHERE gchat_id='{gchat_id}'")
        if not gchat:
            raise ValueError("Unknown gchat id")
        await conn.execute(f"INSERT INTO gchat_channels VALUES ({channel_id}, '{gchat_id}')")
        gchat_channel = GchatChannel(
            channel_id=channel_id,
            gchat_id=gchat_id
        )
        return gchat_channel

    async def delete_gchat(self, gchat_id) -> None:
        """delete a row from database `gchat`."""
        conn = self.conn or await self._setup_connection()
        gchat = await conn.fetch(f"SELECT * FROM gchat WHERE gchat_id='{gchat_id}'")
        if not gchat:
            raise ValueError("Invalid gchat id")
        await conn.execute(f"DELETE FROM gchat_channels WHERE gchat_id='{gchat_id}'")
        await conn.execute(f"DELETE FROM gchat WHERE gchat_id='{gchat_id}'")
        return

    async def delete_gchat_channel(self, channel_id, gchat_id):
        """delete a row from table `gchat_channels`."""
        conn = self.conn or await self._setup_connection()
        gchat_channel = await conn.fetch(f"SELECT * FROM gchat_channels WHERE channel_id={channel_id} AND gchat_id='{gchat_id}'")
        if not gchat_channel:
            raise ValueError("Invalid gchat id or channel id")
        await conn.execute(f"DELETE FROM gchat_channels WHERE channel_id={channel_id} AND gchat_id='{gchat_id}'")
        return
