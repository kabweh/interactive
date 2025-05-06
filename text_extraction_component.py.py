import os
from typing import Optional

import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
import docx


def extract_text(file_path: str) -> str:
    """
    Extract plain text from PDF, DOCX, or image files.

    Args:
        file_path: Path to the input file

    Returns:
        Extracted text as a string.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text_chunks = []

    if ext == ".pdf":
        # Extract text from each page of the PDF
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

    elif ext == ".docx":
        # Extract text from DOCX paragraphs
        document = docx.Document(file_path)
        for para in document.paragraphs:
            if para.text:
                text_chunks.append(para.text)

    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"]:
        # OCR for image files
        try:
            image = Image.open(file_path)
            ocr_text = pytesseract.image_to_string(image)
            text_chunks.append(ocr_text)
        except Exception as e:
            raise RuntimeError(f"OCR extraction failed: {e}")

    else:
        raise ValueError(f"Unsupported file type for text extraction: {ext}")

    # Combine all chunks into a single string
    return "\n".join(text_chunks)
