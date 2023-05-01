import json
from datetime import datetime


def handle_time_zone():
	time_zones = ["00:00:00","06:00:00","12:00:00","18:00:00", "23:59:59"]

	i = 0

	while i<5:
		time_zones[i] = datetime.strptime(time_zones[i], '%H:%M:%S').time()
		i = i+1
	
	return time_zones 


def get_total_dates(input_file_name):

	tweet_dates = []
	# input_file_name = './data/Afghanistan-tweets-April24-original.json'
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



def print_tweet_counts_by_date_and_total_tweets(dt, input_file_name):

	
	time_zones = handle_time_zone()
	freq_on_day = []
	tot_per_head = 0
    
	with open(input_file_name, 'r') as input_file:
		json_object = json.load(input_file)

		frequency = {}

	tot_per_head = 0

	for batch in json_object["batches"]:
		if "data" not in batch:
			continue
		for tweet in batch["data"]:
			if "created_at" in tweet:
				if tweet['lang'] == 'en':
					iso_date = tweet["created_at"]
					date = iso_date[0:10]
					time_sq = datetime.strptime(iso_date[11:19],'%H:%M:%S').time()
					if (date == dt) and (time_sq >= time_zones[0]) and (time_sq < time_zones[1]):
						frequency[time_sq] = frequency.get(time_sq, 0) + 1 

	for key, value in frequency.items():
			tot_per_head += value
	
	freq_on_day.append(tot_per_head)

	frequency = {}
	

	for batch in json_object["batches"]:
		if "data" not in batch:
			continue
		for tweet in batch["data"]:
			if "created_at" in tweet:
				if tweet['lang'] == 'en':
					iso_date = tweet["created_at"]
					date = iso_date[0:10]
					time_sq = datetime.strptime(iso_date[11:19],'%H:%M:%S').time()
					if (date == dt) and(time_sq >= time_zones[1]) and (time_sq < time_zones[2]):
						frequency[time_sq] = frequency.get(time_sq, 0) + 1 
	
	tot_per_head = 0

	for key, value in frequency.items():
		tot_per_head += value

	freq_on_day.append(tot_per_head)

	frequency = {}

	for batch in json_object["batches"]:
		if "data" not in batch:
			continue
		for tweet in batch["data"]:
			if "created_at" in tweet:
				if tweet['lang'] == 'en':
					iso_date = tweet["created_at"]
					date = iso_date[0:10]
					time_sq = datetime.strptime(iso_date[11:19],'%H:%M:%S').time()
					if (date == dt) and(time_sq >= time_zones[2]) and (time_sq < time_zones[3]):
						frequency[time_sq] = frequency.get(time_sq, 0) + 1 

	tot_per_head = 0

	for key, value in frequency.items():
			tot_per_head += value

	freq_on_day.append(tot_per_head)


	frequency = {}
	

	for batch in json_object["batches"]:
		if "data" not in batch:
			continue
		for tweet in batch["data"]:
			if "created_at" in tweet:
				if tweet['lang'] == 'en':
					iso_date = tweet["created_at"]
					date = iso_date[0:10]
					time_sq = datetime.strptime(iso_date[11:19],'%H:%M:%S').time()
					if (date == dt) and(time_sq >= time_zones[3]) and (time_sq < time_zones[4]):
						frequency[time_sq] = frequency.get(time_sq, 0) + 1 

	tot_per_head = 0

	for key, value in frequency.items():
		tot_per_head += value


	freq_on_day.append(tot_per_head)


	return freq_on_day


# if __name__ == "__main__":
# 	print(get_total_dates())