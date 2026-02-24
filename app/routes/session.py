import math
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.session import (
    SessionCreate,
    SessionUpdate,
    SessionRead,
    SessionDetailRead,
)
from app.schemas.pagination import PaginatedResponse
from app.services.session import SessionService

router = APIRouter(prefix="/sessions", tags=["Sessions"])


# GET /sessions/
@router.get("/", response_model=PaginatedResponse[SessionRead])
def lister_sessions(
    page: int = Query(1, ge=1, description="Numéro de page"),
    size: int = Query(20, ge=1, le=100, description="Taille de page"),
    formation_id: int | None = Query(None, description="Filtrer par formation"),
    formateur_id: int | None = Query(None, description="Filtrer par formateur"),
    db: Session = Depends(get_db),
):
    """Lister toutes les sessions avec pagination et filtres."""

    results, total = SessionService.get_all(
        db, page, size, formation_id, formateur_id
    )

    items = []
    for r in results:
        s = SessionRead.model_validate(r["session"])
        s.nombre_inscrits = r["nombre_inscrits"]
        items.append(s)

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total else 0,
    )


# GET /sessions/{id}
@router.get("/{session_id}", response_model=SessionDetailRead)
def obtenir_session(
    session_id: int, db: Session = Depends(get_db)
):
    """Obtenir le détail d'une session (avec formation et formateur)."""

    session = SessionService.get_by_id(db, session_id)
    nb = SessionService.count_inscrits(db, session_id)
    result = SessionDetailRead.model_validate(session)
    result.nombre_inscrits = nb
    return result


# POST /sessions/
@router.post(
    "/",
    response_model=SessionRead,
    status_code=status.HTTP_201_CREATED,
)
def creer_session(
    data: SessionCreate, db: Session = Depends(get_db)
):
    """Créer une nouvelle session de formation."""

    return SessionService.create(db, data)


# PUT /sessions/{id}

@router.put("/{session_id}", response_model=SessionRead)
def modifier_session(
    session_id: int,
    data: SessionUpdate,
    db: Session = Depends(get_db),
):
    """Modifier une session existante."""

    return SessionService.update(db, session_id, data)


# DELETE /sessions/{id}
@router.delete(
    "/{session_id}", status_code=status.HTTP_204_NO_CONTENT
)
def supprimer_session(
    session_id: int, db: Session = Depends(get_db)
):
    """Supprimer une session."""

    SessionService.delete(db, session_id)