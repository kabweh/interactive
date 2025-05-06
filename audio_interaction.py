import streamlit as st

voice_enabled = True
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import av
except ImportError:
    voice_enabled = False

try:
    import speech_recognition as sr
except ImportError:
    voice_enabled = False

from lesson_explainer import LessonExplainer

class DummyAudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        return frame

def start_voice_chat(text: str):
    """Open a WebRTC audio channel and then re‑explain via speech_recognition."""
    if not voice_enabled:
        return

    st.header("🎤 Voice Chat")
    st.write("Listening… ask your questions aloud.")
    webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=DummyAudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )
    # (Here you’d collect and transcribe the audio frames via `speech_recognition`,
    # then feed follow‑up questions back into LessonExplainer. This is stubbed for now.)
    LessonExplainer().explain(text)
