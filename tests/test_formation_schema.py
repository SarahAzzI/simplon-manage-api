# tests/test_formation_schema.py
import pytest
from pydantic import ValidationError
from app.schemas.formation import FormationCreate, FormationUpdate


class TestFormationCreateSchema:
    """Tests de validation du schema FormationCreate"""

    def test_create_valid_data(self):
        """✅ Données valides → Succès"""
        data = FormationCreate(
            title="Titre Valide",
            description="Description valide de test",
            duration=5,
            level="débutant"  # String directe, Pydantic validera l'enum
        )
        assert data.title == "Titre Valide"
        assert data.duration == 5
        assert data.level == "débutant"

    def test_create_title_too_short(self):
        """❌ Titre < 2 caractères → ValidationError"""
        with pytest.raises(ValidationError):
            FormationCreate(
                title="A",  # 1 char
                description="Description valide de test",
                duration=5,
                level="débutant"
            )

    def test_create_title_too_long(self):
        """❌ Titre > 100 caractères → ValidationError"""
        with pytest.raises(ValidationError):
            FormationCreate(
                title="A" * 101,
                description="Description valide de test",
                duration=5,
                level="débutant"
            )

    def test_create_description_too_short(self):
        """❌ Description < 5 caractères → ValidationError"""
        with pytest.raises(ValidationError):
            FormationCreate(
                title="Titre Valide",
                description="ABC",  # 3 chars
                duration=5,
                level="débutant"
            )

    def test_create_description_too_long(self):
        """❌ Description > 500 caractères → ValidationError"""
        with pytest.raises(ValidationError):
            FormationCreate(
                title="Titre Valide",
                description="A" * 501,
                duration=5,
                level="débutant"
            )

    def test_create_invalid_level(self):
        """❌ Level non valide → ValidationError"""
        with pytest.raises(ValidationError):
            FormationCreate(
                title="Titre Valide",
                description="Description valide de test",
                duration=5,
                level="niveau_invalide"  # Pas dans l'enum
            )

    def test_create_all_valid_levels(self):
        """✅ Tous les niveaux de l'enum sont acceptés"""
        valid_levels = ["débutant", "intermédiaire", "avancé"]
        for level in valid_levels:
            data = FormationCreate(
                title="Titre Valide",
                description="Description valide de test",
                duration=5,
                level=level
            )
            assert data.level == level

    def test_create_duration_zero(self):
        """⚠️ Duration = 0 → Validé par Pydantic, rejeté par le service"""
        data = FormationCreate(
            title="Titre Valide",
            description="Description valide de test",
            duration=0,
            level="débutant"
        )
        assert data.duration == 0  # Pydantic laisse passer

    def test_create_duration_negative(self):
        """⚠️ Duration négative → Validé par Pydantic, rejeté par le service"""
        data = FormationCreate(
            title="Titre Valide",
            description="Description valide de test",
            duration=-5,
            level="débutant"
        )
        assert data.duration == -5  # Pydantic laisse passer


class TestFormationUpdateSchema:
    """Tests de validation du schema FormationUpdate"""

    def test_update_partial_data(self):
        """✅ Update partiel (un seul champ) → Succès"""
        data = FormationUpdate(title="Nouveau Titre")
        assert data.title == "Nouveau Titre"
        assert data.duration is None  # Non modifié

    def test_update_all_fields(self):
        """✅ Update complet → Succès"""
        data = FormationUpdate(
            title="Nouveau Titre",
            description="Nouvelle description valide",
            duration=10,
            level="avancé"
        )
        assert data.title == "Nouveau Titre"
        assert data.duration == 10
        assert data.level == "avancé"

    def test_update_empty_object(self):
        """✅ Update avec objet vide → Succès (rien ne change)"""
        data = FormationUpdate()
        assert data.title is None
        assert data.duration is None
        assert data.description is None
        assert data.level is None

    def test_update_invalid_level(self):
        """❌ Level invalide à l'update → ValidationError"""
        with pytest.raises(ValidationError):
            FormationUpdate(level="niveau_invalide")

    def test_update_title_too_short(self):
        """❌ Titre trop court à l'update → ValidationError"""
        with pytest.raises(ValidationError):
            FormationUpdate(title="A")

    def test_update_description_too_short(self):
        """❌ Description trop courte à l'update → ValidationError"""
        with pytest.raises(ValidationError):
            FormationUpdate(description="ABC")