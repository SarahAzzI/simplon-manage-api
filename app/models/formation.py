from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
from sqlalchemy import Enum as SAEnum
from enum import Enum

class Niveau(str, Enum):
    debutant = "débutant"
    intermédiaire = "intermédiaire"
    avancé = "avancé"

class Formation(Base):
    __tablename__ = "formation"

    id = Column(Integer, primary_key=True)
    titre = Column(String, index=True, nullable=True)
    description = Column(String, nullable=True)
    duree = Column(Integer)
    niveau = Column(SAEnum(Niveau))
