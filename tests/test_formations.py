import pytest
from app.models.formation import Niveau

def test_create_formation(client, db):
    response = client.post(
        "/formations/",
        json={
            "title": "Python Basics",
            "description": "Learn the fundamentals of Python programming from scratch.",
            "duration": 40,
            "level": "débutant"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Python Basics"
    assert data["duration"] == 40
    assert data["level"] == "débutant"
    assert "id" in data

def test_get_formations_list(client, db):
    # Create two formations
    client.post("/formations/", json={
        "title": "Formation 1", "description": "Description for formation 1 long enough", "duration": 10, "level": "débutant"
    })
    client.post("/formations/", json={
        "title": "Formation 2", "description": "Description for formation 2 long enough", "duration": 20, "level": "intermédiaire"
    })
    
    response = client.get("/formations/?page=1&size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["formations"]) == 2
    assert data["page"] == 1

def test_get_formation_by_id(client, db):
    create_resp = client.post("/formations/", json={
        "title": "Unique Formation", "description": "Description for unique formation here", "duration": 15, "level": "avancé"
    })
    formation_id = create_resp.json()["id"]
    
    response = client.get(f"/formations/{formation_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Unique Formation"

def test_update_formation(client, db):
    create_resp = client.post("/formations/", json={
        "title": "Old Title", "description": "Description before update is here", "duration": 10, "level": "débutant"
    })
    formation_id = create_resp.json()["id"]
    
    response = client.put(f"/formations/{formation_id}", json={
        "title": "New Title",
        "duration": 50
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["duration"] == 50
    # Level and description should remain unchanged
    assert data["level"] == "débutant"

def test_delete_formation(client, db):
    create_resp = client.post("/formations/", json={
        "title": "To Delete", "description": "Description for deletion test here", "duration": 5, "level": "débutant"
    })
    formation_id = create_resp.json()["id"]
    
    response = client.delete(f"/formations/{formation_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Formation deleted successfully"
    
    # Verify it's gone
    get_resp = client.get(f"/formations/{formation_id}")
    assert get_resp.status_code == 404

def test_create_formation_validation_errors(client, db):
    # Title too short
    response = client.post("/formations/", json={
        "title": "Short", "description": "Valid description length for this test", "duration": 10, "level": "débutant"
    })
    # Title "Short" is 5 chars, wait, schema says min_length=5. Let's try 4.
    response = client.post("/formations/", json={
        "title": "Shor", "description": "Valid description length for this test", "duration": 10, "level": "débutant"
    })
    assert response.status_code == 422
    
    # Duration <= 0
    response = client.post("/formations/", json={
        "title": "Valid Title", "description": "Valid description length for this test", "duration": 0, "level": "débutant"
    })
    assert response.status_code == 422

def test_get_non_existent_formation(client, db):
    response = client.get("/formations/999")
    assert response.status_code == 404
