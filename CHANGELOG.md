# Changelog

All notable changes to this project are documented in this file.

## [1.1.0] - 2026-07-17

### Added
- Delete button in the UI for removing documents (and their vector index entries) without using curl.
- Clear error surfacing when local LLM processing fails (e.g., Ollama not running), instead of failing silently.
- Redesigned UI: glassmorphism cards, drag-and-drop upload, gradient theming, loading states, and status pills.

### Fixed
- `/documents/{id}/process` now returns a proper error message on Ollama timeouts/connection issues instead of leaving the document silently unprocessed.

## [1.0.0] - 2026-07-17

### Added
- Initial release: 100% local Intelligent Document Processing platform.
- OCR and document parsing via Tesseract, poppler, and Apache Tika.
- Document classification and structured field extraction via local Ollama LLM.
- Semantic search and RAG-based Q&A using sentence-transformers + ChromaDB.
- FastAPI backend with SQLite storage.
- Basic web UI for upload, processing, Q&A, and search.
