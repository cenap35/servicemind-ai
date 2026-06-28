from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
GUIDE_PATH = BASE_DIR / "data" / "maintenance_guides" / "toyota_corolla_120k.txt"


def load_toyota_corolla_120k_guide() -> str:
    return GUIDE_PATH.read_text(encoding="utf-8")