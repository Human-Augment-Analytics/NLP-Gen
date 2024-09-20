from transformers import pipeline
import sys
sys.path.append('..')
from get_complaints import get_complaint_only_cases
from ocr import read_doc
import random
import spacy
import pytextrank
from lead3 import lead3 

def pegasus(text):
    text = lead3(text)
    #nlp = spacy.load('en_core_web_sm')
    #nlp.add_pipe("textrank")

    #doc = nlp(text)

    #for phrase in doc._.phrases:
    #    print('Text:   ', phrase.text)
    #    print('Rank:   ', phrase.rank, phrase.count)
    #    print('Chunks: ', phrase.chunks)
    # Create a summarization pipeline
    summarizer = pipeline("summarization", model = "nsi319/legal-pegasus")

    # Perform summarization
    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)

    # Print the summary
    return summary[0]['summary_text']

if __name__ == '__main__':
    complaints = get_complaint_only_cases('../../all_cases_clearinghouse.pkl')
    case = complaints[3]#random.choice(complaints)
    print(case.id)
    text = read_doc(case.case_documents[0])
    print(text)
    print('-' * 50)
    print(pegasus(text))
