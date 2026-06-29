import httpx


def create_embedding(text: str) -> list[float]:
    response = httpx.post(
        "http://127.0.0.1:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text,
        },
        timeout=60,
    )

    response.raise_for_status()

    return response.json()["embedding"]