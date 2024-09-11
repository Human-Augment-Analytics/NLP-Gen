from openapi_client.models.document import Document
from urllib.request import urlretrieve
import pypdf

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = pypdf.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text 

def read_doc(doc):
    urlretrieve(doc.file, '/tmp/doc.pdf')
    return extract_text_from_pdf('/tmp/doc.pdf')

