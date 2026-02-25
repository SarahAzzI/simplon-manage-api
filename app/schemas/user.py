from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class UserCreate(BaseModel):
    email: EmailStr
    surname: str
    name: str
    birth_date: datetime
    role: str
    
    

class UserRead(BaseModel):
    id: int
    email: EmailStr
    surname: str
    name: str
    birth_date: datetime
    role: str
    inscription_date: datetime
    is_active: bool

    class Config:
        from_attributes = True 


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    surname: str | None = None
    name: str | None = None
    birth_date: datetime | None = None
    role: str | None = None
    is_active: bool | None = None


class UserDelete(BaseModel):
    message: str
    user_id: int
    delete_type: str
    