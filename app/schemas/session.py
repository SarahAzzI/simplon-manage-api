from datetime import date, datetime
from pydantic import BaseModel, model_validator, field_validator, ConfigDict
from app.schemas.utilisateur import UtilisateurRead
from app.schemas.formation import FormationRead


# ── BASE ──
class SessionBase(BaseModel):
    formation_id: int
    formateur_id: int
    date_debut: date
    date_fin: date
    capacite_max: int


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
    formation_id: int | None = None
    formateur_id: int | None = None
    date_debut: date | None = None
    date_fin: date | None = None
    capacite_max: int | None = None

    @field_validator("capacite_max")
    @classmethod
    def capacite_valide(cls, v: int | None) -> int | None:
        if v is not None and v < 1:
            raise ValueError("La capacité doit être >= 1")
        return v


# ── LECTURE ──
class SessionRead(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre_inscrits: int = 0
    created_at: datetime
    updated_at: datetime


# ── LECTURE DÉTAILLÉE ──
class SessionDetailRead(SessionRead):
    formation: FormationRead
    formateur: UtilisateurRead
