from datetime import date
from sqlalchemy import Integer, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class SessionFormation(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True
    )
    formation_id: Mapped[int] = mapped_column(
        ForeignKey("formations.id", ondelete="CASCADE"),
        nullable=False,
    )
    formateur_id: Mapped[int] = mapped_column(
        ForeignKey("utilisateurs.id", ondelete="CASCADE"),
        nullable=False,
    )
    date_debut: Mapped[date] = mapped_column(
        Date, nullable=False
    )
    date_fin: Mapped[date] = mapped_column(
        Date, nullable=False
    )
    capacite_max: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    # Contraintes au niveau BDD
    __table_args__ = (
        CheckConstraint(
            "date_fin > date_debut",
            name="check_dates_coherentes",
        ),
        CheckConstraint(
            "capacite_max >= 1",
            name="check_capacite_positive",
        ),
    )

    # ── Relations ──
    formation = relationship(
        "Formation",
        back_populates="sessions",
    )
    formateur = relationship(
        "Utilisateur",
        back_populates="sessions_animees",
    )
    inscriptions = relationship(
        "Inscription",
        back_populates="session",
        cascade="all, delete-orphan",
    )