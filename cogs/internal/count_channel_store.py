import asyncpg
import os
from dotenv import load_dotenv

class CountChannelStore:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None
        load_dotenv()

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                os.getenv("DATABASE_URL")
            )

    async def get(self, guild_id: int) -> list[int]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "select channel_id from counting_channels where guild_id=$1", # this is sql cmd
                guild_id
            )
        return [r["channel_id"] for r in rows]

    async def add(self, guild_id: int, channel_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                insert into counting_channels (guild_id, channel_id)
                values ($1, $2)
                on conflict do nothing
                """, # this is sql cmd
                guild_id, channel_id
            )

    async def remove(self, guild_id: int, channel_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                delete from counting_channels
                where guild_id=$1 and channel_id=$2
                """, # this is sql cmd
                guild_id, channel_id
            )