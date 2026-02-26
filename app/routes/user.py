from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserDelete
from app.services import user as user_service

router = APIRouter(
    prefix="/utilisateurs",
    tags=["Utilisateurs"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.get_users(db, skip, limit)  

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = user_service.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=UserDelete)
def delete_user(user_id: int, hard_delete: bool = False, db: Session = Depends(get_db)):
    if hard_delete:
        success = user_service.hard_delete_user(db, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return UserDelete(message="User hard deleted", user_id=user_id, delete_type="hard")
    else:
        deleted_user = user_service.soft_delete_user(db, user_id)
        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserDelete(message="User soft deleted", user_id=user_id, delete_type="soft")
