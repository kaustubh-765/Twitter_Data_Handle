import json
import csv
import os
import random, re
from datetime import datetime, timedelta, timezone
import pandas as pd
import tweet_sort_by_date_and_time_zone_csv as tw


original_tweet = "Original_tweets_in_json.json"
train_split_file = "train_split.csv"
test_split_file = "test_split.csv"
frequency_count = "Twitter_Data_Handle\Kaustubh-TwitterScript\Data (version 1).xlsx"

try:
    tt = open(original_tweet)
    org_tweet = json.load(tt)
except OSError as error:
   print("Try Again!")
   print(error)
   exit()

xls = pd.ExcelFile(frequency_count)
df1 = pd.read_excel(xls, 'english_original')

col_list = []

for col in df1.columns:
    col_list.append(col)


def train_test_csv_header():
    csvFile_1 = open(train_split_file, "a", newline="", encoding='utf-8')
    csvFile_2 = open(test_split_file, "a", newline="", encoding='utf-8')

    csvWriter = csv.writer(csvFile_1)

    csvWriter.writerow(['Sno.', 'ID', 'Text', 'Like Count', 'Reply Count', 'Retweet Count'])
    csvFile_1.close()

    csvWriter = csv.writer(csvFile_2)

    csvWriter.writerow(['Sno.', 'ID', 'Text', 'Like Count', 'Reply Count', 'Retweet Count'])
    csvFile_1.close()

def random_time(date, i, j ,time_slot, rng):
        
    min_year=2021
    new_string = ""

    if(time_slot == 0):    
        start = datetime(min_year, i+3, j, 00, 00,00)
        end = datetime(min_year, i+3, j, 5, 59, 00)

    
    if(time_slot == 1):    
        start = datetime(min_year, i+3, j, 6, 00, 00)
        end = datetime(min_year, i+3, j, 11, 59, 00)

    
    if(time_slot == 2):    
        start = datetime(min_year, i+3, j, 12, 00,00)
        end = datetime(min_year, i+3, j, 17, 59, 00)

    
    if(time_slot == 3):    
        start = datetime(min_year, i+3, j, 18, 00,00)
        end = datetime(min_year, i+3, j, 23, 59, 00)

    total_list = []

    for i in range(rng):
        random_date = start + (end - start) * random.random()
        random_date = random_date.isoformat()
        
        index = random_date.index('.') + 1
        new_string = random_date[:index] + '000Z'
        total_list.append(new_string)

    return new_string
        

def train_split():

    date = tw.get_total_dates()

    csvFile_1 = open(train_split_file, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile_1)

    i = 1

    while i<6:
        mon_data = df1.loc[:,col_list[i]]
        j=1
        while j<31:
            
            date_for_count = datetime(2021, i+3, j , 00, 00, 00)

            list_slot_wise = tw.print_tweet_counts_by_date_and_total_tweets(date)

            time_slot = 0

            while (time_slot < 4):
                tweet_time = random_time(date = date_for_count,i=i,j=j, time_slot=time_slot, rng = list_slot_wise[time_slot])
                counter = 0
                print("Done_233")
                for response in org_tweet['batches']:
                    for tweets in response['data']:
                        
                        for dt in tweet_time:
                            if dt == tweets['time'] and counter != list_slot_wise[time_slot]:
                                author_id = tweets['author_id']
                                id = tweets['conversation_id']
                                text = tweets['text']
                                retweet_count = tweets['public_metrics']['retweet_count']
                                reply_count = tweets['public_metrics']['reply_count']
                                like_count = tweets['public_metrics']['like_count']

                                res = [author_id, id, text, like_count, reply_count, retweet_count]
                                csvWriter.writerow(res)
                                print("Done ", counter)
                                counter += 1



                time_slot += 1            
            j += 1
        i += 1

        csvFile_1.close()
    return []

def test_split():
    csvFile_1 = open(train_split_file, "r", newline="", encoding='utf-8')
    csvFile_2 = open(test_split_file, "a", newline="", encoding='utf-8')
    csvreader = csv.reader(csvFile_1)
    csvWriter = csv.writer(csvFile_2)


    for response in org_tweet['batches']:
        for tweets in response['data']:
            
            not_in_train = True
            for row in csvreader:
                if(row['conversation_id'] == tweets['conversation_id']):
                    not_in_train = False
                    break

            
            if not_in_train:
                author_id = tweets['author_id']
                id = tweets['conversation_id']
                text = tweets['text']
                retweet_count = tweets['public_metrics']['retweet_count']
                reply_count = tweets['public_metrics']['reply_count']
                like_count = tweets['public_metrics']['like_count']

                res = [author_id, id, text, like_count, reply_count, retweet_count]
                csvWriter.writerow(res)
        

if __name__ == "__main__":

    if not(os.path.exists(test_split_file) and os.path.exists(train_split_file)):
       train_test_csv_header()

    if (os.path.exists(test_split_file) and os.path.exists(train_split_file)):
       train_split()
       #test_split()


    #print(xls)



"""
import csv
import sys
import os

# example usage: python split.py example.csv 200
# above command would split the `example.csv` into smaller CSV files of 200 rows each (with header included)
# if example.csv has 401 rows for instance, this creates 3 files in same directory:
#   - `example_1.csv` (row 1 - 200)
#   - `example_2.csv` (row 201 - 400)
#   - `example_3.csv` (row 401)

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
filename = sys.argv[1]

full_file_path = os.path.join(CURRENT_DIR, filename)
file_name = os.path.splitext(full_file_path)[0]

rows_per_csv = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

with open(filename) as infile:
    reader = csv.DictReader(infile)
    header = reader.fieldnames
    rows = [row for row in reader]
    pages = []

    row_count = len(rows)
    start_index = 0
    # here, we slice the total rows into pages, each page having [row_per_csv] rows
    while start_index < row_count:
        pages.append(rows[start_index: start_index+rows_per_csv])
        start_index += rows_per_csv

    for i, page in enumerate(pages):
        with open('{}_{}.csv'.format(file_name, i+1), 'w+') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=header)
            writer.writeheader()
            for row in page:
                writer.writerow(row)

        print('DONE splitting {} into {} files'.format(filename, len(pages)))
"""