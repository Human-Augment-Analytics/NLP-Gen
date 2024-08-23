import sys
from unstructured.partition.pdf import partition_pdf

from downloader import Downloader

pdf = sys.argv[1]
download_path = sys.argv[2]
file_name = sys.argv[3]

file_pdf = Downloader(pdf).download(download_path, file_name)

text = ""

content = partition_pdf(str(file_pdf))
for entry in content:
    # Possible options: {'ListItem', 'UncategorizedText', 'Title', 'NarrativeText'}
    if entry.category == "NarrativeText":
        text += entry.text

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("nsi319/legal-led-base-16384")  
model = AutoModelForSeq2SeqLM.from_pretrained("nsi319/legal-led-base-16384").to("mps")

padding = "max_length" 

input_tokenized = tokenizer.encode(text, return_tensors='pt', padding=padding, pad_to_max_length=True, truncation=True).to("mps")
summary_ids = model.generate(input_tokenized,
                                  num_beams=4,
                                  no_repeat_ngram_size=3,
                                  length_penalty=2,
                                  min_length=350,
                                  max_length=1000)
summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids][0]
last_sentence = summary.rfind(".")
summary = summary[:last_sentence+1]
print(summary)