import json

def print_tweet_counts_by_date_and_total_tweets():
	input_file_name = "Twitter_Data_Handle/Kaustubh-TwitterScript/tweets_Diyi_Yang.json"
	# 'Original_tweets_in_json.json'
	# "C:/Users/LNMIIT/Desktop/Data/Afghanistan-2021/April-2021/Afghanistan-tweets-April30-original.json"  # relative path
	output_file_name_by_date = "original_tweet_counts_by_date_April30.txt"  # relative path
	output_file_name_total_tweets = "original_tweets_count_April30.txt"

	with open(input_file_name, 'r') as input_file:
		json_object = json.load(input_file)

	
	frequency = {}
	for batch in json_object["batches"]:
		if "data" not in batch:
			continue
		for tweet in batch["data"]:
			if "created_at" in tweet:
				if tweet['lang'] == 'en':
					iso_date = tweet["created_at"]
					date = ""
					for character in iso_date:
						if(character == 'T'):
							break
						date += character
					frequency[date] = frequency.get(date, 0) + 1
			
	input_file.close()

	output_file = open(output_file_name_by_date, "w")
	for date, count in frequency.items():
		print(date, ": ", count, sep='', file=output_file)
	output_file.close()
	
	total_frequency = 0
	for key, value in frequency.items():
		total_frequency += value
	output_file = open(output_file_name_total_tweets, "w")
	print(total_frequency, file=output_file)
	output_file.close()

if __name__ == "__main__":
	print_tweet_counts_by_date_and_total_tweets()
