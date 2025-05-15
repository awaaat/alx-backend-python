import mysql.connector

def paginate_users(page_size, offset):
    #page size is the number of rows fetched... 
    #offset means starting from...
    #E.g.. select 100 rows starting from row 0, or select 100 rows starting from row 101
    try:
        """Fetches one page of users from user_data with given page_size and offset."""
        connection = mysql.connector.connect(
            user = "Allan", 
            host = "localhost", 
            password = "Allan@#@2025",
            database = "ALX_prodev")
        cursor = connection.cursor(dictionary = True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        connection.close
        return rows
    except mysql.connector.Error as err:
        print(f"Error while fetching your data: {err}")
        raise
    except Exception as e: 
        print(f"Error: {e}")
        raise
def lazy_paginate(page_size):
    """Generator that lazily yields pages of users, fetching only when needed."""
    try:
        offset = 0
        while True:
            page = paginate_users(page_size, offset)
            if not page:
                break
            yield page
            offset += page_size
    except Exception as e:
        print(f"Error: {e}")
        raise