import pandas as pd
from app.data.db import connect_database

def insert_ticket(title, priority, status='open', created_date=None):
    """Insert a new IT support ticket."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO it_tickets (title, priority, status, created_date)
        VALUES (?, ?, ?, ?)
    """, (title, priority, status, created_date))

    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id


def get_all_tickets():
    """Retrieve all tickets as a DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC",
        conn
    )
    conn.close()
    return df
