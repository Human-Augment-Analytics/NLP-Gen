import requests


import pandas as pd

df = pd.read_csv("/Users/thomasorth/law-clearinghouse-ocr/parsed_documents.csv", sep="|")
cases = ['People ex rel. Harpaz o/b/o Vance v. Brann',
 'Adkins v. State of Idaho',
 'Munday v. Beaufort County',
 'Planned Parenthood South Atlantic v. South Carolina',
 'Planned Parenthood South Atlantic v. State of South Carolina',
 'Macer v. Dinisio',
 'Kariye v. Mayorkas',
 'T.M. v. City of Philadelphia',
 'Sanders v. District of Columbia',
 'Strifling v. Twitter, Inc.',
 "Mohler v. Prince George's County"]
cases = [cases[5]]

df = df[df["Case Name"].isin(cases)]
doc = df["Document"].iloc[0]
case_name = df["Case Name"].iloc[0]

url = "http://localhost:8000/summarize"
params = {"doc_type": "complaint", "document": doc}

response = requests.post(url, params=params, stream=True)

for chunk in response.iter_lines():
    if chunk:
        print(chunk.decode("utf-8"), end="", flush=True)