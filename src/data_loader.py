from langchain_community.document_loaders import PDFPlumberLoader    # to load PDF documents 
from langchain_core.documents import Document                        # to make langchain documents  
from langchain_text_splitters import RecursiveCharacterTextSplitter  # for text splitting
from config import CHUNK_SIZE, CHUNK_OVERLAP

# Create Langchain Document by loading pdf
def load_doc(pdf_path):
    loader = PDFPlumberLoader(pdf_path)
    docs = loader.load()
    return docs 

# Let's split the documents into smaller chunks for better processing
def split_text(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,                            # size of each chunk in characters
        chunk_overlap=CHUNK_OVERLAP,                          # i.e. 20% overlap
        separators=["\n\n", "\n", " ", ""]          # separators to split on
    )
    all_splits = text_splitter.split_documents(docs)
    return all_splits

