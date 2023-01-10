import json
import csv
import os


json_file = open('E:/Twitter/Original_tweets_in_json.json')
json_response = ""

try:
    json_response = json.load(json_file)
except OSError as error:
   print("Try Again!")
   print(error)
   os._exit(os.EX_OK)

def create_csv_file():
    csvFile = open("Original_tweets_Arrangement.csv", "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    csvWriter.writerow([
        "","","","","","",""
    ])

    csvWriter.writerow([
       "SNo.","Tweet Id","","Tweet Text","", "No. of Likes", "No. of Retweets"  
    ])

    csvFile.close()

def append_to_CSV(json_response):
    
    counter = 1
    fileName = 'Original_tweets_Arrangement.csv'

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    
    for respon in json_response['batches']:
        for tweet in respon['data']:

            id = tweet['id']
            text = tweet['text']
            like_count = tweet['public_metrics']['like_count']
            retweet_count = tweet['public_metrics']['retweet_count']

            fl_name = "Reply/" + "retweets_"+tweet['conversation_id']+".json"

            if (not (os.path.exists(fl_name))):
                continue

            json_file = open(fl_name)
            json_rspnse = json.load(json_file)



            for re_response in json_rspnse['batches']:
                for twts in re_response['data']:
                    if (twts['public_metrics']['reply_count'] != 0):
                        tweets_of_in_reply_to_tweet_id(twts['conversation_id'], tweet['conversation_id'])


            res = [counter, id, text, "", "", like_count, retweet_count]

            csvWriter.writerow(res)
            counter += 1        

    
    csvFile.close()
    print("No. of lines added to file :", counter-1)

def main():
    if not(os.path.exists("Original_tweets_Arrangement.csv")):
        create_csv_file()

    append_to_CSV(json_response=json_response)


if __name__ == "__main__":
    main()

