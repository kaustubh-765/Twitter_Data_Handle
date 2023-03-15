import random, re
from datetime import datetime, timedelta, timezone

min_year=2021
max_year=2021

start = datetime(min_year, 5, 31, 00, 00,00)
years = max_year - min_year+1
end = datetime(min_year, 5, 31, 3, 59, 00)

for i in range(10):
    random_date = start + (end - start) * random.random()
    random_date = random_date.isoformat()
    
    index = random_date.index('.') + 1
    new_string = random_date[:index] + '000Z'
    print(new_string)