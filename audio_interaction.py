import streamlit as st
from lesson_explainer import LessonExplainer

# Feature flag
voice_enabled = True

# Attempt to import WebRTC and speech recognition libraries
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import av
except ImportError:
    voice_enabled = False

try:
    import speech_recognition as sr
except ImportError:
    voice_enabled = False


# Simple AudioProcessor stub
class DummyAudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        return frame


def start_voice_chat(text):
    if not voice_enabled:
        return

    st.header("Voice Chat")
    st.write("Listening... speak your questions aloud.")

    # Start the WebRTC audio stream
    webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=DummyAudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )

    # (Here you could hook up speech_recognition to captured frames and
    # feed questions back into LessonExplainer.)

    # For now, just replay the explanation once the stream starts
    LessonExplainer().explain(text)
