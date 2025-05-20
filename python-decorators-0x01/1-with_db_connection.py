import sqlite3
import functools
from typing import Callable, Any, Optional
import logging

logger = logging.getLogger('db_connection')
logger.setLevel(20)
file_handler = logging.FileHandler("db_connection.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())
from contextlib import contextmanager
import functools

@contextmanager
def db_connection(db_name: str):
    conn = None
    try:
        conn = sqlite3.connect(db_name, check_same_thread=True)
        logger.info(f"Opened Database {db_name}")
        yield conn
    except Exception as e:
        logger.error(f"An Error Occured: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info(f"Closed Database {db_name}")

def with_db_connection(func: Callable[..., Any]):
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        with db_connection('users_db.db') as conn:
            return func(conn, *args, **kwargs)
    return wrapper
            

@with_db_connection 
def get_user_by_id(conn: sqlite3.Connection, user_id: int): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?  LIMIT 10;", (user_id,)) 
    return cursor.fetchone()
    
if __name__ == "__main__":
    try:
        user = get_user_by_id(user_id = 1)
        print(user)
    except Exception as e:
        print(f"A Database Error Occured: {e}")