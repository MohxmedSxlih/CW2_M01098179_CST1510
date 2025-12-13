"""
User entity class for the Multi-Domain Intelligence Platform.
This represents a user in the system with authentication capabilities.
"""


class User:
    """Represents a user in the Multi-Domain Intelligence Platform.

    Attributes:
        __id (int): Unique user identifier
        __username (str): Username for login
        __password_hash (str): Hashed password
        __role (str): User role (e.g., 'user', 'admin')
    """

    def __init__(self, user_id: int, username: str, password_hash: str, role: str = "user"):
        """Initialize a User object.

        Args:
            user_id: Unique identifier for the user
            username: Username for authentication
            password_hash: Hashed password string
            role: User role (default: "user")
        """
        self.__id = user_id
        self.__username = username
        self.__password_hash = password_hash
        self.__role = role

    # Getter methods
    def get_id(self) -> int:
        """Get the user ID."""
        return self.__id

    def get_username(self) -> str:
        """Get the username."""
        return self.__username

    def get_password_hash(self) -> str:
        """Get the password hash."""
        return self.__password_hash

    def get_role(self) -> str:
        """Get the user role."""
        return self.__role

    def is_admin(self) -> bool:
        """Check if the user has admin privileges.

        Returns:
            bool: True if user is admin, False otherwise
        """
        return self.__role.lower() == "admin"

    def __str__(self) -> str:
        """Return a string representation of the user."""
        return f"User(id={self.__id}, username='{self.__username}', role='{self.__role}')"

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return f"User(id={self.__id}, username='{self.__username}', role='{self.__role}')"