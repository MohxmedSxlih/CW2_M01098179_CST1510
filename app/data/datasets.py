import pandas as pd
from app.data.db import connect_database

def insert_dataset(name, source=None, category=None, size=None):
    """Insert a new dataset metadata record."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO datasets_metadata (name, source, category, size)
        VALUES (?, ?, ?, ?)
    """, (name, source, category, size))

    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id


def get_all_datasets():
    """Retrieve all dataset metadata records as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def update_dataset(dataset_id, name=None, source=None, category=None, size=None):

    conn = connect_database()
    cursor = conn.cursor()

    # Build UPDATE query dynamically
    updates = []
    values = []

    if name is not None:
        updates.append("name = ?")
        values.append(name)
    if source is not None:
        updates.append("source = ?")
        values.append(source)
    if category is not None:
        updates.append("category = ?")
        values.append(category)
    if size is not None:
        updates.append("size = ?")
        values.append(size)

    if not updates:
        conn.close()
        return 0

    values.append(dataset_id)

    query = f"UPDATE datasets_metadata SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)

    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()

    return rows_updated


def delete_dataset(dataset_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM datasets_metadata WHERE id = ?",
        (dataset_id,)
    )

    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()

    return rows_deleted