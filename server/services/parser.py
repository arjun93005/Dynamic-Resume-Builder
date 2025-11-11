import os
from docx import Document
from pypdf import PdfReader

"""
Enhanced parser with built-in corrupted file detection.
Implements SRS DRA-F-004 requirement.
"""
def extract_text(path: str) -> str:
    """
    Extract text from PDF/DOCX/TXT files with corruption handling.
    Returns plain text or raises ValueError("Corrupted file").
    """
    if not os.path.exists(path):
        raise FileNotFoundError("File not found")

    _, ext = os.path.splitext(path.lower())

    try:
        if ext == ".pdf":
            return _extract_pdf(path)
        elif ext in (".docx", ".doc"):
            return _extract_docx(path)
        elif ext == ".txt":
            return _extract_txt(path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    except Exception as e:
        # any decoding/parsing failure → treat as corruption
        raise ValueError(f"Corrupted or unreadable file: {str(e)}")

def _extract_pdf(path):
    reader = PdfReader(path)
    text = "\n".join([p.extract_text() or "" for p in reader.pages])
    if not text.strip():
        raise ValueError("Empty PDF file")
    return text

def _extract_docx(path):
    doc = Document(path)
    text = "\n".join([p.text for p in doc.paragraphs])
    if not text.strip():
        raise ValueError("Empty DOCX file")
    return text

def _extract_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()
    if not data.strip():
        raise ValueError("Empty TXT file")
    return data
