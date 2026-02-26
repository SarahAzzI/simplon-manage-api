from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.formation import FormationCreate, FormationUpdate, FormationResponse
from app.schemas.pagination import PaginatedResponse
from app.services.formation import FormationService
import math

router = APIRouter(prefix="/formations", tags=["Formations"])

@router.post("/", response_model=FormationResponse, status_code=status.HTTP_201_CREATED)
def create_formation_route(formation: FormationCreate, db: Session = Depends(get_db)):
    return FormationService.create(db, formation)

@router.get("/", response_model=PaginatedResponse[FormationResponse])
def get_formations_route(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    skip = (page - 1) * size
    items = FormationService.list(db, skip=skip, limit=size)
    total = FormationService.get_total(db)
    pages = math.ceil(total / size)
    return {"items": items, "total": total, "page": page, "size": size, "pages": pages}

@router.get("/{formation_id}", response_model=FormationResponse)
def get_formation_route(formation_id: int, db: Session = Depends(get_db)):
    formation = FormationService.get_by_id(db, formation_id)
    if not formation:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return formation

@router.put("/{formation_id}", response_model=FormationResponse)
def update_formation_route(formation_id: int, formation: FormationUpdate, db: Session = Depends(get_db)):
    updated = FormationService.update(db, formation_id, formation)
    if not updated:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return updated

@router.delete("/{formation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_formation_route(formation_id: int, db: Session = Depends(get_db)):
    if not FormationService.delete(db, formation_id):
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return None
