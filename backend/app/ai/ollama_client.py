import httpx


def ask_ollama(prompt: str) -> str:
    response = httpx.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False,
        },
        timeout=60,
    )

    response.raise_for_status()

    return response.json()["response"]