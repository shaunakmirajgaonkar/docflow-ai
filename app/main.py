from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routers import documents, search

app = FastAPI(
    title="DocFlow AI - Local Intelligent Document Processing",
    description="100% local IDP platform: OCR, classification, extraction, RAG Q&A, semantic search.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(documents.router)
app.include_router(search.router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.get("/health")
def health():
    return {"status": "ok", "mode": "100% local - no cloud calls"}
