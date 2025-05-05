# ai_tutor_project/streamlit_app.py
import streamlit as st
from auth_component import auth_ui
from upload_component import upload
from explanation_component import show_explanation
from quiz_component import show_quiz
from report_component import send_report

st.set_page_config(page_title="AI Tutor", layout="wide")

# --- Authentication ---
auth_ui()
if "user" not in st.session_state:
    st.stop()

# --- Sidebar Navigation ---
mode = st.sidebar.radio("Mode", ["Upload", "Explain", "Quiz", "Report"])

# Initialize state
st.session_state.setdefault("last_text", "")
st.session_state.setdefault("last_explanation", "")
st.session_state.setdefault("user_id", 1)

# --- Main Views ---
if mode == "Upload":
    upload()

elif mode == "Explain":
    # 1) Display explanation visuals
    show_explanation(st.session_state["last_text"])

    # 2) Engage in continuous voice chat
    from audio_interaction import start_voice_chat
    start_voice_chat(st.session_state["last_text"])

elif mode == "Quiz":
    show_quiz(st.session_state["last_text"])

elif mode == "Report":
    send_report()
