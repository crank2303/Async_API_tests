import aioredis
import pytest
from aioredis import Redis

from tests.functional.settings import settings


@pytest.fixture(scope='session')
async def redis_client() -> Redis:
    redis = await aioredis.create_redis(f"{settings.REDIS_PROTOCOL}://{settings.REDIS_HOST}")
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.fixture
def get_redis(redis_client: Redis):
    async def inner(ids: str) -> str:
        value = await redis_client.get(ids)
        return value
    return inner


@pytest.fixture
async def clear_cache(redis_client: Redis):
    async def inner() -> None:
        await redis_client.flushall(async_op=True)
    return inner
