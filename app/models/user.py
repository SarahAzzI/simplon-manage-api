from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
from sqlalchemy import Enum as SAEnum
from enum import Enum
from datetime import datetime

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
    inscription_date = Column(DateTime, default=datetime.utcnow)
    