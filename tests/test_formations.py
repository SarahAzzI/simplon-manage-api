# tests/test_formation_service.py
import pytest
import uuid
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.services.formation import FormationService
from app.schemas.formation import FormationCreate, FormationUpdate
from app.core.exceptions import NotFoundException
from app.models.formation import Formation


# ─────────────────────────────────────────────────────────────
# FIXTURE
# ─────────────────────────────────────────────────────────────
@pytest.fixture
def make_formation_data():
    """Factory pour données valides"""
    def _make(title: str = None, **overrides):
        data = {
            "title": title or f"Formation {uuid.uuid4().hex[:8]}",
            "description": "Description valide de test",
            "duration": 5,
            "level": "débutant",
        }
        data.update(overrides)
        return FormationCreate(**data)
    return _make


# ─────────────────────────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────────────────────────
class TestCreate:
    def test_create_success(self, db, make_formation_data):
        data = make_formation_data(title="Formation Test")
        result = FormationService.create(db, data)
        assert result.id is not None
        assert result.title == "Formation Test"

    def test_create_invalid_duration_negative(self, db, make_formation_data):
        data = make_formation_data(duration=-1)  # ← Override duration
        with pytest.raises(HTTPException) as exc_info:
            FormationService.create(db, data)
        assert exc_info.value.status_code == 400

    def test_create_invalid_duration_zero(self, db, make_formation_data):
        data = make_formation_data(duration=0)  # ← Override duration
        with pytest.raises(HTTPException) as exc_info:
            FormationService.create(db, data)
        assert exc_info.value.status_code == 400

    def test_create_duplicate_title(self, db, make_formation_data):
        FormationService.create(db, make_formation_data(title="Dupliqué"))
        with pytest.raises(HTTPException) as exc_info:
            FormationService.create(db, make_formation_data(title="Dupliqué"))
        assert exc_info.value.status_code == 400

    def test_create_integrity_error(self, db, make_formation_data, mocker):
        """❌ IntegrityError DB → Rollback"""
        # Mocker commit ET rollback
        mock_commit = mocker.patch.object(db, 'commit', side_effect=IntegrityError("", "", ""))
        mock_rollback = mocker.patch.object(db, 'rollback')
        
        with pytest.raises(HTTPException) as exc_info:
            FormationService.create(db, make_formation_data())
        
        assert exc_info.value.status_code == 400
        mock_commit.assert_called_once()  # ✅ Utiliser la référence du mock
        mock_rollback.assert_called_once()  # ✅ Utiliser la référence du mock

    def test_create_returns_formation_object(self, db, make_formation_data):
        data = make_formation_data(title="Test Complet", duration=10, level="avancé")
        result = FormationService.create(db, data)
        assert isinstance(result, Formation)
        assert result.duration == 10
        assert result.level == "avancé"


# ─────────────────────────────────────────────────────────────
# GET_BY_ID
# ─────────────────────────────────────────────────────────────
class TestGetById:
    def test_get_by_id_found(self, db, make_formation_data):
        created = FormationService.create(db, make_formation_data(title="Trouvée"))
        result = FormationService.get_by_id(db, created.id)
        assert result.id == created.id
        assert result.title == "Trouvée"

    def test_get_by_id_not_found(self, db):
        with pytest.raises(NotFoundException):
            FormationService.get_by_id(db, 99999)


# ─────────────────────────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────────────────────────
class TestUpdate:
    def test_update_success(self, db, make_formation_data):
        created = FormationService.create(db, make_formation_data(title="Avant"))
        result = FormationService.update(db, created.id, FormationUpdate(title="Après"))
        assert result.title == "Après"

    def test_update_not_found(self, db):
        with pytest.raises(NotFoundException):
            FormationService.update(db, 99999, FormationUpdate(title="Test"))

    def test_update_invalid_duration(self, db, make_formation_data):
        created = FormationService.create(db, make_formation_data())
        with pytest.raises(HTTPException) as exc_info:
            FormationService.update(db, created.id, FormationUpdate(duration=-1))
        assert exc_info.value.status_code == 400

    def test_update_duplicate_title(self, db, make_formation_data):
        f1 = FormationService.create(db, make_formation_data(title="Titre A"))
        f2 = FormationService.create(db, make_formation_data(title="Titre B"))
        with pytest.raises(HTTPException) as exc_info:
            FormationService.update(db, f2.id, FormationUpdate(title="Titre A"))
        assert exc_info.value.status_code == 400

    def test_update_same_title_success(self, db, make_formation_data):
        created = FormationService.create(db, make_formation_data(title="Même Titre"))
        result = FormationService.update(db, created.id, FormationUpdate(title="Même Titre"))
        assert result.title == "Même Titre"

    def test_update_partial_fields(self, db, make_formation_data):
        created = FormationService.create(db, make_formation_data(title="Original"))
        result = FormationService.update(db, created.id, FormationUpdate(duration=20))
        assert result.title == "Original"
        assert result.duration == 20

    def test_update_integrity_error(self, db, make_formation_data, mocker):
        """❌ IntegrityError → Rollback"""
        created = FormationService.create(db, make_formation_data())
        
        mock_commit = mocker.patch.object(db, 'commit', side_effect=IntegrityError("", "", ""))
        mock_rollback = mocker.patch.object(db, 'rollback')
        
        with pytest.raises(HTTPException) as exc_info:
            FormationService.update(db, created.id, FormationUpdate(title="Test"))
        
        assert exc_info.value.status_code == 400
        mock_commit.assert_called_once()
        mock_rollback.assert_called_once()


# ─────────────────────────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────────────────────────
class TestDelete:
    def test_delete_success(self, db, make_formation_data):
        created = FormationService.create(db, make_formation_data(title="À supprimer"))
        FormationService.delete(db, created.id)
        with pytest.raises(NotFoundException):
            FormationService.get_by_id(db, created.id)

    def test_delete_not_found(self, db):
        with pytest.raises(NotFoundException):
            FormationService.delete(db, 99999)

    def test_delete_sqlalchemy_error(self, db, make_formation_data, mocker):
        """❌ SQLAlchemyError → 500 + Rollback"""
        created = FormationService.create(db, make_formation_data())
        
        mock_commit = mocker.patch.object(db, 'commit', side_effect=SQLAlchemyError("Error"))
        mock_rollback = mocker.patch.object(db, 'rollback')
        
        with pytest.raises(HTTPException) as exc_info:
            FormationService.delete(db, created.id)
        
        assert exc_info.value.status_code == 500
        mock_commit.assert_called_once()
        mock_rollback.assert_called_once()


# ─────────────────────────────────────────────────────────────
# LIST
# ─────────────────────────────────────────────────────────────
class TestList:
    def test_list_empty(self, db):
        results = FormationService.list(db)
        assert len(results) == 0

    def test_list_with_data(self, db, make_formation_data):
        for i in range(5):
            FormationService.create(db, make_formation_data(title=f"F{i}"))
        results = FormationService.list(db)
        assert len(results) == 5

    def test_list_pagination(self, db, make_formation_data):
        for i in range(10):
            FormationService.create(db, make_formation_data(title=f"F{i}"))
        page1 = FormationService.list(db, skip=0, limit=3)
        page2 = FormationService.list(db, skip=3, limit=3)
        assert len(page1) == 3
        assert len(page2) == 3
        assert page1[0].id != page2[0].id


# ─────────────────────────────────────────────────────────────
# GET_TOTAL
# ─────────────────────────────────────────────────────────────
class TestGetTotal:
    def test_get_total_zero(self, db):
        assert FormationService.get_total(db) == 0

    def test_get_total_with_data(self, db, make_formation_data):
        for i in range(7):
            FormationService.create(db, make_formation_data(title=f"F{i}"))
        assert FormationService.get_total(db) == 7