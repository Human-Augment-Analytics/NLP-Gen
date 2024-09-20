from langchain_community.llms import Ollama
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader

print('Load Ollama')
llm = Ollama(model="llama3:8b")
print('Loaded Ollama')
print('Invoke Ollama')
loader = PyPDFLoader("/home/michael/GeorgiaTech/Law_Data_Design/api/pdfs/10874_0.pdf")
documents = loader.load()
chain = load_qa_chain(llm = llm, chain_type = "map_reduce")
query = "Who is the plaintiff?"
print(chain.run(input_documents = documents, question = query))
query = "Who is the defendant?"
print(chain.run(input_documents = documents, question = query))
query = "What is the core issue in the complaint?"
print(chain.run(input_documents = documents, question = query))
print('Invoked Ollama')
