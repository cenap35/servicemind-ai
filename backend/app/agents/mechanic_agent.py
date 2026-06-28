from app.ai.ollama_client import ask_ollama
from app.rag.retriever import retrieve_context


def ask_mechanic(question: str) -> str:
    context = retrieve_context(question)

    prompt = f"""
Sen Türkçe konuşan bir otomotiv bakım asistanısın.

Kurallar:
- Sadece verilen "Bilgi" bölümünü kullan.
- Bilmediğin şeyi uydurma.
- Kısa, net ve madde madde cevap ver.
- Emin değilsen kullanıcıya uzman servis/usta kontrolü öner.
- Teknik terimleri sade açıkla.

Bilgi:
{context}

Kullanıcının sorusu:
{question}

Cevap formatı:
Kontrol edilmesi gerekenler:
-

Servise sorulacak sorular:
-

Güvenlik notu:
-
"""

    return ask_ollama(prompt)