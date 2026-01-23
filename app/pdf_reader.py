# pdf_reader.py
import pdfplumber

def read_pdf(path: str) -> str:
    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if page_text:
                text += page_text + "\n"

    return text.strip()