import streamlit as st
import os
import json
import datetime
from pathlib import Path

# Directories and files for storing materials and metadata
MATERIALS_DIR = "data/materials"
MATERIALS_FILE = "data/materials.json"

class UploadManager:
    """
    Manages saving uploaded files and recording metadata.
    """
    @staticmethod
    def save(uploaded_file):
        # Ensure directories exist
        os.makedirs(MATERIALS_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(MATERIALS_FILE), exist_ok=True)

        # Load existing metadata
        try:
            with open(MATERIALS_FILE, "r") as f:
                materials = json.load(f)
        except FileNotFoundError:
            materials = []

        # Generate a unique filename to prevent collisions
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        safe_name = f"{timestamp}_{uploaded_file.name}"
        save_path = os.path.join(MATERIALS_DIR, safe_name)

        # Save the file to disk
        with open(save_path, "wb") as out_file:
            out_file.write(uploaded_file.getbuffer())

        # Record metadata
        uploader = st.session_state.get("user", {}).get("username", "unknown")
        material_entry = {
            "original_name": uploaded_file.name,
            "stored_name": safe_name,
            "uploaded_at": datetime.datetime.now().isoformat(),
            "uploader": uploader,
            "path": save_path
        }
        materials.append(material_entry)

        # Persist metadata
        with open(MATERIALS_FILE, "w") as f:
            json.dump(materials, f, indent=2)

        return material_entry


def upload():
    """
    Streamlit component to handle file uploads.
    """
    st.header("Upload Material")
    st.write("Upload PDF, DOCX, or image")
    uploaded_files = st.file_uploader(
        "Drag and drop file here",
        type=["pdf", "docx", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="file_upload"
    )

    if uploaded_files:
        for uploaded in uploaded_files:
            try:
                metadata = UploadManager.save(uploaded)
                st.success(f"Saved '{metadata['original_name']}' successfully.")
            except Exception as e:
                st.error(f"Error saving '{uploaded.name}': {str(e)}")
