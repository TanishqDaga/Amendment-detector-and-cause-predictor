import pdfplumber

import fitz  # PyMuPDF

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    print(f"Total pages: {len(doc)}")

    for page in doc:
        text += page.get_text()

    return text


# TESTING
if __name__ == "__main__":
    file_path = "../sample-docs/old.pdf"
    text = extract_text(file_path)

    print("\n--- EXTRACTED TEXT ---\n")
    print(text[:100000000])