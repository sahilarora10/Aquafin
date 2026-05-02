import sqlite3
import json

DB_PATH = "financebot.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            chat_id INTEGER PRIMARY KEY,
            history TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def load_history(chat_id: int) -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT history FROM conversations WHERE chat_id = ?", (chat_id,))
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else []

def save_history(chat_id: int, history: list):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO conversations (chat_id, history) VALUES (?, ?)
        ON CONFLICT(chat_id) DO UPDATE SET history=excluded.history,
        updated_at=CURRENT_TIMESTAMP
    """, (chat_id, json.dumps(history)))
    conn.commit()
    conn.close()

def delete_history(chat_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM conversations WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()
