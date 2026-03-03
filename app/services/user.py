from fastapi import HTTPException, status
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import BadRequestException
from sqlalchemy import func


class UserService:

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Cherche un user par email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, user: UserCreate) -> User:
        """Crée un nouvel utilisateur"""

        # Contrainte : email unique
        existing_user = UserService.get_by_email(db, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Un utilisateur avec l'email {user.email} existe déjà",
            )

        # Contrainte : rôle obligatoire
        if not user.role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le rôle est obligatoire",
            )

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

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        """Récupère un user par ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'id {user_id} non trouvé",
            )
        return user

    @staticmethod
    def list(
        db: Session, skip: int = 0, limit: int = 100, only_active: bool = False
    ) -> List[User]:
        """Liste tous les users avec pagination"""
        query = db.query(User)
        if only_active:
            query = query.filter(User.is_active == True)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_total(db: Session) -> int:
        """Récupère le nombre total d'utilisateurs"""
        return db.query(User).count()

    @staticmethod
    def update(db: Session, user_id: int, user_data: UserUpdate) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'id {user_id} non trouvé",
            )

        update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)

        # Gestion de l'email
        if "email" in update_data:
            new_email = str(update_data["email"]).strip().lower()
            current_email = (user.email or "").strip().lower()

            if new_email == current_email:
                # Email inchangé → on ignore
                del update_data["email"]
            else:
                # Vérifie uniquement s'il est pris par un AUTRE utilisateur
                existing = (
                    db.query(User).filter(func.lower(User.email) == new_email).first()
                )
                if existing is not None and existing.id != user_id:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="L'email est déjà utilisé",
                    )

        # Appliquer les autres champs
        for key, value in update_data.items():
            setattr(user, key, value)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=409, detail="Erreur base de données")
        db.refresh(user)
        return user

    @staticmethod
    def soft_delete(db: Session, user_id: int) -> User:
        """Désactive un user (soft delete)"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'id {user_id} non trouvé",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Utilisateur {user_id} est déjà désactivé",
            )

        user.is_active = False
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def hard_delete(db: Session, user_id: int) -> dict:
        """Supprime définitivement un user"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'id {user_id} non trouvé",
            )

        user_id_deleted = user.id
        db.delete(user)
        db.commit()

        return {
            "message": f"Utilisateur {user_id_deleted} supprimé définitivement",
            "user_id": user_id_deleted,
        }
