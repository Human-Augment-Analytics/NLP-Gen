import pandas as pd
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage
from tqdm import tqdm
import uuid
import datetime

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

df = df[df["Case Name"].isin(cases)]

def generate_prompt(document):
    """Generates a prompt for the model to summarize a legal document with emphasis on detailed legal claims and chronological storytelling."""
    prompt = f"""
      CASE: ```{document}```
      You are a law student, skilled in retrieving case information, who is tasked with identifying major information in the above chunk of a case document. You are to find the requested information below:
      1. The filing date.
      2. Full name of the court where the case was filed.
      3. The name and title of the Judge for this case.
      4. Type of counsel (private, legal services, state protection & advocacy system, ACLU, etc.). Please identify legal service organizations by name
      5. Identify the important parties such as plaintiffs and defendants. For individual plaintiffs, only give a description that makes clear their background and circumstances and no names. For organizations, give names.
      6. Is this a class action lawsuit?
      7. The plaintiffs' legal claims: Describe any legal claims including statutes or consitutional claims.
      8. What rememdies were sought? Describe any declaratory relief, injuctive relief, attorney fees or money fees requested in specific detail when provided by the document.
      9. Any results or events not covered in the list currently.
      10. Highlight any elements of the case that add storytelling value, such as notable conflicts, events or significant turning points in the litigation.
      Provide only the extracted entities:
    """
    return prompt

def generate_reduce_cot_prompt(context):
    prompt = f"""
    CONTEXT: ```{context}```
    You are a law student, skilled at summarizing complaint cases. You are to take the provided summaries and distil them into one final summary, in paragraph format, even if the case is not publically available. Ensure to follow the following guidelines:
    1. Start with a lede sentence to draw in the reader. If it was a class action case, include this in the lede sentence.
    2. Next, describe the facts of case
    3. Mention the important details such as:
        * Filing Date
        * Full name of the court where the case was filed
        * The plaintiffs and defendants, using only descriptions that make clear their background and circumstances and no names for individual plaintiffs and names for organizations.
        * The legal counsel for the plaintiffs
        * The plaintiffs legal claims, providing information about any statutes and consitutional claims.
        * The rememdies sought by the plaintifs, providing specific details and information about the declaratory relief, injuctive relief, attorney fees or money fees requested when presented in the document.
        * Highlight any elements of the case that add storytelling value, such as notable conflicts, events, or significant turning points in the litigation.
    4. Do not end with any claim of impact this case would have at all. Only stick to the facts of the case.
    5. Provide the summary in past tense
    Only provide the requested summary:
    """
    return prompt
  
csv_data = []
model_name = "claude-3-5-sonnet-20240620"
llm = ChatAnthropic(model=model_name, temperature=0.0000000001)
for sample in tqdm(range(len(cases))):
  doc = df["Document"].iloc[sample]
  case_name = df["Case Name"].iloc[sample]
  summary = df["Summary"].iloc[sample]

  prompt = generate_prompt(doc)


  ai_msg = llm.invoke(prompt)
  ai_msg_sum = llm.invoke(generate_reduce_cot_prompt(ai_msg.content))
  sum_join = " ".join(ai_msg_sum.content.split("\n\n"))
  csv_data.append((case_name, summary, sum_join))
df_save = pd.DataFrame(csv_data, columns=["Case Name", "Ground Truth Summary", "Generated Summary"])
df_save.to_csv(f"generated_results_{model_name}_full_{datetime.datetime.now()}.csv")
