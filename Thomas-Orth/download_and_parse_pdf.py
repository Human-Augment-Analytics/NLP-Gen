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

print(text)