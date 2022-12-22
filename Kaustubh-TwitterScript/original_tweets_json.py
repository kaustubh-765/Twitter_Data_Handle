import json
import os


file_name = "Twitter_Data_Handle/Kaustubh-TwitterScript/tweets_Diyi_Yang.json"

json_file = open(file_name)

json_response = json.load(json_file)


def original_json(json_response):
    
    temp = []
    data = {"data":''}
    mult_data = []
    final_batch = {}

    for response in json_response['batches']:
        for tweet in response['data']:
            referenced_tweets = ""
            if ('referenced_tweets' in tweet):
                for i in tweet['referenced_tweets']:
                    oi = i['type']
                    referenced_tweets = oi
            else:
                referenced_tweets = ""

            if (referenced_tweets == "" and tweet["id"] == tweet["conversation_id"]):
                temp.append(tweet)
            
        data["data"] = temp

        mult_data.append(data)

    final_batch["batches"] = mult_data
    output_file_name = "Original_tweets_in_json.json"
    with open(output_file_name, "w", encoding='utf-8') as output_file:
        output_file.write(json.dumps(final_batch, indent=4))
    print("Done")

    
    


if __name__ == "__main__":
    original_json(json_response)