from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
GUIDES_DIR = BASE_DIR / "data" / "maintenance_guides"


def retrieve_context(question: str) -> tuple[str, str]:
    question = question.lower()

    if "corolla" in question and "120000" in question:
        file = GUIDES_DIR / "toyota_corolla_120k.txt"

    elif "corolla" in question and "60000" in question:
        file = GUIDES_DIR / "toyota_corolla_60000.txt"

    else:
        file = GUIDES_DIR / "engine_oil.txt"

    return file.read_text(encoding="utf-8"), file.name