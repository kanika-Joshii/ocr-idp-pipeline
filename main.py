"""
Module: Pipeline Orchestrator (main.py)
Description: Ties together ingestion, OCR extraction, parsing, and file archiving
             into an end-to-end automated pipeline workflow.
"""

import os
import shutil
import json
import logging
from datetime import datetime

# Import our modular components
from ocr import extract_content
from parser import parse_invoice_text

# Configure master logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("MasterPipeline")

# Define directories
INPUT_DIR = "input_invoices"
PROCESSED_DIR = "processed_invoices"
FAILED_DIR = "failed_invoices"
OUTPUT_JSON_DIR = "extracted_outputs"

def run_pipeline():
    print("Initializing End-to-End OCR Invoice Pipeline...")
    logger.info("Pipeline execution started.")

    # Ensure output directories exist
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)
    os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)

    if not os.path.exists(INPUT_DIR):
        logger.error(f"Input directory '{INPUT_DIR}' not found.")
        print(f"Error: {INPUT_DIR} folder missing.")
        return

    files = os.listdir(INPUT_DIR)
    if not files:
        print("No files found in input_invoices to process.")
        return

    print(f"Found {len(files)} files to process through the pipeline.\n")

    success_count = 0
    failure_count = 0

    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        
        # Skip directories if any exist inside input
        if os.path.isdir(file_path):
            continue

        print(f"Processing file: {filename}...")
        logger.info(f"Processing file: {filename}")

        try:
            # Step A: Extract Raw Text (using ocr.py module)
            raw_text = extract_content(file_path)
            
            if not raw_text.strip():
                raise ValueError("Extracted text was empty or unreadable.")

            # Step B: Parse Structured Data (using parser.py module)
            structured_data = parse_invoice_text(raw_text)
            structured_data["source_file"] = filename
            structured_data["processed_at"] = datetime.now().isoformat()

            # Step C: Save structured data as JSON
            json_filename = os.path.splitext(filename)[0] + ".json"
            json_output_path = os.path.join(OUTPUT_JSON_DIR, json_filename)
            with open(json_output_path, "w", encoding="utf-8") as jf:
                json.dump(structured_data, jf, indent=4)

            # Step D: Archive file to processed_invoices folder
            destination_path = os.path.join(PROCESSED_DIR, filename)
            shutil.move(file_path, destination_path)
            
            print(f"  -> Success! Archived to '{PROCESSED_DIR}' and JSON generated.")
            logger.info(f"Successfully processed and archived {filename}")
            success_count += 1

        except Exception as e:
            logger.error(f"Failed to process {filename}: {e}")
            print(f"  -> Error: {e}. Moving to '{FAILED_DIR}'.")
            
            # Move failed file to failed folder
            fail_dest = os.path.join(FAILED_DIR, filename)
            if os.path.exists(file_path):
                shutil.move(file_path, fail_dest)
            failure_count += 1

    print("\n--- Pipeline Execution Summary ---")
    print(f"Total Files Processed: {len(files)}")
    print(f"Successful: {success_count}")
    print(f"Failed/Archived: {failure_count}")
    print(f"Structured JSON results saved in '{OUTPUT_JSON_DIR}/'.")
    logger.info(f"Pipeline finished. Success: {success_count}, Failed: {failure_count}")

if __name__ == "__main__":
    run_pipeline()