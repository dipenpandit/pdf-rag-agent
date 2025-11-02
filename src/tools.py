from config import SIMILARITY_THRESHOLD
from src.vector_store import get_vector_store
from langchain.tools import tool

# Define tool to retrieve context from internal PDFs
@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """
    Retrieve information to help answer a query from internal PDFs.
    """
    vector_store = get_vector_store()
    retrieved_docs = vector_store.similarity_search_with_relevance_scores(query, k=2)
    
    # Check if similarity is above threshold
    if retrieved_docs and all(score >= SIMILARITY_THRESHOLD for _, score in retrieved_docs):
        serialized = "\n\n".join(
            f"Source: {doc.metadata}\n\nContent: {doc.page_content}" 
            for doc, score in retrieved_docs
        )
        return serialized, retrieved_docs
    
    # If PDF retrieval is not confident, return empty string so agent can decide
    return "", []
                     
