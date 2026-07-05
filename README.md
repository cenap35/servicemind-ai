# 🚗 ServiceMind AI

> AI-powered Automotive Intelligence Platform built with FastAPI, Ollama, ChromaDB and Retrieval-Augmented Generation (RAG).

ServiceMind AI is an intelligent automotive assistant that understands technical documentation, maintenance procedures, and vehicle-specific knowledge using Retrieval-Augmented Generation (RAG).

Instead of relying only on a language model, the system retrieves relevant information from its knowledge base and generates grounded, context-aware responses for maintenance and diagnostic scenarios.

---

## ✨ Features

- 🤖 AI-powered automotive assistant
- 📄 PDF & TXT document ingestion
- 🧩 Automatic document chunking
- 🧠 Embedding generation with Ollama
- 🔍 Semantic search using ChromaDB
- 📚 Retrieval-Augmented Generation (RAG)
- 🚗 Vehicle-specific knowledge base
- 🔧 General automotive knowledge support
- 📦 Metadata-based document organization
- ⚡ FastAPI REST API
- 📖 Interactive Swagger documentation

---

## 🏗️ Architecture

```text
Knowledge Base
        │
        ▼
Document Loader
        │
        ▼
Chunker
        │
        ▼
Embedding Model
        │
        ▼
ChromaDB Vector Database
        │
        ▼
Vector Retriever
        │
        ▼
Mechanic Agent
        │
        ▼
LLM (Ollama)
        │
        ▼
Final Response
```

---

## 📂 Project Structure

```text
backend/
│
├── agents/
├── ai/
├── api/
├── core/
├── rag/
│
└── main.py

data/
│
├── knowledge/
│   ├── general/
│   └── vehicles/
│
└── chroma_db/
```

---

## 🧠 Knowledge Base

The knowledge base is organized into two categories:

```text
knowledge/

├── general/
│   ├── engine/
│   ├── brakes/
│   └── ...

└── vehicles/
    └── toyota/
        └── corolla/
            └── 2018/
```

This architecture allows the system to combine:

- General automotive knowledge
- Vehicle-specific documentation

during retrieval.

---

## ⚙️ Tech Stack

- Python
- FastAPI
- Ollama
- ChromaDB
- Pydantic
- HTTPX
- PyPDF
- RAG
- Vector Embeddings

---

## 🚀 Vision

ServiceMind AI aims to become an intelligent automotive engineering platform capable of understanding maintenance manuals, diagnostic procedures, technical documentation, and real-world service workflows using modern AI technologies.

See **docs/VISION.md** for the long-term product vision.