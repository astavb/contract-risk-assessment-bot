from docx import Document
from PyPDF2 import PdfReader
from langdetect import detect

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return " ".join([page.extract_text() or "" for page in reader.pages])

    elif file.name.endswith(".docx"):
        doc = Document(file)
        return " ".join([p.text for p in doc.paragraphs])

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise ValueError("Unsupported file format")

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"
