from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.inscription import InscriptionCreate, InscriptionResponse, InscriptionUpdate
from app.services.inscription import InscriptionService

router = APIRouter(prefix="/inscriptions", tags=["Inscriptions"])

@router.post("/", response_model=InscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_inscription(data: InscriptionCreate, db: Session = Depends(get_db)):
    """Inscrire un apprenant à une session."""
    return InscriptionService.create(db, data)

@router.get("/session/{session_id}", response_model=list[InscriptionResponse])
def get_inscriptions_by_session(session_id: int, db: Session = Depends(get_db)):
    """Lister les inscrits d'une session."""
    return InscriptionService.get_by_session(db, session_id)

@router.get("/student/{user_id}", response_model=list[InscriptionResponse])
def get_sessions_by_student(user_id: int, db: Session = Depends(get_db)):
    """Lister les sessions d'un apprenant."""
    return InscriptionService.get_by_student(db, user_id)

@router.delete("/{inscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inscription(inscription_id: int, db: Session = Depends(get_db)):
    """Désinscrire un apprenant (supprimer l'inscription)."""
    InscriptionService.delete(db, inscription_id)
    return None

@router.patch("/{inscription_id}", response_model=InscriptionResponse)
def update_inscription(inscription_id: int, data: InscriptionUpdate, db: Session = Depends(get_db)):
    """Mettre à jour le statut d'une inscription."""
    return InscriptionService.update(db, inscription_id, data)
