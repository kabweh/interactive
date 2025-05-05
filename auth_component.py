import streamlit as st
import json
import os
import uuid
import hashlib

# File paths for storing users and invite codes\USERS_FILE = 'users.json'
INVITE_FILE = 'invite_codes.json'

# Utility functions

def load_data(file_path, default):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(default, f)
    with open(file_path, 'r') as f:
        return json.load(f)


def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Main authentication UI

def auth_ui():
    st.sidebar.title("Authentication")
    mode = st.sidebar.selectbox("Mode", ["Login", "Sign Up"])

    # Load existing users and invite codes
    users = load_data(USERS_FILE, [])
    invite_codes = load_data(INVITE_FILE, [])

    if mode == "Sign Up":
        st.sidebar.header("Sign Up")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        # First user gets admin rights without invite code
        if len(users) == 0:
            st.sidebar.info("First user: no invite code needed. You will be admin.")
            invite_code = None
        else:
            invite_code = st.sidebar.text_input("Invitation Code")

        if st.sidebar.button("Register"):
            if not username or not password:
                st.sidebar.error("Enter both username and password.")
            elif any(u['username'] == username for u in users):
                st.sidebar.error("Username already taken.")
            elif invite_code is None or invite_code in invite_codes:
                # Remove used invite code
                if invite_code:
                    invite_codes.remove(invite_code)
                    save_data(INVITE_FILE, invite_codes)

                # Assign role
                role = 'admin' if len(users) == 0 else 'user'
                users.append({
                    'username': username,
                    'password': hash_password(password),
                    'role': role
                })
                save_data(USERS_FILE, users)

                # Set session state
                st.session_state['user'] = {
                    'username': username,
                    'role': role
                }
                st.session_state['is_admin'] = (role == 'admin')

                st.sidebar.success("Registration successful!")
                st.experimental_rerun()
            else:
                st.sidebar.error("Invalid invitation code.")

    else:
        st.sidebar.header("Login")
        username = st.sidebar.text_input("Username", key="login_username")
        password = st.sidebar.text_input("Password", type="password", key="login_password")

        if st.sidebar.button("Login"):
            user = next(
                (u for u in users if u['username'] == username and u['password'] == hash_password(password)),
                None
            )
            if user:
                st.session_state['user'] = user
                st.session_state['is_admin'] = (user['role'] == 'admin')
                st.sidebar.success(f"Logged in as {username}")
                st.experimental_rerun()
            else:
                st.sidebar.error("Invalid credentials.")

    # Invitation code management for admin
    if st.session_state.get('is_admin'):
        st.sidebar.header("Invitation Codes (Admin)")
        if st.sidebar.button("Generate New Code"):
            new_code = str(uuid.uuid4()).split('-')[0]
            invite_codes.append(new_code)
            save_data(INVITE_FILE, invite_codes)
            st.sidebar.success(f"New invitation code: {new_code}")

        st.sidebar.subheader("Active Codes")
        if invite_codes:
            for code in invite_codes:
                st.sidebar.text(code)
        else:
            st.sidebar.write("No active codes.")
