import json
import csv
import os


json_file = open('Afghanistan-tweets-may-original.json')
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
        "","","","","","","","","","Replies 1st + 2nd"
    ])

    csvWriter.writerow([
       "SNo.","Tweet Id","","Tweet Text","","Language", "No. of Likes", "No of Replies" ,"No. of Retweets", "Reply"
    ])

    csvFile.close()


def retweet_replies(id):
    
    file_retweet_name = "Retweet/" + "retweets_"+id+".json"

    #Error -- File not taking texts from all the other tweets, only one tweet text is being added.

    if (not (os.path.exists(file_retweet_name))):
        print("The path : "+file_retweet_name+" Doesn't exist")
        return []

    js_fl = open(file_retweet_name)
    js_rsps = json.load(js_fl)

    reply_2nd_hop = []

    for rspn in js_rsps['batches']:
        for twets in rspn['data']:
            dir_path = "Retweet/Replies/" + id
            input_file_name = dir_path + "/replied_to_" + twets['conversation_id'] + "__" + id + ".json"
            print(input_file_name)
            if (not (os.path.exists(input_file_name))):
                print("The path : "+input_file_name+" Doesn't exist")
                continue

            j_r = open(input_file_name)
            j_r_s = json.load(j_r)

            for reply_response in j_r_s['batches']:
                for reply_tweet in reply_response['data']:
                    reply_2nd_hop.append(reply_tweet['text'])
                    reply_2nd_hop.append("")

    #print(reply_2nd_hop)
    return reply_2nd_hop

def reply_to_file(id):
    
    file_reply_name = "Reply_to/" + "replied_"+id+".json"

    #print(file_reply_name)Reply_to

    if (not (os.path.exists(file_reply_name))):
        #print("The path : "+file_reply_name+" Doesn't exist")
        return []

    json_file = open(file_reply_name)
    json_rspnse = json.load(json_file)

    reply_1st_hop = []

    for re_response in json_rspnse['batches']:
        if ("data" in re_response):
            for twts in re_response["data"]:
                #if (twts['public_metrics']['reply_count'] != 0):
                text_1 = twts['text']
                reply_1st_hop.append(text_1)
                reply_1st_hop.append("")


    print(file_reply_name)
    #print(reply_1st_hop)
    
    return reply_1st_hop



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
            lang = tweet['lang']
            reply_count = tweet['public_metrics']['reply_count']
            
            reply_1st_hop = reply_to_file(tweet['conversation_id'])
            #reply_2nd_hop = retweet_replies(tweet['conversation_id'])
            reply_2nd_hop = []           
                
            #print(text)
            res = [counter, id, text, "", "", lang ,like_count, reply_count ,retweet_count] +  reply_1st_hop + [ "", "Replies of Retweet", "" ] +  reply_2nd_hop + [""]

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

