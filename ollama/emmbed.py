# 1. Use the new modern partner library import path
from langchain_ollama import OllamaEmbeddings

# 2. Change the model to the dedicated embedding model you pulled
embeddings = OllamaEmbeddings(model="nomic-embed-text")

myDoc = [
    "india gets freedom in 1947",
    "india has more than 30 states",
    "india  has poor roads",
    "india good  developers",
]

# 3. Generate the vector
print("🔄 Generating embedding via nomic-embed-text...")
query_vector = embeddings.embed_documents(myDoc)

print("🎉 LangChain Ollama embedding generated successfully!")
print(f"📏 Vector Dimensions: {len(query_vector[0])}")
print(f"🔢 First {query_vector}")
