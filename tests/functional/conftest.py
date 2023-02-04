import aiohttp
import aioredis
import pytest
import json
import asyncio

from typing import List

from aiohttp.client import ClientSession
from elasticsearch import AsyncElasticsearch

from tests.functional.testdata.search_persons import get_persons_es_data, get_film_es_data





@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='127.0.0.1:9200') # TODO сделать привязку к переменной окружения
    yield client
    #TODO подумать как сделать красивее
    if await client.indices.exists(index='movies'):
       await client.indices.delete(index='movies')
    if await client.indices.exists(index='persons'):
       await client.indices.delete(index='persons')
    await client.close()


@pytest.fixture(scope='session')
async def aio_client():
    client = aiohttp.ClientSession()
    yield client
    await client.close()


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(_index: str, data: List[dict]):
        bulk_query = get_query_data(_index, data)
        str_query = '\n'.join(bulk_query) + '\n'

        response = await es_client.bulk(str_query, refresh=True)

        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner

@pytest.fixture
def es_drop_record(es_client:AsyncElasticsearch):
    async def inner(_index:str, id):
        response = await es_client.delete(index=_index, id=id)

        if response['errors']:
            raise Exception('Ошибка удаления данных в Elasticsearch')
    return inner
        

def get_query_data(_index: str, data: List[dict]):
    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps({'index':{'_index':_index, 
            '_id':str(row['id'])}}),
            json.dumps(row)
        ])
    return bulk_query


@pytest.fixture
def make_get_request(aio_client:ClientSession):
    async def inner(url, query_data):
        resp_dict = dict()
        async with aio_client.get(url, params=query_data) as response:
            resp_dict['body'] = await response.json()
            resp_dict['headers'] = response.headers
            resp_dict['status'] = response.status
        return resp_dict
    return inner

@pytest.fixture(autouse=True)
async def fill_data(es_write_data):
    index_dict = {
        'movies': get_film_es_data(),
        'persons': get_persons_es_data()
    }
    for _index, data in index_dict.items():
        await es_write_data(_index, data)

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
