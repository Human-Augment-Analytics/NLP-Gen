import spacy
import subprocess
import sys

# ANSI escape codes for colored output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def ensure_model_installed(model_name):
    """
    Check if the specified spaCy model is installed, and if not, attempt to install it.
    
    Args:
    model_name (str): Name of the spaCy model to check/install

    Returns:
    bool: True if the model is installed (or was successfully installed), False otherwise
    """
    try:
        spacy.load(model_name)
        print(f"{GREEN}{model_name} is already installed.{RESET}")
        return True
    except OSError:
        print(f"{YELLOW}{model_name} not found. Attempting to install...{RESET}")
        try:
            subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
            print(f"{GREEN}{model_name} successfully installed.{RESET}")
            return True
        except subprocess.CalledProcessError:
            print(f"{RED}Failed to install {model_name}. Please install it manually using:")
            print(f"python -m spacy download {model_name}{RESET}")
            return False

if __name__ == "__main__":
    # This allows the script to be run standalone to install models
    model_name = "es_core_news_lg"  # Default to Spanish large model
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
    ensure_model_installed(model_name)