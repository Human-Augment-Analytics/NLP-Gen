import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import XMLOutputParser
from langchain_core.messages import AIMessage
from tqdm import tqdm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
import uuid
import re

# Calculate chunk size
chunk_size = 90000
chunk_overlap = 1000

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    length_function=len,
    is_separator_regex=False,
)

df = pd.read_csv("/Users/thomasorth/Downloads/clearinghouse_settlements_ocr_df_complete.csv")
case_ids = [2, 31, 83, 192, 217, 293, 301, 303, 307, 43537, 44070]
df = df[df["case_id"].isin(case_ids)]

def generate_prompt(document):
    prompt = f"""
      You are a law student tasked with extracting key information from a chunk of a settlement agreement. Your goal is to identify and summarize specific elements of the agreement. Here is the settlement chunk you will analyze:

      <settlement_chunk>
      {document}
      </settlement_chunk>

      Please extract the following information from the settlement chunk:

      1. Actions to be Taken by Defendants: Describe who has agreed to do what. Be very detailed in providing this information.
      2. Damages (Money): Identify who is paying for what, including attorney fees. For the money to be paid to plaintiffs, do not name the plaintiffs and report the total sum to be paid to plaintifs
      3. Implementation and Enforcement: Note if there's a court-appointed "monitor" or other oversight.
      4. Duration: How long the settlement is in effect.
      5. Conditional Agreements: Mention any conditions for the settlement (e.g., "will only agree IF ...").
      6. Policy Adoptions: Note any agreement to adopt policies and provide any relevant details about those policies. Do not omit important information and describe in detail. Do not include names of the policies, just the details of the policies.
      7. The date of the settlement: This is typically the document's filing date, the date the document is dated, or the date of execution
      8. The type of settlement: This is the type of settlement that was entered by this document.

      For each piece of information you extract, include a citation of the text from the settlement chunk that supports your conclusion. Use the following format:

      <citation>"Exact quote from the text"</citation>

      If any of the requested information is not present in the settlement chunk, state "Not Specified" for that item.

      If any acronyms are present and their definitions are defined, please spell out the acronym the first time its used.

      After extracting the information, provide a brief summary of your findings.

      Important: Do not extract or include the following types of information:
      - Introductory and Boilerplate Information
      - Reporting Information (how parties must report progress)
      - Notice for Class Actions (how parties must give notice to consumers for class action suits)
      - Giving Up Claims or Admitting Fault (it's a given that settling parties must give up claims)

      Present your findings in the following format:

      <extracted_information>
      1. Actions to be Taken by Defendants:
      [Your summary]
      [Citation if applicable]

      2. Damages (Money):
      [Your summary]
      [Citation if applicable]

      3. Implementation and Enforcement:
      [Your summary]
      [Citation if applicable]

      4. Duration:
      [Your summary]
      [Citation if applicable]

      5. Conditional Agreements:
      [Your summary]
      [Citation if applicable]

      6. Policy Adoptions:
      [Your summary]
      [Citation if applicable]

      7. Date of the settlement:
      [Your info]
      [Citation if applicable]

      8. Type of settlement:
      [Your info]
      [Citation if applicable]
      </extracted_information>

      <summary>
      [Your brief summary of the key points found in the settlement chunk]
      </summary>
    """
    return prompt

def generate_prompt_combined(chunks):
    prompt = f"""
      You are a law student skilled at distilling sets of extracted information and partial summaries into informative summaries. You will be provided with a set of extracted information and a partial summary about a legal settlement. Your task is to create a concise, one-paragraph summary of the settlement.

      Here is the set of extracted information and partial summary:

      <extracted_info_and_summary>
      {chunks}
      </extracted_info_and_summary>

      Using the provided information, create a summary of the settlement following these guidelines:

      1. Begin with a sentence describing when the settlement was entered, including the specific date and the type of settlement that was entered.
      2. If the case was not dismissed in the settlement, include information on the following aspects, if available:
        - Actions to be Taken by Defendants
        - Damages (Money)
        - Implementation and Enforcement
        - Duration
        - Conditional Agreements
        - Policy Adoptions
      3. If the settlement was dismissed, talk about why it was dismissed and what the outcome was.
      4. Keep the summary to one paragraph.
      5. If any information provides a citation, do not use that information in your summary.
      6. Do not omit any of the actions or policy adoptions noted.
      7. Write the summary in past tense.
      8. If for the requested information, all of the chunks say "Not Specified", do not include that information in the summary.

      Carefully review the extracted information and partial summary to ensure you capture all relevant details. Focus on presenting the most important aspects of the settlement in a clear and concise manner.
      On;y provide the requested summary.
    """
    return prompt

model_name = "gemini-1.5-pro"

csv_data = []
llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.1)
for sample in tqdm(range(len(df))):
  doc = df["clean_text"].iloc[sample]
  case_name = df["case_name"].iloc[sample]
  case_id = df["case_id"].iloc[sample]
  texts = text_splitter.create_documents([doc])
  chunks = []
  for text in texts:
    msg = llm.invoke(generate_prompt(text)).content
    chunks.append(msg)

  combined_chunk_elements = ' \n'.join([f"Chunk {idx+1} out of {len(chunks)}: \n" +  chunk
                                            for idx, chunk
                                            in enumerate(chunks)])

  ai_msg_sum = llm.invoke(generate_prompt_combined(combined_chunk_elements))
  summary =  ai_msg_sum.content
  csv_data.append((case_name, case_id, summary))

pd.DataFrame(csv_data, columns=["Case Name", "Case Id", "Summary"]).to_csv("generated_settlement_summaries_with_clearinghouse_feedback_v7.csv", index=False)
