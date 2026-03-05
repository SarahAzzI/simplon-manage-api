# app/schemas/formation.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.core.level import Level


class FormationBase(BaseModel):
    """Champs communs à la création et la lecture."""
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    duration: int
    level: Level


class FormationCreate(FormationBase):
    """Schéma pour la création (tous les champs obligatoires)."""
    pass

# --- UPDATE ---
class FormationUpdate(BaseModel):
    """Schéma pour la mise à jour (tous les champs optionnels)."""
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=5, max_length=500)
    duration: Optional[int] = None
    level: Optional[Level] = None

# --- READ ---
class FormationResponse(FormationBase):
    """Schéma pour la réponse API."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Optionnel : liste des inscriptions associées
    # inscriptions: Optional[List[InscriptionRead]] = None 

    model_config = ConfigDict(from_attributes=True)

# --- LIST ---
class FormationList(BaseModel):
    """Schéma pour la pagination."""
    formations: List[FormationResponse]
    total: int
    page: int
    size: int