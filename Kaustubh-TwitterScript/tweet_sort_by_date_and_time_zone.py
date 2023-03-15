import json
from datetime import datetime

time_zones = ["00:00:00","04:00:00","08:00:00","12:00:00","16:00:00","20:00:00", "23:59:59"]

i = 0

while i<7:
	time_zones[i] = datetime.strptime(time_zones[i], '%H:%M:%S').time()
	i = i+1



def get_total_dates():

	tweet_dates = []
	input_file_name = 'Original_tweets_in_json.json'
	with open(input_file_name, 'r') as input_file:
		json_object = json.load(input_file)

	for batch in json_object["batches"]:
		if "data" not in batch:
			continue
		for tweet in batch["data"]:
			if "created_at" in tweet:
				if tweet['lang'] == 'en':
					iso_date = tweet["created_at"]
					date = iso_date[0:10]

					tweet_dates.append(date)

	tweet_dates = set(tweet_dates)
	tweet_dates = list(tweet_dates)

	input_file.close()

	return tweet_dates



print(type(time_zones[0]))

def print_tweet_counts_by_date_and_total_tweets():

	tweet_dates = get_total_dates()


	input_file_name = 'Original_tweets_in_json.json'

	# "Twitter_Data_Handle/Kaustubh-TwitterScript/tweets_Diyi_Yang.json"
	# "C:/Users/LNMIIT/Desktop/Data/Afghanistan-2021/April-2021/Afghanistan-tweets-April30-original.json"  # relative path
	
    
	with open(input_file_name, 'r') as input_file:
		json_object = json.load(input_file)

	for dt in tweet_dates:
		output_file_name_by_date = f"Original_tweets_count_by_date_and_time_zone_{dt}.txt"
		output_file_name_total_tweets = f"Original_tweets_count_{dt}.txt"
		
		output_file = open(output_file_name_by_date, "w")
		
		total_frequency = 0

		frequency = {}
		print("Date: ",dt, file=output_file)
		print("\n\n", file=output_file)	
		print("Time Zone:" , time_zones[0], file=output_file)

		for batch in json_object["batches"]:
			if "data" not in batch:
				continue
			for tweet in batch["data"]:
				if "created_at" in tweet:
					if tweet['lang'] == 'en':
						iso_date = tweet["created_at"]
						date = iso_date[0:10]
						time_sq = datetime.strptime(iso_date[11:19],'%H:%M:%S').time()
						# time_sq = iso_date[11:]
						print(time_sq)
						print(date)
						if (date == dt) and (time_sq >= time_zones[0]) and (time_sq < time_zones[1]):
							frequency[time_sq] = frequency.get(time_sq, 0) + 1 

		for date, count in frequency.items():
			print(date, ": ", count, sep='', file=output_file)

		for key, value in frequency.items():
			total_frequency += value

		frequency = {}
		
		print("\n\n", file=output_file)	
		print("Time Zone:" , time_zones[1], file=output_file)

		for batch in json_object["batches"]:
			if "data" not in batch:
				continue
			for tweet in batch["data"]:
				if "created_at" in tweet:
					if tweet['lang'] == 'en':
						iso_date = tweet["created_at"]
						date = iso_date[0:10]
						time_sq = datetime.strptime(iso_date[11:19],'%H:%M:%S').time()
						print(time_sq)
						print(date)
						if (date == dt) and(time_sq >= time_zones[1]) and (time_sq < time_zones[2]):
							frequency[time_sq] = frequency.get(time_sq, 0) + 1 

		for date, count in frequency.items():
			print(date, ": ", count, sep='', file=output_file)

		for key, value in frequency.items():
			total_frequency += value

		frequency = {}
		
		print("\n\n", file=output_file)	
		print("Time Zone:" , time_zones[2], file=output_file)

		for batch in json_object["batches"]:
			if "data" not in batch:
				continue
			for tweet in batch["data"]:
				if "created_at" in tweet:
					if tweet['lang'] == 'en':
						iso_date = tweet["created_at"]
						date = iso_date[0:10]
						time_sq = datetime.strptime(iso_date[11:19],'%H:%M:%S').time()
						print(time_sq)
						print(date)
						if (date == dt) and(time_sq >= time_zones[2]) and (time_sq < time_zones[3]):
							frequency[time_sq] = frequency.get(time_sq, 0) + 1 

		for date, count in frequency.items():
			print(date, ": ", count, sep='', file=output_file)

		for key, value in frequency.items():
			total_frequency += value

		frequency = {}
		
		print("\n\n", file=output_file)	
		print("Time Zone:" , time_zones[3], file=output_file)

		for batch in json_object["batches"]:
			if "data" not in batch:
				continue
			for tweet in batch["data"]:
				if "created_at" in tweet:
					if tweet['lang'] == 'en':
						iso_date = tweet["created_at"]
						date = iso_date[0:10]
						time_sq = datetime.strptime(iso_date[11:19],'%H:%M:%S').time()
						print(time_sq)
						print(date)
						if (date == dt) and(time_sq >= time_zones[3]) and (time_sq < time_zones[4]):
							frequency[time_sq] = frequency.get(time_sq, 0) + 1 

		for date, count in frequency.items():
			print(date, ": ", count, sep='', file=output_file)

		for key, value in frequency.items():
			total_frequency += value


		frequency = {}

		print("\n\n", file=output_file)	
		print("Time Zone:" , time_zones[4], file=output_file)

		for batch in json_object["batches"]:
			if "data" not in batch:
				continue
			for tweet in batch["data"]:
				if "created_at" in tweet:
					if tweet['lang'] == 'en':
						iso_date = tweet["created_at"]
						date = iso_date[0:10]
						time_sq = datetime.strptime(iso_date[11:19],'%H:%M:%S').time()
						print(time_sq)
						print(date)
						if (date == dt) and(time_sq >= time_zones[4]) and (time_sq < time_zones[5]):
							frequency[time_sq] = frequency.get(time_sq, 0) + 1 

		for date, count in frequency.items():
			print(date, ": ", count, sep='', file=output_file)

		for key, value in frequency.items():
			total_frequency += value



		frequency = {}
		print("\n\n", file=output_file)	
		print("Time Zone:" , time_zones[5], file=output_file)

		for batch in json_object["batches"]:
			if "data" not in batch:
				continue
			for tweet in batch["data"]:
				if "created_at" in tweet:
					if tweet['lang'] == 'en':
						iso_date = tweet["created_at"]
						date = iso_date[0:10]
						time_sq = datetime.strptime(iso_date[11:19],'%H:%M:%S').time()
						print(time_sq)
						print(date)
						if (date == dt) and (time_sq >= time_zones[5]) and (time_sq < time_zones[6]):
							frequency[time_sq] = frequency.get(time_sq, 0) + 1 

		for date, count in frequency.items():
			print(date, ": ", count, sep='', file=output_file)

		for key, value in frequency.items():
			total_frequency += value

		
		output_file.close()
		input_file.close()

		
		output_file = open(output_file_name_total_tweets, "w")
		print("Date: ",dt, file=output_file)
		print(total_frequency, file=output_file)
		output_file.close()

if __name__ == "__main__":
	print_tweet_counts_by_date_and_total_tweets()
	