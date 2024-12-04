# ollama_model_processor.py

import os
import json
import requests
import time
import subprocess
from typing import Dict, Any

class OllamaModelProcessor:
    def __init__(self, model_name: str, model_storage_path: str = None, **kwargs):
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
        # Set the model storage path if provided
        if model_storage_path:
            os.environ['OLLAMA_MODELS'] = model_storage_path

    def _print_color(self, text, color='WHITE'):
        print(f"{self.colors[color]}{text}{self.colors['RESET']}")

    def _check_model_downloaded(self):
        # Check if the model is installed
        check_model_command = f"ollama list | grep {self.model_name}"
        result = subprocess.run(check_model_command, shell=True, capture_output=True, text=True)
        
        if self.model_name not in result.stdout:
            # If the model is not installed, download it
            self._print_color(f"Model {self.model_name} not found. Downloading...", color='YELLOW')
            
            try:
                pull_model_command = f"ollama pull {self.model_name}"
                subprocess.run(pull_model_command, check=True, shell=True)
            except subprocess.CalledProcessError as e:
                self._print_color(f"Error running command: {e}", color='RED')
                raise Exception(f"Failed to download model {self.model_name}")

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
                    self._print_color(f"Error decoding JSON: {line}", color='RED')
            return {
                "response": response_text.strip(),
                "processing_time": processing_time
            }
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def query_model(self, input_text: str) -> str:
        self._check_model_downloaded()
        output = self._generate_response(input_text)
        return output
