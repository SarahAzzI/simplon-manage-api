import pytest
from datetime import datetime
from app.models.user import Role


def test_create_user(client, db):
    response = client.post(
        "/utilisateurs/",
        json={
            "email": "test@example.com",
            "surname": "Doe",
            "name": "Jane",
            "birth_date": "1990-05-15T00:00:00",
            "role": "Etudiant",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "Etudiant"
    assert data["is_active"] is True
    assert "id" in data


def test_get_user_by_id(client, db):
    create_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "get@test.com",
            "surname": "Test",
            "name": "User",
            "birth_date": "1985-01-01T00:00:00",
            "role": "Formateur",
        },
    )
    user_id = create_resp.json()["id"]

    response = client.get(f"/utilisateurs/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "get@test.com"


def test_list_users(client, db):
    # Add two users
    client.post(
        "/utilisateurs/",
        json={
            "email": "u1@test.com",
            "surname": "One",
            "name": "User",
            "birth_date": "1990-01-01T00:00:00",
            "role": "Etudiant",
        },
    )
    client.post(
        "/utilisateurs/",
        json={
            "email": "u2@test.com",
            "surname": "Two",
            "name": "User",
            "birth_date": "1990-01-01T00:00:00",
            "role": "Etudiant",
        },
    )

    response = client.get("/utilisateurs/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    assert len(data["items"]) >= 2
    assert "page" in data
    assert "pages" in data


def test_update_user(client, db):
    create_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "upd@test.com",
            "surname": "Old",
            "name": "Name",
            "birth_date": "1990-01-01T00:00:00",
            "role": "Etudiant",
        },
    )
    user_id = create_resp.json()["id"]

    response = client.patch(
        f"/utilisateurs/{user_id}", json={"name": "NewName", "surname": "NewSurname"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "NewName"
    assert data["surname"] == "NewSurname"


def test_soft_delete_user(client, db):
    create_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "soft@test.com",
            "surname": "Soft",
            "name": "Del",
            "birth_date": "1990-01-01T00:00:00",
            "role": "Etudiant",
        },
    )
    user_id = create_resp.json()["id"]

    response = client.delete(f"/utilisateurs/{user_id}")
    assert response.status_code == 200
    assert response.json()["delete_type"] == "soft"

    # Verify is_active is False
    get_resp = client.get(f"/utilisateurs/{user_id}")
    assert get_resp.json()["is_active"] is False


def test_hard_delete_user(client, db):
    create_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "hard@test.com",
            "surname": "Hard",
            "name": "Del",
            "birth_date": "1990-01-01T00:00:00",
            "role": "Etudiant",
        },
    )
    user_id = create_resp.json()["id"]

    response = client.delete(f"/utilisateurs/{user_id}?hard_delete=true")
    assert response.status_code == 200
    assert response.json()["delete_type"] == "hard"

    # Verify truly deleted
    get_resp = client.get(f"/utilisateurs/{user_id}")
    assert get_resp.status_code == 404


def test_create_user_invalid_email(client, db):
    """Email invalide doit échouer"""
    response = client.post(
        "/utilisateurs/",
        json={
            "email": "pas-un-email",
            "surname": "Test",
            "name": "User",
            "birth_date": "1990-01-01T00:00:00",
            "role": "Etudiant",
        },
    )
    assert response.status_code == 422  # Erreur de validation


def test_create_user_missing_field(client, db):
    """Champ obligatoire manquant doit échouer"""
    response = client.post(
        "/utilisateurs/",
        json={
            "email": "test@test.com",
            "name": "User",
            "birth_date": "1990-01-01T00:00:00",
            "role": "Etudiant",
        },
    )
    assert response.status_code == 422


def test_create_user_invalid_role(client, db):
    """Rôle invalide doit échouer"""
    response = client.post(
        "/utilisateurs/",
        json={
            "email": "role@test.com",
            "surname": "Test",
            "name": "User",
            "birth_date": "1990-01-01T00:00:00",
            "role": "RoleInvalide",
        },
    )
    assert response.status_code == 422


def test_list_users_pagination(client, db):
    """Test page et size"""
    for i in range(5):
        client.post(
            "/utilisateurs/",
            json={
                "email": f"page{i}@test.com",
                "surname": f"User{i}",
                "name": "Test",
                "birth_date": "1990-01-01T00:00:00",
                "role": "Etudiant",
            },
        )

    response = client.get("/utilisateurs/?page=1&size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["pages"] == 3

    response = client.get("/utilisateurs/?page=3&size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1


def test_create_user_all_roles(client, db):
    """Test création avec chaque rôle"""
    roles = ["Etudiant", "Formateur", "Administrateur"]

    for i, role in enumerate(roles):
        response = client.post(
            "/utilisateurs/",
            json={
                "email": f"role{i}@test.com",
                "surname": "Test",
                "name": "User",
                "birth_date": "1990-01-01T00:00:00",
                "role": role,
            },
        )
        assert response.status_code == 201
        assert response.json()["role"] == role


def test_update_user_partial(client, db):
    """Test modification d'un seul champ"""
    create_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "partial@test.com",
            "surname": "Original",
            "name": "Name",
            "birth_date": "1990-01-01T00:00:00",
            "role": "Etudiant",
        },
    )
    user_id = create_resp.json()["id"]
    original_surname = create_resp.json()["surname"]

    # Modifie seulement le name
    response = client.patch(f"/utilisateurs/{user_id}", json={"name": "NewName"})

    assert response.status_code == 200
    assert response.json()["name"] == "NewName"
    assert response.json()["surname"] == original_surname  # Non modifié


def test_create_user_duplicate_email(client, db):
    """Email en double doit retourner 400"""
    user_data = {
        "email": "dup@test.com",
        "surname": "Dup",
        "name": "User",
        "birth_date": "1990-01-01T00:00:00",
        "role": "Etudiant",
    }
    # Créer le premier
    client.post("/utilisateurs/", json=user_data)

    # Créer le deuxième avec le même email
    response = client.post("/utilisateurs/", json=user_data)
    assert response.status_code == 400
    assert "existe déjà" in response.json()["detail"]


def test_get_user_not_found(client, db):
    """Utilisateur inexistant doit retourner 404"""
    response = client.get("/utilisateurs/99999")
    assert response.status_code == 404
    assert "Utilisateur" in response.json()["detail"]
