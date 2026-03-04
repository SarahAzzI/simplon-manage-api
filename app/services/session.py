from datetime import date
from typing import Optional, Tuple, List, Dict
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func

from app.models.session import SessionFormation
from app.models.inscription import Inscription
from app.core.role import Role
from app.schemas.session import SessionCreate, SessionUpdate
from app.core.exceptions import NotFoundException, BadRequestException
from app.models.user import User


class SessionService:

    # ── LISTER ──
    @staticmethod
    def list(
        db: Session,
        page: int = 1,
        size: int = 20,
        formation_id: Optional[int] = None,
        formateur_id: Optional[int] = None,
    ) -> Tuple[List[Dict], int]:

        query = select(SessionFormation)

        if formation_id:
            query = query.where(SessionFormation.formation_id == formation_id)
        if formateur_id:
            query = query.where(SessionFormation.formateur_id == formateur_id)

        total = db.scalar(select(func.count()).select_from(query.subquery()))

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

    # get by ID
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

    # create
    @staticmethod
    def create(db: Session, data: SessionCreate) -> SessionFormation:

        # Vérifier que le formateur existe
        formateur = db.get(User, data.formateur_id)
        if not formateur:
            raise NotFoundException("Formateur", data.formateur_id)

        # Vérifier que c'est bien un formateur
        if formateur.role != Role.TEACHER:
            raise BadRequestException(
                f"L'utilisateur {data.formateur_id} n'a pas le rôle formateur"
            )

        # Vérifier que la formation existe
        from app.services.formation import FormationService

        FormationService.get_by_id(db, data.formation_id)

        # Valider la cohérence métier
        SessionService._validate_session(
            db,
            data.date_debut,
            data.date_fin,
            data.capacite_max,
            data.capacite_minimale,
        )

        # create (without linking students)
        session = SessionFormation(**data.model_dump())
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    # update
    @staticmethod
    def update(db: Session, session_id: int, data: SessionUpdate) -> SessionFormation:

        session = SessionService.get_by_id(db, session_id)

        # Valider formateur si modifié
        if data.formateur_id is not None:
            formateur = db.get(User, data.formateur_id)
            if not formateur:
                raise NotFoundException("Formateur", data.formateur_id)
            if formateur.role != Role.TEACHER:
                raise BadRequestException(
                    f"L'utilisateur {data.formateur_id} n'a pas le rôle formateur"
                )

        # Valider formation si modifiée
        if data.formation_id is not None:
            from app.services.formation import FormationService

            FormationService.get_by_id(db, data.formation_id)

        update_data = data.model_dump(exclude_unset=True)

        # Valider la cohérence métier (dates, capacité max et min)
        new_debut = update_data.get("date_debut", session.date_debut)
        new_fin = update_data.get("date_fin", session.date_fin)
        new_capacite_max = update_data.get("capacite_max", session.capacite_max)
        new_capacite_min = update_data.get(
            "capacite_minimale", session.capacite_minimale
        )

        SessionService._validate_session(
            db, new_debut, new_fin, new_capacite_max, new_capacite_min, session_id
        )

        # Appliquer
        for key, value in update_data.items():
            setattr(session, key, value)

        db.commit()
        db.refresh(session)
        return session

    # delete
    @staticmethod
    def delete(db: Session, session_id: int) -> None:
        session = SessionService.get_by_id(db, session_id)
        db.delete(session)
        db.commit()

    # count students
    @staticmethod
    def count_inscrits(db: Session, session_id: int) -> int:
        return (
            db.scalar(select(func.count()).where(Inscription.session_id == session_id))
            or 0
        )

    # centralized business validation
    @staticmethod
    def _validate_session(
        db: Session,
        date_debut: date,
        date_fin: date,
        capacite_max: int,
        capacite_minimale: int = 1,
        session_id: Optional[int] = None,
    ) -> None:
        """
        Regroupe les règles de cohérence qui ne peuvent pas être
        vérifiées par le schéma Pydantic seul (ou pour garantir la sécurité du service).
        """

        #  Cohérence des dates
        if date_fin <= date_debut:
            raise BadRequestException(
                "La date de fin doit être postérieure à la date de début"
            )

        #  Cohérence capacité max >= capacité minimale
        if capacite_max < capacite_minimale:
            raise BadRequestException(
                f"La capacité maximale ({capacite_max}) doit être supérieure "
                f"ou égale à la capacité minimale ({capacite_minimale})."
            )

        #  Cohérence capacité minimale >= 1
        if capacite_minimale < 1:
            raise BadRequestException("La capacité minimale doit être au moins de 1.")

        #  Cohérence capacité (si session existante)
        if session_id is not None:
            nb_inscrits = SessionService.count_inscrits(db, session_id)
            if capacite_max < nb_inscrits:
                raise BadRequestException(
                    f"Impossible de réduire la capacité : {nb_inscrits} apprenants "
                    f"sont déjà inscrits à cette session."
                )
        elif capacite_max < 1:
            # Sécurité supplémentaire si le schéma est contourné
            raise BadRequestException("La capacité doit être au moins de 1.")
