from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
GUIDES_DIR = BASE_DIR / "data" / "maintenance_guides"


def load_maintenance_guide(file_name: str) -> str:
    file_path = GUIDES_DIR / file_name
    return file_path.read_text(encoding="utf-8")