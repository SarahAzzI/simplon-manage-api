from sqlalchemy.orm import Session
from app.models.formation import Formation
from app.core.exceptions import NotFoundException

class FormationService:
    @staticmethod
    def get_by_id(db: Session, formation_id: int) -> Formation:
        formation = db.get(Formation, formation_id)
        if not formation:
            raise NotFoundException("Formation", formation_id)
        return formation
