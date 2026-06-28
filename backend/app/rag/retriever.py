from app.rag.knowledge_base import TOYOTA_COROLLA_120K_GUIDE


def retrieve_context(question: str) -> str:
    """
    Şimdilik tüm bilgiyi döndürüyoruz.
    Daha sonra Vector Database burada kullanılacak.
    """

    return TOYOTA_COROLLA_120K_GUIDE