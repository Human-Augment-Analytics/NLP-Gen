import os
import json
import unicodedata
from query_model_main import log_in_color

def normalize_str(s):
    if s is None:
        return ''
    return unicodedata.normalize('NFC', s.strip())

def validate_model_outputs(models_output_folder, validation_set_folder, results_file):
    # Dictionary to store accumulated metrics per model and hyperparameters
    model_hyperparam_metrics = {}

    # For each document in models_output_folder
    for document_name in os.listdir(models_output_folder):
        # Log the document being processed
        log_in_color(f"Processing document: {document_name}", "green")
        document_path = os.path.join(models_output_folder, document_name)
        if not os.path.isdir(document_path):
            continue

        # Get the validation set for this document
        validation_set_file = os.path.join(validation_set_folder, f"{document_name}_validation.json")
        if not os.path.isfile(validation_set_file):
            print(f"Validation set for '{document_name}' not found.")
            continue

        with open(validation_set_file, 'r', encoding='utf-8') as f:
            validation_set = json.load(f)

        # For each model in this document's folder
        for model_name in os.listdir(document_path):
            # Log the model being processed
            log_in_color(f"Processing model: {model_name}", "blue")
            model_path = os.path.join(document_path, model_name)
            if not os.path.isdir(model_path):
                continue

            # Read the model outputs
            model_output_file = os.path.join(model_path, f"{document_name}_{model_name}.json")
            if not os.path.isfile(model_output_file):
                print(f"Model output file '{model_output_file}' not found.")
                continue

            with open(model_output_file, 'r', encoding='utf-8') as f:
                model_outputs = json.load(f)

            # Read the execution metrics
            metrics_file = os.path.join(model_path, f"{document_name}_{model_name}_metrics.json")
            if os.path.isfile(metrics_file):
                with open(metrics_file, 'r', encoding='utf-8') as f:
                    execution_metrics = json.load(f)
            else:
                execution_metrics = []

            # Validate the model outputs against the validation set
            correct = 0
            incorrect = 0
            used_model_indices = set()

            for val_date_obj in validation_set:
                val_date = normalize_str(val_date_obj.get('date'))
                val_event = normalize_str(val_date_obj.get('date event'))
                match_found = False

                # Search for val_date in model outputs
                for idx, model_output in enumerate(model_outputs):
                    # Log the model output index being processed
                    log_in_color(f"Processing model output index: {idx}", "magenta")
                    if idx in used_model_indices:
                        continue  # Skip already matched outputs

                    mod_date = model_output.get('date', '')
                    mod_event = model_output.get('date event', '')
                    # Check if date and date event are strings, if not, cast them to strings
                    if not isinstance(mod_date, str):
                        mod_date = str(mod_date)
                    if not isinstance(mod_event, str):
                        mod_event = str(mod_event)
                    mod_date = normalize_str(mod_date)
                    mod_event = normalize_str(mod_event)

                    if val_date == mod_date:
                        used_model_indices.add(idx)
                        match_found = True

                        # Check if date events match
                        if val_event == mod_event:
                            # Correct response
                            correct += 1
                        else:
                            # Check for 'otros' in both date events
                            if 'otros' in val_event.lower() and 'otros' in mod_event.lower():
                                correct += 1
                            else:
                                incorrect += 1
                        break

                if not match_found:
                    # Date not found in model outputs
                    incorrect += 1

            # Any remaining model outputs are false positives
            false_positives = len(model_outputs) - len(used_model_indices)
            total_validation_dates = len(validation_set)
            total_model_dates = len(model_outputs)

            # Calculate metrics
            precision = correct / (correct + false_positives) if (correct + false_positives) > 0 else 0
            recall = correct / total_validation_dates if total_validation_dates > 0 else 0
            f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            accuracy = correct / total_validation_dates if total_validation_dates > 0 else 0

            # Get hyperparameters from the first execution detail
            if execution_metrics:
                hyperparameters = execution_metrics[0].get('hyperparameters', {})
                # Sum processing times
                total_processing_time = sum([em.get('processing_time', 0.0) for em in execution_metrics])
                execution_count = len(execution_metrics)
            else:
                hyperparameters = {}
                total_processing_time = 0.0
                execution_count = 0
                print(f"No execution metrics found for model {model_name} on document {document_name}")

            # Create key for the model and hyperparameters
            hyperparameters_tuple = tuple(sorted(hyperparameters.items()))
            key = (model_name, hyperparameters_tuple)

            # Initialize or update the metrics in the dictionary
            if key not in model_hyperparam_metrics:
                model_hyperparam_metrics[key] = {
                    'model_name': model_name,
                    'hyperparameters': hyperparameters,
                    'documents': set(),  # Set of documents evaluated
                    'total_correct': 0,
                    'total_incorrect': 0,
                    'total_false_positives': 0,
                    'total_validation_dates': 0,
                    'total_model_dates': 0,
                    'sum_precision': 0.0,
                    'sum_recall': 0.0,
                    'sum_f1_score': 0.0,
                    'sum_accuracy': 0.0,
                    'total_processing_time': 0.0,
                    'execution_count': 0,
                }

            metrics = model_hyperparam_metrics[key]

            # Update the set of documents
            metrics['documents'].add(document_name)

            # Accumulate performance metrics
            metrics['total_correct'] += correct
            metrics['total_incorrect'] += incorrect
            metrics['total_false_positives'] += false_positives
            metrics['total_validation_dates'] += total_validation_dates
            metrics['total_model_dates'] += total_model_dates
            metrics['sum_precision'] += precision
            metrics['sum_recall'] += recall
            metrics['sum_f1_score'] += f1_score
            metrics['sum_accuracy'] += accuracy

            # Update processing time and execution count
            metrics['total_processing_time'] += total_processing_time
            metrics['execution_count'] += execution_count

    # Now, after processing all documents and models, prepare the results
    final_results = []

    for key, metrics in model_hyperparam_metrics.items():
        n = len(metrics['documents'])  # Number of documents evaluated
        # Calculate average metrics
        average_precision = metrics['sum_precision'] / n if n > 0 else 0
        average_recall = metrics['sum_recall'] / n if n > 0 else 0
        average_f1_score = metrics['sum_f1_score'] / n if n > 0 else 0
        average_accuracy = metrics['sum_accuracy'] / n if n > 0 else 0
        average_processing_time = metrics['total_processing_time'] / metrics['execution_count'] if metrics['execution_count'] > 0 else 0

        # Prepare result entry
        result_entry = {
            'model_name': metrics['model_name'],
            'hyperparameters': metrics['hyperparameters'],
            'documents_evaluated': list(metrics['documents']),
            'total_correct': metrics['total_correct'],
            'total_incorrect': metrics['total_incorrect'],
            'total_false_positives': metrics['total_false_positives'],
            'total_validation_dates': metrics['total_validation_dates'],
            'total_model_dates': metrics['total_model_dates'],
            'average_precision': average_precision,
            'average_recall': average_recall,
            'average_f1_score': average_f1_score,
            'average_accuracy': average_accuracy,
            'total_processing_time': metrics['total_processing_time'],
            'average_processing_time_per_execution': average_processing_time,
        }

        final_results.append(result_entry)

    # Write the final results to the benchmark_results.json file
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)

    print(f"Results written to '{results_file}'")

if __name__ == '__main__':
    models_output_folder = 'models_output'
    validation_set_folder = '3.extracted_dates_sample'
    results_file = 'benchmark_results.json'

    validate_model_outputs(models_output_folder, validation_set_folder, results_file)
