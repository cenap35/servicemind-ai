from pathlib import Path

from pypdf import PdfReader


def load_document(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix == ".txt":
        return file_path.read_text(encoding="utf-8")

    if suffix == ".pdf":
        reader = PdfReader(file_path)

        pages = [
            page.extract_text() or ""
            for page in reader.pages
        ]

        return "\n".join(pages)

    raise ValueError(f"Unsupported file type: {file_path.suffix}")