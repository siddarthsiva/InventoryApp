import os
import sys
import sqlite3

BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'db', 'items.db'))

def initialize_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                serial_number TEXT UNIQUE NOT NULL,
                qr_code_path TEXT,
                threshold INTEGER NOT NULL
            )
        ''')
        conn.commit()
        303
        03
        3

        3
        3
        3
        6203



def add_item(name, quantity, serial_number, threshold, qr_code_path):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO items (name, quantity, serial_number, qr_code_path, threshold)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, quantity, serial_number, qr_code_path, threshold))
        conn.commit()

def update_item(serial_number, name, quantity, threshold):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE items
            SET name = ?, quantity = ?, threshold = ?
            WHERE serial_number = ?
        ''', (name, quantity, threshold, serial_number))
        conn.commit()

def get_item_by_serial(serial_number):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE LOWER(serial_number) = LOWER(?)', (serial_number,))
        return cursor.fetchone()

def get_all_items():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        return cursor.fetchall()

def get_low_stock_items():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, quantity, threshold FROM items
            WHERE quantity < threshold
        ''')
        return cursor.fetchall()


if __name__ == '__main__':
    initialize_database()
    print(f"✅ Database created at: {DB_PATH}")
