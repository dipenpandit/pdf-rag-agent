# 🗨️ PDF RAG Agent 
A simple RAG agent that searches through pdf to generate answers.


<img src="./assets/pipeline.jpg" alt="System Workflow" width="1000" />

| Tools         |                                                                                          |
|---------------|----------------------------------------------------------------------------------------------|
| Streamlit     | <img src="https://docs.streamlit.io/logo.svg" alt="Streamlit Logo" width="50"/> |
| Qdrant       | <img src="https://logo.svgcdn.com/l/qdrant.svg" alt="Qdrant Logo" width="80" />               |
| Langchain | <img src="https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/dark/langchain.png" alt="Langchain logo" width="60"/>       |
| SBERT         | <img src="https://sbert.net/_static/logo.png" alt="SBERT Logo" width="80"/>                   |


## Features
- Get answers from your pdf instantly if similar results are found.
- Uses all-MiniLM-L6-v2 model from SBERT to create embeddings.
- Utilizes Qdrant as vector database to store and retrieve embeddings.
- Built using Langchain and Streamlit for easy deployment.


## Run deployed app
Link: https://pdf-rag-agent.streamlit.app/

## Live Demo
Here’s a quick look at how it works:
<!-- ![Demo](assets/demo.gif) -->
<img src="./assets/demo.gif" alt="Demo" width="1000" />

