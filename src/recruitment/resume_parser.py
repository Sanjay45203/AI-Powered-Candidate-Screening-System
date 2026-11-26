from pathlib import Path
from pypdf import PdfReader

def extract_resume_text(file_path: str) -> str:
    path = Path(file_path)
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages).strip()
    raise ValueError("Only PDF and TXT resumes are supported.")

def parse_resume(file_path: str) -> dict:
    text = extract_resume_text(file_path)
    if not text.strip():
        raise ValueError("No text extracted; scanned PDFs may require OCR.")
    return {"resume_path": str(file_path), "resume_text": text}
