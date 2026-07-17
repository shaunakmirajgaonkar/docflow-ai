"""
Lightweight local workflow-automation engine.

Workflows are just Python callables registered in WORKFLOW_REGISTRY.
They run synchronously here for simplicity; swap in a local task queue
(e.g. huey/rq with a local redis) if you need background execution.
"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.database import Document, WorkflowRun
from app.services.analysis_service import classify_document, extract_fields
from app.services import vector_service


def run_ingest_pipeline(db: Session, document: Document) -> dict:
    """Full local pipeline: classify -> extract fields -> index for search."""
    text = document.extracted_text or ""

    classification = classify_document(text)
    doc_class = classification.get("category", "other")

    fields = extract_fields(text, doc_class)

    chunks_indexed = vector_service.index_document(
        document_id=document.id,
        filename=document.filename,
        text=text,
        doc_class=doc_class,
    )

    document.doc_class = doc_class
    document.extracted_fields = fields
    document.status = "done"
    document.updated_at = datetime.now(timezone.utc)
    db.commit()

    result = {
        "classification": classification,
        "fields": fields,
        "chunks_indexed": chunks_indexed,
    }

    run = WorkflowRun(
        document_id=document.id,
        workflow_name="ingest_pipeline",
        status="completed",
        result=result,
    )
    db.add(run)
    db.commit()
    return result


WORKFLOW_REGISTRY = {
    "ingest_pipeline": run_ingest_pipeline,
}
