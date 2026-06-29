from pathlib import Path

from pypdf import PdfReader


def load_document(file_path: Path) -> str:
    if file_path.suffix == ".txt":
        return file_path.read_text(encoding="utf-8")

    if file_path.suffix == ".pdf":
        reader = PdfReader(file_path)

        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages)

    raise ValueError(f"Unsupported file type: {file_path.suffix}")