from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Initialize our local embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 2. Your raw document list
myDoc = [
    "india gets freedom in 1947",
    "india has more than 30 states",
    "india has poor roads",
    "india good developers",
]

print("🔄 Generating embeddings and creating local vector DB...")
# 3. Create the FAISS database directly from your text documents and embedding engine
# This automatically handles both embedding and indexing under the hood!
db = FAISS.from_texts(myDoc, embeddings)
print("🎉 Vector DB created successfully!")
print("showwww", db)
# 4. Define your search query
user_query = "what happend in 19 47"
print(f"\n🔍 Hitting Query: '{user_query}'")

# 5. Search the database for the top 2 closest semantic matches
# k=2 specifies that you want the top 2 closest results
results = db.similarity_search(user_query, k=1)

# 6. Print out the search matches
print("\n🎯 Search Results:")
print(results)


for i, doc in enumerate(results):
    print(f"Match {i+1}: {doc.page_content}")
