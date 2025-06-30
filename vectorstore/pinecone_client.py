import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", None)  # optional, if needed
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "vector-transform")

# Initialize Pinecone client
pinecone_client = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

# Initialize embeddings model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Initialize Pinecone VectorStore (you can reuse this instance)
vectorstore = PineconeVectorStore(index_name=PINECONE_INDEX_NAME, embedding=embeddings)

def get_vectorstore() -> PineconeVectorStore:
    """
    Returns the initialized PineconeVectorStore instance.
    """
    return vectorstore
