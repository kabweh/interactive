# ai_tutor_project/auth_component.py
import streamlit as st
from auth_manager import AuthManager

def auth_ui():
    """
    Renders the invite‑only login/signup UI in the sidebar.
    """
    st.sidebar.title("Secure Access")
    mode = st.sidebar.radio("Action", ["Login", "Sign Up"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if mode == "Login":
        if st.sidebar.button("Log In"):
            if AuthManager.login(email, password):
                st.session_state["user"] = email
                st.success(f"Logged in as {email}")
            else:
                st.error("Invalid credentials")

    else:  # Sign Up flow
        invite_code = st.sidebar.text_input("Invite Code")
        if st.sidebar.button("Sign Up"):
            if AuthManager.invite_only_signup(email, invite_code):
                st.success("Signup successful! Please log in.")
            else:
                st.error("Invalid invite code or email")
