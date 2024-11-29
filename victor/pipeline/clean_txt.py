# text_cleaning.py

import os
import re
from transformers import AutoTokenizer

def clean_document(text):
    """
    Clean a text document by removing unwanted lines and joining lines that are part of the same sentence or paragraph.
    """
    # Split the document into lines
    lines = text.split('\n')
    cleaned_lines = []
    skip_line = False
    seen_elements = set() # Keep track of elements we've seen to avoid duplicates

    # Patterns to remove completely
    remove_patterns = [
        r'^REPÚBLICA DOMINICANA$',
        r'^PODER JUDICIAL$',
        r'^Página \d+( de \d+)?$',
        r'^PRESIDENCIA DE LA CÁMARA CIVIL Y COMERCIAL DEL JUZGADO DE$',
        r'^PRIMERA INSTANCIA DEL DISTRITO NACIONAL$',
        r'^JSS-.$',
        r'^RF.-$',
        r'^S.R.$',
        r'^Jds.-$',
        r'^JADS$'
    ]
    remove_combined = '|'.join(remove_patterns)
    
    # Patterns for elements to keep only once
    single_occurrence_patterns = [
        r'^Ordenanza civil núm\. \d+-\d+-\w+-\d+',
        r'^Número de caso único \(NUC\): \d+-\d+',
        r'^Número único de caso \(NUC\): \d+-\d+'
    ]
    single_combined = '|'.join(single_occurrence_patterns)

    for line in lines:
        stripped_line = line.strip()

        # Check if the line should be removed completely
        if re.match(remove_combined, stripped_line):
            continue
        
        # Check if the line matches any of the single occurrence patterns
        match = re.match(single_combined, stripped_line)
        
        if match:
            # If we've seen this element before, skip it
            if stripped_line in seen_elements:
                continue
            # If it's new, add it to seen elements and keep it
            seen_elements.add(stripped_line)
            cleaned_lines.append(line)
            continue

        # Handle multi-line headers/footers
        if skip_line:
            if not stripped_line:
                skip_line = False
            continue

        # If we're not skipping, add the line to cleaned_lines
        cleaned_lines.append(line)

    # Remove duplicate consecutive lines
    unique_lines = [cleaned_lines[0]]
    for line in cleaned_lines[1:]:
        if line.strip() != unique_lines[-1].strip():
            unique_lines.append(line)

    # Join lines back into a single string
    cleaned_text = '\n'.join(unique_lines)

    # Additional steps to remove line breaks and spaces that break up sentences or paragraphs
    # Join lines that are part of the same sentence or paragraph, including all-caps text
    cleaned_text = re.sub(r'([a-zñáéíóú,;:A-ZÑÁÉÍÓÚ]\s*)\n+\s*([a-zñáéíóúA-ZÑÁÉÍÓÚ])', r'\1 \2', cleaned_text)
    
    # Join lines after list item markers (A), 1-, etc.)
    cleaned_text = re.sub(r'([A-Z]\)|\d+-?)\s*\n+\s*', r'\1 ', cleaned_text)
    
    # Join lines that start with lowercase letters or numbers (for list items)
    cleaned_text = re.sub(r'\n+([a-zñáéíóú0-9])', r' \1', cleaned_text)
    
    # Remove extra spaces
    cleaned_text = re.sub(r' +', ' ', cleaned_text)
    
    # Ensure there's a space after periods that are followed by an uppercase letter
    cleaned_text = re.sub(r'\.([A-ZÑÁÉÍÓÚ])', r'. \1', cleaned_text)

    # Add line breaks before new sentences that start with common sentence starters
    sentence_starters = r'(En|El|La|Los|Las|Por|Para|Según|Considerando|Visto|Oído|Dado|Firmado)'
    cleaned_text = re.sub(f'([.!?])\s+({sentence_starters})', r'\1\n\n\2', cleaned_text)

    return cleaned_text

def tokenize_and_detokenize_text(cleaned_text, tokenizer):
    """
    Tokenize the cleaned text and then detokenize it to ensure consistency with the tokenizer.
    Args:
        cleaned_text (str): The cleaned text to tokenize and detokenize.
        tokenizer: The Hugging Face tokenizer object.
    """
    # Tokenize the text
    tokens = tokenizer.encode(cleaned_text, add_special_tokens=False)
    
    # Detokenize tokens back to text
    detokenized_text = tokenizer.decode(tokens, clean_up_tokenization_spaces=False)
    return detokenized_text

def process_file(input_path, output_folder, tokenizer_name='xlm-roberta-base'):
    """
    Process a text file by cleaning it and saving the cleaned version to the output folder.
    """
    # Check if the file is a .txt file
    if not input_path.lower().endswith('.txt'):
        raise ValueError("Input file must be a .txt file.")

    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        print(f"Error reading file {input_path}. Skipping.")
        return

    # Clean the document
    cleaned_content = clean_document(content)

    # Initialize the tokenizer (use the same tokenizer as in the NER model)
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    # Tokenize and detokenize the text to ensure consistency with next steps
    final_text = tokenize_and_detokenize_text(cleaned_content, tokenizer)

    # Generate output file name
    base_name = os.path.basename(input_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_filename = f"{name_without_ext}.txt"
    output_path = os.path.join(output_folder, output_filename)

    # Write the cleaned content to the output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(final_text)

    return output_path  # Return the path to the cleaned file

# Example usage
if __name__ == '__main__':
    input_path = 'input_path_to_text_file.txt'
    output_folder = 'output_folder'
    cleaned_file_path = process_file(input_path, output_folder)
    print(f"Cleaned text saved to: {cleaned_file_path}")