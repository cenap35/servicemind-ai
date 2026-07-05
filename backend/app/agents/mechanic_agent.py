from app.ai.ollama_client import ask_ollama
from app.rag.vector_retriever import retrieve_vector_context

SYSTEM_PROMPT = """
Sen Türkçe konuşan profesyonel bir otomotiv servis danışmanısın.

Görevin:
- Kullanıcının sorusunu yalnızca verilen bilgiye dayanarak cevaplamak.
- Bilgi yetersizse bunu açıkça belirtmek.
- Teknik terimleri doğru ve anlaşılır şekilde açıklamak.
- İngilizce terimleri doğru çevir:
  - tire = lastik
  - tire pressure = lastik basıncı
  - tire pressure warning light = lastik basıncı uyarı ışığı
- Uydurma bilgi verme.
- Cevabı kısa, net ve anlaşılır yaz.
"""


def ask_mechanic(question: str) -> tuple[str, str]:
    context, source_file = retrieve_vector_context(question)

    prompt = f"""
{SYSTEM_PROMPT}

Bilgi:
{context}

Kullanıcının sorusu:
{question}

Cevap:
"""

    answer = ask_ollama(prompt)

    return answer, source_file