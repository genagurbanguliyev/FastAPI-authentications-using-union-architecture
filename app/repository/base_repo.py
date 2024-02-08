from typing import TypeVar, Generic
from sqlalchemy import delete as sql_delete
from sqlalchemy.future import select

from app.db.database import commit_rollback
from app.db.database import db

T = TypeVar('T')


class BaseRepo:
    model = Generic[T]

    @classmethod
    async def create(cls, **kwargs):
        model = cls.model(**kwargs)
        db.add(model)
        await commit_rollback()
        return model

    @classmethod
    async def get_all(cls):
        query = select(cls.model)
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def delete(cls, model_id: str):
        query = sql_delete(cls.model).where(cls.model.id == model_id)
        await db.execute(query)
        await commit_rollback()