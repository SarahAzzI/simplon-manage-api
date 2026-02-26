from datetime import date, datetime
from sqlalchemy import Integer, Date, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class SessionFormation(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    formation_id: Mapped[int] = mapped_column(
        ForeignKey("formations.id", ondelete="CASCADE"),
        nullable=False,
    )
    formateur_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),  # ← corrigé
        nullable=False,
    )
    date_debut: Mapped[date] = mapped_column(Date, nullable=False)
    date_fin: Mapped[date] = mapped_column(Date, nullable=False)
    capacite_max: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint("date_fin > date_debut", name="check_dates_coherentes"),
        CheckConstraint("capacite_max >= 1", name="check_capacite_positive"),
    )

    # Relations
    formation = relationship("Formation", back_populates="sessions")
    formateur = relationship("User", back_populates="sessions_animees")
    inscriptions = relationship(
        "Inscription",
        back_populates="session",
        cascade="all, delete-orphan",
    )
