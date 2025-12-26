import asyncpg, os, asyncio
from dotenv import load_dotenv

load_dotenv()
async def test():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    await conn.execute("select 1")
    print("DB connected")
    await conn.close()

asyncio.run(test())