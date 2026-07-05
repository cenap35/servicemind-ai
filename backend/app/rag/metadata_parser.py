from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"


def parse_metadata(file_path: Path, chunk_index: int) -> dict:
    relative_parts = file_path.relative_to(KNOWLEDGE_DIR).parts

    metadata = {
        "source": file_path.name,
        "source_path": str(file_path.relative_to(KNOWLEDGE_DIR)),
        "chunk": chunk_index,
        "file_type": file_path.suffix.lower().replace(".", ""),
        "domain": "unknown",
        "brand": "general",
        "model": "general",
        "year": 0,
        "system": "general",
    }

    if not relative_parts:
        return metadata

    domain = relative_parts[0]
    metadata["domain"] = domain

    if domain == "general":
        if len(relative_parts) > 1:
            metadata["system"] = relative_parts[1]

    if domain == "vehicles":
        metadata["domain"] = "vehicle"

        if len(relative_parts) > 1:
            metadata["brand"] = relative_parts[1].title()

        if len(relative_parts) > 2:
            metadata["model"] = relative_parts[2].title()

        if len(relative_parts) > 3 and relative_parts[3].isdigit():
            metadata["year"] = int(relative_parts[3])

    return metadata