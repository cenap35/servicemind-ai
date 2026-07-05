from app.ai.ollama_client import ask_ollama
from app.rag.vector_retriever import retrieve_vector_context


def ask_mechanic(question: str) -> tuple[str, str]:
    context, source_file = retrieve_vector_context(question)

    prompt = f"""
Sen Türkçe konuşan bir otomotiv servis danışmanısın.

Görevin:
Verilen dokümandaki bilgiyi kullanıcıya anlaşılır Türkçe ile açıklamak.

Kurallar:
- Cevabı sadece Bilgi bölümüne dayanarak ver.
- İngilizce terimleri doğru çevir:
  - tire = lastik
  - tire pressure = lastik basıncı
  - tire pressure warning light = lastik basıncı uyarı ışığı
- Bilgi yetersizse bunu açıkça söyle.
- Uydurma parça veya işlem yazma.
- Kısa ve net cevap ver.

Bilgi:
{context}

Kullanıcının sorusu:
{question}

Cevap:
"""

    return ask_ollama(prompt), source_file