# ai_tutor_project/explanation_component.py
import streamlit as st
from lesson_explainer import LessonExplainer

def show_explanation(text: str):
    """
    Renders the AI‑generated, annotated explanation of `text` 
    and stores the raw explanation for TTS playback.
    """
    # Difficulty selector
    level = st.selectbox("Select difficulty level:", ["easy", "medium", "hard"])

    # Generate explanation
    explainer = LessonExplainer(api_key=st.secrets.get("MANUS_API_KEY"))
    resp = explainer.explain(text, level=level)

    # Display annotated HTML (highlights, notes, etc.)
    annotated = resp.get("annotated_html", "")
    st.markdown(annotated, unsafe_allow_html=True)

    # Save the plain explanation text for voice playback
    explanation_text = resp.get("text", "")
    st.session_state["last_explanation"] = explanation_text
