"""
Refactored login page using OOP principles.
Uses AuthManager service class for authentication.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

st.set_page_config(
    page_title="Intelligence Platform - Login",
    page_icon="🔒",
    layout="centered"
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Multi-Domain Intelligence Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Week 11 - OOP Refactored Version</p>", unsafe_allow_html=True)
st.markdown("---")

# Initialize services
db_manager = DatabaseManager()
auth_manager = AuthManager(db_manager)

# If already logged in, show option to go to dashboard
if st.session_state.logged_in:
    st.success(f"You are already logged in as **{st.session_state.username}**")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Go to Dashboard", type="primary", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
    st.stop()

# Create tabs for login and register
tab_login, tab_register = st.tabs(["Login", "Register"])

# Login tab
with tab_login:
    st.subheader("Login to your account")

    with st.form("login_form"):
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_login = st.form_submit_button("Log In", type="primary", use_container_width=True)

        if submit_login:
            if not login_username or not login_password:
                st.error("Please enter both username and password")
            else:
                # Use AuthManager service class
                success, user, message = auth_manager.login_user(login_username, login_password)

                if success:
                    # Set session state with user data
                    st.session_state.logged_in = True
                    st.session_state.username = user.get_username()
                    st.session_state.user_role = user.get_role()

                    st.success(f"Welcome back, {user.get_username()}!")

                    # Show user info (for demonstration of OOP)
                    with st.expander("User Details (OOP)"):
                        st.write(f"**User Object:** {user}")
                        st.write(f"**Username:** {user.get_username()}")
                        st.write(f"**Role:** {user.get_role()}")
                        st.write(f"**Is Admin:** {user.is_admin()}")

                    # Redirect to dashboard
                    st.switch_page("pages/1_Dashboard.py")

                else:
                    st.error(f"Login failed: {message}")

# Register tab
with tab_register:
    st.subheader("Create new account")

    with st.form("register_form"):
        new_username = st.text_input("Choose a username", key="register_username")
        new_password = st.text_input("Choose a password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

        # Display password requirements
        with st.expander("Password Requirements"):
            st.write("- At least 6 characters")
            st.write("- Maximum 50 characters")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_register = st.form_submit_button("Create Account", type="primary", use_container_width=True)

        if submit_register:
            # Validation
            if not new_username or not new_password:
                st.error("Please fill in all fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                # Use AuthManager service class for registration
                success, message = auth_manager.register_user(new_username, new_password)

                if success:
                    st.success("Account created successfully!")
                    st.info("Please go to the Login tab to sign in with your new account")
                else:
                    st.error(f"Registration failed: {message}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Multi-Domain Intelligence Platform | CST1510 Coursework - Week 11 OOP</p>",
    unsafe_allow_html=True
)