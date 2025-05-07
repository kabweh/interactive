# audio_interaction.py
import streamlit as st

# Feature flag + safe‐fallback for AudioProcessorBase
voice_enabled = False
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import av
    import speech_recognition as sr
    voice_enabled = True
except ImportError:
    # define a dummy base so the class below won’t NameError
    class AudioProcessorBase:
        pass

from lesson_explainer import LessonExplainer

class DummyAudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        return frame

def start_voice_chat(text: str):
    if not voice_enabled:
        return
    st.header("🎙 Voice Chat")
    st.write("Listening... speak your questions aloud.")
    webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=DummyAudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )
    # (When you implement transcription, grab frames here and use sr.Recognizer().)
    LessonExplainer().explain(text)
