import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "intelligence_platform.db")

conn = sqlite3.connect(DB_PATH)


def create_users_table(conn):
    cursor = conn.cursor()
    createScript = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """
    cursor.execute(createScript)
    conn.commit()

def create_cyber_incidents_table(conn):
    cursor = conn.cursor()
    createScript = """
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            date TEXT
        )
    """
    cursor.execute(createScript)
    conn.commit()

def create_datasets_metadata_table(conn):
    cursor = conn.cursor()
    createScript = """
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            source TEXT,
            category TEXT,
            size INTEGER
        )
    """
    cursor.execute(createScript)
    conn.commit()

def create_it_tickets_table(conn):
    cursor = conn.cursor()
    createScript = """
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_date TEXT
        )
    """
    cursor.execute(createScript)
    conn.commit()

def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)

# Run the setup
create_all_tables(conn)
conn.close()
