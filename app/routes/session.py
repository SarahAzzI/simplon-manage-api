import math
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.session import (
    SessionCreate,
    SessionUpdate,
    SessionResponse,
    SessionDetailResponse,
)
from app.schemas.pagination import PaginatedResponse
from app.services.session import SessionService

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.get("/", response_model=PaginatedResponse[SessionResponse])
def lister_sessions(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    formation_id: Optional[int] = Query(None),
    formateur_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    results, total = SessionService.list(db, page, size, formation_id, formateur_id)

    items = []
    for r in results:
        s = SessionResponse.model_validate(r["session"])
        s.nombre_inscrits = r["nombre_inscrits"]
        items.append(s)

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total else 0,
    )


@router.get("/{session_id}", response_model=SessionDetailResponse)
def obtenir_session(session_id: int, db: Session = Depends(get_db)):
    session = SessionService.get_by_id(db, session_id)
    nb = SessionService.count_inscrits(db, session_id)
    result = SessionDetailResponse.model_validate(session)
    result.nombre_inscrits = nb
    return result


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def creer_session(data: SessionCreate, db: Session = Depends(get_db)):
    return SessionService.create(db, data)


@router.put("/{session_id}", response_model=SessionResponse)
def modifier_session(
    session_id: int, data: SessionUpdate, db: Session = Depends(get_db)
):
    return SessionService.update(db, session_id, data)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_session(session_id: int, db: Session = Depends(get_db)):
    SessionService.delete(db, session_id)
