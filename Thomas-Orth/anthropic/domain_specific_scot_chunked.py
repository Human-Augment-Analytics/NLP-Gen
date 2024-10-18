import pandas as pd
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage
from tqdm import tqdm
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid

# Calculate chunk size
chunk_size = 15000
chunk_overlap = 1000

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    length_function=len,
    is_separator_regex=False,
)

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
    prompt = f"""
      CHUNK: ```{document}```
      You are a law student, skilled in retrieving case information, who is tasked with identifying major information in the above chunk of a case document. You are to find the requested information below:
      1. The filing date.
      2. Full name of the court where the case was filed.
      3. The name and title of the Judge for this case.
      4. Type of counsel (private, legal services, state protection & advocacy system, ACLU, etc.). Please identify legal service organizations by name
      5. Name any important parties in the case such as plaintiffs and defendants. For individual plaintiffs, only give a general description and no names. For organizations, give names.
      6. The plaintiffs' legal claims: Describe any legal claims including statutes or consitutional claims.
      7. What rememdies were sought? Describe any declaratory relief, injuctive relief, attorney fees or money fees requested in detail as provided.
      8. Any results or events not covered in the list currently.
      9. Highlight any elements of the case that add storytelling value, such as notable conflicts, dramatic events, or significant turning points in the litigation.
      Provide only the extracted entities:
    """
    return prompt

def generate_prompt_combined(chunks):
    prompt = f"""
      SUMMARIES: ```{chunks}```
      You are a law student, skilled at summarizing complaint cases. You are to take the provided summaries and distil them into one final summary, in paragraph format, even if the case is not publically available. Ensure to follow the following guidelines:
      1. Start with a lede sentence to draw in the reader.
      2. Next, describe the facts of case
      3. Mention the important details such as:
          * Filing Date
          * Full name of the court where the case was filed
          * The plaintiffs and defendants, using only general descriptions and no names for individual plaintiffs and names for organizations.
          * The legal counsel for the plaintiffs
          * The plaintiffs legal claims, providing information about any statutes and consitutional claims.
          * The rememdies sought by the plaintifs, providing details and information about the declaratory relief, injuctive relief, attorney fees or money fees requested.
          * Highlight any elements of the case that add storytelling value, such as notable conflicts, dramatic events, or significant turning points in the litigation.
      4. Do not end with any claim of impact this case would have at all. Only stick to the facts of the case.
      5. Provide the summary in past tense
      Only provide the requested summary:
    """
    return prompt

llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.0000000001)

csv_data = []
model_name = "claude-3-haiku-20240307"
llm = ChatAnthropic(model=model_name, temperature=0.0000000001)
for sample in tqdm(range(len(cases))):
  doc = df["Document"].iloc[sample]
  case_name = df["Case Name"].iloc[sample]
  summary = df["Summary"].iloc[sample]
  texts = text_splitter.create_documents([doc])
  chunks = []
  for text in texts:
    chunks.append(llm.invoke(generate_prompt(text)).content)

  combined_chunk_elements = ' \n'.join([f"Chunk {idx+1} out of {len(chunks)}: \n" +  chunk
                                            for idx, chunk
                                            in enumerate(chunks)])

  ai_msg_sum = llm.invoke(generate_prompt_combined(combined_chunk_elements))
  sum_join = " ".join(ai_msg_sum.content.split("\n\n"))
  csv_data.append((case_name, summary, sum_join))
df_save = pd.DataFrame(csv_data, columns=["Case Name", "Ground Truth Summary", "Generated Summary"])
df_save.to_csv(f"generated_results_{model_name}_chunked_{str(uuid.uuid4())}.csv")
