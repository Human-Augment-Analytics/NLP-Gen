from summarizers.get_complaints import get_complaint_only_cases
from summarizers.ocr import read_doc, extract_text_from_pdf
from tqdm import tqdm
import pandas as pd
import os
from urllib.request import urlretrieve

os.mkdir('pdfs')

data = get_complaint_only_cases("all_cases_clearinghouse.pkl")

data_entries = []
for entry in tqdm(data):
    if not entry or not entry.case_documents or len(entry.case_documents) < 1:
        continue
    
    for i, case_doc in enumerate(entry.case_documents):
        #doc = entry.case_documents[-1]
        urlretrieve(case_doc.file, f'pdfs/{entry.id}_{i}.pdf')
