from app.ai.ollama_client import ask_ollama


def ask_mechanic(question: str) -> str:
    prompt = f"""
Sen deneyimli bir otomotiv ustasısın.

Kullanıcının sorusu:

{question}

Türkçe cevap ver.
Madde madde yaz.
"""

    return ask_ollama(prompt)