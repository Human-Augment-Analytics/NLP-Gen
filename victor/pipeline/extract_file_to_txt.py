# extract_file_to_txt.py

import os
import subprocess
import platform
import fitz  # PyMuPDF
import docx
import shutil

def check_file_extension(file_path):
    """
    Checks the file extension and returns the file type.
    """
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()
    if extension == '.pdf':
        return 'pdf'
    elif extension == '.doc' or extension == '.docx':
        return 'doc'
    elif extension == '.txt':
        return 'txt'
    else:
        return None

def convert_doc_to_docx(doc_path):
    """
    Converts a DOC file to DOCX format. Only supports macOS in this implementation.
    """
    docx_path = os.path.splitext(doc_path)[0] + ".docx"

    # For Windows conversion (requires Microsoft Word)
    # if platform.system() == 'Windows':
    #     # Windows conversion using win32com
    #     word = client.Dispatch("Word.Application")
    #     doc = word.Documents.Open(doc_path)
    #     doc.SaveAs(docx_path, FileFormat=16)  # 16 represents DOCX format
    #     doc.Close()
    #     word.Quit()

    if platform.system() == 'Darwin':  # macOS
        subprocess.call(['textutil', '-convert', 'docx', doc_path, '-output', docx_path])
    else:
        raise NotImplementedError("DOC to DOCX conversion is not supported on this operating system.")

    return docx_path

def extract_text_from_pdf(pdf_path, output_location):
    """
    Extracts text from a PDF file using PyMuPDF.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    doc.close()

    output_file_name = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
    output_file_path = os.path.join(output_location, output_file_name)
    with open(output_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

    return output_file_path

def extract_text_from_doc(doc_path, output_location):
    """
    Extracts text from a DOC or DOCX file using python-docx.
    """
    # Convert .doc to .docx if necessary
    if doc_path.endswith('.doc'):
        doc_path = convert_doc_to_docx(doc_path)

    doc = docx.Document(doc_path)
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)

    output_file_name = os.path.splitext(os.path.basename(doc_path))[0] + ".txt"
    output_file_path = os.path.join(output_location, output_file_name)
    with open(output_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

    return output_file_path

def handle_text_file(file_path, output_location):
    """
    Copies a text file to the output location.
    """
    output_file_name = os.path.basename(file_path)
    output_file_path = os.path.join(output_location, output_file_name)
    shutil.copy(file_path, output_file_path)

    return output_file_path

def extract_text(file_path, output_location):
    """
    Main function to extract text from the file based on its type.
    """
    file_type = check_file_extension(file_path)
    if file_type == 'pdf':
        return extract_text_from_pdf(file_path, output_location)
    elif file_type == 'doc':
        return extract_text_from_doc(file_path, output_location)
    elif file_type == 'txt':
        return handle_text_file(file_path, output_location)
    else:
        raise ValueError("Unsupported file type.")
