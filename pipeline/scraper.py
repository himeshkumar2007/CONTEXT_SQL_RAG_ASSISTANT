import os
import hashlib
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_and_save(url: str, hash_file: str = "content_hash.txt", 
                    json_file: str = "data/kb_data.json", html_file: str = "data/document/kb.html") -> bool:
    """
    Scrapes the URL content, checks for changes, saves JSON and HTML if changed.
    Returns True if content updated, False if no changes.
    """

    # Setup Selenium WebDriver options
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p,li"))
        )
    except Exception as e:
        print(f"Timeout waiting for page content: {e}")
        driver.quit()
        return False

    html_content = driver.page_source
    driver.quit()

    # Compute hash
    new_hash = hashlib.sha256(html_content.encode("utf-8")).hexdigest()

    old_hash = ""
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            old_hash = f.read()

    if new_hash == old_hash:
        print("✅ No changes in content detected.")
        return False

    print("🔄 Content changed. Extracting and saving...")

    # Save new hash
    with open(hash_file, "w") as f:
        f.write(new_hash)

    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    kb_data = []
    for element in soup.find_all(['p', 'li']):
        text = element.get_text(strip=True)
        if text:
            kb_data.append({"type": "text", "content": text})

    # Ensure directories exist
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    os.makedirs(os.path.dirname(html_file), exist_ok=True)

    # Save JSON data
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(kb_data, f, ensure_ascii=False, indent=4)

    # Create simple HTML from text only
    html_parts = ["<html><body>"]
    for item in kb_data:
        if item["type"] == "text":
            html_parts.append(f"<p>{item['content']}</p>")
    html_parts.append("</body></html>")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

    print(f"✅ Saved updated KB data to {json_file} and {html_file}")

    return True
