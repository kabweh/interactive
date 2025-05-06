import streamlit as st
from lesson_explainer import LessonExplainer

# Try to import voice chat functionality
voice_chat_available = False
try:
    from audio_interaction import start_voice_chat, voice_enabled
    voice_chat_available = True
except ImportError:
    voice_chat_available = False


def main():
    st.title("Math Tutor")
    mode = st.sidebar.selectbox("Select difficulty level:", ["easy", "quiz"])
    
    if mode == "easy":
        text = st.text_area(
            "Enter material to explain:",
            value=st.session_state.get("last_text", "")
        )
        if st.button("Explain"):
            # Save last text
            st.session_state["last_text"] = text
            
            # Use LessonExplainer to show the explanation
            LessonExplainer().explain(text)
            
            # Attempt to start voice chat if available
            if voice_chat_available and voice_enabled:
                start_voice_chat(text)
            else:
                st.info(
                    "🔈 Audio interaction disabled.\n"
                    "To enable voice chat, install the required packages:\n"
                    "pip install streamlit-webrtc av speechrecognition"
                )

    elif mode == "quiz":
        st.write("Quiz mode coming soon...")


if __name__ == "__main__":
    main()
