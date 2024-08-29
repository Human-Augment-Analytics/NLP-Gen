import docx
# from docx import Document # For Windows conversion (requires Microsoft Word) 

import os

# from win32com import client  # For Windows conversion (requires Microsoft Word)
import subprocess
import platform  # To detect the operating system

import pypdf

def check_file_extension(file_path):
    """
    Checks the file extension and returns 'pdf' or 'doc' if it's a supported type, otherwise None.

    Args:
        file_path: The path to the file.
    """

    _, extension = os.path.splitext(file_path)
    if extension.lower() == '.pdf':
        return 'pdf'
    elif extension.lower() == '.doc' or extension.lower() == '.docx':
        return 'doc'
    else:
        return None
    
def convert_doc_to_docx(doc_path):
    """
    Converts a legacy DOC file to DOCX format.

    Args:
        doc_path: The path to the DOC file.
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
        # macOS conversion using subprocess (requires 'textutil' command)
        subprocess.call(['textutil', '-convert', 'docx', doc_path, '-output', docx_path])
    else:  # Linux or other unsupported OS
        raise NotImplementedError("DOC to DOCX conversion is not supported on this operating system")

    return docx_path

def extract_text_from_pdf(pdf_path, output_location):
    """
    Extracts text from a PDF file and saves it to a .txt file.

    Args:
        pdf_path: The path to the PDF file.
        output_location: The directory where the output .txt file should be saved.
    """

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = pypdf.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()


    # Create output file name based on the PDF file name
    output_file_name = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
    output_file_path = os.path.join(output_location, output_file_name)

    with open(output_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)


def extract_text_from_doc(doc_path, output_location):
    """
    Extracts text from a DOC file and saves it to a .txt file.

    Args:
        doc_path: The path to the DOC file.
        output_location: The directory where the output .txt file should be saved.
    """
    # If it's a .doc file, convert it to .docx first
    if doc_path.endswith('.doc'):
        doc_path = convert_doc_to_docx(doc_path)

    doc = docx.Document(doc_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    # Create output file name based on the DOC file name
    output_file_name = os.path.splitext(os.path.basename(doc_path))[0] + ".txt"
    output_file_path = os.path.join(output_location, output_file_name)

    with open(output_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

def process_file_or_folder(single_file=None, folder=None, output_location="output_texts"):
    """
    Processes a single file or all files in a folder, extracting text and saving it to .txt files.

    Args:
        single_file: The path to a single file (optional).
        folder: The path to a folder containing files (optional).
        output_location: The directory where the output .txt files should be saved (default: "output_texts").
    """

    if single_file:
        file_extension = check_file_extension(single_file)
        if file_extension == 'pdf':
            extract_text_from_pdf(single_file, output_location)
            print(f"Text extracted from {single_file} and saved to {output_location}")
        elif file_extension == 'doc':
            extract_text_from_doc(single_file, output_location)
            print(f"Text extracted from {single_file} and saved to {output_location}")
        else:
            print(f"Unsupported file type: {single_file}")

    elif folder:
        if not os.path.exists(output_location):
            os.makedirs(output_location)

        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            if os.path.isfile(file_path):
                file_extension = check_file_extension(file_path)
                if file_extension == 'pdf':
                    extract_text_from_pdf(file_path, output_location)
                    print(f"Text extracted from {file_name} and saved to {output_location}")
                elif file_extension == 'doc':
                    extract_text_from_doc(file_path, output_location)
                    print(f"Text extracted from {file_name} and saved to {output_location}")


# Accept single file or folder as input when running the script
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract text from PDF or DOC files and save it to .txt files.")
    parser.add_argument("-f", "--file", help="Path to a single file to process")
    parser.add_argument("-d", "--directory", help="Path to a directory containing files to process")
    parser.add_argument("-o", "--output", help="Directory where output .txt files should be saved")

    args = parser.parse_args()

    if args.file:
        process_file_or_folder(single_file=args.file, output_location=args.output)
    elif args.directory:
        process_file_or_folder(folder=args.directory, output_location=args.output)
    else:
        print("Please provide a file or directory to process.")
