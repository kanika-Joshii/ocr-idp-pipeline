# Modular Intelligent Document Processing (IDP) Pipeline

An automated, modular pipeline designed to ingest, scan via OCR, parse, and structure data from complex PDF invoices into clean, organized JSON formats. Built as a portfolio project for Data Science and Data Analyst roles.

---

## 🚀 Project Overview
Manual data extraction from invoices is slow and error-prone. This pipeline automates the end-to-end extraction workflow:
1. **Ingestion & Validation**: Scans incoming directories, validates file formats, manages folder structures, and safely archives processed documents.
2. **OCR Engine**: Extracts raw text blocks and layout details utilizing Tesseract-OCR and PDF utility tools.
3. **Regex Data Parsing**: Applies robust regular expressions to isolate key-value pairs such as invoice numbers, dates, line items, and totals.
4. **Structured Output**: Exports clean, standardized JSON files ready for downstream database ingestion or analytics.

---

## 🛠️ Tech Stack
* **Language**: Python 3.10+
* **OCR & PDF Processing**: `pytesseract`, `pdfplumber`
* **Text Extraction & Manipulation**: `regex`, `os`, `shutil`, `logging`
* **Version Control**: Git & GitHub

---

## 📁 Project Structure
```text
OCR_invoice_pipeline/
│
├── ingest.py          # Handles file monitoring, validation, and safe archiving
├── ocr.py             # Executes Tesseract-OCR and extracts raw text layouts
├── parser.py          # Parses raw text using regex patterns to extract fields
├── main.py            # Orchestrates the end-to-end modular pipeline workflow
├── extracted_outputs/ # Stores structured JSON outputs for each processed invoice
└── logs/              # Operational execution logs

⚙️ Setup and Installation
Clone the Repository:

git clone [https://github.com/kanika-Joshii/ocr-idp-pipeline.git](https://github.com/kanika-Joshii/ocr-idp-pipeline.git)
cd ocr-idp-pipeline

Install Dependencies:
Make sure you have Python installed, then install the required libraries:

pip install pytesseract pdfplumber

Run the Pipeline:
Execute the main controller script to process documents:

python main.py

Sample Output
Processed invoice data is serialized into clean JSON files under the extracted_outputs/ directory, structured like this:

JSON
{
  "invoice_number": "X51005255805",
  "date": "2026-03-15",
  "total_amount": "$1,250.00",
  "line_items": [...]
}
AUTHOR
Kanika Joshi
