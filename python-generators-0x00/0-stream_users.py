import mysql.connector

def stream_users():
    """ This will be a generator function that will stream rows from user data"""
    try:
        connection  = mysql.connector.connect(
            host = "localhost",
            user = "Allan",
            password = "Allan@#@2025",
            database = "ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"Error: {e}")
        raise e
        