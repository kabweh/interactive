import streamlit as st

# feature-flag for voice
voice_enabled = True

# Try to import WebRTC + provide a stub base if that fails
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import av
except ImportError:
    voice_enabled = False
    # stub base so class DummyAudioProcessor can always be defined
    class AudioProcessorBase:
        def __init__(self, *args, **kwargs):
            pass

# Try to import speech recognition
try:
    import speech_recognition as sr
except ImportError:
    voice_enabled = False

from lesson_explainer import LessonExplainer

class DummyAudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        return frame

def start_voice_chat(text):
    if not voice_enabled:
        return
    st.header("Voice Chat")
    st.write("Listening... speak your questions aloud.")
    webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=DummyAudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )
    LessonExplainer().explain(text)
