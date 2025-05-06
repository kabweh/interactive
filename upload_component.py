import os
import streamlit as st

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadManager:
    @staticmethod
    def save(uploaded_file):
        """
        Save the uploaded file to disk and return its path and extracted text.
        """
        # Construct file path
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        # Write file to disk
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        # Attempt text extraction if available
        extracted_text = ""
        try:
            # Import here to avoid breaking if module is missing
            from text_extraction_component import extract_text
            extracted_text = extract_text(file_path)
        except ImportError:
            # No extraction module found; skip
            extracted_text = ""
        return {"path": file_path, "text": extracted_text}


def upload():
    """
    Display a file uploader widget and handle saving uploads.
    """
    st.subheader("Upload PDF, DOCX, or image")
    uploaded_file = st.file_uploader(
        label="Drag and drop file here",
        type=["pdf", "docx", "png", "jpg", "jpeg"],
        help="Limit 200MB per file • PDF, DOCX, PNG, JPG, JPEG"
    )
    if uploaded_file:
        metadata = UploadManager.save(uploaded_file)
        st.success(f"File saved as {metadata['path']}")
        # Store extracted text for downstream components
        st.session_state["last_text"] = metadata["text"]
