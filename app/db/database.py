import asyncio

import trio
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from app.config import settings

# declarative Base class
Base = declarative_base()

# Async engine
engine = create_async_engine(url=settings.DATABASE_URL, future=True, echo=True)

# Session
SessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False, future=True)


@asynccontextmanager
async def get_db_session() -> AsyncSession:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class AsyncDatabaseSession:

    def __init__(self) -> None:
        self.session = None
        self.engine = None

    def __getattr__(self, name):
        return getattr(self.session, name)

    def init(self):
        self.engine = engine
        self.session = SessionLocal()


db = AsyncDatabaseSession()


async def commit_rollback():
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise


async def first_connection():
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        # res = asyncio.run(conn.execute(text("SELECT VERSION()")))
        print(f"{res.first()[0]}")
        # await conn.close()