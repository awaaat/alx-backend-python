import sqlite3 
from typing import List, Tuple
from faker import Faker # type: ignore
from datetime import date

def create_database()-> None:
    try: 
        connection  = sqlite3.connect("users_db.db")
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users;")
        cursor.execute("""CREATE TABLE users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL,
                age INT NOT NULL
            )""")
        faker = Faker()
        # Generate 1000 sample users
        sample_users: List[Tuple[str, str, str, date]] = [
            (faker.first_name(), faker.last_name(), faker.email(), faker.date_of_birth(minimum_age=18, maximum_age=90)) for _ in range(1000)
        ]
        cursor.executemany(
            """ 
            INSERT INTO users(first_name, last_name, email, age)
            VALUES(?,?,?,?)
            """,
            sample_users
        )
        connection.commit()
        print("Successfully created database and inserted 1000 users.")
    except sqlite3.Error as err:
        print(f"An Error Occured: {err}")
    finally:
        connection.close()
if __name__== "__main__":
    create_database()
    
