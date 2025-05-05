import os
import json
import secrets
import streamlit as st

# --- File paths ---
DATA_FOLDER = "data"
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
INVITE_FILE = os.path.join(DATA_FOLDER, "invite_codes.json")

# Ensure data directory exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# --- Data helpers ---
def load_data(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default
    return default


def save_data(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# --- Authentication UI ---
def auth_ui():
    st.sidebar.title("🛡️ Authentication")
    mode = st.sidebar.selectbox("Mode", ["Login", "Sign Up"])

    # Load existing data
    users = load_data(USERS_FILE, [])
    invite_codes = load_data(INVITE_FILE, [])

    if mode == "Sign Up":
        st.sidebar.subheader("Create an account")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        code = st.sidebar.text_input("Invitation Code (leave blank if first user)")

        if st.sidebar.button("Sign Up"):
            # First user becomes admin without code
            if not users:
                is_admin = True
            else:
                # Validate invitation code
                if code in invite_codes:
                    is_admin = False
                    invite_codes.remove(code)
                    save_data(INVITE_FILE, invite_codes)
                else:
                    st.sidebar.error("Invalid invitation code.")
                    st.stop()

            # Check for duplicate username
            if any(u["username"] == username for u in users):
                st.sidebar.error("Username already exists.")
            else:
                # Save new user
                users.append({
                    "username": username,
                    "password": password,
                    "admin": is_admin
                })
                save_data(USERS_FILE, users)
                st.sidebar.success("Account created! Please log in.")
                st.experimental_rerun()

    else:
        st.sidebar.subheader("Login to your account")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            # Authenticate
            for user in users:
                if user["username"] == username and user["password"] == password:
                    st.session_state["user"] = user
                    st.sidebar.success("Logged in successfully.")
                    break
            else:
                st.sidebar.error("Invalid username or password.")
                st.stop()

    # If logged in, show user info and admin panel
    if "user" in st.session_state:
        user = st.session_state["user"]
        st.sidebar.markdown(f"**Logged in as:** {user['username']}")

        if user.get("admin"):
            st.sidebar.subheader("🔑 Invitation Codes")
            if st.sidebar.button("Generate New Code"):
                new_code = secrets.token_urlsafe(8)
                invite_codes.append(new_code)
                save_data(INVITE_FILE, invite_codes)
            st.sidebar.write(invite_codes)

        if st.sidebar.button("Logout"):
            del st.session_state['user']
            st.experimental_rerun()
