"""
Module: Ingestion & File Management
Description: Scans the input directory for incoming invoices, validates formats,
             manages folder structures, and handles safe file archiving.
"""

import os
import shutil
import logging
from datetime import datetime

# Configure operational logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("IngestionModule")

# Define standard folder architecture for the pipeline
FOLDERS = {
    "input": "input_invoices",
    "processed": "processed_invoices",
    "failed": "failed_invoices"
}

def initialize_directories():
    """Ensure all necessary pipeline directories exist on disk."""
    for folder_path in FOLDERS.values():
        os.makedirs(folder_path, exist_ok=True)
    logger.info("Pipeline directory structure verified/initialized.")

def fetch_pending_invoices():
    """
    Scan the input directory and return a list of valid invoice files.
    Supports PDF, text, and common image formats.
    """
    initialize_directories()
    supported_extensions = (".pdf", ".txt", ".jpg", ".jpeg", ".png", ".tiff")
    
    try:
        files = [
            f for f in os.listdir(FOLDERS["input"])
            if f.lower().endswith(supported_extensions) and not f.startswith('.')
        ]
        logger.info(f"Found {len(files)} pending invoice(s) for processing.")
        return files
    except Exception as e:
        logger.error(f"Failed to scan input directory: {e}")
        return []

if __name__ == "__main__":
    print("Initializing Ingestion Module...")
    initialize_directories()
    pending_files = fetch_pending_invoices()
    print(f"Success! Detected {len(pending_files)} files ready for the pipeline.")
    print("Files found:", pending_files)