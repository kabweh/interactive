import streamlit as st
from lesson_explainer import LessonExplainer

# Detect optional dependencies
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ModuleNotFoundError:
    SR_AVAILABLE = False

try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import av
    WEBRTC_AVAILABLE = True
except ModuleNotFoundError:
    WEBRTC_AVAILABLE = False


def start_voice_chat(text: str) -> None:
    """
    Launch a two-way voice chat if dependencies are present.

    Args:
        text: The initial lesson text (unused for now, but kept for signature consistency).
    """
    # If either speech_recognition or WebRTC is missing, show install instructions
    if not WEBRTC_AVAILABLE or not SR_AVAILABLE:
        missing = []
        if not WEBRTC_AVAILABLE:
            missing.append("streamlit-webrtc av")
        if not SR_AVAILABLE:
            missing.append("speechrecognition")
        st.info(
            "🔈 **Audio interaction disabled.**\n\n"
            "To enable voice chat, install the required packages:\n\n"
            "```\n"
            f"pip install {' '.join(missing)}\n"
            "```"
        )
        return

    class _AudioProcessor(AudioProcessorBase):
        """Processes incoming audio, does speech-to-text, and responds via LessonExplainer."""
        def __init__(self):
            self.recognizer = sr.Recognizer()
            self.explainer = LessonExplainer()

        def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
            # Convert WebRTC audio frame to SpeechRecognition AudioData
            pcm = frame.to_ndarray().T
            audio_data = sr.AudioData(
                pcm.tobytes(),
                frame.layout.sample_rate,
                frame.layout.sample_width
            )
            try:
                # Attempt recognition
                user_utterance = self.recognizer.recognize_google(audio_data)
                # Generate an explanation on-the-fly
                response_html = self.explainer.explain(user_utterance, level="medium")
                st.markdown(response_html, unsafe_allow_html=True)
            except sr.UnknownValueError:
                # Couldn't understand audio
                pass
            except sr.RequestError:
                st.error("Speech recognition service is unavailable.")
            return frame

    # Launch the WebRTC component
    webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=_AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )
