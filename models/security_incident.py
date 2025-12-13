"""
SecurityIncident entity class for the Multi-Domain Intelligence Platform.
Represents a cybersecurity incident in the system.
"""


class SecurityIncident:
    """Represents a cybersecurity incident.

    Attributes:
        __id (int): Unique incident identifier
        __date (str): Date of the incident
        __incident_type (str): Type of incident (e.g., Malware, Phishing)
        __severity (str): Severity level (Low, Medium, High, Critical)
        __status (str): Current status (Open, In Progress, Resolved)
        __description (str): Detailed description of the incident
        __reported_by (str): Person who reported the incident
    """

    def __init__(self, incident_id: int, date: str, incident_type: str,
                 severity: str, status: str, description: str, reported_by: str):
        """Initialize a SecurityIncident object.

        Args:
            incident_id: Unique identifier
            date: Date of the incident (YYYY-MM-DD format)
            incident_type: Type of security incident
            severity: Severity level
            status: Current status
            description: Detailed description
            reported_by: Reporter's name
        """
        self.__id = incident_id
        self.__date = date
        self.__incident_type = incident_type
        self.__severity = severity
        self.__status = status
        self.__description = description
        self.__reported_by = reported_by

    # Getter methods
    def get_id(self) -> int:
        """Get the incident ID."""
        return self.__id

    def get_date(self) -> str:
        """Get the incident date."""
        return self.__date

    def get_incident_type(self) -> str:
        """Get the incident type."""
        return self.__incident_type

    def get_severity(self) -> str:
        """Get the severity level."""
        return self.__severity

    def get_status(self) -> str:
        """Get the current status."""
        return self.__status

    def get_description(self) -> str:
        """Get the incident description."""
        return self.__description

    def get_reported_by(self) -> str:
        """Get the reporter's name."""
        return self.__reported_by

    # Setter method for status (incidents can be updated)
    def set_status(self, new_status: str) -> None:
        """Update the incident status.

        Args:
            new_status: New status value
        """
        self.__status = new_status

    def get_severity_level(self) -> int:
        """Get a numeric severity level for sorting/comparison.

        Returns:
            int: Severity level (1=Low, 2=Medium, 3=High, 4=Critical, 0=Unknown)
        """
        severity_map = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }
        return severity_map.get(self.__severity.lower(), 0)

    def is_resolved(self) -> bool:
        """Check if the incident is resolved.

        Returns:
            bool: True if status is 'Resolved', False otherwise
        """
        return self.__status.lower() == "resolved"

    def is_critical(self) -> bool:
        """Check if the incident is critical severity.

        Returns:
            bool: True if severity is 'Critical', False otherwise
        """
        return self.__severity.lower() == "critical"

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return (f"Incident #{self.__id}: {self.__incident_type} "
                f"[{self.__severity.upper()}] - {self.__status}")

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (f"SecurityIncident(id={self.__id}, type='{self.__incident_type}', "
                f"severity='{self.__severity}', status='{self.__status}')")