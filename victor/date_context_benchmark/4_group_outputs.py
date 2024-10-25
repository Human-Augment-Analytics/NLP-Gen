import os
import json
import re

def combine_outputs_per_file_and_model(output_folder):
    # Iterate over each original file in the output folder
    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        if os.path.isdir(file_path):
            # Iterate over each model folder within the original file folder
            for model in os.listdir(file_path):
                model_path = os.path.join(file_path, model)
                if os.path.isdir(model_path):
                    dates_outputs = []
                    metrics_outputs = []
                    # Iterate over each output file within the model folder
                    output_files = sorted([f for f in os.listdir(model_path) if f.endswith('.txt')])
                    for output_file in output_files:
                        if output_file.endswith('_combined.txt'):
                            continue  # Skip combined files
                        output_file_path = os.path.join(model_path, output_file)
                        with open(output_file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        # Parse the content
                        sections = content.strip().split('\n\n')
                        if len(sections) >= 2:
                            # Model output is the first section
                            model_output_text = sections[0].strip()
                            # Execution details is the last section
                            execution_details_json = sections[-1].strip()
                            # Clean up model output text
                            model_output_text = re.sub(r'^```(?:json)?\s*', '', model_output_text)
                            model_output_text = re.sub(r'\s*```$', '', model_output_text)
                            # Parse the model output JSON
                            try:
                                model_output = json.loads(model_output_text)
                            except json.JSONDecodeError as e:
                                print(f"Error decoding model output in file {output_file_path}: {e}")
                                # Optionally, print the problematic text
                                # print(f"Model output text was:\n{model_output_text}\n")
                                continue
                            # Extract "date" and "date event"
                            try:
                                date = model_output.get("date", "")
                                date_event = model_output.get("date event", "")
                            except Exception as e:
                                print(f"Error extracting date and date event in file {output_file_path}: {e}")
                                date = ""
                                date_event = ""
                            # Parse execution details
                            try:
                                execution_details_full = json.loads(execution_details_json)
                                execution_details = execution_details_full.get('execution_details', execution_details_full)
                            except json.JSONDecodeError as e:
                                print(f"Error decoding execution details in file {output_file_path}: {e}")
                                execution_details = {}
                            # Add to dates_outputs
                            dates_outputs.append({
                                "date": date,
                                "date event": date_event
                            })
                            # Add to metrics_outputs
                            metrics_outputs.append(execution_details)
                        else:
                            # Handle unexpected format
                            print(f"Unexpected format in file {output_file_path}")
                            continue
                    # Write dates_outputs to JSON file
                    dates_output_file = os.path.join(model_path, f"{filename}_{model}.json")
                    with open(dates_output_file, 'w', encoding='utf-8') as f:
                        json.dump(dates_outputs, f, ensure_ascii=False, indent=2)
                    # Write metrics_outputs to JSON file
                    metrics_output_file = os.path.join(model_path, f"{filename}_{model}_metrics.json")
                    with open(metrics_output_file, 'w', encoding='utf-8') as f:
                        json.dump(metrics_outputs, f, ensure_ascii=False, indent=2)
    print("Combined output files created.")

if __name__ == "__main__":
    output_folder = "models_output"
    combine_outputs_per_file_and_model(output_folder)
