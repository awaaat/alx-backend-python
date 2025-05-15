import sys
from itertools import islice
processing = __import__('1-batch_processing')
    
for batch in islice(processing.batch_processing(20), 2):  
    for user in batch:
        print(user)
    
    