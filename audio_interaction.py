# audio_interaction.py
import streamlit as st

voice_enabled = False
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
    import av
    import speech_recognition as sr
    voice_enabled = True
except ImportError:
    # Required packages not installed
    voice_enabled = False

from lesson_explainer import LessonExplainer

# A dummy processor for streaming audio frames
class DummyAudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        return frame


def start_voice_chat(text):
    if not voice_enabled:
        return
    st.markdown("---")
    st.header("🎙️ Voice Q&A")
    st.write("Speak your question after clicking 'Start'.")
    ctx = webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=DummyAudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )
    if ctx.audio_receiver:
        # Capture a few seconds of audio then process
        frames = []
        for _ in range(10):  # collect 10 frames
            frame = ctx.audio_receiver.get_frame()
            if frame:
                frames.append(frame.to_ndarray())
        # Convert frames to AudioData and recognize
        recognizer = sr.Recognizer()
        audio_data = sr.AudioData(b"".join([f.tobytes() for f in frames]), sample_rate=48000, sample_width=2)
        try:
            question = recognizer.recognize_google(audio_data)
            st.write(f"**You asked:** {question}")
            answer = LessonExplainer().answer_question(text, question)
            st.write(f"**Answer:** {answer}")
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand your question.")
        except sr.RequestError:
            st.error("Speech recognition service is unavailable.")
