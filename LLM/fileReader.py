from langchain_community.document_loaders import TextLoader

loader = TextLoader("story.txt")
print("asasasas", loader)
docs = loader.load()
print("docsdocsdocs", docs[0].page_content)
