import time
import sqlite3
import functools
from typing import Callable, Any, List, Tuple, Optional
from contextlib import contextmanager
import logging

#set logger handler
logger = logging.getLogger("db_retries")
logger.setLevel(20)
file_handler = logging.FileHandler("retries.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())

@contextmanager
def db_connection(db_name: str):
    conn = None
    try:
        conn = sqlite3.connect(db_name, check_same_thread=True)
        logger.info(f"Success!! Made Connection to  Database {db_name}")
        yield conn
    except Exception as e:
        logger.error(f"Error!! Failed to Make Connection to Database {db_name}")
        raise 
    finally:
        if conn:
            conn.close()
            logger.info(f"Success!! Connection to the Database Was Closed")

def with_db_connection(func: Callable[..., Any]):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with db_connection("users_db.db") as conn:
            return func(conn, *args, **kwargs)
    return wrapper

def retry_on_failure(retries: int, delay: float, rule: Optional[Callable[[Exception], bool]] = None):
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)        
                except sqlite3.OperationalError as o_err:
                    last_exception = o_err
                    if attempt < retries:
                        logger.info(f"Retry {attempt + 1}/{retries} after {delay}s: {o_err}")
                        time.sleep(delay)
                raise last_exception
        return wrapper
    return decorator
                        
                        
@with_db_connection
@retry_on_failure(retries = 3, delay = 1.2)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users LIMIT 10")
    return cursor.fetchall()

if __name__ == "__main__":
    users = fetch_users_with_retry()
    for user in users:
        print(user)