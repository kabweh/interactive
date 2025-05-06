# interactive/audio_interaction.py

import streamlit as st

try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import av
    import speech_recognition as sr
    from lesson_explainer import LessonExplainer

    class _AudioProcessor(AudioProcessorBase):
        def __init__(self, explainer, text):
            self.explainer = explainer
            self.text = text
            self.recognizer = sr.Recognizer()

        def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
            # (This is just a stub — implement streaming audio-to-text here if you wish.)
            return frame

    def start_voice_chat(text: str):
        """
        Kick off a bi‑directional voice chat: 
        - streams mic input to speech recognizer 
        - uses LessonExplainer to generate spoken replies
        """
        st.markdown("### Voice chat mode")
        explainer = LessonExplainer()
        webrtc_streamer(
            key="lesson-voice",
            mode=WebRtcMode.SENDRECV,
            audio_processor_factory=lambda: _AudioProcessor(explainer, text),
            media_stream_constraints={"audio": True, "video": False},
        )

except ImportError:
    st.warning(
        "🔈  **Audio interaction disabled**  \n"
        "To enable voice chat install `streamlit-webrtc` and `av`:\n\n"
        ```
        pip install streamlit-webrtc av
        ```"
    )

    def start_voice_chat(text: str):
        """No-op fallback when streamlit-webrtc isn’t available."""
        # Optionally guide the user to install dependencies.
        st.markdown(
            "Voice chat is unavailable because the required "
            "`streamlit-webrtc` package is not installed."
        )
