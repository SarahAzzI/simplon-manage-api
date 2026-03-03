from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date, datetime
from typing import Optional
from app.models.user import Role


class UserBase(BaseModel):

    email: EmailStr
    surname: str = Field(min_length=2, max_length=100)
    name: str = Field(min_length=2, max_length=100)
    birth_date: datetime
    role: Role


class UserCreate(UserBase):

    pass


class UserResponse(UserBase):
    id: int
    inscription_date: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):

    surname: Optional[str] = Field(default=None, min_length=2, max_length=100)
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    role: Optional[Role] = None


class UserDelete(BaseModel):
    message: str
    user_id: int
    delete_type: str
