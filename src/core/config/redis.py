import asyncio

from redis.asyncio import Redis

from .settings import settings

redis_client: Redis | None = None


async def init_redis(retries: int = 5, delay: int = 2) -> None:
    global redis_client

    for attempt in range(1, retries + 1):
        try:
            redis_client = Redis.from_url(
                settings.APP_REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
            await redis_client.ping()
            return
        except Exception:
            if attempt < retries:
                await asyncio.sleep(delay)
            else:
                raise


async def close_redis() -> None:
    if redis_client:
        await redis_client.close()


def get_redis() -> Redis:
    if not redis_client:
        raise RuntimeError("Redis client is not initialized")
    return redis_client
