# from pymupdf import pymupdf
import fitz
def read_pdf(file_path):
    # reader = fitz.open(file_path)
    doc = fitz.open(file_path)
    text =""
    # for page in reader.pages:
    for page in doc:
        # page_text = page.extract_text()
        # if page_text:
            text += page.get_text()
    return text