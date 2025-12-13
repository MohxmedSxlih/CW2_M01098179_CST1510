"""
AuthManager service class for the Multi-Domain Intelligence Platform.
Handles user authentication, registration, and password management.
"""

import bcrypt
from typing import Optional, Tuple
from services.database_manager import DatabaseManager
from models.user import User


class AuthManager:
    """Manages user authentication and registration.

    This service handles all authentication-related operations including
    user registration, login validation, and password hashing.
    """

    def __init__(self, db_manager: DatabaseManager):
        """Initialize AuthManager with a database manager.

        Args:
            db_manager: DatabaseManager instance for database operations
        """
        self._db = db_manager

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Hash a plain-text password using bcrypt.

        Args:
            plain_password: Plain-text password to hash

        Returns:
            str: Hashed password string
        """
        password_bytes = plain_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        return hashed_bytes.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain-text password against a hash.

        Args:
            plain_password: Plain-text password to check
            hashed_password: Stored password hash

        Returns:
            bool: True if password matches, False otherwise
        """
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    def validate_username(self, username: str) -> Tuple[bool, str]:
        """Validate a username according to platform rules.

        Args:
            username: Username to validate

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if len(username) < 3 or len(username) > 20:
            return False, "Username must be 3-20 characters."
        if not username.isalnum():
            return False, "Username must contain only letters and numbers."
        return True, ""

    def validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate a password according to platform rules.

        Args:
            password: Password to validate

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if len(password) < 6:
            return False, "Password must be at least 6 characters."
        if len(password) > 50:
            return False, "Password cannot exceed 50 characters."
        return True, ""

    def user_exists(self, username: str) -> bool:
        """Check if a username already exists.

        Args:
            username: Username to check

        Returns:
            bool: True if user exists, False otherwise
        """
        row = self._db.fetch_one(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        return row is not None

    def register_user(self, username: str, password: str, role: str = "user") -> Tuple[bool, str]:
        """Register a new user in the system.

        Args:
            username: Desired username
            password: Plain-text password
            role: User role (default: "user")

        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Validate username
        is_valid, error_msg = self.validate_username(username)
        if not is_valid:
            return False, error_msg

        # Check if user exists
        if self.user_exists(username):
            return False, f"Username '{username}' already exists."

        # Validate password
        is_valid, error_msg = self.validate_password(password)
        if not is_valid:
            return False, error_msg

        # Hash password and insert user
        password_hash = self.hash_password(password)

        try:
            self._db.execute_query(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            return True, f"User '{username}' registered successfully!"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"

    def login_user(self, username: str, password: str) -> Tuple[bool, Optional[User], str]:
        """Authenticate a user login attempt.

        Args:
            username: Username to authenticate
            password: Plain-text password to verify

        Returns:
            Tuple[bool, Optional[User], str]: (success, user_object, message)
        """
        # Fetch user from database
        row = self._db.fetch_one(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,)
        )

        if row is None:
            return False, None, "Username not found."

        # Verify password
        user_id = row['id']
        stored_username = row['username']
        password_hash = row['password_hash']
        role = row['role']

        if self.verify_password(password, password_hash):
            # Create and return User object
            user = User(user_id, stored_username, password_hash, role)
            return True, user, "Login successful!"
        else:
            return False, None, "Incorrect password."

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a User object by username.

        Args:
            username: Username to look up

        Returns:
            Optional[User]: User object if found, None otherwise
        """
        row = self._db.fetch_one(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,)
        )

        if row is None:
            return None

        return User(
            user_id=row['id'],
            username=row['username'],
            password_hash=row['password_hash'],
            role=row['role']
        )