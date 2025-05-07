# streamlit_app.py
import streamlit as st
from lesson_explainer import LessonExplainer
from audio_interaction import start_voice_chat, voice_enabled

# --- Session-state defaults ---
if "users" not in st.session_state:
    st.session_state["users"] = {}           # username -> password
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "last_text" not in st.session_state:
    st.session_state["last_text"] = ""

def signup():
    st.header("Sign Up")
    new_user = st.text_input("Choose a username", key="su_user")
    new_pass = st.text_input("Choose a password", type="password", key="su_pass")
    if st.button("Create Account"):
        if new_user in st.session_state["users"]:
            st.error("That username is already taken.")
        else:
            st.session_state["users"][new_user] = new_pass
            st.success("Account created! Please log in.")

def login():
    st.header("Log In")
    user = st.text_input("Username", key="li_user")
    pwd = st.text_input("Password", type="password", key="li_pass")
    if st.button("Log In"):
        if st.session_state["users"].get(user) == pwd:
            st.session_state["authenticated"] = True
            st.success("Logged in!")
        else:
            st.error("Invalid credentials.")

def tutor_mode():
    st.header("📚 Lesson Explainer")
    upload = st.file_uploader("Upload a text file to explain:", type=["txt", "pdf"])
    if upload:
        raw = upload.read().decode("utf-8")
    else:
        raw = st.text_area("Or paste text here:", value=st.session_state["last_text"])
    if st.button("Explain"):
        st.session_state["last_text"] = raw
        LessonExplainer().explain(raw)
        if voice_enabled:
            start_voice_chat(raw)
        else:
            st.info(
                "🔈 Audio interaction disabled.\n"
                "To enable voice chat, install:\n"
                "`pip install streamlit-webrtc av speechrecognition`"
            )

def quiz_mode():
    st.header("📝 Quiz Generator")
    text = st.text_area("Paste the material for quiz generation here:")
    if st.button("Generate Quiz"):
        quiz = LessonExplainer().generate_quiz(text)
        st.write(quiz)

def main_app():
    page = st.sidebar.selectbox("Mode", ["Lesson Explainer", "Quiz"])
    if page == "Lesson Explainer":
        tutor_mode()
    else:
        quiz_mode()

def main():
    st.title("🔢 Math Tutor")
    if not st.session_state["authenticated"]:
        choice = st.sidebar.radio("Account", ["Log In", "Sign Up"])
        if choice == "Sign Up":
            signup()
        else:
            login()
    else:
        main_app()

if __name__ == "__main__":
    main()
