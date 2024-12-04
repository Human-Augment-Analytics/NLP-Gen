# utils.py

import json

def read_json_file(file_path):
    """
    Read a JSON file and return the data
    Args:
        file_path (str): Path to the JSON file
    Returns:
        data (Dict): Data read from the JSON file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def read_text_file(file_path):
    """
    Read a text file and return the content
    Args:
        file_path (str): Path to the text file
    Returns:
        content (str): Content of the text file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def save_json_file(data, path):
    """
    Save data to a JSON file.
    Args:
        data: Data to save.
        path (str): Path to save the JSON file.
    Returns:
        path (str): Path to the saved JSON file.
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return path