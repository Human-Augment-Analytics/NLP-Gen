import os
import re
import json
import spacy
import sys
from install_models import ensure_model_installed

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Ensure the model is installed before loading it
if not ensure_model_installed("es_core_news_lg"):
    sys.exit(1)

# Load the Spanish language model
nlp = spacy.load("es_core_news_lg")


def extract_case_number(text):
    """
    Extract the case number from the text.
    
    Args:
    text (str): Input text

    Returns:
    str or None: Extracted case number or None if not found
    """
    case_number_pattern = r'Número\s+(?:único\s+)?de\s+caso\s+(?:\(NUC\))?\s*:?\s*(\d+-\d+)'
    case_number_match = re.search(case_number_pattern, text, re.IGNORECASE)
    return case_number_match.group(1) if case_number_match else None


def extract_parties(doc):
    """
    Extract persons and organizations from the document.
    
    Args:
    doc (spacy.Doc): Processed spaCy document

    Returns:
    dict: Dictionary containing lists of unique persons and organizations
    """
    persons = set()
    organizations = set()
    for ent in doc.ents:
        if ent.label_ == "PER":
            persons.add(ent.text)
        elif ent.label_ == "ORG":
            organizations.add(ent.text)
    return {
        "persons": list(persons),
        "organizations": list(organizations)
    }


def extract_money_amounts(doc):
    """
    Extract monetary amounts from the document using SpaCy's NER.
    
    Args:
    doc (spacy.Doc): Processed spaCy document

    Returns:
    list: List of extracted monetary amounts
    """
    money_amounts = []
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            money_amounts.append(ent.text)
    
    # Additional regex pattern for amounts that might be missed by SpaCy
    money_pattern = r'\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})?(?: [a-zA-Z]+)?'
    regex_matches = re.findall(money_pattern, doc.text)
    
    # Combine SpaCy results and regex matches, removing duplicates
    all_amounts = list(set(money_amounts + regex_matches))
    return all_amounts


def extract_dates_and_events(doc):
    """
    Extract dates and associated events from the document.
    
    Args:
    doc (spacy.Doc): Processed spaCy document

    Returns:
    list: List of dictionaries containing dates and associated events
    """
    date_events = []
    for sent in doc.sents:
        date = None
        event = []
        for token in sent:
            if token.ent_type_ == "DATE":
                date = token.text
            elif token.pos_ == "VERB":
                event.append(token.text)
        if date and event:
            date_events.append({"date": date, "event": " ".join(event)})
    return date_events


def process_cleaned_file(input_path, output_folder):
    """
    Process a single cleaned file and extract relevant information.
    
    Args:
    input_path (str): Path to the input file
    output_folder (str): Path to the output folder
    """
    # Read the cleaned file
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Process the content with spaCy
    doc = nlp(content)

    # Extract information
    parties = extract_parties(doc)

    extracted_info = {
        "case_number": extract_case_number(content),
        "parties": parties["persons"],
        "organizations": parties["organizations"],
        "money_amounts": extract_money_amounts(doc),
        "dates_and_events": extract_dates_and_events(doc)
    }

    # Generate output file name
    base_name = os.path.basename(input_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_filename = f"{name_without_ext}_extracted.json"
    output_path = os.path.join(output_folder, output_filename)

    # Write the extracted information to a JSON file
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(extracted_info, file, ensure_ascii=False, indent=2)

    print(f"{GREEN}Extracted information:{RESET} {input_path} -> {output_path}")


def process_folder(input_folder, output_folder):
    """
    Process all cleaned files in the input folder and save extracted information to the output folder.
    
    Args:
    input_folder (str): Path to the folder containing cleaned documents
    output_folder (str): Path to the folder where extracted information will be saved
    """

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('_cleaned.txt'):
            input_path = os.path.join(input_folder, filename)
            process_cleaned_file(input_path, output_folder)

# Main execution
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract information from cleaned Spanish legal documents.")
    parser.add_argument("-i", "--input", required=True, help="Path to the folder containing cleaned documents")
    parser.add_argument("-o", "--output", required=True, help="Path to the folder where extracted information will be saved")
    args = parser.parse_args()

    process_folder(args.input, args.output)

# Example usage to copy into the terminal:
# python -m spacy download es_core_news_lg
# python ner_extraction.py -i "../../sentencias_cleaned" -o "../../extracted_info"