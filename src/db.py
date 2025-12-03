from collections.abc import AsyncGenerator
from datetime import datetime
import uuid

from fastapi import Depends
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

# Async SQLite DB URL
DATABASE_URL = "sqlite+aiosqlite:///./test.db"


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


class User(Base, SQLAlchemyBaseUserTableUUID):
    """
    User model from fastapi-users with UUID primary key.
    __tablename__ is "user" by default in SQLAlchemyBaseUserTableUUID.
    """

    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    # Using PostgreSQL UUID type; SQLite will still accept it as a generic type name.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    caption = Column(String, nullable=False)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts")


# Async engine and session factory
engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables() -> None:
    """
    Create all tables based on the current models.
    Only creates missing tables; does not alter existing ones.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an AsyncSession.
    """
    async with async_session_maker() as session:
        yield session


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    """
    Dependency for fastapi-users user database.
    """
    yield SQLAlchemyUserDatabase(session, User)
