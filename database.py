import sqlite3
import os

DB_FILE = "database.db"
VERSION_FILE = "migrations/versioning.txt"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create a migrations table (if it doesn't exist)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        version TEXT NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create a users table (if it doesn't exist)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

    # Update versioning file
    with open(VERSION_FILE, "a") as f:
        f.write("\nVersion 1.0 - Initial setup applied")

if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        initialize_db()
        print("Database initialized with version tracking.")
    else:
        print("Database already exists.")