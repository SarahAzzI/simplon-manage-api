import math
from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.inscription import (
    InscriptionCreate,
    InscriptionResponse,
    InscriptionUpdate,
)
from app.schemas.pagination import PaginatedResponse
from app.services.inscription import InscriptionService

router = APIRouter(prefix="/inscriptions", tags=["Inscriptions"])


@router.post(
    "/", response_model=InscriptionResponse, status_code=status.HTTP_201_CREATED
)
def create_inscription(data: InscriptionCreate, db: Session = Depends(get_db)):
    """Inscrire un apprenant à une session."""
    return InscriptionService.create(db, data)

@router.get(
        "/inscriptions", response_model=List[InscriptionResponse])
def get_all_inscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return InscriptionService.get_all(db, skip=skip, limit=limit)

@router.get(
    "/session/{session_id}", response_model=PaginatedResponse[InscriptionResponse]
)
def get_inscriptions_by_session(
    session_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Lister les inscrits d'une session avec pagination."""
    skip = (page - 1) * size
    items = InscriptionService.get_by_session(db, session_id, skip=skip, limit=size)
    total = InscriptionService.count_by_session(db, session_id)
    pages = math.ceil(total / size) if total else 0
    return {"items": items, "total": total, "page": page, "size": size, "pages": pages}


@router.get("/student/{user_id}", response_model=PaginatedResponse[InscriptionResponse])
def get_sessions_by_student(
    user_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Lister les sessions d'un apprenant avec pagination."""
    skip = (page - 1) * size
    items = InscriptionService.get_by_student(db, user_id, skip=skip, limit=size)
    total = InscriptionService.count_by_student(db, user_id)
    pages = math.ceil(total / size) if total else 0
    return {"items": items, "total": total, "page": page, "size": size, "pages": pages}


@router.delete("/{inscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inscription(inscription_id: int, db: Session = Depends(get_db)):
    """Désinscrire un apprenant (supprimer l'inscription)."""
    InscriptionService.delete(db, inscription_id)
    return None


@router.patch("/{inscription_id}", response_model=InscriptionResponse)
def update_inscription(
    inscription_id: int, data: InscriptionUpdate, db: Session = Depends(get_db)
):
    """Mettre à jour le statut d'une inscription."""
    return InscriptionService.update(db, inscription_id, data)
