# ANSI escape codes for colors
GREEN = '\033[92m'
BLUE = '\033[94m'
WHITE = '\033[97m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_color(text, color = WHITE):
    print(f"{color}{text}{RESET}")