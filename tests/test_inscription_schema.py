# tests/test_inscription_schema.py
import pytest
from pydantic import ValidationError
from app.schemas.inscription import InscriptionCreate, InscriptionUpdate


class TestInscriptionCreateSchema:
    """Tests de validation du schema InscriptionCreate"""

    def test_create_valid_data(self):
        """✅ Données valides → Succès"""
        data = InscriptionCreate(
            session_id=1,
            user_id=1,
            statut="en_attente"  # Valeur string de l'enum
        )
        assert data.session_id == 1
        assert data.user_id == 1
        assert data.statut == "en_attente"

    def test_create_session_id_zero(self):
        """❌ session_id = 0 → ValidationError"""
        with pytest.raises(ValidationError):
            InscriptionCreate(
                session_id=0,  # ❌ Field(gt=0)
                user_id=1,
                statut="en_attente"
            )

    def test_create_session_id_negative(self):
        """❌ session_id négatif → ValidationError"""
        with pytest.raises(ValidationError):
            InscriptionCreate(
                session_id=-1,
                user_id=1,
                statut="en_attente"
            )

    def test_create_user_id_zero(self):
        """❌ user_id = 0 → ValidationError"""
        with pytest.raises(ValidationError):
            InscriptionCreate(
                session_id=1,
                user_id=0,  # ❌ Field(gt=0)
                statut="en_attente"
            )

    def test_create_invalid_statut(self):
        """❌ Statut non valide → ValidationError"""
        with pytest.raises(ValidationError):
            InscriptionCreate(
                session_id=1,
                user_id=1,
                statut="statut_invalide"  # Pas dans StatutInscription
            )

    def test_create_all_valid_statuts(self):
        """✅ Tous les statuts valides sont acceptés"""
        valid_statuts = ["en_attente", "confirmé", "annulé", "terminé"]
        for statut in valid_statuts:
            data = InscriptionCreate(
                session_id=1,
                user_id=1,
                statut=statut
            )
            assert data.statut == statut

    def test_create_missing_required_field(self):
        """❌ Champ requis manquant → ValidationError"""
        with pytest.raises(ValidationError):
            InscriptionCreate(
                session_id=1,
                # user_id manquant ❌
                statut="en_attente"
            )


class TestInscriptionUpdateSchema:
    """Tests de validation du schema InscriptionUpdate"""

    def test_update_partial_data(self):
        """✅ Update partiel (un seul champ) → Succès"""
        data = InscriptionUpdate(statut="confirmé")
        assert data.statut == "confirmé"

    def test_update_empty_object(self):
        """✅ Update avec objet vide → Succès (rien ne change)"""
        data = InscriptionUpdate()
        assert data.statut is None

    def test_update_invalid_statut(self):
        """❌ Statut invalide à l'update → ValidationError"""
        with pytest.raises(ValidationError):
            InscriptionUpdate(statut="statut_invalide")

    def test_update_all_valid_statuts(self):
        """✅ Tous les statuts valides à l'update"""
        valid_statuts = ["en_attente", "confirmé", "annulé", "terminé"]
        for statut in valid_statuts:
            data = InscriptionUpdate(statut=statut)
            assert data.statut == statut