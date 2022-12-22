import json
import pandas as pd
import os

json_file = open('Twitter_Data_Handle/Kaustubh-TwitterScript/tweets_Diyi_Yang.json')

json_response = json.load(json_file)

df = pd.DataFrame(json_response)
df.to_csv('This_is_epic.csv')

