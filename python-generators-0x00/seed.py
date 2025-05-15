import mysql.connector
import uuid
import csv 
import io
import requests

def connect_to_db():
    """ The function connects to the mysql server without selecting a Database """
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "Allan",
            password = "Allan@#@2025",
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error while connecting to the database: {err}")
        return None
    
def create_database(connection):
    """Creates the databse ALX prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS ALX_prodev")
        cursor.execute("CREATE DATABASE ALX_prodev")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error while creating your database: {err}")
    

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            user = "Allan",
            host = "localhost",
            password = "Allan@#@2025",
            database = "ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error while connecting to the database: {err}")
        return None
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("USE ALX_prodev")
        cursor.execute("DROP TABLE IF EXISTS user_data")
        cursor.execute("""
        CREATE TABLE user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(80) NOT NULL,
        age DECIMAL(4,0) NOT NULL
            )
        """)
        print("Success!! Table user_data created")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error while executing your querry: {err}")
        
def insert_data(connection, data_url):
    """Inserts data from user_data.csv into user_data table."""
    #data_url = "https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20250515%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250515T095207Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=a0dcca659123f5c9bcd1b960aa85d896832e733922ad8fa3a427f54f267ec89f"
    try:
        cursor = connection.cursor()
        response = requests.get(data_url)
        response.raise_for_status()
        csv_file = io.StringIO(response.text)
        csv_data = csv.reader(csv_file)
        next(csv_data) #skip the headers
        for row in csv_data:
            user_id = str(uuid.uuid4())
            name, email, age = row
            cursor.execute(
                    """
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES(%s, %s, %s, %s)
                    """,
                    (user_id, name, email, age)
                )
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        # If insertion fails, print database error
        print(f"Error inserting data: {err}")
    except Exception as e:
        # If CSV reading fails, print general error
        print(f"Error reading CSV: {e}")
        