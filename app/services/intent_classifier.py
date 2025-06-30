from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


def classify_intent(user_input: str) -> str:
    prompt = f"""
Classify the following user query into exactly one of the following intents:
- sql → if it asks about orders, invoices, database values, table data, or retrieval.
- kb → if it asks about setup, issues, instructions, configuration, or how-to.
- other → if it does not match any of the above.

Only respond with: sql, kb, or other. No explanation. No extra text.

Query: "{user_input}"
Intent:"""

    response = gemini_model.generate_content(prompt).text.strip().lower()
    cleaned = response.strip("` \n").splitlines()[0]
    return cleaned.replace("intent:", "").strip(" '\"")
