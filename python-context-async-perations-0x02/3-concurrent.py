import logging
import aiosqlite
import asyncio
from typing import List, Tuple, Any

logger = logging.getLogger("async_python")
logger.setLevel(20)
file_handler = logging.FileHandler("async_db.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())

async def async_fetch_users(db_name: str, query:str):
    try:
        async with aiosqlite.connect(db_name) as conn:
            #conn.row_factory = aiosqlite.Row
            cursor = await conn.cursor()
            await cursor.execute(query)
            results = await cursor.fetchall()
            logger.info("Success!! Fetched all users")
            return results
    except Exception as e:
        logger.error(f"Error while executing. {e}")

async def async_fetch_older_users(db_name:str, query:str, parameter: Any):
    try:
        async with aiosqlite.connect(db_name) as conn:
            #conn.row_factory = aiosqlite.Row
            cursor = await conn.cursor()
            await cursor.execute(query, parameter)
            results  = await cursor.fetchall()
            return results
    except Exception as e:
        logger.error(f"Error while processing your request: {e}")
        
async def fetch_concurrently(db_name, query, older_users_query, parameter):
    return await asyncio.gather(
        async_fetch_users(db_name, query),
        async_fetch_older_users(db_name, older_users_query, parameter)
    )
