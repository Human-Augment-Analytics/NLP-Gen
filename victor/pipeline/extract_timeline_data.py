# extract_timeline_data.py

import os
from utils import read_json_file, save_json_file

def get_timeline_data(input_path: str, output_folder: str):

    # Generate output file name
    base_name = os.path.basename(input_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_filename = f"{name_without_ext}.json"
    output_path = os.path.join(output_folder, output_filename)

    # First we read the content of the file containing all the dates and events:
    file_content = read_json_file(input_path)
    cases = file_content['cases']

    # For the timeline we need to generate a list of dictionaries with the date and the event similar to the following:
#     items = [
#     {"id": 1, "content": "2022-10-20", "start": "2022-10-20"},
#     {"id": 2, "content": "2022-10-09", "start": "2022-10-09"},
#     {"id": 3, "content": "2022-10-18", "start": "2022-10-18"},
#     {"id": 4, "content": "2022-10-16", "start": "2022-10-16"},
#     {"id": 5, "content": "2022-10-25", "start": "2022-10-25"},
#     {"id": 6, "content": "2022-10-27", "start": "2022-10-27"},
#     ]

    items = []
    for i, case in enumerate(cases):
        items.append({"id": i+1, "content": case['identified_event'], "start": case['standardized_date']})

    # Now we save the timeline data to a json file:
    output_path = save_json_file(items, output_path)

    return output_path, items

# Example run

if __name__ == "__main__":
    file_path = "process_runs/85f5be3c-3136-4cf7-9ff1-50a6d39a4fea/converted_dates/llama3.2:1b/downloadfile-3.json"
    output_folder = "process_runs/85f5be3c-3136-4cf7-9ff1-50a6d39a4fea/timeline_data"
    get_timeline_data(file_path, output_folder)