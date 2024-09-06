from summarizers.get_complaints import get_complaint_only_cases
from summarizers.ocr import read_doc, extract_text_from_pdf
from tqdm import tqdm
import pandas as pd

data = get_complaint_only_cases("/Users/thomasorth/Downloads/all_cases_clearinghouse.pkl")

data_entries = []
for entry in tqdm(data):
    summary = entry.summary
    if not summary or len(summary) < 1 or not entry or not entry.case_documents or len(entry.case_documents) < 1:
        continue
    doc = entry.case_documents[0]
    document_text = read_doc(doc)
    data_entries.append((document_text, summary))

df = pd.DataFrame(data_entries, columns=["Document", "Summary"])
print(len(df))
df.to_csv("parsed_documents.csv", sep="|", index=False)
