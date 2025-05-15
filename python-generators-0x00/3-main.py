paginate = __import__('2-lazy_paginate')
for page in paginate.lazy_paginate(100):
    for user in page:
        print(user)