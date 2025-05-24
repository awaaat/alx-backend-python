import logging
import sqlite3
from typing import Any


logger = logging.getLogger("db_query_exe")
logger.setLevel(20)
file_handler = logging.FileHandler("db_query.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())

class ExecuteQuery:
    
    def __init__(self, db_name: str, query: Any, parameter):
        self.db_name = db_name
        self.query = query
        self.parameter = parameter
        self.conn = None
        self.results = None
        
    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=True)
            with self.conn as conn: # type: ignore
                cursor = conn.cursor()
                cursor.execute(self.query, self.parameter)
                logger.info(f"Success!! Query with Parameter executed.")
                self.results = cursor.fetchall()
                return self.results
        except Exception as e:
            logger.info(f"Error While executing your query: {e}")
    def __exit__(self, exc_type , exc_val , exc_tb):
        if self.conn:
            self.conn.close()
            logger.info("Success!! Closed Connection to the Database")
            
            
if __name__ == "__main__":
    try:
        with ExecuteQuery(
            db_name="users_db.db",
            query="SELECT * FROM users WHERE id > ? LIMIT 10",
            parameter=(25,)
        ) as results:
            for user in results: # type: ignore
                print(user)
    except Exception as e:
        logger.error(f"Failed to execute query. {e}")