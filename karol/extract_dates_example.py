import os
import re
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

# Regexs in Spanish
date_patterns = [
    r"\b\d{1,2} de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre) de \d{4}\b",
    r"\b\d{1,2}/\d{1,2}/\d{4}\b",
    r"\b\d{1,2}-\d{1,2}-\d{4}\b",
    r"\b(\d+|[a-z]+) \(\d{1,2}\) días del mes de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre) del año (dos mil \w+|\d{4})\b",
]

# Spanish months mapping to numbers
months_mapping = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12",
}

def preprocess_text(text):
    preprocessed_text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    preprocessed_text = re.sub(r'\n+', ' ', preprocessed_text)
    return preprocessed_text

def parse_date(date_string):
    if isinstance(date_string, tuple):
        date_string = ' '.join(date_string)
    
    for pattern in date_patterns:
        match = re.search(pattern, date_string, flags=re.IGNORECASE)
        if match:
            if "de" in date_string:
                day = match.group(0).split(" de ")[0]
                month = months_mapping[match.group(0).split(" de ")[1]]
                year = match.group(0).split(" de ")[2]
                date_string = f"{day}/{month}/{year}"
            elif "días del mes de" in date_string:
                day = match.group(0).split()[1].strip("()")
                month = months_mapping[match.group(0).split(" del mes de ")[1].split(" del año ")[0]]
                year = match.group(0).split(" del año ")[1]
                date_string = f"{day}/{month}/{year}"
            try:
                return datetime.strptime(date_string, "%d/%m/%Y")
            except ValueError:
                return None
    return None

def extract_dates_from_text(text):
    text = preprocess_text(text)
    dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            date_obj = parse_date(match)
            if date_obj:
                dates.append(date_obj)
    return dates

def extract_dates_from_files_in_folder(folder_path):
    extracted_dates = []

    for text_file in os.listdir(folder_path):
        if text_file.endswith('.txt'):
            file_path = os.path.join(folder_path, text_file)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                dates = extract_dates_from_text(text)
                if dates:
                    extracted_dates.extend(dates)
                    print(f"Extracted dates from {text_file}: {dates}")

    return extracted_dates

def plot_date_frequencies(dates):
    date_counts = Counter(dates)
    sorted_dates = sorted(date_counts.items())
    dates, counts = zip(*sorted_dates)

    # Plotting the date frequencies
    plt.figure(figsize=(10, 6))
    plt.plot(dates, counts, marker='o')
    plt.title('Frequency of Extracted Dates')
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    txt_folder_path = "./txt"
    extracted_dates = extract_dates_from_files_in_folder(txt_folder_path)

    if extracted_dates:
        plot_date_frequencies(extracted_dates)
        output_file = os.path.join('.', "extracted_dates.txt")
        with open(output_file, 'w', encoding='utf-8') as out_file:
            for date in extracted_dates:
                out_file.write(f"{date.strftime('%d/%m/%Y')}\n")
            print(f"Saved extracted dates to {output_file}")
