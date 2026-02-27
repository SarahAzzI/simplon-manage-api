from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.formation import Formation
from app.schemas.formation import FormationCreate, FormationUpdate, FormationResponse
from app.core.exceptions import NotFoundException


class FormationService:
    @staticmethod
    def create(db: Session, formation_data: FormationCreate) -> Formation:
        new_formation = Formation(
            title=formation_data.title,
            description=formation_data.description,
            duration=formation_data.duration,
            level=formation_data.level,
        )
        db.add(new_formation)
        db.commit()
        db.refresh(new_formation)
        return new_formation

    @staticmethod
    def get_by_id(db: Session, formation_id: int) -> Formation:
        formation = db.query(Formation).filter(Formation.id == formation_id).first()
        if not formation:
            raise NotFoundException("Formation", formation_id)
        return formation

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100) -> List[Formation]:
        return db.query(Formation).offset(skip).limit(limit).all()

    @staticmethod
    def get_total(db: Session) -> int:
        return db.query(Formation).count()

    @staticmethod
    def update(
        db: Session, formation_id: int, formation_data: FormationUpdate
    ) -> Formation:
        formation = FormationService.get_by_id(db, formation_id)

        update_data = formation_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(formation, key, value)

        db.commit()
        db.refresh(formation)
        return formation

    @staticmethod
    def delete(db: Session, formation_id: int) -> None:
        formation = FormationService.get_by_id(db, formation_id)
        db.delete(formation)
        db.commit()
