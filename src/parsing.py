# src/parsing.py
import fitz  # PyMuPDF
from docx import Document
from pathlib import Path


def parse_pdf(path):
    doc = fitz.open(path)
    text = "\n".join(page.get_text("text") for page in doc)
    doc.close()
    return text


def parse_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def parse_file(path):
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        return parse_pdf(path)
    if p.suffix.lower() == ".docx":
        return parse_docx(path)
    return Path(path).read_text(encoding="utf-8", errors="ignore")
