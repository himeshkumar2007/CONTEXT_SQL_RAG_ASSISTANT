import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper import scrape_and_save
from updater import update_pinecone_with_new_content

KB_URL = "https://disti05.xtributor.com/knowledge/knowledgebase.html"

def run_full_pipeline():
    print("🚀 Starting KB update pipeline...")

    changed = scrape_and_save(KB_URL)
    if changed:
        update_pinecone_with_new_content()
    else:
        print("No update needed for Pinecone vector store.")

if __name__ == "__main__":
    run_full_pipeline()
