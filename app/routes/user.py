import math
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserDelete
from app.schemas.pagination import PaginatedResponse
from app.services.user import UserService

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create(db, user)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_by_id(db, user_id)


@router.get("/", response_model=PaginatedResponse[UserResponse])
def read_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    active_only: bool = Query(False),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size
    items = UserService.list(db, skip=skip, limit=size, only_active=active_only)
    total = UserService.get_total(db)
    pages = math.ceil(total / size) if total else 0
    return {"items": items, "total": total, "page": page, "size": size, "pages": pages}


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update(db, user_id, user)


@router.delete("/{user_id}", response_model=UserDelete)
def delete_user(user_id: int, hard_delete: bool = False, db: Session = Depends(get_db)):
    if hard_delete:
        UserService.hard_delete(db, user_id)
        return UserDelete(
            message="User hard deleted", user_id=user_id, delete_type="hard"
        )
    else:
        UserService.soft_delete(db, user_id)
        return UserDelete(
            message="User soft deleted", user_id=user_id, delete_type="soft"
        )
