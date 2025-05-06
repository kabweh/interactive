import streamlit as st
from lesson_explainer import LessonExplainer

# Try to import voice chat functionality
voice_chat_available = False
try:
    from audio_interaction import start_voice_chat, voice_enabled
    voice_chat_available = True
except ImportError:
    voice_chat_available = False

def main():
    st.set_page_config(page_title="Math Tutor", layout="wide")
    st.title("📚 Math Tutor")

    # --- Simple in‑session login / sign‑up ---
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        choice = st.sidebar.selectbox("Account", ["Login", "Sign Up"])
        user = st.sidebar.text_input("Username")
        pwd  = st.sidebar.text_input("Password", type="password")

        if choice == "Sign Up":
            if st.sidebar.button("Create Account"):
                st.session_state.username = user
                st.session_state.password = pwd
                st.session_state.logged_in = True
                st.success(f"Account created. Logged in as {user}")
        else:
            if st.sidebar.button("Login"):
                if user == st.session_state.get("username") and pwd == st.session_state.get("password"):
                    st.session_state.logged_in = True
                    st.success(f"Welcome back, {user}!")
                else:
                    st.error("❌ Invalid username or password")
        return  # stop here until logged in

    # --- Once logged in, choose mode ---
    mode = st.sidebar.selectbox("Mode", ["Upload Material", "Easy Explain", "Quiz"])

    # 1) Upload page
    if mode == "Upload Material":
        uploaded = st.file_uploader("Upload lesson material (TXT or PDF):", type=["txt","pdf"])
        if uploaded:
            try:
                raw = uploaded.read().decode("utf-8")
            except Exception:
                import io, PyPDF2
                reader = PyPDF2.PdfReader(io.BytesIO(uploaded.read()))
                raw = "\n\n".join(p.extract_text() or "" for p in reader.pages)
            st.session_state.material = raw
            st.success("✅ Material loaded into session.")

    # 2) Easy explanation
    elif mode == "Easy Explain":
        default = st.session_state.get("material", "")
        text = st.text_area("Enter or edit material to explain:", value=default, height=200)
        if st.button("Explain"):
            st.session_state["last_text"] = text
            LessonExplainer().explain(text)

            if voice_chat_available and voice_enabled:
                start_voice_chat(text)
            else:
                st.info(
                    "🔈 Audio interaction disabled.\n"
                    "To enable voice chat, install:\n"
                    "`pip install streamlit-webrtc av speechrecognition`"
                )

    # 3) Quiz mode
    else:  # mode == "Quiz"
        st.header("🔎 Quiz Mode (Coming Soon)")
        st.write("Select or create interactive math quizzes here.")

if __name__ == "__main__":
    main()
