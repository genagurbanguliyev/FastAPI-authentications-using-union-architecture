from sqlalchemy import select

from app.db.database import db
from app.db.models import Users
from app.repository.base_repo import BaseRepo


class UsersRepo(BaseRepo):
    model = Users

    @staticmethod
    async def find_by_username(username: str):
        # query = text(f"SELECT id, username, password, role FROM users WHERE username='{username}'")
        query = select(Users).where(Users.username == username)
        return (await db.execute(query)).scalar_one_or_none()