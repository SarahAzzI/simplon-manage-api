from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
from sqlalchemy import Enum as SAEnum
from enum import Enum

class Niveau(str, Enum):
    beginner = "débutant"
    intermediate = "intermédiaire"
    advance = "avancé"

class Formation(Base):
    __tablename__ = "formations"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    level = Column(SAEnum(Niveau), nullable=False)
