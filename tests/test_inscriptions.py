import pytest
from datetime import date, datetime, timedelta
from app.models.user import  User
from app.models.formation import Formation
from app.models.session import SessionFormation
from app.core.role import Role

def test_create_inscription(client, db):
    # 1. Créer une formation
    formation = Formation(
        title="Python Expert",
        description="Advanced Python",
        duration=35,
        level="avancé",
    )
    db.add(formation)

    # 2. Créer un formateur
    formateur = User(
        email="teacher@test.com",
        surname="Doe",
        name="John",
        birth_date=datetime(1980, 1, 1),
        role=Role.TEACHER,
    )
    db.add(formateur)

    # 3. Créer un apprenant
    apprenant = User(
        email="student@test.com",
        surname="Smith",
        name="Jane",
        birth_date=datetime(2000, 1, 1),
        role=Role.STUDENT,
    )
    db.add(apprenant)

    db.commit()

    # 4. Créer une session
    session = SessionFormation(
        formation_id=formation.id,
        formateur_id=formateur.id,
        date_debut=date.today(),
        date_fin=date.today() + timedelta(days=5),
        capacite_max=10,
    )
    db.add(session)
    db.commit()

    # 5. Tester l'inscription
    response = client.post(
        "/inscriptions/", json={"user_id": apprenant.id, "session_id": session.id}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == apprenant.id
    assert data["session_id"] == session.id
    assert data["statut"] == "en_attente"


def test_create_inscription_already_registered(client, db):
    # Setup similar to above
    formation = Formation(
        title="Python Expert",
        description="Advanced Python",
        duration=35,
        level="avancé",
    )
    db.add(formation)
    formateur = User(
        email="teacher2@test.com",
        surname="Doe",
        name="John",
        birth_date=datetime(1980, 1, 1),
        role=Role.TEACHER,
    )
    db.add(formateur)
    apprenant = User(
        email="student2@test.com",
        surname="Smith",
        name="Jane",
        birth_date=datetime(2000, 1, 1),
        role=Role.STUDENT,
    )
    db.add(apprenant)
    db.commit()
    session = SessionFormation(
        formation_id=formation.id,
        formateur_id=formateur.id,
        date_debut=date.today(),
        date_fin=date.today() + timedelta(days=5),
        capacite_max=10,
    )
    db.add(session)
    db.commit()

    # Première inscription
    client.post(
        "/inscriptions/", json={"user_id": apprenant.id, "session_id": session.id}
    )

    # Deuxième inscription (doublon)
    response = client.post(
        "/inscriptions/", json={"user_id": apprenant.id, "session_id": session.id}
    )

    assert response.status_code == 400
    assert "déjà inscrit" in response.json()["detail"]


def test_create_inscription_session_full(client, db):
    formation = Formation(
        title="Python Expert",
        description="Advanced Python",
        duration=35,
        level="avancé",
    )
    db.add(formation)
    formateur = User(
        email="teacher3@test.com",
        surname="Doe",
        name="John",
        birth_date=datetime(1980, 1, 1),
        role=Role.TEACHER,
    )
    db.add(formateur)
    apprenant1 = User(
        email="student3@test.com",
        surname="Smith",
        name="Jane",
        birth_date=datetime(2000, 1, 1),
        role=Role.STUDENT,
    )
    apprenant2 = User(
        email="student4@test.com",
        surname="Doe",
        name="John",
        birth_date=datetime(1995, 1, 1),
        role=Role.STUDENT,
    )
    db.add_all([apprenant1, apprenant2])
    db.commit()

    # Session avec capacité 1
    session = SessionFormation(
        formation_id=formation.id,
        formateur_id=formateur.id,
        date_debut=date.today(),
        date_fin=date.today() + timedelta(days=5),
        capacite_max=1,
    )
    db.add(session)
    db.commit()

    # Première inscription OK
    client.post(
        "/inscriptions/", json={"user_id": apprenant1.id, "session_id": session.id}
    )

    # Deuxième inscription KO (session complète)
    response = client.post(
        "/inscriptions/", json={"user_id": apprenant2.id, "session_id": session.id}
    )

    assert response.status_code == 400
    assert "complète" in response.json()["detail"]


def test_delete_inscription(client, db):
    formation = Formation(
        title="Python Expert",
        description="Advanced Python",
        duration=35,
        level="avancé",
    )
    db.add(formation)
    formateur = User(
        email="teacher4@test.com",
        surname="Doe",
        name="John",
        birth_date=datetime(1980, 1, 1),
        role=Role.TEACHER,
    )
    db.add(formateur)
    apprenant = User(
        email="student5@test.com",
        surname="Smith",
        name="Jane",
        birth_date=datetime(2000, 1, 1),
        role=Role.STUDENT,
    )
    db.add(apprenant)
    db.commit()
    session = SessionFormation(
        formation_id=formation.id,
        formateur_id=formateur.id,
        date_debut=date.today(),
        date_fin=date.today() + timedelta(days=5),
        capacite_max=10,
    )
    db.add(session)
    db.commit()

    # Inscrire
    response = client.post(
        "/inscriptions/", json={"user_id": apprenant.id, "session_id": session.id}
    )
    inscription_id = response.json()["id"]

    # Supprimer
    del_response = client.delete(f"/inscriptions/{inscription_id}")
    assert del_response.status_code == 204

    # Vérifier que c'est supprimé
    get_response = client.get(f"/inscriptions/session/{session.id}")
    assert len(get_response.json()["items"]) == 0


def test_create_inscription_non_student(client, db):
    """Un formateur ou admin ne peut pas s'inscrire comme apprenant"""
    formation = Formation(
        title="Python Expert",
        description="Advanced Python",
        duration=35,
        level="avancé",
    )
    db.add(formation)
    formateur = User(
        email="teacher6@test.com",
        surname="Doe",
        name="John",
        birth_date=datetime(1980, 1, 1),
        role=Role.TEACHER,
    )
    db.add(formateur)
    db.commit()
    session = SessionFormation(
        formation_id=formation.id,
        formateur_id=formateur.id,
        date_debut=date.today(),
        date_fin=date.today() + timedelta(days=5),
        capacite_max=10,
    )
    db.add(session)
    db.commit()

    # Essayer d'inscrire un formateur (pas un apprenant)
    response = client.post(
        "/inscriptions/", json={"user_id": formateur.id, "session_id": session.id}
    )
    assert response.status_code == 400
    assert "pas un apprenant" in response.json()["detail"]


def test_get_sessions_by_student(client, db):
    """Lister les sessions d'un apprenant"""
    formation = Formation(
        title="Python Expert",
        description="Advanced Python",
        duration=35,
        level="avancé",
    )
    db.add(formation)
    formateur = User(
        email="teacher7@test.com",
        surname="Doe",
        name="John",
        birth_date=datetime(1980, 1, 1),
        role=Role.TEACHER,
    )
    apprenant = User(
        email="student7@test.com",
        surname="Smith",
        name="Jane",
        birth_date=datetime(2000, 1, 1),
        role=Role.STUDENT,
    )
    db.add_all([formateur, apprenant])
    db.commit()
    session = SessionFormation(
        formation_id=formation.id,
        formateur_id=formateur.id,
        date_debut=date.today(),
        date_fin=date.today() + timedelta(days=5),
        capacite_max=10,
    )
    db.add(session)
    db.commit()

    # Inscrire
    client.post(
        "/inscriptions/", json={"user_id": apprenant.id, "session_id": session.id}
    )

    # Lister les sessions de l'apprenant
    response = client.get(f"/inscriptions/student/{apprenant.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["session_id"] == session.id


def test_update_inscription_statut(client, db):
    """Mettre à jour le statut d'une inscription"""
    formation = Formation(
        title="Python Expert",
        description="Advanced Python",
        duration=35,
        level="avancé",
    )
    db.add(formation)
    formateur = User(
        email="teacher8@test.com",
        surname="Doe",
        name="John",
        birth_date=datetime(1980, 1, 1),
        role=Role.TEACHER,
    )
    apprenant = User(
        email="student8@test.com",
        surname="Smith",
        name="Jane",
        birth_date=datetime(2000, 1, 1),
        role=Role.STUDENT,
    )
    db.add_all([formateur, apprenant])
    db.commit()
    session = SessionFormation(
        formation_id=formation.id,
        formateur_id=formateur.id,
        date_debut=date.today(),
        date_fin=date.today() + timedelta(days=5),
        capacite_max=10,
    )
    db.add(session)
    db.commit()

    # Inscrire
    resp = client.post(
        "/inscriptions/", json={"user_id": apprenant.id, "session_id": session.id}
    )
    inscription_id = resp.json()["id"]
    assert resp.json()["statut"] == "en_attente"

    # Mettre à jour le statut
    patch_resp = client.patch(
        f"/inscriptions/{inscription_id}", json={"statut": "confirmé"}
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["statut"] == "confirmé"


def test_get_inscriptions_pagination(client, db):
    """Tester la pagination des inscriptions."""
    # Setup: 1 formation, 1 teacher, 1 session, 5 students
    formation = Formation(
        title="Paginated Inscriptions",
        description="Desc",
        duration=10,
        level="débutant",
    )
    db.add(formation)
    teacher = User(
        email="t_pag@test.com",
        surname="T",
        name="Teacher",
        birth_date=datetime(1980, 1, 1),
        role=Role.TEACHER,
    )
    db.add(teacher)
    db.commit()

    session = SessionFormation(
        formation_id=formation.id,
        formateur_id=teacher.id,
        date_debut=date.today(),
        date_fin=date.today() + timedelta(days=5),
        capacite_max=10,
    )
    db.add(session)

    students = []
    for i in range(5):
        s = User(
            email=f"s{i}@test.com",
            surname=f"S{i}",
            name="Student",
            birth_date=datetime(2000, 1, 1),
            role=Role.STUDENT,
        )
        students.append(s)
        db.add(s)
    db.commit()

    for s in students:
        client.post("/inscriptions/", json={"user_id": s.id, "session_id": session.id})

    # Tester pagination par session
    response = client.get(f"/inscriptions/session/{session.id}?page=1&size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["pages"] == 3

    response = client.get(f"/inscriptions/session/{session.id}?page=3&size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
