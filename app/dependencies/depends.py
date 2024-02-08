from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session

db_dependency = Annotated[AsyncSession, Depends(get_db_session)]

# user_dependency: dict = Depends(get_current_user)