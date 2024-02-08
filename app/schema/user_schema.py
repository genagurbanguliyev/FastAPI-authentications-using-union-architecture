from typing import Optional
from pydantic import BaseModel, Field

from app.db.models import Roles


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=1, description="Username cannot be empty")
    password: str = Field(..., min_length=3, description="Username cannot be empty")


class RegisterSchema(UserBaseSchema):
    role: Optional[Roles] = Field(default="user")


class UserInfoSchema(UserBaseSchema):
    id: int
    role: Roles