# date_classifier.py

from ollama_model_processor import OllamaModelProcessor
import os
from utils import read_json_file, read_text_file, save_json_file

def generate_query(prompt_template: str, date: str, context: str, options: str):
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

    # Replace the context in the prompt content
    query = query.replace("{{CONTEXT}}", context)

    # Replace the options in the prompt content
    query = query.replace("{{OPTIONS}}", str(options))

    return query

def retrieve_date_events(input_path, output_folder, case_type, related_events, ollama_model, model_hyperparameters={},
prompt_template_path="templates/events_prompt_template.txt", 
execution_notes=""):                         
    """
    Query the Ollama model to retrieve date events related to the given events from the set of contexts in the file.
    Args:
        input_path (str): Path to the file containing the contexts.
        output_folder (str): Path to the folder containing the model outputs.
        case_type (str): Type of case to retrieve date events for.
        related_events (List[str]): List of related events to retrieve date events for.
        ollama_model (str): Ollama model to use for querying.
        model_hyperparameters (dict): Hyperparameters to use for the model.
        execution_notes (str): Notes to include in the output file.
    Returns:
        output_path (str): Path to the output file containing the date events.
        first_case (dict): First case in the output file.

    """
    # Generate output file name
    base_name = os.path.basename(input_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_filename = f"{name_without_ext}.json"
    output_path = os.path.join(output_folder, output_filename)

    # Retrieve context and dates from the input json file:
    cases = read_json_file(input_path)

    for i, case in enumerate(cases):
        # Indicate which case is being processed
        print(f"Processing case: {i+1}/{len(cases)}")
        # Get the context and date for the case
        context = case['context']
        date = case['date']
        # Generate the query
        query = generate_query(prompt_template_path, date, context, related_events)
        # Query the model
        output = ollama_model.query_model(query)
        # Append the output event to the case:
        case['identified_event'] = output['response']
        case['classifier_processing_time'] = output['processing_time']

    # Now we wrap the results in another dictionary containing the hyperparameters and the notes passed for the execution
    results = {
        "model": ollama_model.model_name,
        "hyperparameters": model_hyperparameters,
        "case_type": case_type,
        "classifier_execution_notes": execution_notes,
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
    input_path = "process_runs/05d86002-10bf-41f4-ac23-978a9c4503a3/ner_postprocess_results/downloadfile-3.json"
    case_type = "Laboral"
    output_folder = "process_runs/05d86002-10bf-41f4-ac23-978a9c4503a3/llama3.2:1b_output"
    related_events = [
			"Fecha de sentencia",
			"Fecha de presentación de demanda",
			"Fecha de notificación de demanda",
			"Fecha de audiencia",
			"Fecha de ley",
			"Fecha de documento legal",
			"Fecha de contrato",
			"Fecha de despido",
			"Fecha de indemnización",
			"Fecha de última audiencia",
			"Fecha de audiencia aplazada",
			"Otros"
		]
    # Retrieve date events for the related events
    retrieve_date_events(
        input_path=input_path, 
        output_folder=output_folder, 
        case_type=case_type, 
        related_events=related_events, 
        ollama_model=ollama_model,
        model_hyperparameters=hyperparameters,
        execution_notes="Test alpha",
        )