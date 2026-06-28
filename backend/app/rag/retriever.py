from app.rag.knowledge_base import TOYOTA_COROLLA_120K_GUIDE


def retrieve_context(question: str) -> str:
    """
    Şimdilik basit retrieval:
    Kullanıcının sorusuna bakmadan mevcut bilgi tabanını döndürür.

    İleride burada:
    - PDF parçaları
    - embedding
    - vector database
    - en alakalı bakım bilgileri
    dönecek.
    """

    return TOYOTA_COROLLA_120K_GUIDE