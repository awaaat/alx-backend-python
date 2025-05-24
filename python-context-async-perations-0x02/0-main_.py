import asyncio
asn = __import__('3-concurrent')  # or import your module normally

async def main():
    users_query = "SELECT * FROM users LIMIT 10;"
    older_users_query = "SELECT * FROM users WHERE age > ? LIMIT 5;"
    parameter = (40,)

    result = await asn.fetch_concurrently("users_db.db", users_query, older_users_query, parameter)

    print("Users:")
    for user in result[0]:
        print(user)

    print("\nOlder users:")
    for user in result[1]:
        print(user)

asyncio.run(main())
