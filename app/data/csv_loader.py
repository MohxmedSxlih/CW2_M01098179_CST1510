import pandas as pd
from pathlib import Path
from app.data.db import connect_database, DB_PATH

# Get DATA directory from DB_PATH
DATA_DIR = DB_PATH.parent


def load_cyber_incidents():
    """Load cyber_incidents.csv with column mapping."""
    csv_path = DATA_DIR / "cyber_incidents.csv"

    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return 0

    try:
        # Read CSV
        df = pd.read_csv(csv_path)

        # Your CSV has: incident_id, timestamp, severity, category, status, description
        # Your table needs: date, incident_type, severity, status, description, reported_by

        # Rename columns to match database
        df = df.rename(columns={
            'timestamp': 'date',
            'category': 'incident_type'
        })

        # Add reported_by column (doesn't exist in CSV)
        df['reported_by'] = None

        # Select only columns needed for the table
        df = df[['date', 'incident_type', 'severity', 'status', 'description', 'reported_by']]

        # Load into database
        conn = connect_database()
        df.to_sql(name='cyber_incidents', con=conn, if_exists='append', index=False)
        conn.close()

        print(f"Loaded {len(df)} rows into cyber_incidents")
        return len(df)

    except Exception as e:
        print(f"Error loading cyber_incidents: {e}")
        import traceback
        traceback.print_exc()
        return 0


def load_datasets_metadata():
    """Load datasets_metadata.csv with column mapping."""
    csv_path = DATA_DIR / "datasets_metadata.csv"

    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return 0

    try:
        # Read CSV
        df = pd.read_csv(csv_path)

        # Your CSV has: dataset_id, name, rows, columns, uploaded_by, upload_date
        # Your table needs: name, source, category, size

        # Rename and map columns
        df = df.rename(columns={
            'uploaded_by': 'source',
            'rows': 'size'
        })

        # Add category column (doesn't exist in CSV)
        df['category'] = 'General'

        # Select only columns needed for the table
        df = df[['name', 'source', 'category', 'size']]

        # Load into database
        conn = connect_database()
        df.to_sql(name='datasets_metadata', con=conn, if_exists='append', index=False)
        conn.close()

        print(f"Loaded {len(df)} rows into datasets_metadata")
        return len(df)

    except Exception as e:
        print(f"Error loading datasets_metadata: {e}")
        import traceback
        traceback.print_exc()
        return 0


def load_it_tickets():
    """Load it_tickets.csv with column mapping."""
    csv_path = DATA_DIR / "it_tickets.csv"

    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return 0

    try:
        # Read CSV
        df = pd.read_csv(csv_path)

        # Your CSV has: ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours
        # Your table needs: title, priority, status, created_date

        # Rename columns to match database
        df = df.rename(columns={
            'description': 'title',
            'created_at': 'created_date'
        })

        # Select only columns needed for the table
        df = df[['title', 'priority', 'status', 'created_date']]

        # Load into database
        conn = connect_database()
        df.to_sql(name='it_tickets', con=conn, if_exists='append', index=False)
        conn.close()

        print(f"Loaded {len(df)} rows into it_tickets")
        return len(df)

    except Exception as e:
        print(f"Error loading it_tickets: {e}")
        import traceback
        traceback.print_exc()
        return 0


def load_all_csv_data():
    """
    Load all CSV files into their respective database tables.
    Handles column mapping between CSV and database schemas.

    Returns:
        int: Total number of rows loaded across all tables
    """
    print("\n" + "=" * 50)
    print("Loading CSV Data into Database")
    print("=" * 50)

    total_rows = 0

    # Load each CSV with its specific mapping
    total_rows += load_cyber_incidents()
    total_rows += load_datasets_metadata()
    total_rows += load_it_tickets()

    print(f"\nTotal rows loaded: {total_rows}")
    print("=" * 50)

    return total_rows


# Example usage - run this file directly to load data
if __name__ == "__main__":
    from app.data.db import connect_database
    from app.data.schema import create_all_tables

    # First, make sure tables are created
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # Then load the CSV data
    load_all_csv_data()