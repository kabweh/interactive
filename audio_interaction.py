import streamlit as st
from lesson_explainer import LessonExplainer

# Feature flags
voice_enabled = True
webrtc_available = False

# Try to import WebRTC components
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import av
    webrtc_available = True
except ImportError:
    webrtc_available = False

# Try to import speech_recognition
try:
    import speech_recognition as sr
except ImportError:
    voice_enabled = False

# Only define DummyAudioProcessor if AudioProcessorBase was imported
if webrtc_available:
    class DummyAudioProcessor(AudioProcessorBase):
        def recv(self, frame):
            return frame


def start_voice_chat(text):
    # Only proceed if both WebRTC and speech_recognition are present
    if not (webrtc_available and voice_enabled):
        return

    st.header("Voice Chat")
    st.write("Listening... speak your questions aloud.")

    webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=DummyAudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )

    # After or during the stream, you could capture audio and feed back to LessonExplainer.
    # For now we simply replay the explanation:
    LessonExplainer().explain(text)
