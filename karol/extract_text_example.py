import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Exception: {e}")
        return None

def extract_text(pdf_folder_path, txt_folder_path):
    pdf_files = [f for f in os.listdir(pdf_folder_path) if f.endswith('.pdf')]
    extracted_texts = {}

    if not os.path.exists(txt_folder_path):
        os.makedirs(txt_folder_path)

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder_path, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        if text:
            extracted_texts[pdf_file] = text
            print(f"Extracted text from {pdf_file}")
        else:
            print(f"Failed to extract text from {pdf_file}")

    return extracted_texts

if __name__ == "__main__":
    pdf_folder_path = "./sentencias"
    txt_folder_path = "./txt"

    extracted_texts = extract_text(pdf_folder_path, txt_folder_path)

    # Save into txt files in ./txt folder
    for pdf_file, text in extracted_texts.items():
        text_file_name = os.path.splitext(pdf_file)[0] + ".txt"
        text_file_path = os.path.join(txt_folder_path, text_file_name)
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
        print(f"Saved extracted text to {text_file_name}")
