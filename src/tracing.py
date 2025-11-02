# Initialize Langsmith tracing
from dotenv import load_dotenv
import os


def setup_langsmith():
    # Load environment variables from .env file
    load_dotenv()

    os.environ["LANGSMITH_TRACING"] = "true"
    try:
        os.getenv("LANGSMITH_ENDPOINT")
        os.getenv("LANGSMITH_TRACING")
    except Exception as e:
        print("Error loading LANGSMITH_TRACING:", e)
