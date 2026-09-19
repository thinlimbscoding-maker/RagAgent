from langchain_community.document_loaders import WebBaseLoader

web_url = "https://www.sequoia.com/"
web_loader = WebBaseLoader(web_url)
web_docs = web_loader.load()
print(f"Total documents loaded from web: {len(web_docs)}")
