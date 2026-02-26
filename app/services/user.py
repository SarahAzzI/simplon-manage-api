from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate) -> User:
    new_user = User(
        email=user.email,
        surname=user.surname,
        name=user.name,
        birth_date=user.birth_date,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User | None:
    user = get_user(db, user_id)
    if not user:
        return None
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
    
def soft_delete_user(db: Session, user_id: int) -> User | None:
        user = get_user(db, user_id)
        if not user:
            return None
        user.is_active = False
        db.commit()
        db.refresh(user)
        return user

def hard_delete_user(db: Session, user_id: int) -> bool:
   
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True