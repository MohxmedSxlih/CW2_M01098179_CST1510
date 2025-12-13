"""
DatabaseManager service class for the Multi-Domain Intelligence Platform.
Handles all database connections and queries in a centralized way.
"""

import sqlite3
from pathlib import Path
from typing import Any, List, Tuple, Optional


class DatabaseManager:
    """Manages SQLite database connections and operations.

    This class provides a centralized way to interact with the database,
    ensuring consistent connection handling and query execution.
    """

    def __init__(self, db_path: str = None):
        """Initialize DatabaseManager with a database path.

        Args:
            db_path: Path to the SQLite database file.
                    If None, uses default path in app/data/
        """
        if db_path is None:
            # Default path: app/data/intelligence_platform.db
            base_dir = Path(__file__).resolve().parent.parent / "app" / "data"
            db_path = base_dir / "intelligence_platform.db"

        self._db_path = str(db_path)
        self._connection: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """Establish a database connection.

        Returns:
            sqlite3.Connection: Active database connection
        """
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row  # Enable column name access
        return self._connection

    def close(self) -> None:
        """Close the database connection if open."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def execute_query(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a write query (INSERT, UPDATE, DELETE).

        Args:
            sql: SQL query string
            params: Query parameters tuple

        Returns:
            sqlite3.Cursor: Cursor after execution
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor

    def fetch_one(self, sql: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Execute a query and fetch one result.

        Args:
            sql: SQL query string
            params: Query parameters tuple

        Returns:
            Optional[sqlite3.Row]: Single result row or None
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()

    def fetch_all(self, sql: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Execute a query and fetch all results.

        Args:
            sql: SQL query string
            params: Query parameters tuple

        Returns:
            List[sqlite3.Row]: List of result rows
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    def get_last_insert_id(self) -> int:
        """Get the ID of the last inserted row.

        Returns:
            int: Last insert row ID
        """
        cursor = self._connection.cursor()
        return cursor.lastrowid

    def __enter__(self):
        """Context manager entry - establish connection."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connection."""
        self.close()

    def __del__(self):
        """Destructor - ensure connection is closed."""
        self.close()