#!/usr/bin/python3
seed = __import__('seed')

connection = seed.connect_to_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print(f"Success!! connection successful Database Created")
    
    connection = seed.connect_to_prodev()
    if connection:
        seed.create_table(connection)
        data_url = "https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20250515%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250515T095207Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=a0dcca659123f5c9bcd1b960aa85d896832e733922ad8fa3a427f54f267ec89f"
        seed.insert_data(connection, data_url)
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()
        