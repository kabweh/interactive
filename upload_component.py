import os
import streamlit as st
from text_extraction_component import extract_text

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadManager:
    """
    Handles saving uploaded files and extracting text from them.
    """
    @staticmethod
    def save(uploaded_file) -> dict:
        """
        Save the uploaded file to disk and extract its text.

        Args:
            uploaded_file: The file-like object returned by Streamlit's file_uploader.

        Returns:
            A dict with 'path' (str) to the saved file and 'text' (str) extracted.
        """
        # Save file
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract text (PDF, DOCX, image)
        try:
            text = extract_text(file_path)
        except Exception as e:
            st.error(f"Error extracting text: {e}")
            text = ""

        return {"path": file_path, "text": text}


def upload():
    """
    Streamlit UI component to upload a material and save it.
    """
    st.title("AI Tutor – Upload Material")
    uploaded = st.file_uploader(
        "Upload PDF, DOCX, or image",
        type=["pdf", "docx", "png", "jpg", "jpeg"],
        help="Limit 200MB per file • PDF, DOCX, PNG, JPG, JPEG",
        accept_multiple_files=False
    )
    if uploaded:
        metadata = UploadManager.save(uploaded)
        st.success(f"File saved as {metadata['path']}")
        # Store extracted text for downstream use
        st.session_state["last_text"] = metadata["text"]
        return metadata
    return None
