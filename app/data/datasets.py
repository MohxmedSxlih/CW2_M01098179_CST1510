import pandas as pd

def get_all_datasets(conn):
    """Retrieve all dataset metadata records as DataFrame."""
    return pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )

def insert_dataset(conn, name, source, category, size):
    """Insert a new dataset record."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata (name, source, category, size)
        VALUES (?, ?, ?, ?)
    """, (name, source, category, size))
    conn.commit()
    return cursor.lastrowid

def update_dataset(conn, dataset_id, name, source, category, size):
    """Update an existing dataset."""
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE datasets_metadata
        SET name = ?, source = ?, category = ?, size = ?
        WHERE id = ?
    """, (name, source, category, size, dataset_id))
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    """Delete a dataset by ID."""
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM datasets_metadata WHERE id = ?",
        (dataset_id,)
    )
    conn.commit()
    return cursor.rowcount