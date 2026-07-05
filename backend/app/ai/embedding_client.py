import httpx

from app.core.config import settings


def create_embedding(text: str) -> list[float]:
    response = httpx.post(
        settings.embedding_url,
        json={
            "model": settings.embedding_model,
            "prompt": text,
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["embedding"]