import sys
sys.path.append('..')
from get_complaints import get_complaint_only_cases
from ocr import read_doc
import random
import spacy
import re
from nltk.tokenize import sent_tokenize
import nltk
#nltk.download("punkt_tab")

def basic_extract(document):
    document = re.sub(r'\[\*.*\]', '', document)
    #paragraphs = re.split(r'\^[0-9]*\.', document)
    paragraphs = re.split(r'\n', document)
    #re.match(r'\^[0-9]*\.', paragraph) and
    #lines = re.split(r'^[0-9]*\.', '\n'.join([paragraph for paragraph in paragraphs if len(paragraph) > 40]))
    lines = [paragraph for paragraph in paragraphs if len(paragraph) > 40]
    print(lines)
    idxs = []
    for i, line in enumerate(lines):
        matches = bool(re.match(r'^[0-9]*\.', line)) #128. Some other text -> matches = True
        if matches:
            idxs.append(i)
        #print('-' * 50)
        #print(f'{line}', matches)
    bullets = []
    for i, idx in enumerate(idxs[:-1]):
        bullets.append(''.join(lines[idxs[i]:idxs[i+1]])[2:])
    #return '\n'.join([line for line in lines if bool(re.match(r'\^[0-9]*\.', line))])
    return bullets
    #first_complaint = []
    #for i, line in enumerate(lines):
    #    if line[:2] == '1.':
    #        first_complaint = lines[i:]
    #return first_complaint

def lead3(text):
    #print('Source Text: ')
    #print(text)
    text = basic_extract(text)
    print('Basic Cleaned Text: ')
    print(text)
    #for sent in sent_tokenize(text):
    #    print('-' * 50)
    #    print(sent)
    return ''.join(text[:10])

"""def lead3(text):
    # Load a pre-trained spaCy language model
    nlp = spacy.load("en_core_web_sm")  # Small English model

    # Process a text
    doc = nlp(text)

    # Print each sentence
    for sent in doc.sents:
        print('-'  * 50)
        print(sent.text)
"""

if __name__ == '__main__':
    complaints = get_complaint_only_cases('../../all_cases_clearinghouse.pkl')
    case = random.choice(complaints)
    print(case.id)
    print(case.available_documents)
    summary = lead3(read_doc(case.case_documents[0])) 
    print('SUMMARY')
    print('-' * 50)
    print(summary)
