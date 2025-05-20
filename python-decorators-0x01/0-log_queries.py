import sqlite3
import functools 
import logging
from typing import Callable, Any, Tuple, List
from datetime import datetime

logger = logging.getLogger("Database query")
logger.setLevel(20)
handler = logging.FileHandler("database_queries.log")
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

def log_queries(func: Callable[..., Any]) -> Callable[..., Any]:
    """Creates a decorator that logs the fucntion fetch_all

    Args:
        func (Callable[..., Any]): _description_

    Returns:
        Callable[..., Any]: _description_
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs)-> Any:
        query = args[0] if args else "Unknown Query or No Query Provided"
        params = args[1:] if len(args) > 1 else kwargs.get("params", ())
        start_time = datetime.now()
        logger.info(f"Executing query {query} with parameters {params}")
        try:
            results = func(*args, **kwargs)
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Query execution completed in {execution_time:.3f} seconds")
            return results
        except Exception as e:
            logger.error(f"Query Failed: Error: {e}")
    return wrapper

@log_queries
def fetch_all_users(query):
    """Fetches users in a database

    Args:
        query (_type_): _description_

    Returns:
        _type_: _description_
    """
    connection = sqlite3.connect("users_db.db")
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results

if __name__ == "__main__":
    try:
        users = fetch_all_users("SELECT * FROM users LIMIT 10;")
        for user in users:
            print(user)
    except Exception as e:
        print(f"Database Error: {e}")