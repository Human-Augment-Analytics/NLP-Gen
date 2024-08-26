import matplotlib.pyplot as plt
from transformers import pipeline

# Define already implemented model
model_name = "facebook/bart-large-cnn"
summarizer = pipeline("summarization", model=model_name)

# Sample texts for summarization
# Sources for texts:
# 1. https://en.wikipedia.org/wiki/Natural_language_processing
# 2. https://arxiv.org/pdf/1801.10198
# 3. https://en.wikipedia.org/wiki/Portrait_of_Ambroise_Vollard_(C%C3%A9zanne)
# 4. https://en.wikipedia.org/wiki/Dominican_Republic
# 5. https://en.wikipedia.org/wiki/Artificial_intelligence

texts = [
    """
    Natural language processing (NLP) is an interdisciplinary subfield of computer science and artificial intelligence. It is primarily concerned with providing computers with the ability to process data encoded in natural language and is thus closely related to information retrieval, knowledge representation and computational linguistics, a subfield of linguistics. Typically data is collected in text corpora, using either rule-based, statistical or neural-based approaches in machine learning and deep learning.
    """,
    """
    We show that generating English Wikipedia articles can be approached as a multi-document summarization of source documents. 
    We use extractive summarization to coarsely identify salient information and a neural abstractive model to generate 
    the article. For the abstractive model, we introduce a decoder-only architecture that can scalably attend to very long sequences, 
    much longer than typical encoder-decoder architectures used in sequence transduction. We show that this model can 
    generate fluent, coherent multi-sentence paragraphs and even whole Wikipedia articles. When given reference documents, 
    we show it can extract relevant factual information as reflected in perplexity, ROUGE scores, and human evaluations.
    """,
    """
    Portrait of Ambroise Vollard is an 1899 oil-on-canvas portrait by Paul Cézanne of his art dealer Ambroise Vollard. It was bequeathed by Vollard on his death to the Petit Palais in Paris, where it is still housed today. Like many of his portraits, the Portrait of Ambroise Vollard displays the significant role of the subject in Cézanne's life, and specifically, the artist's gratitude for promoting his work and establishing his reputation as an artist.
    """,
    """
    The Dominican Republic[a] is a North American country on the island of Hispaniola in the Greater Antilles archipelago of the Caribbean Sea, bordered by the Atlantic Ocean to the north. It occupies the eastern five-eighths of the island, which it shares with Haiti,[15][16] making Hispaniola one of only two Caribbean islands, along with Saint Martin, that is shared by two sovereign states. It is the second-largest nation in the Antilles by area (after Cuba) at 48,671 square kilometers (18,792 sq mi), and second-largest by population, with approximately 11.4 million people in 2024, of whom approximately 3.6 million live in the metropolitan area of Santo Domingo, the capital city.
    """,
    """
Artificial intelligence (AI), in its broadest sense, is intelligence exhibited by machines, particularly computer systems. It is a field of research in computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximize their chances of achieving defined goals.[1] Such machines may be called AIs.
    """
]

summaries = [summarizer(text, max_length=50, min_length=25, do_sample=False)[0]['summary_text'] for text in texts]

# Calculate lengths of original vs summaries texts
original_lengths = [len(text.split()) for text in texts]
summary_lengths = [len(summary.split()) for summary in summaries]

for i in range(len(texts)):
    print(f"Original text {i+1}:", texts[i])
    print(f"Summarized text {i+1}:", summaries[i])
    print()


# Visualize the length of the original text vs the summaries
labels = ['Text 1', 'Text 2', 'Text 3', 'Text 4', 'Text 5']
x = range(len(labels))

plt.figure(figsize=(10, 6))
plt.bar(x, original_lengths, width=0.4, label='Original Text', align='center')
plt.bar(x, summary_lengths, width=0.4, label='Summary', align='edge')

plt.xticks(x, labels)
plt.ylabel('Word Count')
plt.title('Original Text vs Summary Length')
plt.legend()
plt.show()
