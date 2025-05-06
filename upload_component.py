import os
import streamlit as st
from text_extraction_component import extract_text

# Directory to save uploaded files
UPLOAD_DIR = "uploads"

class UploadManager:
    @staticmethod
    def save(uploaded_file: st.runtime.uploaded_file_manager.UploadedFile) -> dict:
        """
        Save the uploaded file to disk and extract its text content.
        Returns metadata with file path and extracted text.
        """
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        # Construct file path
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        # Save file bytes
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Extract text from the saved file
        text = extract_text(file_path)
        return {"path": file_path, "text": text}


def upload():
    """
    Streamlit UI component for uploading materials.
    Saves the file and stores extracted text in session state.
    """
    st.header("AI Tutor – Upload Material")
    st.write("Upload PDF, DOCX, or image")
    uploaded = st.file_uploader(
        label="Drag and drop file here",
        type=["pdf", "docx", "png", "jpg", "jpeg"],
        help="Limit 200MB per file • PDF, DOCX, PNG, JPG, JPEG"
    )
    if uploaded:
        metadata = UploadManager.save(uploaded)
        st.success(f"File saved as {metadata['path']}")
        # Store extracted text for downstream components
        st.session_state[last_key:="last_text"] = metadata["text"]
