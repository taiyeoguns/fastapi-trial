from datetime import datetime
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column
from sqlalchemy_utils import UUIDType

from config import CONFIG

ENGINE = create_async_engine(CONFIG.DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    pass


class BaseDbModel(Base):
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    uuid: Mapped[UUID] = mapped_column(
        UUIDType(), unique=True, index=True, nullable=False, default_factory=uuid4
    )
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    __abstract__ = True


async def get_session():
    async with SessionLocal() as session:
        yield session
