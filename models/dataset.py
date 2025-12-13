"""
Dataset entity class for the Multi-Domain Intelligence Platform.
Represents a data science dataset in the system.
"""


class Dataset:
    """Represents a data science dataset.

    Attributes:
        __id (int): Unique dataset identifier
        __name (str): Dataset name
        __source (str): Data source
        __category (str): Dataset category
        __size (int): Size in megabytes
    """

    def __init__(self, dataset_id: int, name: str, source: str = "",
                 category: str = "", size: int = 0):
        """Initialize a Dataset object.

        Args:
            dataset_id: Unique identifier
            name: Dataset name
            source: Data source (optional)
            category: Dataset category (optional)
            size: Size in megabytes (default: 0)
        """
        self.__id = dataset_id
        self.__name = name
        self.__source = source if source else "Unknown"
        self.__category = category if category else "Uncategorized"
        self.__size = size

    # Getter methods
    def get_id(self) -> int:
        """Get the dataset ID."""
        return self.__id

    def get_name(self) -> str:
        """Get the dataset name."""
        return self.__name

    def get_source(self) -> str:
        """Get the data source."""
        return self.__source

    def get_category(self) -> str:
        """Get the dataset category."""
        return self.__category

    def get_size(self) -> int:
        """Get the dataset size in MB."""
        return self.__size

    def get_size_gb(self) -> float:
        """Get the dataset size in gigabytes.

        Returns:
            float: Size in GB (rounded to 2 decimal places)
        """
        return round(self.__size / 1024, 2)

    def get_size_formatted(self) -> str:
        """Get a human-readable size string.

        Returns:
            str: Formatted size (e.g., "1.5 GB" or "500 MB")
        """
        if self.__size >= 1024:
            return f"{self.get_size_gb()} GB"
        else:
            return f"{self.__size} MB"

    def is_large(self) -> bool:
        """Check if the dataset is considered large (>1GB).

        Returns:
            bool: True if size > 1024 MB, False otherwise
        """
        return self.__size > 1024

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return (f"Dataset #{self.__id}: {self.__name} "
                f"[{self.get_size_formatted()}] - {self.__category}")

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (f"Dataset(id={self.__id}, name='{self.__name}', "
                f"size={self.__size}MB, category='{self.__category}')")