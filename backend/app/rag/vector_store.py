import logging
import time
from pathlib import Path

from chromadb import PersistentClient

from app.ai.embedding_client import create_embedding
from app.rag.chunker import split_text
from app.rag.loader import load_document
from app.rag.metadata_parser import parse_metadata

BASE_DIR = Path(__file__).resolve().parents[3]
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"
CHROMA_PATH = BASE_DIR / "data" / "chroma_db"

COLLECTION_NAME = "maintenance_guides"
SUPPORTED_EXTENSIONS = {".txt", ".pdf"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

client = PersistentClient(path=str(CHROMA_PATH))


def recreate_collection():
    try:
        client.delete_collection(name=COLLECTION_NAME)
        logger.info("Eski ChromaDB collection silindi: %s", COLLECTION_NAME)
    except ValueError:
        logger.info(
            "Silinecek eski collection bulunamadı: %s",
            COLLECTION_NAME,
        )

    return client.get_or_create_collection(name=COLLECTION_NAME)


def index_documents():
    start_time = time.perf_counter()

    indexed_files = 0
    failed_files = 0
    created_chunks = 0

    collection = recreate_collection()

    if not KNOWLEDGE_DIR.exists():
        logger.error(
            "Knowledge klasörü bulunamadı: %s",
            KNOWLEDGE_DIR,
        )
        return

    for file in KNOWLEDGE_DIR.rglob("*"):
        if not file.is_file():
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            logger.info("Doküman işleniyor: %s", file)

            text = load_document(file)

            if not text.strip():
                logger.warning("Doküman boş, atlanıyor: %s", file)
                continue

            chunks = split_text(text)

            if not chunks:
                logger.warning("Chunk oluşturulamadı: %s", file)
                continue

            for index, chunk in enumerate(chunks):
                embedding = create_embedding(chunk)

                collection.add(
                    ids=[f"{file.stem}_{index}"],
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[
                        parse_metadata(file, index),
                    ],
                )

                created_chunks += 1

            indexed_files += 1

            logger.info(
                "Doküman indexlendi: %s | chunk=%s",
                file.name,
                len(chunks),
            )

        except Exception:
            failed_files += 1
            logger.exception(
                "Doküman indexlenirken hata oluştu: %s",
                file,
            )

    elapsed_time = time.perf_counter() - start_time

    logger.info(
        (
            "Indexleme tamamlandı | başarılı_dosya=%s | "
            "başarısız_dosya=%s | chunk=%s | süre=%.2f saniye"
        ),
        indexed_files,
        failed_files,
        created_chunks,
        elapsed_time,
    )


if __name__ == "__main__":
    index_documents()