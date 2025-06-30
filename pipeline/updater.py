import os
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from app.config import PINECONE_API_KEY, PINECONE_INDEX_NAME

def update_pinecone_with_new_content(html_file: str = "data/document/kb.html"):
    """
    Loads the cleaned HTML knowledge base, splits into chunks, 
    and uploads to Pinecone vectorstore.
    """
    print(f"📦 Loading KB from {html_file}...")

    loader = UnstructuredHTMLLoader(html_file)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
    documents = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv("GEMINI_API_KEY"))
    pinecone = Pinecone(api_key=PINECONE_API_KEY)
    vectorstore = PineconeVectorStore(index_name=PINECONE_INDEX_NAME, embedding=embeddings)

    print(f"📤 Uploading {len(documents)} chunks to Pinecone index '{PINECONE_INDEX_NAME}'...")
    vectorstore.add_documents(documents)
    print("✅ Upload completed.")
