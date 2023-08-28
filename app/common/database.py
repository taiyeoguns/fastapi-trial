from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine

from config import CONFIG

ENGINE = AsyncEngine(create_engine(CONFIG.DATABASE_URL, echo=True, future=True))
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=ENGINE, class_=AsyncSession
)


async def get_session():
    async with SessionLocal() as session:
        yield session
