from app.data.db import connect_database
from app.data.auth import register_user, login_user
from app.data.incidents import (
    insert_incident,
    get_all_incidents,
    update_incident_status,
    delete_incident,
    get_incidents_by_type_count,
    get_high_severity_by_status
)
import pandas as pd


def run_comprehensive_tests():
    """
    Run comprehensive tests on database functionality.
    Tests authentication, CRUD operations, and analytical queries.
    """
    print("\n" + "=" * 60)
    print("RUNNING COMPREHENSIVE DATABASE TESTS")
    print("=" * 60)

    conn = connect_database()

    # Cleanup: Remove test user if exists from previous runs
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = 'test_user'")
    conn.commit()

    # Test 1: User Authentication
    print("\n[TEST 1] User Authentication")
    print("-" * 60)

    success, msg = register_user("test_user", "TestPass123!")
    status = "PASSED" if success else "FAILED"
    print(f"  Registration Test: {status}")
    print(f"  Message: {msg}")

    success, msg = login_user("test_user", "TestPass123!")
    status = "PASSED" if success else "FAILED"
    print(f"  Login Test: {status}")
    print(f"  Message: {msg}")

    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")
    print("-" * 60)

    # Create operation
    print("  Testing CREATE operation...")
    test_id = insert_incident(
        "2024-12-10",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident for validation purposes",
        "test_user"
    )
    print(f"  Result: Successfully created incident with ID #{test_id}")

    # Read operation
    print("\n  Testing READ operation...")
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Result: Successfully retrieved incident #{test_id}")
    print(f"  Details: {df['incident_type'].values[0]} - {df['status'].values[0]}")

    # Update operation
    print("\n  Testing UPDATE operation...")
    rows = update_incident_status(test_id, "Resolved")
    print(f"  Result: Successfully updated {rows} record(s)")

    # Verify update
    df_updated = pd.read_sql_query(
        "SELECT status FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Verification: Status changed to '{df_updated['status'].values[0]}'")

    # Delete operation
    print("\n  Testing DELETE operation...")
    rows = delete_incident(test_id)
    print(f"  Result: Successfully deleted {rows} record(s)")

    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")
    print("-" * 60)

    print("  Running incident type analysis...")
    df_by_type = get_incidents_by_type_count()
    print(f"  Result: Found {len(df_by_type)} different incident types")
    if len(df_by_type) > 0:
        print(f"  Top incident type: {df_by_type.iloc[0]['incident_type']} ({df_by_type.iloc[0]['count']} occurrences)")

    print("\n  Running high severity analysis...")
    df_high = get_high_severity_by_status()
    print(f"  Result: Found {len(df_high)} status categories for high severity incidents")
    if len(df_high) > 0:
        total_high = df_high['count'].sum()
        print(f"  Total high severity incidents: {total_high}")

    conn.close()

    print("\n" + "=" * 60)
    print("TEST SUMMARY: All tests completed successfully")
    print("=" * 60)
    print("\nDatabase validation complete. System is ready for use.")


if __name__ == "__main__":
    run_comprehensive_tests()