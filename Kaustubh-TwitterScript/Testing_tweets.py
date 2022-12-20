import requests
import json
import time

# Put bearer token here
bearer_token = "AAAAAAAAAAAAAAAAAAAAAJF6IQEAAAAARkYD8uKFUDZT0R%2BWzdkYNfc9bFw%3DWU7slkHso0Kn6U7vivUaK3aGrHnHm19blQ8vCoXabA2vFV34DU"

#search_url = "https://api.twitter.com/2/tweets/search/all"

search_url =  'https://api.twitter.com/2/tweets?ids=1225917697675886593&tweet.fields=author_id,conversation_id,created_at,in_reply_to_user_id,referenced_tweets&expansions=author_id,in_reply_to_user_id,referenced_tweets.id&user.fields=name,username'

#  1488623432271024130

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

query_string_keywords_and_hashtags = '#taliban OR #afghanistan OR #Afghanistan OR #Taliban'

#query_string_example = 'PCOS OR #PCOS'

#query_params = {'query': query_string_keywords_and_hashtags, 'start_time': '2022-02-01T00:00:00Z', 'end_time': '2022-02-01T23:59:59Z', 'expansions': expansions, 'media.fields': media_fields, 'place.fields': place_fields, 'poll.fields': poll_fields, 'tweet.fields': tweet_fields, 'max_results': 100, 'user.fields': user_fields}

query_params = {  'ids': '1605086055832915968'  , 'expansions': expansions, 'media.fields': media_fields, 'place.fields': place_fields, 'poll.fields': poll_fields, 'tweet.fields': tweet_fields, 'max_results': 100, 'user.fields': user_fields}

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
            print("Sleeping for", remaining_seconds / 60, "minutes.")
            time.sleep(remaining_seconds)
        elif response.status_code != 200:
            raise Exception(response.status_code, response.text)
        else:
            return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    print("Fetched response.")
    data = [json_response]
    
    while 'next_token' in json_response['meta']:
        query_params['next_token'] = json_response['meta']['next_token']
        json_response = connect_to_endpoint(search_url, query_params)
        print("Fetched response.")
        print(json.dumps(json_response, indent=4, sort_keys=True))
        data.append(json_response)

    result = {"batches": data}
    with open("Ukraine-Russia-War-tweets-feb.json", "w", encoding='utf-8') as output_file:
        output_file.write(json.dumps(result, indent=4))

if __name__ == "__main__":
    #main()
    response = response = requests.request("GET", search_url, auth=bearer_oauth)
    json_response = response.json()
    data = [json_response]
    print("Fetched response.")
    print(json.dumps(json_response, indent=4, sort_keys=True))
