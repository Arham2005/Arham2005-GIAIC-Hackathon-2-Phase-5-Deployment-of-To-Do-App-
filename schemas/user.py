from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    email: str
    password: str


class UserRead(UserBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str