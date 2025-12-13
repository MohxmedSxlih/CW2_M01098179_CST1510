"""
TicketService class for managing IT tickets.
Handles CRUD operations and business logic for ITTicket entities.
"""

from typing import List, Optional
from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket


class TicketService:
    """Service class for managing IT support tickets.

    Provides business logic and database operations for IT tickets,
    converting between database rows and ITTicket objects.
    """

    def __init__(self, db_manager: DatabaseManager):
        """Initialize TicketService with a database manager.

        Args:
            db_manager: DatabaseManager instance
        """
        self._db = db_manager

    def get_all_tickets(self) -> List[ITTicket]:
        """Retrieve all IT tickets.

        Returns:
            List[ITTicket]: List of all tickets
        """
        rows = self._db.fetch_all(
            "SELECT id, title, priority, status, created_date FROM it_tickets ORDER BY id DESC"
        )

        tickets = []
        for row in rows:
            ticket = ITTicket(
                ticket_id=row['id'],
                title=row['title'],
                priority=row['priority'],
                status=row['status'],
                created_date=row['created_date'] or ""
            )
            tickets.append(ticket)

        return tickets

    def get_ticket_by_id(self, ticket_id: int) -> Optional[ITTicket]:
        """Retrieve a specific ticket by ID.

        Args:
            ticket_id: ID of the ticket to retrieve

        Returns:
            Optional[ITTicket]: Ticket object if found, None otherwise
        """
        row = self._db.fetch_one(
            "SELECT id, title, priority, status, created_date FROM it_tickets WHERE id = ?",
            (ticket_id,)
        )

        if row is None:
            return None

        return ITTicket(
            ticket_id=row['id'],
            title=row['title'],
            priority=row['priority'],
            status=row['status'],
            created_date=row['created_date'] or ""
        )

    def create_ticket(self, title: str, priority: str,
                      status: str = "Open", created_date: str = "") -> int:
        """Create a new IT ticket.

        Args:
            title: Ticket title/subject
            priority: Priority level
            status: Initial status (default: "Open")
            created_date: Creation date (YYYY-MM-DD)

        Returns:
            int: ID of the newly created ticket
        """
        cursor = self._db.execute_query(
            "INSERT INTO it_tickets (title, priority, status, created_date) VALUES (?, ?, ?, ?)",
            (title, priority, status, created_date)
        )
        return cursor.lastrowid

    def update_ticket_status(self, ticket_id: int, new_status: str) -> bool:
        """Update the status of a ticket.

        Args:
            ticket_id: ID of the ticket to update
            new_status: New status value

        Returns:
            bool: True if update successful, False otherwise
        """
        cursor = self._db.execute_query(
            "UPDATE it_tickets SET status = ? WHERE id = ?",
            (new_status, ticket_id)
        )
        return cursor.rowcount > 0

    def delete_ticket(self, ticket_id: int) -> bool:
        """Delete a ticket by ID.

        Args:
            ticket_id: ID of the ticket to delete

        Returns:
            bool: True if deletion successful, False otherwise
        """
        cursor = self._db.execute_query(
            "DELETE FROM it_tickets WHERE id = ?",
            (ticket_id,)
        )
        return cursor.rowcount > 0

    def get_open_tickets(self) -> List[ITTicket]:
        """Get all open tickets.

        Returns:
            List[ITTicket]: List of open tickets
        """
        tickets = self.get_all_tickets()
        return [ticket for ticket in tickets if ticket.is_open()]

    def get_critical_tickets(self) -> List[ITTicket]:
        """Get all tickets with critical priority.

        Returns:
            List[ITTicket]: List of critical tickets
        """
        tickets = self.get_all_tickets()
        return [ticket for ticket in tickets if ticket.is_critical()]

    def get_unresolved_tickets(self) -> List[ITTicket]:
        """Get all tickets that are not resolved.

        Returns:
            List[ITTicket]: List of unresolved tickets
        """
        tickets = self.get_all_tickets()
        return [ticket for ticket in tickets if not ticket.is_resolved()]

    def close_ticket(self, ticket_id: int) -> bool:
        """Close a ticket by marking it as resolved.

        Args:
            ticket_id: ID of the ticket to close

        Returns:
            bool: True if successful, False otherwise
        """
        return self.update_ticket_status(ticket_id, "Resolved")