"""
Module: OCR & Text Extraction
Description: Handles multi-format text extraction supporting plain text files,
             scanned images via Tesseract OCR, and PDF documents.
"""

import os
import logging
import pytesseract
import pdfplumber
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

logger = logging.getLogger("IngestionModule") # Reusing our pipeline logger

def extract_text_from_txt(file_path):
    """Read raw text directly from a .txt file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading text file {file_path}: {e}")
        return ""

def extract_text_from_image(file_path):
    """Extract text from image formats (JPG, JPEG, PNG) using Tesseract OCR."""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"OCR failed for image {file_path}: {e}")
        return ""

def extract_text_from_pdf(file_path):
    """Extract text from PDF documents using pdfplumber."""
    text_accumulator = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_accumulator.append(page_text)
        return "\n".join(text_accumulator)
    except Exception as e:
        logger.error(f"Failed to parse PDF {file_path}: {e}")
        return ""

def extract_content(file_path):
    """
    Unified router that determines file type and calls the appropriate
    extraction method.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".txt":
        return extract_text_from_txt(file_path)
    elif ext in [".jpg", ".jpeg", ".png", ".tiff"]:
        return extract_text_from_image(file_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    else:
        logger.warning(f"Unsupported file format encountered: {ext}")
        return ""

if __name__ == "__main__":
    print("Testing OCR Extraction Module...")
    # Automatically grab the first available file from input_invoices to test
    input_dir = "input_invoices"
    if os.path.exists(input_dir):
        files = os.listdir(input_dir)
        if files:
            test_file = os.path.join(input_dir, files[0])
            print(f"Testing extraction on: {files[0]}")
            sample_text = extract_content(test_file)
            print(f"\n--- Extracted Text Result ---\n{sample_text[:300]}...\n-----------------------------")
        else:
            print("No files found inside input_invoices folder.")
    else:
        print("input_invoices folder not found.")