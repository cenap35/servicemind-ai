from app.rag.knowledge_base import load_toyota_corolla_120k_guide


def retrieve_context(question: str) -> str:
    return load_toyota_corolla_120k_guide()