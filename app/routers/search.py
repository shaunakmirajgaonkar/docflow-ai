from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db, ChatHistory
from app.models.schemas import QARequest, QAResponse, SearchRequest
from app.services import vector_service
from app.services.analysis_service import answer_question

router = APIRouter(tags=["search"])


@router.post("/search")
def semantic_search(req: SearchRequest):
    hits = vector_service.semantic_search(
        query=req.query, top_k=req.top_k, document_id=req.document_id
    )
    return {"query": req.query, "results": hits}


@router.post("/qa", response_model=QAResponse)
def document_qa(req: QARequest, db: Session = Depends(get_db)):
    hits = vector_service.semantic_search(
        query=req.question, top_k=req.top_k, document_id=req.document_id
    )
    context_chunks = [h["text"] for h in hits]
    answer = answer_question(req.question, context_chunks)

    chat = ChatHistory(
        document_id=req.document_id,
        question=req.question,
        answer=answer,
        sources=hits,
    )
    db.add(chat)
    db.commit()

    return QAResponse(answer=answer, sources=hits)
