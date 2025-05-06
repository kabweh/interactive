import streamlit as st
import os
import json
import hashlib
import random
import string
from datetime import datetime

# Paths for user and invite data
USERS_FILE = "data/users.json"
INVITE_FILE = "data/invite_codes.json"

# Ensure data directory and files exist
os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)
if not os.path.exists(INVITE_FILE):
    with open(INVITE_FILE, 'w') as f:
        json.dump([], f)


def load_data(path, default):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return default


def save_data(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def gen_invite_code(length: int = 8):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def auth_ui():
    """
    Streamlit UI for user authentication and invitation management.
    """
    st.sidebar.title("Authentication")
    mode = st.sidebar.selectbox("Mode", ["Login", "Sign Up"])

    users = load_data(USERS_FILE, [])
    invite_codes = load_data(INVITE_FILE, [])

    # --- LOGIN ---
    if mode == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            hashed = hash_password(password)
            user = next((u for u in users if u['username']==username and u['password']==hashed), None)
            if user:
                st.session_state.user = user
                st.sidebar.success(f"Logged in as {username}")
            else:
                st.sidebar.error("Invalid credentials")

    # --- SIGN UP ---
    else:
        username = st.sidebar.text_input("Choose a Username")
        password = st.sidebar.text_input("Choose a Password", type="password")
        need_code = len(users) > 0
        code = None
        if need_code:
            code = st.sidebar.text_input("Invitation Code")

        if st.sidebar.button("Sign Up"):
            if not username or not password:
                st.sidebar.error("Please provide both username and password.")
            elif need_code and code not in invite_codes:
                st.sidebar.error("Invalid or missing invitation code.")
            else:
                hashed = hash_password(password)
                is_admin = len(users) == 0
                new_user = {
                    'username': username,
                    'password': hashed,
                    'admin': is_admin,
                    'joined': datetime.utcnow().isoformat()
                }
                users.append(new_user)
                save_data(USERS_FILE, users)

                # consume invite code if used
                if code:
                    invite_codes.remove(code)
                    save_data(INVITE_FILE, invite_codes)

                st.session_state.user = new_user
                st.sidebar.success(f"Signed up as {username}{' (Admin)' if is_admin else ''}")

    # --- AFTER AUTH ---
    if "user" in st.session_state:
        current = st.session_state.user
        st.sidebar.markdown("---")
        st.sidebar.write(f"**Current User:** {current['username']}{' (Admin)' if current.get('admin') else ''}")

        # Admin panel for invite codes
        if current.get('admin'):
            st.sidebar.subheader("Admin Panel")
            if st.sidebar.button("Generate Invite Code"):
                new_code = gen_invite_code()
                invite_codes.append(new_code)
                save_data(INVITE_FILE, invite_codes)
                st.sidebar.success(f"New invite code: {new_code}")

            if invite_codes:
                st.sidebar.write("**Active Codes:**")
                for c in invite_codes:
                    st.sidebar.text(c)
