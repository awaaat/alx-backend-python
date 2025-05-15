import mysql.connector

def stream_user_ages():
    try:
        connection  = mysql.connector.connect(
            host = "localhost",
            user = "Allan",
            password = "Allan@#@2025",
            database = "ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield row[0]
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"Error: {e}")
        raise e
    
def average_age():
    try:
        count = 0
        total = 0
        for age in stream_user_ages():
            total += age
            count+=1
        if count > 0 and total > 0:
            aver = total/count
        else:
            ZeroDivisionError
        return aver

    except Exception as e:
        print(f"Error: {e}")
        raise