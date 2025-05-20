import sqlite3
import functools 
from typing import Callable, Any, List, Tuple, Optional
import logging
from contextlib import contextmanager

logger = logging.getLogger('db_transaction')
logger.setLevel(20)
file_handler = logging.FileHandler('transaction.log')
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())

@contextmanager
def db_connection(db_name):
    conn = None
    try:
        conn = sqlite3.connect(database=db_name, check_same_thread = True)
        yield conn
        logger.info(f"Success! Opened database {db_name}")
    except Exception as e:
        logger.error(f"An error occured. Failed to connect to the database {db_name}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info(f"Success! Closed database {db_name}")

def with_db_connection(func: Callable[..., Any]) -> Any:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) ->Any:
        with db_connection('users_db.db') as conn:
            return func(conn, *args, **kwargs)
    return wrapper

def transactional(func: Callable[..., Any]):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            results = func(conn, *args, **kwargs)
            conn.commit()
            logger.info("Success! Transaction Committed")
            return results
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction Rolled Back. Error:  {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    #### Update user's email with automatic transaction handling 

if __name__ == "__main__":
    try:
        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
        logger.info(f"User updated Successfully")
    except Exception as e:
        logger.error(f"Error while updating: {e}")
    