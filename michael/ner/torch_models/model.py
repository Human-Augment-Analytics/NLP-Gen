from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
import spacy
import string
import sys
sys.path.append('../')
from mistral.mistral_datasets import DocumentClassificationDataset

tokenizer = get_tokenizer("basic_english")

# Load SpaCy's English model
nlp = spacy.load("en_core_web_sm")

def normalize_text(text):
    # Process the text using SpaCy
    doc = nlp(text)

    # Define a list to hold normalized tokens
    normalized_tokens = []

    for token in doc:
        # Convert to lowercase, remove punctuation and stop words, and lemmatize the tokens
        if not token.is_punct and not token.is_stop:
            lemma = token.lemma_.lower()  # Lowercase and lemmatize
            normalized_tokens.append(lemma)

    # Join the tokens back into a normalized string
    normalized_text = ' '.join(normalized_tokens)

    return normalized_text

def yield_token(data_iter):
    for text, lbl in data_iter:
        yield tokenizer(normalize_text(text))

if __name__ == '__main__':
    ds = DocumentClassificationDataset(None, cases_path = '../../all_cases_clearinghouse.pkl')
    vocab = build_vocab_from_iterator(yield_token(ds), specials = ["<unk>"])
    vocab.set_default_index(vocab["<unk>"])

    text_preprocessing_pipeline = lambda x: vocab(tokenizer(normalize_text(x)))
    print(normalize_text(ds[0][0]))
