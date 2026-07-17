import os
import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, Document
from app.config import settings
from app.models.schemas import DocumentOut, WorkflowTriggerRequest
from app.services.ocr_service import extract_text
from app.services.workflow_service import WORKFLOW_REGISTRY
from app.services import vector_service

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentOut)
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    dest_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    document = Document(
        filename=file.filename,
        filepath=dest_path,
        file_type=Path(file.filename).suffix.lower().lstrip("."),
        status="uploaded",
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    # Local OCR / parsing happens immediately (synchronous, all on-device)
    try:
        text = extract_text(dest_path)
        document.extracted_text = text
        document.status = "parsed"
        db.commit()
        db.refresh(document)
    except Exception as e:
        document.status = "parse_failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Local OCR/parsing failed: {e}")

    return document


@router.post("/{document_id}/process")
def process_document(document_id: int, req: WorkflowTriggerRequest = None, db: Session = Depends(get_db)):
    """Run classification + field extraction + indexing via the local workflow engine."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    workflow_name = req.workflow_name if req else "ingest_pipeline"
    workflow_fn = WORKFLOW_REGISTRY.get(workflow_name)
    if not workflow_fn:
        raise HTTPException(status_code=400, detail=f"Unknown workflow '{workflow_name}'")

    try:
        result = workflow_fn(db, document)
    except RuntimeError as e:
        # Typically: local Ollama isn't running / model not pulled
        document.status = "process_failed"
        db.commit()
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        document.status = "process_failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

    return {"document_id": document_id, "workflow": workflow_name, "result": result}


@router.get("/", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.created_at.desc()).all()


@router.get("/{document_id}", response_model=DocumentOut)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/{document_id}/text")
def get_document_text(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"document_id": document_id, "text": document.extracted_text}


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if os.path.exists(document.filepath):
        os.remove(document.filepath)
    vector_service.delete_document(document_id)

    db.delete(document)
    db.commit()
    return {"deleted": document_id}
