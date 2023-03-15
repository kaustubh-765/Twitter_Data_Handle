import json
import csv
import datetime
import dateutil.parser
import unicodedata

json_file = open('Twitter_Data_Handle/Kaustubh-TwitterScript/tweets_Diyi_Yang.json')


jr = json.load(json_file)

#print(jr['batches'][0]['data'][0]['lang'])


#print(jr['batches'][0]['data'][0]['text'])


#print(jr['batches'][0]['data'][0]['entities'])

#print(jr['batches'][0]['data'][0]['entities']['mentions'][0]['start'])

# print(jr['batches'][0]['data'][0]['entities']['mentions'][0]['end'])

# # attachments = []
# urls = []
# for tweet in jr['batches'][0]['data']:
#     if 'mentions' in tweet['entities']:
#         for i in (tweet['entities']['mentions']):
# #           #print(i['mentions'][0]['start'])
#             # ur = i['url']
#             # pp = i['expanded_url']
#             # op = i['display_url']

#             # lo = [ur, pp, op]

#             urls.append(i)

# for i in urls:
#     print(i)

        # if 'urls' in i:
        #     print(i['urls'])
        #print(i)

# for i in attachments:
#     print(i)


#print(jr['batches'][0]['includes']['users'][0]['created_at'])

count = 0

while count < 6:
    for i in jr['batches'][count]['data']:

        print((i['conversation_id']))
        # created_at = dateutil.parser.parse(i['created_at'])
        # name = i['name']
        # username = i['username']
        # description = i['description']
        # protected = i['protected']
        # id = i['id']
        # verified = i['verified']
        


    count += 1


context_annotations  = "Hello2"
conversation_id  = "Hello3"

withheld = "Hello"
attachments_poll_ids = "Hello"
attachments_media_keys = "Hello"
author_id_1 = "Hello"

geo_place_id = "Hello"
in_reply_to_user_id_2 = "Hello" 
referenced_tweets_id = "Hello"
referenced_tweets_id_author_id = "Hello"
duration_ms = "Hello"
height = "Hello"
media_key = "Hello"
preview_image_url = "Hello"
typ = "Hello"
url = "Hello"
width = "Hello"
public_metrics_2  = "Hello",
alt_text = "Hello"
variants = "Hello"
contained_within = "Hello"
country = "Hello"
country_code = "Hello"
full_name = "Hello"
geo_2 = "Hello"
place_field_id = "Hello"
name_1 = "Hello"
place_type = "Hello"
duration_minutes = "Hello"
end_datetime = "Hello"
pll_fields_id = "Hello"
options = "Hello"
voting_status = "Hello"
created_at_2 = "Hello"
description = "Hello"
entities_2 = "Hello"
user_field_id = "Hello"
location = "Hello"
name_2 = "Hello"
pinned_tweet_id = "Hello"
profile_image_url = "Hello"
protected = "Hello"
public_metrics_2 = "Hello"
url_2 = "Hello"
username = "Hello"
verified = "Hello"
withheld_2  = "Hello"