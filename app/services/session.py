from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func

from app.models.session import SessionFormation
from app.models.inscription import Inscription
from app.models.user import User, RoleEnum              # ← user.py
from app.schemas.session import SessionCreate, SessionUpdate
from app.exceptions import NotFoundException, BadRequestException


class SessionService:

    # ── LISTER ──
    @staticmethod
    def get_all(
        db: Session,
        page: int = 1,
        size: int = 20,
        formation_id: int | None = None,
        formateur_id: int | None = None,
    ) -> tuple[list[dict], int]:

        query = select(SessionFormation)

        if formation_id:
            query = query.where(SessionFormation.formation_id == formation_id)
        if formateur_id:
            query = query.where(SessionFormation.formateur_id == formateur_id)

        total = db.scalar(
            select(func.count()).select_from(query.subquery())
        )

        offset = (page - 1) * size
        sessions = (
            db.scalars(
                query.options(
                    joinedload(SessionFormation.formation),
                    joinedload(SessionFormation.formateur),
                )
                .offset(offset)
                .limit(size)
            )
            .unique()
            .all()
        )

        result = []
        for s in sessions:
            nb = SessionService.count_inscrits(db, s.id)
            result.append({"session": s, "nombre_inscrits": nb})

        return result, total

    # ── OBTENIR PAR ID ──
    @staticmethod
    def get_by_id(db: Session, session_id: int) -> SessionFormation:

        session = db.scalar(
            select(SessionFormation)
            .options(
                joinedload(SessionFormation.formation),
                joinedload(SessionFormation.formateur),
            )
            .where(SessionFormation.id == session_id)
        )

        if not session:
            raise NotFoundException("Session", session_id)

        return session

    # ── CRÉER ──
    @staticmethod
    def create(db: Session, data: SessionCreate) -> SessionFormation:

        # Vérifier que le formateur existe
        formateur = db.get(User, data.formateur_id)
        if not formateur:
            raise NotFoundException("Formateur", data.formateur_id)

        # Vérifier que c'est bien un formateur
        if formateur.role != RoleEnum.FORMATEUR:
            raise BadRequestException(
                f"L'utilisateur {data.formateur_id} n'a pas le rôle formateur"
            )

        # Vérifier que la formation existe
        from app.services.formation import FormationService
        FormationService.get_by_id(db, data.formation_id)

        # Créer
        session = SessionFormation(**data.model_dump())
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    # ── MODIFIER ──
    @staticmethod
    def update(
        db: Session, session_id: int, data: SessionUpdate
    ) -> SessionFormation:

        session = SessionService.get_by_id(db, session_id)

        # Valider formateur si modifié
        if data.formateur_id is not None:
            formateur = db.get(User, data.formateur_id)
            if not formateur:
                raise NotFoundException("Formateur", data.formateur_id)
            if formateur.role != RoleEnum.FORMATEUR:
                raise BadRequestException(
                    f"L'utilisateur {data.formateur_id} n'a pas le rôle formateur"
                )

        # Valider formation si modifiée
        if data.formation_id is not None:
            from app.services.formation import FormationService
            FormationService.get_by_id(db, data.formation_id)

        update_data = data.model_dump(exclude_unset=True)

        # Vérifier cohérence des dates
        new_debut = update_data.get("date_debut", session.date_debut)
        new_fin = update_data.get("date_fin", session.date_fin)
        if new_fin <= new_debut:
            raise BadRequestException(
                "La date de fin doit être postérieure à la date de début"
            )

        # Vérifier capacité vs inscrits
        if "capacite_max" in update_data:
            nb_inscrits = SessionService.count_inscrits(db, session_id)
            if update_data["capacite_max"] < nb_inscrits:
                raise BadRequestException(
                    f"Impossible : {nb_inscrits} apprenants déjà inscrits, "
                    f"capacité demandée : {update_data['capacite_max']}"
                )

        # Appliquer
        for key, value in update_data.items():
            setattr(session, key, value)

        db.commit()
        db.refresh(session)
        return session

    # ── SUPPRIMER ──
    @staticmethod
    def delete(db: Session, session_id: int) -> None:
        session = SessionService.get_by_id(db, session_id)
        db.delete(session)
        db.commit()

    # ── COMPTER INSCRITS ──
    @staticmethod
    def count_inscrits(db: Session, session_id: int) -> int:
        return (
            db.scalar(
                select(func.count()).where(
                    Inscription.session_id == session_id
                )
            )
            or 0
        )