def settlement_extraction_prompt(document: str) -> str:
    prompt = f"""
      You are a law student tasked with extracting key information from a settlement agreement. Your goal is to identify and summarize specific elements of the agreement. Here is the settlement you will analyze:

      <settlement>
      {document}
      </settlement>

      Please extract the following information from the settlement:

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
    """
    return prompt

def settlement_combined_prompt(extracted_info: str, document: str) -> str:
    prompt = f"""
      You are a law student skilled at distilling sets of extracted information and original into informative summaries. You will be provided with a set of extracted information and a document about a legal settlement. Your task is to create a concise, one-paragraph summary of the settlement.

      Here is the set of extracted information and original document:

      <extracted_info>
      {extracted_info}
      </extracted_info>

      <document>
      {document}
      </document>

      Using the provided information, create a summary of the settlement following these guidelines:

      1. Begin with a sentence describing, in a natural way, when the settlement was entered, including the specific date and the type of settlement that was entered.
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
      Only provide the requested summary.
    """
    return prompt

def complaint_extraction_prompt(document: str) -> str:
    return f"""
      You are a law student, skilled in retrieving case information, who is tasked with extracting key information from the following legal document and summarizing it concisely.
      Identify the following elements:
      1. Entity: Who are the key parties involved in the case (e.g., plaintiffs, defendants)? Include descriptions for individual plaintiffs and names for organizations if relevant.
      2. Date: Identify all significant dates (e.g., filing date, important court events).
      3. Event: Summarize key litigation events in chronological order, including complaints, motions, hearings, and decisions.
      4. Result: Summarize any outcomes, orders, or settlements, including the current status of the case.
      5. Legal Provisions and Legal Basis: Identify the legal provisions cited in the complaints, including relevant statutes, sections, or constitutional basis for the claims.
      6. Remedies Sought: Detail the remedies sought by the plaintiffs, including injunctive relief, damages, etc.
      7. Court Information: Provide the full name of the court where the case was filed.
      8. Judges: Names and titles of the judge(s) assigned to the case.
      9. Storytelling: Highlight any elements of the case that add storytelling value, such as notable conflicts, events, or significant turning points in the litigation.
      Document:
      ```{document}```
    """

def complaint_combined_prompt(content: str, document: str) -> str:
    """Generates a prompt for integrating extracted elements and chunk summaries into a cohesive legal case summary."""
    return f"""
      You are a law student, skilled in summarizing legal cases, who is tasked with creating a cohesive summary of the entire case.
      Using the extracted elements and original document provided, create a cohesive and informative summary of the case. Ensure that the final summary follows these guidelines:
      Write the summary in a human-readable paragraph format.
      Guidelines:
      - Begin with a brief introduction stating what the case is about.
      - Include essential details such as filing date, names of plaintiffs and defendants (including titles and positions where relevant), full name of the court where the case was filed, and names and titles of the judge(s) assigned to the case.
      - Clearly outline the legal claims made by the plaintiffs, specifying relevant statutes and sections cited.
      - Detail the remedies sought by the plaintiffs, including injunctive relief, damages, etc.
      - Present important litigation events chronologically, including motions filed, amendments to the complaint, responses from the defendants, and significant court decisions or orders.
      - Highlight any storytelling elements, including events, conflicts, or notable turning points in the case.
      - Include important dates and present events in a narrative, chronological order.
      - Conclude with the current status of the case as of the most recent date in the document.
      - Use a formal and professional tone suitable for a legal case summary.
      - Write in past tense and avoid personal opinions or unnecessary embellishments.
      - Make the summary understandable to someone without a legal background.
      Elements:
      ```{content}```
      Document:
      ```{document}```
    """