import json
import csv
import datetime
import dateutil.parser
import unicodedata
import os


json_file = open('Twitter_Data_Handle/Kaustubh-TwitterScript/tweets_Diyi_Yang.json')

json_response = json.load(json_file)


def create_csv_file():
    csvFile = open("test_data.csv", "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow([
        'Sno.',
        'id',
        'author_id', 
        'conversation_id',
        'created_at',
        'geo',
        'lang',
        'mentions',
        'url', 
        'annotations',
        'cashtag',
        'hashtag',
        'in_reply_to_user_id',
        'retweet_count',
        'reply_count',
        'like_count',
        'quote_count',
        'attachments_media_keys',
        'attachments_poll_ids',
        'possibly_sensitive',
        'referenced_tweets',
        'reply_settings',
        'source',
        'text',
        'context_annotations'
         ])
    csvFile.close()

def append_to_csv(json_response):

    #A counter variable
    counter = 1
    count = 0
    fileName = 'test_data.csv'

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    
    while count<6:

        
        for tweet in json_response['batches'][count]['data']:
            
            # We will create a variable for each since some of the keys might not exist for some tweets
            # So we will account for that

            # Tweet fields
            # 1. Author ID
            author_id = tweet['author_id']

            #in_reply_to_user_id
            in_reply_to_user_id = ""
            if 'in_reply_to_user_id' in tweet:
                in_reply_to_user_id = tweet['in_reply_to_user_id']
            else:
                in_reply_to_user_id = ""

            #conversation_id
            conversation_id = tweet['conversation_id']

            #referenced_tweets
            referenced_tweets = ""
            type = []
            if ('referenced_tweets' in tweet):
                for i in tweet['referenced_tweets']:
                    oi = i['type']
                    po = i['id']
                    referenced_tweets = [oi, po]
                    type.append(oi) 
            else:
                referenced_tweets = ""

            #attachments
            attachments_media_keys = []
            attachments_poll_ids = []
            if 'attachments' in tweet:
                if 'media_keys' in tweet['attachments']:
                    for i in (tweet['attachments']['media_keys']):
                        attachments_media_keys.append(i)
                
                if 'poll_ids' in tweet['attachments']:
                    for i in (tweet['attachments']['poll_ids']):
                        attachments_poll_ids.append(i)

            #possibly senstivity
            possibly_sensitive = tweet['possibly_sensitive']

            #reply settings
            reply_settings = tweet['reply_settings']

            # Time created
            created_at = dateutil.parser.parse(tweet['created_at'])

            # Geolocation
            geo = " "
            if ('geo' in tweet):   
                geo = tweet['geo']['place_id']
            else:
                geo = " "

            # Tweet ID
            id = tweet['id']

            # Language
            lang = tweet['lang']

            #  Tweet metrics
            retweet_count = tweet['public_metrics']['retweet_count']
            reply_count = tweet['public_metrics']['reply_count']
            like_count = tweet['public_metrics']['like_count']
            quote_count = tweet['public_metrics']['quote_count']

            #public_metrics = [retweet_count, reply_count, like_count, quote_count]
            
            # 7. source
            source = tweet['source']

            
            # 8. Tweet text
            text = tweet['text']

            #entities:
            mentions = []
            url = []
            annotations = []
            hashtag = []
            cashtag = []

            if 'entities' in tweet:

                if 'mentions' in tweet['entities']:
                    for i in (tweet['entities']['mentions']):
                        io = i['username']
                        pu =  i['id']
                        kl = [io, pu]
                        mentions.append(kl)

                if 'urls' in tweet['entities']:
                    for i in (tweet['entities']['urls']):
                        url.append(i)

                if 'annotations' in tweet['entities']:
                    for i in (tweet['entities']['annotations']):
                        oi = i['probability']
                        po = i['type']
                        lo = i['normalized_text']
                        lkj = [oi, po, lo]
                        annotations.append(lkj)

                if 'hashtags' in tweet['entities']:
                    for i in (tweet['entities']['hashtags']):
                        hashtag.append(i['tag'])
                
                if 'cashtags' in tweet['entities']:
                    for i in (tweet['entities']['cashtags']):
                        cashtag.append(i['tag'])

           
            #context annotations

            context_annotations = []
            if 'context_annotations' in tweet:
                for i in tweet['context_annotations']:
                    io = i['domain']
                    oi = i['entity']

                    po = [io, oi]

                    context_annotations.append(po)

            for i in type:
                if (i == "replied_to"):
                    # Assemble all data in a list
                    res = [
                        counter,
                        id,
                        author_id , 
                        conversation_id ,
                        created_at ,
                        geo,
                        lang,
                        mentions,
                        url, 
                        annotations,
                        cashtag,
                        hashtag,
                        in_reply_to_user_id,
                        retweet_count,
                        reply_count,
                        like_count,
                        quote_count,
                        attachments_media_keys,
                        attachments_poll_ids,
                        possibly_sensitive,
                        referenced_tweets,
                        reply_settings,
                        source,
                        text,
                        context_annotations
                    ]
                    
                    # Append the result to the CSV file
                    csvWriter.writerow(res)
                    counter += 1
            
        count += 1
        # When done, close the CSV file
    csvFile.close()
    # Print the number of tweets for this iteration    
    print("# of Tweets added from this response: ", counter-1) 


if not(os.path.exists('test_data.csv')):
    create_csv_file()

append_to_csv(json_response = json_response)

#print(json_response['batches'])
#print(json_response['batches'][0]['data'])

"""
Sno
attachments
author_id 
context_annotations 
conversation_id 
created_at 
entities
geo
id
in_reply_to_user_id
lang
public_metrics
possibly_sensitive
referenced_tweets
reply_settings
source
text
withheld
attachments_poll_ids
attachments_media_keys
author_id_1
entities.mentions_username
geo_place_id
in_reply_to_user_id
referenced_tweets_id
referenced_tweets_id_author_id
duration_ms
height
media_key
preview_image_url
typ
url
width
public_metrics
alt_text
variants
contained_within
country
country_code
full_name
geo_2
place_field_id
name_1
place_type
duration_minutes
end_datetime
pll_fields_id
options
voting_status,
created_at
description
entities
user_field_id
location
name_2
pinned_tweet_id
profile_image_url
protected
public_metrics
url_2
username
verified
withheld
"""


# def getitems(obj):

#   def getkeys(obj, stack):
#     for k, v in obj.items():
#       k2 = ([k] if k else []) + stack # don't return empty keys
#       if v and isinstance(v, dict):
#         for c in getkeys(v, k2):
#           yield c
#       else: # leaf
#         yield k2

#   def getvalues(obj):
#     for v in obj.values():
#       if not v: continue
#       if isinstance(v, dict):
#         for c in getvalues(v):
#           yield c
#       else: # leaf
#         yield v if isinstance(v, list) else [v]

#   return list(getkeys(obj,[])), list(getvalues(obj))

# print(getitems(json_response))