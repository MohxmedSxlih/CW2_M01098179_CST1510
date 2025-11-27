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
