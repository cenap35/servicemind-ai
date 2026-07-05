from pathlib import Path

from chromadb import PersistentClient

from app.ai.embedding_client import create_embedding
from app.rag.chunker import split_text
from app.rag.loader import load_document

BASE_DIR = Path(__file__).resolve().parents[3]
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"

client = PersistentClient(path="data/chroma_db")

try:
    client.delete_collection(name="maintenance_guides")
except Exception:
    pass

collection = client.get_or_create_collection(name="maintenance_guides")


def index_documents():
    for file in KNOWLEDGE_DIR.rglob("*"):
        if file.suffix.lower() not in [".txt", ".pdf"]:
            continue

        text = load_document(file)
        chunks = split_text(text)

        for index, chunk in enumerate(chunks):
            embedding = create_embedding(chunk)

            collection.add(
                ids=[f"{file.stem}_{index}"],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[
                    {
                        "source": file.name,
                        "chunk": index,
                        "source_path": str(file.relative_to(KNOWLEDGE_DIR)),
                        "knowledge_type": get_knowledge_type(file),
                        "brand": get_brand(file),
                        "model": get_model(file),
                        "year": get_year(file),
                    }
                ],
            )

    print("✅ Tüm dokümanlar indexlendi.")


def get_knowledge_type(file: Path) -> str:
    parts = file.relative_to(KNOWLEDGE_DIR).parts

    if "general" in parts:
        return "general"

    if "vehicles" in parts:
        return "vehicle"

    return "unknown"


def get_brand(file: Path) -> str:
    parts = file.relative_to(KNOWLEDGE_DIR).parts

    if "vehicles" in parts and len(parts) >= 2:
        vehicle_index = parts.index("vehicles")
        if len(parts) > vehicle_index + 1:
            return parts[vehicle_index + 1].title()

    return "general"


def get_model(file: Path) -> str:
    parts = file.relative_to(KNOWLEDGE_DIR).parts

    if "vehicles" in parts:
        vehicle_index = parts.index("vehicles")
        if len(parts) > vehicle_index + 2:
            return parts[vehicle_index + 2].title()

    return "general"


def get_year(file: Path) -> int:
    parts = file.relative_to(KNOWLEDGE_DIR).parts

    for part in parts:
        if part.isdigit() and len(part) == 4:
            return int(part)

    return 0


if __name__ == "__main__":
    index_documents()