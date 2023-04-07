# import random

# # Total number of tweets for the month
# total_tweets = 10000

# # Create a list of percentages for each day in the month
# percentages = [0.03, 0.05, 0.07, 0.09, 0.11, 0.12, 0.13, 0.13, 0.11, 0.09, 0.07, 0.05, 0.03, 0.03, 0.05, 0.07, 0.09, 0.11, 0.12, 0.13, 0.13, 0.11, 0.09, 0.07, 0.05, 0.03, 0.03, 0.05, 0.07, 0.09, 0.11, 0.12]

# # Divide each day into 6 time zones of 4 hours each
# time_zones_per_day = 6
# hours_per_day = 24
# tweets_per_time_zone = [[0 for _ in range(time_zones_per_day)] for _ in range(len(percentages))]

# #print(tweets_per_time_zone)

# for i, percentage in enumerate(percentages):
#     for j in range(time_zones_per_day):
#         tweets_per_time_zone[i][j] = int(total_tweets * percentage / time_zones_per_day / hours_per_day * 4)

# print(tweets_per_time_zone)


# # Calculate the total number of tweets for each day
# tweets_per_day = [sum(tweets_per_time_zone[i][j] for j in range(time_zones_per_day)) for i in range(len(percentages))]

# # Calculate the total number of tweets for the month based on the tweets_per_day list
# total_tweets_calculated = sum(tweets_per_day)

# # Adjust the total number of tweets for the month to match the total number of tweets calculated based on the percentages
# if total_tweets_calculated != total_tweets:
#     adjustment_factor = total_tweets / total_tweets_calculated
#     tweets_per_day = [int(tweets * adjustment_factor) for tweets in tweets_per_day]
#     for i in range(len(percentages)):
#         for j in range(time_zones_per_day):
#             tweets_per_time_zone[i][j] = int(tweets_per_time_zone[i][j] * adjustment_factor)

# # Create a list of tweet indices for each day and time zone based on the number of tweets for that time zone
# tweet_indices_per_time_zone = [[[start_index + k for k in range(num_tweets)] for start_index, num_tweets in enumerate(tweets_per_time_zone[i])] for i in range(len(percentages))]

# # Flatten the list of tweet indices
# tweet_indices_per_day = [[index for sublist in tweet_indices_per_time_zone[i] for index in sublist] for i in range(len(percentages))]
# tweet_indices = [index for sublist in tweet_indices_per_day for index in sublist]

# # Shuffle the list of tweet indices
# #random.shuffle(tweet_indices)

# # Choose N tweets from the shuffled list of tweet indices
# N = 500
# chosen_tweet_indices = tweet_indices[:N]

# # Print the chosen tweet indices
# #print(chosen_tweet_indices)


import random

# Total number of tweets for the month
total_tweets = 10000

# Create a list of percentages for each time zone in a day
time_zone_percentages = [0.05, 0.10, 0.15, 0.20, 0.25, 0.25]

# Divide each day into 6 time zones of 4 hours each and distribute the weight equally among those time zones using the percentages for that time zone
tweets_per_time_zone = [[int(total_tweets * time_zone_percentages[i] / sum(time_zone_percentages)) for i in range(len(time_zone_percentages))] for _ in range(31)]

# Calculate the total number of tweets for each day
tweets_per_day = [sum(tweets_per_time_zone[i]) for i in range(31)]

# Calculate the total number of tweets for the month based on the tweets_per_day list
total_tweets_calculated = sum(tweets_per_day)

# Adjust the total number of tweets for the month to match the total number of tweets calculated based on the time zone percentages
if total_tweets_calculated != total_tweets:
    adjustment_factor = total_tweets / total_tweets_calculated
    tweets_per_day = [int(tweets * adjustment_factor) for tweets in tweets_per_day]
    for i in range(31):
        tweets_per_time_zone[i] = [int(tweets_per_time_zone[i][j] * adjustment_factor) for j in range(len(time_zone_percentages))]

# Create a list of tweet indices for each day and time zone based on the number of tweets for that time zone
tweet_indices_per_time_zone = [[[start_index + k for k in range(num_tweets)] for start_index, num_tweets in enumerate(tweets_per_time_zone[i])] for i in range(31)]

# Flatten the list of tweet indices
tweet_indices_per_day = [[index for sublist in tweet_indices_per_time_zone[i] for index in sublist] for i in range(31)]
tweet_indices = [index for sublist in tweet_indices_per_day for index in sublist]

# Shuffle the list of tweet indices
random.shuffle(tweet_indices)

# Choose N tweets from the shuffled list of tweet indices
N = 500
chosen_tweet_indices = tweet_indices[:N]

# Print the chosen tweet indices
print(chosen_tweet_indices)

