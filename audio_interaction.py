# audio_interaction.py
import streamlit as st

# Feature flag
voice_enabled = False
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import av
    import speech_recognition as sr
    voice_enabled = True
except ImportError:
    # If any of these fail, audio interaction stays off
    voice_enabled = False

from lesson_explainer import LessonExplainer

class DummyAudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        return frame

def start_voice_chat(text: str):
    if not voice_enabled:
        return
    st.header("🎙 Voice Chat")
    st.write("Listening... please speak your questions aloud.")
    webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=DummyAudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )
    # TODO: gather audio frames, run `sr.Recognizer()` to transcribe
    # For now, re-run the explanation as a placeholder:
    LessonExplainer().explain(text)
