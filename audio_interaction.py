# ai_tutor_project/audio_interaction.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av
import speech_recognition as sr
from lesson_explainer import LessonExplainer
from text_to_speech import TTS

def start_voice_chat(content: str):
    """
    Begins a continuous voice interaction where the student speaks queries
    and the AI tutor responds with synthesized speech.
    """
    st.write("🔊 Voice chat initiated. Please speak your question.")

    class VoiceProcessor(AudioProcessorBase):
        def __init__(self, lesson_content: str):
            self.lesson_content = lesson_content
            self.recognizer = sr.Recognizer()

        def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
            # Convert incoming audio frame to raw PCM bytes
            pcm = frame.to_ndarray()
            audio_data = sr.AudioData(
                pcm.tobytes(),
                frame.sample_rate,
                pcm.dtype.itemsize
            )
            try:
                # Recognize student speech
                query = self.recognizer.recognize_google(audio_data)
                st.session_state["last_query"] = query

                # Generate AI response
                explainer = LessonExplainer(api_key=st.secrets.get("MANUS_API_KEY"))
                resp = explainer.explain(
                    self.lesson_content + "\nStudent asked: " + query,
                    level="medium"
                )
                answer = resp.get("text", "")
                st.session_state["last_answer"] = answer

                # Play synthesized response
                audio_bytes = TTS.synthesize(answer)
                st.audio(audio_bytes, format="audio/mp3")

            except Exception:
                # Ignore recognition errors silently
                pass

            return frame

    # Start WebRTC streamer for audio send/receive
    webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=lambda: VoiceProcessor(content)
    )