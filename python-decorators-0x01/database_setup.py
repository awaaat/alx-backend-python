import sqlite3 
from typing import List, Tuple
from faker import Faker # type: ignore

def create_database()-> None:
    try: 
        connection  = sqlite3.connect("users_db.db")
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users;")
        cursor.execute("""CREATE TABLE users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL
            )""")
        faker = Faker()
        # Generate 1000 sample users
        sample_users: List[Tuple[str, str, str]] = [
            (faker.first_name(), faker.last_name(), faker.email()) for _ in range(1000)
        ]
        cursor.executemany(
            """ 
            INSERT INTO users(first_name, last_name, email)
            VALUES(?, ?,?)
            """,
            sample_users
        )
        connection.commit()
        print("Successfully created database and inserted 1000 users.")
    except sqlite3.Error as err:
        print("'An Error Occured: {err}")
    finally:
        connection.close()
if __name__== "__main__":
    create_database()
    
