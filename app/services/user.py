from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    @staticmethod
    def create(db: Session, user: UserCreate) -> User:
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

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = UserService.get_by_id(db, user_id)
        if not user:
            return None
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
        
    @staticmethod
    def soft_delete(db: Session, user_id: int) -> Optional[User]:
            user = UserService.get_by_id(db, user_id)
            if not user:
                return None
            user.is_active = False
            db.commit()
            db.refresh(user)
            return user

    @staticmethod
    def hard_delete(db: Session, user_id: int) -> bool:
        user = UserService.get_by_id(db, user_id)
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True