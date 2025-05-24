import sqlite3
import logging
from typing import Optional

logger = logging.getLogger("db_connection")
logger.setLevel(20)
file_handler = logging.FileHandler('db_connection.log')
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())

class DatabaseConnection:
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn: Optional[sqlite3.Connection] = None
        
    def __enter__(self):
        try: 
            self.conn = sqlite3.connect(self.db_name, check_same_thread=True)
            logger.info(f"Success!! Opened Connection to the Database {self.db_name}")
            return self.conn
        except Exception as e:
            logger.error(f"Error. Failed to Connect to the Database {self.db_name}")
            raise
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            logger.info(f"Success!! Closed Connection to the Database {self.db_name}")
            
if __name__ == "__main__":
    db_conn = DatabaseConnection("users_db.db")
    try:
        with db_conn as conn:
            conn.__enter__()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users LIMIT 10")
            users = cursor.fetchall()
            for user in users:
                print(user)
            cursor.close()
    except Exception as e:
        logger.error(f"Error!! Failed to execute. {e}")