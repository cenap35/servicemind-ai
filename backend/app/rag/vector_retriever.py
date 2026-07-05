from pathlib import Path

from chromadb import PersistentClient

from app.ai.embedding_client import create_embedding

BASE_DIR = Path(__file__).resolve().parents[3]
CHROMA_PATH = BASE_DIR / "data" / "chroma_db"
COLLECTION_NAME = "maintenance_guides"

client = PersistentClient(path=str(CHROMA_PATH))

collection = client.get_or_create_collection(name=COLLECTION_NAME)


def retrieve_vector_context(question: str) -> tuple[str, str]:
    question_embedding = create_embedding(question)

    result = collection.query(
        query_embeddings=[question_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"],
    )

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]
    distances = result["distances"][0]

    context = "\n\n---\n\n".join(documents)

    sources = []

    for metadata, distance in zip(metadatas, distances):
        source = metadata.get("source", "unknown")
        source_path = metadata.get("source_path", "unknown")
        chunk = metadata.get("chunk", "unknown")
        domain = metadata.get("domain", "unknown")
        brand = metadata.get("brand", "general")
        model = metadata.get("model", "general")
        year = metadata.get("year", 0)
        system = metadata.get("system", "general")
        file_type = metadata.get("file_type", "unknown")

        sources.append(
            f"{source}#chunk-{chunk} "
            f"path={source_path} "
            f"domain={domain} "
            f"system={system} "
            f"brand={brand} "
            f"model={model} "
            f"year={year} "
            f"file_type={file_type} "
            f"distance={distance:.4f}"
        )

    source_info = " | ".join(sources)

    return context, source_info