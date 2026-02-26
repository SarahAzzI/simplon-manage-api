from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.formation import Formation
from app.schemas.formation import FormationCreate, FormationUpdate, FormationRead


def create_formation(db: Session, formation_data: FormationCreate) -> Formation:

    new_formation = Formation(
        title=formation_data.title,
        description=formation_data.description,
        duration=formation_data.duration,
        level=formation_data.level
    )
    db.add(new_formation)
    db.commit()
    db.refresh(new_formation)
    return new_formation


def get_formation(db: Session, formation_id: int) -> Optional[Formation]:

    return db.query(Formation).filter(Formation.id == formation_id).first()


def get_formations(db: Session, skip: int = 0, limit: int = 100) -> List[Formation]:

    return db.query(Formation).offset(skip).limit(limit).all()


def get_formations_total(db: Session) -> int:

    return db.query(Formation).count()


def update_formation(db: Session, formation_id: int, formation_data: FormationUpdate) -> Optional[Formation]:

    formation = get_formation(db, formation_id)
    if not formation:
        return None
    
    update_data = formation_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(formation, key, value)
    
    db.commit()
    db.refresh(formation)
    return formation


def delete_formation(db: Session, formation_id: int) -> bool:

    formation = get_formation(db, formation_id)
    if not formation:
        return False
    
    db.delete(formation)
    db.commit()
    return True