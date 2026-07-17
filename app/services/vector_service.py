"""
100% local vector search:
  - sentence-transformers runs the embedding model on your CPU/GPU
  - chromadb persists vectors to a local folder (no server, no cloud)
"""
from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer

from app.config import settings

_embedder = SentenceTransformer(settings.EMBEDDING_MODEL)  # downloaded once, runs locally
_client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
_collection = _client.get_or_create_collection(name="documents")


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> List[str]:
    words = text.split()
    if not words:
        return []
    chunks = []
    step = max(chunk_size - overlap, 1)
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        if i + chunk_size >= len(words):
            break
    return chunks


def embed(texts: List[str]):
    return _embedder.encode(texts, show_progress_bar=False).tolist()


def index_document(document_id: int, filename: str, text: str, doc_class: str = None):
    chunks = chunk_text(text)
    if not chunks:
        return 0

    vectors = embed(chunks)
    ids = [f"doc{document_id}_chunk{i}" for i in range(len(chunks))]
    metadatas = [
        {"document_id": document_id, "filename": filename, "chunk_index": i,
         "doc_class": doc_class or "unclassified"}
        for i in range(len(chunks))
    ]

    # remove any previous chunks for this doc before re-indexing
    try:
        _collection.delete(where={"document_id": document_id})
    except Exception:
        pass

    _collection.add(ids=ids, embeddings=vectors, documents=chunks, metadatas=metadatas)
    return len(chunks)


def semantic_search(query: str, top_k: int = 5, document_id: int = None) -> List[Dict[str, Any]]:
    query_vec = embed([query])[0]
    where = {"document_id": document_id} if document_id else None

    results = _collection.query(
        query_embeddings=[query_vec],
        n_results=top_k,
        where=where,
    )

    hits = []
    for doc, meta, dist in zip(
        results.get("documents", [[]])[0],
        results.get("metadatas", [[]])[0],
        results.get("distances", [[]])[0],
    ):
        hits.append({"text": doc, "metadata": meta, "score": 1 - dist})
    return hits


def delete_document(document_id: int):
    try:
        _collection.delete(where={"document_id": document_id})
    except Exception:
        pass
