# date_converter.py

from ollama_model_processor import OllamaModelProcessor
import os
from utils import read_json_file, read_text_file, save_json_file

def generate_query(prompt_template: str, date: str):
    """
    Generate a query to retrieve date events for the given date and context.
    Args:
        prompt_template (str): Path to the prompt template file.
        date (str): Date to retrieve events for.
        context (str): Context of the date.
        options (str): List of related events to retrieve date events for.
    Returns:
        query (str): Query to retrieve date events.
    """
    # Read the content of the query template
    query = read_text_file(prompt_template)

    # Replace the date in the prompt content
    query = query.replace("{{DATE}}", date)
    return query

def convert_dates(input_path, output_folder, ollama_model, prompt_template_path="templates/date_conversion_prompt_template.txt", execution_notes=""):                         
    """
    Query the Ollama model to retrieve date events related to the given events from the set of contexts in the file.
    Args:
        input_path (str): Path to the file containing the contexts.
        output_folder (str): Path to the folder containing the model outputs.
        ollama_model (str): Ollama model to use for querying.
        prompt_template_path (str): Path to the prompt template file.
        execution_notes (str): Notes to include in the output file.
        
    Returns:
        output_path (str): Path to the output file containing the standardized dates.

    """
    # Generate output file name
    base_name = os.path.basename(input_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_filename = f"{name_without_ext}.json"
    output_path = os.path.join(output_folder, output_filename)

    # Retrieve context and dates from the input json file:
    file_content = read_json_file(input_path)
    cases = file_content['cases']

    for i, case in enumerate(cases):
        # Indicate which case is being processed
        print(f"Processing case: {i+1}/{len(cases)}")
        # Get the date for the case
        date = case['date']
        # Generate the query
        query = generate_query(prompt_template_path, date)
        # Query the model
        output = ollama_model.query_model(query)
        # Append the output event to the case:
        case['standardized_date'] = output['response']
        case['date_converter_processing_time'] = output['processing_time']

    # Now we wrap the results in another dictionary containing the hyperparameters and the notes passed for the execution
    results = {
        "model": ollama_model.model_name,
        "hyperparameters": file_content['hyperparameters'],
        "case_type": file_content['case_type'],
        "classifier_execution_notes": file_content['classifier_execution_notes'],
        "converter_execution_notes": execution_notes,
        "cases": cases
    }

    first_case = cases[0]

    # Write the output to a json file
    saved_path = save_json_file(results, output_path) 
    return saved_path, first_case


# Example run
if __name__ == "__main__":
    ollama_model = OllamaModelProcessor(model_name="llama3.2:1b")
    hyperparameters = {
                    "temperature": 0.0000000000001
                    ,"top_k": 5
                    ,"top_p": 0.5
                    ,"seed": 42
                }
    input_path = "process_runs/85f5be3c-3136-4cf7-9ff1-50a6d39a4fea/classified_dates/llama3.2:1b/downloadfile-3.json"
    # /Users/vicuko/Desktop/CS8903-Research Projects/Sentencias/nlp/evaluation/
    output_folder = "process_runs/85f5be3c-3136-4cf7-9ff1-50a6d39a4fea/normalized_dates/llama3.2:1b"
    # Retrieve date events for the related events
    convert_dates(
        input_path=input_path, 
        output_folder=output_folder, 
        ollama_model=ollama_model,
        execution_notes="Test alpha",
        )