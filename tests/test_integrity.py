import pytest
from datetime import date, datetime, timedelta
from app.models.user import  User
from app.models.formation import Formation
from app.models.session import SessionFormation
from app.models.inscription import Inscription
from app.core.role import Role

def test_delete_user_cascades_inscriptions(client, db):
    # Setup: Create formation, teacher, student, session, and inscription
    formation = Formation(title="Integrity Test", description="Desc for integrity test", duration=10, level="débutant")
    db.add(formation)
    
    teacher = User(email="t_int@test.com", surname="Teacher", name="Internal", birth_date=datetime(1980, 1, 1), role=Role.TEACHER)
    student = User(email="s_int@test.com", surname="Student", name="Internal", birth_date=datetime(2000, 1, 1), role=Role.STUDENT)
    db.add_all([teacher, student])
    db.commit()
    
    session = SessionFormation(
        formation_id=formation.id, formateur_id=teacher.id,
        date_debut=date.today(), date_fin=date.today() + timedelta(days=5),
        capacite_max=10
    )
    db.add(session)
    db.commit()
    
    # Inscribe student
    client.post("/inscriptions/", json={"user_id": student.id, "session_id": session.id})
    
    # Verify inscription exists
    assert db.query(Inscription).filter(Inscription.user_id == student.id).count() == 1
    
    # Hard delete user
    client.delete(f"/utilisateurs/{student.id}?hard_delete=true")
    
    # Verify inscription is gone (cascade)
    assert db.query(Inscription).filter(Inscription.user_id == student.id).count() == 0

def test_delete_formation_cascades_sessions(client, db):
    # Setup: Create formation, teacher, session
    formation = Formation(title="Form Cascade", description="Desc for formation cascade", duration=10, level="débutant")
    db.add(formation)
    
    teacher = User(email="t_form@test.com", surname="Teacher", name="Formation", birth_date=datetime(1980, 1, 1), role=Role.TEACHER)
    db.add(teacher)
    db.commit()
    
    session = SessionFormation(
        formation_id=formation.id, formateur_id=teacher.id,
        date_debut=date.today(), date_fin=date.today() + timedelta(days=5),
        capacite_max=10
    )
    db.add(session)
    db.commit()
    
    # Verify session exists
    assert db.query(SessionFormation).filter(SessionFormation.formation_id == formation.id).count() == 1
    
    # Delete formation
    client.delete(f"/formations/{formation.id}")
    
    # Verify session is gone (cascade)
    assert db.query(SessionFormation).filter(SessionFormation.formation_id == formation.id).count() == 0
