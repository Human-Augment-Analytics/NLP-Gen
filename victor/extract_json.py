import os
import json

def extract_json_from_text(text):
    """Extract JSON objects from text using a stack-based approach."""
    json_objects = []
    stack = []
    start = -1
    
    for i, char in enumerate(text):
        if char == '{':
            if not stack:
                start = i
            stack.append(char)
        elif char == '}':
            if stack:
                stack.pop()
                if not stack:
                    try:
                        json_obj = json.loads(text[start:i+1])
                        json_objects.append(json_obj)
                    except json.JSONDecodeError:
                        print(f"Warning: Could not parse JSON object: {text[start:i+1][:50]}...")
    
    return json_objects

def process_file(input_path, output_path):
    """Process a single file, extract JSON, and save as new file."""
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    json_objects = extract_json_from_text(content)
    
    if len(json_objects) == 2:
        # Combine the two JSON objects
        combined_json = {**json_objects[0], **json_objects[1]}
    elif len(json_objects) == 1:
        combined_json = json_objects[0]
    else:
        print(f"Warning: Unexpected number of JSON objects ({len(json_objects)}) in {input_path}")
        return
    
    # Save the combined JSON
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(combined_json, file, ensure_ascii=False, indent=2)
    
    print(f"Processed: {input_path} -> {output_path}")

def process_model_directory(model_input_dir, model_output_dir):
    """Process all text files in a single model's directory."""
    if not os.path.exists(model_output_dir):
        os.makedirs(model_output_dir)
    
    for filename in os.listdir(model_input_dir):
        if filename.startswith("output_") and filename.endswith(".txt"):
            input_path = os.path.join(model_input_dir, filename)
            new_name = filename.replace("output_", "").replace(".txt", "_extracted.json")
            output_path = os.path.join(model_output_dir, new_name)
            process_file(input_path, output_path)

def process_parent_directory(parent_input_dir, parent_output_dir):
    """Process all model directories in the parent directory."""
    for model_dir in os.listdir(parent_input_dir):
        model_input_path = os.path.join(parent_input_dir, model_dir)
        if os.path.isdir(model_input_path):
            model_output_path = os.path.join(parent_output_dir, model_dir)
            print(f"\033[94mProcessing model: {model_dir}\033[0m")
            process_model_directory(model_input_path, model_output_path)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract and format JSON from text files for multiple models")
    parser.add_argument("parent_input_dir", help="Parent directory containing model subdirectories with input text files")
    parser.add_argument("parent_output_dir", help="Parent directory to save extracted JSON files for each model")
    
    # args = parser.parse_args()

    args = {
        "parent_input_dir": "../../Documents/Generated/2.models_output/v1",
        "parent_output_dir": "../../Documents/Generated/2.models_output/v1_json"
    }

    args = argparse.Namespace(**args)
    
    process_parent_directory(args.parent_input_dir, args.parent_output_dir)
    print("JSON extraction and formatting complete for all models.")

    # Example usage:
    # python extract_json.py ../../Documents/Generated/2.models_output/v1 ../../Documents/Generated/2.models_output/v1_json