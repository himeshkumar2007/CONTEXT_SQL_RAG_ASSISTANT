import mysql.connector
from logger import log_error
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


def generate_sql_prompt(user_input: str) -> str:
    return f"""
You are an expert SQL query generator for a MySQL database named `demo1`. Convert user requests into valid SELECT queries using only the schema below.

### SCHEMA:

- order_master(order_no, order_date, entity_code, status)
- order_details(sku_id, qty, unit_price, entity_code, cost_price, status)
- invoice_master(invoice_no, invoice_date, entity_code, status)
- invoice_details(sku_id, qty, unit_price, entity_code)
- entity_master(entity_code, entity_name, contact_no, email_id, billing_address1, billing_address2, billing_city, billing_state, billing_country, billing_pincode,mailing_address1,mailing_address2,mailing_city,mailing_country,mailing_state)
- service_detail(entity_code, subscription_id, subscription_start_date, subscription_end_date, sku_id, selling_price,  billing_frequency, subscriptional_auto_renewal,service_name)
- user_info(entity_code, email_id, name)

### RULES:

1. Generate only valid SELECT queries.
2. Never generate INSERT, UPDATE, DELETE, or any explanation.
3. Always filter using `entity_code` (assume it is an integer).
4. Match values like order numbers, invoice numbers, and email using appropriate columns:
   - invoice_no → invoice_master.invoice_no
   - order_no → order_master.order_no
   - email → user_info.email_id
5. Use JOINs only when necessary.
6. Use readable column aliases and formatting.
7. Return only the SQL query. No pre-text or explanation.

### EXAMPLES :

Q: Show invoice and entity details for invoice INV/2023/100  
SQL:
SELECT
    im.invoice_no,
    im.invoice_date,
    im.status AS invoice_status,
    em.entity_name,
    em.billing_city
FROM invoice_master im
JOIN entity_master em ON im.entity_code = em.entity_code
WHERE im.invoice_no = 'INV/2023/100';

Q: Get all subscription details for entity 2005  
SQL:
SELECT
    sd.subscription_id,
    sd.subscription_start_date,
    sd.subscription_end_date,
    sd.selling_price,
    em.entity_name
FROM service_detail sd
JOIN entity_master em ON sd.entity_code = em.entity_code
WHERE em.entity_code = 2005;

Q: {user_input}  
SQL:
"""


def clean_generated_sql(raw_sql: str) -> str:
    cleaned_sql = raw_sql.strip()
    if cleaned_sql.startswith("```sql"):
        cleaned_sql = cleaned_sql[6:]
    if cleaned_sql.endswith("```"):
        cleaned_sql = cleaned_sql[:-3]
    return cleaned_sql.strip()


def generate_sql(user_input: str) -> str:
    prompt = generate_sql_prompt(user_input)
    raw_sql = gemini_model.generate_content(prompt).text
    return clean_generated_sql(raw_sql)


def execute_sql(sql: str):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return data, columns
    except Exception as e:
        log_error(f"SQL Execution Error: {e}")
        return None, [str(e)]



def handle_sql_query(user_input: str, db_config: dict):
    try:
        sql = generate_sql(user_input)
        data, columns = execute_sql(sql)
        return {
            "sql": sql,
            "data": data,
            "columns": columns
        }
    except Exception as e:
        log_error(f"Handle SQL Query Error: {e}")
        return {
            "error": str(e)
        }
