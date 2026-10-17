"""Natural-language question endpoint (backend: app/routers/ai_query.py)."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app import ai_service
from app.config import settings
from app.database import get_db

router = APIRouter(tags=["AI Assistant"])


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)


class AskResponse(BaseModel):
    question: str
    answer: str
    model: str
    students_in_context: int


@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, db: Session = Depends(get_db)):
    context = ai_service.build_context(db, payload.question)  # read-only ORM queries
    try:
        answer = ai_service.query_ollama(payload.question, context)
    except ai_service.OllamaUnavailableError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))
    except ai_service.OllamaResponseError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc))
    return AskResponse(
        question=payload.question,
        answer=answer,
        model=settings.OLLAMA_MODEL,
        students_in_context=context["students_shown"],
    )
