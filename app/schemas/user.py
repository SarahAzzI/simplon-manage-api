from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from datetime import date, datetime
from typing import Optional
from app.core.role import Role

class UserBase(BaseModel):
    email: EmailStr
    surname: str = Field(min_length=2, max_length=100)
    name: str = Field(min_length=2, max_length=100)
    birth_date: date
    role: Role

    @field_validator('birth_date', mode='before')
    @classmethod
    def parse_birth_date(cls, v):
        if isinstance(v, datetime):
            return v.date()
        return v

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    inscription_date: date
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

    @field_validator('inscription_date', mode='before')
    @classmethod
    def parse_inscription_date(cls, v):
        if isinstance(v, datetime):
            return v.date()
        return v

class UserUpdate(BaseModel):
    surname: Optional[str] = Field(default=None, min_length=2, max_length=100)
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    role: Optional[Role] = None

class UserDelete(BaseModel):
    message: str
    user_id: int
    delete_type: str