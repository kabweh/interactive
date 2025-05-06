import streamlit as st
from lesson_explainer import LessonExplainer

# Attempt to import WebRTC and speech libraries; disable if unavailable
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import speech_recognition as sr
    webrtc_available = True
except ImportError:
    webrtc_available = False


def start_voice_chat(text: str) -> None:
    """
    Start an interactive voice chat session using WebRTC and speech recognition.
    If WebRTC isn't installed, inform the user and skip audio.

    Args:
        text: The initial lesson text (unused placeholder for compatibility).
    """
    if not webrtc_available:
        st.warning("Voice chat is unavailable because 'streamlit-webrtc' is not installed.")
        return

    explainer = LessonExplainer()

    class VoiceChatProcessor(AudioProcessorBase):
        def __init__(self):
            self.recognizer = sr.Recognizer()

        def recv(self, frame):
            # Convert incoming audio frame to raw bytes
            audio_frame = frame.to_ndarray()
            raw_bytes = audio_frame.tobytes()
            # Build AudioData for recognition
            try:
                audio_data = sr.AudioData(raw_bytes, frame.sample_rate, audio_frame.dtype.itemsize)
                user_query = self.recognizer.recognize_google(audio_data)
                # Generate and display explanation for spoken input
                explanation_html = explainer.explain(user_query)
                st.markdown(explanation_html, unsafe_allow_html=True)
            except Exception:
                # Ignore unrecognized speech or errors
                pass
            return frame

    # Launch WebRTC streamer for bidirectional audio
    webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=VoiceChatProcessor,
    )
