import os
import json
import sys

def extract_dates_from_json(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):  # Ensure we're only processing JSON files
            input_file_path = os.path.join(input_folder, filename)
            
            # Open and read the content of the JSON file
            with open(input_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            # Extract only the first and second keys for each entry in the list
            extracted_data = []
            for entry in data:
                keys = list(entry.keys())  # Get the list of keys in order
                if len(keys) >= 2:  # Ensure there are at least two keys
                    extracted_data.append({
                        "standard_format": entry[keys[0]],  # First key and its value
                        "original_format": entry[keys[1]],  # Second key and its value
                        "context": "TO_BE_FILLED_IN"        # Third key to be filled in
                    })

            # Define the output file path
            output_file_path = os.path.join(output_folder, filename)
            
            # Save the extracted data into a new JSON file
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(extracted_data, output_file, ensure_ascii=False, indent=4)

    print("Extraction complete. Check the output folder:", output_folder)

if __name__ == "__main__":
    input_folder = "dates"
    output_folder = "dates_only"
    extract_dates_from_json(input_folder, output_folder)

    # if len(sys.argv) != 3:
    #     print("Usage: python script_name.py <input_folder> <output_folder>")
    # else:
    #     input_folder = sys.argv[1]
    #     output_folder = sys.argv[2]
    #     extract_dates_from_json(input_folder, output_folder)

    