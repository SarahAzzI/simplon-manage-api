from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db.database import Base
from sqlalchemy import Enum as SAEnum
from enum import Enum


class Inscritpion():

    __table__ = "inscritpion"

    id = Column(Integer, primary_key=True, nullable=False)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    capacitée_max = Column(Integer, nullable=False)
