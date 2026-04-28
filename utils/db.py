import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "agmarknet_cache.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Prices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            crop TEXT,
            state TEXT,
            market TEXT,
            min_price REAL,
            max_price REAL,
            modal_price REAL
        )
    ''')
    
    # Alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop TEXT,
            market TEXT,
            target_price REAL,
            condition TEXT,
            email TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def save_alert(crop, market, target_price, condition, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alerts (crop, market, target_price, condition, email)
        VALUES (?, ?, ?, ?, ?)
    ''', (crop, market, target_price, condition, email))
    conn.commit()
    conn.close()

def get_active_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alerts WHERE is_active = 1')
    alerts = cursor.fetchall()
    conn.close()
    return alerts
