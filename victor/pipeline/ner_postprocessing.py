# ner_postprocessing.py

import json
import os
import re

def load_json_file(path):
    """
    Load JSON data from a file.
    Args:
        path (str): Path to the JSON file.
    Returns:
        content: JSON data as a dictionary.
    """
    with open(path, 'r', encoding='utf-8') as file:
        content = json.load(file)
    return content

def load_cleaned_text(path):
    """
    Load cleaned text from a file.
    Args:
        path (str): Path to the cleaned text file.
    Returns:
        content: Cleaned text content.
    """
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def collect_date_entities(ner_results):
    """
    Extract date entities from NER results.
    Args:
        ner_results (list): List of dictionaries containing NER results.
    Returns:
        date_entities: List of date entities with adjusted indices.
    """
    date_entities = []
    for chunk in ner_results:
        entities = chunk.get('entities', [])
        for entity in entities:
            if entity['entity_group'] == 'DATE':
                date_entities.append({
                    'date': entity['word'],
                    'start_index': entity['full_doc_start'],
                    'end_index': entity['full_doc_end'],
                    'score': entity['score']
                })
    return date_entities

def remove_duplicate_dates(date_entities):
    """
    Remove duplicates and keep the longest date for each start_index.
    Args:
        date_entities (list): List of date entities with adjusted indices.
    Returns:
        unique_dates: List of unique date entities.
    """
    dates_by_start = {}
    for entity in date_entities:
        start_index = entity['start_index']
        if start_index not in dates_by_start:
            dates_by_start[start_index] = entity
        else:
            if entity['end_index'] > dates_by_start[start_index]['end_index']:
                dates_by_start[start_index] = entity
    unique_dates = list(dates_by_start.values())
    return unique_dates

def mask_other_instances(date_text, context, date_context_start, date_context_end, error_margin=5):
    """
    Mask other instances of the date in the context with 'X' characters.
    Args:
        date_text (str): The date text to mask.
        context (str): The context text.
        date_context_start (int): The start index of the date in the context.
        date_context_end (int): The end index of the date in the context.
    """
    pattern = re.escape(date_text)
    matches = list(re.finditer(pattern, context))

    context_list = list(context)  # Convert context to a list for mutability
    for match in matches:
        match_start = match.start()
        match_end = match.end()
        if not ( abs(match_start - date_context_start) < error_margin and abs(match_end - date_context_end) < error_margin ):
            # Replace characters with 'X'
            for i in range(match_start, match_end):
                context_list[i] = 'X'
    context_masked = ''.join(context_list)
    return context_masked

def build_final_dates_list(unique_dates, cleaned_text, context_window):
    """
    Build the final list of date objects with context and masked dates.
    Args:
        unique_dates (list): List of unique date entities.
        cleaned_text (str): Cleaned text content.
        context_window (int): Number of characters before and after the date to include in context.
    Returns:
        final_dates: List of date objects with context and indices.
    """
    final_dates = []
    for entity in unique_dates:
        date_text = entity['date']
        start_index = entity['start_index']
        end_index = entity['end_index']

        # Get context window
        context_start = max(0, start_index - context_window)
        context_end = min(len(cleaned_text), end_index + context_window)
        context = cleaned_text[context_start:context_end]

        # Mask other instances of the date in the context
        date_context_start = start_index - context_start
        date_context_end = end_index - context_start

        context_masked = mask_other_instances(date_text, context, date_context_start, date_context_end)

        # Build the final date object
        final_dates.append({
            'date': date_text,
            'start_index': start_index,
            'end_index': end_index,
            'context': context_masked
        })
    return final_dates

def save_json_file(data, path):
    """
    Save data to a JSON file.
    Args:
        data: Data to save.
        path (str): Path to save the JSON file.
    Returns:
        None
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def postprocess_ner_results(ner_results_path, cleaned_text_path, output_folder, context_window=400):
    """
    Postprocess NER results to remove duplicates and prepare final output.

    Args:
        ner_results_path (str): Path to the NER results JSON file from Step 4.
        cleaned_text_path (str): Path to the cleaned text file from Step 2.
        output_path (str): Path to save the final output JSON file.
        context_window (int): Number of characters before and after the date to include in context.

    Returns:
        List of date objects with context and indices.
    """
    # Generate output file name
    base_name = os.path.basename(ner_results_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_filename = f"{name_without_ext}.json"
    output_path = os.path.join(output_folder, output_filename)

    # Load NER results
    ner_results = load_json_file(ner_results_path)

    # Load cleaned text
    cleaned_text = load_cleaned_text(cleaned_text_path)

    # Collect all date entities with adjusted indices
    date_entities = collect_date_entities(ner_results)

    # Remove duplicates: keep the longest date for each start_index
    unique_dates = remove_duplicate_dates(date_entities)

    # Build the final list with context and masked dates
    final_dates = build_final_dates_list(unique_dates, cleaned_text, context_window)

    # Save the final dates to the output file
    save_json_file(final_dates, output_path)

    first_result = final_dates[0] if final_dates else None

    return output_path, first_result

# Example usage
if __name__ == "__main__":
    ner_results_path = "ner_results_path_to_file.json"
    cleaned_text_path = "cleaned_text_path_to_file.txt"
    output_folder = "output_folder"
    context_window = 400

    output_path, first_result = postprocess_ner_results(ner_results_path, cleaned_text_path, output_folder, context_window)

    print(f"NER postprocess results saved to `{output_path}`")
    print("Preview of the first result:")
    print(first_result)