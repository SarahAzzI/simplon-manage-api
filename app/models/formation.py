from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy import Enum as SAEnum
from enum import Enum

class Niveau(str, Enum):
    """Enum pour les niveaux de formation."""
    BEGINNER = "débutant"
    INTERMEDIATE = "intermédiaire"
    ADVANCED = "avancé"

class Formation(Base):
    __tablename__ = "formations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=False)
    duration = Column(Integer, nullable=False)
    level = Column(SAEnum(Niveau), nullable=False, default=Niveau.BEGINNER)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    inscriptions = relationship("Inscription", back_populates="formation")

    __table_args__ = (
        Index("ix_formations_level", "level"),
    )

    def __repr__(self):
        return f"<Formation(id={self.id}, title={self.title})>"