import os

from docx import Document
from PyPDF2 import PdfReader


def extract_text(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError("File not found")
    _, ext = os.path.splitext(path.lower())
    if ext == ".pdf":
        return _extract_pdf(path)
    elif ext in (".docx", ".doc"):
        return _extract_docx(path)
    elif ext == ".txt":
        return _extract_txt(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _extract_pdf(path):
    reader = PdfReader(path)
    return "\n".join([p.extract_text() or "" for p in reader.pages])


def _extract_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def _extract_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
