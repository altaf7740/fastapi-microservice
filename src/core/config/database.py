from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .settings import settings

engine = create_async_engine(settings.APP_DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False, class_=AsyncSession, autocommit=False
)


class Base(DeclarativeBase):
    pass
