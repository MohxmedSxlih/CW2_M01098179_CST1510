import os
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.data.users import get_user_by_username
from app.data.auth import register_user, login_user, user_exists
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets
from app.data.incidents import get_all_incidents
from app.data.csv_loader import load_all_csv_data


def init_database():
    """
    Complete database setup - Step 9
    """
    print("\n" + "=" * 60)
    print("STARTING DATABASE SETUP")
    print("=" * 60)

    # step 1: connect
    print("\n[1/4] Connecting to database...")
    conn = connect_database()
    print("      Connected")

    # step 2: create tables
    print("\n[2/4] Creating database tables...")
    create_all_tables(conn)
    conn.close()

    # step 3: load csv data
    print("\n[3/4] Loading CSV data...")
    load_all_csv_data()

    # step 4: verify
    print("\n[4/4] Verifying database setup...")
    conn = connect_database()
    cursor = conn.cursor()

    # count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\nDatabase Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()

    print("\n" + "=" * 60)
    print("DATABASE SETUP COMPLETE!")
    print("=" * 60)


def display_menu():
    print("\n" + "=" * 50)
    print("   MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("=" * 50)
    print("[1] Register User")
    print("[2] Login")
    print("[3] View Datasets")
    print("[4] View IT Tickets")
    print("[5] View Cyber Incidents")
    print("[6] Exit")
    print("-" * 50)


def main():
    print("\nStarting Intelligence Platform...")
    init_database()

    logged_in_user = None

    while True:
        display_menu()
        choice = input("Select an option (1-6): ").strip()

        # 1. REGISTER USER
        if choice == "1":
            print("\n--- REGISTER USER ---")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            success, msg = register_user(username, password)
            print(msg)

            if success:
                logged_in_user = username


        # 2. LOGIN
        elif choice == "2":
            print("\n--- LOGIN ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            success, msg = login_user(username, password)
            print(msg)

            if success:
                logged_in_user = username


        # 3. VIEW DATASETS
        elif choice == "3":
            print("\n--- DATASETS METADATA ---")
            df = get_all_datasets()
            if df.empty:
                print("No datasets found.")
            else:
                print(df)


        # 4. VIEW IT TICKETS
        elif choice == "4":
            print("\n--- IT SUPPORT TICKETS ---")
            df = get_all_tickets()
            if df.empty:
                print("No tickets found.")
            else:
                print(df)


        # 5. VIEW CYBER INCIDENTS
        elif choice == "5":
            print("\n--- CYBER INCIDENTS ---")
            df = get_all_incidents()
            if df.empty:
                print("No incidents found.")
            else:
                print(df)


        # 6. EXIT
        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("Invalid option. Please choose 1–6.")


if __name__ == "__main__":
    main()