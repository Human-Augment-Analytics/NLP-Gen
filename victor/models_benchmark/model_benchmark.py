import os
import json
from typing import Dict, Any, List
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from helper_functions import load_json, compare_values

def evaluate_document(prediction: Dict[str, Any], validation: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, float]:
    scores = {}

    for category, fields in config.items():
        for field, field_config in fields.items():
            pred_value = prediction.get(category, {}).get(field)
            true_value = validation.get(category, {}).get(field, {})
            scores[f"{category}_{field}"] = compare_values(pred_value, true_value, field_config)

    return scores

def evaluate_model(model_outputs_dir: str, validation_dir: str, config_path: str) -> Dict[str, Any]:
    config = load_json(config_path)
    total_scores = {}
    file_count = 0
    total_processing_time = 0
    model_name = os.path.basename(model_outputs_dir)

    print(f"Processing model: {model_name}")
    print(f"Model output directory: {model_outputs_dir}")
    print(f"Validation directory: {validation_dir}")

    for filename in os.listdir(model_outputs_dir):
        if filename.endswith("_extracted.json"):
            base_name = filename.replace("_extracted.json", "")
            prediction_path = os.path.join(model_outputs_dir, filename)
            validation_path = os.path.join(validation_dir, f"{base_name}_validation.json")

            print(f"Processing file: {filename}")
            print(f"Prediction path: {prediction_path}")
            print(f"Validation path: {validation_path}")

            try:
                if not os.path.exists(validation_path):
                    print(f"Warning: Validation file not found for {filename}")
                    continue

                prediction = load_json(prediction_path)
                validation = load_json(validation_path)

                scores = evaluate_document(prediction, validation, config)

                print(f"Scores for {filename}:")
                for key, value in scores.items():
                    print(f"  {key}: {value}")
                    if key not in total_scores:
                        total_scores[key] = 0
                    total_scores[key] += value

                # Extract execution details
                execution_details = prediction.get("execution_details", {})
                total_processing_time += execution_details.get("processing_time", 0)

                file_count += 1
                print(f"Successfully processed file: {filename}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {filename}: {str(e)}")
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")

    if file_count == 0:
        print(f"No valid files processed for model {model_name}")
        return {
            "model_name": model_name,
            "error": "No valid files processed",
            "average_scores": {},
            "overall_score": 0,
            "files_processed": 0,
            "average_processing_time": 0
        }

    # Calculate average scores
    avg_scores = {key: value / file_count for key, value in total_scores.items()}
    
    # Calculate overall score
    overall_score = sum(avg_scores.values()) / len(avg_scores) if avg_scores else 0

    return {
        "model_name": model_name,
        "average_scores": avg_scores,
        "overall_score": overall_score,
        "files_processed": file_count,
        "average_processing_time": total_processing_time / file_count if file_count > 0 else 0
    }

def compare_models(models_parent_dir: str, validation_dir: str, config_path: str) -> Dict[str, Any]:
    results = {}
    for model_dir in os.listdir(models_parent_dir):
        full_model_dir = os.path.join(models_parent_dir, model_dir)
        if os.path.isdir(full_model_dir):
            model_result = evaluate_model(full_model_dir, validation_dir, config_path)
            results[model_dir] = model_result
    return results

def plot_model_comparison(results: Dict[str, Any], output_file: str = "model_comparison.png"):
    models = list(results.keys())
    metrics = list(results[models[0]]["average_scores"].keys())
    
    data = []
    for model in models:
        for metric in metrics:
            data.append({
                "Model": model,
                "Metric": metric,
                "Score": results[model]["average_scores"][metric]
            })
    
    df = pd.DataFrame(data)
    
    plt.figure(figsize=(20, 12))
    sns.barplot(x="Metric", y="Score", hue="Model", data=df)
    plt.xticks(rotation=90)
    plt.title("Model Comparison Across Metrics")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

    # Overall score comparison
    plt.figure(figsize=(10, 6))
    overall_scores = [results[model]["overall_score"] for model in models]
    sns.barplot(x=models, y=overall_scores)
    plt.title("Overall Score Comparison")
    plt.savefig("overall_score_comparison.png")
    plt.close()

    # Processing time comparison
    plt.figure(figsize=(10, 6))
    processing_times = [results[model]["average_processing_time"] for model in models]
    sns.barplot(x=models, y=processing_times)
    plt.title("Average Processing Time Comparison")
    plt.ylabel("Time (seconds)")
    plt.savefig("processing_time_comparison.png")
    plt.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate and compare legal document extraction models")
    parser.add_argument("models_parent_dir", help="Parent directory containing subdirectories for each model's outputs")
    parser.add_argument("validation_dir", help="Directory containing validation files")
    parser.add_argument("config_path", help="Path to the validation configuration JSON file")
    parser.add_argument("--output", default="comparison_results.json", help="Output file for comparison results")

    # args = parser.parse_args()
    args = {
        "models_parent_dir": "../../Documents/Generated/2.models_output/v1_json",
        "validation_dir": "../../Documents/model_validation_files",
        "config_path": "../../Documents/model_validation_files/config_v1.json",
        "output": "benchmark_results.json"
    }

    args = argparse.Namespace(**args)

    # Run the comparison
    results = compare_models(args.models_parent_dir, args.validation_dir, args.config_path)
    # results = compare_models("../../Documents/Generated/2.models_output/v1", "../../Documents/model_validation_files", "../../Documents/model_validation_files/config_v1.json")

    # Save the results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Results saved to {args.output}")
    
    # Generate the comparison charts
    plot_model_comparison(results)

    print("Evaluation complete. Charts have been saved.")


    # Example usage:
    # python model_benchmark.py ../../Documents/Generated/2.models_output/v1 ../../Documents/model_validation_files ../../Documents/model_validation_files/config_v1.json --output comparison_results.json