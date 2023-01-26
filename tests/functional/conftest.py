import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator, Callable

import aiohttp
import pytest_asyncio
from aioredis import Redis, create_redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from multidict import CIMultiDictProxy

from settings import settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture(scope='function')
async def es_client() -> AsyncGenerator[AsyncElasticsearch, None]:
    client = AsyncElasticsearch(hosts=f"{settings.es_url}", verify_certs=True)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='function')
async def redis_client() -> AsyncGenerator[Redis, None]:
    redis = await create_redis(address=f"redis://{settings.redis_url}")
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest_asyncio.fixture(scope='function')
async def session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
def clear_cache(redis_client: Redis):
    async def inner() -> None:
        await redis_client.flushall(async_op=True)
    return inner


@pytest_asyncio.fixture
def send_data_to_elastic(es_client: AsyncElasticsearch, clear_cache: Callable):
    @asynccontextmanager
    async def inner(data: list[dict], with_clear_cache: bool = True)\
            -> AsyncGenerator[None, None]:
        await async_bulk(client=es_client, actions=data)
        await asyncio.sleep(1.5)
        try:
            yield
        finally:
            data_to_delete = (
                dict({'_op_type': 'delete'}, **doc) for doc in data
            )
            await async_bulk(client=es_client, actions=data_to_delete)
            if with_clear_cache:
                await clear_cache()
    return inner


@pytest_asyncio.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f'{settings.service_url}{method}'
        async with session.get(url, params=params) as response:
            return HTTPResponse(
              body=await response.json(),
              headers=response.headers,
              status=response.status,
            )
    return inner
