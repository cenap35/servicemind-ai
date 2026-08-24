from pathlib import Path

from chromadb import PersistentClient

from app.ai.embedding_client import create_embedding

BASE_DIR = Path(__file__).resolve().parents[3]
CHROMA_PATH = BASE_DIR / "data" / "chroma_db"
COLLECTION_NAME = "maintenance_guides"

client = PersistentClient(path=str(CHROMA_PATH))

collection = client.get_or_create_collection(name=COLLECTION_NAME)

MetadataFilterValue = str | int | float | bool
MetadataFilter = dict[str, MetadataFilterValue]


def retrieve_vector_context(
    question: str,
    metadata_filter: MetadataFilter | None = None,
    max_distance: float | None = None,
) -> tuple[str, str]:
    question_embedding = create_embedding(question)

    query_parameters = {
        "query_embeddings": [question_embedding],
        "n_results": 3,
        "include": ["documents", "metadatas", "distances"],
    }

    if metadata_filter is not None:
        query_parameters["where"] = metadata_filter

    result = collection.query(**query_parameters)

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]
    distances = result["distances"][0]

    retrieved_items = list(
        zip(documents, metadatas, distances)
    )

    if max_distance is not None:
        retrieved_items = [
            (document, metadata, distance)
            for document, metadata, distance in retrieved_items
            if distance <= max_distance
        ]

    context = "\n\n---\n\n".join(
        document
        for document, _, _ in retrieved_items
    )

    sources = []

    for _, metadata, distance in retrieved_items:
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
