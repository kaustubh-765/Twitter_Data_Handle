import json
import requests
import os
import time
from time import localtime


# Put bearer token here
bearer_token = "SOME_TOKEN"

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


# Opening the JSON file to access data


file_name = "Original_tweets_in_json.json"


json_file = open(file_name)
json_response = json.load(json_file)

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
        response = requests.request("GET", url, auth=bearer_oauth, params=params)
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


def tweets_of_in_reply_to_tweet_id(id):
    print(id)
    query_string = "in_reply_to_tweet_id:" + id
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
    #print(result)

    folder_name = "Reply_to"
    output_file_name = folder_name + "/" +"replied_to_" + id + ".json"
    print(output_file_name)
    with open(output_file_name, "w", encoding='utf-8') as output_file:
        output_file.write(json.dumps(result, indent=4))

    print("exiting")


def tweets_of_retweets_of_tweet_id(id):
    print(id)
    query_string = "retweets_of_tweet_id:" + id
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
    #print(result)
    
    folder_name = "Retweet"
    output_file_name = folder_name + "/" + "retweets_" + id + ".json"

    print(output_file_name)
    with open(output_file_name, "w", encoding='utf-8') as output_file:
        output_file.write(json.dumps(result, indent=4))


def main():
    
    try:
        os.mkdir("Retweet")
    except OSError as error:
        print(error)

    try:
        os.mkdir("Reply_to")
    except OSError as error:
        print(error)



    print("1. To get the replied to tweets of the original tweets")
    print("2. To get the retweeted tweets of the original tweets")
    choice = int(input("Enter your choice:"))


    for response in json_response['batches']:
        for tweet in response['data']:
            if choice == 1 and tweet['public_metrics']['reply_count'] != 0:
                tweets_of_in_reply_to_tweet_id(tweet['conversation_id'])
            
            elif choice == 2 and tweet['public_metrics']['retweet_count'] != 0:
                tweets_of_retweets_of_tweet_id(tweet['conversation_id'])


if __name__ == "__main__":
    main()