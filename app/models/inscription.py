from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
from enum import Enum


class StatutInscription(Enum):
    EN_ATTENTE = "en_attente"
    CONFIRME = "confirmé"
    ANNULE = "annulé"
    TERMINE = "terminé"


class Inscription(Base):
    """
    Inscription model representing the inscriptions table.
    Links a User to a Session for a Formation.
    """

    __tablename__ = "inscriptions"  # Correction: __tablename__ (et orthographe)

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Foreign Keys
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    date_inscription = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    statut = Column(
        String(50), default=StatutInscription.EN_ATTENTE.value, nullable=False
    )

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="inscriptions")
    session = relationship("SessionFormation", back_populates="inscriptions")

    __table_args__ = (
        UniqueConstraint("user_id", "session_id", name="uq_inscription_user_session"),
        Index("ix_inscriptions_user_session", "user_id", "session_id"),
    )

    def __repr__(self):
        return (
            f"<Inscription(id={self.id}, user_id={self.user_id}, statut={self.statut})>"
        )
