import asyncpg
import os
from dotenv import load_dotenv
import asyncio

class CountChannelStore:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None
        load_dotenv()

    async def connect(self):
        if self.pool is not None:
            return  # already connected

        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise RuntimeError("DATABASE_URL not set")

        # Transaction pooler-safe settings
        self.pool = await asyncio.wait_for(
            asyncpg.create_pool(
                dsn=db_url,
                ssl="require",                 # must for Supabase
                min_size=1,                     # safest for pooler
                max_size=1,                     # avoid pooler hangs
                max_inactive_connection_lifetime=60,
                command_timeout=10,
            ),
            timeout=15
        )

        # sanity check
        async with self.pool.acquire() as conn:
            await conn.execute("SELECT 1")

    async def get(self, guild_id: int) -> list[int]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT channel_id FROM counting_channels WHERE guild_id=$1",
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

store = CountChannelStore()