from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, field_validator, ConfigDict
from app.schemas.user import UserResponse
from app.schemas.formation import FormationResponse
from app.core.session_status import SessionStatus


# BASE
class SessionBase(BaseModel):
    formation_id: int
    formateur_id: int
    date_debut: date
    date_fin: date
    capacite_max: int
    statut: SessionStatus = SessionStatus.PLANNED


# create
class SessionCreate(SessionBase):
    @field_validator("capacite_max")
    @classmethod
    def capacite_max_valide(cls, v: int) -> int:
        if v < 1:
            raise ValueError("La capacité maximale doit être >= 1")
        return v


# update (PATCH)
class SessionUpdate(BaseModel):
    formation_id: Optional[int] = None
    formateur_id: Optional[int] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    capacite_max: Optional[int] = None
    statut: Optional[SessionStatus] = None

    @field_validator("capacite_max")
    @classmethod
    def capacite_max_valide(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 1:
            raise ValueError("La capacité maximale doit être >= 1")
        return v


# read
class SessionResponse(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre_inscrits: int = 0
    created_at: datetime
    updated_at: datetime


# read (detail)
class SessionDetailResponse(SessionResponse):
    formation: FormationResponse
    formateur: UserResponse
