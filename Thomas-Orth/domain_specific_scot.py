import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from tqdm import tqdm

df = pd.read_csv("/Users/thomasorth/law-clearinghouse-ocr/parsed_documents.csv", sep="|")
doc = df["Document"].iloc[0]

def generate_prompt(document):
    """Generates a prompt for the model to summarize a legal document with emphasis on detailed legal claims and chronological storytelling."""
    prompt = f"""
      CASE: ```{document}```
      You are a law student, skilled in retrieving case information, who is tasked with identifying major entities in the above complaint case. You are to find the listed entities below:
      1. The filing date. If no explicit date is given but a year is, provide the year only.
      2. Full name of the court where the case was filed e.g. “U.S. District Court for the District of New York”. This should include the state district that this course is taking place in.
      3. The name and title of the Judge. Example: District Judge J. Paul Oetken.
      4. Type of counsel (private, legal services, state protection & advocacy system, ACLU, etc.). Please identify legal service organizations by name
      5. Indiciate if this is a class action lawsuit or if it involves individual plantiffs. Do not name any attorneys as plaintiffs.
      6. Who are the defendents?
      7. Who are the plaintiffs? If plaintiffs are not an organization, just describe them.
      7. The plaintiffs legal claims which includes: The Statutory or constitutional basis for claim. If there is a state law claim, note the state.
      8. As part of the remedies for the case, was injuctive relief sought? If so, describe the injuctive relief sought in relation to any judgement.
      9. As part of the remedies for the case, was Declaratory relief sought?
      10. As part of the remedies for the case, was Attorney fees sought and how much?
      11. As part of the remedies for the case, was money damages sought?
      Provide only the requested entities in this list above.
    """
    return prompt

def generate_reduce_cot_prompt(context):
    prompt = f"""
    CONTEXT: ```{context}```
    By using the above context, summarize the case in paragraph format into a concise by informative summary.
    The format of the paragraph should be the following:
    1. The first sentence should be: "This is a case about <factual info>" where <factual info> is the factual background of the case, from the context.
    2. The second sentence should be: "On <date>, <plaintiffs> filed this lawsuit in <court>" where <date> is the date provided by the context, <plaintiffs> are the plaintiff(s), in lowercase, in the case as noted by the context.
    3. The third sentence should be: "<plaintiffs> suded <defendents> under <statute>" where <plaintiffs> are the plaintiff(s) in the case from the context provided, <defendents> are the defendents in the case, and <statute> is the statute that the case is claiming.
    4. The fourth sentence should be: "Represented by <counsel>, <plantiffs> sought <remedy>" where <counsel> is the counsel representing the plaintiffs, <plaintiffs> are the plaintiffs of the case, and <remedy> is the rememdies described in the case, such as injuctive relief, declaratory relief, attorney fees, or money damages.
    5. The last sentence should be: "They claim that <claim>" where claim is the legal claim that the plaintiffs are making.
    Please follow the above format when making the paragraph. Only provide the requested summary, no other text:
    """
    return prompt

prompt = generate_prompt(doc)

llm = ChatOllama(model="llama3.2", temperature=0.0000000001)

ai_msg = llm.invoke(prompt)
ai_msg_sum = llm.invoke(generate_reduce_cot_prompt(ai_msg.content))
print(" ".join(ai_msg_sum.content.split("\n\n")))