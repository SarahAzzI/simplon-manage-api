from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, model_validator, field_validator, ConfigDict
from app.schemas.user import UserResponse
from app.schemas.formation import FormationResponse


from app.models.session import SessionStatus


# ── BASE ──
class SessionBase(BaseModel):
    formation_id: int
    formateur_id: int
    date_debut: date
    date_fin: date
    capacite_max: int
    statut: SessionStatus = SessionStatus.PLANIFIEE
    co_formateur_id: Optional[int] = None


# ── CRÉATION ──
class SessionCreate(SessionBase):
    @field_validator("capacite_max")
    @classmethod
    def capacite_valide(cls, v: int) -> int:
        if v < 1:
            raise ValueError("La capacité doit être >= 1")
        return v


# ── MISE À JOUR ──
class SessionUpdate(BaseModel):
    formation_id: Optional[int] = None
    formateur_id: Optional[int] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    capacite_max: Optional[int] = None
    statut: Optional[SessionStatus] = None
    co_formateur_id: Optional[int] = None

    @field_validator("capacite_max")
    @classmethod
    def capacite_valide(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 1:
            raise ValueError("La capacité doit être >= 1")
        return v


# ── LECTURE ──
class SessionResponse(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre_inscrits: int = 0
    created_at: datetime
    updated_at: datetime
    formation: Optional[FormationResponse] = None
    formateur: Optional[UserResponse] = None
    co_formateur: Optional[UserResponse] = None


# ── LECTURE DÉTAILLÉE ──
class SessionDetailResponse(SessionResponse):
    pass
