from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from config import COLLECTION_NAME
from dotenv import load_dotenv
import os
from src.embeddings import get_embeddings
from src.data_loader import load_doc, split_text
     
load_dotenv()

# Create a global cache for embeddings to avoid redundant initializations
_embeddings_cache = None
def get_cached_embeddings():
    global _embeddings_cache            # tell python to use the global _embeddings_cache variable defined outside this function
    if _embeddings_cache is None:       # if the embeddings cache is empty, fetch embeddings
        _embeddings_cache = get_embeddings()
    return _embeddings_cache

# Create Qdrant Cient
def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL"), 
        api_key=os.getenv("QDRANT_API_KEY")
    )

# Create collection if it doesn't exist
def create_collection(client=None, embeddings=None):
    client = client or get_qdrant_client()
    embeddings = embeddings or get_cached_embeddings()
    try:
        client.get_collection(COLLECTION_NAME)
    except Exception:
        vector_size = len(embeddings.embed_query("sample text"))
        client.create_collection(
            collection_name = COLLECTION_NAME,
            vectors_config = VectorParams(size=vector_size, distance=Distance.COSINE)
            )

# Create a global cache for vector store to prevent wiping indexing every time
_vector_store = None

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        client = get_qdrant_client()

        # Ensure collection exists
        create_collection(client)

        # Wrap Langchain's Qdrant Vector Store      
        _vector_store = QdrantVectorStore(
            client=client,
            collection_name = COLLECTION_NAME,
            embedding = get_cached_embeddings()
        )
    return _vector_store

# Reset Collection
def reset_collection():
    client = get_qdrant_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass
    
    embeddings = get_cached_embeddings()
    vector_size = len(embeddings.embed_query("sample text"))

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )

    # Reset cached vector store
    global _vector_store
    _vector_store = None

# Initialize Qdrant Vector Store in LangChain
def store_splits(all_splits):
    vector_store = get_vector_store()
    document_ids = vector_store.add_documents(all_splits)
    print(document_ids[:3])

# Combine all the data ingestion steps in one pipeline       
def data_ingestion(pdf_path):
    docs = load_doc(pdf_path)       # Create documents
    all_splits = split_text(docs)   # Split documents (chunking)
    store_splits(all_splits)        # Store embeddings in vector store

