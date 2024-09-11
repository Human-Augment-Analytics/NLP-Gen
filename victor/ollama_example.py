import requests
import json

def generate_response(prompt, model="llama3.1"):
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": model,
        "prompt": prompt
    }
    
    response = requests.post(url, data=json.dumps(data))
    
    if response.status_code == 200:
        # The response is a stream of JSON objects, each on a new line
        response_text = ""
        for line in response.text.strip().split('\n'):
            try:
                response_json = json.loads(line)
                if 'response' in response_json:
                    response_text += response_json['response']
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {line}")
        
        return response_text
    else:
        return f"Error: {response.status_code} - {response.text}"

# Example usage
prompt = "Why is the sky blue?"
response = generate_response(prompt)
print(response)