from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import NotFoundException, BadRequestException


class UserService:
    @staticmethod
    def create(db: Session, user: UserCreate) -> User:
        try:
            new_user = User(
                email=user.email,
                surname=user.surname,
                name=user.name,
                birth_date=user.birth_date,
                role=user.role,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except IntegrityError:
            db.rollback()
            raise BadRequestException("Un utilisateur avec cet email existe déjà")

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("Utilisateur", user_id)
        return user

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def get_total(db: Session) -> int:
        return db.query(User).count()

    @staticmethod
    def update(db: Session, user_id: int, user_data: UserUpdate) -> User:
        user = UserService.get_by_id(db, user_id)
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def soft_delete(db: Session, user_id: int) -> User:
        user = UserService.get_by_id(db, user_id)
        user.is_active = False
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def hard_delete(db: Session, user_id: int) -> None:
        user = UserService.get_by_id(db, user_id)
        db.delete(user)
        db.commit()
