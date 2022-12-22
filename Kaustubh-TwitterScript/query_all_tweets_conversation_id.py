import requests
import json
import time
from time import localtime

# Put bearer token here
bearer_token = "AAAAAAAAAAAAAAAAAAAAAJF6IQEAAAAARkYD8uKFUDZT0R%2BWzdkYNfc9bFw%3DWU7slkHso0Kn6U7vivUaK3aGrHnHm19blQ8vCoXabA2vFV34DU"

search_url = "https://api.twitter.com/2/tweets/search/all"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
# See this link for more params:
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all

tweet_fields = 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld'
expansions = 'attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id'
media_fields = 'duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,alt_text,variants'
place_fields = 'contained_within,country,country_code,full_name,geo,id,name,place_type'
poll_fields = 'duration_minutes,end_datetime,id,options,voting_status'
user_fields = 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
# change max results
# set end_time
# set start time YYYY-MM-DDTHH:mm:ssZ
# TODO: max_results = 500?

# query_string_conversation_id = 'conversation_id:1334987486343299072'
# 'has:geo' for only geo tagged tweets, 'lang:', 'is:quote'

# query_string_keywords_and_hashtags = 'from:MagnusCarlsen'

# input_file_names = [
#     "tweets_aliciagarza.json",
#     "tweets_Amira_Adawe.json",
#     "tweets_anandmahindra.json",
#     "tweets_anishgiri.json",
#     "tweets_AnnaRogers.json"
# ]  # relative path

input_file_name = [ 'Twitter_Data_Handle/Kaustubh-TwitterScript/tweets_Diyi_Yang.json' ]

query_string = ''
start_time = '2006-03-21T00:00:00Z'
end_time = '2022-09-16T23:59:59Z'

query_params = {'query': query_string, 'start_time': start_time, 'end_time': end_time, 'expansions': expansions, 'media.fields': media_fields, 'place.fields': place_fields, 'poll.fields': poll_fields, 'tweet.fields': tweet_fields, 'max_results': 100, 'user.fields': user_fields}

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r

def connect_to_endpoint(url, params):
    while True:
        response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
        if response.status_code == 429:
            current_time = int(time.time())
            reset_time = int(response.headers["x-rate-limit-reset"])
            remaining_seconds = reset_time - current_time
            print("Sleeping for", remaining_seconds / 60, "minutes. Current Time = ", localtime())
            time.sleep(remaining_seconds)
            print("Awake. Current Time = ", localtime())
        elif response.status_code != 200:
            raise Exception(response.status_code, response.text)
        else:
            return response.json()

def print_replies(input_file_name):
    with open(input_file_name, 'r', encoding='utf-8') as input_file:
        json_object = json.load(input_file)

    for batch in json_object["batches"]:
        if "data" in batch:
            for tweet in batch["data"]:
                if tweet["id"] == tweet["conversation_id"]:
                    is_retweet = False
                    if 'referenced_tweets' in tweet and len(tweet["referenced_tweets"]) == 1:
                        if(tweet["referenced_tweets"][0]["type"] == "retweeted"):
                            is_retweet = True
                    if (is_retweet):
                        print_replies_of_conversation_id_retweeted(tweet["id"], input_file_name, 
                            tweet["referenced_tweets"][0]["id"], tweet["author_id"])
                    else:
                        print_replies_of_conversation_id(tweet["id"], input_file_name)

def print_replies_of_conversation_id_retweeted(id_file_name, input_file_name, id, author_id):
    print(id)
    query_string = "conversation_id:" + id
    query_params["query"] = query_string

    json_response = connect_to_endpoint(search_url, query_params)
    print("Fetched response.")

    temp = []

    # print(json.dumps(json_response["data"], indent=4))

    for tweet in json_response["data"]:
        has_mention = False
        if("entities" in tweet):
            if("mentions" in tweet["entities"]):
                if("id" in tweet["entities"]["mentions"]):
                    print("Hi")
                    if(tweet["entities"]["mentions"]["id"] == author_id):
                        has_mention = True
        if(has_mention):
            temp.append(tweet)

    json_response["data"] = temp

    data = [json_response]
    while 'next_token' in json_response['meta']:
        query_params['next_token'] = json_response['meta']['next_token']
        json_response = connect_to_endpoint(search_url, query_params)
        print("Fetched response.")

        temp = []

        for tweet in json_response["data"]:
            has_mention = False
            if("entities" in tweet and tweet["entities"]):
                if("mentions" in tweet["entities"] and "username" in tweet["entities"]["mentions"]):
                    if(tweet["entities"]["mentions"]["username"] == author_id):
                        has_mention = True
            if(has_mention):
                temp.append(tweet)

        json_response["data"] = temp

        data.append(json_response)

    result = {"batches": data}
    folder_name = input_file_name[:-5]
    print(folder_name)
    output_file_name = folder_name + "/" + id_file_name + ".json"
    print(output_file_name)
    with open(output_file_name, "w", encoding='utf-8') as output_file:
        output_file.write(json.dumps(result, indent=4))

    print("exiting")

def print_replies_of_conversation_id(id):
    print(id)
    query_string = "conversation_id:" + id
    query_params["query"] = query_string

    json_response = connect_to_endpoint(search_url, query_params)
    print("Fetched response.")
    data = [json_response]
    while 'next_token' in json_response['meta']:
        query_params['next_token'] = json_response['meta']['next_token']
        json_response = connect_to_endpoint(search_url, query_params)
        print("Fetched response.")
        data.append(json_response)

    result = {"batches": data}
    print(result)
    #folder_name = input_file_name[:-5]
    #print(folder_name)
    # output_file_name = folder_name + "/" + id + ".json"
    # print(output_file_name)
    # with open(output_file_name, "w", encoding='utf-8') as output_file:
    #     output_file.write(json.dumps(result, indent=4))

    print("exiting")

if __name__ == "__main__":
    #for input_file_name in input_file_names:
    #print_replies("Twitter_Data_Handle/Kaustubh-TwitterScript/tweets_Diyi_Yang.json")
    # print_replies_of_conversation_id_retweeted("123", input_file_names[0], "1579307582078222336", "1556654184732233729")

    print_replies_of_conversation_id("1565002386879328257")