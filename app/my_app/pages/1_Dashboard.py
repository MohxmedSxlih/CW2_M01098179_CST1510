"""
Refactored Dashboard using OOP principles.
Uses service classes and entity objects instead of procedural code.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Import service classes
from services.database_manager import DatabaseManager
from services.incident_service import IncidentService
from services.dataset_service import DatasetService
from services.ticket_service import TicketService
from services.ai_assistant import AIAssistant


# ------------------ SESSION CHECK --------------------------------
def ensure_session():
    """Ensure session state is initialized."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None


def redirect_if_not_logged_in():
    """Redirect to login if user is not authenticated."""
    ensure_session()
    if not st.session_state.logged_in:
        st.error("You must be logged in to view the dashboard.")
        st.stop()


def logout():
    """Log out the current user."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.success("You have been logged out.")
    st.switch_page("pages/home.py")


# ------------------ MAIN PAGE -----------------------------------
def main():
    st.set_page_config(page_title="Dashboard", layout="wide")
    redirect_if_not_logged_in()

    st.title("📊 Multi-Domain Intelligence Dashboard")
    st.caption(
        "Week 11: OOP Refactored - Using Service Classes and Entity Objects"
    )

    # Top bar (Username + Logout)
    col_user, col_logout = st.columns([3, 1])
    with col_user:
        st.write(f"👋 Logged in as **{st.session_state.username}**")
    with col_logout:
        if st.button("Logout", key="logout_button"):
            logout()

    # Initialize services
    db_manager = DatabaseManager()
    incident_service = IncidentService(db_manager)
    dataset_service = DatasetService(db_manager)
    ticket_service = TicketService(db_manager)

    # Tabs
    tab_incidents, tab_datasets, tab_tickets, tab_ai = st.tabs(
        ["🛡 Cyber Incidents", "📂 Datasets", "🛠 IT Tickets", "🤖 AI Assistant"]
    )

    # -------------------- INCIDENTS TAB ----------------------------
    with tab_incidents:
        st.subheader("🛡 Cyber Incidents – OOP Version")

        # Get all incidents as objects
        incidents = incident_service.get_all_incidents()

        st.write("### All Incidents")
        if incidents:
            # Display incidents using object methods
            for incident in incidents:
                with st.expander(f"{incident}"):
                    st.write(f"**Date:** {incident.get_date()}")
                    st.write(f"**Type:** {incident.get_incident_type()}")
                    st.write(f"**Severity:** {incident.get_severity()}")
                    st.write(f"**Status:** {incident.get_status()}")
                    st.write(f"**Reported By:** {incident.get_reported_by()}")
                    st.write(f"**Description:** {incident.get_description()}")
                    st.write(f"**Severity Level:** {incident.get_severity_level()}/4")
                    st.write(f"**Is Critical:** {'Yes' if incident.is_critical() else 'No'}")
                    st.write(f"**Is Resolved:** {'Yes' if incident.is_resolved() else 'No'}")
        else:
            st.info("No incidents found.")

        st.markdown("---")
        st.write("### ➕ Add New Incident")

        with st.form("add_incident_form"):
            date = st.date_input("Date")
            incident_type = st.text_input("Incident Type (e.g. Malware, Phishing)")
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
            description = st.text_area("Description")
            reported_by = st.text_input("Reported By")

            submitted = st.form_submit_button("Add Incident")

            if submitted:
                if incident_type and reported_by:
                    # Use service class method
                    incident_service.create_incident(
                        date.strftime("%Y-%m-%d"),
                        incident_type,
                        severity,
                        status,
                        description,
                        reported_by
                    )
                    st.success("Incident added successfully.")
                    st.rerun()
                else:
                    st.error("Please fill at least Incident Type and Reported By.")

        st.markdown("---")
        st.write("### ✏️ Update / 🗑 Delete Incident")

        if incidents:
            incident_ids = [inc.get_id() for inc in incidents]
            selected_id = st.selectbox(
                "Select Incident ID",
                incident_ids,
                key="incident_select_id",
            )

            new_status = st.selectbox(
                "New Status",
                ["Open", "In Progress", "Resolved"],
                key="incident_new_status",
            )

            col_update, col_delete = st.columns(2)
            with col_update:
                if st.button("Update Status", key="incident_update_button"):
                    # Use service class method
                    if incident_service.update_incident_status(selected_id, new_status):
                        st.success(f"Incident {selected_id} updated.")
                        st.rerun()

            with col_delete:
                if st.button("Delete Incident", key="incident_delete_button"):
                    # Use service class method
                    if incident_service.delete_incident(selected_id):
                        st.warning(f"Incident {selected_id} deleted.")
                        st.rerun()

    # -------------------- DATASETS TAB ----------------------------
    with tab_datasets:
        st.subheader("📂 Datasets – OOP Version")

        # Get all datasets as objects
        datasets = dataset_service.get_all_datasets()

        st.write("### All Datasets")
        if datasets:
            for dataset in datasets:
                with st.expander(f"{dataset}"):
                    st.write(f"**Name:** {dataset.get_name()}")
                    st.write(f"**Source:** {dataset.get_source()}")
                    st.write(f"**Category:** {dataset.get_category()}")
                    st.write(f"**Size:** {dataset.get_size_formatted()}")
                    st.write(f"**Is Large (>1GB):** {'Yes' if dataset.is_large() else 'No'}")
        else:
            st.info("No datasets found.")

        st.markdown("---")
        st.write("### ➕ Add New Dataset")

        with st.form("add_dataset_form"):
            name = st.text_input("Dataset Name")
            source = st.text_input("Source (optional)")
            category = st.text_input("Category (optional)")
            size = st.number_input("Size (MB)", min_value=0, step=1)

            submitted_ds = st.form_submit_button("Add Dataset")

            if submitted_ds:
                if name.strip() == "":
                    st.error("Dataset name is required.")
                else:
                    # Use service class method
                    dataset_service.create_dataset(name, source, category, size)
                    st.success("Dataset added successfully.")
                    st.rerun()

        st.markdown("---")
        st.write("### ✏️ Update / 🗑 Delete Dataset")

        if datasets:
            dataset_ids = [ds.get_id() for ds in datasets]
            selected_dataset_id = st.selectbox(
                "Select Dataset ID",
                dataset_ids,
                key="dataset_select_id",
            )

            st.write("### Update Dataset")

            with st.form("update_dataset_form"):
                new_name = st.text_input("New Name")
                new_source = st.text_input("New Source")
                new_category = st.text_input("New Category")
                new_size = st.number_input("New Size (MB)", min_value=0, step=1)

                update_button = st.form_submit_button("Update Dataset")

                if update_button:
                    if new_name.strip() == "":
                        st.error("Name cannot be empty.")
                    else:
                        # Use service class method
                        if dataset_service.update_dataset(
                                selected_dataset_id,
                                new_name,
                                new_source,
                                new_category,
                                new_size
                        ):
                            st.success("Dataset updated successfully.")
                            st.rerun()

            st.write("### Delete Dataset")
            if st.button("Delete Dataset", key="dataset_delete_button"):
                # Use service class method
                if dataset_service.delete_dataset(selected_dataset_id):
                    st.warning(f"Dataset {selected_dataset_id} deleted.")
                    st.rerun()

    # -------------------- TICKETS TAB ----------------------------
    with tab_tickets:
        st.subheader("🛠 IT Tickets – OOP Version")

        # Get all tickets as objects
        tickets = ticket_service.get_all_tickets()

        st.write("### All Tickets")
        if tickets:
            for ticket in tickets:
                with st.expander(f"{ticket}"):
                    st.write(f"**Title:** {ticket.get_title()}")
                    st.write(f"**Priority:** {ticket.get_priority()}")
                    st.write(f"**Status:** {ticket.get_status()}")
                    st.write(f"**Created:** {ticket.get_created_date()}")
                    st.write(f"**Priority Level:** {ticket.get_priority_level()}/4")
                    st.write(f"**Is Critical:** {'Yes' if ticket.is_critical() else 'No'}")
                    st.write(f"**Is Resolved:** {'Yes' if ticket.is_resolved() else 'No'}")
        else:
            st.info("No tickets found.")

        st.markdown("---")
        st.write("### ➕ Add New Ticket")

        with st.form("add_ticket_form"):
            date = st.date_input("Date", key="ticket_date")
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
            subject = st.text_input("Subject")

            submitted_tk = st.form_submit_button("Add Ticket")

            if submitted_tk:
                if subject:
                    # Use service class method
                    ticket_service.create_ticket(
                        subject,
                        priority,
                        status,
                        date.strftime("%Y-%m-%d")
                    )
                    st.success("Ticket added successfully.")
                    st.rerun()
                else:
                    st.error("Please fill in the subject.")

        st.markdown("---")
        st.write("### ✏️ Update / 🗑 Delete Ticket")

        if tickets:
            ticket_ids = [ticket.get_id() for ticket in tickets]
            selected_ticket_id = st.selectbox(
                "Select Ticket ID",
                ticket_ids,
                key="ticket_select_id",
            )

            new_ticket_status = st.selectbox(
                "New Status",
                ["Open", "In Progress", "Resolved"],
                key="ticket_new_status",
            )

            col_update_tk, col_delete_tk = st.columns(2)

            with col_update_tk:
                if st.button("Update Ticket Status", key="ticket_update_button"):
                    # Use service class method
                    if ticket_service.update_ticket_status(selected_ticket_id, new_ticket_status):
                        st.success(f"Ticket {selected_ticket_id} updated.")
                        st.rerun()

            with col_delete_tk:
                if st.button("Delete Ticket", key="ticket_delete_button"):
                    # Use service class method
                    if ticket_service.delete_ticket(selected_ticket_id):
                        st.warning(f"Ticket {selected_ticket_id} deleted.")
                        st.rerun()

    # -------------------- AI ASSISTANT TAB ----------------------------
    with tab_ai:
        st.subheader("🤖 AI Assistant (OOP Version)")

        st.write(
            "Ask questions about cyber incidents, datasets, or IT tickets.\n"
            "The assistant will give simple, clear advice."
        )

        domain = st.selectbox(
            "Choose domain for advice:",
            ["General", "Cybersecurity", "Data Science", "IT Operations"],
        )

        # Initialize AI Assistant (using service class)
        if "ai_assistant" not in st.session_state:
            try:
                st.session_state.ai_assistant = AIAssistant(
                    api_key=st.secrets["GEMINI_API_KEY"]
                )
            except Exception as e:
                st.error(f"Error initializing AI Assistant: {e}")
                st.stop()

        # Set domain
        st.session_state.ai_assistant.set_domain(domain)

        if st.button("Reset Chat"):
            st.session_state.ai_assistant.clear_history()
            st.success("Chat reset.")
            st.rerun()

        # Show conversation history
        history = st.session_state.ai_assistant.get_history()
        for msg in history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        user_input = st.chat_input("Ask a question...")

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)

            try:
                # Use AI service class method
                reply = st.session_state.ai_assistant.send_message(user_input)

                with st.chat_message("assistant"):
                    st.markdown(reply)

                st.rerun()

            except Exception as e:
                st.error(f"AI Error: {e}")


if __name__ == "__main__":
    main()