from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.formation import Formation
from app.schemas.formation import FormationCreate, FormationUpdate, FormationResponse


class FormationService:
    @staticmethod
    def create(db: Session, formation_data: FormationCreate) -> Formation:
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

    @staticmethod
    def get_by_id(db: Session, formation_id: int) -> Optional[Formation]:
        return db.query(Formation).filter(Formation.id == formation_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Formation]:
        return db.query(Formation).offset(skip).limit(limit).all()

    @staticmethod
    def get_total(db: Session) -> int:
        return db.query(Formation).count()

    @staticmethod
    def update(db: Session, formation_id: int, formation_data: FormationUpdate) -> Optional[Formation]:
        formation = FormationService.get_by_id(db, formation_id)
        if not formation:
            return None
        
        update_data = formation_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(formation, key, value)
        
        db.commit()
        db.refresh(formation)
        return formation

    @staticmethod
    def delete(db: Session, formation_id: int) -> bool:
        formation = FormationService.get_by_id(db, formation_id)
        if not formation:
            return False
        
        db.delete(formation)
        db.commit()
        return True
