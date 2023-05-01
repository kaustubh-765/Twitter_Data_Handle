import json
import csv
import os
import random, re
from datetime import datetime
import pandas as pd
import tweet_sort_by_date_and_time_zone_csv as tw
import math

# Data_of_month = 'April'
# date = "2021-04-24"
# Date = int(date[8:10])
# Month = int(date[5:7])
original_tweet = 'data/Afghanistan-tweets-April24-original.json'

total_date_list = tw.get_total_dates(original_tweet)

train_split_file = "train_split.csv"
test_split_file = "test_split.csv"
frequency_count = "Twitter_Data_Handle/Kaustubh-TwitterScript/Data (version 1).xlsx"

try:
    tt = open(original_tweet)
    org_tweet = json.load(tt)
except OSError as error:
   print("Try Again!")
   print(error)
   exit()

xls = pd.ExcelFile(frequency_count)
df1 = pd.read_excel(xls, 'Sample_count')

col_list = []

for col in df1.columns:
    col_list.append(col)


sample_data = df1['April_sample_count'].tolist()
cal_data = df1['April_final_count'].tolist()



def almost_matches(str1, str2):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"  # Change the format to match your datetime string
    
    # Parse the datetime from the strings
    dt1 = datetime.strptime(str1, date_format)
    dt2 = datetime.strptime(str2, date_format)
    
    # Check if the dates match exactly and the hours are within 1 hour of each other
    # if dt1.date() == dt2.date() and abs(dt1.hour - dt2.hour) <= 1:
    if dt1.date() == dt2.date() and abs(dt1.hour - dt2.hour) <= 1 and abs(dt1.minute - dt2.minute) <= 1:
        return True
    else:
        return False

def almost_matches_per_30_min(str1, str2):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"  # Change the format to match your datetime string
    
    # Parse the datetime from the strings
    dt1 = datetime.strptime(str1, date_format)
    dt2 = datetime.strptime(str2, date_format)
    
    # Check if the dates match exactly and the hours are within 1 hour of each other
    # if dt1.date() == dt2.date() and abs(dt1.hour - dt2.hour) <= 1:
    if dt1.date() == dt2.date() and abs(dt1.hour - dt2.hour) <= 1 and abs(dt1.minute - dt2.minute) <= 30:
        return True
    else:
        return False

def train_test_csv_header():
    csvFile_1 = open(train_split_file, "a", newline="", encoding='utf-8')
    csvFile_2 = open(test_split_file, "a", newline="", encoding='utf-8')

    csvWriter = csv.writer(csvFile_1)

    csvWriter.writerow(['Sno.','Author_ID', 'ID', 'Text', 'Like Count', 'Reply Count', 'Retweet Count'])
    csvFile_1.close()

    csvWriter = csv.writer(csvFile_2)

    csvWriter.writerow(['Sno.', 'Author_ID' , 'ID', 'Text', 'Like Count', 'Reply Count', 'Retweet Count'])
    csvFile_1.close()

def random_time(date, i, j ,time_slot, rng):
        
    min_year=2021
    new_string = ""

    if(time_slot == 0):    
        start = datetime(min_year, i, j, 00, 00,00)
        end = datetime(min_year, i, j, 5, 59, 00)

    
    if(time_slot == 1):    
        start = datetime(min_year, i, j, 6, 00, 00)
        end = datetime(min_year, i, j, 11, 59, 00)

    
    if(time_slot == 2):    
        start = datetime(min_year, i, j, 12, 00,00)
        end = datetime(min_year, i, j, 17, 59, 00)

    
    if(time_slot == 3):    
        start = datetime(min_year, i, j, 18, 00,00)
        end = datetime(min_year, i, j, 23, 59, 00)

    total_list = []

    for i in range(rng):
        random_date = start + (end - start) * random.random()
        random_date = random_date.isoformat()
        
        index = random_date.index('.') + 1
        new_string = random_date[:index] + '000Z'
        total_list.append(new_string)

    return total_list
        

def train_split():

    # date = tw.get_total_dates()

    sum_of_range = 0
    csvFile_1 = open(train_split_file, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile_1)
    sno = 1
    
    for date in total_date_list:
        Date = int(date[8:10])
        Month = int(date[5:7])
        
        list_slot_wise = tw.print_tweet_counts_by_date_and_total_tweets(date, original_tweet)
        print(list_slot_wise)
        
        print(f"Iterating for Date : {date}")

        time_slot = 0
        
        while (time_slot < 4):

            print(f"Time Slot : {time_slot}")
            _range = list_slot_wise[time_slot]*cal_data[Date]
            _range = int(math.ceil(_range))
            print(f"Range for this slot : {_range}")
            sum_of_range += _range
            tweet_time = random_time(date = date,i=Month,j=Date, time_slot=time_slot, rng = _range)
            print(tweet_time)
            counter = 0
            for response in org_tweet['batches']:
                for tweets in response['data']:
                    
                    for dt in tweet_time:
                        tweet_time_loops = tweets['created_at']

                        # date_present = tweet_time_loops[0:10]
                        # time_sq = datetime.strptime(tweet_time_loops[11:19],'%H:%M:%S').time()
                        # tweet_time = f"{date_present} {time_sq}"
                        # dt = f"{dt[0:10]} {datetime.strptime(dt[11:19],'%H:%M:%S').time()}"
                        # print(tweet_time_loops, " ", dt)
                        # # print(tweet_time, type(tweet_time))
                        # tweet_time = temp_time[0:10]
                        # if dt == tweet_time:
                        
                        if almost_matches(dt, tweet_time_loops) and counter != _range:
                            author_id = tweets['author_id']
                            id = tweets['conversation_id']
                            text = tweets['text']
                            retweet_count = tweets['public_metrics']['retweet_count']
                            reply_count = tweets['public_metrics']['reply_count']
                            like_count = tweets['public_metrics']['like_count']

                            res = [sno, author_id, id, text, like_count, reply_count, retweet_count]
                            csvWriter.writerow(res)
                            print(f"Done {counter}")
                            counter += 1
                            sno += 1

                        elif almost_matches_per_30_min(dt, tweet_time_loops) and counter != _range:
                            author_id = tweets['author_id']
                            id = tweets['conversation_id']
                            text = tweets['text']
                            retweet_count = tweets['public_metrics']['retweet_count']
                            reply_count = tweets['public_metrics']['reply_count']
                            like_count = tweets['public_metrics']['like_count']

                            res = [sno, author_id, id, text, like_count, reply_count, retweet_count]
                            csvWriter.writerow(res)
                            print(f"Done {counter}")
                            counter += 1 
                            sno += 1                      

            time_slot += 1            
    
    print("Total Tweets in Train Split: ",sum_of_range)
    csvFile_1.close()

def test_split():
    csvFile_1 = open(train_split_file, "r", newline="", encoding='utf-8')
    csvFile_2 = open(test_split_file, "a", newline="", encoding='utf-8')
    csvreader = pd.read_csv(csvFile_1)
    csvWriter = csv.writer(csvFile_2)

    ids = csvreader['ID']
    sno = 1
    for response in org_tweet['batches']:
        for tweets in response['data']:
            
            not_in_train = True
            for id in ids:
                if(id == tweets['conversation_id']):
                    not_in_train = False
                    break

            
            if not_in_train:
                author_id = tweets['author_id']
                id = tweets['conversation_id']
                text = tweets['text']
                retweet_count = tweets['public_metrics']['retweet_count']
                reply_count = tweets['public_metrics']['reply_count']
                like_count = tweets['public_metrics']['like_count']

                res = [sno, author_id, id, text, like_count, reply_count, retweet_count]
                csvWriter.writerow(res)
                print(f"Test_data : {sno}")
                sno += 1

if __name__ == "__main__":

    if not(os.path.exists(test_split_file) and os.path.exists(train_split_file)):
       train_test_csv_header()

    if (os.path.exists(test_split_file) and os.path.exists(train_split_file)):
       train_split()
       test_split()


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