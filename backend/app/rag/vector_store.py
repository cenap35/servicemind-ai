from pathlib import Path

from chromadb import PersistentClient

from app.ai.embedding_client import create_embedding
from app.rag.chunker import split_text

BASE_DIR = Path(__file__).resolve().parents[3]
GUIDES_DIR = BASE_DIR / "data" / "maintenance_guides"

client = PersistentClient(path="data/chroma_db")

try:
    client.delete_collection(name="maintenance_guides")
except Exception:
    pass

collection = client.get_or_create_collection(name="maintenance_guides")


def index_documents():
    for file in GUIDES_DIR.glob("*.txt"):
        text = file.read_text(encoding="utf-8")
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
                    }
                ],
            )

    print("✅ Tüm dokümanlar indexlendi.")


if __name__ == "__main__":
    index_documents()