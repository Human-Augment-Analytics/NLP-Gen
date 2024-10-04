
import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from tqdm import tqdm

model = "llama3.2"
temperature = 0.4
llm = ChatOllama(model=model, temperature=temperature)
df = pd.read_csv("/Users/thomasorth/law-clearinghouse-ocr/parsed_documents.csv", sep="|").dropna()

def generate_sum_cot_prompt(document):
    """Generates a prompt for the model to summarize a legal document with emphasis on detailed legal claims and chronological storytelling."""
    prompt = f"""
    CASE: ```{document}```
    For the above court case:
    What are the important entities in this document?
    What are the important dates in this document?
    What events are happening in this document?
    What is the result of these events?
    Please answer the above questions:
    """
    return prompt

def generate_reduce_cot_prompt(document, context):
    """Generates a prompt for the model to summarize a legal document with emphasis on detailed legal claims and chronological storytelling."""
    prompt = f"""
    CASE: ```{document}```
    CONTEXT: ```{context}```
    By using the above context, summarize the case in past tense and in paragraph format into a concise by informative summary. If a date is mentioned, mention that in the summary.
    If no date is found, do not mention it. Do not make note of any content you decided to exclude. Only use the information provided in the case and the content to create the summary.
    Only provide the summary, do not include any text outside the summary:
    """
    return prompt

predicted_summaries = []
cot_info_extracted = []
pbar = tqdm(range(1))
for i in pbar:
    doc = df["Document"].iloc[0]
    pbar.set_description(f"Size of Document: {len(doc)}")
    prompt = generate_sum_cot_prompt(doc)

    ai_msg = llm.invoke(prompt)
    cot_info = ai_msg.content
    sum_prompt = generate_reduce_cot_prompt(doc, cot_info)
    ai_msg_final = llm.invoke(sum_prompt)
    predicted_summaries.append(ai_msg_final.content)
    cot_info_extracted.append(cot_info)
    print(ai_msg_final.content)


"""
df["cot_info_extracted"] = cot_info_extracted
df["predicted_summary"] = predicted_summaries
df.to_csv(f"generated_results_{model}_temperature_{temperature}.csv", sep="|", index=False)
"""