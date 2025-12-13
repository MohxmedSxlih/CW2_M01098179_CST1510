"""
ITTicket entity class for the Multi-Domain Intelligence Platform.
Represents an IT support ticket in the system.
"""


class ITTicket:
    """Represents an IT support ticket.

    Attributes:
        __id (int): Unique ticket identifier
        __title (str): Ticket title/subject
        __priority (str): Priority level (Low, Medium, High, Critical)
        __status (str): Current status (Open, In Progress, Resolved)
        __created_date (str): Date the ticket was created
    """

    def __init__(self, ticket_id: int, title: str, priority: str,
                 status: str, created_date: str = ""):
        """Initialize an ITTicket object.

        Args:
            ticket_id: Unique identifier
            title: Ticket title/subject
            priority: Priority level
            status: Current status
            created_date: Creation date (YYYY-MM-DD format)
        """
        self.__id = ticket_id
        self.__title = title
        self.__priority = priority
        self.__status = status
        self.__created_date = created_date

    # Getter methods
    def get_id(self) -> int:
        """Get the ticket ID."""
        return self.__id

    def get_title(self) -> str:
        """Get the ticket title."""
        return self.__title

    def get_priority(self) -> str:
        """Get the priority level."""
        return self.__priority

    def get_status(self) -> str:
        """Get the current status."""
        return self.__status

    def get_created_date(self) -> str:
        """Get the creation date."""
        return self.__created_date

    # Setter method for status
    def set_status(self, new_status: str) -> None:
        """Update the ticket status.

        Args:
            new_status: New status value
        """
        self.__status = new_status

    def get_priority_level(self) -> int:
        """Get a numeric priority level for sorting/comparison.

        Returns:
            int: Priority level (1=Low, 2=Medium, 3=High, 4=Critical, 0=Unknown)
        """
        priority_map = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }
        return priority_map.get(self.__priority.lower(), 0)

    def is_resolved(self) -> bool:
        """Check if the ticket is resolved.

        Returns:
            bool: True if status is 'Resolved', False otherwise
        """
        return self.__status.lower() == "resolved"

    def is_open(self) -> bool:
        """Check if the ticket is still open.

        Returns:
            bool: True if status is 'Open', False otherwise
        """
        return self.__status.lower() == "open"

    def is_critical(self) -> bool:
        """Check if the ticket has critical priority.

        Returns:
            bool: True if priority is 'Critical', False otherwise
        """
        return self.__priority.lower() == "critical"

    def close_ticket(self) -> None:
        """Mark the ticket as resolved/closed."""
        self.__status = "Resolved"

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return (f"Ticket #{self.__id}: {self.__title} "
                f"[{self.__priority.upper()}] - {self.__status}")

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (f"ITTicket(id={self.__id}, title='{self.__title}', "
                f"priority='{self.__priority}', status='{self.__status}')")