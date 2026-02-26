from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from app.services import formation as formation_service
from app.schemas.formation import FormationCreate, FormationUpdate, FormationRead, FormationList

router = APIRouter(prefix="/formations", tags=["Formations"])


@router.post("/", response_model=FormationRead)
def create_formation(formation_data: FormationCreate, db: Session = Depends(get_db)):
    return formation_service.create_formation(db, formation_data)


@router.get("/", response_model=FormationList)
def get_formations(page: int = 1, size: int = 20, db: Session = Depends(get_db)):
    skip = (page - 1) * size
    formations = formation_service.get_formations(db, skip=skip, limit=size)
    total = formation_service.get_formations_total(db)
    
    return {
        "formations": formations,
        "total": total,
        "page": page,
        "size": size
    }


@router.get("/{formation_id}", response_model=FormationRead)
def get_formation(formation_id: int, db: Session = Depends(get_db)):
    formation = formation_service.get_formation(db, formation_id)
    if not formation:
        raise HTTPException(status_code=404, detail="Formation not found")
    return formation


@router.put("/{formation_id}", response_model=FormationRead)
def update_formation(formation_id: int, formation_data: FormationUpdate, db: Session = Depends(get_db)):
    formation = formation_service.update_formation(db, formation_id, formation_data)
    if not formation:
        raise HTTPException(status_code=404, detail="Formation not found")
    return formation


@router.delete("/{formation_id}")
def delete_formation(formation_id: int, db: Session = Depends(get_db)):
    success = formation_service.delete_formation(db, formation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Formation not found")
    return {"message": "Formation deleted successfully"}