from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional
from models.user import Role


class UserBase(BaseModel):

    email: EmailStr
    surname: str = Field(min_length=2, max_length=100)
    name: str = Field(min_length=2, max_length=100)
    birth_date: datetime
    role: Role


class UserCreate(UserBase):
   
    pass


class UserRead(UserBase):
    id: int
    inscription_date: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    surname: str | None = Field(default=None, min_length=2, max_length=100)
    name: str | None = Field(default=None, min_length=2, max_length=100)
    birth_date: datetime | None = None
    role: Role | None = None
    is_active: bool | None = None


class UserDelete(BaseModel):
    message: str
    user_id: int
    delete_type: str