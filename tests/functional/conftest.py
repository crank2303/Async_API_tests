import asyncio
import aioredis
import json
from typing import List

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='http://127.0.0.1:9200/',
                                validate_cert=False,
                                use_ssl=False)
    yield client
    await client.close()


@pytest.fixture(scope='session', autouse=True)
async def es_delete_index():
    client = AsyncElasticsearch(hosts='http://127.0.0.1:9200/',
                                validate_cert=False,
                                use_ssl=False)
    yield client
    await client.indices.delete(index='movies')
    await client.indices.delete(index='genres')
    await client.indices.delete(index='persons')
    
    
@pytest.fixture()
def es_create_index(es_client):
    async def inner(name_of_index: str, index_body: dict):
        await es_client.indices.create(index=name_of_index, body=index_body)
    return inner


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: List[dict], index: str):
        bulk_query = []
        for row in data:
            bulk_query.extend([
                json.dumps({'index': {'_index': index, '_id': row['id']}}),
                json.dumps(row)
            ])
        str_query = '\n'.join(bulk_query) + '\n'
        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture(scope='session')
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(aiohttp_session):
    async def inner(url, params):
        resp_dict = dict()
        async with aiohttp_session.get(url, params=params) as response:
            resp_dict['body'] = await response.json()
            resp_dict['headers'] = response.headers
            resp_dict['status'] = response.status
        return resp_dict
    return inner


@pytest.fixture(scope='session')
async def redis_client():
    redis = await aioredis.create_redis(f"redis://localhost")
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.fixture
def clear_cache(redis_client):
    async def inner() -> None:
        await redis_client.flushall(async_op=True)
    return inner


@pytest.fixture
def get_redis(redis_client):
    async def inner(ids):
        value = await redis_client.get(ids)
        return value
    return inner
