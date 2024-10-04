import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage

df = pd.read_csv("/Users/thomasorth/law-clearinghouse-ocr/parsed_documents.csv", sep="|")
doc = df["Document"].iloc[0]

def generate_prompt(document):
    """Generates a prompt for the model to summarize a legal document with emphasis on detailed legal claims and chronological storytelling."""
    prompt = f"""
      CASE: ```{document}```
      You are a law student tasked with identifying major entities in the above complaint case. You are to find the listed entities below:
      1. The filing date. If no explicit date is given but a year is, provide the year only.
      2. Full name of the court where the case was filed e.g. “U.S. District Court for the District of New York”. This should include the state district that this course is taking place in.
      3. The name and title of the Judge. Example: District Judge J. Paul Oetken.
      4. Type of counsel. Such as: private, legal services, state protection & advocacy system, ACLU, etc. Do not list organizations or names.
      5. Indiciate if this is a class action lawsuit or if it involves individual plantiffs. Do not name any attorneys as plaintiffs.
      6. Who are the defendents?
      7. Who are the plaintiffs? If plaintiffs are not an organization, just describe them.
      7. The plaintiffs legal claims which includes: The Statutory or constitutional basis for claim If there is a state claim, note the state.
      8. As part of the remedies for the case, was injuctive relief sought? If so, describe the injuctive relief sought in relation to any judgement.
      9. As part of the remedies for the case, was Declaratory relief sought?
      10. As part of the remedies for the case, was Attorney fees sought and how much?
      11. As part of the remedies for the case, was money damages sought? If so, what kind?
      Provide only the requested entities in this list above.
    """
    return prompt

prompt = generate_prompt(doc)

llm = ChatOllama(model="llama3.2")

ai_msg = llm.invoke(prompt)
print(ai_msg.content)