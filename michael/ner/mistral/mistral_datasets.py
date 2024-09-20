import torch
import numpy as np
from torch.utils.data import Dataset
from tqdm import tqdm
from datasets import load_dataset, Dataset as HFDataset
import re
from transformers import AutoTokenizer
import string
from langdetect import detect
import random
from transformers import DataCollatorForLanguageModeling
import sys
sys.path.append('../../')
from summarizers.get_complaints import get_complaint_only_cases
from summarizers.ocr import read_doc, extract_text_from_pdf

def normalize(comment, lowercase, remove_stopwords):
    if lowercase:
        comment = comment.lower()
    comment = nlp(comment)
    lemmatized = list()
    for word in comment:
        lemma = word.lemma_.strip()
        if lemma:
            if not remove_stopwords or (remove_stopwords and lemma not in stops):
                lemmatized.append(lemma)
    return " ".join(lemmatized)

ISSUE_IDS = {
    'Child Welfare': 0,
    'Criminal Justice (Other)': 1,
    'Disability Rights': 2,
    'Education': 3,
    'Election/Voting Rights': 4,
    'Environmental Justice': 5,
    'Equal Employment': 6,
    'Fair Housing/Lending/Insurance': 7,
    'Immigration and/or the Border': 8,
    'Indigent Defense': 9,
    'Intellectual Disability (Facility)': 10,
    'Jail Conditions': 11,
    'Juvenile Institution': 12,
    'Labor Rights': 13,
    'Mental Health (Facility)': 14,
    'National Security': 15,
    'Nursing Home Conditions': 16,
    'Policing': 17,
    'Presidential/Gubernatorial Authority': 18,
    'Prison Conditions': 19,
    'Public Accommodations/Contracting': 20,
    'Public Benefits/Government Services': 21,
    'Public Housing': 22,
    'Reproductive Issues': 23,
    'School Desegregation': 24,
    'Speech and Religious Freedom': 25
}

class DocumentClassificationDataset(Dataset):
    def __init__(self, tokenizer, cases_path):
        self.dataset = {'text': [], 'labels': []}
        print('Retrieving complaints')
        cases = get_complaint_only_cases(cases_path)
        print('Iterate over complaints')
        self.text_len = 512
        for entry in tqdm(cases):
            summary = entry.summary
            if not summary or len(summary) < 1 or not entry or not entry.case_documents or len(entry.case_documents) < 1:
                continue
            doc = entry.case_documents[0]
            document_text = read_doc(doc)
            print(entry.case_types)
            self.dataset['text'].append(document_text)
            self.dataset['labels'].append(ISSUE_IDS[entry.case_types[0]])

        self.dataset = HFDataset.from_dict(self.dataset)
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.dataset)
    
    def __getitem__(self, idx):
        """
        Args:
            idx (int): Index of the sample to retrieve.

        Returns:
            tuple: (data_sample, label) where data_sample is the data at index idx,
                    and label is the corresponding label.
        """
        data_sample = self.dataset[idx]['text']
        while data_sample.isspace() or detect(data_sample) != 'en':
            idx += 1
            data_sample = self.dataset[idx%len(self.dataset)]['text']
        return data_sample, self.dataset[idx%len(self.dataset)]['labels']

    
    #Use this in the event of using a DataCollator
    def prepare_corpus(self):

        def tokenize(sample):
            return self.tokenizer(sample['text'])

        tokenized_input = self.dataset.map(tokenize, batched = True, num_proc = 4, remove_columns = ['text', 'labels'])

        def crop(sample):
            print(len(sample['input_ids']))
            return {'input_ids': sample['input_ids'][:4096], 'attention_mask': sample['attention_mask'][:4096]}

        tokenized_input = tokenized_input.map(crop, batched = True, num_proc = 4)
        print(tokenized_input)
        
        return tokenized_input



class MistralMLMDataset(Dataset):
    def __init__(self, tokenizer, split = 'train', text_len = 24):
        """
        Args:
            split (list or ndarray): "train" or "validation".
        """
        self.dataset = load_dataset("pile-of-law/pile-of-law", "nlrb_decisions")
        self.dataset = self.dataset[split]
        print(self.dataset)
        self.text_len = text_len
        self.tokenizer = tokenizer

    def __len__(self):
        """Returns the number of samples in the dataset."""
        return len(self.dataset)

    def __getitem__(self, idx):
        """
        Args:
            idx (int): Index of the sample to retrieve.

        Returns:
            tuple: (data_sample, label) where data_sample is the data at index idx,
                    and label is the corresponding label.
        """
        data_sample = self.dataset[idx]['text']
        lang = ''
        while data_sample.isspace() or lang != 'en':
            try:
                lang = detect(data_sample)
                idx += 1
                data_sample = self.dataset[idx%len(self.dataset)]['text']
            except:
                lang = ''
        #tokens = self.tokenizer(data_sample, return_tensors='pt')
        #text_index = random.randrange(0, len(data_sample) - self.text_len + 1)
        #data_sample = data_sample[text_index: text_index + self.text_len]
        return data_sample
    
    #Use this in the event of using a DataCollator
    def prepare_corpus(self):
        #concatenated_sequences = []
        #concatenated_masks = []
        #for data_sample in self.dataset:
        #    data_sample = data_sample['text']
        #    tokenized = self.tokenizer(data_sample)
        #    concatenated_samples.extend(tokenized['input_ids'])
        #    concatenated_masks.extend(tokenized['attention_masks'])

        def tokenize(sample):
            return self.tokenizer(sample['text'])

        tokenized_input = self.dataset.map(tokenize, batched = True, num_proc = 4, remove_columns = ['text', 'created_timestamp', 'downloaded_timestamp', 'url'])
        print(tokenized_input)
        def group_texts(samples):
            
            examples = {k: sum(samples[k], []) for k in samples.keys()}
            total_length = len(examples[list(examples.keys())[0]])

            if total_length >= self.text_len:
                total_length = (total_length // self.text_len) * self.text_len

            return {
                    k : [t[ i: i + self.text_len] for i in range(0, total_length, self.text_len)] for k, t in examples.items()
                   }

        mlm_dataset = tokenized_input.map(group_texts, batched = True, num_proc = 4)
        
        return mlm_dataset

# Example usage:
if __name__ == "__main__":
    import numpy as np
    
    # Create dataset
    #train_dataset = MistralMLMDataset(AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased"))
    train_dataset = DocumentClassificationDataset(AutoTokenizer.from_pretrained("allenai/longformer-base-4096"), cases_path = '../../all_cases_clearinghouse.pkl')
    #val_dataset = DocumentClassificationDataset(AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased"), cases_path = '../../all_cases_clearinghouse.pkl')
   
    #data_collator = DataCollatorForLanguageModeling(tokenizer = train_dataset.tokenizer, mlm_probability = 0.1)
    # DataLoader for batching and shuffling
    mlm_train = train_dataset.prepare_corpus()
    #mlm_val = val_dataset.prepare_corpus()

    #dataloader = torch.utils.data.DataLoader(mlm_train, batch_size=2, shuffle=False)
    # Iterate through the DataLoader
    #for batch_data in dataloader:
    #    #print(batch_data)
    #    quit()

