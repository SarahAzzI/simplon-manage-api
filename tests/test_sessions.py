import pytest
from datetime import date, timedelta

def test_create_session(client, db):
    # 1. Create a formation
    form_resp = client.post("/formations/", json={
        "title": "FastAPI Course", "description": "Learning FastAPI with tests is great.", 
        "duration": 35, "level": "débutant"
    })
    form_id = form_resp.json()["id"]
    
    # 2. Create a teacher
    teach_resp = client.post("/utilisateurs/", json={
        "email": "teacher@simplon.com", "surname": "Teacher", "name": "Bob", 
        "birth_date": "1980-01-01T00:00:00", "role": "Formateur"
    })
    teach_id = teach_resp.json()["id"]
    
    # 3. Create session
    today = date.today()
    response = client.post("/sessions/", json={
        "formation_id": form_id,
        "formateur_id": teach_id,
        "date_debut": today.isoformat(),
        "date_fin": (today + timedelta(days=5)).isoformat(),
        "capacite_max": 15
    })
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
    form_resp = client.post("/formations/", json={
        "title": "To Update", "description": "Desc long enough characters here.", 
        "duration": 10, "level": "débutant"
    })
    form_id = form_resp.json()["id"]
    teach_resp = client.post("/utilisateurs/", json={
        "email": "t_upd@test.com", "surname": "Tu", "name": "Upd", 
        "birth_date": "1980-01-01T00:00:00", "role": "Formateur"
    })
    teach_id = teach_resp.json()["id"]
    sess_resp = client.post("/sessions/", json={
        "formation_id": form_id, "formateur_id": teach_id,
        "date_debut": date.today().isoformat(),
        "date_fin": (date.today() + timedelta(days=2)).isoformat(),
        "capacite_max": 10
    })
    sess_id = sess_resp.json()["id"]
    
    # Update capacity and dates
    new_fin = (date.today() + timedelta(days=10)).isoformat()
    response = client.put(f"/sessions/{sess_id}", json={
        "capacite_max": 20,
        "date_fin": new_fin
    })
    assert response.status_code == 200
    assert response.json()["capacite_max"] == 20
    assert response.json()["date_fin"] == new_fin

def test_create_session_invalid_dates(client, db):
    form_resp = client.post("/formations/", json={
        "title": "Invalid Dates", "description": "Description is here for validation test", 
        "duration": 10, "level": "débutant"
    })
    form_id = form_resp.json()["id"]
    teach_resp = client.post("/utilisateurs/", json={
        "email": "t_err@test.com", "surname": "Te", "name": "Err", 
        "birth_date": "1980-01-01T00:00:00", "role": "Formateur"
    })
    teach_id = teach_resp.json()["id"]
    
    # Start date AFTER end date
    response = client.post("/sessions/", json={
        "formation_id": form_id,
        "formateur_id": teach_id,
        "date_debut": (date.today() + timedelta(days=10)).isoformat(),
        "date_fin": date.today().isoformat(),
        "capacite_max": 10
    })
    # Should trigger BadRequestException (400) or validation error (422) depending on implementation
    # Service implementation uses BadRequestException(400)
    assert response.status_code == 400
    assert "date de fin" in response.json()["detail"]

def test_delete_session(client, db):
    # Setup
    form_resp = client.post("/formations/", json={
        "title": "To Delete", "description": "Desc for deletion test is here.", 
        "duration": 5, "level": "débutant"
    })
    form_id = form_resp.json()["id"]
    teach_resp = client.post("/utilisateurs/", json={
        "email": "t_del@test.com", "surname": "Te", "name": "Del", 
        "birth_date": "1980-01-01T00:00:00", "role": "Formateur"
    })
    teach_id = teach_resp.json()["id"]
    sess_resp = client.post("/sessions/", json={
        "formation_id": form_id, "formateur_id": teach_id,
        "date_debut": date.today().isoformat(), "date_fin": (date.today() + timedelta(days=1)).isoformat(),
        "capacite_max": 5
    })
    sess_id = sess_resp.json()["id"]
    
    response = client.delete(f"/sessions/{sess_id}")
    assert response.status_code == 204
    
    # Verify 404
    get_resp = client.get(f"/sessions/{sess_id}")
    assert get_resp.status_code == 404
