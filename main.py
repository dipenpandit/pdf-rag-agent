import streamlit as st
import os
from src.vector_store import get_vector_store, data_ingestion, reset_collection
from src.agent import get_agent, get_response

st.set_page_config(page_title="RAG Chatbot")

# Sidebar
st.sidebar.title("⚙️ Settings")

# File uploader
uploaded_files = st.sidebar.file_uploader("Upload PDF Documents", type=["pdf"], accept_multiple_files=True)

# Button to process docs
process_docs = st.sidebar.button("Process Documents")

# Session flags
if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Process Uploaded PDFs
if process_docs:
    if not uploaded_files:
        st.sidebar.error("Upload PDF(s) first!")
    else:
        with st.spinner("Processing documents..."):
            # CLEAR previous vectors 
            reset_collection()
            
            for f in uploaded_files:
                temp_path = f"temp_{f.name}"              # create a temp file path
                with open(temp_path, "wb") as temp_file:  # write the uploaded file to temp path
                    temp_file.write(f.getbuffer())        # f.getbuffer() get the view not the copy to save memory

                data_ingestion(temp_path)

            st.session_state.vectorstore = get_vector_store()
            st.session_state.pdf_loaded = True
            st.success("Docs processed!")

# Chat Section 
st.title("💬 RAG Chat Assistant")

# Check if pdf is uploaded
if not st.session_state.pdf_loaded:
    st.warning("📄 Upload and process PDFs to start chatting.")
else:
    clear_docs = st.sidebar.button("🧹 Clear PDF & Reset VectorDB")

    if clear_docs:        
        reset_collection()
        st.session_state.pdf_loaded = False
        st.success("Cleared PDF and Vector DB!")

    query = st.text_input("Ask something about your documents:")

    # Get agent
    agent = get_agent()

    # Get Response from the agent
    if st.button("🔍Search"):
        if not query.strip():
            st.warning("❓ Please enter a question")
        else:
            with st.spinner("Thinking..."):
                get_response(agent, query)


    