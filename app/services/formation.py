from fastapi import HTTPException, status
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.formation import Formation
from app.schemas.formation import FormationCreate, FormationUpdate, FormationResponse
from app.core.exceptions import NotFoundException


class FormationService:
    @staticmethod
    def create(db: Session, formation_data: FormationCreate) -> Formation:
        if formation_data.duration <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La durée de la formation doit être supérieure à 0"
            )
        existing_formation = db.query(Formation).filter(Formation.title == formation_data.title).first()
        if existing_formation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Une formation avec le titre {formation_data.title} existe déjà"
            )
        if not formation_data.level:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le niveau doit être spécifié"
            )
        try:
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
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur d'intégrité, impossible de créer l'utilisateur"
            )
        

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

        if not formation:
            raise Exception(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La formation avec l'id {formation_id} non trouvé"
            )
        
        if not formation_data.level:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le niveau doit être spécifié"
            )
        
        try:
            if formation_data.duration <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La durée de la formation doit être supérieure à 0"
                )
            
            existing_formation = db.query(Formation).filter(Formation.title == formation_data.title).first()
        
            if existing_formation:
                if existing_formation:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Une formation avec ce titre existe déjà"
                    )


            update_data = formation_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(formation, key, value)

            db.commit()
            db.refresh(formation)
            return formation
        
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur d'intégrité des données. Impossible de mettre à jour la formation."
            )
        
    @staticmethod
    def delete(db: Session, formation_id: int) -> None:

        formation = FormationService.get_by_id(db, formation_id)
        if formation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La formation avec l'id {formation_id} n'existe pas."
            )
        try:

            db.delete(formation)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Une erreur inattendue est survenue : {str(e)}"
            )
