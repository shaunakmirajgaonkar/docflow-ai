from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class DocumentOut(BaseModel):
    id: int
    filename: str
    file_type: Optional[str] = None
    status: str
    doc_class: Optional[str] = None
    extracted_fields: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class QARequest(BaseModel):
    question: str
    document_id: Optional[int] = None
    top_k: int = 5


class QAResponse(BaseModel):
    answer: str
    sources: list[dict]


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    document_id: Optional[int] = None


class WorkflowTriggerRequest(BaseModel):
    document_id: int
    workflow_name: str = "ingest_pipeline"
