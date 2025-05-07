# streamlit_app.py
import streamlit as st
from lesson_explainer import LessonExplainer
from audio_interaction import start_voice_chat, voice_enabled

# --- Session-state defaults ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "last_text" not in st.session_state:
    st.session_state.last_text = ""

# Simple in-memory credentials (for demo purposes)
USERS = {"student": "password123"}

def login():
    st.title("🔒 Login to Math Tutor")
    st.write("Please sign in to continue.")
    username = st.text_input("Username", key="_login_username")
    password = st.text_input("Password", type="password", key="_login_password")
    if st.button("Login"):
        if USERS.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials.")


def app_interface():
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    mode = st.sidebar.selectbox("Select mode:", ["Upload & Explain", "Quiz"])

    if mode == "Upload & Explain":
        st.header("📄 Upload and Explain Material")
        uploaded_file = st.file_uploader("Choose a text file", type=["txt", "md"]);
        if uploaded_file:
            text = uploaded_file.read().decode("utf-8")
            st.text_area("Material Preview", text, height=200)
            if st.button("Explain"):
                st.session_state.last_text = text
                explainer = LessonExplainer()
                explanation = explainer.explain(text)
                st.markdown("### Explanation")
                st.write(explanation)
                if voice_enabled:
                    start_voice_chat(text)
                else:
                    st.info(
                        "🔈 Audio disabled. To enable, install:"
                        " pip install streamlit-webrtc av speechrecognition"
                    )
    else:
        st.header("📝 Quiz Mode")
        text = st.session_state.last_text
        if not text:
            st.warning("Please upload and explain some material first.")
        else:
            if st.button("Generate Quiz"):
                explainer = LessonExplainer()
                quiz_questions = explainer.generate_quiz(text)
                st.markdown("### Quiz Questions")
                for i, q in enumerate(quiz_questions, 1):
                    st.write(f"**Q{i}.** {q}")


def main():
    if not st.session_state.logged_in:
        login()
    else:
        app_interface()

if __name__ == "__main__":
    main()


# audio_interaction.py
import streamlit as st

voice_enabled = False
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import av
    import speech_recognition as sr
    voice_enabled = True
except ImportError:
    # Required packages not installed
    voice_enabled = False

from lesson_explainer import LessonExplainer

# A dummy processor for streaming audio frames
class DummyAudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        return frame


def start_voice_chat(text):
    if not voice_enabled:
        return
    st.markdown("---")
    st.header("🎙️ Voice Q&A")
    st.write("Speak your question after clicking 'Start'.")
    ctx = webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=DummyAudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )
    if ctx.audio_receiver:
        # Capture a few seconds of audio then process
        frames = []
        for _ in range(10):  # collect 10 frames
            frame = ctx.audio_receiver.get_frame()
            if frame:
                frames.append(frame.to_ndarray())
        # Convert frames to AudioData and recognize
        recognizer = sr.Recognizer()
        audio_data = sr.AudioData(b"".join([f.tobytes() for f in frames]), sample_rate=48000, sample_width=2)
        try:
            question = recognizer.recognize_google(audio_data)
            st.write(f"**You asked:** {question}")
            answer = LessonExplainer().answer_question(text, question)
            st.write(f"**Answer:** {answer}")
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand your question.")
        except sr.RequestError:
            st.error("Speech recognition service is unavailable.")
