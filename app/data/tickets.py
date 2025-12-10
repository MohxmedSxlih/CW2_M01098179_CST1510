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


def update_ticket_status(ticket_id, new_status):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE it_tickets SET status = ? WHERE id = ?",
        (new_status, ticket_id)
    )

    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()

    return rows_updated


def update_ticket(ticket_id, title=None, priority=None, status=None, created_date=None):

    conn = connect_database()
    cursor = conn.cursor()

    # Build UPDATE query dynamically
    updates = []
    values = []

    if title is not None:
        updates.append("title = ?")
        values.append(title)
    if priority is not None:
        updates.append("priority = ?")
        values.append(priority)
    if status is not None:
        updates.append("status = ?")
        values.append(status)
    if created_date is not None:
        updates.append("created_date = ?")
        values.append(created_date)

    if not updates:
        conn.close()
        return 0

    values.append(ticket_id)

    query = f"UPDATE it_tickets SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)

    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()

    return rows_updated


def delete_ticket(ticket_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM it_tickets WHERE id = ?",
        (ticket_id,)
    )

    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()

    return rows_deleted

