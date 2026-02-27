from datetime import date, timedelta


def test_create_session(client, db):
    # 1. Create a formation
    form_resp = client.post(
        "/formations/",
        json={
            "title": "FastAPI Course",
            "description": "Learning FastAPI with tests is great.",
            "duration": 35,
            "level": "débutant",
        },
    )
    form_id = form_resp.json()["id"]

    # 2. Create a teacher
    teach_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "teacher@simplon.com",
            "surname": "Teacher",
            "name": "Bob",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    )
    teach_id = teach_resp.json()["id"]

    # 3. Create session
    today = date.today()
    response = client.post(
        "/sessions/",
        json={
            "formation_id": form_id,
            "formateur_id": teach_id,
            "date_debut": today.isoformat(),
            "date_fin": (today + timedelta(days=5)).isoformat(),
            "capacite_max": 15,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["formation_id"] == form_id
    assert data["capacite_max"] == 15
    assert "id" in data


def test_list_sessions(client, db):
    response = client.get("/sessions/")
    assert response.status_code == 200
    # Should be paginated
    assert "items" in response.json()
    assert "total" in response.json()


def test_update_session(client, db):
    # Setup: Create formation, teacher, and session
    form_resp = client.post(
        "/formations/",
        json={
            "title": "To Update",
            "description": "Desc long enough characters here.",
            "duration": 10,
            "level": "débutant",
        },
    )
    form_id = form_resp.json()["id"]
    teach_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "t_upd@test.com",
            "surname": "Tu",
            "name": "Upd",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    )
    teach_id = teach_resp.json()["id"]
    sess_resp = client.post(
        "/sessions/",
        json={
            "formation_id": form_id,
            "formateur_id": teach_id,
            "date_debut": date.today().isoformat(),
            "date_fin": (date.today() + timedelta(days=2)).isoformat(),
            "capacite_max": 10,
        },
    )
    sess_id = sess_resp.json()["id"]

    # Update capacity and dates
    new_fin = (date.today() + timedelta(days=10)).isoformat()
    response = client.put(
        f"/sessions/{sess_id}", json={"capacite_max": 20, "date_fin": new_fin}
    )
    assert response.status_code == 200
    assert response.json()["capacite_max"] == 20
    assert response.json()["date_fin"] == new_fin


def test_create_session_invalid_dates(client, db):
    form_resp = client.post(
        "/formations/",
        json={
            "title": "Invalid Dates",
            "description": "Description is here for validation test",
            "duration": 10,
            "level": "débutant",
        },
    )
    form_id = form_resp.json()["id"]
    teach_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "t_err@test.com",
            "surname": "Te",
            "name": "Err",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    )
    teach_id = teach_resp.json()["id"]

    # Start date AFTER end date
    response = client.post(
        "/sessions/",
        json={
            "formation_id": form_id,
            "formateur_id": teach_id,
            "date_debut": (date.today() + timedelta(days=10)).isoformat(),
            "date_fin": date.today().isoformat(),
            "capacite_max": 10,
        },
    )
    # Should trigger BadRequestException (400) or validation error (422) depending on implementation
    # Service implementation uses BadRequestException(400)
    assert response.status_code == 400
    assert "date de fin" in response.json()["detail"]


def test_delete_session(client, db):
    # Setup
    form_resp = client.post(
        "/formations/",
        json={
            "title": "To Delete",
            "description": "Desc for deletion test is here.",
            "duration": 5,
            "level": "débutant",
        },
    )
    form_id = form_resp.json()["id"]
    teach_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "t_del@test.com",
            "surname": "Te",
            "name": "Del",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    )
    teach_id = teach_resp.json()["id"]
    sess_resp = client.post(
        "/sessions/",
        json={
            "formation_id": form_id,
            "formateur_id": teach_id,
            "date_debut": date.today().isoformat(),
            "date_fin": (date.today() + timedelta(days=1)).isoformat(),
            "capacite_max": 5,
        },
    )
    sess_id = sess_resp.json()["id"]

    response = client.delete(f"/sessions/{sess_id}")
    assert response.status_code == 204

    # Verify 404
    get_resp = client.get(f"/sessions/{sess_id}")
    assert get_resp.status_code == 404


def test_create_session_invalid_capacity(client, db):
    """Capacité < 1 doit retourner 400"""
    form_resp = client.post(
        "/formations/",
        json={
            "title": "Cap Test",
            "description": "Description validation cap.",
            "duration": 5,
            "level": "débutant",
        },
    )
    form_id = form_resp.json()["id"]
    teach_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "t_cap@test.com",
            "surname": "Te",
            "name": "Cap",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    )
    teach_id = teach_resp.json()["id"]

    response = client.post(
        "/sessions/",
        json={
            "formation_id": form_id,
            "formateur_id": teach_id,
            "date_debut": date.today().isoformat(),
            "date_fin": (date.today() + timedelta(days=1)).isoformat(),
            "capacite_max": 0,
        },
    )
    # Schema validation might catch this if min_value is set,
    # but Service also has a safety check.
    assert response.status_code in [400, 422]


def test_get_session_not_found(client, db):
    """Session inexistante doit retourner 404"""
    response = client.get("/sessions/99999")
    assert response.status_code == 404
    assert "Session" in response.json()["detail"]


def test_create_session_non_existent_teacher(client, db):
    """Formateur inexistant doit retourner 404"""
    form_resp = client.post(
        "/formations/",
        json={
            "title": "No Teacher",
            "description": "Description for no teacher test",
            "duration": 10,
            "level": "débutant",
        },
    )
    form_id = form_resp.json()["id"]

    response = client.post(
        "/sessions/",
        json={
            "formation_id": form_id,
            "formateur_id": 99999,
            "date_debut": date.today().isoformat(),
            "date_fin": (date.today() + timedelta(days=1)).isoformat(),
            "capacite_max": 10,
        },
    )
    assert response.status_code == 404
    assert "Formateur" in response.json()["detail"]


def test_create_session_non_existent_formation(client, db):
    """Formation inexistante doit retourner 404"""
    teach_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "t_noform@test.com",
            "surname": "Te",
            "name": "NoForm",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    )
    teach_id = teach_resp.json()["id"]

    response = client.post(
        "/sessions/",
        json={
            "formation_id": 99999,
            "formateur_id": teach_id,
            "date_debut": date.today().isoformat(),
            "date_fin": (date.today() + timedelta(days=1)).isoformat(),
            "capacite_max": 10,
        },
    )
    assert response.status_code == 404
    assert "Formation" in response.json()["detail"]


def test_create_session_with_non_teacher_role(client, db):
    """Un utilisateur non-formateur ne peut pas animer une session"""
    form_resp = client.post(
        "/formations/",
        json={
            "title": "Role Check",
            "description": "Description for role check test",
            "duration": 10,
            "level": "débutant",
        },
    )
    form_id = form_resp.json()["id"]
    student_resp = client.post(
        "/utilisateurs/",
        json={
            "email": "student_role@test.com",
            "surname": "St",
            "name": "Role",
            "birth_date": "2000-01-01T00:00:00",
            "role": "Etudiant",
        },
    )
    student_id = student_resp.json()["id"]

    response = client.post(
        "/sessions/",
        json={
            "formation_id": form_id,
            "formateur_id": student_id,
            "date_debut": date.today().isoformat(),
            "date_fin": (date.today() + timedelta(days=1)).isoformat(),
            "capacite_max": 10,
        },
    )
    assert response.status_code == 400
    assert "rôle formateur" in response.json()["detail"]


def test_list_sessions_filters(client, db):
    """Tester les filtres par formation et formateur"""
    # 1. Setup two formations, two teachers
    f1 = client.post(
        "/formations/",
        json={
            "title": "Formation 1",
            "description": "Cette description est assez longue pour passer.",
            "duration": 10,
            "level": "débutant",
        },
    ).json()["id"]
    f2 = client.post(
        "/formations/",
        json={
            "title": "Formation 2",
            "description": "Cette description est également assez longue.",
            "duration": 10,
            "level": "débutant",
        },
    ).json()["id"]
    t1 = client.post(
        "/utilisateurs/",
        json={
            "email": "t1@s.com",
            "surname": "Surname1",
            "name": "Name1",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    ).json()["id"]
    t2 = client.post(
        "/utilisateurs/",
        json={
            "email": "t2@s.com",
            "surname": "Surname2",
            "name": "Name2",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    ).json()["id"]

    # 2. Create 3 sessions
    client.post(
        "/sessions/",
        json={
            "formation_id": f1,
            "formateur_id": t1,
            "date_debut": "2025-01-01",
            "date_fin": "2025-01-10",
            "capacite_max": 10,
        },
    )
    client.post(
        "/sessions/",
        json={
            "formation_id": f1,
            "formateur_id": t2,
            "date_debut": "2025-02-01",
            "date_fin": "2025-02-10",
            "capacite_max": 10,
        },
    )
    client.post(
        "/sessions/",
        json={
            "formation_id": f2,
            "formateur_id": t2,
            "date_debut": "2025-03-01",
            "date_fin": "2025-03-10",
            "capacite_max": 10,
        },
    )

    # Test filters
    resp = client.get(f"/sessions/?formation_id={f1}")
    assert len(resp.json()["items"]) == 2

    resp = client.get(f"/sessions/?formateur_id={t2}")
    assert len(resp.json()["items"]) == 2

    resp = client.get(f"/sessions/?formation_id={f2}&formateur_id={t2}")
    assert len(resp.json()["items"]) == 1


def test_update_session_invalid_role(client, db):
    """Tester l'échec de mise à jour avec un utilisateur qui n'est pas formateur"""
    f_id = client.post(
        "/formations/",
        json={
            "title": "Formation Valid",
            "description": "Description correcte de plus de vingt caractères.",
            "duration": 10,
            "level": "débutant",
        },
    ).json()["id"]
    t_id = client.post(
        "/utilisateurs/",
        json={
            "email": "t_upd_role@s.com",
            "surname": "Teacher",
            "name": "Name",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    ).json()["id"]
    s_id = client.post(
        "/sessions/",
        json={
            "formation_id": f_id,
            "formateur_id": t_id,
            "date_debut": "2025-01-01",
            "date_fin": "2025-01-10",
            "capacite_max": 10,
        },
    ).json()["id"]

    st_id = client.post(
        "/utilisateurs/",
        json={
            "email": "st_upd_role@s.com",
            "surname": "Student",
            "name": "Name",
            "birth_date": "2000-01-01T00:00:00",
            "role": "Etudiant",
        },
    ).json()["id"]

    resp = client.put(f"/sessions/{s_id}", json={"formateur_id": st_id})
    assert resp.status_code == 400
    assert "rôle formateur" in resp.json()["detail"]


def test_update_session_invalid_formation(client, db):
    """Tester l'échec de mise à jour avec une formation inexistante"""
    f_id = client.post(
        "/formations/",
        json={
            "title": "Formation Valid",
            "description": "Description correcte de plus de vingt caractères.",
            "duration": 10,
            "level": "débutant",
        },
    ).json()["id"]
    t_id = client.post(
        "/utilisateurs/",
        json={
            "email": "t_upd_form@s.com",
            "surname": "Teacher",
            "name": "Name",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    ).json()["id"]
    s_id = client.post(
        "/sessions/",
        json={
            "formation_id": f_id,
            "formateur_id": t_id,
            "date_debut": "2025-01-01",
            "date_fin": "2025-01-10",
            "capacite_max": 10,
        },
    ).json()["id"]

    resp = client.put(f"/sessions/{s_id}", json={"formation_id": 99999})
    assert resp.status_code == 404


def test_update_session_invalid_capacity_reduction(client, db):
    """Empêcher de réduire la capacité en dessous du nombre d'inscrits"""
    f_id = client.post(
        "/formations/",
        json={
            "title": "Formation Valid",
            "description": "Description correcte de plus de vingt caractères.",
            "duration": 10,
            "level": "débutant",
        },
    ).json()["id"]
    t_id = client.post(
        "/utilisateurs/",
        json={
            "email": "t_upd_cap@s.com",
            "surname": "Teacher",
            "name": "Name",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    ).json()["id"]
    s_id = client.post(
        "/sessions/",
        json={
            "formation_id": f_id,
            "formateur_id": t_id,
            "date_debut": "2025-01-01",
            "date_fin": "2025-01-10",
            "capacite_max": 10,
        },
    ).json()["id"]

    for i in range(5):
        st_id = client.post(
            "/utilisateurs/",
            json={
                "email": f"st_cap_{i}@s.com",
                "surname": "Student",
                "name": f"Name{i}",
                "birth_date": "2000-01-01T00:00:00",
                "role": "Etudiant",
            },
        ).json()["id"]
        client.post("/inscriptions/", json={"session_id": s_id, "user_id": st_id})

    resp = client.put(f"/sessions/{s_id}", json={"capacite_max": 4})
    assert resp.status_code == 400
    assert "Impossible de réduire la capacité" in resp.json()["detail"]


def test_session_statut_flow(client, db):
    """Vérifier le cycle de vie du statut d'une session"""
    f_id = client.post(
        "/formations/",
        json={
            "title": "Formation Valid",
            "description": "Description correcte de plus de vingt caractères.",
            "duration": 10,
            "level": "débutant",
        },
    ).json()["id"]
    t_id = client.post(
        "/utilisateurs/",
        json={
            "email": "t_stat@s.com",
            "surname": "Teacher",
            "name": "Name",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    ).json()["id"]

    resp = client.post(
        "/sessions/",
        json={
            "formation_id": f_id,
            "formateur_id": t_id,
            "date_debut": "2025-01-01",
            "date_fin": "2025-01-10",
            "capacite_max": 10,
        },
    )
    s_id = resp.json()["id"]
    assert resp.json()["statut"] == "planifiée"

    resp = client.put(f"/sessions/{s_id}", json={"statut": "en_cours"})
    assert resp.json()["statut"] == "en_cours"

    resp = client.put(f"/sessions/{s_id}", json={"statut": "terminée"})
    assert resp.json()["statut"] == "terminée"


def test_get_session_detail(client, db):
    """Vérifier les détails d'une session avec les relations et le compte d'inscrits"""
    f_id = client.post(
        "/formations/",
        json={
            "title": "Formation Detail",
            "description": "Description correcte de plus de vingt caractères.",
            "duration": 10,
            "level": "débutant",
        },
    ).json()["id"]
    t_id = client.post(
        "/utilisateurs/",
        json={
            "email": "t_det@s.com",
            "surname": "Teacher",
            "name": "Name",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    ).json()["id"]
    s_id = client.post(
        "/sessions/",
        json={
            "formation_id": f_id,
            "formateur_id": t_id,
            "date_debut": "2025-01-01",
            "date_fin": "2025-01-10",
            "capacite_max": 10,
        },
    ).json()["id"]

    for i in range(2):
        st_id = client.post(
            "/utilisateurs/",
            json={
                "email": f"st_det_fin_{i}@s.com",
                "surname": "Student",
                "name": f"Name{i}",
                "birth_date": "2000-01-01T00:00:00",
                "role": "Etudiant",
            },
        ).json()["id"]
        client.post("/inscriptions/", json={"session_id": s_id, "user_id": st_id})

    resp = client.get(f"/sessions/{s_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["nombre_inscrits"] == 2
    assert data["formation"]["title"] == "Formation Detail"
    assert data["formateur"]["email"] == "t_det@s.com"


def test_update_session_non_existent_teacher(client, db):
    """Tester la mise à jour avec un formateur inexistant"""
    f_id = client.post(
        "/formations/",
        json={
            "title": "Formation Valid",
            "description": "Description correcte de plus de vingt caractères.",
            "duration": 10,
            "level": "débutant",
        },
    ).json()["id"]
    t_id = client.post(
        "/utilisateurs/",
        json={
            "email": "t_ex@s.com",
            "surname": "Teacher",
            "name": "Name",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    ).json()["id"]
    s_id = client.post(
        "/sessions/",
        json={
            "formation_id": f_id,
            "formateur_id": t_id,
            "date_debut": "2025-01-01",
            "date_fin": "2025-01-10",
            "capacite_max": 10,
        },
    ).json()["id"]

    resp = client.put(f"/sessions/{s_id}", json={"formateur_id": 99999})
    assert resp.status_code == 404


def test_create_session_zero_capacity(client, db):
    """Tester la création avec une capacité de 0 (devrait être bloqué par le service)"""
    f_id = client.post(
        "/formations/",
        json={
            "title": "Formation Valid",
            "description": "Description correcte de plus de vingt caractères.",
            "duration": 10,
            "level": "débutant",
        },
    ).json()["id"]
    t_id = client.post(
        "/utilisateurs/",
        json={
            "email": "t_zero@s.com",
            "surname": "Teacher",
            "name": "Name",
            "birth_date": "1980-01-01T00:00:00",
            "role": "Formateur",
        },
    ).json()["id"]

    # On utilise 0. Le schéma Pydantic Field(gt=0) pourrait déjà le bloquer (422),
    # mais le service a une vérification interne aussi.
    resp = client.post(
        "/sessions/",
        json={
            "formation_id": f_id,
            "formateur_id": t_id,
            "date_debut": "2025-01-01",
            "date_fin": "2025-01-10",
            "capacite_max": 0,
        },
    )
    assert resp.status_code in [400, 422]
