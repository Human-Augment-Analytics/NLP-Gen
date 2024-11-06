from ollama_model_processor import OllamaModelProcessor
import os
import json
from termcolor import colored

def generate_query(query_template: str, document_content: str, options: str):
    # Read the content of the query template
    with open(query_template, 'r', encoding='utf-8') as f:
        query_template_content = f.read()

    # Replace the placeholders in the query template with the actual content
    query = query_template_content.replace("{{DOCUMENT_CONTENT}}", document_content)
    query = query.replace("{{OPTIONS}}", options)

    return query

def log_in_color(text: str, color: str):
    # Function to print log in specific color using termcolor
    print(colored(text, color))

def extract_context_around_date(text, date, window_size=1000):
    # text_lower = text.lower()
    date_lower = date.strip()
    start = 0
    start_position = text.find(date_lower, start)    
    if start_position == -1:
        print(f"Date '{date}' not found in the text.")
    else:
        start_index = max(start_position - window_size, 0)
        end_index = min(start_position + len(date_lower) + window_size, len(text))
        context = text[start_index:end_index]
    return context


def generate_output(ollama_models: list, query_template: str, input_folder: str, dates_folder: str, clusters_file: str, output_folder: str, repetitions: int = 1, delete_models_after_query: bool = False, model_hyperparameters: dict = {}):
    # Instantiate the OllamaModelProcessor
    for model in ollama_models:
        # Log the model being processed:
        log_in_color(f"Processing model: {model}", "green")
        # Step 1: Instantiate the OllamaModelProcessor
        processor = OllamaModelProcessor(model, **model_hyperparameters)

        # Step 2: Get the output options from the clusters.json file contained in the options key
        options_file = clusters_file
        with open(options_file, 'r', encoding='utf-8') as f:
            options_content = json.load(f)
        # Now set the options to be the value of the options key
        options = json.dumps(options_content["options"], ensure_ascii=False)

        for filename in os.listdir(input_folder):    
            if filename.endswith(".txt"): # Process only txt files
                # Log the file being processed:
                log_in_color(f"Processing file: {filename}", "blue")
                # Remove the extension from the filename
                filename_name = os.path.splitext(filename)[0]
                # We append locate the output folder under a folder with the file name first and then a folder with the model name
                file_output_folder = os.path.join(output_folder, filename_name, model)
                # Create the output folder if it doesn't exist
                os.makedirs(file_output_folder, exist_ok=True)
        
                # Read the content of the document
                document_path = os.path.join(input_folder, filename)
                with open(document_path, 'r', encoding='utf-8') as f:
                    document_content = f.read()

                # query_without_dates = generate_query(query_template, document_content, options)

                # Now we query the model replacing the last place holder with each date independently
                # Read the dates JSON file with same name as the document
                dates_file = os.path.join(dates_folder, f"{filename_name}.json")

                with open(dates_file, 'r', encoding='utf-8') as f:
                    date_objects = json.load(f)

                for i, date_object in enumerate(date_objects):
                    date_for_context = date_object["date"]
                    date_context = extract_context_around_date(document_content, date_for_context)
                    query_without_date = generate_query(query_template, date_context, options)

                    # Log the date position being processed:
                    log_in_color(f"Processing date: {i}", "magenta")
                    expected_output = json.dumps(date_object, ensure_ascii=False)
                    query = query_without_date.replace("{{MODEL_OUTPUT_FORMAT}}", expected_output)

                    # For each query, we generate <repetitions> outputs to ensure output consistency
                    for repetition in range(repetitions):
                        # Log the repetition being processed:
                        log_in_color(f"Processing repetition: {repetition + 1}", "yellow")
                        output = processor.query_model(query)
                        output_path = os.path.join(file_output_folder, f"{filename_name}_{i}_{repetition + 1}.txt")
                        with open(output_path, 'w', encoding='utf-8') as f:
                            # First write a line with the date object passed to the model
                            # f.write(expected_output + "\n\n")
                            f.write(output)
        # Log the model being deleted:
        log_in_color(f"Deleting model: {model}", "red")
        # Delete the ollama model to free up space
        if delete_models_after_query:
            processor._delete_model()

if __name__ == "__main__":
    generate_output(
        ollama_models=[
            # Smaller models
            "llama3.2:1b",
            # "llama3.2",
            # "llama3.1",
            # "nemotron-mini",
            # "gemma2",
            # "mistral-nemo",
            # "qwen2",
            # "deepseek-coder-v2",
            # "phi3",
            # "mixtral"
            # Intermediate models
            # "mistral-small",
            # "gemma2:27b",
            # Larger models
            # "nemotron",
            # "llama3.1:70b",
            # "qwen2.5:72b",

            ],
        query_template="query_template.txt",
        output_folder="models_output",
        input_folder="4.selected_files_for_benchmark",
        dates_folder="5.extracted_dates_for_model_benchmark",
        clusters_file="clusters.json",
        repetitions=10,
        delete_models_after_query=False,
        model_hyperparameters={
            "temperature": 0.0000001
            ,"top_k": 5
            ,"top_p": 0.5
            ,"seed": 42
            }
        )