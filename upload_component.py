# ai_tutor_project/upload_component.py
import streamlit as st
from upload_manager import UploadManager

def upload():
    """
    Renders the upload UI and handles saving and parsing of uploaded materials.
    """
    st.title("AI Tutor – Upload Material")
    uploaded = st.file_uploader(
        "Upload PDF, DOCX, or image",
        type=["pdf", "docx", "png", "jpg", "jpeg"]
    )
    if uploaded:
        metadata = UploadManager.save(uploaded)
        st.success(f"File saved as {metadata['path']}")
        # Store extracted text for downstream use
        st.session_state["last_text"] = metadata["text"]
