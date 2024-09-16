import json
import requests
import time
import os
import subprocess
from typing import Dict, Any, List

class OllamaModelProcessor:
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.base_url = "http://localhost:11434/api/generate"
        self.kwargs = kwargs
        self.colors = {
            'GREEN':'\033[92m',
            'BLUE': '\033[94m',
            'WHITE': '\033[97m',
            'RED': '\033[91m',
            'YELLOW': '\033[93m',
            'RESET': '\033[0m'
        }

    # ANSI escape codes for colors
    def _print_color(self, text, color = 'WHITE'):
        print(f"{self.colors[color]}{text}{self.colors['RESET']}")

    def _check_model_downloaded(self):
        # Check if the model is installed
        check_model_command = f"ollama list | grep {self.model_name}"
        result = subprocess.run(check_model_command, shell=True, capture_output=True, text=True)
        
        if self.model_name not in result.stdout:
            # If the model is not installed, download it
            self._print_color(f"Model {self.model_name} not found. Downloading...", color = 'YELLOW')
            
            try:
                pull_model_command = f"ollama pull {self.model_name}"
                subprocess.run(pull_model_command, check=True, shell=True)
            except subprocess.CalledProcessError as e:
                self._print_color(f"Error running command: {e}", color = 'RED')
    
    def _delete_model(self):
        # Delete the model
        delete_model_command = f"ollama rm {self.model_name}"
        try:
            subprocess.run(delete_model_command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            self._print_color(f"Error running command: {e}", color = 'RED')


    def _generate_response(self, prompt: str) -> Dict[str, Any]:
        start_time = time.time()
        response = requests.post(self.base_url, json={
            "model": self.model_name,
            "prompt": prompt,
            **self.kwargs
        })
        end_time = time.time()
        processing_time = end_time - start_time

        if response.status_code == 200:
            response_text = ""
            for line in response.text.strip().split('\n'):
                try:
                    response_json = json.loads(line)
                    if 'response' in response_json:
                        response_text += response_json['response']
                except json.JSONDecodeError:
                    self._print_color(text = f"Error decoding JSON: {line}", color = 'RED')
            return {
                "response": response_text,
                "processing_time": processing_time
            }
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def _save_output(self, output: str, output_path: str):
        # Firsth check if the output folder exists, if not, create it
        output_folder = os.path.dirname(output_path)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)

    def _append_execution_details(self, output: str) -> str:
        execution_details = {
            "execution_details": {
                "model_name": self.model_name,
                "hyperparameters": self.kwargs,
                "processing_time": output["processing_time"],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        return output["response"] + "\n\n" + json.dumps(execution_details, indent=2)

    def query_model(self, input_text: str, output_path: str = "", save_output: bool = False) -> str:
        self._check_model_downloaded()
        output = self._generate_response(input_text)
        final_output = self._append_execution_details(output)
        
        if save_output and output_path:
            self._save_output(final_output, output_path)
        
        return final_output

    def query_model_with_file(self, file_path: str, prompt_template_path: str, input_placeholder: str, output_format_path: str, output_placeholder: str, 
                              output_path: str = "", save_output: bool = False) -> str:
        
        with open(prompt_template_path, 'r', encoding='utf-8') as f:
            input_text = f.read()

        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

        with open(output_format_path, 'r', encoding='utf-8') as f:
            output_format = f.read()
        
        full_input = input_text.replace(input_placeholder, file_content)
        full_input = full_input.replace(output_placeholder, output_format)

        return self.query_model(full_input, output_path, save_output)


    def query_model_bulk(self, prompt_template_path: str, input_placeholder: str, output_format_path: str, output_placeholder: str, folder_path: str, 
                         output_folder: str, save_output: bool = True) -> List[str]:
        
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"): 
                # Print the name of the file being processed
                self._print_color(f"Processing file: {filename}", color = 'GREEN')
                
                # Define the path for the output file within the folder
                output_path = os.path.join(output_folder, f"output_{filename}") if save_output else ""

                # Query the model with the file content using key arguments
                self.query_model_with_file(file_path=os.path.join(folder_path, filename), 
                                           prompt_template_path=prompt_template_path, 
                                           input_placeholder=input_placeholder, 
                                           output_format_path=output_format_path, 
                                           output_placeholder=output_placeholder, 
                                           output_path=output_path, 
                                           save_output=save_output)