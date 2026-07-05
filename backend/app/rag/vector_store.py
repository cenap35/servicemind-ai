from pathlib import Path

from chromadb import PersistentClient

from app.ai.embedding_client import create_embedding
from app.rag.chunker import split_text
from app.rag.loader import load_document
from app.rag.metadata_parser import parse_metadata

BASE_DIR = Path(__file__).resolve().parents[3]
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"
CHROMA_PATH = BASE_DIR / "data" / "chroma_db"
COLLECTION_NAME = "maintenance_guides"

client = PersistentClient(path=str(CHROMA_PATH))

try:
    client.delete_collection(name=COLLECTION_NAME)
except Exception:
    pass

collection = client.get_or_create_collection(name=COLLECTION_NAME)


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
                    parse_metadata(file, index),
                ],
            )

    print("✅ Tüm dokümanlar indexlendi.")


if __name__ == "__main__":
    index_documents()