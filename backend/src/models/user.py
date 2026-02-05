from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str


class User(UserBase):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None