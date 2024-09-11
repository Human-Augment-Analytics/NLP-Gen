import os
import json
import requests
from datetime import datetime
import argparse
import time
from utils import *

def generate_response(prompt, model="llama3.1"):
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": model,
        "prompt": prompt
    }
    
    start_time = time.time()
    response = requests.post(url, data=json.dumps(data))
    end_time = time.time()
    
    if response.status_code == 200:
        response_text = ""
        for line in response.text.strip().split('\n'):
            try:
                response_json = json.loads(line)
                if 'response' in response_json:
                    response_text += response_json['response']
            except json.JSONDecodeError:
                print_color(text = f"Error decoding JSON: {line}", color = RED)
        
        return response_text, end_time - start_time
    else:
        return f"Error: {response.status_code} - {response.text}", end_time - start_time
    
def extract_json_from_text(text):
    """
    Extracts a valid JSON object from a text that may contain additional content.
    """
    def find_matching_bracket(s, start):
        stack = []
        for i, c in enumerate(s[start:], start):
            if c == '{':
                stack.append(c)
            elif c == '}':
                stack.pop()
                if not stack:
                    return i
        return -1

    start = text.find('{')
    if start != -1:
        end = find_matching_bracket(text, start)
        if end != -1:
            try:
                json_str = text[start:end+1]
                return json.loads(json_str)
            except json.JSONDecodeError:
                return None
    return None

def process_document(file_path, template_json, model="llama3.1"):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    prompt = f"""
    Analiza el siguiente documento legal y extrae la información solicitada en formato JSON. Si algún dato no está presente, usa "N/A". Aquí está el documento:

    {content}

    Por favor, extrae y formatea la siguiente información en JSON, siguiendo exactamente esta estructura:

    {json.dumps(template_json, ensure_ascii=False, indent=2)}

    Nota: Incluye solo el JSON en la respuesta.
    """

    response, processing_time = generate_response(prompt, model)

    extracted_json = extract_json_from_text(response)
    if extracted_json:
        # Add benchmarking information and timestamp
        extracted_json['benchmarking'] = {
            'model_name': model,
            'processing_time_seconds': processing_time,
            'token_count': len(response.split()),  # Simple word count as a proxy for tokens
            'document_length': len(content),
            'timestamp': datetime.now().isoformat()
        }
        return extracted_json
    else:
        print_color(text = f"Error: Unable to extract valid JSON from the response for file {file_path}", color = RED)
        return None

def process_directory(directory_path, output_dir, template_file, model="llama3.1"):
    with open(template_file, 'r', encoding='utf-8') as f:
        template_json = json.load(f)

    # Create a model-specific subfolder in the output directory
    model_output_dir = os.path.join(output_dir, model)
    os.makedirs(model_output_dir, exist_ok=True)

    results = []
    total_processing_time = 0
    total_documents = 0
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            print_color(text = f"Processing {filename}...", color = GREEN)
            result = process_document(file_path, template_json, model)
            if result:
                result['file_name'] = filename
                
                # Save individual result to a separate file with new naming convention
                base_name = os.path.splitext(filename)[0]
                individual_output_file = os.path.join(model_output_dir, f"{base_name}_{model}.json")
                with open(individual_output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                results.append(result)
                total_processing_time += result['benchmarking']['processing_time_seconds']
                total_documents += 1

    # Add overall benchmarking information
    overall_benchmarks = {
        'total_documents_processed': total_documents,
        'total_processing_time_seconds': total_processing_time,
        'average_processing_time_seconds': total_processing_time / total_documents if total_documents > 0 else 0,
        'model_name': model,
        'timestamp': datetime.now().isoformat()
    }

    # Include overall benchmarks in the results
    results.append({'overall_benchmarks': overall_benchmarks})

    # Save the combined results
    combined_output_file = os.path.join(model_output_dir, f"combined_results_{model}.json")
    with open(combined_output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print_color(text = f"Processing complete. Results saved to {model_output_dir}", color = BLUE)
    print_color(text = f"Combined results saved as {combined_output_file}", color = BLUE)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process legal documents using Ollama LLM")
    parser.add_argument("input_dir", help="Directory containing input text files")
    parser.add_argument("output_dir", help="Directory for output files")
    parser.add_argument("template_file", help="JSON template file path")
    parser.add_argument("--model", default="llama3.1", help="Ollama model to use (default: llama3.1)")
    
    args = parser.parse_args()

    process_directory(args.input_dir, args.output_dir, args.template_file, args.model)

# Execution example: python ollama_query.py "../../sentencias_cleaned" "../../model_outputs" "response_template.json" --model "llama3.1"