from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

from app.schemas.user import UserResponse
from app.schemas.session import SessionResponse


class InscriptionBase(BaseModel):
    """Base schema with common inscription fields."""
    statut: str = Field(default="en_attente", max_length=50)
    capacite_max: Optional[int] = Field(None, gt=0)


class InscriptionCreate(InscriptionBase):
    """Schema for creating a new inscription."""
    session_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)


class InscriptionUpdate(BaseModel):
    """Schema for updating inscription - all fields optional."""
    statut: Optional[str] = Field(None, max_length=50)
    capacite_max: Optional[int] = Field(None, gt=0)


class InscriptionResponse(InscriptionBase):
    """Schema for inscription responses."""
    id: int
    session_id: int
    user_id: int
    date_inscription: datetime
    created_at: datetime
    updated_at: datetime

    # Relations imbriquées optionnel
    user: Optional[UserResponse] = None
    session: Optional[SessionResponse] = None

    model_config = ConfigDict(from_attributes=True)


class InscriptionList(BaseModel):
    """Schema for paginated inscription list."""
    inscriptions: list[InscriptionResponse]
    total: int
    page: int
    size: int
    pages: int