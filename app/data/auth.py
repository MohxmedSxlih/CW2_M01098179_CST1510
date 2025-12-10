import bcrypt
import os

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_text_password, hashed_password_str):
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password_str.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

USER_DATA_FILE = "users.txt"

def register_user(username, password):
    if user_exists(username):
        return False, f"Error: Username '{username}' already exists."

    hashed_password = hash_password(password)

    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password}\n")

    return True, f"Success: User '{username}' registered successfully!"


def user_exists(username):
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                stored_username = line.strip().split(",")[0]
                if stored_username == username:
                    return True
    except FileNotFoundError:
        return False
    return False

def login_user(username, password):
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f.readlines():
                user, hashed_password = line.strip().split(",", 1)
                if user == username:
                    if verify_password(password, hashed_password):
                        return True, "Login successful"
                    else:
                        return False, "Incorrect password"
        return False, "Username not found"
    except FileNotFoundError:
        return False, "User data file not found"

def validate_user(username, password=None):
    if not user_exists(username):
        return False, "User does not exist"
    if password is not None:
        if login_user(username, password):
            return True, "Login successful"
        else:
            return False, "Incorrect password"
    return True, ""

def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be 3–20 characters."
    if not username.isalnum():
        return False, "Username must contain only letters and numbers."
    return True, ""

def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if len(password) > 50:
        return False, "Password cannot exceed 50 characters."
    return True, ""

def display_menu():
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("_"*50)

def main():
    print("\nWelcome to Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("Please select an option (1-3): ").strip()

        if choice == "1":
            print("\n--- USER REGISTERING ---")
            username = input("Enter username: ").strip()

            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"\nError: {error_msg}")
                continue

            # Check duplicate AFTER validation
            if user_exists(username):
                print("\nError: Username already exists")
                continue

            password = input("Enter password: ").strip()
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"\nError: {error_msg}")
                continue

            register_user(username, password)
        elif choice == "2":
            print("\n--- USER LOGIN ---")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            if login_user(username, password):
                print(f"\nSuccess: Welcome, {username}!")
            else:
                if not user_exists(username):
                    print("\nError: Username not found.")
                else:
                    print("\nError: Invalid password.")


        elif choice == "3":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")
if __name__ == "__main__":
    main()

