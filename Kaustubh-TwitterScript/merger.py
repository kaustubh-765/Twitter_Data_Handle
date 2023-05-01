import json
import os

output_file_name = "final.json"

test_batch = []

merge_file = "Afganishtan tweet_May.json"
i=0

while os.path.exists(merge_file):
        json_response = json.load(output_file_name)
        test_batch.append(json_response['batches'])
        print(f"Taken data from file {i}")

        i += 1
        merge_file = f"Afganishtan tweet_May_({i}).json"

final_batch = {}
final_batch['batches'] = test_batch


with open(output_file_name, "w", encoding='utf-8') as output_file:
        output_file.write(json.dumps(final_batch, indent=4))

print("Done")