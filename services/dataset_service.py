"""
DatasetService class for managing datasets.
Handles CRUD operations and business logic for Dataset entities.
"""

from typing import List, Optional
from services.database_manager import DatabaseManager
from models.dataset import Dataset


class DatasetService:
    """Service class for managing datasets.

    Provides business logic and database operations for datasets,
    converting between database rows and Dataset objects.
    """

    def __init__(self, db_manager: DatabaseManager):
        """Initialize DatasetService with a database manager.

        Args:
            db_manager: DatabaseManager instance
        """
        self._db = db_manager

    def get_all_datasets(self) -> List[Dataset]:
        """Retrieve all datasets.

        Returns:
            List[Dataset]: List of all datasets
        """
        rows = self._db.fetch_all(
            "SELECT id, name, source, category, size FROM datasets_metadata ORDER BY id DESC"
        )

        datasets = []
        for row in rows:
            dataset = Dataset(
                dataset_id=row['id'],
                name=row['name'],
                source=row['source'] or "",
                category=row['category'] or "",
                size=row['size'] or 0
            )
            datasets.append(dataset)

        return datasets

    def get_dataset_by_id(self, dataset_id: int) -> Optional[Dataset]:
        """Retrieve a specific dataset by ID.

        Args:
            dataset_id: ID of the dataset to retrieve

        Returns:
            Optional[Dataset]: Dataset object if found, None otherwise
        """
        row = self._db.fetch_one(
            "SELECT id, name, source, category, size FROM datasets_metadata WHERE id = ?",
            (dataset_id,)
        )

        if row is None:
            return None

        return Dataset(
            dataset_id=row['id'],
            name=row['name'],
            source=row['source'] or "",
            category=row['category'] or "",
            size=row['size'] or 0
        )

    def create_dataset(self, name: str, source: str = "",
                       category: str = "", size: int = 0) -> int:
        """Create a new dataset.

        Args:
            name: Dataset name
            source: Data source
            category: Dataset category
            size: Size in MB

        Returns:
            int: ID of the newly created dataset
        """
        cursor = self._db.execute_query(
            "INSERT INTO datasets_metadata (name, source, category, size) VALUES (?, ?, ?, ?)",
            (name, source, category, size)
        )
        return cursor.lastrowid

    def update_dataset(self, dataset_id: int, name: str, source: str,
                       category: str, size: int) -> bool:
        """Update an existing dataset.

        Args:
            dataset_id: ID of the dataset to update
            name: New name
            source: New source
            category: New category
            size: New size in MB

        Returns:
            bool: True if update successful, False otherwise
        """
        cursor = self._db.execute_query(
            """UPDATE datasets_metadata
               SET name     = ?,
                   source   = ?,
                   category = ?,
                   size     = ?
               WHERE id = ?""",
            (name, source, category, size, dataset_id)
        )
        return cursor.rowcount > 0

    def delete_dataset(self, dataset_id: int) -> bool:
        """Delete a dataset by ID.

        Args:
            dataset_id: ID of the dataset to delete

        Returns:
            bool: True if deletion successful, False otherwise
        """
        cursor = self._db.execute_query(
            "DELETE FROM datasets_metadata WHERE id = ?",
            (dataset_id,)
        )
        return cursor.rowcount > 0

    def get_large_datasets(self) -> List[Dataset]:
        """Get all datasets that are considered large (>1GB).

        Returns:
            List[Dataset]: List of large datasets
        """
        datasets = self.get_all_datasets()
        return [ds for ds in datasets if ds.is_large()]

    def get_datasets_by_category(self, category: str) -> List[Dataset]:
        """Get all datasets in a specific category.

        Args:
            category: Category name to filter by

        Returns:
            List[Dataset]: List of datasets in the category
        """
        datasets = self.get_all_datasets()
        return [ds for ds in datasets if ds.get_category().lower() == category.lower()]

    def get_total_size(self) -> int:
        """Calculate the total size of all datasets.

        Returns:
            int: Total size in MB
        """
        datasets = self.get_all_datasets()
        return sum(ds.get_size() for ds in datasets)