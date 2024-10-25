import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_charts(results_file):
    # Read the benchmark results JSON file
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # Convert the results to a pandas DataFrame
    data = []
    for entry in results:
        model_name = entry['model_name']
        hyperparameters = entry['hyperparameters']
        # Create a label combining model name and hyperparameters
        hyperparameters_str = ', '.join([f"{k}={v}" for k, v in hyperparameters.items()])
        # label = f"{model_name} ({hyperparameters_str})"
        label = f"{model_name}"
        data.append({
            'Model': label,
            'Accuracy': entry['average_accuracy'],
            'Precision': entry['average_precision'],
            'Recall': entry['average_recall'],
            'F1 Score': entry['average_f1_score'],
            'Total Processing Time (s)': entry['total_processing_time'],
            'Avg Processing Time per Execution (s)': entry['average_processing_time_per_execution'],
            'Total Correct': entry['total_correct'],
            'Total Incorrect': entry['total_incorrect'],
            'Total False Positives': entry['total_false_positives'],
            'Total Validation Dates': entry['total_validation_dates'],
            'Total Model Dates': entry['total_model_dates'],
        })
    
    df = pd.DataFrame(data)
    
    # Set the style for seaborn
    sns.set(style="whitegrid")
    
    # Create a directory to save the charts
    import os
    charts_dir = 'charts'
    os.makedirs(charts_dir, exist_ok=True)
    
    # Bar charts for metrics
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    for metric in metrics:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=metric, y='Model', data=df, palette='viridis', edgecolor='black')
        plt.title(f'Model Comparison - {metric}')
        plt.xlabel(metric)
        plt.ylabel('Model')
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, f'model_comparison_{metric.lower().replace(" ", "_")}.png'))
        plt.close()
    
    # Bar chart for Total Processing Time
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Total Processing Time (s)', y='Model', data=df, palette='coolwarm', edgecolor='black')
    plt.title('Total Processing Time per Model')
    plt.xlabel('Total Processing Time (seconds)')
    plt.ylabel('Model')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'total_processing_time_per_model.png'))
    plt.close()
    
    # Bar chart for Average Processing Time per Execution
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Avg Processing Time per Execution (s)', y='Model', data=df, palette='magma', edgecolor='black')
    plt.title('Average Processing Time per Execution')
    plt.xlabel('Average Processing Time per Execution (seconds)')
    plt.ylabel('Model')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'average_processing_time_per_execution.png'))
    plt.close()
    
    # If you have multiple hyperparameter combinations for the same model, you can create additional charts
    # For example, let's create a scatter plot of Accuracy vs. Processing Time
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Avg Processing Time per Execution (s)', y='Accuracy', hue='Model', data=df, s=100)
    plt.title('Accuracy vs. Avg Processing Time per Execution')
    plt.xlabel('Average Processing Time per Execution (seconds)')
    plt.ylabel('Accuracy')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'accuracy_vs_processing_time.png'))
    plt.close()
    
    print(f"Charts have been generated and saved in the '{charts_dir}' directory.")

if __name__ == '__main__':
    results_file = 'benchmark_results.json'
    generate_charts(results_file)
