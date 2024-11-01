import pandas as pd
from langchain_anthropic import ChatAnthropic
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

df = pd.read_csv("settlements_tmp.csv")

def generate_prompt(document):
    prompt = f"""
    You are a law student tasked with extracting key information from a chunk of text belonging to a settlement document. Your goal is to identify and extract important details, provide citations for each extracted piece of information, and then create a partial summary based on the extracted information.

    Here is the chunk of text from the settlement document:

    <settlement_text>
    {document}
    </settlement_text>

    Your task is to:

    1. Extract key information from the text. This may include, but is not limited to:
      - Parties involved
      - Filing date
      - Monetary amounts
      - Key terms or conditions
      - Deadlines or important dates
      - Any specific legal language or clauses

    2. For each piece of extracted information, provide a citation. The citation should be the exact quote from the original text that supports the extracted information. Format your extracted information and citations as follows:

    <extracted_info>
    [Key Information]: [Your extracted information]
    [Citation]: "Exact quote from the text"
    </extracted_info>

    3. After extracting the key information, provide a partial summary of this chunk of text using the extracted information. The summary should be concise but comprehensive, capturing the main points of the settlement chunk.

    Present your findings in the following format:

    <key_information>
    [List your extracted information with citations here]
    </key_information>

    <summary>
    [Your partial summary of the chunk based on the extracted information]
    </summary>

    Remember to be thorough in your extraction of key information, accurate in your citations, and concise yet comprehensive in your summary.
    """
    return prompt

def generate_prompt_combined(chunks):
    prompt = f"""
    You are a law student tasked with creating a concise summary of a settlement document. You will be provided with chunks of extracted information from the settlement document. Your goal is to analyze this information and create a clear, concise summary of the settlement, including a bulleted list of its key terms.

    Here are the chunks of information from the settlement document:

    <settlement_chunks>
    {chunks}
    </settlement_chunks>

    Please follow these steps to complete your task:

    1. Carefully read and analyze all the provided chunks of information from the settlement document.

    2. Identify the key components of the settlement, including but not limited to:
      - Parties involved
      - Filling date
      - Key terms and conditions
      - Financial arrangements (if any)
      - Timelines or deadlines
      - Any special provisions or clauses

    3. Create a brief introductory paragraph summarizing the overall nature and purpose of the settlement. This should include the parties involved, the date of the settlement, and a high-level overview of what the settlement aims to resolve.

    4. List the key terms of the settlement in a bulleted format. Each bullet point should be concise but informative, capturing the essential details of each term.

    5. If there are any notable or unusual aspects of the settlement, briefly mention these in a concluding paragraph.

    Present your summary in the following format:

    <summary>
    [Introductory paragraph here]

    Key Terms of the Settlement:
    • [Bullet point 1]
    • [Bullet point 2]
    • [Bullet point 3]
    [...continue with all relevant bullet points]

    [Concluding paragraph here, if applicable]
    </summary>

    Remember to use clear, professional language throughout your summary. Avoid legal jargon where possible, but retain any necessary legal terms that are crucial to understanding the settlement. Your goal is to create a summary that would be easily understood by someone with basic legal knowledge.
    """
    return prompt

model_name = "claude-3-haiku-20240307"

csv_data = []
llm = ChatAnthropic(model=model_name, temperature=0.0000000001)
for sample in tqdm(range(len(df))):
  doc = df["Text"].iloc[sample]
  case_name = df["Case Name"].iloc[sample]
  texts = text_splitter.create_documents([doc])
  chunks = []
  for text in texts:
    chunks.append(llm.invoke(generate_prompt(text)).content)

  combined_chunk_elements = ' \n'.join([f"Chunk {idx+1} out of {len(chunks)}: \n" +  chunk
                                            for idx, chunk
                                            in enumerate(chunks)])

  ai_msg_sum = llm.invoke(generate_prompt_combined(combined_chunk_elements))
  summary =  re.search(r'<summary>\n(.*?)\n</summary>', ai_msg_sum.content, re.DOTALL).group(1).strip()
  print(summary + "\n")
  break
  """
  csv_data.append((case_name, summary))

pd.DataFrame(csv_data, columns=["Case Name", "Summary"]).to_csv("generated_settlement_summaries.csv", index=False)
"""