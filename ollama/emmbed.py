# 1. Use the new modern partner library import path
from langchain_ollama import OllamaEmbeddings

# 2. Change the model to the dedicated embedding model you pulled
embeddings = OllamaEmbeddings(model="nomic-embed-text")

text_string = "Why is my API not calling?"

# 3. Generate the vector
print("🔄 Generating embedding via nomic-embed-text...")
query_vector = embeddings.embed_query(text_string)

print("🎉 LangChain Ollama embedding generated successfully!")
print(f"📏 Vector Dimensions: {len(query_vector)}")
print(f"🔢 First 5 numbers: {query_vector[:5]}")
