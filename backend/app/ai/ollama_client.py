import httpx

from app.core.config import settings


def ask_ollama(prompt: str) -> str:
    response = httpx.post(
        settings.ollama_url,
        json={
            "model": settings.ollama_model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=60,
    )

    response.raise_for_status()

    return response.json()["response"]