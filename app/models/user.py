from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db.database import Base
from sqlalchemy import Enum as SAEnum
from enum import Enum
from datetime import datetime, timezone
from sqlalchemy.orm import relationship


class Role(Enum):
    STUDENT = "Etudiant"
    TEACHER = "Formateur"
    ADMIN = "Administrateur"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=False)
    role = Column(SAEnum(Role), nullable=False)
    inscription_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)  # True for actif, False for inactif.

    inscriptions = relationship(
        "Inscription", back_populates="user", cascade="all, delete-orphan"
    )
    sessions_animees = relationship(
        "SessionFormation",
        primaryjoin="User.id == SessionFormation.formateur_id",
        foreign_keys="[SessionFormation.formateur_id]",
        back_populates="formateur",
    )
