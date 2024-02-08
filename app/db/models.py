import datetime
from enum import StrEnum
from typing import Annotated

from fastapi import HTTPException, status
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.db.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
# created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
# updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]


class Roles(StrEnum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    USER = "user"


class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Roles] = mapped_column(default=Roles.USER)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @validates('username')
    def validate_name(self, key, value):
        # Custom validation logic
        min_length = 3
        max_length = 50
        if not min_length <= len(value) <= max_length:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username must be between {min_length} and {max_length} characters.",
            )
        return value

    @validates('password')
    def validate_name(self, key, value):
        # Custom validation logic
        min_length = 3
        if not min_length <= len(value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password must be min {min_length} characters.",
            )
        return value