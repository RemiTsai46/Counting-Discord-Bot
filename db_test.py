import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def test():
    conn = await asyncio.wait_for(
        asyncpg.connect(os.getenv("DATABASE_URL"), timeout=5),
        timeout=10
    )
    rows = await conn.fetch("select 1")
    await conn.close()
    print(rows)

asyncio.run(test())