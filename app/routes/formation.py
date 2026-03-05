from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.formation import FormationCreate, FormationUpdate, FormationResponse
from app.schemas.pagination import PaginatedResponse
from app.services.formation import FormationService
import math

router = APIRouter(prefix="/formations", tags=["Formations"])


@router.post("/", response_model=FormationResponse, status_code=status.HTTP_201_CREATED)
def create_formation(formation: FormationCreate, db: Session = Depends(get_db)):
    return FormationService.create(db, formation)


@router.get("/", response_model=PaginatedResponse[FormationResponse])
def get_formations(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size
    items = FormationService.list(db, skip=skip, limit=size)
    total = FormationService.get_total(db)
    pages = math.ceil(total / size)
    return {"items": items, "total": total, "page": page, "size": size, "pages": pages}


@router.get("/{formation_id}", response_model=FormationResponse)
def get_formation(formation_id: int, db: Session = Depends(get_db)):
    return FormationService.get_by_id(db, formation_id)


@router.patch("/{formation_id}", response_model=FormationResponse)
def update_formation(
    formation_id: int, formation: FormationUpdate, db: Session = Depends(get_db)
):
    return FormationService.update(db, formation_id, formation)


@router.delete("/{formation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_formation(formation_id: int, db: Session = Depends(get_db)):
    FormationService.delete(db, formation_id)
    return None
