from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_text_input(text_input):
    return text_input.strip()
