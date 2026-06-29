from chromadb import PersistentClient

from app.ai.embedding_client import create_embedding

client = PersistentClient(path="data/chroma_db")

collection = client.get_or_create_collection(
    name="maintenance_guides"
)


def retrieve_vector_context(question: str) -> tuple[str, str]:
    question_embedding = create_embedding(question)

    result = collection.query(
        query_embeddings=[question_embedding],
        n_results=2,
    )

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]

    context = "\n\n---\n\n".join(documents)

    source_files = []

    for metadata in metadatas:
        source = metadata["source"]
        chunk = metadata["chunk"]
        source_files.append(f"{source}#chunk-{chunk}")

    source_info = ", ".join(source_files)

    return context, source_info