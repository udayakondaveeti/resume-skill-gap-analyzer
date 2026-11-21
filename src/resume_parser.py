from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract and return text from all pages of a PDF file."""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"Resume file not found: {path}")

    reader = PdfReader(str(path))
    pages_text = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages_text.append(text.strip())

    return "\n".join(pages_text)


def load_text_file(file_path: str | Path) -> str:
    """Load text from a PDF or text-based file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(path)

    return path.read_text(encoding="utf-8", errors="ignore")