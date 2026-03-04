# tests/test_inscription_service.py
import pytest
import uuid
from datetime import date, datetime, timezone

from app.services.inscription import InscriptionService
from app.schemas.inscription import InscriptionCreate, InscriptionUpdate
from app.core.exceptions import NotFoundException, BadRequestException
from app.models.inscription import Inscription
from app.models.user import User
from app.models.session import SessionFormation, SessionStatus
from app.models.formation import Formation
from app.core.role import Role


# ─────────────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────────────
@pytest.fixture
def create_formation(db):
    """Crée une formation"""
    def _create(title: str = None, **overrides):
        formation = Formation(
            title=title or f"Formation {uuid.uuid4().hex[:8]}",
            description="Description valide de test",
            duration=5,
            level="débutant",
            **overrides
        )
        db.add(formation)
        db.commit()
        db.refresh(formation)
        return formation
    return _create


@pytest.fixture
def create_student(db):
    """Crée un utilisateur STUDENT avec email unique via uuid"""
    def _create(email: str = None, **overrides):
        if email is None:
            email = f"student_{uuid.uuid4().hex[:8]}@test.com"
        user = User(
            email=email,
            surname="Nom",
            name="Prénom",
            birth_date=datetime(2000, 1, 1, tzinfo=timezone.utc),
            role=Role.STUDENT,
            **overrides
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return _create


@pytest.fixture
def create_teacher(db):
    """Crée un utilisateur TEACHER (formateur) avec email unique"""
    def _create(email: str = None, **overrides):
        if email is None:
            email = f"teacher_{uuid.uuid4().hex[:8]}@test.com"
        user = User(
            email=email,
            surname="Nom",
            name="Prénom",
            birth_date=datetime(2000, 1, 1, tzinfo=timezone.utc),
            role=Role.TEACHER,
            **overrides
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return _create


@pytest.fixture
def create_session(db, create_formation, create_teacher):
    """Crée une session de formation"""
    def _create(capacite_max: int = 10, **overrides):
        formation = create_formation()
        teacher = create_teacher()
        session = SessionFormation(
            formation_id=formation.id,
            formateur_id=teacher.id,
            date_debut=date(2025, 1, 1),
            date_fin=date(2025, 12, 31),
            capacite_max=capacite_max,
            statut=SessionStatus.PLANIFIEE,
            **overrides
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    return _create


@pytest.fixture
def make_inscription_data():
    """Factory pour données d'inscription valides"""
    def _make(session_id: int, user_id: int, **overrides):
        return InscriptionCreate(
            session_id=session_id,
            user_id=user_id,
            statut="en_attente",
            **overrides
        )
    return _make


# ─────────────────────────────────────────────────────────────
# CREATE - Tests de création
# ─────────────────────────────────────────────────────────────
class TestCreate:
    def test_create_success(self, db, create_student, create_session, make_inscription_data):
        """✅ Création valide"""
        student = create_student()
        session = create_session()
        data = make_inscription_data(session_id=session.id, user_id=student.id)
        
        result = InscriptionService.create(db, data)
        
        assert result.id is not None
        assert result.user_id == student.id
        assert result.session_id == session.id
        assert result.statut == "en_attente"

    def test_create_user_not_found(self, db, create_session, make_inscription_data):
        """❌ User inexistant → NotFoundException"""
        session = create_session()
        data = make_inscription_data(session_id=session.id, user_id=99999)
        
        with pytest.raises(NotFoundException) as exc_info:
            InscriptionService.create(db, data)
        
        assert "Apprenant" in exc_info.value.detail

    def test_create_user_not_student(self, db, create_teacher, create_session, make_inscription_data):
        """❌ User n'est pas STUDENT → BadRequestException"""
        teacher = create_teacher()
        session = create_session()
        data = make_inscription_data(session_id=session.id, user_id=teacher.id)
        
        with pytest.raises(BadRequestException) as exc_info:
            InscriptionService.create(db, data)
        
        assert "n'est pas un apprenant" in exc_info.value.detail

    def test_create_session_not_found(self, db, create_student, make_inscription_data):
        """❌ Session inexistante → NotFoundException"""
        student = create_student()
        data = make_inscription_data(session_id=99999, user_id=student.id)
        
        with pytest.raises(NotFoundException) as exc_info:
            InscriptionService.create(db, data)
        
        assert "Session" in exc_info.value.detail

    def test_create_already_enrolled_same_session(self, db, create_student, create_session, make_inscription_data):
        """❌ Déjà inscrit à CETTE session → BadRequestException"""
        student = create_student()
        session = create_session()
        data = make_inscription_data(session_id=session.id, user_id=student.id)
        
        InscriptionService.create(db, data)
        
        with pytest.raises(BadRequestException) as exc_info:
            InscriptionService.create(db, data)
        
        assert "déjà inscrit" in exc_info.value.detail.lower() or "une seule session" in exc_info.value.detail.lower()

    def test_create_student_already_in_another_session(self, db, create_student, create_session, make_inscription_data):
        """
        ❌ Étudiant déjà inscrit à une AUTRE session → BadRequestException
        Règle métier : un étudiant ne peut suivre qu'UNE session à la fois
        """
        student = create_student()
        session1 = create_session(capacite_max=10)
        session2 = create_session(capacite_max=10)
        
        InscriptionService.create(db, make_inscription_data(session_id=session1.id, user_id=student.id))
        
        with pytest.raises(BadRequestException) as exc_info:
            InscriptionService.create(db, make_inscription_data(session_id=session2.id, user_id=student.id))
        
        assert "une seule session" in exc_info.value.detail.lower() or "déjà inscrit" in exc_info.value.detail.lower()

    def test_create_session_full(self, db, create_student, create_session, make_inscription_data, mocker):
        """❌ Session complète → BadRequestException"""
        student = create_student()
        session = create_session(capacite_max=2)
        data = make_inscription_data(session_id=session.id, user_id=student.id)
        
        mocker.patch(
            'app.services.session.SessionService.count_inscrits',
            return_value=2
        )
        
        with pytest.raises(BadRequestException) as exc_info:
            InscriptionService.create(db, data)
        
        assert "complète" in exc_info.value.detail.lower()


# ─────────────────────────────────────────────────────────────
# GET_ALL - Tests de récupération globale
# ─────────────────────────────────────────────────────────────
class TestGetAll:
    def test_get_all_empty(self, db):
        """✅ Liste vide"""
        results = InscriptionService.get_all(db)
        assert len(results) == 0

    def test_get_all_with_data(self, db, create_student, create_session):
        """✅ Liste avec données (étudiants uniques)"""
        session = create_session()
        
        for i in range(3):
            student = create_student()
            inscription = Inscription(user_id=student.id, session_id=session.id, statut="confirmé")
            db.add(inscription)
        db.commit()
        
        results = InscriptionService.get_all(db)
        assert len(results) == 3
        assert len(set(r.user_id for r in results)) == 3

    def test_get_all_pagination(self, db, create_student, create_session):
        """✅ Pagination avec étudiants uniques"""
        session = create_session()
        
        for i in range(10):
            student = create_student()
            inscription = Inscription(user_id=student.id, session_id=session.id, statut="confirmé")
            db.add(inscription)
        db.commit()
        
        page1 = InscriptionService.get_all(db, skip=0, limit=3)
        page2 = InscriptionService.get_all(db, skip=3, limit=3)
        
        assert len(page1) == 3
        assert len(page2) == 3
        assert page1[0].id != page2[0].id


# ─────────────────────────────────────────────────────────────
# GET_BY_SESSION - Tests par session
# ─────────────────────────────────────────────────────────────
class TestGetBySession:
    def test_get_by_session_not_found(self, db):
        """❌ Session inexistante → NotFoundException"""
        with pytest.raises(NotFoundException) as exc_info:
            InscriptionService.get_by_session(db, 99999)
        assert "Session" in exc_info.value.detail

    def test_get_by_session_success(self, db, create_student, create_session):
        """✅ Récupérer inscriptions d'une session (étudiants différents)"""
        session = create_session()
        
        for i in range(3):
            student = create_student()
            inscription = Inscription(user_id=student.id, session_id=session.id, statut="confirmé")
            db.add(inscription)
        db.commit()
        
        results = InscriptionService.get_by_session(db, session.id)
        assert len(results) == 3
        assert all(r.session_id == session.id for r in results)
        assert len(set(r.user_id for r in results)) == 3


# ─────────────────────────────────────────────────────────────
# COUNT_BY_SESSION - Tests de comptage par session
# ─────────────────────────────────────────────────────────────
class TestCountBySession:
    def test_count_by_session_zero(self, db, create_session):
        """✅ Comptage = 0"""
        session = create_session()
        count = InscriptionService.count_by_session(db, session.id)
        assert count == 0

    def test_count_by_session_with_data(self, db, create_student, create_session):
        """✅ Comptage avec plusieurs étudiants dans la même session"""
        session = create_session()
        
        for i in range(5):
            student = create_student()
            inscription = Inscription(user_id=student.id, session_id=session.id, statut="confirmé")
            db.add(inscription)
        db.commit()
        
        count = InscriptionService.count_by_session(db, session.id)
        assert count == 5


# ─────────────────────────────────────────────────────────────
# GET_BY_STUDENT - Tests par étudiant
# ─────────────────────────────────────────────────────────────
class TestGetByStudent:
    def test_get_by_student_not_found(self, db):
        """❌ Étudiant inexistant → NotFoundException"""
        with pytest.raises(NotFoundException) as exc_info:
            InscriptionService.get_by_student(db, 99999)
        assert "Apprenant" in exc_info.value.detail

    def test_get_by_student_success(self, db, create_student, create_session):
        """✅ Récupérer l'unique inscription d'un étudiant"""
        student = create_student()
        session = create_session()
        
        inscription = Inscription(user_id=student.id, session_id=session.id, statut="confirmé")
        db.add(inscription)
        db.commit()
        
        results = InscriptionService.get_by_student(db, student.id)
        assert len(results) == 1
        assert results[0].user_id == student.id

    def test_get_by_student_cannot_have_multiple_sessions(self, db, create_student, create_session):
        """✅ Vérifie la règle métier : un étudiant ne peut pas avoir 2 inscriptions"""
        student = create_student()
        session1 = create_session()
        session2 = create_session()
        
        InscriptionService.create(db, InscriptionCreate(
            session_id=session1.id, user_id=student.id, statut="en_attente"
        ))
        
        with pytest.raises(BadRequestException):
            InscriptionService.create(db, InscriptionCreate(
                session_id=session2.id, user_id=student.id, statut="en_attente"
            ))
        
        results = InscriptionService.get_by_student(db, student.id)
        assert len(results) == 1


# ─────────────────────────────────────────────────────────────
# COUNT_BY_STUDENT - Tests de comptage par étudiant
# ─────────────────────────────────────────────────────────────
class TestCountByStudent:
    def test_count_by_student_zero(self, db, create_student):
        """✅ Comptage = 0"""
        student = create_student()
        count = InscriptionService.count_by_student(db, student.id)
        assert count == 0

    def test_count_by_student_with_data(self, db, create_student, create_session):
        """✅ Comptage pour un étudiant (toujours 0 ou 1)"""
        student = create_student()
        session = create_session()
        
        inscription = Inscription(user_id=student.id, session_id=session.id, statut="confirmé")
        db.add(inscription)
        db.commit()
        
        count = InscriptionService.count_by_student(db, student.id)
        assert count == 1


# ─────────────────────────────────────────────────────────────
# DELETE - Tests de suppression
# ─────────────────────────────────────────────────────────────
class TestDelete:
    def test_delete_success(self, db, create_student, create_session):
        """✅ Suppression valide"""
        student = create_student()
        session = create_session()
        
        inscription = Inscription(user_id=student.id, session_id=session.id, statut="confirmé")
        db.add(inscription)
        db.commit()
        
        InscriptionService.delete(db, inscription.id)
        
        assert db.get(Inscription, inscription.id) is None

    def test_delete_not_found(self, db):
        """❌ ID inexistant → NotFoundException"""
        with pytest.raises(NotFoundException) as exc_info:
            InscriptionService.delete(db, 99999)
        assert "Inscription" in exc_info.value.detail


# ─────────────────────────────────────────────────────────────
# UPDATE - Tests de mise à jour
# ─────────────────────────────────────────────────────────────
class TestUpdate:
    def test_update_success(self, db, create_student, create_session):
        """✅ Update valide (changer le statut)"""
        student = create_student()
        session = create_session()
        
        inscription = Inscription(user_id=student.id, session_id=session.id, statut="en_attente")
        db.add(inscription)
        db.commit()
        
        result = InscriptionService.update(db, inscription.id, InscriptionUpdate(statut="confirmé"))
        
        assert result.statut == "confirmé"

    def test_update_not_found(self, db):
        """❌ ID inexistant → NotFoundException"""
        with pytest.raises(NotFoundException) as exc_info:
            InscriptionService.update(db, 99999, InscriptionUpdate(statut="confirmé"))
        assert "Inscription" in exc_info.value.detail

    def test_update_partial_fields(self, db, create_student, create_session):
        """✅ Update partiel (seulement statut)"""
        student = create_student()
        session = create_session()
        
        inscription = Inscription(user_id=student.id, session_id=session.id, statut="en_attente")
        db.add(inscription)
        db.commit()
        
        result = InscriptionService.update(db, inscription.id, InscriptionUpdate(statut="annulé"))
        
        assert result.statut == "annulé"
        assert result.user_id == student.id
        assert result.session_id == session.id