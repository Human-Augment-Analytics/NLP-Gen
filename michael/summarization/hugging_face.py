from datasets import load_dataset
import re
# please install HuggingFace datasets by pip install datasets 

multi_lexsum = load_dataset("allenai/multi_lexsum", name="v20220616")
# Download multi_lexsum locally and load it as a Dataset object 

example = multi_lexsum["validation"][67] # The first instance of the dev set 
print('Source Document Text:')
print(len(example["sources"])) # A list of source document text for the case
for document in example["sources"]:
    print('-' * 50)
    document = re.sub(r'\[\*.*\]', '', document)
    #document = re.sub(r'Page.*\n', '', document)
    paragraphs = re.split(r'\n', document)
    #print(paragraphs)
    #print(len(paragraphs))
    print(''.join([paragraph for paragraph in paragraphs if len(paragraph) > 80]))
for sum_len in ["long", "short", "tiny"]:
    print(example["summary/" + sum_len]) # Summaries of three lengths
