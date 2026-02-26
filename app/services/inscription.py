from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func
from app.models.inscription import Inscription, StatutInscription
from app.models.session import SessionFormation
from app.models.user import User, Role
from app.schemas.inscription import InscriptionCreate, InscriptionUpdate
from app.core.exceptions import NotFoundException, BadRequestException

class InscriptionService:

    @staticmethod
    def create(db: Session, data: InscriptionCreate) -> Inscription:
        # 1. Vérifier si l'apprenant existe
        user = db.get(User, data.user_id)
        if not user:
            raise NotFoundException("Apprenant", data.user_id)
        
        # 2. Vérifier si c'est bien un apprenant (STUDENT)
        if user.role != Role.STUDENT:
            raise BadRequestException(f"L'utilisateur {data.user_id} n'est pas un apprenant.")

        # 3. Vérifier si la session existe
        session = db.get(SessionFormation, data.session_id)
        if not session:
            raise NotFoundException("Session", data.session_id)

        # 4. Vérifier si l'apprenant est déjà inscrit
        existing = db.scalar(
            select(Inscription).where(
                Inscription.user_id == data.user_id,
                Inscription.session_id == data.session_id
            )
        )
        if existing:
            raise BadRequestException("L'apprenant est déjà inscrit à cette session.")

        # 5. Vérifier la capacité de la session
        from app.services.session import SessionService
        nb_inscrits = SessionService.count_inscrits(db, data.session_id)
        if nb_inscrits >= session.capacite_max:
            raise BadRequestException("La session est complète.")

        # 6. Créer l'inscription
        inscription = Inscription(**data.model_dump())
        db.add(inscription)
        db.commit()
        db.refresh(inscription)
        return inscription

    @staticmethod
    def get_by_session(db: Session, session_id: int) -> list[Inscription]:
        # Vérifier si la session existe
        session = db.get(SessionFormation, session_id)
        if not session:
            raise NotFoundException("Session", session_id)
            
        return db.scalars(
            select(Inscription)
            .options(joinedload(Inscription.user))
            .where(Inscription.session_id == session_id)
        ).all()

    @staticmethod
    def get_by_student(db: Session, user_id: int) -> list[Inscription]:
        # Vérifier si l'apprenant existe
        user = db.get(User, user_id)
        if not user:
            raise NotFoundException("Apprenant", user_id)
            
        return db.scalars(
            select(Inscription)
            .options(joinedload(Inscription.session).joinedload(SessionFormation.formation))
            .where(Inscription.user_id == user_id)
        ).all()

    @staticmethod
    def delete(db: Session, inscription_id: int) -> None:
        inscription = db.get(Inscription, inscription_id)
        if not inscription:
            raise NotFoundException("Inscription", inscription_id)
        
        db.delete(inscription)
        db.commit()

    @staticmethod
    def update(db: Session, inscription_id: int, data: InscriptionUpdate) -> Inscription:
        inscription = db.get(Inscription, inscription_id)
        if not inscription:
            raise NotFoundException("Inscription", inscription_id)
            
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(inscription, key, value)
            
        db.commit()
        db.refresh(inscription)
        return inscription
