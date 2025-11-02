import os 
import streamlit as st
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from config import MODEL
from src.tools import retrieve_context

load_dotenv()

def get_agent():
    # Define model for the agent
    model = ChatOpenAI( 
        api_key = os.getenv("OPENROUTER_API_KEY"),  # We'll be using Open Router's API KEY
        base_url="https://openrouter.ai/api/v1",     
        model = MODEL,  # select the model you want to use
    )

    # Define tools for the agent
    tools = [retrieve_context]

    # Define system prompt with instructions
    prompt = f"""
    You have access to a tool:
    1. retrieve_context: Retrieves context from internal PDFs.

    Use retrieve_context first, and display the retrieved information without tweaking or summarizing it to the user. 
    If it returns empty then just notify that you could not find relevant information in the documents.
    """

    # Create an agent with the model, tools, and prompt
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt,
    )
    return agent

# Return response from agent
def get_response(agent, query, delay=0.02):
    placeholder = st.empty()  # Container for streaming text
    full_message = ""

    for event in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
    ):
        message = event["messages"][-1].content
        if message:
            # Append new content to the full message
            full_message = message
            # Update the placeholder with Markdown
            placeholder.markdown(full_message)