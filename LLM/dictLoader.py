# Install the community package if you haven't already:
# pip install langchain-community pypdf
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(path="data", glob="*.pdf", loader_cls=PyPDFLoader)
# it load as data comes
for doc in loader.lazy_load():
    print(doc.page_content)

for doc in loader.load():
    print(doc.page_content)
