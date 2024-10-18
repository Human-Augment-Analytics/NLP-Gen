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

def generate_output(ollama_models: list, query_template: str, input_folder: str, dates_folder: str, output_folder: str, model_hyperparameters: dict = {}):
    # Instantiate the OllamaModelProcessor
    for model in ollama_models:
        # Log the model being processed:
        log_in_color(f"Processing model: {model}", "green")
        # Step 1: Instantiate the OllamaModelProcessor
        processor = OllamaModelProcessor(model, **model_hyperparameters)

        # Step 2: Get the output options from the date_options.json file contained in the option key
        options_file = "date_options.json"
        with open(options_file, 'r', encoding='utf-8') as f:
            options_content = json.load(f)
        # Now set the options to be the value of the options key
        options = json.dumps(options_content["options"])

        for filename in os.listdir(input_folder):    
            if filename.endswith(".txt"): # Process only txt files
                # Log the file being processed:
                log_in_color(f"Processing file: {filename}", "blue")
                # We append locate the output folder under a folder with the file name first and then a folder with the model name
                file_output_folder = os.path.join(output_folder, filename, model)
                # Create the output folder if it doesn't exist
                os.makedirs(file_output_folder, exist_ok=True)
        
                # Read the content of the document
                document_path = os.path.join(input_folder, filename)
                with open(document_path, 'r', encoding='utf-8') as f:
                    document_content = f.read()

                query_without_dates = generate_query(query_template, document_content, options)

                # Now we query the model replacing the last place holder with each date independently
                # Read the dates JSON file with same name as the document
                dates_file = os.path.join(dates_folder, f"{os.path.splitext(filename)[0]}.json")

                with open(dates_file, 'r', encoding='utf-8') as f:
                    date_objects = json.load(f)

                for i, date_object in enumerate(date_objects):
                    # Log the date position being processed:
                    log_in_color(f"Processing date: {i}", "magenta")
                    expected_output = json.dumps(date_object)
                    query = query_without_dates.replace("{{MODEL_OUTPUT_FORMAT}}", expected_output)

                    output = processor.query_model(query)
                    output_path = os.path.join(file_output_folder, f"{os.path.splitext(filename)[0]}_{i}.txt")
                    with open(output_path, 'w', encoding='utf-8') as f:
                        # First write a line with the date object passed to the model
                        f.write(expected_output + "\n\n")
                        f.write(output)


if __name__ == "__main__":
    generate_output(
        ollama_models=[
            "nemotron",
            # "llama3.2",
            # "gemma2",
            # "mistral-nemo",
            # "qwen2",
            # "deepseek-coder-v2",
            # "phi3",
            # "mixtral"
            ],
        query_template="input_text_dates_v2.txt",
        output_folder="models_output_v2",
        input_folder="cleaned",
        dates_folder="dates_only",
        model_hyperparameters={
            "temperature": 0.0000001
            ,"top_k": 5
            ,"top_p": 0.5
            ,"seed": 42
            }
        )