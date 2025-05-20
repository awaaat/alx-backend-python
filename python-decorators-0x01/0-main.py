log_query = __import__('0-log_queries')
users = log_query.fetch_all_users("SELECT * FROM users LIMIT 10;")
for user in users:
    print(user)