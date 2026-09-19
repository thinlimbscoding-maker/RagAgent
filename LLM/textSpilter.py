from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader("data/long_dummy_document copy 9.pdf")
documents = loader.load()
# Create splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Split loaded PDF
chunks = text_splitter.split_documents(documents)

print("Total pages loaded:", len(documents))
print("Total chunks:", len(chunks))

print(f"{chunks} ")
