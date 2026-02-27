from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import NotFoundException, BadRequestException



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
                detail=f"Un utilisateur avec l'email {user.email} existe déjà"
            )
        
        # Contrainte : rôle obligatoire
        if not user.role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le rôle est obligatoire"
            )
        
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
    def get_by_id(db: Session, user_id: int) -> User:
        """Récupère un user par ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'id {user_id} non trouvé"
            )
        return user

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Liste tous les users avec pagination"""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, user_id: int, user_data: UserUpdate) -> User:
        """Met à jour un user"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'id {user_id} non trouvé"
            )
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        # Si on modifie l'email, vérifier qu'il n'existe pas déjà
        if "email" in update_data:
            existing = UserService.get_by_email(db, update_data["email"])
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"L'email {update_data['email']} est déjà utilisé"
                )
        
        for key, value in update_data.items():
            setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def soft_delete(db: Session, user_id: int) -> User:
        """Désactive un user (soft delete)"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'id {user_id} non trouvé"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Utilisateur {user_id} est déjà désactivé"
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
                detail=f"Utilisateur avec l'id {user_id} non trouvé"
            )
        
        user_id_deleted = user.id
        db.delete(user)
        db.commit()
        
        return {
            "message": f"Utilisateur {user_id_deleted} supprimé définitivement",
            "user_id": user_id_deleted
        }
