# ner_processing.py

import os
import json
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

class NerProcessor:
    def __init__(self, model_name_or_path='agomez302/nlp-dr-ner', output_folder='ner_results'):
        """
        Initializes the NER processor with the given model name or path.
        Args:
            model_name_or_path (str): The name of the model or path to the model
            output_folder (str): The name of the folder to save the NER results
        Returns:
            None
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name_or_path)
        self.ner_pipeline = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple",
        )
        self.output_folder = output_folder

    def process_chunks(self, chunks):
        """Runs NER model on list of chunks and returns list of processed chunks with predictions.
        Args:
            chunks (list): List of dictionaries with 'chunk' and 'start_index' keys
        Returns:
            chunks_with_entities (list): List of dictionaries with 'chunk', 'start_index', 'entities' keys
            all_predictions (list): List of dictionaries with 'entity', 'start', 'end', 'score', 'context' keys
        """
        all_predictions = []
        for chunk_info in chunks:
            chunk_text = chunk_info['chunk']
            start_index = chunk_info['start_index']
            preds = self.ner_pipeline(chunk_text)
            
            # Adjust the indices to the original text
            for pred in preds:
                pred['full_doc_start'] = pred['start'] + start_index
                pred['full_doc_end'] = pred['end'] + start_index
                # Convert 'score' to float
                pred['score'] = float(pred['score'])
                # Ensure 'start' and 'end' are ints
                pred['start'] = int(pred['start'])
                pred['end'] = int(pred['end'])

            chunk_info['entities'] = preds
            all_predictions.append(chunk_info)

        return all_predictions

    def save_predictions(self, chunks_with_entities, output_file_path):
        """Save chunks with entities to a JSON file.
        Args:
            chunks_with_entities (list): List of dictionaries with 'chunk', 'start_index', 'entities' keys
            output_file_path (str): The path to save the JSON file
        Returns:
            None
        """
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(chunks_with_entities, f, ensure_ascii=False, indent=2)

    def generate_ner_predictions(self, input_path):
        """
        Generate NER predictions from input json file with chunked text.
        Args:
            input_path (str): The path to the input JSON file with chunked text.
        Returns:
            output_path (str): The path to the saved JSON file with NER predictions.
        """
         # Check if the file is a .json file
        if not input_path.lower().endswith('.json'):
            raise ValueError("Input file must be a .json file.")

        try:
            # Read the JSON file
            with open(input_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
            
        except UnicodeDecodeError:
            print(f"Error reading file {input_path}. Skipping.")
            return
        
        # Generate output file name
        base_name = os.path.basename(input_path)
        name_without_ext = os.path.splitext(base_name)[0]
        output_filename = f"{name_without_ext}.json"
        output_path = os.path.join(self.output_folder, output_filename)

        results = self.process_chunks(content)
        first_chunk_result = results[0]
        self.save_predictions(results, output_path)

        return output_path, first_chunk_result
    
# Example usage
if __name__ == "__main__":
    # Initialize the NerProcessor
    ner_processor = NerProcessor(output_folder='process_runs/b8ad7e3f-1a4c-496d-b5cf-f967ac3e5a08/ner_results')

    # Generate NER predictions
    input_path = "process_runs/b8ad7e3f-1a4c-496d-b5cf-f967ac3e5a08/chunked_text/downloadfile-3.json"
    output_path, first_result = ner_processor.generate_ner_predictions(input_path)

    print(f"NER results saved to `{output_path}`")
    print(f"Preview of the first result:")
    print(first_result)