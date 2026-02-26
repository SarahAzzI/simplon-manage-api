from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func

from app.models.session import SessionFormation
from app.models.inscription import Inscription
from app.models.user import User, Role  # ← user.py
from app.schemas.session import SessionCreate, SessionUpdate
from app.core.exceptions import NotFoundException, BadRequestException


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
            db, data.date_debut, data.date_fin, data.capacite_max
        )

        # Créer
        session = SessionFormation(**data.model_dump())
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    # ── MODIFIER ──
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

        # Valider la cohérence métier (dates et capacité)
        new_debut = update_data.get("date_debut", session.date_debut)
        new_fin = update_data.get("date_fin", session.date_fin)
        new_capacite = update_data.get("capacite_max", session.capacite_max)

        SessionService._validate_session(
            db, new_debut, new_fin, new_capacite, session_id
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
            db.scalar(select(func.count()).where(Inscription.session_id == session_id))
            or 0
        )

    # ── VALIDATION MÉTIER CENTRALISÉE ──
    @staticmethod
    def _validate_session(
        db: Session,
        date_debut: date,
        date_fin: date,
        capacite_max: int,
        session_id: int | None = None,
    ) -> None:
        """
        Regroupe les règles de cohérence qui ne peuvent pas être
        vérifiées par le schéma Pydantic seul (ou pour garantir la sécurité du service).
        """

        # 1. Cohérence des dates
        if date_fin <= date_debut:
            raise BadRequestException(
                "La date de fin doit être postérieure à la date de début"
            )

        # 2. Cohérence capacité (si session existante)
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
