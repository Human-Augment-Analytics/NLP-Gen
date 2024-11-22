import json
import os
import pandas as pd
from ner_processor import NerProcessor

cleaned_files_folder = "../../Documents/Generated/1.sentencias_cleaned"

ner_processor = NerProcessor()
df = pd.DataFrame(columns=['filename', 'date', 'score', 'start', 'end', 'context'])
# We are going to iterate over all the cleaned files and extract the dates in each of them.
# Then we will store these in a file called filename_dates.json

for filename in os.listdir(cleaned_files_folder):
    with open(os.path.join(cleaned_files_folder, filename), 'r', encoding='utf-8') as file:
        # Print in green the filename being processed
        print(f'\033[92mProcessing {filename}\033[0m')
        cleaned_text = file.read()
        ner_output = ner_processor.process_text(cleaned_text)
        ner_json = json.loads(ner_output)
        dates = []
        for entity in ner_json['entities']:
            # For each entity, we extract 500 chars before and 500 after the entity to provide context
            # start = entity['start']
            # end = entity['end']
            # context_start = max(0, start - 500)
            # context_end = min(len(cleaned_text), end + 500)
            # context = cleaned_text[context_start:context_end]

            # # We add one row to the dataframe for each date found without using the append method since it's deprecated
            # if entity['word'] not in context:
            #     print(f"Date {entity['word']} not found in context")
            df.loc[len(df)] = [filename, entity['word'], entity['score'], entity['start'], entity['end'], entity['context']]
            # df = df.append({'filename': filename, 'date': entity['word'], 'score': entity['score'], 'start': entity['start'], 'end': entity['end'], 'context': context}, ignore_index=True)
            
# We now save the results into a csv file called dates.csv (if it exists, we append a new number to the filename as dates_1.csv, dates_2.csv, etc.)
if os.path.exists('dates.csv'):
    i = 1
    while os.path.exists(f'dates_{i}.csv'):
        i += 1
    df.to_csv(f'dates_{i}.csv', index=False)
else:
    df.to_csv('dates.csv', index=False)