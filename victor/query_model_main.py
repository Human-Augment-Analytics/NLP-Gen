from ollama_model_processor import OllamaModelProcessor
import os

def generate_output(ollama_models: list, output_folder: str, model_hyperparameters: dict = {}):
    # Instantiate the OllamaModelProcessor
    for model in ollama_models:
        # Step 1: Instantiate the OllamaModelProcessor
        processor = OllamaModelProcessor(model, **model_hyperparameters)

        # Step 2: 
        sentencias_path = "../../sentencias_txt"
        
        prompt_template_path = "../../model_input_templates/input_text_v1.txt"
        input_placeholder = "{{DOCUMENT_CONTENT}}"
        output_placeholder = "{{MODEL_OUTPUT_FORMAT}}"
        
        output_template_folder = "../../model_output_templates"
        
        version_number = 1
        for filename in os.listdir(output_template_folder):
            if filename.endswith(".txt"):
                output_template_file_name = f"output_json_v{version_number}.txt"
                output_file_template_path = os.path.join(output_template_folder, output_template_file_name)
                output_folder_path = f"{output_folder}/{model}/v{version_number}"
                processor.query_model_bulk(prompt_template_path=prompt_template_path, 
                                            input_placeholder=input_placeholder, 
                                            output_format_path=output_file_template_path, 
                                            output_placeholder=output_placeholder, 
                                            folder_path=sentencias_path, 
                                            output_folder=output_folder_path, 
                                            save_output=True)
                version_number += 1

if __name__ == "__main__":
    generate_output(
        ollama_models=[
            "llama3.1",
            "gemma2",
            "mistral-nemo",
            "qwen2",
            "deepseek-coder-v2",
            "phi3",
            "mixtral"
            ],
        output_folder="../../model_output",
        # model_hyperparameters={"temperature": 0.7, "top_p": 0.9}
        )