from langchain_community.document_loaders import PyPDFLoader

pdfData = PyPDFLoader("fillable-form.pdf")
readPdf = pdfData.load()
print("READ", readPdf, readPdf[0])
