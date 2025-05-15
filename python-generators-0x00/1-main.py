
from itertools import islice
stream = __import__('0-stream_users')

users = stream.stream_users()
for user in islice(users, 6):
    print(user)
