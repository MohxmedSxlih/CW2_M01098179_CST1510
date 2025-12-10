import pandas as pd
from app.data.db import connect_database


def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO cyber_incidents
                       (date, incident_type, severity, status, description, reported_by)
                   VALUES (?, ?, ?, ?, ?, ?)
                   """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id


def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def update_incident_status(incident_id, new_status):
    """
    Update the status of an incident.

    Args:
        incident_id: ID of the incident to update
        new_status: New status value

    Returns:
        int: Number of rows updated (1 if successful, 0 if not found)
    """
    # connect to database
    conn = connect_database()
    cursor = conn.cursor()

    # update status
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )

    # commit and return count
    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()

    return rows_updated


def update_incident(incident_id, date=None, incident_type=None, severity=None,
                    status=None, description=None, reported_by=None):
    """
    Update multiple fields of an incident.
    Only updates fields that are provided (not None).

    Args:
        incident_id: ID of the incident to update
        date: New date (optional)
        incident_type: New incident type (optional)
        severity: New severity (optional)
        status: New status (optional)
        description: New description (optional)
        reported_by: New reporter (optional)

    Returns:
        int: Number of rows updated
    """
    # connect to database
    conn = connect_database()
    cursor = conn.cursor()

    # build update query dynamically based on provided fields
    updates = []
    values = []

    if date is not None:
        updates.append("date = ?")
        values.append(date)
    if incident_type is not None:
        updates.append("incident_type = ?")
        values.append(incident_type)
    if severity is not None:
        updates.append("severity = ?")
        values.append(severity)
    if status is not None:
        updates.append("status = ?")
        values.append(status)
    if description is not None:
        updates.append("description = ?")
        values.append(description)
    if reported_by is not None:
        updates.append("reported_by = ?")
        values.append(reported_by)

    if not updates:
        conn.close()
        return 0

    # add incident_id to values
    values.append(incident_id)

    # execute update query
    query = f"UPDATE cyber_incidents SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)

    # commit and return count
    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()

    return rows_updated


def delete_incident(incident_id):
    """
    Delete an incident from the database.

    WARNING: This is permanent and cannot be undone!

    Args:
        incident_id: ID of the incident to delete

    Returns:
        int: Number of rows deleted (1 if successful, 0 if not found)
    """
    # connect to database
    conn = connect_database()
    cursor = conn.cursor()

    # delete incident
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id,)
    )

    # commit and return count
    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()

    return rows_deleted


# analytical queries
def get_incidents_by_type_count():
    """Count incidents by type."""
    # connect and query
    conn = connect_database()
    query = """
            SELECT incident_type, COUNT(*) as count
            FROM cyber_incidents
            GROUP BY incident_type
            ORDER BY count DESC \
            """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_high_severity_by_status():
    """Count high severity incidents by status."""
    # connect and query
    conn = connect_database()
    query = """
            SELECT status, COUNT(*) as count
            FROM cyber_incidents
            WHERE severity = 'High'
            GROUP BY status
            ORDER BY count DESC \
            """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_incident_types_with_many_cases(min_count=5):
    """Find incident types with more than min_count cases."""
    # connect and query
    conn = connect_database()
    query = """
            SELECT incident_type, COUNT(*) as count
            FROM cyber_incidents
            GROUP BY incident_type
            HAVING COUNT (*) > ?
            ORDER BY count DESC \
            """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    conn.close()
    return df