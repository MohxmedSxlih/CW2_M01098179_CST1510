"""
IncidentService class for managing security incidents.
Handles CRUD operations and business logic for SecurityIncident entities.
"""

from typing import List, Optional
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident


class IncidentService:
    """Service class for managing security incidents.

    Provides business logic and database operations for security incidents,
    converting between database rows and SecurityIncident objects.
    """

    def __init__(self, db_manager: DatabaseManager):
        """Initialize IncidentService with a database manager.

        Args:
            db_manager: DatabaseManager instance
        """
        self._db = db_manager

    def get_all_incidents(self) -> List[SecurityIncident]:
        """Retrieve all security incidents.

        Returns:
            List[SecurityIncident]: List of all incidents
        """
        rows = self._db.fetch_all(
            "SELECT id, date, incident_type, severity, status, description, reported_by FROM cyber_incidents ORDER BY id DESC"
        )

        incidents = []
        for row in rows:
            incident = SecurityIncident(
                incident_id=row['id'],
                date=row['date'],
                incident_type=row['incident_type'],
                severity=row['severity'],
                status=row['status'],
                description=row['description'] or "",
                reported_by=row['reported_by'] or ""
            )
            incidents.append(incident)

        return incidents

    def get_incident_by_id(self, incident_id: int) -> Optional[SecurityIncident]:
        """Retrieve a specific incident by ID.

        Args:
            incident_id: ID of the incident to retrieve

        Returns:
            Optional[SecurityIncident]: Incident object if found, None otherwise
        """
        row = self._db.fetch_one(
            "SELECT id, date, incident_type, severity, status, description, reported_by FROM cyber_incidents WHERE id = ?",
            (incident_id,)
        )

        if row is None:
            return None

        return SecurityIncident(
            incident_id=row['id'],
            date=row['date'],
            incident_type=row['incident_type'],
            severity=row['severity'],
            status=row['status'],
            description=row['description'] or "",
            reported_by=row['reported_by'] or ""
        )

    def create_incident(self, date: str, incident_type: str, severity: str,
                        status: str, description: str, reported_by: str) -> int:
        """Create a new security incident.

        Args:
            date: Date of the incident (YYYY-MM-DD)
            incident_type: Type of incident
            severity: Severity level
            status: Initial status
            description: Detailed description
            reported_by: Reporter's name

        Returns:
            int: ID of the newly created incident
        """
        cursor = self._db.execute_query(
            """INSERT INTO cyber_incidents (title, date, incident_type, severity, status, description, reported_by)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (incident_type, date, incident_type, severity, status, description, reported_by)
        )
        return cursor.lastrowid

    def update_incident_status(self, incident_id: int, new_status: str) -> bool:
        """Update the status of an incident.

        Args:
            incident_id: ID of the incident to update
            new_status: New status value

        Returns:
            bool: True if update successful, False otherwise
        """
        cursor = self._db.execute_query(
            "UPDATE cyber_incidents SET status = ? WHERE id = ?",
            (new_status, incident_id)
        )
        return cursor.rowcount > 0

    def delete_incident(self, incident_id: int) -> bool:
        """Delete an incident by ID.

        Args:
            incident_id: ID of the incident to delete

        Returns:
            bool: True if deletion successful, False otherwise
        """
        cursor = self._db.execute_query(
            "DELETE FROM cyber_incidents WHERE id = ?",
            (incident_id,)
        )
        return cursor.rowcount > 0

    def get_critical_incidents(self) -> List[SecurityIncident]:
        """Get all incidents with critical severity.

        Returns:
            List[SecurityIncident]: List of critical incidents
        """
        incidents = self.get_all_incidents()
        return [inc for inc in incidents if inc.is_critical()]

    def get_unresolved_incidents(self) -> List[SecurityIncident]:
        """Get all incidents that are not resolved.

        Returns:
            List[SecurityIncident]: List of unresolved incidents
        """
        incidents = self.get_all_incidents()
        return [inc for inc in incidents if not inc.is_resolved()]