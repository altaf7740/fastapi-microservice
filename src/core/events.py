from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config.database import Base, engine
from .config.redis import close_redis, init_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(lambda conn: Base.metadata.create_all(conn))
    await init_redis()
    yield
    await close_redis()
    await engine.dispose()
