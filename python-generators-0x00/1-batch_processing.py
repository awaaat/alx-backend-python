import mysql.connector

def stream_users_in_batches(batch_size):
    """ This function streams/fetches users in batches based on the specified batch size"""
    try:
        connection = mysql.connector.connect(
        host = "localhost",
        user = "Allan", 
        password = "Allan@#@2025",
        database = "ALX_prodev"
        )
        cursor = connection.cursor(dictionary = True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
            
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise
def batch_processing(batch_size):
    try:
        batches = stream_users_in_batches(batch_size)
        for batch in batches:
            over_25_users = [user for user in batch if user['age']> 25]
            if over_25_users:
                return over_25_users
    
    except Exception as e:
        print(f"Error: {e}")
        raise