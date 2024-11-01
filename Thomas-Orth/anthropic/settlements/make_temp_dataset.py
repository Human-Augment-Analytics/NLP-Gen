from unstructured.partition.pdf import partition_pdf
ids = [82472, 152022, 151557, 130154]
cases = ["Adams v Kentucky", "Progeny v. City of Wichita", "Terrill v. Oregon", "Remick v. City of Philadelphia"]

def extract_text_from_pdf(pdf_path):
  elements = partition_pdf(pdf_path)
  parsed_text = "\n".join([element.text for element in elements])
  return parsed_text

data = []
for id, case in zip(ids, cases):
    path = f"pdfs/{id}.pdf"
    text = extract_text_from_pdf(path)
    data.append((case, id, text))

import pandas as pd

df = pd.DataFrame(data, columns=["Case Name", "Doc ID", "Text"])
df.to_csv("settlements_tmp.csv", index=False)
