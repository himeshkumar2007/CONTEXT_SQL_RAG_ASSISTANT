import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
pinecone = Pinecone(api_key=PINECONE_API_KEY)
vectorstore = PineconeVectorStore(index_name="vector-transform", embedding=embeddings)


def interactive_response(query: str, intent: str, context: str = "") -> str:
    prompt = f"""
You are a support assistant who only helps with database (SQL) queries or documentation (KB), answer in details from kb. Do not answer anything outside of these.
If query is not related to db or kb, say: "I'm trained only to assist with database and knowledge base queries."
If the query is vague, ask a relevant follow-up.

Query: "{query}"
Intent: {intent}

{f"Context:\n{context}" if context else ""}

Respond:
"""
    return gemini_model.generate_content(prompt).text.strip()


def ask_knowledgebase(query: str) -> str:
    docs = vectorstore.similarity_search(query, k=4)
    context = "\n\n".join([doc.page_content for doc in docs])
    return interactive_response(query, "kb", context)

def handle_kb_query(query: str) -> str:
    return ask_knowledgebase(query)
