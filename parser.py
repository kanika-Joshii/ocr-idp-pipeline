"""
Module: Parser & Structured Data Extraction
Description: Uses regular expressions and text pattern matching to extract
             key entities (Invoice Number, Date, Total, Vendor) from raw OCR text.
"""

import re
import logging

logger = logging.getLogger("IngestionModule")

def parse_invoice_text(raw_text):
    """
    Extract structured fields from raw OCR/document text using robust regex patterns.
    """
    structured_data = {
        "invoice_number": None,
        "date": None,
        "total_amount": None,
        "vendor_name": None
    }

    if not raw_text:
        return structured_data

    # 1. Extract Invoice Number (Looking for common patterns like INV-1234, Invoice #, etc.)
    inv_match = re.search(r'(?:invoice\s*(?:no|number|#)?[:\-]?\s*)([A-Z0-9\-_]+)', raw_text, re.IGNORECASE)
    if inv_match:
        structured_data["invoice_number"] = inv_match.group(1)

    # 2. Extract Date (Looking for standard date formats like YYYY-MM-DD or DD/MM/YYYY)
    date_match = re.search(r'\b(?:\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4})\b', raw_text)
    if date_match:
        structured_data["date"] = date_match.group(0)

    # 3. Extract Total Amount (Looking for currency symbols followed by numbers)
    total_match = re.search(r'(?:total|amount\s*due|balance)[:\-]?\s*[\$€£]?\s*([\d,]+\.\d{2})', raw_text, re.IGNORECASE)
    if total_match:
        structured_data["total_amount"] = total_match.group(1)

    # 4. Fallback Vendor identification (Grab the first meaningful line or header)
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    if lines:
        structured_data["vendor_name"] = lines[0] # Typically the company header

    return structured_data

if __name__ == "__main__":
    print("Testing Parser Module...")
    sample_ocr_text = """
    Global Shipping Service Inc.
    123 Logistics Way, Paris, France
    
    Invoice #: INV-2026-9981
    Date: 2026-10-05
    
    Description                  Qty    Price
    Express Freight Service       1     450.00
    
    Total Due: $450.00
    """
    
    parsed_result = parse_invoice_text(sample_ocr_text)
    print("Extracted Structured Data:")
    for key, value in parsed_result.items():
        print(f"  - {key}: {value}")