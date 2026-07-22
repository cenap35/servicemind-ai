import logging
import time
from pathlib import Path

from chromadb import PersistentClient

from app.ai.embedding_client import create_embedding
from app.rag.chunker import split_text
from app.rag.loader import load_document
from app.rag.metadata_parser import parse_metadata
from app.utils.hash_utils import calculate_file_hash

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


def get_collection():
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
    )

    logger.info(
        "ChromaDB collection hazır: %s",
        COLLECTION_NAME,
    )

    return collection


def get_stored_file_hash(
    collection,
    source_path: str,
) -> str | None:
    result = collection.get(
        where={"source_path": source_path},
        include=["metadatas"],
        limit=1,
    )

    metadatas = result.get("metadatas") or []

    if not metadatas:
        return None

    return metadatas[0].get("file_hash")


def index_documents():
    start_time = time.perf_counter()

    indexed_files = 0
    skipped_files = 0
    failed_files = 0
    created_chunks = 0

    collection = get_collection()

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
            logger.info("Doküman kontrol ediliyor: %s", file)

            source_path = str(file.relative_to(KNOWLEDGE_DIR))
            file_hash = calculate_file_hash(file)

            stored_file_hash = get_stored_file_hash(
                collection,
                source_path,
            )

            if stored_file_hash == file_hash:
                skipped_files += 1

                logger.info(
                    "Doküman değişmemiş, atlanıyor: %s",
                    source_path,
                )
                continue

            if stored_file_hash is not None:
                collection.delete(
                    where={"source_path": source_path},
                )

                logger.info(
                    "Dokümanın eski chunk'ları silindi: %s",
                    source_path,
                )

            text = load_document(file)

            if not text.strip():
                logger.warning(
                    "Doküman boş, atlanıyor: %s",
                    source_path,
                )
                continue

            chunks = split_text(text)

            if not chunks:
                logger.warning(
                    "Chunk oluşturulamadı: %s",
                    source_path,
                )
                continue

            for index, chunk in enumerate(chunks):
                embedding = create_embedding(chunk)

                collection.add(
                    ids=[f"{source_path}::{index}"],
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[
                        parse_metadata(
                            file,
                            index,
                            file_hash,
                        ),
                    ],
                )

                created_chunks += 1

            indexed_files += 1

            logger.info(
                "Doküman indexlendi: %s | chunk=%s",
                source_path,
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
            "Indexleme tamamlandı | indexlenen_dosya=%s | "
            "atlanan_dosya=%s | başarısız_dosya=%s | "
            "chunk=%s | süre=%.2f saniye"
        ),
        indexed_files,
        skipped_files,
        failed_files,
        created_chunks,
        elapsed_time,
    )


if __name__ == "__main__":
    index_documents()