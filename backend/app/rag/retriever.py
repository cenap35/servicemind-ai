from app.rag.knowledge_base import load_maintenance_guide

DOCUMENTS = [
    {
        "file": "toyota_corolla_120k.txt",
        "keywords": ["toyota", "corolla", "120000", "120.000", "120k", "bakım"],
    },
    {
        "file": "toyota_corolla_60000.txt",
        "keywords": ["toyota", "corolla", "60000", "60.000", "60k", "bakım"],
    },
    {
        "file": "engine_oil.txt",
        "keywords": ["motor", "yağ", "yağı", "oil", "filtre"],
    },
]


def retrieve_context(question: str) -> tuple[str, str]:
    question = question.lower()

    best_document = DOCUMENTS[0]
    best_score = 0

    for document in DOCUMENTS:
        score = 0

        for keyword in document["keywords"]:
            if keyword in question:
                score += 1

        if score > best_score:
            best_score = score
            best_document = document

    file_name = best_document["file"]
    context = load_maintenance_guide(file_name)

    return context, file_name