import streamlit as st
import speech_recognition as sr
from lesson_explainer import LessonExplainer

# Try to import the WebRTC streamer
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import av
    WEBRTC_AVAILABLE = True
except ModuleNotFoundError:
    WEBRTC_AVAILABLE = False


def start_voice_chat(text: str) -> None:
    """
    If possible, starts a two‐way voice chat:
      - Streams microphone audio in
      - Runs speech recognition on it
      - Sends each transcript back through LessonExplainer
    Otherwise, shows an install hint.
    """
    if not WEBRTC_AVAILABLE:
        st.info(
            "🔈 **Audio interaction disabled.**\n\n"
            "To enable voice chat, install the required packages:\n\n"
            "```\n"
            "pip install streamlit-webrtc av\n"
            "```"
        )
        return

    # A minimal audio processor that recognizes speech and explainer responds
    class _AudioProcessor(AudioProcessorBase):
        def __init__(self):
            self.recognizer = sr.Recognizer()
            self.explainer = LessonExplainer()

        def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
            # Convert the incoming WebRTC audio frame to raw bytes
            sr_audio = sr.AudioData(
                frame.to_ndarray().tobytes(),
                frame.layout.sample_rate,
                frame.layout.sample_width
            )
            try:
                # Recognize speech (you may choose a different API/language)
                user_utterance = self.recognizer.recognize_google(sr_audio)
                # Generate an explanation for what was just said
                response_html = self.explainer.explain(user_utterance, level="medium")
                # Display it in the Streamlit app
                st.markdown(response_html, unsafe_allow_html=True)
            except sr.UnknownValueError:
                # could not parse audio
                pass
            except sr.RequestError:
                st.error("Speech recognition service is unavailable.")
            return frame

    webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=_AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )
