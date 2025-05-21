import sqlite3
import logging
import functools
from typing import Callable, Any, Tuple, Dict, List
from contextlib import contextmanager
query_cache: Dict[tuple, tuple]= {}

logger = logging.getLogger("db_cache")
logger.setLevel(20)
file_handler = logging.FileHandler("cache.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())


@contextmanager
def db_connection(db_name: str):
    conn = None
    try:
        conn = sqlite3.connect(db_name, check_same_thread=True)
        logger.info(f"Success!! Connected to the database {db_name}")
        yield conn
    except Exception as e:
        logger.error(f"Error while connecting to the database: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info(f"Success!! Closed Connection to the Database {db_name}")


def with_db_connection(func: Callable[..., Any]):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with db_connection('users_db.db') as conn:
            return func(conn, *args, **kwargs)
    return wrapper

def cache_query(func: Callable[..., Any]):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        cache_key = (query, args, tuple(sorted(kwargs.items())))
        if cache_key in query_cache:
            logger.info(f" Cache hit for query : { query }")
            return query_cache[cache_key]
        logger.info(f"Cache miss for query : { query }")
        results = func(conn, query, *args, **kwargs)
        if results:
            query_cache[cache_key] = results
        return results
    return wrapper



@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    query = "SELECT * FROM users LIMIT 10;"
    users = fetch_users_with_cache(query=query)
    print("First call:")
    print(users)

    print("\nSecond call (should be cached):")
    users2 = fetch_users_with_cache(query=query)
    print(users2)
