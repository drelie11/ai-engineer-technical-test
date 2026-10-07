import os
import sqlite3
import json
from datetime import datetime, date
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()
DB_PATH = "receipts.db"

DB_SCHEMA = """
Tables in the SQLite Database:

1. receipts
   - id (INTEGER, PRIMARY KEY)
   - date (DATE, format YYYY-MM-DD)
   - merchant_name (TEXT)
   - total_amount (INTEGER, in IDR Rupiah)

2. receipt_items
   - id (INTEGER, PRIMARY KEY)
   - receipt_id (INTEGER, FOREIGN KEY -> receipts.id)
   - item_name (TEXT)
   - price (INTEGER, in IDR Rupiah)
   - quantity (INTEGER)
"""

def get_sql_query(user_question: str) -> str:
    today_str = date.today().strftime('%Y-%m-%d')
    
    prompt = f"""
    You are an expert SQLite developer. Convert the following natural language question into a valid SQL query.
    
    Database Schema:
    {DB_SCHEMA}
    
    Context:
    - Today's date is: {today_str}
    - Use lower() or LIKE for text matching (e.g. LOWER(item_name) LIKE '%hamburger%').
    - Only return valid SQLite 'SELECT' queries. Never return DELETE, UPDATE, or INSERT statements.
    - Return ONLY the executable SQL query inside raw text or a SQL code block without extra explanations.
    
    User Question: "{user_question}"
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite', 
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.0)
        )
    except Exception as e:
        return f"API_ERROR: {str(e)}"
        
    sql = response.text.strip()
    if sql.startswith("```sql"):
        sql = sql[6:]
    if sql.startswith("```"):
        sql = sql[3:]
    if sql.endswith("```"):
        sql = sql[:-3]
        
    return sql.strip()

def run_sql_query(sql_query: str):
    """Executes the generated SQL query against receipts.db safely."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        conn.close()
        return columns, rows
    except Exception as e:
        conn.close()
        return None, f"SQL Execution Error: {e}"

def answer_user_query(user_question: str) -> str:
    sql = get_sql_query(user_question)
    if sql.startswith("API_ERROR"):
        return f"Google AI is currently too busy to process this request. Please try again in a few moments."
        
    print(f"\n[Generated SQL]: {sql}")
    
    columns, results = run_sql_query(sql)
    print(f"[Raw DB Results]: {results}")
    
    if isinstance(results, str) and "Error" in results:
        return f"Sorry, I had trouble querying the database: {results}"
    
    prompt = f"""
    You are a helpful financial assistant for food receipt tracking.
    
    User Question: "{user_question}"
    Generated SQL: {sql}
    SQL Execution Columns: {columns}
    SQL Execution Rows: {results}
    
    Instructions:
    - Synthesize the database results into a clear, direct answer for the user.
    - If prices/amounts are present, format them clearly in Indonesian Rupiah (e.g., Rp 45.000).
    - If no rows were returned, politely inform the user that no matching records were found for that period or query.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite', 
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.0)
        )
    except Exception as e:
        return f"API_ERROR: {str(e)}"
    
    return response.text

if __name__ == "__main__":
    test_questions = [
        "What food did i buy recently?",
        "Give me total expenses for food on 13 September 2026?",
        "Where did i buy Matcha from most recently?"
    ]
    
    for q in test_questions:
        print("="*60)
        print(f"User Asked: {q}")
        ans = answer_user_query(q)
        print(f"Assistant Answer:\n{ans}")