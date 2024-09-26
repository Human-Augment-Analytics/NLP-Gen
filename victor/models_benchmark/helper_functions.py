import json
from typing import Dict, Any, List
from datetime import datetime

def load_json(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON in {file_path}: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {str(e)}")

def word_similarity(pred: Any, true: Any, threshold: float = 0.8) -> float:
    pred_str = str(pred).lower()
    true_str = str(true).lower()
    
    pred_words = set(pred_str.split())
    true_words = set(true_str.split())
    
    if not true_words:
        return 1.0 if not pred_words else 0.0
    
    intersection = pred_words.intersection(true_words)
    union = pred_words.union(true_words)
    
    return len(intersection) / len(union)

def compare_lists(pred: List[Any], true: List[Any], threshold: float = 0.8) -> float:
    if not isinstance(pred, list):
        pred = [pred]
    if not isinstance(true, list):
        true = [true]
    
    if not true:
        return 1.0 if not pred else 0.0
    
    matches = sum(word_similarity(p, t, threshold) for p in pred for t in true)
    return min(matches / len(true), 1.0)

def compare_dates(pred: Any, true: Any) -> float:
    try:
        pred_date = datetime.strptime(str(pred), "%d/%m/%Y")
        true_date = datetime.strptime(str(true), "%d/%m/%Y")
        return 1.0 if pred_date == true_date else 0.0
    except ValueError:
        return 0.0

def compare_numbers(pred: Any, true: Any) -> float:
    try:
        return 1.0 if float(pred) == float(true) else 0.0
    except ValueError:
        return 0.0

def compare_booleans(pred: Any, true: Any) -> float:
    return 1.0 if bool(pred) == bool(true) else 0.0

def get_comparison_function(data_type: str):
    comparison_functions = {
        "string": word_similarity,
        "list": compare_lists,
        "date": compare_dates,
        "date_list": compare_lists,
        "integer": compare_numbers,
        "boolean": compare_booleans
    }
    return comparison_functions.get(data_type, word_similarity)

def compare_values(pred: Any, true: Any, field_config: Dict[str, Any]) -> float:
    if pred is None and true is None:
        return 1.0
    elif pred is None or true is None:
        return 0.0
    
    data_type = field_config["type"]
    comparison_function = get_comparison_function(data_type)
    
    if data_type in ["string", "list"]:
        precision = field_config.get("precision", 0.8)
        return comparison_function(pred, true, precision)
    else:
        return comparison_function(pred, true)